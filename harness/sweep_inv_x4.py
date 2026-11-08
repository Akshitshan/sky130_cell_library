import os
from netlist_tools import add_stress
from sweep import run_sweep
from run_sim import INV_X4

SRC = os.path.expanduser("~/sky130_cell_library/magic_layout/inv_x4/inv_x4_pex.spice")
DST = os.path.expanduser("~/sky130_cell_library/harness/inv_x4_pex_sa.spice")

add_stress(SRC, DST)
run_sweep(INV_X4, "inv_x4_pex_tables.json")