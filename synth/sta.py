import os
import re

OUT_LOAD_PF = 0.00952062     # every primary output carries 9.52 fF
IN_SLEW_NS = 0.122474        # every primary input arrives at t = 0 with this slew
KINDS = ("cell_fall", "cell_rise", "fall_transition", "rise_transition")
NUM = r'-?\d+\.?\d*(?:[eE][-+]?\d+)?'


def nums(s):
    return [float(x) for x in re.findall(NUM, s)]


def load_cell(path, cell):
    # input pin capacitances and the four timing tables of every input -> Y arc
    text = open(path).read()
    m = re.search(r'cell\s*\(\s*"?%s"?\s*\)' % re.escape(cell), text)
    if not m:
        raise RuntimeError("cell %s not found in %s" % (cell, path))
    nxt = re.search(r'\n\s*cell\s*\(', text[m.end():])
    block = text[m.start(): m.end() + nxt.start()] if nxt else text[m.start():]
    arcs, caps = {}, {}
    for part in re.split(r'timing\s*\(\s*\)\s*\{', block)[1:]:
        pin = re.search(r'related_pin\s*:\s*"?(\w+)"?', part).group(1)
        tabs = {}
        for kind in KINDS:
            body = re.search(kind + r'\s*\(\s*"?[^")]*"?\s*\)\s*\{(.*?)\}', part, re.S).group(1)
            i1 = nums(re.search(r'index_1\s*\(\s*"([^"]*)"', body).group(1))
            i2 = nums(re.search(r'index_2\s*\(\s*"([^"]*)"', body).group(1))
            vals = nums(re.search(r'values\s*\((.*?)\)\s*;', body, re.S).group(1))
            if len(vals) != len(i1) * len(i2):
                raise RuntimeError("table size mismatch in %s %s %s" % (cell, pin, kind))
            tabs[kind] = (i1, i2, [vals[k * len(i2):(k + 1) * len(i2)] for k in range(len(i1))])
        arcs[pin] = tabs
    for pin in arcs:
        pm = re.search(r'pin\s*\(\s*"?%s"?\s*\)' % pin, block)
        caps[pin] = float(re.search(r'\bcapacitance\s*:\s*(%s)' % NUM, block[pm.end():]).group(1))
    return caps, arcs


def lookup(tab, s, c):
    # bilinear interpolation, clamped to the table edges; rows = slew, columns = load
    xs, ys, v = tab

    def seg(axis, x):
        x = min(max(x, axis[0]), axis[-1])
        for k in range(len(axis) - 1):
            if x <= axis[k + 1]:
                return k, (x - axis[k]) / (axis[k + 1] - axis[k])

    i, a = seg(xs, s)
    j, b = seg(ys, c)
    return ((1 - a) * (1 - b) * v[i][j] + a * (1 - b) * v[i + 1][j]
            + (1 - a) * b * v[i][j + 1] + a * b * v[i + 1][j + 1])


def read_netlist(path):
    text = open(path).read()
    insts = []
    for m in re.finditer(r'(\w+)\s+(\S+)\s*\(\s*(\.\w+\([^)]*\)(?:\s*,\s*\.\w+\([^)]*\))*)\s*\)\s*;', text):
        pins = {p: n.strip() for p, n in re.findall(r'\.(\w+)\(\s*([^)]*?)\s*\)', m.group(3))}
        insts.append((m.group(1), m.group(2), pins))
    alias = {m.group(1): m.group(2) for m in re.finditer(r'assign\s+(\S+)\s*=\s*(\S+?)\s*;', text)}
    outs = []
    for m in re.finditer(r'output\s*(?:\[(\d+):(\d+)\])?\s*(\w+)\s*;', text):
        hi, lo, name = m.groups()
        outs += ["%s[%d]" % (name, k) for k in range(int(lo), int(hi) + 1)] if hi else [name]
    return insts, alias, outs


def sta(label, lib_path, netlist_path):
    insts, alias, outs = read_netlist(netlist_path)
    types = sorted({t for t, _, _ in insts})
    lib = {t: load_cell(lib_path, t) for t in types}

    def res(n):
        while n in alias:
            n = alias[n]
        return n

    driver, load = {}, {}
    for t, name, pins in insts:
        driver[res(pins["Y"])] = (t, name, pins)
        for p, n in pins.items():
            if p != "Y":
                load[res(n)] = load.get(res(n), 0.0) + lib[t][0][p]
    for o in outs:
        load[res(o)] = load.get(res(o), 0.0) + OUT_LOAD_PF

    memo = {}

    def arrival(net):
        # {edge: (arrival ns, slew ns, how we got here)} for a rising and a falling edge on this net
        net = res(net)
        if net in memo:
            return memo[net]
        if net not in driver:                                   # primary input
            memo[net] = {"rise": (0.0, IN_SLEW_NS, None), "fall": (0.0, IN_SLEW_NS, None)}
            return memo[net]
        t, name, pins = driver[net]
        arcs = lib[t][1]
        c = load.get(net, 0.0)
        best = {"rise": None, "fall": None}
        for p, n in pins.items():
            if p == "Y":
                continue
            a_in = arrival(n)
            # every cell here is inverting: output rises after an input fall, and vice versa
            for out_e, in_e, dk, sk in (("rise", "fall", "cell_rise", "rise_transition"),
                                        ("fall", "rise", "cell_fall", "fall_transition")):
                t_in, s_in, _ = a_in[in_e]
                arr = t_in + lookup(arcs[p][dk], s_in, c)
                if best[out_e] is None or arr > best[out_e][0]:
                    best[out_e] = (arr, lookup(arcs[p][sk], s_in, c), (t, p, res(n), in_e))
        memo[net] = best
        return best

    worst = None
    for o in outs:
        a = arrival(o)
        if len(outs) <= 2:
            print("   %s: rise %.2f ps, fall %.2f ps" % (o, a["rise"][0] * 1000, a["fall"][0] * 1000))
        for e in ("rise", "fall"):
            if worst is None or a[e][0] > worst[0]:
                worst = (a[e][0], o, e)
    path, net, edge = [], res(worst[1]), worst[2]
    while net in driver:
        arr, _, pred = arrival(net)[edge]
        path.append((pred[0], pred[1], edge, arr))
        net, edge = pred[2], pred[3]
    path.reverse()
    counts = {t: sum(1 for x in insts if x[0] == t) for t in types}
    print("== %s: %d cells %s" % (label, len(insts), counts))
    print("   critical path: %.1f ps to %s (%s edge), %d cells deep" % (worst[0] * 1000, worst[1], worst[2], len(path)))
    for t, p, e, arr in path:
        print("     %-26s via pin %s  output %s at %.1f ps" % (t, p, e, arr * 1000))
    return worst[0] * 1000, len(path), counts


if __name__ == "__main__":
    H = os.path.expanduser("~/sky130_cell_library/harness")
    # sanity check: a single inverter at the table centre should reproduce the Monte Carlo nominals
    open("inv_test.v", "w").write("module t(a, y);\n input a;\n output y;\n inv_x1 u (.A(a), .Y(y));\nendmodule\n")
    print("sanity check (expect fall about 106.7 ps, rise about 110.9 ps):")
    sta("single inv_x1", H + "/mylib_tt.lib", "inv_test.v")
    sta("ours", H + "/mylib_tt.lib", "adder8_ours.v")
    sta("foundry subset", "hd_subset.lib", "adder8_hd.v")