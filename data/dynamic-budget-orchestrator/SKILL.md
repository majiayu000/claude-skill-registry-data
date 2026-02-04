---
name: dynamic-budget-orchestrator
description: Dynamically scale model token budgets using resource telemetry, prompt size, and profile presets. Use when token limits must adapt to hardware constraints, per-request size, or safe/fast/quality modes.
---

# Dynamic Budget Orchestrator

Use this skill to make LLM token limits elastic to local resources and request size.

## Workflow

1) Capture RAM and VRAM snapshot (best effort).
2) Estimate prompt size and compute a prompt-based cap.
3) Apply a profile factor (safe, fast, balanced, quality).
4) Clamp to min/max and emit an effective token budget.

## Scripts

- Run: python skills/automation/dynamic-budget-orchestrator/scripts/probe_budget.py

## References

- references/profile_presets.json
