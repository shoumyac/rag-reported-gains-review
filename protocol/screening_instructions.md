# Screening instructions

Project: Do reported gains in retrieval-augmented generation (RAG) survive scrutiny? A systematic review, meta-analysis and evaluation-validity audit.
Authors: Anmita Das, Shoumya Chowdhury.
Version 1.2, 1 November 2026 (version 1.0 is in the OSF registration; the changes are section 3A (deviation D4) and section 3B (deviation D5), recorded in the deviations log). Any later change is recorded in the deviations log with a date.

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

## 3B. Stage 1 clarifications (added in version 1.2, deviation D5)

Agreed by both authors on 1 November 2026 after round 2 (100 records, kappa 0.63 between the authors, below the 0.70 target). Derived from the 22 records on which the authors differed (`experiments/screening_pilot/round2_reconciled_decisions_22.csv`). Where 3B is more specific than 3A, 3B applies.

1. **Image, audio or video tasks (E9).** EXCLUDE (E9) when every task input requires an image, audio or video (for example image-pair change captioning or visual question answering) and there is no text-only task setting, even if the model retrieves from a text corpus. A text-based RAG knowledge base inside a code or text generation framework is INCLUDE even if auxiliary tools convert other data into text.
2. **Multimodal with text.** MAYBE when a multimodal RAG system is tested on benchmarks that combine text and page images, or text queries with video, and the abstract does not say whether a text-only setting is tested. A work-in-progress paper that reports only a preliminary comparison is also MAYBE.
3. **Design-only application papers (E2).** EXCLUDE (E2) when an application paper describes only a proposed platform or architecture and its intended benefits, and the abstract mentions no built artifact, test, dataset or evaluation. EXCLUDE (E2) an organisational pilot or lessons-learned report that mentions RAG only in the keywords and reports no experimental evaluation of a RAG system.
4. **Built but no evaluation stated.** MAYBE when the abstract says a RAG framework or pipeline was built (including with a released demo or repository link), or claims general operational improvement, but does not mention an experiment, metric, test set or baseline.
5. **"Experimentally illustrated" or qualitative evidence only.** MAYBE for a proof of concept that only says it illustrates the approach experimentally; for a deployed RAG tool evaluated only by small focus groups or satisfaction questionnaires; and for a multi-stage pipeline that reports numbers only for a non-RAG module and shows the RAG module only in qualitative case studies.
6. **Evaluation stated without numbers.** INCLUDE when the abstract states that an experimental evaluation or comparison was run and names what improved (for example detection accuracy or response time), for a system that contains a RAG component, even if no numbers appear. INCLUDE when the abstract explicitly says that several language models or settings were compared within a RAG system, even if the comparison is described only in words.
7. **RAG as part of an evaluated workflow.** INCLUDE when a RAG system is a component of an experimentally evaluated workflow with reported quantitative results, even if the study focuses on productivity or human-AI collaboration rather than the RAG architecture.
8. **RAG only as background (E1).** EXCLUDE (E1) when RAG is mentioned only as background motivation for a non-retrieval method, only as planned future work, or only in passing as an existing strategy in a conceptual paper that reports no experiments on a RAG system. EXCLUDE (E1) a software architecture paper that mentions RAG only as an existing practice and demonstrates its framework on non-RAG exemplars.
9. **Retrieval without generation (E1).** EXCLUDE (E1) a paper that evaluates only vector indexing, embedding quantization or similarity search, or only builds a retrieval benchmark and tests embedding retrieval, without a language model generating from the retrieved results.
10. **Semi-parametric language models.** INCLUDE a language model that retrieves text spans or tokens from an external corpus at inference time to condition generation (for example nearest-neighbor decoding) and is experimentally compared with RAG baselines.
11. **Surveys.** EXCLUDE (E2) when the abstract identifies the paper as a survey, review or taxonomy with no new experiments, even if the opening sentences describe an architecture in detail.

Open point to check at full text: the page-image RAG paper D2-ScaleAgent (W7203727208) was set to MAYBE under rule 2, although its retrieved items are page images. If the full text shows no text-only setting, it becomes E9 at Stage 2.

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
