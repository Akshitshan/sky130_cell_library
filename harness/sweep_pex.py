import os
from netlist_tools import add_stress
from sweep import run_sweep
from run_sim import OURS_PEX

SRC = os.path.expanduser("~/sky130_cell_library/magic_layout/inverter/inverter_pex.spice")
DST = os.path.expanduser("~/sky130_cell_library/harness/inverter_pex_sa.spice")

add_stress(SRC, DST)
run_sweep(OURS_PEX, "inv_x1_pex_tables.json")