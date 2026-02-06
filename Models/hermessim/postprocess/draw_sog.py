#!/usr/bin/env python3
"""
Draw the SOG (Semantics‐Oriented Graph) from a JSON file, filter out "literal" nodes (L(…)),
merge by label, collapse multiple edges, and produce an SVG using rectangles for nodes with
larger fonts and better organization. Node labels are completely stripped of any numbers
and parenthesized content. Uses hierarchical layout for better space efficiency.

Usage:
    python draw_sog.py path/to/input.json
"""

import sys
import json
import os
import re
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np


def find_key_recursive(obj, target_key):
    """
    Recursively search a nested dict/list structure for the first occurrence of
    `target_key`. Return its value (which must be a dict) or raise KeyError if not found.
    """
    if isinstance(obj, dict):
        if target_key in obj and isinstance(obj[target_key], dict):
            return obj[target_key]
        for v in obj.values():
            try:
                return find_key_recursive(v, target_key)
            except KeyError:
                pass

    elif isinstance(obj, list):
        for item in obj:
            try:
                return find_key_recursive(item, target_key)
            except KeyError:
                pass

    raise KeyError(f"Could not find key '{target_key}' in the JSON.")


def strip_all_numbers_and_parens(label):
    """
    Strip away any numbers, parentheses, and content inside parentheses from the label.
    Also remove any trailing/leading underscores or special characters.
    E.g. "REG(20, 8)" -> "REG", "MEM(1090, 8)" -> "MEM", "ISUB10" -> "ISUB", etc.
    """
    # Remove parentheses and everything inside them
    label = re.sub(r"\([^)]*\)", "", label)
    
    # Remove all digits more aggressively - including those at the end
    label = re.sub(r"\d+", "", label)
    
    # Remove trailing/leading underscores, whitespace, and special characters
    label = re.sub(r"[_\s\d]+", "", label).strip()
    
    # Additional cleanup for common patterns
    label = re.sub(r"[0-9]+", "", label)  # Extra digit removal
    
    # Special handling for common assembly instruction patterns
    # Remove single letters that are typically numeric suffixes
    if len(label) <= 2 and label in ['SD', 'BR', 'R', 'D', 'B', 'S']:
        return "NODE"
    
    # If label becomes empty or too short, return a placeholder
    if not label or len(label) < 2:
        return "NODE"
    
    return label


def get_hierarchical_layout(G):
    """
    Create a hierarchical layout that's more space-efficient than Kamada-Kawai.
    Attempts to create layers based on node connectivity and importance.
    """
    if len(G.nodes()) == 0:
        return {}
    
    # Try to use graphviz layout if available, otherwise fall back to spring layout
    try:
        # Use dot layout for hierarchical structure
        pos = nx.nx_agraph.graphviz_layout(G, prog='dot')
    except:
        try:
            # Fall back to spring layout with better parameters
            pos = nx.spring_layout(G, k=3, iterations=100, seed=42)
        except:
            # Final fallback to circular layout
            pos = nx.circular_layout(G)
    
    return pos


def optimize_node_positions(pos, min_distance=0.25):
    """
    Adjust node positions to ensure minimum distance between nodes
    for better readability and to prevent overlapping. Increased distance for larger rectangles.
    """
    positions = np.array(list(pos.values()))
    nodes = list(pos.keys())
    
    # Scale down all positions for more compactness
    positions = positions * 0.7
    
    # Iteratively adjust positions to maintain minimum distance
    for _ in range(40):  # More iterations for larger rectangles
        adjusted = False
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                dist = np.linalg.norm(positions[i] - positions[j])
                if dist < min_distance:
                    # Move nodes apart
                    direction = positions[i] - positions[j]
                    if np.linalg.norm(direction) > 0:
                        direction = direction / np.linalg.norm(direction)
                        move = direction * (min_distance - dist) / 2
                        positions[i] += move
                        positions[j] -= move
                        adjusted = True
        
        if not adjusted:
            break
    
    # Update positions dictionary
    for i, node in enumerate(nodes):
        pos[node] = positions[i]
    
    return pos


