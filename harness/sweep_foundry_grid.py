import json
import sweep
from compare_cells import lib_tables
from run_sim import FOUNDRY_NAND2_A, FOUNDRY_NAND2_B, FOUNDRY_NOR2_A, FOUNDRY_NOR2_B

JOBS = [
    ("nand2_1", "A", FOUNDRY_NAND2_A, "foundry_nand2_A"),
    ("nand2_1", "B", FOUNDRY_NAND2_B, "foundry_nand2_B"),
    ("nor2_1", "A", FOUNDRY_NOR2_A, "foundry_nor2_A"),
    ("nor2_1", "B", FOUNDRY_NOR2_B, "foundry_nor2_B"),
]

for cell, pin, rec, stem in JOBS:
    ax = lib_tables(cell, pin)
    sweep.slews_ns = ax["index_1"]      # the cell's own slew axis from the .lib
    sweep.loads_pF = ax["index_2"]      # the cell's own load axis from the .lib
    sweep.run_sweep(rec, stem + "_grid.json")
    print(stem, "done")