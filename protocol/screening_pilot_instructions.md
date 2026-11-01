# Screening pilot: instructions for screeners

Project: Do reported gains in retrieval-augmented generation (RAG) survive scrutiny? A systematic review, meta-analysis and evaluation-validity audit.
Registration: https://doi.org/10.17605/OSF.IO/XGPCZ
Version 1.0, 1 November 2026. These instructions apply the registered Stage 1 rules (`screening_instructions.md`) to the calibration sample. Nothing here changes the registered rules.

## 1. What this is and who does what

You will receive one file, `screening_sheet_300_for_humans.csv`, with 300 records picked at random from the search. For each record you see a title and an abstract. You decide whether the paper should go on to full-text reading.

| Person | Records to screen |
|---|---|
| Anmita Das | All 300 (rows 1 to 300) |
| Shoumya Chowdhury | All 300 (rows 1 to 300) |
| Annotator 1 and Annotator 2 | Rows 1 to 50 only (the 50-record calibration set) |

The aim is to measure how well we agree (Cohen's kappa, target at least 0.70) and to find unclear rules before the main screening starts. Your own honest first reaction is what we need. Disagreement is useful information, not a mistake.

## 2. Independence rules (important)

1. Work alone, in your own copy of the file. Rename it `screening_<your initials>.csv`.
2. Do not talk to anyone about any record until everyone has sent back their file. This includes the other annotator and the authors.
3. Do not look at any other person's answers.
4. Do not look up a paper online, open its full text, or search for its authors. The decision is made from the title and abstract in the file only.
5. Do not use ChatGPT, Claude, Gemini or any other AI tool to help with a decision. Language models have already screened these records and their answers must not influence yours.
6. A dictionary or translator is fine for words you do not understand.
7. Authors: if a record is a paper that you or your co-author wrote, do not decide it. Leave the decision blank and write `OWN` in the note column. The annotators will screen it.

## 3. The file

Keep the file as CSV (UTF-8). Open it in Excel or Google Sheets. Do not sort, delete or move rows or columns, and do not change the first three columns.

| Column | What to do |
|---|---|
| record_id, title, abstract | Read only. |
| decision | Write exactly one of `INCLUDE`, `EXCLUDE` or `MAYBE`. |
| code | Only if you wrote EXCLUDE: the reason code (see section 5). Leave blank otherwise. |
| note | Optional. Write a few words when the case was hard, or `OWN` (authors only). |
| screener_initials | Your initials on every row you complete. |
| date | The date you screened the row (for example 2026-11-03). |

Every row must have a decision, except authors' own papers (blank decision, `OWN` in note). If you change your mind on a row before you send the file, just overwrite it. After you send the file, nothing changes.

## 4. What counts as RAG here

A system in which a language model conditions its output on documents that are retrieved at the time of the question. The retriever can be dense, sparse or hybrid, a web search, or a knowledge graph, as long as the retrieved text is given to the generator.

Not RAG: a vector database or search method on its own with no language model generating from the results; "RAG" meaning red-amber-green status or something else; a model that only memorises its training data.

## 5. How to decide

Ask in this order.

1. Is the record in English and about RAG? If not, write EXCLUDE with code `E1` (not RAG) or `E6` (not in English).
2. Is it a survey, review, taxonomy, position or vision paper, tutorial, whitepaper, product description, conceptual design, or a dataset or corpus description, with no new experiments of a RAG method? EXCLUDE, code `E2`.
3. Is it only about images, audio, video or other non-text inputs for retrieval (multimodal only)? EXCLUDE, code `E9`. If the paper uses both text-only and multimodal parts, choose MAYBE.
4. Does the abstract suggest the paper runs experiments with a RAG system (it proposes a RAG method, evaluates a RAG system, or compares RAG with another setting)? INCLUDE.
5. Not sure? MAYBE. A MAYBE goes to full text, so it is the safe answer when you are unsure.

Rules of thumb:
- Do not EXCLUDE only because the abstract does not mention a baseline or a metric. Baselines are checked later, at full text.
- An application paper (for example a RAG chatbot for a hospital) is INCLUDE if the abstract says it was tested or evaluated. If it only describes the design and plans, EXCLUDE with `E2`. If you cannot tell, MAYBE.
- Do not use what you know about the authors, the journal or the year.
- If there is no abstract, use the title. A title that clearly has nothing to do with RAG or language models is EXCLUDE `E1`. A title that suggests RAG is MAYBE.
- When two reasons both apply, use the first one that applies in the order above.

## 6. Examples (made up, not in the file)

| Title and abstract (short) | Decision |
|---|---|
| "A survey of retrieval-augmented generation for NLP" | EXCLUDE, E2 |
| "We propose X, a RAG method that improves answer accuracy on three QA datasets" | INCLUDE |
| "Faster approximate nearest neighbour search for vector databases" (no generation) | EXCLUDE, E1 |
| "RAG-based assessment of project risk (red, amber, green)" | EXCLUDE, E1 |
| "Retrieval-augmented medical visual question answering with chest X-rays" | EXCLUDE, E9 |
| "We present a conceptual architecture for a RAG assistant in banking" | EXCLUDE, E2 |
| "We built a RAG chatbot for university admissions and report user feedback" | MAYBE or INCLUDE |
| "Improving LLM safety with an external knowledge store" (abstract does not say how) | MAYBE |
| Title only: "Controlled firms, preferences and carbon emissions" | EXCLUDE, E1 |

## 7. Time and breaks

Expect 1 to 2 minutes per record: about 5 to 8 hours for 300 records, 1 to 1.5 hours for 50. Work in sessions of 50 records or fewer and take breaks, because attention drops. Do not rush through the later rows.

## 8. Sending your file back

Send your finished file only to Shoumya (shoumyac@student.unimelb.edu.au), not to anyone else. Suggested deadline: 8 November 2026 (to be confirmed by Shoumya). Tell Shoumya if you cannot finish in time, and how many rows you completed.

## 9. What happens next

1. Shoumya computes agreement between the screeners (Cohen's kappa and percent agreement) and compares everyone with the model suggestions, only after all files are in.
2. If kappa is below 0.70, we discuss the records where we differed, clarify the rules in writing, and screen a new random sample of 100.
3. The annotators receive feedback on the 50 records before they screen any other paper.
4. Decisions are recorded with initials only. Annotators are named in the paper only with their consent.

## 10. Questions

During the pilot, ask only about the rules (not about a specific record), by email to Shoumya. The answer is shared with everyone so that nobody has an unfair advantage. If a rule is unclear, choose MAYBE and write a short note.
