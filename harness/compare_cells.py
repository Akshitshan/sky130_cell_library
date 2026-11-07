import json
import os
import re

LIB = os.path.expandvars("$PDK_ROOT/sky130A/libs.ref/sky130_fd_sc_hd/lib/sky130_fd_sc_hd__tt_025C_1v80.lib")
KINDS = ("cell_fall", "cell_rise", "fall_transition", "rise_transition")


def lib_tables(cell, pin):
    # find the cell's block, split it into timing () groups, keep the one whose related_pin is `pin`
    text = open(LIB).read()
    start = text.index('cell ("sky130_fd_sc_hd__%s")' % cell)
    nxt = text.find('cell ("', start + 10)
    block = text[start:nxt if nxt != -1 else len(text)]
    parts = block.split("timing () {")[1:]
    if not parts:
        raise RuntimeError("no 'timing () {' groups found in " + cell)
    for part in parts:
        m = re.search(r'related_pin\s*:\s*"(\w+)"', part)
        if not m or m.group(1) != pin:
            continue
        out = {}
        for kind in KINDS:
            t = re.search(kind + r'\s*\("[^"]*"\)\s*\{.*?values\s*\((.*?)\)\s*;', part, re.S)
            nums = [float(x) for x in re.findall(r'-?\d+\.?\d*(?:[eE][-+]?\d+)?', t.group(1))]
            if len(nums) != 49:
                raise RuntimeError("%s %s %s: expected 49 numbers, got %d" % (cell, pin, kind, len(nums)))
            out[kind] = [nums[i * 7:(i + 1) * 7] for i in range(7)]
            out["index_1"] = [float(x) for x in re.search(r'index_1\s*\("([^"]*)"\)', part).group(1).split(",")]
            out["index_2"] = [float(x) for x in re.search(r'index_2\s*\("([^"]*)"\)', part).group(1).split(",")]
        return out
    raise RuntimeError("no timing group with related_pin %s in %s" % (pin, cell))


def compare(cell, pin, jfile):
    lib = lib_tables(cell, pin)
    mine = json.load(open(jfile))
    print("==", cell, "input", pin, " (harness / foundry .lib)")
    for kind in KINDS:
        r = [[mine[kind][i][j] / lib[kind][i][j] for j in range(7)] for i in range(7)]
        flat = [x for row in r for x in row]
        print("%-16s fast-slew/light %.2f  fast/heavy %.2f  slow/light %.2f  slow/heavy %.2f   min %.2f  max %.2f"
              % (kind, r[0][0], r[0][6], r[6][0], r[6][6], min(flat), max(flat)))


if __name__ == "__main__":
    compare("nand2_1", "A", "foundry_nand2_A_grid.json")
    compare("nand2_1", "B", "foundry_nand2_B_grid.json")
    compare("nor2_1", "A", "foundry_nor2_A_grid.json")
    compare("nor2_1", "B", "foundry_nor2_B_grid.json")