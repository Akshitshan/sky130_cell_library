import os
import subprocess
from sta import sta

H = os.path.expanduser("~/sky130_cell_library/harness")

open("chain.v", "w").write("""module chain(a, y);
  input a;
  output y;
  wire n1, n2, n3, n5, hi, lo;
  inv_x1 u1 (.A(a), .Y(n1));
  nand2 u2 (.A(n1), .B(hi), .Y(n2));
  nor2 u3 (.A(n2), .B(lo), .Y(n3));
  inv_x1 u4 (.A(n3), .Y(y));
  inv_x1 u5 (.A(n2), .Y(n5));
endmodule
""")


def header(path):
    for line in open(path):
        if line.lower().startswith(".subckt"):
            return line.split()[2:]


def inst(name, cell, path, conns):
    return "%s %s %s" % (name, " ".join(conns[p] for p in header(path)), cell)


INV, NAND, NOR = (H + "/inverter_pex_sa.spice", H + "/nand2_pex_sa.spice", H + "/nor2_pex_sa.spice")
tr = 0.122474 / 0.6
deck = "\n".join([
    "* STA validation chain", ".temp 25",
    ".include %s/sky130_min.spice" % H, ".include " + INV, ".include " + NAND, ".include " + NOR,
    inst("X1", "inverter", INV, {"Vdd": "vdd", "GND": "0", "Vin": "a", "Vout": "n1"}),
    inst("X2", "nand2", NAND, {"Vdd": "vdd", "GND": "0", "A": "n1", "B": "hi", "Y": "n2"}),
    inst("X3", "nor2", NOR, {"Vdd": "vdd", "GND": "0", "A": "n2", "B": "lo", "Y": "n3"}),
    inst("X4", "inverter", INV, {"Vdd": "vdd", "GND": "0", "Vin": "n3", "Vout": "y"}),
    inst("X5", "inverter", INV, {"Vdd": "vdd", "GND": "0", "Vin": "n2", "Vout": "n5"}),
    "VH hi 0 1.8", "VL lo 0 0", "V1 vdd 0 1.8",
    "V2 a 0 pulse(0 1.8 1n %.5fn %.5fn 3n 100n)" % (tr, tr),
    "C1 y 0 9.52062f", ".tran 1p 8n",
    ".control", "run", "wrdata chain.txt v(a) v(y)", "quit", ".endc", ".end", ""])
open("chain.spice", "w").write(deck)
if os.path.exists("chain.txt"):
    os.remove("chain.txt")
out = subprocess.run(["ngspice", "-b", "chain.spice"], capture_output=True, text=True)
if not os.path.exists("chain.txt"):
    raise RuntimeError("ngspice failed:\n" + out.stdout[-2000:])


def cross(t, v, level, rising):
    for k in range(1, len(t)):
        a, b = v[k - 1], v[k]
        if (rising and a < level <= b) or (not rising and a > level >= b):
            return t[k - 1] + (level - a) * (t[k] - t[k - 1]) / (b - a)
    raise RuntimeError("no crossing found")


t, a, y = [], [], []
for line in open("chain.txt"):
    c = line.split()
    t.append(float(c[0])); a.append(float(c[1])); y.append(float(c[3]))
print("STA:")
sta("chain", H + "/mylib_tt.lib", "chain.v")
print("SPICE: y rise %.2f ps, y fall %.2f ps" % (
    (cross(t, y, 0.9, True) - cross(t, a, 0.9, True)) * 1e12,
    (cross(t, y, 0.9, False) - cross(t, a, 0.9, False)) * 1e12))