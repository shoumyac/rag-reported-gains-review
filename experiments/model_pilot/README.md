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

## Round 2: with a fixed selection rule (deviation D2)

Same ten papers, Haiku 5.5 and DeepSeek V4 Flash, prompt `PROMPT_V2` in `extract_pilot.py` (run with `PILOT_VERSION=v2`; outputs in `out_v2/`; numbers from `python3 evaluate_v2.py`). The first DeepSeek run returned nothing because its hidden reasoning used up the token limit; reasoning was switched off and the runs repeated. Cost of round 2: about USD 0.15 in total.

| Check | Haiku 5.5 | DeepSeek V4 Flash |
|---|---|---|
| Comparisons extracted | 164 | 207 |
| Both quotes found in the paper | 100% | 97.6% |
| Both scores inside their quotes | 94.5% | 100% |
| All four automatic checks pass | 94.5% | 97.6% |

Agreement between the two models: they filled the same slot (same method cell and comparator type) in 124 cases, and gave the same comparator score in 105 of them (84.7%). This is below the registered 95% target. Exact pairs of scores overlap with Jaccard 0.45, up from about 0.3 in round 1.

Why they differ: almost always baseline-row ambiguity, not misread numbers. Examples: "Top 5 documents" versus "Top 1 document" as the vanilla RAG row (RECOMP), Llama2 7B with retrieval versus Alpaca 7B (Self-RAG), different generator sizes as the no-retrieval row. Both models took the numbers correctly from the rows they chose.

Proposed next step (not yet done): extract the whole main results table verbatim (every row and column, one-line quotes) so the models must agree on cell values, then label row types (no retrieval, vanilla RAG, prior method) in a separate step that humans check, and build comparisons by script.

## Round 3: table-first extraction (deviation D3)

The model copies the whole main results table verbatim (every row, one-line quote per row, values per column). Comparisons are then built by script and row types are labelled in a separate, human-checked step. Prompt `PROMPT_V3`, run with `PILOT_VERSION=v3`, outputs in `out_v3/`, numbers from `python3 evaluate_v3.py <modelA> <modelB>`. Cost of round 3: about USD 0.25 for five models on ten papers.

Compared with Claude Haiku 5.5 (187 rows, 1,196 cells; all quotes found; every row has the right number of values):

| Second model | Row quote found | Value count = column count | Rows extracted by both | Same numbers on shared rows | Cost, 10 papers |
|---|---|---|---|---|---|
| Gemma 4 31B | 95.5% | 100% | 83.8% of union | 100% (176 rows, 1,214 numbers) | about USD 0.03 |
| Qwen3 235B | 99.0% | 92.7% | 81.3% of union | 100% (170 rows, 1,179 numbers) | about USD 0.03 |
| DeepSeek V4 Flash | 94.8% | 22.2% | 75.8% of union | 97.5% of rows, 99.3% of numbers (the 4 differences are a section sign read as a number) | USD 0.02 |
| GPT-OSS 120B | not run: the endpoint forces hidden reasoning and the run failed | | | | |

Reading the table:
- When two models extract the same table row, they agree on the numbers 97.5% to 100% of the time, above the registered 95% target. The task is now easy for models.
- The remaining disagreement is which table counts as "main" and how many rows are extracted (coverage 76% to 84% of the union). In this pilot it comes mostly from two papers with several large tables (In-Context RALM, RankRAG).
- DeepSeek often splits slash cells or copies model-size labels into value slots, so its values do not line up with column headers (22% aligned). It is not suitable for table extraction in this form.
- Quote validity and number agreement say nothing about whether both models share the same mistake. The registered human verification of the primary values is still needed.

Proposed setup for extraction: Claude Haiku 5.5 plus Gemma 4 31B, with Qwen3 235B as tie-breaker in place of Sonnet; a human confirms the list of main tables once per paper; the union of rows from both models is kept, and rows seen by only one model are verified by a human.
