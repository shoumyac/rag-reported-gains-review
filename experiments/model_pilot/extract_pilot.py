"""Pilot: several LLMs extract RAG-vs-baseline comparisons from 10 papers. Quotes are checked automatically."""
import json, os, re, sys, time, urllib.request, concurrent.futures as cf
HERE = os.path.dirname(os.path.abspath(__file__))
ENV = os.path.join(HERE, "..", "..", ".env")  # keys live in the git-ignored .env at the repo root
if os.path.exists(ENV):
    for line in open(ENV):
        if "=" in line and not line.startswith("#"): k, v = line.strip().split("=", 1); os.environ.setdefault(k, v)
PAPERS = ["2310.11511","2401.15884","2403.14403","2310.04408","2301.12652","2305.06983","2310.01352","2311.09210","2302.00083","2407.02485"]
MODELS = {  # name: (provider, id, $/M in, $/M out)
 "haiku-5.5": ("anthropic", "claude-haiku-5-5", 0.10, 0.50),
 "sonnet-5.5": ("anthropic", "claude-sonnet-5-5", 2.0, 10.0),
 "deepseek-v4-flash": ("openrouter", "deepseek/deepseek-v4-flash", 0.091, 0.182),
 "gemma-4-31b": ("openrouter", "google/gemma-4-31b-it", 0.20, 0.40),
 "qwen3-235b": ("openrouter", "qwen/qwen3-235b-a22b-2507", 0.09, 0.55),
 "gpt-oss-120b": ("openrouter", "openai/gpt-oss-120b", 0.15, 0.60),
}
PROMPT = """You are extracting data from one research paper about retrieval-augmented generation (RAG). Use only what the paper states. Never use memory or other papers.

Task: list up to 12 comparisons taken from the paper's MAIN results tables. One comparison = one proposed method versus one comparator, on one benchmark and one metric, where both scores are reported in the paper by the same study.
Comparator types: "no_retrieval" (same or similar model without retrieval), "vanilla_rag" (standard retrieve-then-read baseline), "prior_method" (another published method).
Prefer, for each benchmark in the main table, the comparison of the proposed method against the vanilla RAG or standard retrieval baseline; add no_retrieval comparisons if space remains.

For each comparison return an object with keys:
 benchmark, metric, method_name, method_score, comparator_name, comparator_type, comparator_score, page, quote
Rules:
- Scores are numbers exactly as printed in the paper (do not convert or round).
- quote: an exact copy of at most 25 words from the paper text that contains the method score and the row or caption that identifies it (a table row copied from the text is fine; keep the original spacing and characters). Do not paraphrase.
- page: the page number given in the [PAGE n] marker before the quote.
- If a value is not reported write null. Never guess.
Return only a JSON list, no other text.

PAPER TEXT:
"""
PROMPT_V2 = """You are extracting data from one research paper about retrieval-augmented generation (RAG). Use only what the paper states. Never use memory or other papers.

SELECTION RULE (follow exactly, it decides which rows you output):
1. Find the main results table(s): the table(s) holding the proposed method's headline results on the paper's task benchmarks (at most two tables). Ignore ablations, analyses, appendices, cost or speed tables and metrics that are not task quality (for example citation precision, latency, number of steps).
2. For every benchmark-and-metric column of those tables, and for the proposed method's main row (the row marked as ours; if several variants are marked, use the first one listed), output at most two comparisons:
   (a) versus the "no_retrieval" row: the closest row that uses the same or the smallest-gap generator without retrieval;
   (b) versus the "vanilla_rag" row: the closest row that uses the same or the smallest-gap generator with standard retrieve-then-read retrieval and no special method.
3. If no such row exists in the table, output nothing for that case. Do not use other comparator types. Output at most 24 rows.

For each comparison return an object with keys:
 benchmark, metric, method_name, method_score, comparator_name, comparator_type, comparator_score, page, method_quote, comparator_quote
Rules:
- Scores are numbers exactly as printed (no conversion, no rounding). Write null if not reported. Never guess.
- method_quote and comparator_quote: copy ONE single line of the paper text, character by character, from the row that holds the score (a whole table row is fine, at most 25 words). Do not fix spacing, do not replace symbols, do not paraphrase.
- page: the number in the [PAGE n] marker before the quote.
Return only a JSON list, no other text.

PAPER TEXT:
"""
PROMPT_V3 = """You are extracting data from one research paper about retrieval-augmented generation (RAG). Use only what the paper states. Never use memory or other papers.

Task: copy the paper's main results table(s) into structured form. Main results table = the table(s) holding the proposed method's headline results on task benchmarks (at most two tables; ignore ablations, analyses, appendix, cost or speed tables).
Return a JSON list with one object per table:
 {"caption": short caption or title, "page": page number from the [PAGE n] marker, "columns": [one string per numeric column, in the printed order, in the form "Benchmark / metric" using the printed header words], "rows": [ {"label": printed row label (method or model name), "quote": exact one-line copy of the row from the text, "values": [one entry per column, in the same order, number exactly as printed, or null where the cell is empty, a dash or not applicable]} ]}
Rules:
- Include EVERY data row of the table, in order, including baselines, no-retrieval rows, and the authors' own rows. Skip pure section-heading rows that have no numbers.
- quote: copy the line character by character (do not fix spacing or symbols). If the row spans two lines in the text, copy the line that holds the numbers.
- values: one entry per column; keep the printed text of each number as a string (for example "54.9"). If a cell shows two numbers separated by a slash, keep it as printed in one string.
- Never guess or complete a missing value.
Return only the JSON list, no other text.

PAPER TEXT:
"""
VERSION = os.environ.get("PILOT_VERSION", "v1")
OUT = "out" if VERSION == "v1" else "out_" + VERSION
os.makedirs(f"{HERE}/{OUT}", exist_ok=True)
def paper_text(pid):
    raw = open(f"{HERE}/papers/{pid}.txt", encoding="utf-8", errors="ignore").read()
    return "".join(f"\n[PAGE {i+1}]\n{p}" for i, p in enumerate(raw.split("\f")))
