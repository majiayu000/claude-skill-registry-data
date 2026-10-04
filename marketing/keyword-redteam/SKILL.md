---
name: keyword-redteam
description: Layer 4 of the keyword research pipeline. Spawns a "skeptical SEO" adversarial sub-agent to argue against every survivor of Layers 1-3. Catches mechanical-classifier blind spots — wrong SERP intent, hidden link-graph gauntlets, AIO trajectory shifts, vanity-rank metrics. Same pattern as quality-check's adversarial draft read, applied to keyword selection.
allowed-tools: Read, Write, Edit, Bash, Task
---

# Keyword Red-Team Skill

After Layers 1-3 mechanically vet the candidate pool, Layer 4 challenges the survivors with adversarial judgment. The mechanical layers see what's measurable; the redteam catches what's missable.

This is Ryan Law's "challenge / verify / push back" principle applied to keyword selection. Same shape as `quality-check`'s adversarial sub-agent (a skeptical reader argues against the draft), just one stage earlier in the pipeline.

## Input

`/keyword-redteam`

Reads:
- `content-pipeline/0-keywords/keyword-ideas.csv` (after Layer 3 — must have `bid_verdict`, `aio_verdict`)
- `brand-config.md`
- `.claude/skills/quality-check/SKILL.md` lines 68-70 — the "agent says everything is fine" override pattern (we mirror it here)

## Process

