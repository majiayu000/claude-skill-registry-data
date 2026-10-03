---
name: confidence-calibration
description: Maintain or extend confidence calibration diagnostics that compare predicted confidence bands (low/medium/high) against realized win rates. Use when inspecting or extending calibration logic in app/learning/analytics.py or displaying calibration surfaces in the UI. Never use for auto-tuning thresholds.
---

# Confidence Calibration

## Binding sources

- **`docs/FINAL_SYSTEM_VISION.md`** — **Layer 6** strategy-quality diagnostics; **Layer 9–10** operator visibility.
- **`AGENTS.md`** — descriptive only; no silent threshold changes; **L7** intact; see `docs/IMPLEMENTATION_GAP.md` for vision vs repo scope.

## Purpose

Use this skill to keep confidence calibration diagnostics accurate and operator-readable.

Calibration compares grouped confidence scores against realized outcomes to show whether confidence predictions are well-aligned with actual performance.

## Use When

Use this skill when:
- editing confidence calibration logic in `app/learning/analytics.py`
- displaying calibration bands or overall calibration state in the panel
- extending calibration with new band definitions or expected ranges
- reviewing whether confidence scores are overperforming, underperforming, or well-calibrated

## Do Not Use When

Do not use this skill for:
- auto-tuning confidence thresholds
- changing scoring math
- adjusting risk policy based on calibration results
- adding predictive claims

## Safety Contract

- Calibration remains a descriptive review tool only.
- No calibration output may alter confidence thresholds, scoring, or execution.
- The overall calibration label is an observation, not an instruction.
- Bands use only paired outcome data from closed position records.

## Required Checks

- Calibration uses only realized outcome data.
- Expected ranges are conservative and documented.
- Overall labels are descriptive (well_calibrated, needs_review, miscalibrated, insufficient_data).
- UI labels are bilingual (EN/TR).
