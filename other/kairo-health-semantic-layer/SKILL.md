---
name: kairo-health-semantic-layer
description: Use Kairo's private health semantic layer to interpret its HealthKit ledger, daily profiles, trends, personal baselines, mood targets, learned factor scores, and evidence-backed insights without confusing ingestion activity with health activity.
---

# Kairo health semantic layer

Use this skill when analysing Kairo health data, designing its dashboard or AI tools, or explaining its learned personal patterns.

1. Read `references/semantic-layer.md` before constructing queries or claims.
2. Read `references/source-inventory.md` when assessing coverage or freshness.
3. Read `references/evidence.md` before interpreting sleep, mood, provenance, or predictive factors.
4. Prefer `health_daily_profiles` and `health_daily_features` for day/trend questions. Use `health_current_observations` only when a required feature is absent or being audited.
5. Use effective time for health behaviour and receipt time only for ingestion reliability.
6. Treat mood self-reports as targets. Treat passive signals as predictors or context.
7. Compare this owner with their own trailing baseline before invoking population reference ranges.
8. Never imply causality, diagnosis, or certainty from `k`; report target, horizon, lag, sample size, coverage, validation, and caveats.
9. Never interpret a missing record as zero or a denied HealthKit permission.
10. Keep assistant context bounded and owner-authenticated. Do not expose unrestricted SQL or raw dumps to an AI model.

The canonical implementation and feature catalog live in the Kairo repository under `docs/` and `web/db/`.
