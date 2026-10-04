---
name: llm-campaign-drift-gate
description: |
  Gate resumption of any multi-day LLM batch-scoring campaign that calls an
  unpinned model alias (deepseek-chat, gpt-*-latest, gemini-*-preview, any
  provider alias without a pinned version). Use when: (1) resuming a paused or
  credit-exhausted scoring run days after its last chunk, (2) topping up
  credits to finish a campaign, (3) extending a cached scoring pipeline with
  new items. Prevents silently splicing two model versions or serving
  revisions into one measure. Verified 2026-07-16: for $0.30 caught a
  serving-revision drift WITHIN DeepSeek v4-flash (same alias, same family,
  litigation scores systematically shifted across a 2-day gap) before an $83
  resume spend.
author: Claude Code
version: 1.1.0
date: 2026-07-16
---

# LLM Campaign Drift Gate

## Problem

Batch-scoring campaigns (exposure measures, classifiers, extraction runs) call
provider aliases that can be silently repointed to a new model at any time.
Resuming a half-finished campaign after the alias moves splices two different
scorers into one variable, with the version boundary correlated with whatever
orders the chunks (time, firm id) — a silent confound. Providers can also
RETIRE the old model entirely, making the original campaign uncompletable.

## Context / Trigger Conditions

- Resuming a scoring run more than ~a day after its last paid chunk
- "Top up credits and finish the run" requests
- Any incremental scoring against an existing response cache
- Symptom of a missed gate: a step-change in scores at a resume boundary

## Solution

Before ANY production spend on resume, run a two-part gate (~$0.30–2):

1. **Canary (the decisive check):** sample ~100 already-cached items, re-send
   their EXACT stored prompts fresh, compare fresh vs cached scores. Gate:
   ≥97% all-field exact match and no systematic directional shift. Write the
   comparison in a standalone script — never through the pipeline's cache
   layer, which would overwrite production entries.
2. **Gold re-validation:** re-score the gold/validation panel fresh and compare
   agreement metrics to the prior validation (e.g. median F1/κ within ~0.03,
   no domain dropping >0.10).

Also capture `response.model` on every gate call — pipelines rarely store it,
and it is the only direct evidence of a repoint. Check the provider's
`/models` endpoint: if the old model id is gone, no rollback exists.

3. **If the canary fails, diagnose BEFORE concluding — two mandatory
   follow-ups:**
   - **Date the suspected flip against the provider's changelog** before
     inferring a model splice. `response.model` on fresh calls identifies
     today's model only; if the alias already pointed there when the cache was
     written, there is no family splice and the mismatch needs another
     explanation. (Verified failure mode: an alias that had served the "new"
     model for months was misread as a fresh repoint.)
   - **Fresh-vs-fresh canary** to separate serving drift from temperature-0
     nondeterminism: re-score the same items a second time. Drift signature =
     fresh2-vs-fresh1 agreement high and symmetric while both fresh runs
     disagree with the cache at a higher rate in the SAME signed direction.
     Noise signature = fresh-vs-fresh disagrees about as much as
     fresh-vs-cache, with no directional bias.
   - Supporting forensic: compare raw-response formatting fingerprints
     (JSON pretty/compact ratio, key order) between cache and fresh — a
     heterogeneous or shifted style distribution corroborates a serving
     change when no model id was recorded.

**Key subtlety (why both checks):** a new model or revision can validate
AGAINST GOLD as well as the old one (κ holds or improves) while still
disagreeing with the old scores on 10–30% of items, concentrated in
borderline-heavy fields. Gold agreement does not license splicing — the gate
fails on the canary alone. And alias stability is not serving stability:
the same alias serving the same model family can still drift across days via
silent serving revisions; a canary-failed resume is a seam either way, and
the decision (resume with a documented seam vs re-score the universe) belongs
to the budget owner.

## Verification

The gate script logs: fresh `response.model` ids, canary exact-match rate,
per-field mismatch counts with signed direction, and the gold-metric deltas.
GO only if both checks pass.

## Example

T1 exposure_v2 resume, 2026-07-16: canary returned 71% exact (gate ≥97%) with
a litigation-concentrated negative shift, yet holdout median κ improved
0.607→0.644. First interpretation — "alias repointed to a new model family" —
was WRONG: the provider changelog showed `deepseek-chat` had served v4-flash
since April, months before the campaign. The fresh-vs-fresh follow-up then
isolated the true cause: fresh2-vs-fresh1 93% exact/symmetric/litigation 0,
both fresh runs vs cache 71–72% with litigation −12 identically — a serving
revision within the same model across a 2-day gap, corroborated by a shifted
JSON-formatting fingerprint. Total diagnosis cost ~$0.30; the resume-vs-rescore
decision went to the budget owner with the seam quantified.

## Notes

- Design campaigns for this failure: per-response content-addressed cache +
  append-only checkpoint makes "re-score everything under the new model" a
  clean cache-rotation, not a data loss.
- If the cache key embeds the alias string rather than the resolved model,
  record actual `response.model` in run reports — the cache cannot tell you
  later which model produced an entry.
- One campaign = one model. Budget and schedule so the universe completes
  within days, or accept that a provider release can force a full re-score.
- See also: [llm-gold-bound-failure-check] for the companion pre-campaign
  check — whether a validation-gate failure is fixable by prompt at all, or
  bound to the gold construct.
