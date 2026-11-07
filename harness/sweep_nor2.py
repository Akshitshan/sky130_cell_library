import os
from netlist_tools import add_stress
from sweep import run_sweep
from run_sim import NOR2_A, NOR2_B

SRC = os.path.expanduser("~/sky130_cell_library/magic_layout/nor2/nor2_pex.spice")
DST = os.path.expanduser("~/sky130_cell_library/harness/nor2_pex_sa.spice")

add_stress(SRC, DST)
run_sweep(NOR2_A, "nor2_A_pex_tables.json")
run_sweep(NOR2_B, "nor2_B_pex_tables.json")