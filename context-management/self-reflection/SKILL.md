---
name: self-reflection
description: |-
  Turn owner feedback about agent behavior into concrete system changes. Use when the owner says
  something is off, wants the assistant to improve how it operates, asks for a reflection, or wants
  a durable fix instead of a one-off apology.
---

# Self-Reflection

Use this when the owner wants a real operating change, not just a nicer reply.

## Goal
Convert vague dissatisfaction into technical updates to prompts, memory, skills, config, tooling, or routines.

## 1. Understand the Problem
Ask at most 2-3 focused questions, only if needed:
- What specifically went wrong?
- What should have happened instead?
- Is this a local tweak or a deeper operating issue?

If the failure is already clear from context, skip the questions and move to diagnosis.

## 2. Deep System Scan
Read broadly before changing anything.

### Core behavior
Check the relevant parts of:
- `SOUL.md`
- `IDENTITY.md`
- `USER.md`
- `MEMORY.md`
- relevant daily notes
- tool or channel instructions that affect the behavior

### Skills
Check:
- the directly related workspace skills
- any bundled skill that overlaps
- collisions where a workspace skill overrides a bundled one

### Runtime / config
Check anything relevant to the issue:
- model or routing settings
- channel behavior
- queue / heartbeat behavior
- crons
- helper scripts or hooks

## 3. Diagnose
Present a short diagnosis before editing behavior-critical files:
1. **Root cause** — what produced the bad behavior
2. **Proposed changes** — exact files to change
3. **Side effects** — what else those changes might affect
4. **Alternatives** — only if there are real tradeoffs

Do not offer fake fixes like "I'll be more careful" unless that is backed by a concrete system change.

## 4. Implement After Approval
Once approved, make the changes concretely:
- edit prompts or memory files
- create or update skills
- adjust scripts, hooks, or config
- add/remove cron behavior if timing is the issue

Prefer the smallest durable fix that prevents repeat failures.

## 5. Verify
- Re-read the changed files for consistency.
- Run a small proof when possible: test, grep, diff, or reproduction check.
- Document what changed and why.
- Commit the changes.

## Principles
- Scan everything relevant, then change only what matters.
- Behavioral fixes need technical artifacts.
- Owner approval is required before changing core behavior rules.
- If a limitation is model-level, say that plainly.
- The output of reflection is a durable improvement, not a performance of regret.
