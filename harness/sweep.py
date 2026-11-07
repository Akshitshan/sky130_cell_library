import json
from run_sim import simulate, OURS, FOUNDRY_INV1
from measure import first_crossing, slew

VDD = 1.8
slews_ns = [0.01, 0.0230506, 0.0531329, 0.122474, 0.282311, 0.650743, 1.5]
loads_pF = [0.0005, 0.00133517, 0.00356533, 0.00952062, 0.0254232, 0.0678883, 0.181284]
NAMES = ["cell_fall", "cell_rise", "fall_transition", "rise_transition"]


def run_sweep(cell, outfile):
    tables = {name: [] for name in NAMES}
    for s in slews_ns:
        row = {name: [] for name in NAMES}
        for c in loads_pF:
            t, vin, vout = simulate(s, c * 1000, cell)
            half = VDD / 2
            tphl = first_crossing(t, vout, half, "falling") - first_crossing(t, vin, half, "rising")
            tplh = first_crossing(t, vout, half, "rising") - first_crossing(t, vin, half, "falling")
            row["cell_fall"].append(round(tphl * 1e9, 4))
            row["cell_rise"].append(round(tplh * 1e9, 4))
            row["fall_transition"].append(round(slew(t, vout, VDD, "falling") * 1e9, 4))
            row["rise_transition"].append(round(slew(t, vout, VDD, "rising") * 1e9, 4))
        for name in NAMES:
            tables[name].append(row[name])
    with open(outfile, "w") as f:
        json.dump(tables, f, indent=1)


if __name__ == "__main__":
    run_sweep(OURS, "inv_x1_tables.json")
    run_sweep(FOUNDRY_INV1, "inv1_foundry_tables.json")