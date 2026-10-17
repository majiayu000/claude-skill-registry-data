---
name: improve
description: Autonomous session-exit skill that improves all ecosystem files from
  session learnings
version: 1.4.0
category: workspace-hub
author: workspace-hub
type: skill
trigger: session-exit
auto_execute: false
tools:
- Read
- Write
- Edit
- Bash
- Grep
- Glob
- Task
related_skills:
- knowledge-management
- skill-creator
capabilities:
- config_improvement
- skill_lifecycle
- memory_management
- rule_enhancement
- doc_updates
- ecosystem_review
tags:
- self-improvement
- ecosystem
- session-exit
- meta
platforms:
- all
requires: []
---

# Improve

## Sub-Skills

- [Trigger Conditions](trigger-conditions/SKILL.md)
- [Phase 1: COLLECT — Gather Session Signals (+6)](phase-1-collect-gather-session-signals/SKILL.md)
- [Decision Logic (Scoring)](decision-logic-scoring/SKILL.md)
- [Creating New Skills (+3)](creating-new-skills/SKILL.md)
- [Integration](integration/SKILL.md)
- [Scope](scope/SKILL.md)
- [Related Commands](related-commands/SKILL.md)
- [Manual vs Automatic Invocation](manual-vs-automatic-invocation/SKILL.md)

## Iron Law

> No improvement shall be applied without a scored candidate entry and evidence of the session signal that triggered it — no speculative edits to skills, rules, or config.

## Rationalization Defense

| Excuse | Reality |
|--------|---------|
| "This improvement is obviously correct, no need to score it" | Obvious-seeming improvements have broken skills before. The scoring gate exists to catch false positives. |
| "I'll create the candidate entry after I apply the change" | Post-hoc justification is not a gate — it is rubber-stamping. Score first, apply second. |
| "The user asked me to improve this skill directly" | Direct user requests bypass the nightly pipeline, but they do not bypass the evidence requirement. Show the signal before editing. |
| "This is just a typo fix, not a real improvement" | Typo fixes are fine inline. But if you are changing behavior, logic, or constraints, it is an improvement and needs a candidate entry. |

## Red Flags

These phrases signal you are about to violate the Iron Law:
- "while I'm here, let me also update this skill"
- "this improvement is straightforward enough to apply directly"
- "I noticed this could be better"
- "no need for a candidate entry — this is minor"
