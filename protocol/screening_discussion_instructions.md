# Screening pilot: instructions for the discussion session

Project: Do reported gains in retrieval-augmented generation (RAG) survive scrutiny? A systematic review, meta-analysis and evaluation-validity audit.
Registration: https://doi.org/10.17605/OSF.IO/XGPCZ
Version 1.0, 1 November 2026. Use together with `disagreements_for_discussion.csv` and `screening_pilot_instructions.md`.

## 1. Purpose

The calibration pilot did not reach the registered agreement target (kappa 0.70 between the two authors; they reached 0.59 on three classes and 0.62 on EXCLUDE versus keep). The registered next step is to clarify the criteria in writing and screen a new sample of 100 records.

This session has one job: turn the disagreements into clear, written rules. It is not to decide which person was right. Every disagreement shows a place where the rules did not say enough. Success is a rule that a new screener could follow without asking.

## 2. Who takes part and how

- Everyone who screened takes part: the two authors (SC and AD in the file) and the two independent annotators (S and R). The initials are the ones used in the screening files.
- One person chairs and one person types into the shared copy of the CSV. The chair should not be one of the authors who disagreed on that record. Rotate if you can.
- Use one video call, 90 minutes at a time, with a break every 45 minutes. Plan about two sessions for 51 records.
- Do not use any AI tool to decide a record or to write a rule. The earlier model suggestions are not to be consulted.
- Do not open full texts or look papers up. Decide from the title and abstract in the file only, exactly as in the pilot.

## 3. The file

`disagreements_for_discussion.csv` has 51 records where the screeners split between EXCLUDE and keep (INCLUDE or MAYBE). For each record you see the title, abstract, and every screener's decision, code and note (columns marked S, AD, R, SC). Fill in the last three columns:

| Column | What to write |
|---|---|
| agreed final decision | INCLUDE, EXCLUDE or MAYBE, as decided by the group |
| final code | E1, E2, E6 or E9 if EXCLUDE, otherwise blank |
| reason for the rule | One general sentence that would also settle similar records. Not "this paper is about X". |

## 4. How to run each record (3 to 5 minutes)

1. The chair reads the title and the abstract aloud. If there is no abstract, say so.
2. Each person who disagreed says in one sentence why they chose their answer, in their own words and without arguing.
3. The group asks: which rule in `screening_pilot_instructions.md` section 5 applies, and where does it fall short?
4. Decide. Try to agree by discussion. If it is genuinely unclear, record MAYBE. MAYBE is a valid answer and means "read the full text".
5. Write the one-sentence general rule in the last column.
6. Move on. Do not reopen a settled record unless a later record shows the rule contradicts it.

If the two authors cannot agree on a record, the independent annotators decide, as in the registered protocol. If the annotators split, record MAYBE.

## 5. Work through the records in four groups

Sort or filter the sheet by these groups. Within a group, settle the general rule first, then apply it to each record.

**Group A. Applications, systems and designs with no clear evaluation in the abstract.** Question: when is a system or prototype description EXCLUDE (E2) and when is it MAYBE or INCLUDE?
Draft rule to test: EXCLUDE (E2) only if the abstract itself says it is conceptual, a design, a proposal, a plan, a whitepaper, an overview or a survey, or clearly reports no results. If the abstract says it was built and tested, evaluated, compared or measured, INCLUDE. If it only says "we present a system" and does not say either way, MAYBE.

**Group B. Records with no abstract.** Question: how should the title alone be used?
Facts to keep in mind: the search matched title or abstract, so the missing abstract probably mentions RAG. The authors plan to recover missing abstracts (for example from Crossref) before the new sample is drawn.
Draft rule to test: if the title shows a link to language models, retrieval, question answering or generation, MAYBE. If the title is clearly about something else (for example finance, climate, medicine with no language-model sign), EXCLUDE E1. Never EXCLUDE a title that itself says RAG or retrieval-augmented, unless it is a survey.

**Group C. RAG as one component of a larger LLM system.** Question: does a system that uses RAG as one module count?
Draft rule to test: INCLUDE or MAYBE if the abstract says the evaluated system uses retrieval-augmented generation, even as one component. EXCLUDE E1 only if RAG is background or future work, or "RAG" or "retrieval" means something else, or retrieval is used without a language model generating from the retrieved text.

**Group D. Multimodal records.** Question: when is a record multimodal-only (E9)?
Draft rule to test: E9 if the inputs, the retrieved items or the evaluation task are images, audio, video or other non-text and there is no text-only RAG experiment. If the paper has both text-only and multimodal parts, or the abstract does not say, MAYBE.

The draft rules are suggestions written from the pilot data. Change, reject or replace them as the group sees fit. If the group's rule conflicts with a draft, the group's rule wins.

## 6. After the discussion

1. Send the filled CSV to Shoumya. Include any record the group left as MAYBE because it could not agree, and note the rule gap.
2. Shoumya (with Claude's help drafting) writes version 1.1 of `screening_instructions.md` and `screening_pilot_instructions.md`, adding the agreed rules, and records the change in the deviations log as D4.
3. Because the criteria change, the OSF registration gets an update note, as with the earlier search deviation.
4. A new random sample of 100 records is drawn, with missing abstracts filled in where possible. All four screeners screen it independently using the new rules. Target: kappa at least 0.70 between the two authors. If it is still lower, repeat steps 1 to 4 once more and report the agreement in the paper.
5. Annotators receive the updated rules before they screen anything else.

## 7. Ground rules for the discussion

- Be specific: refer to the rule text, not to who is right.
- Hard cases are expected. Do not rush to avoid disagreement. A rule that hides a real doubt will fail on the next sample.
- Keep notes of each rule's reason. They go into the paper's methods section.
- Everyone's contribution is recorded with initials only. Annotators are named in the paper only with their consent.
