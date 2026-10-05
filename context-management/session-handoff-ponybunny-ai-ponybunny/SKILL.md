---
name: session-handoff
description: Use when concluding or pausing work so the next Claude Code session can continue reliably without hidden context.
---

# Session Handoff

## Use this skill when
- ending a meaningful work session
- pausing a migration mid-phase
- handing work from one subagent or session to another
- recording partial completion honestly

## Goals
- preserve continuity safely
- prevent hidden context loss
- distinguish implemented from verified
- make the next safest step obvious

## Required handoff contents
1. What changed
2. Current status
3. What is verified
4. What is still unverified
5. Open risks or questions
6. Recommended next safest step
7. Files/docs to read first next time

## Rules
- do not mark something verified without evidence
- do not hide partial work
- do not leave future sessions guessing where to resume
- do not rely on memory alone

## Output contract
Return a handoff note using the required handoff contents exactly.
