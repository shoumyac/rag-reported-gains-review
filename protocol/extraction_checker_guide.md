# Extraction check: guide for everyone who checks

Project: Do reported gains in retrieval-augmented generation (RAG) survive scrutiny? A systematic review, meta-analysis and evaluation-validity audit.
Registration: https://doi.org/10.17605/OSF.IO/XGPCZ
Version 1.0, 1 November 2026. Use with the sheets listed in section 2 and with `extraction_instructions.md` (the codebook).

## 1. What this is

Two language models copied the main results table of 24 RAG papers, a script built 298 comparisons from them (a proposed method against a no-retrieval row and against a vanilla RAG row), and a model labelled each table row. Nobody has checked any of it yet. The registration says a human must check every number that enters the main analysis. This round checks a small sample, to measure how accurate the pipeline is and whether two people check the same way. It also sets the process for the full run.

The check is against the paper itself, not against another person or a model. This differs from screening: here you open the paper.

## 2. Who does what

| Person | Sheet | What |
|---|---|---|
| Rasel and Shifa, each on their own | `B_sample_40_for_checkers.csv` | The same 40 comparisons, checked independently. About 2 to 3 hours. |
| Shoumya | `A_main_tables_S.csv` (22 tables, 12 papers) | Confirm which tables are the main results tables. |
| Anmita | `A_main_tables_AD.csv` (17 tables, 11 papers) | Same, for the other 11 papers. |

Rules for Rasel and Shifa: work alone, in your own copy named `check40_<initials>.csv`. Do not discuss any row, and do not look at each other's answers or at the pipeline's answers beyond the sheet, until both of you have sent your file. Do not use ChatGPT, Claude, Gemini or any other AI tool to find or read a value. The authors do not take part in sheet B in this round.

## 3. Open the paper

Every row has an arXiv ID. The paper is at `https://arxiv.org/abs/<id>` (PDF at `https://arxiv.org/pdf/<id>`). Use the latest version.

Two warnings:
- `table_no` in the sheets is the order in which the models extracted the tables, not the number printed in the paper. Find the row by its quote (`method_quote`, `comparator_quote`), which is a line copied from the paper.
- Use the numbers printed in tables or text, not numbers read off plots.

## 4. Sheet B: how to fill each row (Rasel and Shifa)

First read the row: benchmark and metric, the method, the comparator type, the comparator, and the two scores. Then find both lines in the paper's table.

| Column | Write | Meaning |
|---|---|---|
| method_row_ok | YES / NO | The method row is the authors' own main method (the row marked ours; the first variant if several). |
| method_score_ok | YES / NO | The method score is the number in that row and in that column (the benchmark and metric named in `benchmark_metric`). If NO, write the right value in `note`. |
| comparator_role_ok | YES / NO | The comparator row really is of the type stated: `no_retrieval` means the same kind of model without retrieval; `vanilla_rag` means a standard retrieve-then-read baseline with no special method. |
| comparator_choice_ok | YES / NO | Among all rows of that type in the table, this is the closest one: same generator model as the method, or if none, the smallest difference in size. If NO, put the better row's label in `better_comparator_row`. |
| comparator_score_ok | YES / NO | The comparator score is the number in that row and column. If NO, write the right value in `note`. |
| test_set_size | number or NR | The number of test questions or examples for that benchmark, from the paper or the benchmark's documentation. NR if you cannot find it in a few minutes. |
| note | free text | Anything odd, in a few words. Always give the right value when a score is wrong. |
| checker_initials | R or SC | |

Answer YES only when you checked it in the paper. If you cannot decide, write `UNSURE` and say why in `note`; do not guess.

Special cases:
- **Two numbers in one cell** (for example `82.9 / 89.5`): the column header says which metric each number belongs to. The sheet's score keeps both; mark `method_score_ok` YES if the number for the metric in `benchmark_metric` is among them, and say which in `note`.
- **Lower is better** (perplexity, loss): ignore the direction; just check the numbers.
- **The metric is not a task score** (for example recall of retrieved passages, latency, cost): write `OUT OF SCOPE` in `note`. The registered outcome is the task metric of the RAG system.
- **The row is missing from the paper or the table is different**: `NO` in the relevant column, and explain.

## 5. Sheet A: how to fill each row (Shoumya and Anmita)

One row per table that the models extracted. Write YES in `is_main_table` if the table holds the proposed method's headline results on task benchmarks. Write NO for ablations, analyses, appendix, cost or speed tables, and tables of other kinds. At most two tables per paper are main tables. If the models missed a main table, write `MISSING` in `note` with the table number printed in the paper. A paper where no table fits "proposed method against baselines" (a benchmark or best-practices paper, for example) gets `NO MAIN TABLE` in `note`.

## 6. How the checks will be scored

- **Pipeline accuracy** (Rasel and Shifa, separately and combined): the share of rows where `method_score_ok` and `comparator_score_ok` are both YES. Registered target for the primary values: at least 95%.
- **Do you check the same way?** Agreement between Rasel and Shifa on each YES/NO column (Cohen's kappa and percent agreement). Where you differ we look at the row together afterwards and settle it from the paper.
- **Role labelling and comparator choice**: the share of YES in `comparator_role_ok` and `comparator_choice_ok`. These two are the weaker parts of the pipeline, so they decide how much human checking the full run needs.
- Nobody is being graded. A NO is a useful result: it shows where the pipeline needs fixing.

## 7. Sending your file back

Send the finished file only to Shoumya (shoumyac@student.unimelb.edu.au). Suggested deadline: 10 November 2026 (to be confirmed by Shoumya). Keep a short list of rows where the instructions were unclear; that list improves this guide.

## 8. Credit and privacy

Checkers are recorded by initials only. Annotators are named in the paper only with their consent.
