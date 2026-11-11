import contextlib
import io
import os
import re
import subprocess
from sta import sta

H = os.path.expanduser("~/sky130_cell_library/harness")
DESIGNS = ["adder8", "mult4", "cmp8", "parity16"]
LIBS = [("ours", H + "/mylib_tt.lib"), ("foundry", "hd_subset.lib")]

rows = []
for d in DESIGNS:
    res = {}
    for tag, lib in LIBS:
        net = "%s_%s.v" % (d, tag)
        cmd = ("read_verilog %s.v; synth -top %s -flatten; abc -liberty %s -script area.abc; "
               "opt_clean -purge; write_verilog -noattr %s; stat -liberty %s" % (d, d, lib, net, lib))
        out = subprocess.run(["yosys", "-p", cmd], capture_output=True, text=True).stdout
        m = re.search(r"Chip area for module '\\\w+': ([0-9.]+)", out)
        if not m:
            raise RuntimeError("yosys failed for %s / %s:\n%s" % (d, tag, out[-1500:]))
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            delay, depth, counts = sta(tag, lib, net)
        open("sta_%s_%s.txt" % (d, tag), "w").write(buf.getvalue())
        res[tag] = (float(m.group(1)), delay, depth, sum(counts.values()))
    rows.append((d, res))

print("%-9s %7s %9s %9s %6s | %9s %9s %6s | %5s" % ("design", "cells", "area ours", "area hd", "ratio",
                                                  "delay ours", "delay hd", "ratio", "depth"))
for d, r in rows:
    o, h = r["ours"], r["foundry"]
    print("%-9s %3d/%-3d %9.1f %9.1f %6.2f | %9.1f %9.1f %6.2f | %2d/%-2d" % (
        d, o[3], h[3], o[0], h[0], o[0] / h[0], o[1], h[1], o[1] / h[1], o[2], h[2]))