def post(url, headers, body, tries=3):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, json.dumps(body).encode(), headers)
            with urllib.request.urlopen(req, timeout=300) as r: return json.load(r)
        except Exception as e:
            err = repr(e)[:300]
            if hasattr(e, "read"):
                try: err += " " + e.read().decode()[:300]
                except Exception: pass
            time.sleep(3 * (i + 1))
    return {"error": err}
def call(model, pid):
    prov, mid, pin, pout = MODELS[model]
    prompt = {"v1": PROMPT, "v2": PROMPT_V2, "v3": PROMPT_V3}[VERSION] + paper_text(pid)
    if prov == "anthropic":
        d = post("https://api.anthropic.com/v1/messages", {"x-api-key": os.environ["ANTHROPIC_API_KEY"], "anthropic-version": "2023-06-01", "content-type": "application/json"},
                 {"model": mid, "max_tokens": 16000, "messages": [{"role": "user", "content": prompt}]})
        if "error" in d: return {"error": d["error"]}
        return {"text": "".join(b.get("text", "") for b in d["content"] if b.get("type") == "text"), "tin": d["usage"]["input_tokens"], "tout": d["usage"]["output_tokens"]}
    d = post("https://openrouter.ai/api/v1/chat/completions", {"Authorization": "Bearer " + os.environ["OPENROUTER_API_KEY"], "content-type": "application/json"},
             {"model": mid, "max_tokens": 32000, "temperature": 0, "reasoning": {"enabled": False}, "messages": [{"role": "user", "content": prompt}]})
    if "error" in d: return {"error": str(d["error"])}
    if "choices" not in d: return {"error": json.dumps(d)[:300]}
    return {"text": d["choices"][0]["message"].get("content") or "", "tin": d["usage"]["prompt_tokens"], "tout": d["usage"]["completion_tokens"]}
def job(args):
    model, pid = args
    path = f"{HERE}/{OUT}/{model}__{pid}.json"
    if os.path.exists(path) and "error" not in json.load(open(path)): return model, pid, "cached"
    r = call(model, pid); r["model"] = model; r["paper"] = pid
    if "tin" in r: r["cost_usd"] = (r["tin"] * MODELS[model][2] + r["tout"] * MODELS[model][3]) / 1e6
    json.dump(r, open(path, "w"))
    return model, pid, r["error"] if "error" in r else f"ok ${r['cost_usd']:.4f}"
if __name__ == "__main__":
    models = sys.argv[1].split(",") if len(sys.argv) > 1 else list(MODELS)
    papers = sys.argv[2].split(",") if len(sys.argv) > 2 else PAPERS
    with cf.ThreadPoolExecutor(6) as ex:
        for m, p, s in ex.map(job, [(m, p) for m in models for p in papers]): print(m, p, s, flush=True)
