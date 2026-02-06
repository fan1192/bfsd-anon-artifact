##############################################################################
#                                                                            #
#  Code for the USENIX Security '22 paper:                                   #
#  How Machine Learning Is Solving the Binary Function Similarity Problem.   #
#                                                                            #
#  MIT License                                                               #
#                                                                            #
#  Copyright (c) 2019-2022 Cisco Talos                                       #
#                                                                            #
#  Permission is hereby granted, free of charge, to any person obtaining     #
#  a copy of this software and associated documentation files (the           #
#  "Software"), to deal in the Software without restriction, including       #
#  without limitation the rights to use, copy, modify, merge, publish,       #
#  distribute, sublicense, and/or sell copies of the Software, and to        #
#  permit persons to whom the Software is furnished to do so, subject to     #
#  the following conditions:                                                 #
#                                                                            #
#  The above copyright notice and this permission notice shall be            #
#  included in all copies or substantial portions of the Software.           #
#                                                                            #
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,           #
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF        #
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND                     #
#  NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE    #
#  LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION    #
#  OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION     #
#  WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.           #
#                                                                            #
#  IDA_flowchart.py - Extract BBs info using IDA's FlowChart APIs.           #
#                                                                            #
##############################################################################

import hashlib
import idaapi
import idautils
import idc
import os
import time
import ida_pro

from collections import namedtuple

COLUMNS = [
    'idb_path',
    'fva',
    'func_name',
    'start_ea',
    'end_ea',
    'bb_num',
    'bb_list',
    'hashopcodes']

BasicBlock = namedtuple('BasicBlock', ['va', 'size'])

def get_basic_blocks(fva):
    bb_list = list()
    func = idaapi.get_func(fva)
    if func is None:
        return bb_list

    for bb in idaapi.FlowChart(func):
        bb_list.append(BasicBlock(
            va=bb.start_ea,
            size=bb.end_ea - bb.start_ea))

    return bb_list

def get_basic_block_opcodes(bb):
    opc_list = list()
    t_va = bb.va
    while t_va < bb.va + bb.size:
        opc_list.append(idaapi.ua_mnem(t_va))
        t_va = idc.next_head(t_va)
    return opc_list

def get_function_hashopcodes(fva):
    opc_list = list()
    bb_list = get_basic_blocks(fva)
    sorted_bb_list = sorted(bb_list)
    for bb in sorted_bb_list:
        opc_list.extend(get_basic_block_opcodes(bb))
    opc_string = ''.join(opc_list)
    opc_string = opc_string.upper()
    hashopcodes = hashlib.sha256(opc_string.encode()).hexdigest()
    return hashopcodes

def analyze_functions(idb_path, output_csv):
    start_time = time.time()
    csv_out = None
    if os.path.isfile(output_csv):
        csv_out = open(output_csv, "a")
    else:
        csv_out = open(output_csv, "w")
        csv_out.write(",".join(COLUMNS) + "\n")

    print("[D] Output CSV: %s" % output_csv)

    function_count = 0
    for c, fva in enumerate(idautils.Functions()):
        try:
            func = idaapi.get_func(fva)
            func_name = idaapi.get_func_name(fva)
            bb_sa_list = list(idaapi.FlowChart(func))

            if len(bb_sa_list) < 5:
                continue

            data = [idb_path,
                    hex(fva).strip("L"),
                    func_name,
                    hex(func.start_ea).strip("L"),
                    hex(func.end_ea).strip("L"),
                    len(bb_sa_list),
                    ';'.join([hex(x.start_ea).strip("L") for x in bb_sa_list]),
                    get_function_hashopcodes(fva)]

            csv_out.write(','.join([str(x) for x in data]) + "\n")
            function_count += 1

        except Exception as e:
            print("[!] Exception: skipping function fva: %d" % fva)
            print(e)

    print("[D] Processing %d functions took: %d seconds" %
          (function_count, time.time() - start_time))

    csv_out.close()

if __name__ == "__main__":
    if not idaapi.get_plugin_options("flowchart"):
        print("[!] -Oflowchart option is missing")
        ida_pro.qexit(0)

    plugin_options = idaapi.get_plugin_options("flowchart").split(':')
    if len(plugin_options) != 2:
        print("[!] -Oflowchart:IDB_PATH:OUTPUT_CSV is required")
        ida_pro.qexit(0)

    idb_path = plugin_options[0]
    output_csv = plugin_options[1]

    print("[D] IDB Path: %s" % idb_path)
    print("[D] Output CSV: %s" % output_csv)

    analyze_functions(idb_path, output_csv)
    ida_pro.qexit(0)

