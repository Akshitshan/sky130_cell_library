import os
import subprocess
from measure import read_wave

LIB = os.path.expanduser("~/sky130_cell_library/harness/sky130_min.spice")
OURS = {
    "file": os.path.expanduser("~/sky130_cell_library/lvs/schematic.spice"),
    "inst": "Xdut vin vout vdd 0 inverter",
}
FOUNDRY_INV1 = {
    "file": os.path.expanduser("~/sky130_cell_library/harness/foundry_inv_1.spice"),
    "inst": "Xdut vin 0 0 vdd vdd vout sky130_fd_sc_hd__inv_1",
}
FOUNDRY_INV1_SA = {
    "file": os.path.expanduser("~/sky130_cell_library/harness/foundry_inv_1_sa.spice"),
    "inst": "Xdut vin 0 0 vdd vdd vout sky130_fd_sc_hd__inv_1",
}
OURS_PEX = {
    "file": os.path.expanduser("~/sky130_cell_library/harness/inverter_pex_sa.spice"),
    "inst": "Xdut vdd 0 vout vin inverter",
}
NAND2_A = {
    "file": os.path.expanduser("~/sky130_cell_library/harness/nand2_pex_sa.spice"),
    "inst": "Xdut vin b vdd 0 vout nand2",
    "extra": "VB b 0 1.8",
}
NAND2_B = {
    "file": os.path.expanduser("~/sky130_cell_library/harness/nand2_pex_sa.spice"),
    "inst": "Xdut a vin vdd 0 vout nand2",
    "extra": "VA a 0 1.8",
}
NOR2_A = {
    "file": os.path.expanduser("~/sky130_cell_library/harness/nor2_pex_sa.spice"),
    "inst": "Xdut b vin vout vdd 0 nor2",
    "extra": "VB b 0 0",
}
NOR2_B = {
    "file": os.path.expanduser("~/sky130_cell_library/harness/nor2_pex_sa.spice"),
    "inst": "Xdut vin a vout vdd 0 nor2",
    "extra": "VA a 0 0",
}
FOUNDRY_NAND2_A = {"file": os.path.expanduser("~/sky130_cell_library/harness/foundry_nand2_1.spice"),
                   "inst": "Xdut vin b 0 0 vdd vdd vout sky130_fd_sc_hd__nand2_1", "extra": "VB b 0 1.8"}
FOUNDRY_NAND2_B = {"file": os.path.expanduser("~/sky130_cell_library/harness/foundry_nand2_1.spice"),
                   "inst": "Xdut a vin 0 0 vdd vdd vout sky130_fd_sc_hd__nand2_1", "extra": "VA a 0 1.8"}
FOUNDRY_NOR2_A = {"file": os.path.expanduser("~/sky130_cell_library/harness/foundry_nor2_1.spice"),
                  "inst": "Xdut vin b 0 0 vdd vdd vout sky130_fd_sc_hd__nor2_1", "extra": "VB b 0 0"}
FOUNDRY_NOR2_B = {"file": os.path.expanduser("~/sky130_cell_library/harness/foundry_nor2_1.spice"),
                  "inst": "Xdut a vin 0 0 vdd vdd vout sky130_fd_sc_hd__nor2_1", "extra": "VA a 0 0"}

def simulate(slew_ns, load_fF, cell=OURS):
    tr = slew_ns / 0.6
    width = 2 + 0.04 * load_fF
    tstop = 1 + 2 * tr + 2 * width
    deck = f"""* auto-generated deck
.include {LIB}
.temp 25
.include {cell['file']}
{cell['inst']}
{cell.get('extra', '')}
C1 vout 0 {load_fF}f
V1 vdd 0 1.8
V2 vin 0 pulse(0 1.8 1n {tr:.5f}n {tr:.5f}n {width:.3f}n 100n)
.tran 1p {tstop:.3f}n
.control
run
wrdata wave.txt v(vin) v(vout) i(V2)
.endc
.end
"""
    with open("deck.spice", "w") as f:
        f.write(deck)
    if os.path.exists("wave.txt"):
        os.remove("wave.txt")
    result = subprocess.run(["ngspice", "-b", "deck.spice"], capture_output=True, text=True)
    if not os.path.exists("wave.txt"):
        raise RuntimeError("ngspice failed:\n" + result.stdout[-2000:] + result.stderr[-2000:])
    return read_wave("wave.txt")