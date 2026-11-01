# Human calibration pilot: results (1 November 2026)

Four screeners (initials S, AD, R, SC; AD and SC are the two authors, S and R the two independent annotators) screened the 300-record calibration sample from title and abstract. AD and SC screened all 300 rows; S and R screened rows 1 to 50 only. Per-screener decision files are kept private until the annotators have agreed to their decisions being shared. Agreement statistics only are reported here.

## Agreement, rows 1 to 50 (all four screeners)

Cohen's kappa, three classes (INCLUDE, MAYBE, EXCLUDE) / two classes (EXCLUDE versus INCLUDE-or-MAYBE):

| Pair | 3 classes | 2 classes | Exact agreement (3 classes) |
|---|---|---|---|
| S, AD | 0.58 | 0.70 | 74% |
| S, R | 0.70 | 0.75 | 80% |
| S, SC | 0.66 | 0.83 | 78% |
| AD, R | 0.52 | 0.78 | 68% |
| AD, SC | 0.62 | 0.86 | 76% |
| R, SC | 0.85 | 0.91 | 90% |

Fleiss kappa, four raters: 0.65 (three classes), 0.80 (two classes). All four identical on 33 of 50 rows; at least three identical on 40 of 50.

## Agreement, rows 1 to 300 (AD and SC)

Kappa 0.59 (three classes) and 0.62 (two classes); exact agreement 75% and 85%. They disagreed on EXCLUDE versus keep in 45 of 300 records (AD excluded and SC kept in 25; SC excluded and AD kept in 20). Where both excluded (58 records), the reason code matched in 53.

AD and SC are the two authors, so this is the registered author-versus-author measurement. Registered target: kappa of at least 0.70 on the 300 records. Not reached, so the registered next step applies: clarify the criteria in writing, then screen a new random sample of 100.

## Where the disagreements come from (45 exclude-versus-keep records)

1. Applications or system descriptions with no clear evaluation in the abstract: E2 versus MAYBE or INCLUDE.
2. Records with no abstract: some exclude as E1 when the title does not mention RAG, others keep as MAYBE.
3. RAG as one component of a larger LLM system: E1 versus INCLUDE.
4. Multimodal records: E9 versus MAYBE.

## Models against humans (EXCLUDE versus keep, kappa)

Between 0.43 and 0.63 for all five models against each human, similar to the lower end of human-human agreement. Models stay ranking aids only.
