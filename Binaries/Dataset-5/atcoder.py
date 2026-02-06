#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from argparse import ArgumentParser
from html import unescape
import http.cookiejar
import logging
import os
import re
import sys
import time
import json
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode

import requests
from lxml import html

log = logging.getLogger()

# ---------- Config ----------
from pathlib import Path

# ---------- Paths ----------
SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_DEBUG_DUMP_DIR = SCRIPT_DIR / "_debug_dump"
DEFAULT_COOKIES_PATH = SCRIPT_DIR / "cookies.txt"   # 你可以把 cookies.txt 放这儿

# ---------- Config ----------
DEBUG_DUMP_DIR = os.getenv("ATCODER_DEBUG_DUMP_DIR", str(DEFAULT_DEBUG_DUMP_DIR))
SUB_LINK_RE = re.compile(r"/contests/[^/]+/submissions/\d+$")


# ---------- Session ----------
session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:118.0) Gecko/20100101 Firefox/118.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
})

# ---------- Logging ----------
def init_logging(level: int):
    log.setLevel(level)
    h = logging.StreamHandler()
    h.setFormatter(logging.Formatter("%(levelname)7s | %(asctime)15s | %(message)s"))
    log.addHandler(h)

# ---------- Helpers ----------
def load_cookies_from_file(path: str):
    """Load Netscape cookies.txt into the global requests session."""
    cj = http.cookiejar.MozillaCookieJar()
    cj.load(path, ignore_discard=True, ignore_expires=True)
    for c in cj:
        session.cookies.set_cookie(c)
    log.info("Loaded %d cookies from %s", len(cj), path)

def _normalize_results_url(url: str) -> str:
    """Remove empty f.User= (causes empty result sets)."""
    sp = urlsplit(url)
    q = list(parse_qsl(sp.query, keep_blank_values=True))
    q = [(k, v) for (k, v) in q if not (k == "f.User" and v == "")]
    return urlunsplit((sp.scheme, sp.netloc, sp.path, urlencode(q, doseq=True), sp.fragment))

def _with_params(url: str, extra_params: dict) -> str:
    sp = urlsplit(url)
    q = dict(parse_qsl(sp.query, keep_blank_values=True))
    q.update(extra_params)
    return urlunsplit((sp.scheme, sp.netloc, sp.path, urlencode(q, doseq=True), sp.fragment))

def _parse_rows_from_dom(dom):
    """Parse table or fragment rows into [task_name, submission_url]."""
    rows = dom.xpath("//table//tbody/tr")
    if not rows:
        rows = dom.xpath("//tr[td]")
    out = []
    for row in rows:
        tds = row.xpath("./td")
        if len(tds) < 2:
            continue
        task_name = tds[1].text_content().strip()
        link = tds[-1].xpath(".//a[@href]/@href")
        if not link:
            # fallback: any submission link in the row
            link = [h for h in row.xpath(".//a[@href]/@href") if SUB_LINK_RE.search(h)]
        if not link:
            continue
        href = link[0]
        sub_url = "https://atcoder.jp" + href if href.startswith("/") else href
        out.append([task_name, sub_url])
    return out

def _parse_any_detail_links(dom):
    """Fallback: find any submission detail link anywhere; infer task if possible."""
    out = []
    for a in dom.xpath("//a[@href]"):
        href = a.get("href") or ""
        if not SUB_LINK_RE.search(href):
            continue
        tr = a
        while tr is not None and tr.tag.lower() != "tr":
            tr = tr.getparent()
        task_name = "UNKNOWN_TASK"
        if tr is not None:
            tds = tr.xpath("./td")
            if len(tds) >= 2:
                task_name = tds[1].text_content().strip()
        sub_url = "https://atcoder.jp" + href if href.startswith("/") else href
        out.append([task_name, sub_url])
    # de-dup preserve order
    seen, uniq = set(), []
    for t,u in out:
        if u in seen: continue
        seen.add(u); uniq.append([t,u])
    return uniq

def _find_next_from_dom(dom):
    hrefs = dom.xpath("//a[@rel='next']/@href")
    if not hrefs:
        hrefs = dom.xpath("//ul[contains(@class,'pagination')]//a[contains(., 'Next')]/@href")
    if not hrefs:
        return None
    href = hrefs[0]
    return "https://atcoder.jp" + href if href.startswith("/") else href

def _dump_html(page_idx: int, text: str, note: str = ""):
    try:
        os.makedirs(DEBUG_DUMP_DIR, exist_ok=True)
        tag = f"_{note}" if note else ""
        out_path = os.path.join(DEBUG_DUMP_DIR, f"atcoder_page_{page_idx}{tag}.html")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(text)
        log.info("Saved HTML to %s", out_path)
    except Exception as e:
        log.warning("Could not save debug HTML: %s", e)

