import os
import sweep
from compare_cells import lib_tables, compare
from run_sim import FOUNDRY_NAND2_A, FOUNDRY_NAND2_B, FOUNDRY_NOR2_A, FOUNDRY_NOR2_B

H = os.path.expanduser("~/sky130_cell_library/harness")

# (sa, sb) in um from the hd .mag layouts: NMOS and PMOS separately
STRESS = {
    "foundry_nand2_1": {"nfet": (0.26, 0.68), "pfet": (0.26, 0.68)},
    "foundry_nor2_1": {"nfet": (0.26, 0.68), "pfet": (0.26, 0.62)},
}

for stem, d in STRESS.items():
    out = []
    for line in open(f"{H}/{stem}.spice"):
        if line.startswith("X"):
            sa, sb = d["pfet" if "pfet" in line else "nfet"]
            line = line.rstrip("\n") + f" sa={sa:.4f} sb={sb:.4f}\n"
            print(stem, line.strip())
        out.append(line)
    open(f"{H}/{stem}_sa.spice", "w").writelines(out)


def sa_version(rec, stem):
    r = dict(rec)
    r["file"] = f"{H}/{stem}_sa.spice"
    return r


JOBS = [
    ("nand2_1", "A", sa_version(FOUNDRY_NAND2_A, "foundry_nand2_1"), "foundry_nand2_A_sa_grid.json"),
    ("nand2_1", "B", sa_version(FOUNDRY_NAND2_B, "foundry_nand2_1"), "foundry_nand2_B_sa_grid.json"),
    ("nor2_1", "A", sa_version(FOUNDRY_NOR2_A, "foundry_nor2_1"), "foundry_nor2_A_sa_grid.json"),
    ("nor2_1", "B", sa_version(FOUNDRY_NOR2_B, "foundry_nor2_1"), "foundry_nor2_B_sa_grid.json"),
]

for cell, pin, rec, outfile in JOBS:
    ax = lib_tables(cell, pin)
    sweep.slews_ns = ax["index_1"]
    sweep.loads_pF = ax["index_2"]
    sweep.run_sweep(rec, outfile)

for cell, pin, rec, outfile in JOBS:
    compare(cell, pin, outfile)