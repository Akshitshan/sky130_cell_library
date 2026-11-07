def read_wave(filename):
    t = []
    vin = []
    vout = []
    with open(filename) as f:
        for line in f:
            cols = line.split()
            t.append(float(cols[0]))
            vin.append(float(cols[1]))
            vout.append(float(cols[3]))
    return t, vin, vout


def first_crossing(t, v, level, direction):
    for i in range(1, len(t)):
        before = v[i - 1]
        after = v[i]
        if direction == "rising" and before < level <= after:
            frac = (level - before) / (after - before)
            return t[i - 1] + frac * (t[i] - t[i - 1])
        if direction == "falling" and before > level >= after:
            frac = (level - before) / (after - before)
            return t[i - 1] + frac * (t[i] - t[i - 1])
    return None

def slew(t, v, vdd, direction):
    low = 0.2 * vdd
    high = 0.8 * vdd
    if direction == "rising":
        return first_crossing(t, v, high, "rising") - first_crossing(t, v, low, "rising")
    else:
        return first_crossing(t, v, low, "falling") - first_crossing(t, v, high, "falling")