---
name: dense-state-logic
description: Resonant state mapping and stability checks for Dense-State Logic v1, including phase-wrapped token mapping, telemetry-biased resonance scoring, and intent integrity drift verification. Use when implementing or validating temporal formalism, resonance gating, or dense state kernels.
---

# Dense-State Logic

## Overview

Implement and validate Dense-State Logic v1 with resonance gating, phase-wrapped token mapping, and Fourier spectrum summaries.

## Workflow

1. Use `core/resonant_kernel/interface.py` for TemporalFormalismContract.
2. Use `core/dense_logic/decoder.py` to verify intent drift.
3. Call the skill to evolve resonance, verify drift, or export spectrum.

## Skill Usage

- `capability=resonate`: Map tokens + telemetry into a resonant state and return stability.
- `capability=verify`: Validate drift against a provided state or the current kernel state.
- `capability=spectrum`: Export FFT magnitudes for human-readable logs.

Example payloads:

```json
{
  "capability": "resonate",
  "text": "heartbeat seed",
  "telemetry": {"cpu": 12.0, "vram": 8.0}
}
```

```json
{
  "capability": "verify",
  "tokens": [1, 2, 3, 4],
  "state": [[0.0, 1.0], [0.5, 0.5]]
}
```

## Notes

- Keep resonance thresholds at or above 0.95 for gating.
- Use baseline floors for telemetry and control-plane budgets before adaptive updates.
