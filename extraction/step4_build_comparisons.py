"""Step 4. Build comparisons by script from the merged rows and the row labels (no model involved).
Rule (D2/D3): for the main proposed row of each table and every task-quality column, one comparison against the no-retrieval row and one against the vanilla-RAG row.
Comparator row: the one with the same generator as the proposed row if there is one, otherwise the nearest row (by row position) with that role.
Effect = proposed minus comparator in percentage points (scores on a 0 to 1 scale are multiplied by 100). Test-set size is not in the table and is added at human verification.
Output: data/comparisons.csv"""
import csv, json, collections
from common import *
def pick(cands, main, key):
    if not cands: return None, None
    same = [c for c in cands if c["generator"] and c["generator"] != "unknown" and c["generator"] == main["generator"]]
    if same: return min(same, key=lambda c: abs(c["row_no"] - main["row_no"])), "same_generator"
    return min(cands, key=lambda c: abs(c["row_no"] - main["row_no"])), "nearest_row"
def main():
    rows = list(csv.DictReader(open(f"{DATA}/merged_rows.csv", encoding="utf-8-sig")))
    byp = collections.OrderedDict()
    for r in rows:
        if r.get("status") != "no_tables": byp.setdefault((r["paper"], r["table_no"]), []).append(r)
    out, summ = [], collections.Counter()
    for (pid, tno), rs in byp.items():
        lp = f"{DATA}/labels/{pid}.json"
        if not os.path.exists(lp): continue
        lab = json.load(open(lp)); tabs = parse_json_list(lab.get("text", "")) or []
        t = next((x for x in tabs if str(x.get("table")) == str(tno)), None)
        if not t: summ["table_without_labels"] += 1; continue
        L = {int(x["row_no"]): x for x in t.get("rows", []) if str(x.get("row_no", "")).isdigit()}
        info = []
        for r in rs:
            l = L.get(int(r["row_no"]))
            if l: info.append(dict(row_no=int(r["row_no"]), label=r["label"], role=l.get("role"), main=bool(l.get("main")), generator=(l.get("generator") or "").lower(), values=json.loads(r["values"]), seen_by=r["seen_by"], status=r["status"], needs=r["needs_human"], quote=r["quote"]))
        mains = [i for i in info if i["main"] and i["role"] == "proposed"] or [i for i in info if i["role"] == "proposed"][:1]
        if not mains: summ["table_without_proposed_row"] += 1; continue
        m = mains[0]; cols = json.loads(rs[0]["columns"]); qc = [c for c in t.get("quality_columns", []) if isinstance(c, int)]
        for c in qc:
            if c >= len(m["values"]) or c >= len(cols): continue
            ms = num(m["values"][c])
            if ms is None: continue
            col_all = [num(i["values"][c]) for i in info if c < len(i["values"]) and num(i["values"][c]) is not None]
            scale = 100.0 if col_all and max(col_all) <= 1.0 else 1.0
            for ctype in ("no_retrieval", "vanilla_rag"):
                cands = [i for i in info if i["role"] == ctype and c < len(i["values"]) and num(i["values"][c]) is not None]
                comp, rule = pick(cands, m, ctype)
                if comp is None: summ["no_" + ctype] += 1; continue
                cs = num(comp["values"][c])
                flags = [f for f in (m["needs"], comp["needs"]) if f]
                out.append(dict(paper=pid, table_no=tno, benchmark_metric=cols[c], method=m["label"], method_score=m["values"][c], comparator_type=ctype, comparator=comp["label"], comparator_score=comp["values"][c],
                                effect_pp=round((ms - cs) * scale, 2), scale_x100=scale == 100.0, comparator_rule=rule, method_quote=m["quote"], comparator_quote=comp["quote"], row_flags="; ".join(flags)))
                summ["comparisons"] += 1
    keys = list(out[0].keys())
    with open(f"{DATA}/comparisons.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, keys); w.writeheader(); [w.writerow(o) for o in out]
    print(dict(summ), "papers with comparisons:", len({o["paper"] for o in out}))
if __name__ == "__main__":
    main()
