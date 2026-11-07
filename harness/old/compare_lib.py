import os
import re
import json

LIBFILE = os.path.expandvars("$PDK_ROOT/sky130A/libs.ref/sky130_fd_sc_hd/lib/sky130_fd_sc_hd__tt_025C_1v80.lib")
NAMES = ["cell_fall", "cell_rise", "fall_transition", "rise_transition"]


def read_cell_tables(libfile, cellname):
    text = open(libfile).read()
    start = text.index('cell ("' + cellname + '")')
    end = text.index('cell ("', start + 10)
    block = text[start:end]
    tables = {}
    for name in NAMES:
        m = re.search(r'\b' + name + r'\s*\("[^"]*"\)\s*\{.*?values\((.*?)\);', block, re.S)
        rows = re.findall(r'"([^"]*)"', m.group(1))
        tables[name] = [[float(x) for x in row.split(",")] for row in rows]
    return tables


foundry = read_cell_tables(LIBFILE, "sky130_fd_sc_hd__inv_1")
mine = json.load(open("inv1_foundry_tables.json"))

for name in NAMES:
    print(name, "(harness / foundry)")
    for row_m, row_f in zip(mine[name], foundry[name]):
        print([round(m / f, 2) for m, f in zip(row_m, row_f)])