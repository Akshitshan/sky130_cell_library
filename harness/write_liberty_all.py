import json
import os
from sweep import slews_ns, loads_pF

ROOT = os.path.expanduser("~/sky130_cell_library")
HARN = ROOT + "/harness"


def mag_area(path):
    # bounding box of painted rectangles only; skips non-layout sections like checkpaint
    # unit size comes from the file's own "magscale a b" line: 0.01 um * a / b per unit
    xs, ys = [], []
    um_per_unit = 0.01
    section = ""
    for line in open(path):
        p = line.split()
        if line.startswith("<<"):
            section = line.strip("<> \n")
        elif p and p[0] == "magscale":
            um_per_unit = 0.01 * int(p[1]) / int(p[2])
        elif p and p[0] == "rect" and section != "checkpaint" and not section.startswith("error"):
            x1, y1, x2, y2 = map(int, p[1:5])
            xs += [x1, x2]
            ys += [y1, y2]
    return (max(xs) - min(xs)) * (max(ys) - min(ys)) * um_per_unit ** 2


CELLS = [
    {"name": "inv_x1", "mag": ROOT + "/magic_layout/inverter/inverter.mag",
     "function": "!A", "sense": "negative_unate",
     "pins": {"A": "inv_x1/A"},
     "arcs": {"A": HARN + "/inv_x1_pex_tables.json"}},
    {"name": "inv_x2", "mag": ROOT + "/magic_layout/inv_x2/inv_x2.mag",
     "function": "!A", "sense": "negative_unate",
     "pins": {"A": "inv_x2/A"},
     "arcs": {"A": HARN + "/inv_x2_pex_tables.json"}},
    {"name": "inv_x4", "mag": ROOT + "/magic_layout/inv_x4/inv_x4.mag",
     "function": "!A", "sense": "negative_unate",
     "pins": {"A": "inv_x4/A"},
     "arcs": {"A": HARN + "/inv_x4_pex_tables.json"}},
    {"name": "nand2", "mag": ROOT + "/magic_layout/nand2/nand2.mag",
     "function": "!(A&B)", "sense": "negative_unate",
     "pins": {"A": "nand2/A", "B": "nand2/B"},
     "arcs": {"A": HARN + "/nand2_A_pex_tables.json", "B": HARN + "/nand2_B_pex_tables.json"}},
    {"name": "nor2", "mag": ROOT + "/magic_layout/nor2/nor2.mag",
     "function": "!(A|B)", "sense": "negative_unate",
     "pins": {"A": "nor2/A", "B": "nor2/B"},
     "arcs": {"A": HARN + "/nor2_A_pex_tables.json", "B": HARN + "/nor2_B_pex_tables.json"}},
]

HEADER = """library (mylib_tt) {
  delay_model : table_lookup;
  time_unit : "1ns";
  voltage_unit : "1V";
  current_unit : "1mA";
  capacitive_load_unit (1, pf);
  pulling_resistance_unit : "1kohm";
  leakage_power_unit : "1nW";
  nom_process : 1;
  nom_temperature : 25;
  nom_voltage : 1.8;
  input_threshold_pct_rise : 50;
  input_threshold_pct_fall : 50;
  output_threshold_pct_rise : 50;
  output_threshold_pct_fall : 50;
  slew_lower_threshold_pct_rise : 20;
  slew_upper_threshold_pct_rise : 80;
  slew_lower_threshold_pct_fall : 20;
  slew_upper_threshold_pct_fall : 80;
  lu_table_template (del_template) {
    variable_1 : input_net_transition;
    variable_2 : total_output_net_capacitance;
    index_1 ("%s");
    index_2 ("%s");
  }
"""


def nums(xs):
    return ", ".join(str(x) for x in xs)


def table(kind, rows, pad):
    sp = " " * pad
    body = ", \\\n".join(sp + '    "' + nums(r) + '"' for r in rows)
    return (f"{sp}{kind} (del_template) {{\n"
        f'{sp}  index_1 ("{nums(slews_ns)}");\n'
        f'{sp}  index_2 ("{nums(loads_pF)}");\n'
        f"{sp}  values ( \\\n{body} \\\n{sp}  );\n{sp}}}\n")


def write_all(out_file):
    pincaps = json.load(open(HARN + "/pincaps.json"))
    f = open(out_file, "w")
    f.write(HEADER % (nums(slews_ns), nums(loads_pF)))
    for c in CELLS:
        area = mag_area(c["mag"])
        print(c["name"], "area um^2:", round(area, 3))
        f.write(f'  cell ({c["name"]}) {{\n    area : {area:.3f};\n')
        for pin, key in c["pins"].items():
            f.write(f'    pin ({pin}) {{\n      direction : input;\n      capacitance : {pincaps[key]};\n    }}\n')
        f.write(f'    pin (Y) {{\n      direction : output;\n      function : "{c["function"]}";\n      max_capacitance : {max(loads_pF)};\n      max_transition : {max(slews_ns)};\n')
        for pin, tfile in c["arcs"].items():
            t = json.load(open(tfile))
            f.write(f'      timing () {{\n        related_pin : "{pin}";\n        timing_sense : {c["sense"]};\n')
            for kind in ("cell_fall", "cell_rise", "fall_transition", "rise_transition"):
                f.write(table(kind, t[kind], 8))
            f.write("      }\n")
        f.write("    }\n  }\n")
    f.write("}\n")
    f.close()


if __name__ == "__main__":
    write_all(HARN + "/mylib_tt.lib")