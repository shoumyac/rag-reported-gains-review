# Screening instructions

Project: Do reported gains in retrieval-augmented generation (RAG) survive scrutiny? A systematic review, meta-analysis and evaluation-validity audit.
Authors: Anmita Das, Shoumya Chowdhury.
Version 1.1, 1 November 2026 (version 1.0 is in the OSF registration; the changes are section 3A and are recorded as deviation D4 in the deviations log). Any later change is recorded in the deviations log with a date.

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

## 3A. Stage 1 clarifications (added in version 1.1, deviation D4)

Agreed by both authors on 1 November 2026 after the 300-record calibration pilot (kappa 0.62 between the authors, below the 0.70 target). They apply to title and abstract screening only. Codes and the full-text rules in section 4 are unchanged.

1. **Applications, systems and designs.** EXCLUDE (E2) only if the abstract describes a design, architecture, proposal, plan, vision, overview, survey or whitepaper, lists projected targets instead of results, or plans a future evaluation. Also EXCLUDE (E2) for organisational or qualitative case studies of RAG adoption that report no experiments on a RAG system. If the abstract says the system was built, implemented or deployed but does not say whether it was tested, choose MAYBE. If it reports tests, metrics, user-study results or comparisons, INCLUDE.
2. **RAG as one part of a larger system.** INCLUDE if the abstract reports experiments on a system that uses retrieval-augmented generation, even as one component of the evaluated method. If the abstract mixes qualitative reflection with partial experiments, or a platform or demo enables RAG comparison without clear quantitative results, choose MAYBE.
3. **When RAG does not count (E1).** EXCLUDE (E1) if: RAG appears only as background or future work; RAG appears only as a baseline that the paper's own non-RAG method outperforms; the word means something else; retrieval feeds a generator that is not a language model; retrieval is used only to build a knowledge base or dataset for later RAG and the experiments do not evaluate RAG at query time; or "GraphRAG" or similar wording refers to graph learning on non-language data with no language model generating from retrieved documents.
4. **Surveys.** EXCLUDE (E2) overviews and surveys, including those titled "architecture, techniques and evaluations".
5. **Records with no abstract.** First try to recover the abstract (for example from Crossref or arXiv). If it cannot be recovered: a title that names RAG or retrieval-augmented generation gives MAYBE; a title that names a language-model system, agent, chatbot or assistant but not RAG or retrieval gives EXCLUDE (E1); a title about unrelated topics gives EXCLUDE (E1).
6. **Multimodal (E9).** EXCLUDE (E9) when retrieval and generation work on images, audio, video or other non-text data and the abstract suggests no text-only RAG experiment. MAYBE when text-only and multimodal parts are both present or the abstract does not say. If the retrieval-augmented language-model part works on text and the abstract reports its results, INCLUDE even if other modules process images or sensor data.

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
