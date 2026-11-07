import os
from netlist_tools import add_stress
from sweep import run_sweep
from run_sim import NAND2_A, NAND2_B

SRC = os.path.expanduser("~/sky130_cell_library/magic_layout/nand2/nand2_pex.spice")
DST = os.path.expanduser("~/sky130_cell_library/harness/nand2_pex_sa.spice")

add_stress(SRC, DST)
run_sweep(NAND2_A, "nand2_A_pex_tables.json")
run_sweep(NAND2_B, "nand2_B_pex_tables.json")