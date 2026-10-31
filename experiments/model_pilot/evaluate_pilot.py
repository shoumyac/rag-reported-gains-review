import json, re, glob, collections, os
H = os.path.dirname(os.path.abspath(__file__))
from extract_pilot import PAPERS, MODELS
sq = lambda s: re.sub(r"[^a-z0-9.%]", "", str(s).lower())
def num(x):
    try: return float(str(x).replace("%", "").strip())
    except Exception: return None
texts = {}
for p in PAPERS:
    raw = open(f"{H}/papers/{p}.txt", encoding="utf-8", errors="ignore").read()
    pages = raw.split("\f")
    texts[p] = {"pages": [sq(x) for x in pages], "all": sq(raw), "lines": [sq(l) for l in raw.split("\n") if l.strip()]}
def parse(t):
    t = t.strip()
    m = re.search(r"\[.*\]", t, re.S)
    try: return json.loads(m.group(0)) if m else None
    except Exception: return None
rows = []; stats = collections.defaultdict(lambda: collections.Counter())
for m in MODELS:
    for p in PAPERS:
        r = json.load(open(f"{H}/out/{m}__{p}.json")); items = parse(r["text"])
        s = stats[m]; s["papers"] += 1
        if items is None: s["bad_json"] += 1; continue
        for it in items:
            if not isinstance(it, dict): continue
            s["rows"] += 1
            q = sq(it.get("quote") or ""); ms = it.get("method_score"); cs = it.get("comparator_score")
            qf = len(q) > 5 and q in texts[p]["all"]
            mq = ms is not None and sq(ms) in q
            cn = sq((it.get("comparator_name") or ""))
            cname_tok = re.sub(r"\(.*?\)", "", str(it.get("comparator_name") or ""))
            tok = sq(cname_tok.split()[0]) if cname_tok.split() else ""
            cl = cs is not None and any(sq(cs) in l and (tok and tok in l) for l in texts[p]["lines"])
            cnum = cs is not None and sq(cs) in texts[p]["all"]
            pg = it.get("page"); pgok = isinstance(pg, int) and 1 <= pg <= len(texts[p]["pages"]) and q in texts[p]["pages"][pg - 1] if qf else False
            s["quote_found"] += qf; s["method_in_quote"] += mq; s["quote_ok_and_method_in_quote"] += (qf and mq)
            s["comp_score_in_paper"] += cnum; s["comp_name_and_score_same_line"] += cl; s["page_correct"] += pgok
            rows.append({"model": m, "paper": p, "ms": num(ms), "cs": num(cs), "bench": it.get("benchmark"), "metric": it.get("metric"), "mname": it.get("method_name"), "cname": it.get("comparator_name"), "ctype": it.get("comparator_type"), "qf": qf, "mq": mq, "cl": cl})
json.dump(rows, open(f"{H}/rows.json", "w"))
print(f"{'model':18s} {'rows':>5s} {'quote found':>12s} {'method score in quote':>22s} {'comp. score in paper':>21s} {'comp. name+score same line':>27s} {'page ok':>8s} bad_json")
for m, s in stats.items():
    n = s["rows"] or 1
    print(f"{m:18s} {s['rows']:5d} {100*s['quote_found']/n:11.1f}% {100*s['method_in_quote']/n:21.1f}% {100*s['comp_score_in_paper']/n:20.1f}% {100*s['comp_name_and_score_same_line']/n:26.1f}% {100*s['page_correct']/n:7.1f}% {s['bad_json']}")
# consensus on method-score cells
cells = collections.defaultdict(set)
for r in rows:
    if r["ms"] is not None: cells[(r["paper"], r["ms"])].add(r["model"])
cons = {k for k, v in cells.items() if len(v) >= 4}
print("\nconsensus method-score cells (>=4 of 6 models):", len(cons))
for m in MODELS:
    got = {(r["paper"], r["ms"]) for r in rows if r["model"] == m}
    print(f"  {m:18s} covers {len(got & cons):3d}/{len(cons)} consensus cells; {len(got - cons)} non-consensus cells")
# comparator agreement: same method cell, same comparator score
pair = collections.defaultdict(dict)
for r in rows:
    pair[(r["paper"], r["ms"], r["cs"])].setdefault("m", set()).add(r["model"])
print("\npairwise agreement on (method score, comparator score) triples, Jaccard:")
ms_ = list(MODELS)
sets = {m: {(r["paper"], r["ms"], r["cs"]) for r in rows if r["model"] == m} for m in ms_}
print(" " * 18 + "".join(f"{m[:9]:>10s}" for m in ms_))
for a in ms_:
    print(f"{a:18s}" + "".join(f"{len(sets[a]&sets[b])/max(1,len(sets[a]|sets[b])):10.2f}" for b in ms_))
