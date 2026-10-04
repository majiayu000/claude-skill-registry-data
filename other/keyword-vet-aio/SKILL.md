---
name: keyword-vet-aio
description: Evaluate Google AI Overview presence and click-cannibalization risk for BID-passing Pleasur.ai Stage 01 keyword candidates using current Ahrefs evidence. Use after BID validation and before prioritization, in either presence-only or human-approved deep-completeness mode.
---

# Keyword Vet — AI Overview

Evaluate only candidates with `bid_verdict=PASS`. Read [references/aio-rubric.md](references/aio-rubric.md) before deep scoring.

## Required inputs

Require:

- BID evaluation, keyword, target country, observed intent, and tool-led routing status;
- current Ahrefs Keywords Explorer evidence containing `serp_features`;
- a human-approved run mode: `presence_only` or `deep`;
- for `deep`, a fresh Google AI Overview response body from current Ahrefs Brand Radar coverage.

If run mode is absent, use the safer `presence_only` mode and record that decision. Apply the run packet's approved evidence-freshness and bounded-retry policies.

## Evidence contract

- Use the configured Ahrefs integration as the only external SEO data source.
- Inspect live schemas before requesting fields. Do not assume legacy tool names.
- Detect AIO presence only from Keywords Explorer `serp_features`; the literal feature is `ai_overview`.
- Do not request `serp_features` from SERP Overview; it does not provide that field.
- Use a Google AI Overview response captured by Ahrefs Brand Radar as the only acceptable deep-scoring body.
- Never use general web fetch, another provider, a search snippet, or model memory as a body substitute.
- Record exact query, country, report/tool, fields, filters, retrieval time, provider freshness/reference, status, and error.

## Process

### 1. Detect presence

Batch compatible keyword requests when the live integration supports it, while preserving candidate-level provenance.

- If `ai_overview` is absent, set `has_aio=false` and `aio_verdict=PASS` with reason `aio_absent`.
- If present, set `has_aio=true` and continue.
- If current presence evidence is unavailable after bounded retries, return `needs_data` with reason `aio_presence_unavailable`.

Do not infer absence from a null or failed response.

### 2. Evaluate routing exceptions

For an AIO-present candidate:

- tool-led intent is outside the blog queue; retain `PASS` only as an AIO routing note with reason `tool_led_immune`.
- comparison-led commercial investigation is not automatically exempt. Record the specific reason readers may still need options, criteria, evidence, or firsthand comparison, then apply presence-only mode or the deep verdict table normally.

No blog candidate is exempt merely because an intent label is commercial.

### 3. Apply presence-only mode

For each non-tool-led AIO-present candidate, set:

- `aio_completeness_score=null`;
- `aio_click_intent=null`;
- `aio_verdict=RISKY`;
- `aio_reasoning=aio_present` plus a candidate-specific information-gain requirement for any later article.

Presence-only mode must never emit `FAIL_CANNIBALIZED`; that verdict requires observed-body evidence.

### 4. Apply deep mode

Obtain a fresh Google AIO response body from Ahrefs Brand Radar. Record the body source, engine, capture/freshness timestamp, query and country match, and cited-page evidence when available.

If the body is missing, stale under the approved policy, for the wrong engine, query, or country, or cannot be retrieved after bounded retries, return `needs_data` for deep evaluation. Do not silently downgrade the same candidate to presence-only unless the run packet explicitly authorizes that fallback.

Score the observed body using the reference rubric. Judge how completely the AIO satisfies the search need, not how polished it sounds. Record:

- `aio_completeness_score` from 0–10;
- `aio_click_intent` as `yes-deep`, `yes-shallow`, or `no`;
- one specific rationale naming what the AIO covers and what a click would still provide;
- uncertainty and any missing evidence.

Use an independent review pass only when the active Buzz runtime exposes a general review capability. Do not select or name a provider or model. When no independent pass exists, perform a second documented self-review against the same rubric and set `review_mode=self_review`.

### 5. Set the deep verdict

Apply this table to every non-tool-led candidate:

| Completeness score | Click intent | Verdict |
|---|---|---|
| `0–4` | `yes-deep` or `yes-shallow` | `PASS` |
| `5–7` | `yes-deep` or `yes-shallow` | `RISKY` |
| `8–10` | `yes-shallow` | `RISKY` |
| `8–10` | `no` | `FAIL_CANNIBALIZED` |

Treat any unlisted combination as internally inconsistent. Perform one documented rescore against the observed body. If it remains inconsistent, return `needs_data` with reason `aio_score_click_mismatch`; do not choose a verdict.

Never force a distribution of PASS, RISKY, and FAIL results.

## Output schema

Persist for every BID-PASS candidate:

- `keyword`, `country`, `aio_mode`, `has_aio`, and the raw observed `serp_features`;
- `aio_completeness_score`, `aio_click_intent`, `aio_verdict`, `aio_reasoning`, and `aio_reason_code`;
- `aio_body_source`, engine, body freshness/capture reference, cited pages when used, and nulls when no body was requested;
- `review_mode`, information-gain requirement, uncertainty, retry outcomes, evidence provenance, and rubric version.

Keep this evidence in the immutable Stage 01 validated-research packet. Do not write caches, CSVs, repositories, CMS records, or production systems. Do not trigger prioritization or Stage 02.

## Summary

Report candidate counts for:

- no AIO / PASS;
- AIO present / exempt or routed;
- AIO present / RISKY in presence-only mode;
- deep scores `0–4`, `5–7`, and `8–10`;
- `needs_data` with reason;
- deep-body source coverage.

List the highest-risk candidates with their exact evidence and reasoning.

## Quality checks

- Every BID-PASS candidate has a terminal AIO result or `needs_data`.
- Presence came from the literal `ai_overview` feature in Keywords Explorer.
- No failed/null response was interpreted as AIO absence.
- Presence-only mode emitted no `FAIL_CANNIBALIZED` verdict.
- Every deep score used an observed, fresh, query-matched Google AIO body from Ahrefs Brand Radar.
- Every deep verdict follows the completeness-score/click-intent table; retained click value is never marked `FAIL_CANNIBALIZED`.
- Every score and exemption has candidate-specific click reasoning.
- No provider, model, sub-agent primitive, environment flag, cache path, cron behavior, or exit code is assumed.
