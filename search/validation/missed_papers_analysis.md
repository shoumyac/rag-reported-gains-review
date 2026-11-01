# The four gold-list papers missed by the extended query (1 November 2026)

Extended query: 34 of 38 found (89%). Registered query: 30 of 38 (79%). Registered target: at least 95%.

| OpenAlex ID | Paper | Why it is missed |
|---|---|---|
| W4226082499 | Improving language models by retrieving from trillions of tokens (RETRO, 2021) | Title and abstract describe retrieval-enhanced language models and never use the words "retrieval-augmented" or "RAG". |
| W4391876619 | Lost in the Middle: How Language Models Use Long Contexts | About long-context use; no RAG wording in the title or abstract. |
| W4385570777 | When Not to Trust Language Models | The OpenAlex abstract field holds only the author list and proceedings line, so there is no abstract text to match. |
| W4404783040 | Dense X Retrieval: What Retrieval Granularity Should We Use? | A dense retrieval paper; its abstract does not use RAG wording. |

## Cost of widening the query (counts on 1 Nov 2026, same filters)

| Added clause | Records | Finds of the 4 |
|---|---|---|
| none (extended query) | 27,279 | 0 |
| "retrieval" AND (language model OR LLM) | 43,671 | 3 |
| (retrieved OR retrieving) AND (language model OR LLM) | 35,140 | 2 |

Widening would add 8,000 to 16,000 records to find at most 3 of 4 papers that are borderline cases for "RAG" by their own wording, and one paper cannot be found by any title-and-abstract query because OpenAlex holds no abstract for it.

## Proposed handling (not yet a deviation)

Keep the extended query. Report the recall figures (79% registered, 89% extended) and these four reasons in the paper. Add backward and forward citation chasing from the included papers and from the surveys, which is the route that would find papers like RETRO and Dense X. Any change to the query itself would be logged as D6.
