import os
import re
import json
from run_sim import simulate, OURS_PEX, FOUNDRY_INV1, NAND2_A, NAND2_B, NOR2_A, NOR2_B, INV_X2, INV_X4

LIBFILE = os.path.expandvars("$PDK_ROOT/sky130A/libs.ref/sky130_fd_sc_hd/lib/sky130_fd_sc_hd__tt_025C_1v80.lib")


def charge(t, i, t_start, t_stop):
    # add up current x time over a window = charge delivered (trapezoid rule)
    q = 0.0
    for k in range(1, len(t)):
        if t_start <= t[k - 1] and t[k] <= t_stop:
            q += (i[k - 1] + i[k]) / 2 * (t[k] - t[k - 1])
    return q


def input_cap_fF(cell):
    # drive the pin with a 0.05 ns edge, measure the charge the source supplies, C = Q / VDD
    simulate(0.05, 1.0, cell)
    t = []
    i = []
    for line in open("wave.txt"):
        cols = line.split()
        t.append(float(cols[0]))
        i.append(float(cols[5]))
    q_rise = charge(t, i, 0.9e-9, 2.0e-9)
    q_fall = charge(t, i, 3.0e-9, 4.0e-9)
    return round(-q_rise / 1.8 * 1e15, 3), round(q_fall / 1.8 * 1e15, 3)


if __name__ == "__main__":
    text = open(LIBFILE).read()
    start = text.index('cell ("sky130_fd_sc_hd__inv_1")')
    end = text.index('cell ("', start + 10)
    print("foundry inv_1 lib (pF):", re.findall(r'\b(\w*capacitance)\s*:\s*([0-9.]+)', text[start:end]))
    print("foundry inv_1 netlist in my harness (fF, rise, fall):", input_cap_fF(FOUNDRY_INV1))

    pins = {
        "inv_x1/A": OURS_PEX,
        "nand2/A": NAND2_A,
        "nand2/B": NAND2_B,
        "nor2/A": NOR2_A,
        "nor2/B": NOR2_B,
        "inv_x2/A": INV_X2,
        "inv_x4/A": INV_X4
    }
    out = {}
    for name, cell in pins.items():
        r, f = input_cap_fF(cell)
        print(name, "(fF, rise edge, fall edge):", r, f)
        out[name] = round((r + f) / 2 / 1000, 6)   # average, in pF (Liberty unit)
    json.dump(out, open("pincaps.json", "w"), indent=1)
    print("saved pincaps.json (pF):", out)