# Model pilot: which models can extract numbers from RAG papers?

Run on 1 November 2026. Ten papers from the gold list (arXiv IDs are in `extract_pilot.py`), six models, one prompt, temperature left at default. Each model was asked to list up to 12 method-versus-comparator comparisons from the main results tables, with an exact quote and page for each value.

Paper texts are not committed (copyright). To rebuild them: `curl -L https://arxiv.org/pdf/<id> -o papers/<id>.pdf` then `pdftotext -layout papers/<id>.pdf papers/<id>.txt`. Raw model outputs are in `out/`. `evaluate_pilot.py` produces the numbers below from `out/`.

## Automatic checks (no human involved)

| Model | Comparisons | Quote found in paper | Method score inside quote | Comparator score exists in paper | Cost, 10 papers |
|---|---|---|---|---|---|
| Claude Haiku 5.5 | 116 | 97.4% | 98.3% | 100% | USD 0.054 |
| Claude Sonnet 5.5 | 119 | 97.5% | 100% | 100% | USD 0.994 |
| DeepSeek V4 Flash | 108 | 79.6% | 94.4% | 100% | USD 0.034 |
| Qwen3 235B | 120 | 87.5% | 40.8% | 100% | USD 0.033 |
| GPT-OSS 120B | 121 | 37.2% | 86.8% | 100% | USD 0.055 |
| Gemma 4 31B | 120 | 10.0% | 98.3% | 99.2% | USD 0.055 |

Total spend: USD 1.23 for 60 paper runs.

## Checked against the papers by Claude (not by a human)

A random sample of 12 rows (6 Haiku, 6 DeepSeek) was checked against the source tables, including the column the number sits in. All 12 were correct (every uncertain case was traced to the right cell). This is a small sample checked by the same assistant family, so it is a smoke test only. The registered human verification still has to be done by the authors and annotators.

## What the pilot shows

1. Numbers are rarely invented. Every model's comparator scores exist in the paper (99% to 100%).
2. Exact quotes separate the models. Haiku and Sonnet copy quotes exactly; Gemma and GPT-OSS usually alter spacing or characters, so the registered "quote must be found in the paper" check would reject most of their rows. DeepSeek is borderline.
3. Models disagree about which comparisons to extract, not about the numbers. Agreement between models on the same (method score, comparator score) pair is only 0.2 to 0.4 (Jaccard), because each model picks a different comparator or a different subset. The registered 95% agreement target cannot be met unless the codebook says exactly which comparisons to extract. This needs a deviation or a codebook update before the extraction pilot.
4. Cost is not the constraint. Extrapolating this pilot to 1,000 papers: about USD 5 (Haiku), USD 3 (DeepSeek), USD 100 (Sonnet).

## Decision for the authors

Proposed pair for extraction: Claude Haiku 5.5 and DeepSeek V4 Flash (different families, as registered), with Sonnet 5.5 only as arbiter where they disagree. DeepSeek needs a stricter quoting instruction and a retry on quotes that are not found. Gemma, Qwen and GPT-OSS are not adopted for extraction on this evidence.

Not yet tested: the 95% agreement target on a fixed set of comparisons, and screening.
