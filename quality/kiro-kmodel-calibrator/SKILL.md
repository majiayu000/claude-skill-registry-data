---
name: kiro-kmodel-calibrator
description: Use when recalibrating conservative Kiro cache-estimation coefficients from recent successful usage samples before updating admin Kmodel settings.
---

# Kiro Kmodel Calibrator

## Overview

This skill defines the reproducible offline process for recomputing per-model
`Kmodel` coefficients used by StaticFlow's conservative Kiro cache estimate.

The output is a recommendation, not a production write. Update the live values
manually in `/admin/kiro-gateway` after reviewing the sample quality.

## When to Use

- Kiro model pricing or multiplier guidance changed
- Recent Kiro credit usage trends drifted away from current estimates
- A new Kiro model needs a default `Kmodel`

Do not use this skill to mutate production config automatically.

## Data Scope

Query the content DB table `llm_gateway_usage_events` under the canonical root:

- `/mnt/wsl/data4tb/static-flow-data/lancedb`

Use only rows matching all of these conditions:

- `provider_type = "kiro"`
- `status_code = 200`
- `credit_usage_missing = false`
- `credit_usage` is finite and `>= 0`
- `created_at` is within the last 30 days

Historical note:

- For Kiro calibration, existing `input_uncached_tokens` should be treated as
  the historical total input token estimate for that request.

## Model Normalization

Normalize aliases before bucketing:

- `claude-opus-4.6 -> claude-opus-4-6`

Keep all other model names unchanged.

## Formula

For each sample, define:

- `Tin = input_uncached_tokens`
- `Tout = output_tokens`
- `Cobs = credit_usage`

Drop samples where:

- `Tin <= 0`
- `Tout < 0`
- `Tin > 200_000`
- `Tin + 5 * Tout <= 0`

Then compute:

```text
ratio = Cobs / (Tin + 5 * Tout)
```

Group by normalized model name and compute:

- sample count
- `p50`
- `p80`
- `p90`

Recommended runtime coefficient:

- `Kmodel = p80`

`p80` is intentionally conservative: it reduces the chance of overstating
`cache_read_input_tokens`.

## Output Contract

For each model, report:

- normalized model name
- sample count
- `p50`
- `p80`
- `p90`
- recommended `Kmodel`

Also report:

- date window used
- filters applied
- rows dropped by each filter if available

## Guardrails

- Do not auto-write the result into LanceDB or admin config
- Do not mix failed requests into calibration
- Do not use a single global coefficient across models
- If a model has too few samples, say so explicitly instead of inventing a value
