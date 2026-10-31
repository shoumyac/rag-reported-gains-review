# Extraction instructions and codebook

Project: Do reported gains in retrieval-augmented generation (RAG) survive scrutiny? A systematic review, meta-analysis and evaluation-validity audit.
Authors: Anmita Das, Shoumya Chowdhury.
Version 1.0, 1 November 2026. Part of the OSF registration. Any later change is recorded in the deviations log with a date.

## 1. Who extracts

- Two large language models extract independently (different model families, exact versions and run dates logged).
- Humans verify: the two authors and 1 to 2 independent annotators (students of engineering or machine learning in Bangladesh).
- Papers written by the authors are verified only by an independent annotator.

## 2. General rules

1. Extract only what the paper states. Never fill a value from memory, from another paper, or by guessing.
2. If a value is not reported, write NR (not reported). If it is unclear, write UNCLEAR and explain in the note.
3. Every extracted value must have: the page number, the table or figure or section, and a short quoted span (at most 25 words) copied exactly from the paper. A value without a quote is not accepted.
4. Take numbers from tables or text, not from plots, unless nothing else exists. If read from a plot, mark it as PLOT.
5. Record scores as in the paper, then convert to percentage points (0 to 100) in a separate column. Keep both.
6. One row per comparison: a RAG method versus one comparator, on one benchmark, with one metric.
7. Use the main metric the authors declare. If none is declared, use the first metric in the main results table and note that.
8. Do not extract from ablation tables, unless the ablation is the only comparison of a RAG method with a baseline.
9. If the paper has several experiments with different test sets, extract each as its own comparison.

## 3. Entities (one row per comparison unless stated)

| Group | Field | Notes |
|-------|-------|-------|
| Metadata | record_id, DOI or arXiv ID, title, year, venue, venue type (peer reviewed / preprint), source file hash | Per paper |
| Metadata | is_review_team_paper | Set by script, not by the extractor |
| Study | task (open-domain QA, multi-hop QA, long-form, fact verification, domain QA, other), domain, language of benchmark | |
| System | retriever type (sparse, dense, hybrid, web search, graph, other), retriever model | |
| System | generator family, generator model, size (parameters) | Closed model: give name and date if stated |
| System | corpus used for retrieval, number of retrieved passages, reranker (yes/no) | |
| Comparison | method name, comparator name, comparator type (no retrieval, vanilla RAG, prior method) | |
| Comparison | benchmark name, test-set size, metric name, metric type (EM, F1, accuracy, LLM-judged, other) | |
| Outcome | score of method, score of comparator (as reported), both converted to points | |
| Outcome | variance reported (SD, SE or CI), number of runs or seeds, significance test reported (yes/no, which, p) | |
| Judge | if LLM-judged: judge model, judge prompt reported (yes/no), judge validated against humans (yes/no, how, result) | |
| Reporting | code available, data available, prompts reported, model versions reported, random seeds reported, hyperparameters of baselines reported | Yes / no / partial |
| Quality | baseline tuned with similar effort (yes/no/unclear), same retriever and generator for method and comparator (yes/no/unclear), test-set leakage discussed (yes/no), compute budget compared (yes/no) | Risk of bias indicators |
| Quality | claims in abstract (state the headline claim in one sentence, quoted) | |

## 4. Stages

1. Pilot: extract 20 papers, compare, fix the codebook. If the codebook changes, update this file and the registration.
2. Automatic extraction: two language models extract each paper into a fixed structured format. Settings and prompts are saved.
3. Automatic checks: each quoted span must be found in the paper text; each number must appear in the quoted span; scores must be within valid ranges.
4. Human verification (see the OSF form for the sample size).
5. Reconciliation of disagreements and final data freeze before analysis.

## 5. Human verification

For each row, the verifier sees the extracted value, the page, and the quote, and checks it against the paper. The verifier marks CORRECT, CORRECTED (with the right value) or CANNOT FIND. The verifier does not see which model produced which value.

## 6. Disagreements

If the two models disagree, or the human corrects a value, the human decides from the paper. If two humans disagree, they discuss. If they cannot agree, a third person decides, and the case is logged.

## 7. Privacy and credit

Only paper data and initials of verifiers are recorded. Annotators are acknowledged with their consent.
