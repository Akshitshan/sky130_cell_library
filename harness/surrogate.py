import json
import math
import os
import random
from run_sim import simulate, OURS_PEX, NAND2_A
from measure import first_crossing, slew
from sweep import slews_ns, loads_pF, NAMES, VDD

CELLS = [("inv_x1", OURS_PEX, "inv_x1_pex_tables.json"),
         ("nand2_A", NAND2_A, "nand2_A_pex_tables.json")]
M_TEST = 40
S_MAX, C_MAX = slews_ns[-1], loads_pF[-1]


def metrics(cell, s, c):
    # same measurements as sweep.run_sweep, but unrounded and for one (slew, load) point
    t, vin, vout = simulate(s, c * 1000, cell)
    half = VDD / 2
    return {
        "cell_fall": (first_crossing(t, vout, half, "falling") - first_crossing(t, vin, half, "rising")) * 1e9,
        "cell_rise": (first_crossing(t, vout, half, "rising") - first_crossing(t, vin, half, "falling")) * 1e9,
        "fall_transition": slew(t, vout, VDD, "falling") * 1e9,
        "rise_transition": slew(t, vout, VDD, "rising") * 1e9,
    }


def interval(axis, x):
    for k in range(len(axis) - 1):
        if axis[k] <= x <= axis[k + 1]:
            return k, (x - axis[k]) / (axis[k + 1] - axis[k])
    raise ValueError("point outside the table")


def bilinear(table, sx, cx, s, c):
    # straight-line interpolation between the four surrounding grid points
    i, a = interval(sx, s)
    j, b = interval(cx, c)
    return ((1 - a) * (1 - b) * table[i][j] + a * (1 - b) * table[i + 1][j]
            + (1 - a) * b * table[i][j + 1] + a * b * table[i + 1][j + 1])


def terms(s, c, deg):
    # polynomial terms u^i * v^j with i + j <= deg, on axes scaled to 0..1
    u, v = s / S_MAX, c / C_MAX
    return [u ** i * v ** j for i in range(deg + 1) for j in range(deg + 1 - i)]


def fit(points, deg):
    # least squares through the normal equations, solved by Gauss-Jordan elimination
    A = [terms(s, c, deg) for s, c, _ in points]
    y = [v for _, _, v in points]
    n = len(A[0])
    M = [[sum(r[i] * r[j] for r in A) for j in range(n)] + [sum(r[i] * yy for r, yy in zip(A, y))]
         for i in range(n)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(M[r][col]))
        M[col], M[piv] = M[piv], M[col]
        for r in range(n):
            if r != col:
                f = M[r][col] / M[col][col]
                for k in range(col, n + 1):
                    M[r][k] -= f * M[col][k]
    return [M[i][n] / M[i][i] for i in range(n)]


def stats(errs):
    rms = math.sqrt(sum(e * e for e in errs) / len(errs)) * 1000
    return "%6.2f /%6.2f" % (rms, max(abs(e) for e in errs) * 1000)


rng = random.Random(1)
tests = []
for _ in range(M_TEST):
    s = math.exp(rng.uniform(math.log(slews_ns[0]), math.log(S_MAX)))
    c = math.exp(rng.uniform(math.log(loads_pF[0]), math.log(C_MAX)))
    tests.append((min(max(s, slews_ns[0]), S_MAX), min(max(c, loads_pF[0]), C_MAX)))

for name, rec, tfile in CELLS:
    truth_file = "surrogate_truth_%s.json" % name
    if os.path.exists(truth_file):
        truth = json.load(open(truth_file))
    else:
        truth = [metrics(rec, s, c) for s, c in tests]      # 40 fresh simulations
        json.dump(truth, open(truth_file, "w"))
    tables = json.load(open(tfile))
    print("== %s   (each cell: RMS / worst error in ps, vs %d off-grid simulations)" % (name, M_TEST))
    print("%-16s %-10s %-15s %-15s %-15s" % ("metric", "trained on", "bilinear", "poly deg 2", "poly deg 3"))
    for metric in NAMES:
        mean_ps = 1000 * sum(abs(t[metric]) for t in truth) / len(truth)
        for label, I, J in (("49 points", range(7), range(7)), ("16 points", (0, 2, 4, 6), (0, 2, 4, 6))):
            sx = [slews_ns[i] for i in I]
            cx = [loads_pF[j] for j in J]
            sub = [[tables[metric][i][j] for j in J] for i in I]
            pts = [(slews_ns[i], loads_pF[j], tables[metric][i][j]) for i in I for j in J]
            w2, w3 = fit(pts, 2), fit(pts, 3)
            e_bi = [bilinear(sub, sx, cx, s, c) - t[metric] for (s, c), t in zip(tests, truth)]
            e_p2 = [sum(a * b for a, b in zip(w2, terms(s, c, 2))) - t[metric] for (s, c), t in zip(tests, truth)]
            e_p3 = [sum(a * b for a, b in zip(w3, terms(s, c, 3))) - t[metric] for (s, c), t in zip(tests, truth)]
            print("%-16s %-10s %-15s %-15s %-15s mean %.0f ps" % (metric, label, stats(e_bi), stats(e_p2), stats(e_p3), mean_ps))