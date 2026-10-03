---
name: system-architecture
description: Align implementation and docs with the repo's 10-layer vision (docs/FINAL_SYSTEM_VISION.md) and AGENTS.md. Use when planning or reviewing cross-cutting features touching AI (Layer 5), learning (Layer 6), risk (Layer 7), observability (Layers 9–10), or when layer numbering or responsibilities are unclear.
---

# System architecture alignment

## Purpose

Keep coding agents, skills, and PRs consistent with:

1. **`docs/FINAL_SYSTEM_VISION.md`** — canonical product and architecture vision (10 layers).  
2. **`AGENTS.md`** — enforceable module boundaries, safety defaults, and **current** code mapping.  
3. **`docs/IMPLEMENTATION_GAP.md`** — short **vision vs implementation** honesty (optional read when scoping work).

This skill does **not** replace reading those files.

## Layer anchors (must not swap)

- **Layer 5** = **AI support** — LLM **confirmation / recommendation**; never the only authority for execution.  
- **Layer 6** = **Learning and optimization** — outcome-driven improvement, shadow/diagnostic first in this repo unless explicitly extended.

## Cross-cutting principles (binding with `AGENTS.md`)

- **Strong operator observability** — L9–L10 surfaces and journals should reflect what the system did and why.
- **Continuous research / testnet data** — prefer runs that feed journals and metrics for L6; avoid untracked “fire and forget” experiments.
- **Bounded autonomy** — autonomous loops stay within config, env, and operator controls; no silent background traders.
- **No black-box runtime** — no untraced changes to effective signals, weights, or risk; decision paths remain structured and logged where the repo already does so.

## Use when

- Designing or reviewing features that span multiple packages (`market`, `strategies`, `ai`, `learning`, `risk`, `execution`, `operator_panel`).  
- Documenting or refactoring “layers” in skills or README.  
- Clarifying whether a change belongs to advisory AI (L5) vs learning (L6) vs risk (L7).

## Do not use when

- Single-file trivial edits with no architectural implication.  
- Replacing a full read of `FINAL_SYSTEM_VISION.md` for detailed formulas or future data sources.

## Workflow

1. Read **`AGENTS.md`** (boundaries + safety).  
2. Skim relevant sections of **`docs/FINAL_SYSTEM_VISION.md`** for the layers you touch.  
3. Ensure the change **advances** the vision without **violating** AGENTS (paper default, risk not bypassed, AI advisory, learning not secretly trading).  
4. Prefer minimal diff; update skills/docs only when guidance would otherwise stay wrong.

## Output

- State which **layers** are affected (numbers + names).  
- Note **vision vs current repo** gap if the implementation is partial.  
- Explicit **safety** confirmation: risk ordering, paper defaults, no live enablement.
