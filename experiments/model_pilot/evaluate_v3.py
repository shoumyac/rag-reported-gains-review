"""Evaluate v3 (table-first) extraction: row coverage and cell-value agreement between two models."""
import json, re, os, collections, sys
H = os.path.dirname(os.path.abspath(__file__))
PAPERS = ["2310.11511","2401.15884","2403.14403","2310.04408","2301.12652","2305.06983","2310.01352","2311.09210","2302.00083","2407.02485"]
A, B = (sys.argv[1], sys.argv[2]) if len(sys.argv) > 2 else ("haiku-5.5", "deepseek-v4-flash")
sq = lambda s: re.sub(r"[^a-z0-9.%/]", "", str(s).lower())
txt = {p: sq(open(f"{H}/papers/{p}.txt", encoding="utf-8", errors="ignore").read()) for p in PAPERS}
def val(v):
    if v is None: return None
    v = str(v).strip()
    return None if v in ("", "-", "–", "—", "null", "None", "n/a", "N/A") else sq(v)
def load(m):
    rows = {}; st = collections.Counter()
    for p in PAPERS:
        r = json.load(open(f"{H}/out_v3/{m}__{p}.json"))
        mm = re.search(r"\[.*\]", r["text"], re.S)
        try: tables = json.loads(mm.group(0))
        except Exception: st["bad_json"] += 1; continue
        for t in tables:
            st["tables"] += 1
            for row in t.get("rows", []):
                q = sq(row.get("quote") or ""); vals = [val(x) for x in row.get("values", [])]
                st["rows"] += 1; st["cells"] += sum(v is not None for v in vals)
                qf = len(q) > 5 and q in txt[p]; st["quote_found"] += qf
                nn = [v for v in vals if v is not None]
                inq = sum(v in q for v in nn); st["cells_in_quote"] += inq; st["cells_nonnull"] += len(nn)
                rows[(p, q)] = (vals, row.get("label"), t.get("page"))
    return rows, st
ra, sa = load(A); rb, sb = load(B)
for m, s in ((A, sa), (B, sb)):
    print(f"{m}: tables {s['tables']}, rows {s['rows']}, non-empty cells {s['cells']}, bad_json {s['bad_json']}, row quote found {100*s['quote_found']/s['rows']:.1f}%, cell value inside its row quote {100*s['cells_in_quote']/max(1,s['cells_nonnull']):.1f}%")
both = set(ra) & set(rb); union = set(ra) | set(rb)
print(f"\nrows: {A} {len(ra)}, {B} {len(rb)}, both {len(both)}, union {len(union)}, share of union extracted by both {100*len(both)/len(union):.1f}%")
pos_eq = tot = set_eq = 0; bad = []
cellsame = cellall = 0
for k in both:
    va, vb = ra[k][0], rb[k][0]
    na = [x for x in va if x is not None]; nb = [x for x in vb if x is not None]
    if na == nb: set_eq += 1
    else: bad.append((k[0], ra[k][1], na[:6], nb[:6]))
    # per-cell positional agreement over the non-empty cells of either
    n = max(len(va), len(vb)); va = va + [None]*(n-len(va)); vb = vb + [None]*(n-len(vb))
    for x, y in zip(va, vb):
        if x is None and y is None: continue
        cellall += 1; cellsame += (x == y)
print(f"matched rows with identical non-empty value lists: {set_eq}/{len(both)} = {100*set_eq/len(both):.1f}%")
print(f"cell-level agreement over matched rows (position by position): {cellsame}/{cellall} = {100*cellsame/cellall:.1f}%")
print("first mismatching rows:")
for b in bad[:8]: print("  ", b)
miss = collections.Counter(k[0] for k in union - both)
print("rows extracted by only one model, per paper:", dict(miss))

# --- Second view: compare the numbers only (ignores how each model split slash cells or whether it
# copied a model-size or label token into a value slot). Column alignment is checked separately.
def numtokens(vals, label):
    s = " ".join(str(x) for x in vals if x is not None)
    toks = re.findall(r"(?<![\w.])\d+(?:\.\d+)?(?![\w]|\.\d)", s)
    lab = set(re.findall(r"\d+(?:\.\d+)?", str(label or "")))
    return [t for t in toks if t not in lab]
raw = {}
def loadraw(m):
    out = {}
    for p in PAPERS:
        r = json.load(open(f"{H}/out_v3/{m}__{p}.json"))
        try: tables = json.loads(re.search(r"\[.*\]", r["text"], re.S).group(0))
        except Exception: continue
        for t in tables:
            for row in t.get("rows", []):
                out[(p, sq(row.get("quote") or ""))] = numtokens(row.get("values", []), row.get("label"))
    return out
na_, nb_ = loadraw(A), loadraw(B)
both2 = set(na_) & set(nb_)
same = [k for k in both2 if na_[k] == nb_[k]]
tok_total = sum(max(len(na_[k]), len(nb_[k])) for k in both2)
tok_same = sum(sum(x == y for x, y in zip(na_[k], nb_[k])) for k in both2)
print(f"\nNumbers only: rows with identical number lists {len(same)}/{len(both2)} = {100*len(same)/len(both2):.1f}%; number-by-number {tok_same}/{tok_total} = {100*tok_same/tok_total:.1f}%")
diff = [k for k in both2 if na_[k] != nb_[k]]
for k in diff[:10]: print("  ", k[0], na_[k][:8], "|", nb_[k][:8])
# agreement on the number *set* per row regardless of order
setsame = sum(sorted(na_[k]) == sorted(nb_[k]) for k in both2)
print(f"same numbers ignoring order: {setsame}/{len(both2)} = {100*setsame/len(both2):.1f}%")
