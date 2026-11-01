# Deviations log

Every departure from the registered protocol (https://doi.org/10.17605/OSF.IO/XGPCZ) is recorded here with its date, the reason, and what was done instead. The paper states each one.

| Date | Stage | What changed | Reason | Decided by |
|---|---|---|---|---|
| D1, 1 Nov 2026 | Search (before any search was run) | Added two clauses to the OpenAlex query: "retrieval augmentation" and ("retrieval-augmented" AND (language OR LLM OR LLMs OR generation OR generative)). The registered query is still run and reported. | Recall test on 38 known RAG papers (`search/validation/gold_list.csv`): registered query found 30 (79%), extended query found 34 (89%). Cost: about 2,400 more records (27,279 vs 24,876). | Shoumya Chowdhury (decision); posted to the OSF registration as an update on 1 Nov 2026 from Anmita Das's signed-in account |
| D2, 1 Nov 2026 | Extraction (before extraction started) | Codebook now fixes which comparisons are extracted (main results tables; proposed method versus the nearest no-retrieval row and the nearest vanilla RAG row). See `protocol/extraction_instructions.md`. | Pilot of 6 models on 10 papers: models agreed on numbers but chose different baselines; agreement on shared slots was 84.7% with the rule, below the registered 95% target. Under the old open instruction the pairwise overlap was about 0.3. | Shoumya Chowdhury |
| D3, 1 Nov 2026 | Extraction (before extraction started) | Extraction is table-first: models copy the whole main results table verbatim with one-line row quotes; comparisons are built by script; row types (no retrieval, vanilla RAG, prior method) are labelled in a separate step checked by a human. Humans confirm the main tables per paper. Extractor models: Claude Haiku 5.5 and Gemma 4 31B, Qwen3 235B as tie-breaker. Replaces the model-chosen comparisons of D2. | Pilot: with model-chosen comparisons agreement was 84.7% (below 95%), because models picked different baseline rows. Table-first: same numbers on shared rows 97.5% to 100% (`experiments/model_pilot/`). | Shoumya Chowdhury |
| D4, 1 Nov 2026 | Screening (before main screening) | Stage 1 rules clarified in `screening_instructions.md` version 1.1, section 3A: application papers, RAG as component, E1 cases, surveys, missing abstracts, multimodal. A new random sample of 100 records is screened by all four screeners. | Calibration pilot on 300 records: kappa between the authors 0.59 (three classes) and 0.62 (EXCLUDE versus keep), below the registered 0.70. Rules written from the 51 disagreements (`experiments/screening_pilot/reconciled_decisions_51.csv`). | Shoumya Chowdhury and Anmita Das |

## Notes on the registered text

- The registration is the authoritative protocol. Files in this repository are working copies.
- The OpenAlex query in `search/queries/openalex_query.md` is the registered query. A test run of the registered filter on 1 November 2026 returned 29,324 English-language records for 2020-01-01 to 2026-11-30 (24,876 with the three document types article, preprint and conference-paper). The search is re-run at the 30 November 2026 freeze and the final counts are reported.

- The registered search validation target is at least 95% of the gold list. On 1 Nov 2026 the extended query found 34 of 38 (89%). The 4 still missed are being analysed (missing term or indexing problem) and any further change will be logged as D5.
