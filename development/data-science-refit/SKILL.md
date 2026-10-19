---
name: data-science-refit
description: "Use for reusable data science refit recipes in software and coding-agent work."
---

# Data-science refit (outer loop) — recipes (generic tier)

On-demand recipes (6). Trigger→action heuristics; pull the relevant one when its situation arises.

#### 1. Take labels and joins from authoritative ID fields, never from manifests or list position
`generic` · **negative result**

Take labels and join keys from authoritative per-record ID fields, never from a manifest, from list/array position, or from a join-time default value -- those silently mismatch data to the wrong entity and corrupt downstream models without erroring. Two illustrative failures: a manifest 'role' field that was always written as a default at join time silently zeroed every minority-class label and corrupted a model fit (the ground truth lived in per-record state rows instead); and joining scores by array position broke when an upstream process rotated each entity through every position, so the correct key was the stable per-entity identifier. Identify the field that is the source of truth for each label/key and join on that.
  <sub>sources: claude-code:0e7b14ca-ffd5-4137-9456-47485d3c6f87, codex:019e4c28-d516-7ca0-b145-153c152b4f43, codex:019eaea8-4f78-7072-b4b0-539df963b7df, player_labs/best_practices.md</sub>

#### 2. Pick the authoritative source per field: event-derived vs result-derived is not uniform
`generic` · **negative result** · ⚠ _session-derived, unverified_

When the same quantity can be derived two ways -- from final/aggregated results vs from an intermediate event stream -- the two will silently disagree, and neither is uniformly correct: pick the authoritative source per field and reconcile. Some fields are right only from the event timeline (e.g. exact event counts that final aggregates round or lose); others built from intermediate events OVERCOUNT and must be taken from final results. Build the reconciliation check into the tooling (records processed, integrity/hash failures, event-vs-result mismatches all zero) and run it before quoting any number.
  <sub>sources: codex:019e9656-7cfc-7032-ae70-82b6dbc0a053</sub>

#### 3. Never judge a policy on one aggregate score: decompose by role/opponent/submetric and against the corpus
`generic` · ⚠ _session-derived, unverified_

An aggregate score hides the story; before judging anything on it, decompose along its meaningful cuts (the most discriminating cut first) and contextualize against a baseline/corpus distribution, not in isolation. Establish the baseline range first (corpus mean/best/worst) so a value reads as below- or above-average rather than being interpreted blind. Illustrative case: a policy whose headline 'wins most games' hid that in one role it won every game while scoring far below every opponent, and in the other role it lost every game at the score floor -- the aggregate masked two opposite stories that only the per-role and per-opponent cuts revealed.
  <sub>sources: claude-code:3c867a71-3057-4e87-a149-4185e82ee728, opencode:ses_1ffba12c8ffegXTM7TLJ7oigMW</sub>

#### 4. Apply statistical rigor to policy comparisons: leaderboards on raw means are mostly noise
`generic`

When comparing candidates on a noisy metric (A/B variants, leaderboard entries), do not rank on raw means -- they are mostly noise at typical sample sizes. Report effect sizes (Hedges' g, Cliff's delta) alongside means, run BOTH a mean-based test (Welch t) and a rank-based test (Mann-Whitney), apply multiple-comparison correction (Benjamini-Hochberg) across all pairwise tests, and pool matched batches for power. Materialize per-candidate summaries and pairwise comparisons (with corrected p-values and effect sizes) as queryable tables, not printouts. Illustrative: across 28 pairwise 'best policy' comparisons with ~40-100 samples each, only one pair separated after correction and zero parametric tests survived -- so the raw-mean leaderboard ordering was almost entirely noise.
  <sub>sources: codex:019e941c-8eb9-7402-a77f-8fe75a5d19bf, player_labs/best_practices.md</sub>

#### 5. Read distribution shape, not just stdev; and re-verify every cited number, tagging its source
`generic`

Before treating higher variance as risk, inspect distribution shape (report min/max and median alongside mean/sd): a rising stdev with an unchanged median is a one-sided upside outlier (good), not added downside. On any long write-up, re-run the analysis and re-verify every cited figure -- numbers drift on recompute (one figure moved 27%->23.3%, a correlation 0.72->0.86). Tag the source of every number, because different sources of the 'same' metric diverge (a cached/accumulating aggregate drifts away from a live snapshot) and because team-totals vs per-unit and per-trial-means vs leaderboard-scores are easy to conflate; state which source each headline number uses.
  <sub>sources: opencode:ses_1fa6f7b71ffeMqiFWPAD235jUs, archive/cogames_playground/alpha_cog/experiments/notebook/tournaments/</sub>

#### 6. Put asset/palette constants in the loader and assert layout at import time
`generic`

Put game-palette constants and atlas slot indices in the data/asset-loader module that owns them rather than in a compute-kernel module, and have the atlas loader assert at import time that the loaded JSON layout matches the named constants, so drift between named indices and the actual atlas layout fails loudly at startup instead of silently mis-decoding pixels.
  <sub>sources: players_checkouts/players/archive/players/among_them/coborg/PLAN.md</sub>
