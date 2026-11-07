import re

def number(line, name):
    return float(re.search(r"\b" + name + r"=([0-9.e+-]+)", line).group(1))

def add_stress(src, dst):
    out = []
    for line in open(src):
        line = line.rstrip("\n")
        if line.startswith("X"):
            ad = number(line, "ad")
            as_ = number(line, "as")
            w = number(line, "w")
            l = number(line, "l")
            big = max(ad, as_) / w
            small = min(ad, as_) / w
            if abs(ad - as_) < 1e-6:
                sa = sb = big
            else:
                sa = big
                sb = 2 * small + l + big
            line = line + f" sa={sa:.4f} sb={sb:.4f}"
        out.append(line)
    with open(dst, "w") as f:
        f.write("\n".join(out) + "\n")