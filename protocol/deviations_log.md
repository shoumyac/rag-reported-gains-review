# Deviations log

Every departure from the registered protocol (https://doi.org/10.17605/OSF.IO/XGPCZ) is recorded here with its date, the reason, and what was done instead. The paper states each one.

| Date | Stage | What changed | Reason | Decided by |
|---|---|---|---|---|
| 1 Nov 2026 | Search (before any search was run) | Added two clauses to the OpenAlex query: "retrieval augmentation" and ("retrieval-augmented" AND (language OR LLM OR LLMs OR generation OR generative)). The registered query is still run and reported. | Recall test on 38 known RAG papers (`search/validation/gold_list.csv`): registered query found 30 (79%), extended query found 34 (89%). Cost: about 2,400 more records (27,279 vs 24,876). | Shoumya Chowdhury (decision); posted to the OSF registration as an update on 1 Nov 2026 from Anmita Das's signed-in account |

## Notes on the registered text

- The registration is the authoritative protocol. Files in this repository are working copies.
- The OpenAlex query in `search/queries/openalex_query.md` is the registered query. A test run of the registered filter on 1 November 2026 returned 29,324 English-language records for 2020-01-01 to 2026-11-30 (24,876 with the three document types article, preprint and conference-paper). The search is re-run at the 30 November 2026 freeze and the final counts are reported.

- The registered search validation target is at least 95% of the gold list. On 1 Nov 2026 the extended query found 34 of 38 (89%). The 4 still missed are being analysed (missing term or indexing problem) and any further change will be logged as D2.
