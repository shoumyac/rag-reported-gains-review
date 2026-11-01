# Screening pilot: can models screen titles and abstracts?

Run on 1 November 2026.

- **Sample:** 300 records drawn at random (OpenAlex `sample`, seed 20261101) from the extended query of deviation D1. Record IDs and titles: `sample_300_ids.csv`. This is also the sample intended for the registered human calibration (about 300 records, kappa target 0.70), so the authors and annotators can screen the same records. `draw_sample.py` reproduces it. 47 of the 300 have no abstract in OpenAlex.
- **Task:** Stage 1 of the registered screening instructions (INCLUDE, EXCLUDE with code E1, E2 or E9, or MAYBE), from title and abstract only, one record per call. Prompt in `screen_pilot.py`. Raw outputs in `out/`.
- **Models:** Claude Haiku 5.5, Claude Sonnet 5.5, Gemma 4 31B, Qwen3 235B, DeepSeek V4 Flash. Cost for all 1,500 calls: about USD 1.15 (Sonnet USD 0.97 of it).

## Agreement between models (Cohen's kappa, EXCLUDE versus INCLUDE-or-MAYBE)

Pairs range from 0.52 (Haiku with Qwen) to 0.79 (Haiku with Sonnet). Only the Anthropic pair reaches the 0.70 target set for human screeners; most others are 0.6 to 0.75. In 53 of 300 records the models split between excluding and keeping.

## Checked against an adjudicated label (by Claude, not by a human)

The 53 split records were read and labelled KEEP (include or maybe) or EXCLUDE by Claude against the registered rules (`adjudicated_labels.json`). The 247 records on which all models agreed were taken as agreed. Because those 247 follow the models, the fair test is the 53 contested records:

| Model | Agrees with adjudicated label | Wrongly excludes | Wrongly keeps |
|---|---|---|---|
| Claude Sonnet 5.5 | 35 of 53 | 0 | 18 |
| Gemma 4 31B | 31 of 53 | 7 | 15 |
| Qwen3 235B | 28 of 53 | 16 | 9 |
| Claude Haiku 5.5 | 27 of 53 | 0 | 26 |
| DeepSeek V4 Flash | 27 of 53 | 5 | 21 |

Reading it: Claude models never wrongly excluded a record but keep many records that should go (cheap to fix at full text). Qwen excludes eligible-looking records too often and is not suitable for screening. Gemma and DeepSeek wrongly exclude a few.

Typical records models struggled with: applications and system descriptions without experiments (E2), multimodal papers (E9), and records with no abstract. Many of the sampled records are applications of RAG, not experiments with baselines, so Stage 1 can only remove the clear surveys, position papers, multimodal papers and non-RAG uses of "RAG". Eligibility (experiments with a baseline) is decided at full text.

## Implication

The registered rule that models never exclude a record alone is the right one. Models are used to rank records for the human screeners in the active-learning tool. If a model-only filter were ever used, "exclude only if both Claude Haiku 5.5 and Gemma 4 31B say EXCLUDE" had zero wrongly excluded records on this sample (0 of 239 kept records; 33 exclusions, all correct), but this has not been tested by humans and is not part of the protocol.
