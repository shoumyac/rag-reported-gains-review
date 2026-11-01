"""Shared helpers for the table-first extraction pipeline (deviation D3)."""
import json, os, re, sys, time, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
for l in open(os.path.join(ROOT, ".env")):
    if "=" in l and not l.startswith("#"): k, v = l.strip().split("=", 1); os.environ.setdefault(k, v)
DATA = os.path.join(HERE, "data"); os.makedirs(DATA, exist_ok=True)
MODELS = {  # name: (provider, id, USD per M input, USD per M output)
    "haiku-5.5": ("anthropic", "claude-haiku-5-5", 0.10, 0.50),
    "gemma-4-31b": ("openrouter", "google/gemma-4-31b-it", 0.20, 0.40),
    "qwen3-235b": ("openrouter", "qwen/qwen3-235b-a22b-2507", 0.09, 0.55),
}
def sq(s): return re.sub(r"[^a-z0-9.%/]", "", str(s).lower())
def paper_text(pid):
    raw = open(f"{HERE}/papers/{pid}.txt", encoding="utf-8", errors="ignore").read()
    return "".join(f"\n[PAGE {i+1}]\n{p}" for i, p in enumerate(raw.split("\f")))
def post(url, headers, body, tries=3):
    err = ""
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, json.dumps(body).encode(), headers), timeout=300) as r: return json.load(r)
        except Exception as e:
            err = repr(e)[:300]
            if hasattr(e, "read"):
                try: err += " " + e.read().decode()[:300]
                except Exception: pass
            time.sleep(3 * (i + 1))
    return {"error": err}
def call(model, prompt, max_tokens=16000):
    prov, mid, pin, pout = MODELS[model]
    if prov == "anthropic":
        d = post("https://api.anthropic.com/v1/messages", {"x-api-key": os.environ["ANTHROPIC_API_KEY"], "anthropic-version": "2023-06-01", "content-type": "application/json"},
                 {"model": mid, "max_tokens": max_tokens, "messages": [{"role": "user", "content": prompt}]})
        if "error" in d: return {"error": str(d["error"])}
        r = {"text": "".join(b.get("text", "") for b in d["content"] if b.get("type") == "text"), "tin": d["usage"]["input_tokens"], "tout": d["usage"]["output_tokens"]}
    else:
        d = post("https://openrouter.ai/api/v1/chat/completions", {"Authorization": "Bearer " + os.environ["OPENROUTER_API_KEY"], "content-type": "application/json"},
                 {"model": mid, "max_tokens": 32000, "temperature": 0, "reasoning": {"enabled": False}, "messages": [{"role": "user", "content": prompt}]})
        if "error" in d: return {"error": str(d["error"])}
        if "choices" not in d: return {"error": json.dumps(d)[:300]}
        r = {"text": d["choices"][0]["message"].get("content") or "", "tin": d["usage"]["prompt_tokens"], "tout": d["usage"]["completion_tokens"]}
    r["cost_usd"] = (r["tin"] * pin + r["tout"] * pout) / 1e6
    return r
def parse_json_list(text):
    m = re.search(r"\[.*\]", text, re.S)
    if not m: return None
    try: return json.loads(m.group(0))
    except Exception: return None
def val(v):
    """Normalised cell value: None for empty cells, else the printed text reduced to comparable characters."""
    if v is None: return None
    v = str(v).strip()
    return None if v in ("", "-", "–", "—", "null", "None", "n/a", "N/A") else sq(v)
def num(v):
    """First number in a printed cell, as float, or None."""
    if v is None: return None
    m = re.search(r"-?\d+(?:\.\d+)?", str(v))
    return float(m.group(0)) if m else None
