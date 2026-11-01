"""Step 3. Label each table row (proposed method, no retrieval, vanilla RAG, prior method, other) and mark the task-quality columns.
One call per paper, Claude Haiku 5.5. A human checks the labels (step 5). Output: data/labels/<paper>.json"""
import csv, json, sys, os, concurrent.futures as cf, collections
from common import *
MODEL = "haiku-5.5"
os.makedirs(f"{DATA}/labels", exist_ok=True)
PROMPT = """You are labelling the rows of results tables from one research paper about retrieval-augmented generation (RAG). Use only the paper text and the tables below. Never use memory.

For every row give:
 role: one of
   "proposed"      the authors' own method or one of its variants (rows marked ours, or named in the title or abstract as the contribution)
   "no_retrieval"  a language model used WITHOUT retrieval (closed-book, plain prompting, fine-tuned without retrieval)
   "vanilla_rag"   a standard retrieve-then-read baseline with no special method (for example a retriever plus the same generator, or "Ret-<model>")
   "prior_method"  another published method (with or without retrieval) that is not a plain baseline
   "other"         anything else (oracle, human, ablation of the authors' method, a different task, a closed commercial system without a clear category)
 main: true for the single row that is the authors' main proposed method (the first one if several variants are marked), otherwise false
 generator: the generator model of that row in a short normalised form such as "llama2-13b", "chatgpt", "t5-large", or "unknown"
 why: at most 12 words

Also, for each table, list quality_columns: the zero-based indexes of columns that hold a task quality metric (accuracy, exact match, F1, ROUGE, FactScore and similar). Leave out cost, speed, citation, fluency-only or count columns.

Return only JSON: [{"table": <table number as given>, "quality_columns": [..], "rows": [{"row_no": <row number as given>, "role": "...", "main": false, "generator": "...", "why": "..."}]}]

PAPER BEGINNING (title, abstract and start of introduction):
{head}

TABLES:
{tables}
"""
def tables_for(pid, rows):
    by = collections.OrderedDict()
    for r in rows: by.setdefault(r["table_no"], []).append(r)
    s = []
    for t, rs in by.items():
        s.append(f"Table {t}: {rs[0]['caption']}\nColumns: " + "; ".join(f"[{i}] {c}" for i, c in enumerate(json.loads(rs[0]['columns']))))
        for r in rs: s.append(f"  row {r['row_no']}: {r['label']} | " + " | ".join(str(v) for v in json.loads(r['values'])))
    return "\n".join(s)
def job(a):
    pid, rows = a; path = f"{DATA}/labels/{pid}.json"
    if os.path.exists(path) and "error" not in json.load(open(path)): return pid, "cached"
    head = open(f"{HERE}/papers/{pid}.txt", encoding="utf-8", errors="ignore").read()[:6000]
    r = call(MODEL, PROMPT.replace("{head}", head).replace("{tables}", tables_for(pid, rows)), 8000); r["paper"] = pid
    json.dump(r, open(path, "w"))
    return pid, r.get("error") or f"ok ${r['cost_usd']:.4f}"
if __name__ == "__main__":
    allrows = list(csv.DictReader(open(f"{DATA}/merged_rows.csv", encoding="utf-8-sig")))
    byp = collections.OrderedDict()
    for r in allrows:
        if r.get("status") != "no_tables": byp.setdefault(r["paper"], []).append(r)
    with cf.ThreadPoolExecutor(6) as ex:
        for pid, s in ex.map(job, byp.items()): print(pid, s, flush=True)
