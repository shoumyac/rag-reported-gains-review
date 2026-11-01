"""Evaluate v2 extraction (selection rule): quote validity and agreement between two models."""
import json, re, os, collections, sys
H = os.path.dirname(os.path.abspath(__file__))
PAPERS = ["2310.11511","2401.15884","2403.14403","2310.04408","2301.12652","2305.06983","2310.01352","2311.09210","2302.00083","2407.02485"]
A, B = (sys.argv[1], sys.argv[2]) if len(sys.argv) > 2 else ("haiku-5.5", "deepseek-v4-flash")
sq = lambda s: re.sub(r"[^a-z0-9.%]", "", str(s).lower())
def num(x):
    try: return float(str(x).replace("%", "").strip())
    except Exception: return None
txt = {p: sq(open(f"{H}/papers/{p}.txt", encoding="utf-8", errors="ignore").read()) for p in PAPERS}
def rows(m):
    out = []; st = collections.Counter()
    for p in PAPERS:
        r = json.load(open(f"{H}/out_v2/{m}__{p}.json")); t = r["text"]
        mm = re.search(r"\[.*\]", t, re.S)
        try: items = json.loads(mm.group(0))
        except Exception: st["bad_json"] += 1; continue
        for it in items:
            if not isinstance(it, dict): continue
            st["rows"] += 1
            mq, cq = sq(it.get("method_quote") or ""), sq(it.get("comparator_quote") or "")
            a = len(mq) > 5 and mq in txt[p]; b = len(cq) > 5 and cq in txt[p]
            c = it.get("method_score") is not None and sq(it["method_score"]) in mq
            d = it.get("comparator_score") is not None and sq(it["comparator_score"]) in cq
            st["mq_found"] += a; st["cq_found"] += b; st["ms_in_mq"] += c; st["cs_in_cq"] += d; st["all4"] += (a and b and c and d)
            out.append((p, num(it.get("method_score")), num(it.get("comparator_score")), it.get("comparator_type"), it.get("benchmark"), it.get("metric"), it.get("method_name"), it.get("comparator_name")))
    return out, st
(ra, sa), (rb, sb) = rows(A), rows(B)
for m, s in ((A, sa), (B, sb)):
    n = s["rows"]
    print(f"{m}: rows {n}, bad_json {s['bad_json']}, method quote found {100*s['mq_found']/n:.1f}%, comparator quote found {100*s['cq_found']/n:.1f}%, scores inside quotes {100*s['ms_in_mq']/n:.1f}% / {100*s['cs_in_cq']/n:.1f}%, all four checks pass {100*s['all4']/n:.1f}%")
ka = {(p, ms, ct): cs for p, ms, cs, ct, *_ in ra}; kb = {(p, ms, ct): cs for p, ms, cs, ct, *_ in rb}
both = set(ka) & set(kb); union = set(ka) | set(kb)
same = sum(ka[k] == kb[k] for k in both)
print(f"\nmethod-cell x comparator-type slots: {A} {len(ka)}, {B} {len(kb)}, both {len(both)}, union {len(union)}, share of union found by both {100*len(both)/len(union):.1f}%")
print(f"where both filled the same slot, comparator score identical in {same}/{len(both)} = {100*same/len(both):.1f}%")
ta = {(p, ms, cs) for p, ms, cs, *_ in ra}; tb = {(p, ms, cs) for p, ms, cs, *_ in rb}
print(f"exact (method score, comparator score) pairs: both {len(ta&tb)}, union {len(ta|tb)}, Jaccard {len(ta&tb)/len(ta|tb):.2f}")
by = collections.defaultdict(lambda: [0, 0, 0])
for k in ta | tb: by[k[0]][0] += 1; by[k[0]][1] += k in ta and k in tb
print("per paper (pairs in union, pairs both found):", {p: (v[0], v[1]) for p, v in by.items()})
json.dump({"only_A": sorted(map(list, ta - tb), key=str), "only_B": sorted(map(list, tb - ta), key=str)}, open(f"{H}/v2_disagreements.json", "w"))

# slots both filled with different comparator scores
diff = [(k, ka[k], kb[k]) for k in both if ka[k] != kb[k]]
names = {}
for p, ms, cs, ct, bm, me, mn, cn in ra: names[("A", p, ms, ct)] = (bm, cn)
for p, ms, cs, ct, bm, me, mn, cn in rb: names[("B", p, ms, ct)] = (bm, cn)
print("\nslots with different comparator scores:", len(diff))
for (p, ms, ct), x, y in sorted(diff, key=str)[:12]:
    print(f"  {p} method {ms} [{ct}]: {A} {x} ({names[('A',p,ms,ct)][1]}) | {B} {y} ({names[('B',p,ms,ct)][1]})")
only = collections.Counter()
for k in set(ka) - set(kb): only[(A, k[2])] += 1
for k in set(kb) - set(ka): only[(B, k[2])] += 1
print("slots filled by one model only, by comparator type:", dict(only))
