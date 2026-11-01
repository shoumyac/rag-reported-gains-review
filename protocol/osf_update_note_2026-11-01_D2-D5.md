# OSF update note (D2 to D5), submitted 1 November 2026 from Shoumya Chowdhury's account, waiting for Anmita Das to approve

Update 1 November 2026 (after the calibration work; no search has been run yet). Five changes, all logged in the public repository file protocol/deviations_log.md:

1. D1: Two clauses added to the OpenAlex query ("retrieval augmentation"; "retrieval-augmented" with language/LLM/generation terms). The registered query is still run and both counts are reported. Reason: on 38 known RAG papers the registered query found 30 (79%) and the extended one 34 (89%).
2. D2: The extraction codebook now fixes which comparisons are extracted (main results tables; proposed method against the nearest no-retrieval and vanilla RAG rows). Reason: in a six-model pilot on 10 papers, models agreed on numbers but chose different baselines.
3. D3: Extraction is table-first (models copy the main results table; comparisons are built by script; row types checked by a human). Reason: agreement on shared rows rose from 84.7% to 97.5 to 100%.
4. D4 and D5: Title and abstract screening rules were clarified twice (versions 1.1 and 1.2). Reason: kappa between the authors was 0.59 on 300 records and 0.63 on a second sample of 100; on a third fresh sample of 100 it was 0.83 (annotators 0.84 to 0.91 with the first author).
5. The registered 95% search-recall target was not met (89%). The four missed papers do not use RAG wording or have no abstract in OpenAlex; we keep the query and add citation chasing, and will report recall openly.

Nothing else in the registration changes.

Posted as the justification of the update. One registered field was also edited, as OSF requires a changed answer: "Current review stage" now ends with "Update 1 November 2026: the calibration screening described in Stage 3 was carried out on 300, 100 and 100 records by the two authors and two independent annotators, and the criteria were clarified (see the justification for this update). No records from the frozen search have been screened and no data have been extracted from included studies."
