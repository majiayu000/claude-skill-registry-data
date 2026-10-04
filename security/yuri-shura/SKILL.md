---
name: yuri-shura
description: "6-perspective adversarial review for high-stakes turns (architecture decisions, refactor planning, deployment review) — fans out architect, adversary (7-vector attack), maintainer, ops, product, and security perspectives in parallel, then consolidates. Use when user says 'review this decision', '/shura', 'adversarial review', 'what could go wrong', 'architecture review', or 'deployment review'."
triggers:
  - "/shura"
  - "strategic review"
  - "architecture review"
  - "yuri-shura"
scope: harness
invocation: workflow
---

# Yuri Shura -- 6-Perspective Review

Inspired by Istishraf (MIT-licensed Claude plugin). Original implementation adapted to Yuri OS's pulse-cortex.

## When to invoke

Model-invocable for high-stakes strategic review (architecture, refactor planning, deployment); or `/shura <topic>`. Advisory only — never holds implementation authority.

## 6 Perspectives (native Workflow fan-out)

Run via the **Workflow tool**: 6 parallel agents, each adopting one perspective lens (Opus/Sonnet, self-selected per depth). Each returns a bounded structured finding; the main thread consolidates. No external model lanes.

| Perspective | Lens |
|---|---|
| Architect | soundness of design |
| Adversary | 7-vector attack protocol (see below) |
| Maintainer | long-term cost |
| Ops | production readiness |
| Product | user impact |
| Security | risk surface |

## Output format

Six bounded sections (50 lines each) consolidated by main thread. Each perspective answers: assessment, risks, recommendation.

## Adversary Protocol — 7-Vector Attack Checklist

The `@ds-pro` adversary lane runs this checklist against every artifact. Derived from Anderson's security framework + Ibn Khaldun's resilience/decay model + SOUL.md reversibility principle. Source: strategic-thinker MIT brief (2026-05-16).

| # | Vector | Question |
|---|--------|----------|
| 1 | **Policy** | Does this violate an explicit rule, boundary, or operating constraint? |
| 2 | **Mechanism** | How could the implementation fail, hang, corrupt state, or be exploited? |
| 3 | **Assurance** | What cannot be monitored, audited, or verified after the fact? |
| 4 | **Incentives** | What system or actor benefits from this failing silently? |
| 5 | **Fragility** | Where are the single points of failure, tight coupling, or cascade paths? |
| 6 | **Scope creep** | What silent expansion or unapproved scope increase does this permit? |
| 7 | **Irreversibility** | How hard is rollback if this is wrong? Is there a tested recovery path? |

Adversary prompt injection: for each vector, deliver one finding or "clean" — no filler. Total output ≤ 35 lines.

## Quarantine rules

Advisory output only — no implementation authority. Findings are consolidated for the owner; any resulting change goes through the normal owner-gated commit path.

## Trigger phrases (auto-classify)

- "architecture review"
- "should we refactor"
- "deployment plan"
- "high stakes"
- "before we ship"

## Session Notes

### 2026-05-17
- session: 113m | peak ctx: 0% | compacts: 0
- tools: Bash×168, Edit×41, Read×33, mcp×33, Write×11, ToolSearch×2, Skill×1, AskUserQuestion×1, ExitPlanMode×1
- corrections: none
- errors: none

### 2026-05-16
- session: 61m | peak ctx: 0% | compacts: 0
- tools: Bash×50, Edit×28, Write×13, Read×12
- corrections: none
- errors: none
