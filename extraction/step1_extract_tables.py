"""Step 1. Models copy the main results table(s) of each paper verbatim (prompt from experiments/model_pilot, PROMPT_V3).
Usage: python3 step1_extract_tables.py MODEL[,MODEL] PAPER[,PAPER...]   Output: data/tables/<model>__<paper>.json"""
import sys, os, json, concurrent.futures as cf
from common import *
PROMPT = open(os.path.join(HERE, "prompt_tables.txt")).read()
os.makedirs(f"{DATA}/tables", exist_ok=True)
def job(a):
    m, p = a; path = f"{DATA}/tables/{m}__{p}.json"
    if os.path.exists(path) and "error" not in json.load(open(path)): return m, p, "cached"
    r = call(m, PROMPT + paper_text(p)); r.update(model=m, paper=p)
    json.dump(r, open(path, "w"))
    return m, p, r.get("error") or f"ok ${r['cost_usd']:.4f}"
if __name__ == "__main__":
    models, papers = sys.argv[1].split(","), sys.argv[2].split(",")
    with cf.ThreadPoolExecutor(6) as ex:
        for m, p, s in ex.map(job, [(m, p) for m in models for p in papers]): print(m, p, s, flush=True)
