---
name: zf-pipeline-contracts
description: Pipeline contract enforcement for ZINC-Fusion-V15 soybean oil forecasting system. Use when working on any ZINC-Fusion-V15 task involving schema definitions, training pipelines, L0 specialists, data ingestion, MLflow/Dagster configuration, or debugging contract drift. Triggers on mentions of fusion.db, specialist models, horizon encoding, quantile outputs, OOF predictions, or any ZINC-Fusion development work.
---

# ZF Pipeline Contracts

Enforce schema, drift prevention, and pipeline contracts across the L0→L1→L2→L3 architecture for ZINC-Fusion-V15.

## Canonical Naming (Non-Negotiable)

| Item | Canonical | Never Use |
|------|-----------|-----------|
| Project | ZINC-Fusion-V15 | CBI-V15, CBI, zinc_fusion |
| Database | fusion.db | zinc_fusion_v15.db, cbi.db |
| Python module | `fusion.*` | `zinc_fusion.*`, `cbi.*` |
| Dagster package | `quickstart_etl` | (intentional scaffold name) |
| Model term | "Specialists" | "Big-10", "buckets", "Big-8" |

If you drift to legacy names, stop and correct immediately.

## L0 Architecture (11 Models)

| ID | Name | Type | Domain |
|----|------|------|--------|
| 0 | `core` | TimeSeriesPredictor | ZL price action |
| 1 | `crush` | TabularPredictor | Crush margin dynamics |
| 2 | `china` | TabularPredictor | Chinese demand/policy |
| 3 | `fx` | TabularPredictor | Currency impacts |
| 4 | `fed` | TabularPredictor | Fed policy |
| 5 | `tariff` | TabularPredictor | Trade policy |
| 6 | `energy` | TabularPredictor | Energy prices |
| 7 | `biofuel` | TabularPredictor | Biofuel demand |
| 8 | `palm` | TabularPredictor | Palm oil competition |
| 9 | `volatility` | TabularPredictor | Volatility regimes |
| 10 | `substitutes` | TabularPredictor | Veg oil substitution |

## Time Grains (LOCKED)

| Grain | PK Column | Horizon Steps | Use Case |
|-------|-----------|---------------|----------|
| `_1h` | `ts_event` | N/A (features only) | Intraday volatility, sentiment |
| `_1d` | `as_of_date` | 5, 21, 63, 126 | Core forecasting, all OOF |

**Only `_1h` and `_1d` exist.** Do not invent `_4h`, `_8h`, `_1w` grains.

## Pipeline Layers

```
L3: Risk Layer      → Monte Carlo → VaR/CVaR → Procurement signals
        ↑
L2: Ensemble Layer  → Weighted fusion → P10/P50/P90 forecasts
        ↑
L1: Meta-Learner    → TabularPredictor stacking OOF from L0
        ↑
L0: Base Models     → 1 Core + 10 Specialists (11 total)
```

## Neural Sentiment → ALL Specialists

Sentiment feeds ALL specialists, not just tariff/china/biofuel:

| Specialist | Weight | Rationale |
|------------|--------|-----------|
| crush | 0.10 | WASDE/supply sentiment |
| china | 0.15 | Trade/demand sentiment |
| fx | 0.08 | Currency sentiment |
| fed | 0.10 | Monetary policy tone |
| tariff | 0.15 | Trade policy sentiment |
| energy | 0.12 | Energy/crude sentiment |
| biofuel | 0.12 | Biofuel mandate sentiment |
| palm | 0.08 | Palm/deforestation sentiment |
| volatility | 0.05 | Risk sentiment amplifier |
| substitutes | 0.05 | Cross-commodity sentiment |

**Total: 1.00**

## Top 3 Failure Modes

| Priority | Failure | Cause | Detection |
|----------|---------|-------|-----------|
| 1 | Contract drift | Column names diverge from code | Schema diff query |
| 2 | Join-key drift | L0 outputs don't uniquely key on (as_of_date, horizon_steps) | Duplicate check |
| 3 | Quantile crossing | p10 > p50 or p50 > p90 | Monotonicity query |

## Reference Files

Load these based on task:

| File | Load When |
|------|-----------|
| `references/naming_contracts.md` | Starting any ZF work |
| `references/schema_contracts.md` | Creating/modifying tables |
| `references/horizon_encoding.md` | Working with time horizons |
| `references/hourly_contracts.md` | Working with 1h grain data |
| `references/neural_sentiment_routing.md` | Sentiment feature engineering |
| `references/guardrail_queries.sql` | Before/after data mutations |
| `references/manifest.yaml` | Adding data sources |
| `references/new_specialist_checklist.md` | Adding L0 specialist |

## Quick Validation Workflow

Before any commit touching pipeline code:

1. Read `references/guardrail_queries.sql`
2. Run quantile crossing check
3. Run join-key uniqueness check (per specialist)
4. Run horizon encoding check
5. If adding tables, verify against `references/schema_contracts.md`
