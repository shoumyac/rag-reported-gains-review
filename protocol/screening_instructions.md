# Screening instructions

Project: Do reported gains in retrieval-augmented generation (RAG) survive scrutiny? A systematic review, meta-analysis and evaluation-validity audit.
Authors: Anmita Das, Shoumya Chowdhury.
Version 1.0, 1 November 2026. Part of the OSF registration. Any later change is recorded in the deviations log with a date.

## 1. Who screens

- Screeners: the two authors, plus 1 to 2 independent annotators (students of engineering or machine learning in Bangladesh).
- The annotators screen papers written by the authors, and act as the third person who settles disagreements.
- Nobody screens a paper that they or a co-author of theirs wrote.

## 2. What counts as RAG here

A system in which a language model conditions its output on documents retrieved at inference time. The retrieval step may use a dense, sparse or hybrid retriever, a web search, or a knowledge graph, as long as retrieved text is given to the generator.

## 3. Stage 1: title and abstract

You see only the title and abstract. Authors, venue and year are hidden.

Decide: INCLUDE (go to full text), EXCLUDE, or MAYBE.
- INCLUDE if the abstract suggests the paper runs experiments with a RAG system.
- If unsure, choose MAYBE. MAYBE goes to full text.
- Do not exclude a paper only because the abstract does not mention a baseline. Baselines are checked at full text.
- Do not use what you know about the authors or the venue.

## 4. Stage 2: full text

Check the codes below in order. Record the first one that applies. If none applies, INCLUDE.

| Code | Exclude if |
|------|-----------|
| E1 | Not about retrieval-augmented generation (for example, "RAG" means red-amber-green). |
| E2 | Survey, position paper, tutorial, or dataset description with no new experiments of a RAG method. |
| E3 | No quantitative result on a task metric. |
| E4 | No baseline that the same study evaluates on the same benchmark. |
| E5 | Published or posted before 1 January 2020 or after 30 November 2026. |
| E6 | Not in English. |
| E7 | Full text cannot be accessed after reasonable effort. |
| E8 | Duplicate or earlier version of a study already included (link the versions, count once). |
| E9 | Multimodal-only RAG (text-only RAG is in scope). |

A valid baseline (E4) is any of: no retrieval, vanilla (naive) RAG, or a prior published method, evaluated by the same study with the same benchmark and metric.

## 5. Independence rules

1. Work in your own copy of the screening sheet.
2. Do not look at another screener's decisions until you have finished the batch.
3. Large language model suggestions may be viewed after your own decision. Do not copy them.
4. Do not discuss individual papers before both of you have finished.

## 6. What to record for each paper

Record ID, screener initials, stage, decision, exclusion code (if excluded), a short note (optional), and the date. Never delete a row. To change a decision, add a new row and keep the old one.

## 7. Disagreements

Disagreements are discussed by the two screeners. If they cannot agree, a third person decides: an independent annotator. For a paper by the authors, the independent annotator decides. The numbers of conflicts and their resolutions are reported for each stage.

## 8. Calibration

Before main screening, both authors independently screen the same random sample of 300 records at title and abstract level. Target Cohen's kappa is at least 0.70 (proposed). If it is lower, the criteria are clarified and a new sample of 100 is screened. Annotators screen a shared sample of 50 records and are given feedback before they start.

## 9. Privacy and credit

Only paper metadata and decisions are recorded. Screeners are recorded by initials. Annotators are acknowledged in the paper if they agree.
