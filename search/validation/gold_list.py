"""Match each candidate title to an OpenAlex work and test the registered query.

Usage: python search/validation/gold_list.py  (needs OPENALEX_API_KEY in env or .env)
Writes gold_list.csv next to this file. A title is accepted only if the OpenAlex
title is at least 0.92 similar; everything else is listed as UNMATCHED for hand checking.
"""
import csv, difflib, json, os, re, sys, time, urllib.parse, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
def key():
    k = os.environ.get("OPENALEX_API_KEY")
    if k: return k
    for p in (os.path.join(ROOT, ".env"),):
        if os.path.exists(p):
            for line in open(p):
                if line.startswith("OPENALEX_API_KEY="): return line.split("=", 1)[1].strip()
    sys.exit("no OPENALEX_API_KEY")
KEY = key()
def get(params):
    url = "https://api.openalex.org/works?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"Authorization": "Bearer " + KEY})
    for i in range(4):
        try:
            with urllib.request.urlopen(req, timeout=60) as r: return json.load(r)
        except Exception as e:
            err = e; time.sleep(2 * (i + 1))
    raise err
norm = lambda s: re.sub(r"[^a-z0-9 ]", "", s.lower().replace("-", " ")).strip()
sys.path.insert(0, os.path.join(ROOT, "search"))
QUERY = ('("retrieval-augmented generation" OR "retrieval augmented generation" OR "retrieval-augmented language model" '
         'OR "retrieval-augmented language models" OR "retrieval-augmented LLM" OR "retrieval-augmented large language model" '
         'OR ("RAG" AND (retrieval OR retriever OR "language model" OR LLM)))')
BASE = "from_publication_date:2020-01-01,to_publication_date:2026-11-30,language:en,type:article|preprint|conference-paper"
rows = []
for title in [t.strip() for t in open(os.path.join(HERE, "gold_candidates.txt")) if t.strip()]:
    d = get({"filter": "title.search:" + title.replace(",", " ").replace(":", " "), "per-page": 10,
             "select": "id,doi,title,publication_year,type,cited_by_count"})
    best = max(d["results"], key=lambda w: difflib.SequenceMatcher(None, norm(title), norm(w["title"] or "")).ratio(), default=None)
    sim = difflib.SequenceMatcher(None, norm(title), norm(best["title"] or "")).ratio() if best else 0
    row = {"candidate": title, "openalex_id": "", "doi": "", "oa_title": "", "year": "", "type": "", "similarity": round(sim, 3), "status": "UNMATCHED", "in_registered_query": ""}
    if best and sim >= 0.92:
        row.update(openalex_id=best["id"].split("/")[-1], doi=best["doi"] or "", oa_title=best["title"], year=best["publication_year"], type=best["type"], status="matched")
    rows.append(row)
    time.sleep(0.15)
ids = [r["openalex_id"] for r in rows if r["openalex_id"]]
hits = set()
for i in range(0, len(ids), 40):
    chunk = ids[i:i + 40]
    d = get({"filter": f"title_and_abstract.search:{QUERY},{BASE},openalex:{'|'.join(chunk)}", "per-page": 100, "select": "id"})
    hits |= {w["id"].split("/")[-1] for w in d["results"]}
for r in rows:
    if r["openalex_id"]: r["in_registered_query"] = "yes" if r["openalex_id"] in hits else "no"
with open(os.path.join(HERE, "gold_list.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
m = [r for r in rows if r["status"] == "matched"]
print(f"candidates {len(rows)}, matched {len(m)}, retrieved by registered query {sum(r['in_registered_query']=='yes' for r in m)}")
for r in rows:
    if r["status"] != "matched" or r["in_registered_query"] == "no": print(r["status"], r["in_registered_query"], r["similarity"], r["candidate"], "|", r["oa_title"], r["type"], r["year"])
