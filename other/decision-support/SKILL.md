---
name: decision-support
description: Maintain or extend the advisory decision-support layer that structures signal fusion, external context, AI validation, probabilistic edge, pipeline stage, and supervisor readiness without changing execution behavior. Use when working in app/decision_support.py, journaled decision-support payloads, or operator-facing decision interpretation.
---

# Decision Support

## Binding sources

- **`docs/FINAL_SYSTEM_VISION.md`** — **Layer 5** (AI support); feeds structured context for LLM confirm/recommend, **not** sole execution authority.
- **`AGENTS.md`** — advisory only; **L7** unchanged; decisions must stay **traceable** in payloads and journals.

## Purpose

Use this skill to keep the repository's advisory decision-support layer coherent, structured, and operator-readable.

In `docs/FINAL_SYSTEM_VISION.md`, structured decision context feeds **Layer 5 (AI support)** and observability; this code path must remain **advisory** per `AGENTS.md`.

This layer exists to explain decisions, waits, blocks, and safe-operational readiness. It is not a trading engine and it must not become one by accident.

## Use When

Use this skill when:
- editing `app/decision_support.py`
- editing `app/decision_support_analytics.py`
- editing `app/external_context/*`
- standardizing advisory provider interfaces for manual/news/social/calendar context inputs
- extending `decision_support` payloads in journaling or reporting
- surfacing decision-support fields in the operator panel
- deriving journal-based decision-support analytics or stability views
- improving human-readable labels around fusion, edge, validation, or supervisor state
- extending passive learning-readiness or AI-readiness summaries derived from journaled decision-support traces
- keeping `learning_snapshot` and `ai_audit` records clearly separated from runtime trading decisions

## Do Not Use When

Do not use this skill for:
- changing strategy actions
- changing scorer thresholds or weights
- changing hard risk policy
- auto-enabling AI or experiments
- adding fake predictive claims or guaranteed-edge language

## Safety Contract

- Decision support remains advisory only.
- Hard risk, confidence gates, and execution adapters remain authoritative.
- AI stays a validation or interpretation layer, not an uncontrolled trader.
- External context ingestion must degrade safely when absent or invalid.
- External context may enrich explainability and analytics, but it must never trigger or veto execution by itself.
- Provider stacks or source adapters for external context must fail safely to empty and keep the same advisory-only boundary.
- Freshness, expiry, and provider-health fields for external context may be surfaced for operator review, but they must remain descriptive only.
- AI validation may become context-aware for advisory summaries, but it must not become an execution path, risk override, or order generator.
- Passive learning-readiness fields may summarize snapshot quality, label coverage, or shadow insight availability, but they must not enable runtime learning by themselves.
- Passive AI-readiness fields may summarize audit structure, reason coverage, or evidence usefulness, but they must not activate AI runtime authority.
- Probabilistic edge fields must be labeled clearly if heuristic or uncalibrated.
- Journal-derived edge calibration must remain passive evidence only and must never mutate runtime behavior.
- Passive market regime classification may enrich summaries and future evidence review, but it must not alter scoring, risk, or execution behavior.
- Regime-aware evidence breakdowns must stay descriptive and review-oriented; they must not become promotion logic or runtime gating unless a later task adds that explicitly.
- Mode-aware regime comparison must stay an experiment-review aid only and must not alter baseline, experiment, or scoped-trial execution behavior by itself.

## Primary Workflow

1. Read `AGENTS.md`.
2. Inspect the current pipeline boundary that produces or consumes decision-support metadata.
3. Reuse existing journal, dashboard, and operator-panel payloads where possible.
4. Prefer stable, short field names and operator-readable summaries.
5. Prefer journal-derived normalization over runtime rewrites when adding operator analytics.
6. Verify the new layer did not change execution behavior.

## Required Checks

- `signal_fusion`, `external_context`, `ai_validation`, `probabilistic_edge`, `pipeline`, and `supervisor` stay logically distinct.
- No new field implies trade approval that the backend does not perform.
- Operator-facing labels are short, human-readable, and low-noise.
- Missing context files or skipped AI calls still produce safe, interpretable output.
- External signals remain optional and must not change execution behavior when empty, invalid, or stale.
- Provider-stack extensions must keep local-file behavior intact while making future source additions explicit and bounded.
- Supervisor readiness stays advisory unless a later task explicitly adds controlled gating.

## Expected Output

- `Decision Support:` what changed in the advisory layer.
- `Operator Surface:` how it is shown without adding noise.
- `Decision Analytics:` what became measurable over time.
- `Safety Check:` explicit note that execution behavior did not change.
