---
name: repo-system-research
description: Research the open web for enhancement opportunities (Layer 3 — Opus subagent with WebSearch + WebFetch). Topic-driven. Returns structured findings with hype tags + source URLs. Does NOT auto-implement.
allowed-tools:
  - Bash
  - Read
  - Edit
  - Write
  - Glob
  - Grep
  - Agent
  - TodoWrite
model: opus
argument-hint: [optional research topic, ≥3 words]
---

# System Research — entry point (Layer 3)

This skill is the invocation handle for outward-facing R&D. The architecture, 8 finding categories, anti-hallucination controls, verbatim Layer 3 subagent prompt, topic auto-discovery scoring heuristic, and output rendering format all live in the workflow doc — this file just routes you there.

## When this fires

Auto-triggers when the user wants to scan the open web for enhancement opportunities — or explicit `/repo-system-research [topic]`. Designed for "leftover credits" use, weekly cadence: find one improvement to consider, discuss it, done.

This is **Layer 3** of the three-layer system_audit pipeline. Layers 1+2 (`audit` skill) look INWARD for rot; Layer 3 looks OUTWARD for enhancements. Convergent vs divergent — different jobs.

## Arguments

`$ARGUMENTS` is an optional research topic. If provided, must be ≥3 words (the workflow's Step 3 sanity-checks this). If absent, the auto-discovery heuristic in the workflow proposes 2–3 candidate topics for the user to pick from.

## Begin

Read [workflows/system_research.md](../../../workflows/system_research.md) — authoritative spec. The "Orchestration sequence" section defines the 7 steps and contains:
- The verbatim Layer 3 prompt to pass to the subagent (Step 4)
- The topic auto-discovery scoring heuristic (Step 3, mode b)
- The output rendering format (Step 5)

The "Anti-hallucination + anti-hype controls" section enumerates the 8 hard rules (mandatory source URLs, 4-tier authority model, system-map cross-check, additive-only, freshness window, topic anchor, hard search budget).

Then execute Steps 1–7 from the workflow. Hard rule: **only ONE enhancement adopted per invocation.**

## See also

- [tools/system_audit.py](../../../tools/system_audit.py) — Layer 1, runs in Step 1 prelude
- [.claude/skills/audit/SKILL.md](../audit/SKILL.md) — Layers 1+2, the convergent counterpart
