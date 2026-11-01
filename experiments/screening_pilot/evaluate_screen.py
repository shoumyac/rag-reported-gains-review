import json, glob, collections, itertools, os
H = os.path.dirname(os.path.abspath(__file__))
from screen_pilot import MODELS
recs = {r["id"]: r for r in json.load(open(f"{H}/raw/sample_300.json"))}
dec = collections.defaultdict(dict)
for f in glob.glob(f"{H}/out/*.json"):
    r = json.load(open(f))
    if r["parsed"] and r["parsed"].get("decision") in ("INCLUDE", "EXCLUDE", "MAYBE"): dec[r["model"]][r["id"]] = r["parsed"]["decision"]
def kappa(a, b, ids, f=lambda x: x):
    ids = [i for i in ids if i in a and i in b]; n = len(ids)
    ca = collections.Counter(f(a[i]) for i in ids); cb = collections.Counter(f(b[i]) for i in ids)
    po = sum(f(a[i]) == f(b[i]) for i in ids) / n
    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / n / n
    return (po - pe) / (1 - pe) if pe < 1 else 1.0, po, n
ids = list(recs)
print("answered:", {m: len(dec[m]) for m in MODELS})
two = lambda x: "EXCL" if x == "EXCLUDE" else "KEEP"
print("\nCohen's kappa, 2 classes (EXCLUDE vs INCLUDE-or-MAYBE):")
print(" " * 18 + "".join(f"{m[:8]:>10s}" for m in MODELS))
for a in MODELS: print(f"{a:18s}" + "".join(f"{kappa(dec[a], dec[b], ids, two)[0]:10.2f}" for b in MODELS))
print("\nCohen's kappa, 3 classes:")
for a in MODELS: print(f"{a:18s}" + "".join(f"{kappa(dec[a], dec[b], ids)[0]:10.2f}" for b in MODELS))
split = [i for i in ids if len({two(dec[m][i]) for m in MODELS if i in dec[m]}) > 1]
print("\nrecords where models split between EXCLUDE and keep:", len(split), "of", len(ids))
json.dump(split, open(f"{H}/raw/split_ids.json", "w"))
