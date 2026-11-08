import os
from netlist_tools import add_stress
from sweep import run_sweep
from run_sim import INV_X2

SRC = os.path.expanduser("~/sky130_cell_library/magic_layout/inv_x2/inv_x2_pex.spice")
DST = os.path.expanduser("~/sky130_cell_library/harness/inv_x2_pex_sa.spice")

add_stress(SRC, DST)
run_sweep(INV_X2, "inv_x2_pex_tables.json")