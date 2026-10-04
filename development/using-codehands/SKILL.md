---
name: using-codehands
description: >
  Introduction and onboarding for the CodeHands agent skills framework.
  Use when starting a new session, when a user mentions CodeHands, or
  when you need to understand how the framework works.
version: 1.0.0
permissions:
  - fs.read
triggers:
  - context: "first message in a new session"
  - context: "user mentions CodeHands"
platforms:
  - claude-code
  - cursor
  - gemini-cli
  - copilot
  - codex
  - opencode
  - windsurf
  - kiro
author: codehands-core
signed: true
tier: 2
---

## Overview

CodeHands is a production-grade agent skills framework that provides 33 composable skills across 8 development phases. It guides AI coding agents toward engineering excellence through mandatory workflows, anti-rationalization tables, and verification gates. Named after the "Invisible Hand" — developers pursuing their own interests produce better code through CodeHands' structured guardrails.

## When to Use

- At the start of every session — familiarize yourself with available skills
- When a user asks "what can you do?" or "how do you work?"
- When you need to decide which skill applies to the current task
- NOT when you're already deep in a skill workflow

## Process

### 1. Start with the Task Decomposition Engine

Every request — no matter how small — passes through the root orchestrator FIRST:

```
★ TASK-DECOMPOSITION-ENGINE (always first)
  ↓ classifies → assesses → reconnoiters → decomposes → routes
  ↓
DEFINE → PLAN → BUILD → ORCHESTRATE → VERIFY → REVIEW → SHIP → GOVERN
 /spec   /plan  /build                /test    /review  /ship   /audit
```

Read `skills/task-decomposition-engine/SKILL.md` — it decides which phases apply to your current task.

### 2. Skill Activation

Skills activate in two ways:
- **Contextual**: Automatically based on what you're doing (e.g., writing code triggers `codehands:test-driven-development`)
- **Slash commands**: Manually via `/spec`, `/plan`, `/build`, `/test`, `/review`, `/ship`, `/debug`, `/audit`

### 3. Core Principles

These are non-negotiable:

1. **Test first, always.** No production code without a failing test. See `codehands:test-driven-development`.
2. **Verify before declaring success.** Run the code. Check the output. Confirm it works. See `codehands:verification-before-completion`.
3. **Security is not optional.** Every feature gets security review. See `codehands:security-and-hardening`.
4. **Read before writing.** Understand existing code before modifying it. See `codehands:source-driven-development`.
5. **Surface ambiguity.** When uncertain, ask the human — don't guess.

### 4. Anti-Rationalization

Every skill includes a "Common Rationalizations" table — excuses agents use to skip steps, with factual rebuttals. When you feel the urge to skip a step, check the table first. The rationalization table is behavioral shaping code, not optional documentation.

### 5. Model Awareness

CodeHands detects which LLM you are and adjusts skill enforcement language accordingly. You don't need to do anything — the framework handles this via `model_variants` in skill frontmatter.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "This project is too simple for all these skills" | Simple projects are where unexamined assumptions cause the most wasted work. The process can be short, but it must happen. |
| "I'll write tests after the code works" | This is the #1 predictor of untested code in production. TDD is mandatory. |
| "Security isn't relevant for this task" | Every feature that handles user input, makes network calls, or touches data has security implications. |
| "The user seems to be in a hurry, I'll skip review" | Skipping review to save 5 minutes costs hours in debugging later. |

## Red Flags

- Jumping straight to code without understanding requirements
- Writing tests after production code
- Declaring "done" without running the code
- Ignoring anti-rationalization tables

## Verification

- [ ] You understand the 8-phase lifecycle
- [ ] You know which slash command maps to which phase
- [ ] You have identified which skills are relevant to the current task
- [ ] You have not skipped any mandatory workflow

## See Also

- `codehands:task-decomposition-engine` — Root orchestrator (start here)
- `codehands:codebase-reconnaissance` — Understand before modifying
- `codehands:risk-assessment-and-escalation` — Auto-escalate risky changes
- `codehands:test-driven-development` — The Iron Law of TDD
- `codehands:systematic-debugging` — 4-phase root cause investigation
- `codehands:security-and-hardening` — OWASP-aligned security engineering
- `codehands:context-engineering` — Manage your context window efficiently
