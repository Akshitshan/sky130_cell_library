import os

LIB = os.path.expandvars("$PDK_ROOT/sky130A/libs.ref/sky130_fd_sc_hd/lib/sky130_fd_sc_hd__tt_025C_1v80.lib")
KEEP = ["inv_1", "inv_2", "inv_4", "nand2_1", "nor2_1"]    # same functions and drive range as ours

text = open(LIB).read()
first = text.index('cell ("')
out = text[:first]                                         # library header: units, templates, thresholds
for name in KEEP:
    start = text.index('cell ("sky130_fd_sc_hd__%s")' % name)
    nxt = text.find('cell ("', start + 10)
    out += text[start:nxt if nxt != -1 else len(text)]
out += "}\n"
open("hd_subset.lib", "w").write(out)
print("wrote hd_subset.lib with", KEEP)