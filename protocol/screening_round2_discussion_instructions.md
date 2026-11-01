# Screening round 2: instructions for the discussion between the two authors

Project: Do reported gains in retrieval-augmented generation (RAG) survive scrutiny? A systematic review, meta-analysis and evaluation-validity audit.
Registration: https://doi.org/10.17605/OSF.IO/XGPCZ
Version 1.0, 1 November 2026. Use with `round2_disagreements_for_discussion.csv` and the rules in `screening_instructions.md` version 1.1, section 3A.

## 1. Purpose

In round 2 the two authors reached kappa 0.63 (three classes) and 0.58 (EXCLUDE versus keep), below the registered target of 0.70. Rasel and Shifa agreed with each other and with Shoumya (kappa 0.82 to 0.84), so the v1.1 rules are mostly clear. The 22 records in the file are where Shoumya and Anmita chose differently.

The job of this session is to find the places where the written rules still leave room for two readings, and to write them down as clearer rules (version 1.2). It is not to decide who was right. Success is a rule that a new screener could follow without asking.

## 2. Who and how

- Shoumya and Anmita together, on one call, about 60 to 90 minutes for 22 records.
- One person reads each record aloud and the other types into the shared copy of the CSV. Swap roles halfway.
- Do not use any AI tool to decide a record or write a rule.
- Do not open full texts or look papers up. Decide from the title and abstract in the file only.
- Rasel and Shifa are not in the session. Their decisions are shown in the file for information only (see section 5).

## 3. The file

`round2_disagreements_for_discussion.csv` has one row per record. For each you see the title, the abstract, your two decisions, codes and notes, and what Rasel and Shifa chose. Fill in the last three columns:

| Column | What to write |
|---|---|
| agreed_decision | INCLUDE, EXCLUDE or MAYBE, as decided together |
| agreed_code | E1, E2, E6 or E9 if EXCLUDE, otherwise blank |
| why_rule | One general sentence that would also settle similar records. Not "this paper is about X". |

## 4. How to run each record (about 3 minutes)

1. Read the title and abstract aloud. If there is no abstract, say so.
2. Each of you says in one sentence why you chose your answer, without arguing.
3. Ask together: which rule in section 3A of `screening_instructions.md` applies, and where is its wording too loose?
4. Decide. Try to agree by discussion. If it is genuinely unclear, record MAYBE, which means "read the full text".
5. Write the one-sentence general rule in `why_rule`.
6. Move on. Reopen a settled record only if a later one shows the rule contradicts it.

## 5. If you cannot agree on a record

Leave `agreed_decision` blank, write `SPLIT` in `why_rule`, and look at the two annotators' decisions. If they agree with each other, use that as the tie-break, as in the registered protocol. If they split, record MAYBE. Do not look at the annotators' decisions before you have discussed the record.

## 6. Where the differences are

Group the records first, then settle the general rule, then apply it to each record in the group.

| Pattern | Records | Typical question |
|---|---|---|
| Shoumya EXCLUDE, Anmita INCLUDE | 6 | Is this really an experiment with a RAG system, or RAG only as background, a baseline or a component that is not evaluated? |
| Shoumya EXCLUDE, Anmita MAYBE | 4 | Is the missing information a reason to keep the record, or is the exclusion rule already clear? |
| Shoumya MAYBE, Anmita INCLUDE | 8 | When does "built and tested, but no numbers in the abstract" count as INCLUDE and when as MAYBE? |
| Shoumya INCLUDE, Anmita EXCLUDE | 2 | Which exclusion reason did Anmita apply and is it covered by section 3A? |
| Shoumya MAYBE, Anmita EXCLUDE | 2 | Same question for records where one of you excludes and the other keeps. |

The largest group is the 8 records where Shoumya chose MAYBE and Anmita chose INCLUDE. For these, decide what the abstract has to say before a record counts as INCLUDE (for example: an experiment, an evaluation or a comparison is mentioned) and write that as a plain test.

## 7. After the discussion

1. Send the filled CSV to Claude.
2. Claude drafts version 1.2 of section 3A from your `why_rule` sentences, and you check it. Claude logs the change as deviation D5.
3. Because the criteria change again, the OSF registration gets an update note covering D2 to D5.
4. If the new rules are clear, a third round is drawn: a new random sample of 100 records, screened independently by all four, with a target of kappa at least 0.70 between the authors. If it is still lower, the agreement is reported in the paper as it is.

## 8. Ground rules

- Be specific: refer to the rule text, not to who is right.
- Hard cases are expected. A rule that hides a real doubt will fail on the next sample.
- Keep the reason for each rule, because the reasons go into the methods section of the paper.
