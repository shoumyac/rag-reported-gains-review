"""Stage 1 (title and abstract) screening by several models on the 300-record calibration sample."""
import json, os, re, sys, time, concurrent.futures as cf
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "model_pilot"))
import extract_pilot as E
INSTR = open(os.path.join(HERE, "..", "..", "protocol", "screening_instructions.md")).read()
PROMPT = """You are a screener in a systematic review of retrieval-augmented generation (RAG). Apply the registered Stage 1 rules below to ONE record. You see only the title and abstract. Do not use anything you know about the authors or venue.

RULES (from the registered screening instructions):
- RAG = a system in which a language model conditions its output on documents retrieved at inference time (dense, sparse, hybrid, web search or knowledge-graph retrieval, as long as retrieved text is given to the generator).
- INCLUDE if the title/abstract suggests the paper runs experiments with a RAG system (proposes or evaluates a RAG method, or compares RAG with other settings).
- EXCLUDE if clearly: E1 not about RAG (for example "RAG" means red-amber-green, or retrieval without a generator conditioning on it); E2 survey, review, position paper, tutorial or dataset/resource description with no new experiments of a RAG method; E9 multimodal-only RAG (text-only RAG is in scope).
- MAYBE if unsure, or if there is no abstract and the title alone is not enough. Do not exclude only because the abstract does not mention a baseline or metrics.

Return only JSON: {"decision": "INCLUDE" | "EXCLUDE" | "MAYBE", "code": "E1" | "E2" | "E9" | null, "reason": "at most 15 words"}

TITLE: %s
ABSTRACT: %s
"""
MODELS = ["haiku-5.5", "sonnet-5.5", "gemma-4-31b", "qwen3-235b", "deepseek-v4-flash"]
OUT = os.path.join(HERE, "out"); os.makedirs(OUT, exist_ok=True)
def call(model, prompt):
    prov, mid, pin, pout = E.MODELS[model]
    if prov == "anthropic":
        d = E.post("https://api.anthropic.com/v1/messages", {"x-api-key": os.environ["ANTHROPIC_API_KEY"], "anthropic-version": "2023-06-01", "content-type": "application/json"},
                   {"model": mid, "max_tokens": 3000, "messages": [{"role": "user", "content": prompt}]})
        if "error" in d: return None, 0
        return "".join(b.get("text", "") for b in d["content"] if b.get("type") == "text"), (d["usage"]["input_tokens"] * pin + d["usage"]["output_tokens"] * pout) / 1e6
    d = E.post("https://openrouter.ai/api/v1/chat/completions", {"Authorization": "Bearer " + os.environ["OPENROUTER_API_KEY"], "content-type": "application/json"},
               {"model": mid, "max_tokens": 4000, "temperature": 0, "reasoning": {"enabled": False}, "messages": [{"role": "user", "content": prompt}]})
    if "choices" not in d: return None, 0
    u = d["usage"]; return d["choices"][0]["message"].get("content") or "", (u["prompt_tokens"] * pin + u["completion_tokens"] * pout) / 1e6
def job(a):
    model, r = a; path = f"{OUT}/{model}__{r['id']}.json"
    if os.path.exists(path): return 0
    txt, cost = call(model, PROMPT % (r["title"], r["abstract"] or "(no abstract available)"))
    dec = None
    if txt:
        m = re.search(r"\{.*\}", txt, re.S)
        try: dec = json.loads(m.group(0))
        except Exception: dec = None
    json.dump({"model": model, "id": r["id"], "raw": txt, "parsed": dec, "cost_usd": cost}, open(path, "w"))
    return cost
if __name__ == "__main__":
    recs = json.load(open(f"{HERE}/raw/sample_300.json"))
    models = sys.argv[1].split(",") if len(sys.argv) > 1 else MODELS
    tot = 0
    with cf.ThreadPoolExecutor(10) as ex:
        for c in ex.map(job, [(m, r) for m in models for r in recs]): tot += c
    print("done, cost this run", round(tot, 3))
