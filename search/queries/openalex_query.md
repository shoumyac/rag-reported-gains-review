# OpenAlex queries

Two variants are kept. `search/oa_search.py --query registered` runs the exact OSF query; `--query extended` (the default) runs the registered query plus two clauses, logged as deviation D1 in `protocol/deviations_log.md`. Both are run and both counts are reported.

## Registered query (OSF, unchanged)

Copied from the OSF registration (https://doi.org/10.17605/OSF.IO/XGPCZ), Search Strategy, Query strings.

```
title_and_abstract.search:("retrieval-augmented generation" OR "retrieval augmented generation" OR "retrieval-augmented language model" OR "retrieval-augmented language models" OR "retrieval-augmented LLM" OR "retrieval-augmented large language model" OR ("RAG" AND (retrieval OR retriever OR "language model" OR LLM)))
from_publication_date: 2020-01-01
to_publication_date: 2026-11-30
language: en
type: article | preprint | conference-paper
```

## Extended query (deviation D1, decided 1 November 2026)

The registered query plus two clauses: `OR "retrieval augmentation"` and `OR ("retrieval-augmented" AND (language OR LLM OR LLMs OR generation OR generative))`. Same filters.

```
title_and_abstract.search:("retrieval-augmented generation" OR "retrieval augmented generation" OR "retrieval-augmented language model" OR "retrieval-augmented language models" OR "retrieval-augmented LLM" OR "retrieval-augmented large language model" OR ("RAG" AND (retrieval OR retriever OR "language model" OR LLM)) OR "retrieval augmentation" OR ("retrieval-augmented" AND (language OR LLM OR LLMs OR generation OR generative)))
```

Test counts on 1 November 2026: 32,066 records with no type filter; 27,279 with the three types (the registered query gave 24,876). On a list of 38 known RAG papers (`search/validation/`), the registered query found 30 and the extended query found 34.

## Notes
- Wildcards (`retriev*`, `model*`) are not used. A test on 1 November 2026 showed that the combined query with wildcards returns an HTTP 400 error.
- Test counts on 1 November 2026: 29,324 records with the filters above and no type filter; 24,876 with the three types.
- The frozen run, with raw responses and hashes, is made on or before 30 November 2026 using `search/oa_search.py`.

Other sources (registered): arXiv API (categories cs.CL, cs.IR, cs.AI, cs.LG), ACL Anthology bibliography export, and ACM DL, IEEE Xplore and Scopus where accessible through the university login. Their exact strings and run logs are added to this folder when those searches are run.
