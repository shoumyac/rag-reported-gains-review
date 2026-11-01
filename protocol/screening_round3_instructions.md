# Screening round 3: instructions for screeners

Project: Do reported gains in retrieval-augmented generation (RAG) survive scrutiny? A systematic review, meta-analysis and evaluation-validity audit.
Registration: https://doi.org/10.17605/OSF.IO/XGPCZ
Version 1.0, 1 November 2026. Use with `screening_sheet_round3_100_for_humans.csv` and the rules in `screening_instructions.md` version 1.2, sections 3A and 3B.

## 1. What this is

In round 2 the two authors agreed at kappa 0.63, below the target of 0.70. The rules were clarified again (version 1.2, section 3B). Round 3 tests whether they now work, on 100 new random records that nobody has seen. All four screeners (the two authors and the two annotators) screen all 100.

Target: kappa of at least 0.70 between the two authors. If it is lower, the actual number is reported and the authors discuss the differences. The annotators' results show whether the rules are clear to people who were not in the discussions.

## 2. Independence rules (same as before)

1. Work alone, in your own copy of the file. Rename it `round3_<your initials>.csv`.
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
| note | A few words when the case was hard, or `OWN`. |
| screener_initials, date | On every row you complete. |

Some records show "(no abstract)". Follow rule 5 below.

## 4. How to decide

Use the first rule that applies. The full wording is in sections 3A and 3B of `screening_instructions.md` (version 1.2). Short version:

1. **Not English.** EXCLUDE E6.
2. **Not about RAG.** EXCLUDE E1. This covers: RAG only as background motivation, future work or a passing mention; RAG only as a baseline that the paper's own non-RAG method beats; "RAG" meaning something else; retrieval without a language model generating from the results (vector indexing, quantization, a retrieval-only benchmark); retrieval used only to build a dataset for later RAG; a software architecture paper that mentions RAG only as an existing practice.
3. **Survey, overview or position paper, or design only.** EXCLUDE E2. This includes a survey or taxonomy with no new experiments, a proposed platform or architecture with no built artifact, test or evaluation mentioned, a projected target instead of results, a planned future evaluation, and an organisational pilot that mentions RAG only in the keywords.
4. **Image, audio or video tasks only.** EXCLUDE E9 when every task input needs an image, audio or video and there is no text-only setting, even if the retrieval corpus is text. If text and page images or video are both involved and the abstract does not say whether a text-only setting was tested, MAYBE.
5. **Experiments with a RAG system, even as one component.** INCLUDE. This also holds when:
   - the abstract states that an evaluation or comparison was run and names what improved, but gives no numbers;
   - several language models or settings were compared inside a RAG system, even only in words;
   - a RAG system is part of an evaluated workflow with quantitative results, even if the paper is about productivity or human-AI collaboration;
   - a language model retrieves text spans or tokens at inference time (for example nearest-neighbor decoding) and is compared with RAG baselines.
6. **MAYBE** when:
   - the abstract says a RAG system was built or deployed (including a demo or code link), or claims general improvement, but names no experiment, metric, test set or baseline;
   - a proof of concept only says it "illustrates" the approach experimentally;
   - the only evidence is a small focus group or satisfaction questionnaire;
   - numbers are given only for a non-RAG module and the RAG part is shown only in qualitative case studies;
   - a work-in-progress paper reports only a preliminary comparison;
   - you are still not sure. Do not exclude only because the abstract does not mention a baseline or a metric.
7. **No abstract.** The title names RAG or retrieval-augmented generation: MAYBE (EXCLUDE E2 if the title says survey or overview). The title names a language-model system, agent, chatbot or assistant but not RAG or retrieval: EXCLUDE E1. The title is about unrelated topics: EXCLUDE E1.

## 5. Time

Expect 1 to 2 minutes per record: about 2 to 3 hours for 100 records. Work in one or two sessions with a break.

## 6. Sending your file back

Send your finished file only to Shoumya (shoumyac@student.unimelb.edu.au). Suggested deadline: 8 November 2026 (to be confirmed by Shoumya).

## 7. What happens next

1. Shoumya computes agreement (Cohen's kappa and percent agreement) after all files are in.
2. If kappa between the authors is at least 0.70, main screening starts with the version 1.2 rules.
3. If not, the authors discuss the differences, the actual number is reported in the paper, and a further round is decided together.
