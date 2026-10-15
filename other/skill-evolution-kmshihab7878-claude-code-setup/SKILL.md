---
name: skill-evolution
description: >
  Self-evolving skill lifecycle with three triggers: post-execution fix, degradation detection,
  and periodic metric review. Skills improve automatically based on real execution data.
risk: low
tags: [process, quality, meta, skills]
created: 2026-03-25
updated: 2026-03-25
---

# Skill Evolution

Framework for treating skills as living entities that evolve based on execution feedback.
Inspired by HKUDS/OpenSpace's self-evolving skill engine.

## How to use

- `/skill-evolution`
  Review all skills for evolution candidates based on recent execution patterns.

- `/skill-evolution <skill-name>`
  Analyze a specific skill's health metrics and propose evolution if needed.

## When to use

- A skill consistently fails or produces poor results
- After significant codebase or tool changes that may degrade existing skills
- During periodic maintenance (weekly recommended)
- When the autoresearch loop identifies a skill as underperforming

## When NOT to use

- For brand new skills (let them accumulate execution data first)
- During active development of a skill (wait for it to stabilize)

## Core Concept: Skills as Living Entities

Static skills degrade over time as:
- Underlying tools change or deprecate
- Codebase patterns evolve
- User needs shift
- Models improve (old constraints become unnecessary)

**Solution**: Track execution metrics per skill and evolve them through three triggers.

## Three Evolution Triggers

### Trigger 1: Post-Execution Analysis (Reactive, Per-Task)

After each significant skill application:
1. Did the skill produce the expected output?
2. Were there manual corrections needed?
3. Was the skill's guidance followed or overridden?

**Action**: If corrections were needed 3+ times, trigger FIX evolution.

### Trigger 2: Degradation Detection (Reactive, Cross-Task)

Monitor across multiple executions:
- Success rate dropping below threshold (< 70%)
- Increasing override frequency
- Growing number of exceptions/workarounds

**Action**: If degradation detected, trigger DERIVED evolution (create improved variant).

### Trigger 3: Periodic Health Review (Proactive)

On schedule (weekly/monthly):
- Scan all skills for staleness (no use in 30+ days)
- Check for skills that reference deprecated tools or patterns
- Identify skills with low confidence scores in memory

**Action**: Flag for review, propose updates or retirement.

## Three Evolution Modes

### FIX: In-Place Repair
- Minimal targeted changes to fix specific failures
- Preserves original intent and structure
- Applied when root cause is identified and isolated

### DERIVED: Enhanced Variant
- Creates improved version from parent skill
- Inherits base structure, adds improvements
- Used when the skill concept is sound but execution needs rethinking

### CAPTURED: New Pattern Extraction
- Extracts novel patterns from successful ad-hoc executions
- Creates new skills from recurring successful behaviors
- Maps to Operating Framework promotion policy (3+ successes = template)

## Skill Health Metrics

Track these per skill (store in memory or dedicated log):

| Metric | Description | Healthy | Warning | Critical |
|--------|-------------|---------|---------|----------|
| Applied Rate | How often the skill is triggered | > 1/week | 1/month | < 1/quarter |
| Completion Rate | Tasks completed when skill is active | > 80% | 60-80% | < 60% |
| Override Rate | How often user overrides skill guidance | < 20% | 20-40% | > 40% |
| Freshness | Days since last update | < 30 | 30-90 | > 90 |

## Evolution Process

```
1. DETECT: Trigger fires (post-exec, degradation, or periodic)
2. DIAGNOSE: Identify what's failing and why
3. PROPOSE: Generate minimal diff (FIX), new variant (DERIVED), or new skill (CAPTURED)
4. REVIEW: Human approval required before applying
5. APPLY: Update SKILL.md
6. VERIFY: Test evolved skill on the original failure case
7. LOG: Record evolution in memory (date, trigger, changes, outcome)
```

## Integration with Existing Setup

| Component | Integration |
|-----------|------------|
| `autoresearch` skill | Evolution triggers feed into autoresearch improvement loops |
| `prompt-reliability-engine` | Mode 9 (Self-Improving) maps directly to this framework |
| `skill-creator` | Creates the initial skill; this skill manages its lifecycle |
| `skill-architect` | Designs skill systems; this skill keeps them healthy |
| Memory system | Evolution logs stored in `mistakes.md` and `patterns.md` |
| Operating Framework | 3+ success promotion policy drives CAPTURED evolution |

## Cross-references

- **autoresearch** skill: Karpathy-inspired iterative improvement (broader scope)
- **prompt-reliability-engine** skill: Mode 9 (Self-Improving Skill) for prompt-specific evolution
- **skill-creator** skill: initial skill creation
- **operating-framework** skill: promotion policy and maintenance cadence
- **OpenSpace** (HKUDS): original research on self-evolving AI agent skills
