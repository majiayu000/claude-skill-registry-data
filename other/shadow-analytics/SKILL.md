---
name: shadow-analytics
description: Maintain or extend shadow analytics diagnostics, strategy×regime matrix, regime transition tracking, AI advisory comparison, confidence calibration, and insight persistence. Use when working in app/learning/analytics.py, app/shadow_learning.py, or shadow-related UI surfaces. Never use for changing runtime execution, risk, or signal generation.
---

# Shadow Analytics

## Binding sources

- **`docs/FINAL_SYSTEM_VISION.md`** — **Layer 6** learning/optimization diagnostics; **strategy quality** first-class; shadow-first in this repo unless explicitly extended.
- **`AGENTS.md`** — passive/diagnostic; no silent runtime mutation; **L7** not bypassed.

## Purpose

Use this skill to keep the shadow analytics layer coherent, operator-readable, and structurally rich.

Aligns with **`docs/FINAL_SYSTEM_VISION.md` Layer 6** (learning and optimization) and reporting surfaces — **diagnostic / shadow-first** in this repo unless explicitly extended.

This layer exists to provide passive diagnostics from paper-trading data. It must never alter runtime behavior.

## Use When

Use this skill when:
- editing `app/learning/analytics.py` shadow insight structures
- editing `app/shadow_learning.py` summary or persistence helpers
- extending shadow diagnostic dimensions (stability, calibration, regime transitions, strategy matrix)
- surfacing shadow analytics in the operator panel
- adding new insight persistence or trend tracking structures
- extending AI advisory comparison signals
- improving confidence calibration diagnostics

## Do Not Use When

Do not use this skill for:
- changing strategy scoring or thresholds
- changing risk policy
- changing execution behavior
- auto-enabling learning or AI modes
- adding adaptive runtime behavior

## Safety Contract

- Shadow analytics remain descriptive and advisory only.
- Strategy×regime matrix is an observation tool, not a strategy selector.
- Regime transitions describe observed market behavior, not predictions.
- AI comparison signals describe alignment, not AI authority.
- Confidence calibration is a review aid, not an automatic tuner.
- Insight persistence is bounded (max 200 entries) and local-only.
- No shadow output may trigger trades, change risk, or alter runtime modes.

## Primary Workflow

1. Read `AGENTS.md`.
2. Inspect current shadow insight structures.
3. Extend descriptive dimensions without changing runtime paths.
4. Verify the new insight does not alter execution behavior.
5. Add bilingual labels (EN/TR) for any new surface.

## Required Checks

- New diagnostics remain purely heuristic and descriptive.
- Strategy×regime cells derive from realized closed records only.
- Calibration bands use paired outcome data only.
- AI comparison collects only when AI_MODE != OFF.
- Persistence helpers are bounded and fail safely.
- Labels exist in both EN and TR.

## Expected Output

- `Shadow Analytics:` what diagnostic dimension changed or was added.
- `Operator Surface:` how the new data appears in the panel.
- `Safety Check:` explicit note that execution behavior was not changed.
