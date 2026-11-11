import json
import os
import statistics
import subprocess
from run_sim import OURS_PEX, INV_X2, INV_X4, NAND2_A, NAND2_B, NOR2_A, NOR2_B

H = os.path.expanduser("~/sky130_cell_library/harness")
LIB_OFF = H + "/sky130_min.spice"
LIB_MM = H + "/sky130_min_mm.spice"
SLEW_NS = 0.122474      # middle of the Liberty slew axis
LOAD_FF = 9.52062       # middle of the Liberty load axis
N = 200

CELLS = [("inv_x1", OURS_PEX), ("inv_x2", INV_X2), ("inv_x4", INV_X4),
         ("nand2_A", NAND2_A), ("nand2_B", NAND2_B), ("nor2_A", NOR2_A), ("nor2_B", NOR2_B)]


def cross(t, v, level, rising):
    for k in range(1, len(t)):
        a, b = v[k - 1], v[k]
        if (rising and a < level <= b) or (not rising and a > level >= b):
            return t[k - 1] + (level - a) * (t[k] - t[k - 1]) / (b - a)
    raise RuntimeError("no crossing found")


def one_run(rec, seed, lib):
    tr = SLEW_NS / 0.6
    width = 3.0
    tstop = 1 + 2 * tr + 2 * width
    deck = f"""* monte carlo run
.temp 25
.option seed={seed}
.include {lib}
.include {rec['file']}
{rec['inst']}
{rec.get('extra', '')}
C1 vout 0 {LOAD_FF}f
V1 vdd 0 1.8
V2 vin 0 pulse(0 1.8 1n {tr:.5f}n {tr:.5f}n {width:.3f}n 100n)
.tran 1p {tstop:.3f}n
.control
run
wrdata mcwave.txt v(vin) v(vout)
quit
.endc
.end
"""
    wave = H + "/mcwave.txt"
    if os.path.exists(wave):
        os.remove(wave)
    open(H + "/mcdeck.spice", "w").write(deck)
    out = subprocess.run(["ngspice", "-b", H + "/mcdeck.spice"], capture_output=True, text=True, cwd=H)
    if not os.path.exists(wave):
        raise RuntimeError("ngspice did not write the waveform:\n" + out.stdout[-1500:])
    t, vin, vout = [], [], []
    for line in open(wave):
        c = line.split()
        t.append(float(c[0])); vin.append(float(c[1])); vout.append(float(c[3]))
    d_fall = cross(t, vout, 0.9, False) - cross(t, vin, 0.9, True)     # output falls after input rises
    d_rise = cross(t, vout, 0.9, True) - cross(t, vin, 0.9, False)     # output rises after input falls
    return d_fall * 1e12, d_rise * 1e12


results = {}
for name, rec in CELLS:
    nom_f, nom_r = one_run(rec, 1, LIB_OFF)
    fall, rise = [], []
    for seed in range(1, N + 1):
        f, r = one_run(rec, seed, LIB_MM)
        fall.append(f)
        rise.append(r)
    results[name] = {"nominal_fall_ps": nom_f, "nominal_rise_ps": nom_r, "fall_ps": fall, "rise_ps": rise}
    print("%-8s fall: nominal %.2f  mean %.2f  sigma %.2f ps (%.1f%%)   rise: nominal %.2f  mean %.2f  sigma %.2f ps (%.1f%%)" % (
        name, nom_f, statistics.mean(fall), statistics.stdev(fall), 100 * statistics.stdev(fall) / statistics.mean(fall),
        nom_r, statistics.mean(rise), statistics.stdev(rise), 100 * statistics.stdev(rise) / statistics.mean(rise)))
    json.dump(results, open(H + "/mc_results.json", "w"))