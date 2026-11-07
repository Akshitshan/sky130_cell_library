import json

A = "inv_x1_tables.json"
B = "inv_x1_pex_tables.json"
a = json.load(open(A))
b = json.load(open(B))

for name in a:
    print(name, "(", B, "/", A, ")")
    for row_a, row_b in zip(a[name], b[name]):
        print([round(y / x, 2) for x, y in zip(row_a, row_b)])