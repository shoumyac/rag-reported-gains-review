"""Step 2. Merge the table copies of two models (plus Qwen3 235B as tie-breaker if present), check every row, flag what a human must look at.
Output: data/merged_rows.csv (one row per table row) and data/merge_summary.json."""
import csv, glob, json, re, sys, collections
from common import *
PRIMARY, SECOND, TIE = "haiku-5.5", "gemma-4-31b", "qwen3-235b"
def numtokens(vals, label):
    s = " ".join(str(x) for x in vals if x is not None)
    toks = re.findall(r"(?<![\w.])\d+(?:\.\d+)?(?![\w]|\.\d)", s)
    lab = set(re.findall(r"\d+(?:\.\d+)?", str(label or "")))
    return [t for t in toks if t not in lab]
def load(model, pid):
    path = f"{DATA}/tables/{model}__{pid}.json"
    if not os.path.exists(path): return None
    r = json.load(open(path))
    if "error" in r: return None
    tabs = parse_json_list(r["text"])
    if tabs is None: return None
    rows = []
    for ti, t in enumerate(tabs):
        for ri, row in enumerate(t.get("rows", [])):
            vals = row.get("values", []) or []
            rows.append(dict(table=ti, caption=t.get("caption"), page=t.get("page"), columns=t.get("columns", []), idx=ri, label=row.get("label"), quote=row.get("quote") or "", values=vals, nums=numtokens(vals, row.get("label"))))
    return rows
def match(a_rows, b_rows):
    """Pair rows by normalised quote, then by label plus numbers. Returns dict a_index -> b_index."""
    pairs, used = {}, set()
    bq = collections.defaultdict(list)
    for j, b in enumerate(b_rows): bq[sq(b["quote"])].append(j)
    for i, a in enumerate(a_rows):
        for j in bq.get(sq(a["quote"]), []):
            if j not in used and len(sq(a["quote"])) > 5: pairs[i] = j; used.add(j); break
    bl = collections.defaultdict(list)
    for j, b in enumerate(b_rows):
        if j not in used: bl[(sq(b["label"]), tuple(b["nums"]))].append(j)
    for i, a in enumerate(a_rows):
        if i in pairs: continue
        for j in bl.get((sq(a["label"]), tuple(a["nums"])), []):
            if j not in used: pairs[i] = j; used.add(j); break
    return pairs
def main(papers):
    out, summ = [], collections.Counter()
    for pid in papers:
        txt = sq(open(f"{HERE}/papers/{pid}.txt", encoding="utf-8", errors="ignore").read())
        A, B, C = load(PRIMARY, pid), load(SECOND, pid), load(TIE, pid)
        if A is None and B is None: summ["paper_without_tables"] += 1; out.append(dict(paper=pid, status="no_tables")); continue
        A = A or []; B = B or []
        pr = match(A, B); inv = {j: i for i, j in pr.items()}
        cm = match(A, C) if C else {}
        recs = []
        for i, a in enumerate(A):
            r = dict(a, seen_by=PRIMARY, other=None)
            if i in pr: r["seen_by"] = f"{PRIMARY}+{SECOND}"; r["other"] = B[pr[i]]
            recs.append(r)
        for j, b in enumerate(B):
            if j not in inv: recs.append(dict(b, seen_by=SECOND, other=None))
        for r in recs:
            a_vals = r["values"]; status = "single_model"; chosen = r["values"]; needs = []
            if r["other"] is not None:
                if r["nums"] == r["other"]["nums"]: status = "agree"
                else:
                    status = "conflict"
                    # tie-break with the third model: take the version that matches Qwen's numbers
                    if C is not None:
                        k = next((i for i, a in enumerate(A) if a is not None and sq(a["quote"]) == sq(r["quote"])), None)
                        qrow = None
                        for c in C:
                            if sq(c["quote"]) == sq(r["quote"]) or (sq(c["label"]) == sq(r["label"]) and c["table"] == r["table"]): qrow = c; break
                        if qrow is not None and qrow["nums"] == r["nums"]: status = "conflict_resolved_by_majority"; 
                        elif qrow is not None and qrow["nums"] == r["other"]["nums"]: status = "conflict_resolved_by_majority"; chosen = r["other"]["values"]
                    if status == "conflict": needs.append("models disagree on numbers")
            else:
                needs.append("seen by one model only")
            qf = len(sq(r["quote"])) > 5 and sq(r["quote"]) in txt
            vin = all(val(v) in sq(r["quote"]) for v in chosen if val(v) is not None) if r["quote"] else False
            ncol = len(r["columns"]); nval = len(chosen)
            if not qf: needs.append("quote not found in paper")
            if not vin: needs.append("a value is not in its quote")
            if ncol and nval != ncol: needs.append("value count differs from column count")
            summ["rows"] += 1; summ["status_" + status] += 1; summ["needs_human"] += bool(needs); summ["quote_found"] += qf
            out.append(dict(paper=pid, table_no=r["table"] + 1, caption=r["caption"], page=r["page"], row_no=r["idx"] + 1, label=r["label"], quote=r["quote"],
                            columns=json.dumps(r["columns"], ensure_ascii=False), values=json.dumps(chosen, ensure_ascii=False), seen_by=r["seen_by"], status=status,
                            quote_found=qf, values_in_quote=vin, needs_human="; ".join(needs)))
    keys = ["paper", "table_no", "caption", "page", "row_no", "label", "quote", "columns", "values", "seen_by", "status", "quote_found", "values_in_quote", "needs_human"]
    with open(f"{DATA}/merged_rows.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, keys, extrasaction="ignore"); w.writeheader(); [w.writerow(o) for o in out]
    json.dump(summ, open(f"{DATA}/merge_summary.json", "w"), indent=1); print(dict(summ))
if __name__ == "__main__":
    main(sys.argv[1].split(","))
