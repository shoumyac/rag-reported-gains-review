"""Round 3: a new random sample of 100 records (seed 20261103), excluding the 300 of round 1 and the 100 of round 2.
Missing abstracts are recovered from Crossref, then arXiv (DOI 10.48550/arXiv.*), where possible."""
import csv, json, os, re, sys, time, urllib.parse, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, "..", "..")
for l in open(os.path.join(ROOT, ".env")):
    if "=" in l: k, v = l.strip().split("=", 1); os.environ.setdefault(k, v)
sys.path.insert(0, os.path.join(ROOT, "search")); sys.path.insert(0, HERE)
import oa_search as O
from draw_sample import ab
O.QUERY = O.QUERY_EXTENDED
SEED = 20261103
prev = {r["id"] for r in json.load(open(f"{HERE}/raw/sample_300.json"))} | {r["id"] for r in json.load(open(f"{HERE}/raw/sample_100_round2.json"))}
out = []
for page in (1, 2):
    params = {"filter": O.build_filter(True), "sample": 160, "seed": SEED, "per-page": 100, "page": page, "select": "id,doi,title,type,abstract_inverted_index"}
    req = urllib.request.Request("https://api.openalex.org/works?" + urllib.parse.urlencode(params), headers={"Authorization": "Bearer " + os.environ["OPENALEX_API_KEY"]})
    for w in json.load(urllib.request.urlopen(req, timeout=60))["results"]:
        out.append({"id": w["id"].split("/")[-1], "doi": w.get("doi"), "title": w.get("title"), "abstract": ab(w.get("abstract_inverted_index")), "abstract_source": "openalex" if w.get("abstract_inverted_index") else ""})
    time.sleep(0.3)
seen = set(); recs = []
for r in out:
    if r["id"] in prev or r["id"] in seen: continue
    seen.add(r["id"]); recs.append(r)
recs = recs[:100]
UA = {"User-Agent": "rag-review (mailto:shoumyac@student.unimelb.edu.au)"}
for r in recs:
    if r["abstract"] or not r["doi"]: continue
    doi = r["doi"].replace("https://doi.org/", "")
    try:
        m = json.load(urllib.request.urlopen(urllib.request.Request("https://api.crossref.org/works/" + urllib.parse.quote(doi), headers=UA), timeout=30))["message"]
        a = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", m.get("abstract", "") or "")).strip()
        a = re.sub(r"^Abstract\s*", "", a)
        if a: r["abstract"], r["abstract_source"] = a, "crossref"
    except Exception: pass
    if not r["abstract"] and "arxiv" in doi.lower():
        try:
            aid = doi.lower().split("arxiv.")[-1]
            x = urllib.request.urlopen("http://export.arxiv.org/api/query?id_list=" + aid, timeout=30).read().decode()
            m = re.search(r"<summary>(.*?)</summary>", x, re.S)
            if m: r["abstract"], r["abstract_source"] = re.sub(r"\s+", " ", m.group(1)).strip(), "arxiv"
        except Exception: pass
    time.sleep(0.15)
json.dump(recs, open(f"{HERE}/raw/sample_100_round3.json", "w"))
with open(f"{HERE}/sample_100_round3_ids.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["openalex_id", "doi", "title", "abstract_source"]); [w.writerow([r["id"], r["doi"], r["title"], r["abstract_source"] or "none"]) for r in recs]
with open(f"{HERE}/screening_sheet_round3_100_for_humans.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f); w.writerow(["record_id", "title", "abstract", "decision (INCLUDE/EXCLUDE/MAYBE)", "code (E1,E2,E6,E9 if EXCLUDE)", "note", "screener_initials", "date"])
    for r in recs: w.writerow([r["id"], r["title"], r["abstract"] or "(no abstract)", "", "", "", "", ""])
import collections
print(len(recs), dict(collections.Counter(r["abstract_source"] or "none" for r in recs)))