# ---------- Core ----------
def fetch_submissions(results_url: str):
    """
    Page by ?page=1,2,... ; for each page try HTML first, then JSON fragment (?json=1).
    Stops when a page yields zero rows.
    Returns list of [task_name, submission_detail_url].
    """
    base_url = _normalize_results_url(results_url)
    results = []
    page = 1
    seen_urls = set()

    while True:
        page_url = _with_params(base_url, {"page": str(page)})
        if page_url in seen_urls:
            break
        seen_urls.add(page_url)

        log.debug("Fetching HTML page %d: %s", page, page_url)
        res = session.get(page_url, headers={"Referer": page_url}, allow_redirects=True)
        if res.status_code != 200:
            log.error("Unexpected status code: %d", res.status_code)
            break

        # If bounced to login, stop (cookies likely expired)
        if "Sign In - AtCoder" in res.text or "Please sign in first." in res.text:
            _dump_html(page, res.text, note="redirected_to_login")
            break

        dom = html.fromstring(res.text)
        page_rows = _parse_rows_from_dom(dom)
        if not page_rows:
            page_rows = _parse_any_detail_links(dom)

        # Try JSON/fragment for the same page if HTML yielded nothing
        if not page_rows:
            json_url = _with_params(page_url, {"json": "1"})
            log.debug("No rows from HTML; trying JSON: %s", json_url)
            resj = session.get(json_url, headers={
                "X-Requested-With": "XMLHttpRequest",
                "Referer": page_url,
            })
            if resj.status_code == 200:
                fragment = None
                items = None
                try:
                    j = resj.json()
                    if isinstance(j, dict) and isinstance(j.get("result"), str):
                        fragment = j["result"]
                    else:
                        items = j.get("data") or j.get("items")
                        if items is None and isinstance(j, list):
                            items = j
                except json.JSONDecodeError:
                    fragment = resj.text

                if fragment:
                    dom_frag = html.fromstring(fragment)
                    page_rows = _parse_rows_from_dom(dom_frag) or _parse_any_detail_links(dom_frag)
                elif items:
                    # Best-effort structured JSON (rare)
                    for it in items:
                        task_name = None
                        sub_url = None
                        if isinstance(it, dict):
                            if "task" in it and isinstance(it["task"], str):
                                task_name = it["task"]
                            elif "Task" in it and isinstance(it["Task"], dict):
                                task_name = it["Task"].get("ScreenName") or it["Task"].get("Name")
                            if "url" in it and isinstance(it["url"], str):
                                sub_url = it["url"]
                            elif "Url" in it and isinstance(it["Url"], str):
                                sub_url = it["Url"]
                            elif "Id" in it or "id" in it:
                                sub_id = str(it.get("Id") or it.get("id"))
                                sub_url = f"/contests/UNKNOWN/submissions/{sub_id}"
                        if task_name and sub_url:
                            if sub_url.startswith("/"):
                                sub_url = "https://atcoder.jp" + sub_url
                            page_rows.append([task_name, sub_url])

        # Stop when no rows on this page
        if not page_rows:
            if page == 1:
                _dump_html(page, res.text, note="no_rows_first_page")
            break

        results.extend(page_rows)
        page += 1

    log.info("Fetched %d submissions", len(results))
    return results


# def save_code(output_dir: str, task_name: str, submission_id: str, code: str):
#     os.makedirs(os.path.join(output_dir, task_name), exist_ok=True)
#     sub_fp = os.path.join(output_dir, task_name, f"{submission_id}.c")
#     log.info("Saving: %s", sub_fp)
#     with open(sub_fp, "w", encoding="utf-8") as ofile:
#         ofile.write(code)

def sanitize(name: str) -> str:
    # remove/replace characters that are problematic in filenames
    return re.sub(r'[\\/:*?"<>|]+', '_', name).strip()

def save_code(output_dir: str, task_name: str, submission_id: str, code: str):
    # Flat: save directly under output_dir
    os.makedirs(output_dir, exist_ok=True)
    sub_fp = os.path.join(output_dir, f"{submission_id}.c")
    log.info("Saving: %s", sub_fp)
    with open(sub_fp, "w", encoding="utf-8") as ofile:
        ofile.write(code)


def download_code(task_name: str, url: str, output_dir: str):
    log.debug("Fetching submission: %s", url)
    res = session.get(url)
    if res.status_code != 200:
        log.error("Unexpected status code: %d", res.status_code)
        return
    dom = html.fromstring(res.text)
    sub_id = url.rstrip("/").split("/")[-1]

    code_text = None
    code_nodes = dom.xpath('//pre[@id="submission-code"]')
    if code_nodes:
        code_text = unescape(code_nodes[0].text or "")
    if not code_text:
        code_nodes = dom.xpath('//pre//code')
        if code_nodes:
            code_text = unescape(code_nodes[0].text or "")
    if not code_text:
        log.error("Could not locate code block for submission %s", sub_id)
        return

    save_code(output_dir, task_name, sub_id, code_text)
    time.sleep(1.0)  # be nice

# ---------- CLI ----------
def parse_arguments():
    p = ArgumentParser()
    p.add_argument("-l", "--logging", type=int, default=20, help="Log level [10-50] (default: 20 - Info)")
    p.add_argument(
        "--cookies",
        type=str,
        default=str(DEFAULT_COOKIES_PATH),
        help="Path to Netscape cookies.txt for atcoder.jp (default: ./cookies.txt next to this script)"
    )

    p.add_argument("results_url", type=str, help="AtCoder submissions search URL to scrape")
    p.add_argument("output_directory", type=str, help="Directory to save code into")
    return p.parse_args()

def main():
    opts = parse_arguments()
    init_logging(opts.logging)

    if os.path.exists(opts.output_directory) and not os.path.isdir(opts.output_directory):
        log.error("Output path already exists and is not a directory: %s", opts.output_directory)
        sys.exit(1)

    load_cookies_from_file(opts.cookies)

    subs = fetch_submissions(opts.results_url)
    log.info("Fetched %d submissions", len(subs))

    for task_name, sub_url in subs:
        download_code(task_name, sub_url, opts.output_directory)

if __name__ == "__main__":
    main()
