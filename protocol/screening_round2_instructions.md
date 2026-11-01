# Screening round 2: instructions for screeners

Project: Do reported gains in retrieval-augmented generation (RAG) survive scrutiny? A systematic review, meta-analysis and evaluation-validity audit.
Registration: https://doi.org/10.17605/OSF.IO/XGPCZ
Version 1.0, 1 November 2026. Use with `screening_sheet_round2_100_for_humans.csv` and the rules in `screening_instructions.md` version 1.1, section 3A.

## 1. What this is

After the first pilot (300 records) the two authors agreed only moderately (kappa 0.59 on three classes, 0.62 on EXCLUDE versus keep). The rules were clarified in writing (version 1.1). Round 2 tests whether the clearer rules give better agreement, on 100 new random records.

| Person | Records |
|---|---|
| All four screeners (the two authors and the two annotators) | All 100 rows |

Target: kappa of at least 0.70 between the two authors. If it is still lower, we discuss the differences once more, refine the rules and repeat. The annotators' results are used to check how clear the rules are for people who were not in the discussion.

## 2. Independence rules (same as before)

1. Work alone, in your own copy of the file. Rename it `round2_<your initials>.csv`.
2. Do not discuss any record, and do not look at anyone's answers, until everybody has sent their file.
3. Do not look up papers, open full texts or search for authors. Use the title and abstract in the file only.
4. Do not use ChatGPT, Claude, Gemini or any other AI tool.
5. A dictionary or translator is fine.
6. If a record is a paper that you or your co-author wrote, leave the decision blank and write `OWN` in the note column.

## 3. The file

Keep it as a CSV (UTF-8). Do not sort, delete or move rows or columns, and do not change the first three columns.

| Column | What to do |
|---|---|
| decision | Exactly one of `INCLUDE`, `EXCLUDE`, `MAYBE`. |
| code | If EXCLUDE: `E1`, `E2`, `E6` (not English) or `E9`. Otherwise blank. |
| note | A few words when the case was hard, or `OWN`. Short notes help the later discussion. |
| screener_initials, date | On every row you complete. |

Some records show "(no abstract)". We tried to recover missing abstracts, so a few records still have none. Follow rule 5 below.

## 4. How to decide

Ask in this order and use the first rule that applies. The complete wording is in section 3A of `screening_instructions.md` (version 1.1). Short version:

1. **Not about RAG, or not English.** EXCLUDE E1 or E6. E1 also covers: RAG only as background or future work; RAG only as a baseline that the paper's own non-RAG method beats; "RAG" meaning something else; retrieval feeding a generator that is not a language model; retrieval used only to build a knowledge base or dataset for later RAG; "GraphRAG" wording on non-language data.
2. **Survey, overview or position paper, or design only.** EXCLUDE E2. This includes designs, architectures, proposals, plans, visions, whitepapers, projected targets instead of results, a future evaluation, and organisational or qualitative case studies with no experiments on a RAG system.
3. **Only images, audio, video or other non-text.** EXCLUDE E9. If text-only and multimodal parts both appear, or the abstract does not say, MAYBE.
4. **Experiments with a RAG system, even as one component of the evaluated method.** INCLUDE.
5. **No abstract.** The title names RAG or retrieval-augmented generation: MAYBE (EXCLUDE E2 if the title says survey or overview). The title names a language-model system, agent, chatbot or assistant but not RAG or retrieval: EXCLUDE E1. The title is about unrelated topics: EXCLUDE E1.
6. **Built, implemented or deployed, but the abstract does not say whether it was tested.** MAYBE.
7. **Mixed qualitative and partial experiments, or a platform or demo that enables RAG comparison without clear quantitative results.** MAYBE.
8. **Still not sure.** MAYBE. Do not exclude only because the abstract does not mention a baseline or a metric.

## 5. Time

Expect 1 to 2 minutes per record: about 2 to 3 hours for 100 records. Work in one or two sessions with a break.

## 6. Sending your file back

Send your finished file only to Shoumya (shoumyac@student.unimelb.edu.au). Suggested deadline: 7 November 2026 (to be confirmed by Shoumya).

## 7. What happens next

1. Shoumya computes agreement (Cohen's kappa and percent agreement) after all files are in.
2. If kappa between the authors is at least 0.70, the main screening starts with the version 1.1 rules.
3. If not, the group discusses the differences again, as before, and the rules are refined.