def build_and_save_sog_rectangles_large(sog_dict, output_svg_path):
    """
    Build a directed graph where we exclude nodes whose labels start with "L(",
    merge the remaining nodes by label, collapse multiple edges, and save as a large,
    readable SVG using hierarchical layout, rectangles for nodes, and larger fonts.
    Node labels have all numbers and parenthesized content removed.
    """
    nodes = sog_dict.get("nodes", [])
    nverbs = sog_dict.get("nverbs", {})
    edges = sog_dict.get("edges", [])

    # 1) Map each node ID → its label (string). Fallback to str(node_id) if missing.
    #    Then strip any numbers and parentheses from that label.
    label_by_id = {}
    for node_id in nodes:
        raw_label = str(node_id)
        if (
            str(node_id) in nverbs
            and isinstance(nverbs[str(node_id)], list)
            and len(nverbs[str(node_id)]) > 0
        ):
            raw_label = nverbs[str(node_id)][0]
        # Now remove any numbers and parentheses
        clean_label = strip_all_numbers_and_parens(raw_label)
        label_by_id[node_id] = clean_label

    # 2) Determine which node‐IDs to keep: exclude those with label starting "L" and "END"
    keep_ids = {nid for nid, lbl in label_by_id.items() 
                if not lbl.startswith("L") and lbl != "END"}

    # 3) Build a new DiGraph H where nodes = unique labels of kept IDs
    H = nx.DiGraph()
    unique_labels = {label_by_id[nid] for nid in keep_ids}
    H.add_nodes_from(unique_labels)

    # 4) For each edge (u,v,w), if both u and v are kept, add/collapse in H
    for triple in edges:
        if len(triple) < 2:
            continue
        u, v = triple[0], triple[1]
        if u not in keep_ids or v not in keep_ids:
            continue
        lu = label_by_id[u]
        lv = label_by_id[v]
        if H.has_edge(lu, lv):
            H[lu][lv]["count"] += 1
        else:
            H.add_edge(lu, lv, count=1)

    if len(H.nodes()) == 0:
        print("No nodes to display after filtering.")
        return

    # 5) Draw H: use hierarchical layout for better organization
    plt.figure(figsize=(16, 12))  # More compact size
    
    # Get hierarchical layout
    pos = get_hierarchical_layout(H)
    
    # Optimize positions to prevent overlapping with larger minimum distance for bigger rectangles
    pos = optimize_node_positions(pos, min_distance=0.25)

    # Draw edges first (so they appear behind nodes)
    nx.draw_networkx_edges(
        H,
        pos,
        arrowstyle="->",
        arrowsize=30,
        width=3,
        edge_color="#666666",
        alpha=0.7,
        connectionstyle="arc3,rad=0.1"  # Slight curve for better visibility
    )

    # Draw nodes as rectangles with better styling
    ax = plt.gca()
    node_colors = ["#E8F4FD", "#FFF2CC", "#E1D5E7", "#D5E8D4", "#FFE6CC"]  # Variety of light colors
    
    for i, (n, (x, y)) in enumerate(pos.items()):
        # Calculate rectangle size based on text length - made larger
        text_len = len(n)
        w = max(0.18, text_len * 0.035)  # Much larger width
        h = 0.12  # Much larger height
        
        # Choose color based on node type or use cycling colors
        color = node_colors[i % len(node_colors)]
        
        rect = Rectangle(
            (x - w/2, y - h/2),
            w,
            h,
            facecolor=color,
            edgecolor="#333333",
            linewidth=2.5,  # Thicker border for larger rectangles
            alpha=0.9
        )
        ax.add_patch(rect)

    # Ensure aspect is equal for proper rectangle shape
    ax.set_aspect('equal')

    # Draw node labels inside each rectangle with larger, cleaner font
    for n, (x, y) in pos.items():
        plt.text(
            x,
            y,
            n,
            horizontalalignment="center",
            verticalalignment="center",
            fontsize=22,  # Much larger font size
            fontweight="bold",
            fontfamily="sans-serif",
            color="#333333"
        )

    # Draw edge‐count labels for edges where count > 1
    edge_labels = {
        (u, v): str(data["count"])
        for u, v, data in H.edges(data=True)
        if data.get("count", 1) > 1
    }
    if edge_labels:
        nx.draw_networkx_edge_labels(
            H,
            pos,
            edge_labels=edge_labels,
            font_size=16,  # Larger edge labels
            font_color="#666666",
            bbox=dict(boxstyle="round,pad=0.2", facecolor="white", alpha=0.8)
        )

    # Remove title
    plt.axis("off")
    plt.tight_layout()

    # Save as SVG with high DPI
    plt.savefig(output_svg_path, format="svg", dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved improved SOG graph as SVG to: {output_svg_path}")


def main():
    if len(sys.argv) != 2:
        print("Usage: python draw_sog.py path/to/input.json")
        sys.exit(1)

    json_path = sys.argv[1]
    try:
        with open(json_path, "r") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        sys.exit(1)

    try:
        sog_block = find_key_recursive(data, "SOG")
    except KeyError as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Save SVG alongside this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_svg_path = os.path.join(script_dir, "sog.svg")

    build_and_save_sog_rectangles_large(sog_block, output_svg_path)


if __name__ == "__main__":
    main()