---
name: beam-tracking-ml
description: Design and refactor beam tracking ML/RL pipelines (CSI teacher vs RSRP student), enforce shape contracts, and produce inference-safe models.
allowed-tools: Read, Grep, Glob, Bash
---

# Beam Tracking ML Skill

Use this Skill when:
- translating the RL架構 diagram into code
- refactoring `sionna_beam_tracking_v2.py` ideas into modular components
- designing observation/action schemas

## Guardrails
- Always define and test shapes (B,N_BEAMS) etc.
- Keep student (online) policy lightweight and deterministic.
- Treat CSI-heavy path as offline only unless we explicitly design compression.

## Where to put code
- Models: `beam_tracking/model/`
- Training scripts: `scripts/` (do not bloat runtime xApp)
- Interfaces: `beam_tracking/schemas.py`

## Suggested distillation workflow
1) Train teacher on CSI dataset (offline).
2) Run teacher over same trajectories, log action distributions.
3) Train student to match teacher (KL divergence).
4) Optionally fine-tune student with small online data.
