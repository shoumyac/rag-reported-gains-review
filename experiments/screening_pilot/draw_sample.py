"""Draw the random calibration sample of 300 records from the extended OpenAlex query (seed fixed)."""
import json, os, sys, time, urllib.parse, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, "..", "..")
for l in open(os.path.join(ROOT, ".env")):
    if "=" in l: k, v = l.strip().split("=", 1); os.environ.setdefault(k, v)
sys.path.insert(0, os.path.join(ROOT, "search"))
import oa_search as O
O.QUERY = O.QUERY_EXTENDED
SEED = 20261101
os.makedirs(f"{HERE}/raw", exist_ok=True)
def ab(inv):
    if not inv: return ""
    pos = {}
    for w, idx in inv.items():
        for i in idx: pos[i] = w
    return " ".join(pos[i] for i in sorted(pos))
out = []
for page in (1, 2, 3):
    params = {"filter": O.build_filter(True), "sample": 300, "seed": SEED, "per-page": 100, "page": page, "select": "id,doi,title,type,publication_year,abstract_inverted_index"}
    req = urllib.request.Request("https://api.openalex.org/works?" + urllib.parse.urlencode(params), headers={"Authorization": "Bearer " + os.environ["OPENALEX_API_KEY"]})
    d = json.load(urllib.request.urlopen(req, timeout=60))
    for w in d["results"]:
        out.append({"id": w["id"].split("/")[-1], "doi": w.get("doi"), "title": w.get("title"), "type": w.get("type"), "abstract": ab(w.get("abstract_inverted_index"))})
    time.sleep(0.3)
seen = set(); uniq = []
for r in out:
    if r["id"] not in seen: seen.add(r["id"]); uniq.append(r)
json.dump(uniq, open(f"{HERE}/raw/sample_300.json", "w"))
import csv
with open(f"{HERE}/sample_300_ids.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["openalex_id", "doi", "title"]); [w.writerow([r["id"], r["doi"], r["title"]]) for r in uniq]
print(len(out), len(uniq), "with abstract:", sum(bool(r["abstract"]) for r in uniq))
