import os
import subprocess

H = os.path.expanduser("~/sky130_cell_library/harness")
LIB_OFF = H + "/sky130_min.spice"
LIB_ON = H + "/sky130_min_mm.spice"


def cross(t, v, level, rising):
    # time at which v crosses `level`, linearly interpolated between samples
    for k in range(1, len(t)):
        a, b = v[k - 1], v[k]
        if (rising and a < level <= b) or (not rising and a > level >= b):
            return t[k - 1] + (level - a) * (t[k] - t[k - 1]) / (b - a)
    raise RuntimeError("no crossing found")


def run(lib, seed):
    seedline = "" if seed is None else ".option seed=%d" % seed
    deck = f"""* mismatch probe: two identical inverters, same input
.temp 25
{seedline}
.include {lib}
.include {H}/inverter_pex_sa.spice
X1 vdd 0 o1 vin inverter
X2 vdd 0 o2 vin inverter
C1 o1 0 5f
C2 o2 0 5f
V1 vdd 0 1.8
V2 vin 0 pulse(0 1.8 1n 0.1n 0.1n 3n 20n)
.tran 1p 5n
.control
run
wrdata mcwave.txt v(vin) v(o1) v(o2)
quit
.endc
.end
"""
    wave = H + "/mcwave.txt"
    if os.path.exists(wave):
        os.remove(wave)                      # never measure a stale file
    open(H + "/mcdeck.spice", "w").write(deck)
    out = subprocess.run(["ngspice", "-b", H + "/mcdeck.spice"], capture_output=True, text=True, cwd=H)
    if not os.path.exists(wave):
        raise RuntimeError("ngspice did not write the waveform:\n" + out.stdout[-1500:])
    t, vin, o1, o2 = [], [], [], []
    for line in open(wave):
        c = line.split()
        t.append(float(c[0])); vin.append(float(c[1])); o1.append(float(c[3])); o2.append(float(c[5]))
    t_in = cross(t, vin, 0.9, True)
    return (cross(t, o1, 0.9, False) - t_in) * 1e12, (cross(t, o2, 0.9, False) - t_in) * 1e12


RUNS = [
    ("mismatch OFF", LIB_OFF, 1),
    ("mismatch ON, seed 1", LIB_ON, 1),
    ("mismatch ON, seed 1 again", LIB_ON, 1),
    ("mismatch ON, seed 2", LIB_ON, 2),
    ("mismatch ON, no seed", LIB_ON, None),
    ("mismatch ON, no seed again", LIB_ON, None),
]
for name, lib, seed in RUNS:
    a, b = run(lib, seed)
    print("%-28s inverter A %.3f ps   inverter B %.3f ps" % (name, a, b))