1. **Filter to survivors.** Take rows where:
   - `bid_verdict == PASS`
   - `aio_verdict ∈ {PASS, RISKY}` (UNKNOWN is also kept — Layer 4 reasons about it)
   - Not yet in `redteam_verdict` column (idempotent: re-running doesn't re-redteam unchanged rows)

2. **Take the top 30** by current `priority_score` (after Layer 5 boosts will be applied — but Layer 4 runs before Layer 5 to keep the red-team pool small, since the redteam is the most token-expensive step).

   If fewer than 30 survivors exist, take all of them.

3. **Spawn the redteam sub-agent** via `Task` with `subagent_type=general-purpose` and a self-contained brief. Per project memory ("Claude-in-Chrome work always runs on Sonnet 4.6") and the model-routing principle, this stays on the **parent model** (Opus by default) because the work is judgment-heavy:

   > You are a senior SEO consultant who has reviewed 1,000+ content briefs. You are reviewing 30 candidate keywords for **{brand}** — see {brand-config-path}. The brand has already passed each candidate through:
   >
   > - Layer 1: keyword discovery (competitor gap + seed/modifier expansion + AI-search citation gap)
   > - Layer 2: BID method — Business potential (brand_fit, product_fit), Intent (SERP-classified), Difficulty (KD% + AS)
   > - Layer 3: AI Overview cannibalization check (0-10 completeness scoring on AIOs that exist)
   >
   > Each candidate's row also exposes Semrush-native columns worth reasoning about: an `intents` array (Semrush's per-keyword intent classifier — multi-label across informational / navigational / commercial / transactional) and a `cluster_id` from Keyword Strategy Builder (the topical cluster the keyword belongs to). Use both as you work through (a)-(d): `intents` is a higher-quality intent signal than the URL-pattern heuristic, and `cluster_id` tells you whether neighbouring keywords in the same cluster already rank for the brand or for a single dominant competitor.
   >
   > Your job: **argue against each candidate**. For each keyword, address all four:
   >
   > **(a) SERP-intent classification challenge.** Layer 2 classified the SERP intent from URL patterns and titles. Why might that classification be wrong for this specific keyword? Is the SERP a hybrid where the dominant intent depends on user context? Would a hands-on reader of the SERP disagree with the classifier?
   >
   > **(b) AIO trajectory.** Even if there's no AIO today, will Google add one in 12 months? What's the shape of the query — definitional, comparative, walkthrough, opinion-driven, news-driven? Definitional and walkthrough queries are getting AIOs fast; opinion / comparison / fresh-news queries are AIO-resistant. Is this candidate AIO-bait?
   >
   > **(c) Hidden difficulty.** Layer 2 used AS + KD% as proxies. What's hiding in the link graph that those metrics miss? E.g.: top result is a publisher with editorial link velocity competitors can't match; SERP is dominated by a single industry institution; YouTube videos rank in the SERP and crowd out blog posts; SERP has high domain diversity (suggesting it's hard to displace any one player). Cross-reference `cluster_id`: are neighbouring keywords in the same cluster also dominated by the same authority sites? If so, the difficulty is cluster-deep, not query-specific.
   >
   > **(d) Business potential overstatement.** Layer 2 used brand_fit + product_fit. Is this keyword a "vanity rank" that produces traffic but no users / revenue / brand mentions? Would shipping content for this keyword actually move the brand's KPIs, or is it a number-gone-up trap?
   >
   > For EACH of the 30 candidates, end with one of three verdicts:
   >
   > - **KEEP** — the candidate is genuinely good; proceed to writing pipeline.
   > - **DROP** — fatal flaw in (a)-(d) that the mechanical layers missed; remove from queue.
   > - **REVISE_PRIORITY** — keep but adjust priority_score by `+X.X` or `-X.X` (capped at ±2.0). Explain why the score is wrong.
   >
   > Be specific. Don't say "this might be hard." Say "the top three results are all from Healthline, Mayo Clinic, and Cleveland Clinic — link velocity from medical institutions is editorial-graded; brand DR + 30 wouldn't beat them."
   >
   > Don't be diplomatic. If 25 of the 30 candidates are good, KEEP 25 and DROP 5. If only 5 are good, that's the verdict — KEEP 5 and DROP 25. Don't pad KEEP rates to look productive.
   >
   > Output format (one block per candidate, in the order I give you):
   >
   > ```
   > ## {n}. {keyword}
   > Verdict: {KEEP | DROP | REVISE_PRIORITY +X.X | REVISE_PRIORITY -X.X}
   > (a) SERP-intent challenge: <one sentence>
   > (b) AIO trajectory: <one sentence>
   > (c) Hidden difficulty: <one sentence>
   > (d) Business potential check: <one sentence>
   > One-line summary: <why your verdict>
   > ```

   Provide the agent with:
   - The 30 candidates with their full vetting metadata as a markdown table
   - The brand-config path
   - The output format template

4. **Validate the response.**
   - Every candidate has a verdict line
   - Verdict is one of: `KEEP`, `DROP`, `REVISE_PRIORITY +X.X`, `REVISE_PRIORITY -X.X` (X.X within ±2.0)
   - Each (a)-(d) is filled and specific (not generic placeholder)
   - **KEEP rate sanity check**: if > 80% of verdicts are KEEP AND total response < 200 words per candidate average, treat as a low-quality "rubber-stamp" pass and re-run the agent with this addendum:
     > Your previous response had a KEEP rate of {X}% across {N} candidates with weak per-candidate critique. Re-do the redteam with these constraints: (1) maximum KEEP rate of 70% — at least 30% of candidates must DROP or REVISE_PRIORITY-down; (2) per-candidate critique must be at least 60 words and name something specific (a competitor domain, an SERP feature, a brand-fit gap, a difficulty metric, etc.); (3) if you genuinely believe most candidates are excellent, prove it by producing the strongest available counter-argument anyway and rebutting it.
     This mirrors `quality-check/SKILL.md` lines 68-70 — same override on adversarial-agent rubber-stamping.

5. **Apply verdicts to the CSV:**
   - DROP → `redteam_verdict=DROP`, the row is excluded from `keyword-queue.csv`
   - KEEP → `redteam_verdict=KEEP`, no priority adjustment
   - REVISE_PRIORITY → `redteam_verdict=REVISE_PRIORITY`, `redteam_priority_delta` set to the proposed delta (capped at ±2.0)
   - Each row also gets `redteam_critique_summary` (the one-line summary from the agent)

6. **Write the full critique** to `content-pipeline/0-keywords/redteam-notes.md` (preserves the (a)-(d) detail per candidate for editor / future reference).

7. **Print summary**:
   ```
   Redteam over N candidates:
     KEEP:              X
     DROP:              X
     REVISE_PRIORITY+:  X (sum delta: +X.X)
     REVISE_PRIORITY-:  X (sum delta: -X.X)
   Top 3 DROPs:
     - <keyword> — <one-line summary>
   Top 3 REVISE-:
     - <keyword> — <one-line summary> (delta: -X.X)
   ```

## Output

Updated `content-pipeline/0-keywords/keyword-ideas.csv` with `redteam_verdict`, `redteam_priority_delta`, `redteam_critique_summary`.

Full critique at `content-pipeline/0-keywords/redteam-notes.md`.

## Quality checklist

- [ ] Every candidate in the top-30 input has a verdict (no skipped rows)
- [ ] At least 1 DROP verdict (gate is doing real work — if all KEEP, run the override)
- [ ] Per-candidate (a)-(d) critique is specific, not generic
- [ ] `redteam_priority_delta` values are within ±2.0
- [ ] `redteam-notes.md` preserves the full agent output for future review

## Why this layer matters

The mechanical layers (BID, AIO) are necessary but not sufficient. Real keyword selection is judgment-heavy: a high-DR competitor isn't always unbeatable (they may have stale content); a low-AIO query may sprout one tomorrow; a "great brand fit" keyword may be a vanity rank in disguise. Layer 4 is the only layer that reasons about the future and the implicit. Without it, the autonomous pipeline ships content for keywords that look right on paper but fail in the SERP.

## When the redteam wants to KEEP everything

Per the override protocol above. The brief is structured to force a contrarian read; if the agent comes back with all-praise, the brief failed to bite. Re-run with the explicit "max 70% KEEP rate, 60-word minimum critique" addendum.

## When the redteam wants to DROP everything

Rare. Usually means Layers 1-3 produced a genuinely poor pool (e.g., gap analysis returned only branded competitor terms; seeds were too generic). Don't disagree with the agent — if it has specific (a)-(d) reasoning per candidate, the pool IS bad. Halt the pipeline, log to `content-pipeline/0-keywords/cache/redteam-poor-pool.log`, and signal to the keyword-research-pipeline orchestrator that Layer 1 needs investigation. Don't ship a queue from a poor pool.

## Idempotency

Re-running this skill on a CSV where some rows already have `redteam_verdict` skips those rows. The agent only sees rows with a missing verdict. This means:
- A failed run can be resumed by re-invoking the skill
- Adding new candidates from a fresh `/content-gap-analysis` doesn't re-redteam old candidates

To force a re-redteam (e.g., after threshold tuning or a major brand-config change), pass `--regen` to clear the redteam columns first.

## Cost notes

Layer 4 is the most expensive layer per keyword (one Opus/Sonnet call per 30-candidate batch). Per-run budget: ~30K tokens output + 10K tokens input ≈ $0.40-0.60 per keyword-research-pipeline invocation. The orchestrator's weekly cadence keeps this annual cost under $30 — cheap insurance against shipping a single dead-traffic article.
