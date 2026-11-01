"""Step 5. Sheets for the human checks that the registered protocol requires. Output in data/review/:
 A_main_tables_to_confirm.csv   one row per extracted table: is it the main results table? (once per paper)
 B_comparisons_to_verify.csv    one row per comparison: are role labels, comparator choice and both scores right? (primary values, 100%)
 C_rows_seen_by_one_model.csv   rows that only one model extracted or that failed an automatic check"""
import csv, collections, os
from common import *
os.makedirs(f"{DATA}/review", exist_ok=True)
R = list(csv.DictReader(open(f"{DATA}/merged_rows.csv", encoding="utf-8-sig")))
C = list(csv.DictReader(open(f"{DATA}/comparisons.csv", encoding="utf-8-sig")))
def w(name, rows, keys):
    with open(f"{DATA}/review/{name}", "w", newline="", encoding="utf-8-sig") as f:
        d = csv.DictWriter(f, keys, extrasaction="ignore"); d.writeheader(); [d.writerow(r) for r in rows]
t = collections.OrderedDict()
for r in R:
    if r.get("status") == "no_tables": continue
    k = (r["paper"], r["table_no"]); t.setdefault(k, dict(paper=r["paper"], table_no=r["table_no"], caption=r["caption"], page=r["page"], rows=0)); t[k]["rows"] += 1
w("A_main_tables_to_confirm.csv", [dict(v, is_main_table="", note="") for v in t.values()], ["paper", "table_no", "caption", "page", "rows", "is_main_table", "note"])
w("B_comparisons_to_verify.csv", [dict(c, roles_and_comparator_ok="", scores_match_paper="", test_set_size="", note="", checker_initials="") for c in C],
  ["paper", "table_no", "benchmark_metric", "method", "method_score", "comparator_type", "comparator", "comparator_score", "improvement_pp", "lower_is_better", "retrieval_metric_flag", "comparator_rule", "row_flags", "method_quote", "comparator_quote", "roles_and_comparator_ok", "scores_match_paper", "test_set_size", "note", "checker_initials"])
w("C_rows_seen_by_one_model.csv", [dict(r, correct="", note="") for r in R if r.get("needs_human")], ["paper", "table_no", "page", "row_no", "label", "quote", "values", "seen_by", "needs_human", "correct", "note"])
print({n: sum(1 for _ in open(f"{DATA}/review/{n}", encoding="utf-8-sig")) - 1 for n in os.listdir(f"{DATA}/review")})
