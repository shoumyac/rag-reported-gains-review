# Table-first extraction pipeline (deviation D3)

Built and tested on 1 November 2026 on 24 papers (the 10 pilot papers of `experiments/model_pilot/` plus 14 new RAG papers from the gold list; arXiv IDs are the file names in the `data/` outputs). Paper texts and outputs are not committed (`papers/` and `data/` are git-ignored); rebuild a text with `curl -L https://arxiv.org/pdf/<id> -o papers/<id>.pdf && pdftotext -layout papers/<id>.pdf papers/<id>.txt`.

## Steps

| Step | Script | Who does it | Output |
|---|---|---|---|
| 1 | `step1_extract_tables.py` | Claude Haiku 5.5 and Gemma 4 31B each copy the main results table(s) verbatim, one quoted line per row | `data/tables/` |
| 2 | `step2_merge.py` | Script: pairs rows from the two models, checks quotes, values, column counts; Qwen3 235B is used as tie-breaker when the two disagree on numbers (it was not needed in this test) | `data/merged_rows.csv` |
| 3 | `step3_label_rows.py` | Haiku 5.5 labels each row (proposed, no retrieval, vanilla RAG, prior method, other), the generator, and the task-quality columns | `data/labels/` |
| 4 | `step4_build_comparisons.py` | Script only: main proposed row against the no-retrieval row and the vanilla-RAG row for every quality column; same generator first, nearest row otherwise | `data/comparisons.csv` |
| 5 | `step5_review_sheets.py` | Script: sheets for the human checks | `data/review/` |

Human checks required by the registration: (A) confirm the main table once per paper; (B) verify the role labels, comparator choice and both scores of every comparison against the paper, and add the test-set size; (C) check rows that only one model extracted or that failed an automatic check.

## Results of the test (24 papers)

- 505 table rows from 39 tables. Cost: USD 0.27 for table extraction (two models), USD 0.04 for labelling. About USD 0.013 per paper, so roughly USD 15 for 1,000 papers.
- When both models extracted a row they agreed on every number: 377 of 377 rows (100%). This is above the registered 95% target.
- Coverage is the weak point: 128 rows (25%) were extracted by one model only, and 19 rows have a quote not found verbatim in the paper text, 11 have a value not inside its quote. All of these go to sheet C for a human.
- 298 comparisons from 21 papers (159 against no retrieval, 139 against vanilla RAG); 192 used a comparator with the same generator, 106 the nearest row. In 291 of 298 both scores appear inside their own quote (the other 7 are cells with two numbers separated by a slash).
- Three papers gave no comparison (a fine-tuning-versus-retrieval comparison study, a financial-documents study, a best-practices study): they have no "proposed method against baseline" structure, so a human decides whether and how they enter.

## Problems the test found, and what the pipeline does about them

1. Lower-is-better metrics (perplexity, loss): 11 comparisons. The column `improvement_pp` flips the sign; `lower_is_better` marks them for the human check.
2. Retrieval-only metrics (recall@k): 20 comparisons from one paper. They are flagged (`retrieval_metric_flag`) and are outside the registered primary outcome (task metric of the RAG system).
3. Role labelling is the least reliable step. In a 12-comparison read-through, one comparator labelled "vanilla RAG" (a fine-tuned Llama2 7B) was doubtful, and one paper's proposed row was a retrieval-granularity variant, not a method. This is why sheet B asks a human to confirm every role and comparator choice.
4. Slash cells such as "82.9 / 89.5" take the first number; the column header decides which metric that is, and the human check confirms it.
5. Test-set size is not in results tables; the human adds it in sheet B (or from the benchmark documentation, as registered).

## Not yet done

- No human has verified any value. The 12-comparison read-through above was done by Claude and is only a smoke test.
- Tested on arXiv papers with machine-readable text; scanned or two-column PDFs with broken tables will need a separate check.
- Qwen tie-break and the one-model-only rows were not exercised because the two models never disagreed on a shared row.
