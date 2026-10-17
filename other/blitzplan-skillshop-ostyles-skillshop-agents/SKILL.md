---
name: blitzplan
description: "Lightweight design coach: 3-5 questions, a clear spec, no code until you approve. Inspired by superpowers, built for vibe coders."
trigger: /blitzplan
vibe: true
---

# /blitzplan

## What this is for

You want to build something. Before you start prompting code, blitzplan helps you clarify scope, tech stack, and auth model in 3-5 questions. No code until you approve the design. This prevents wasted effort from vague specs and unexamined assumptions.

## Usage

- `/blitzplan <description>` - start a design session
- `/blitzplan quick` - 3 questions, ready in 2 minutes
- `/blitzplan full` - up to 5 questions, more depth
- `/blitzplan -help` - show full usage and stop

## HARD-GATE - read before ANY code

If the user describes a feature, component, or app change and immediately asks for code: STOP. Ask if they want to run `/blitzplan` first.

No code, no implementation prompt, no scaffolding before the user has approved a design. This applies to EVERY feature regardless of perceived simplicity.

A "design" can be 3 sentences. You still need approval before implementation.

## DIALOG PROTOCOL - STRICT

Follow DIALOG.md exactly. 4 phases: Welcome -> Clarifying (one question per message) -> Design Presentation -> Plan.

### Rules
1. Only ONE question per message in Phase 1
2. Present design as a compact block (no prose paragraphs)
3. Get explicit approval (`[y/n]`) before showing the plan
4. No files written, no commits - everything stays in the conversation

## Phases

| Phase | What | Questions |
|-------|------|-----------|
| Welcome | 3 options + exit | 1 |
| Clarifying | Scope, stack, users, constraints | 3-5 (one per message) |
| Design | Architecture overview, get approval | 1-2 |
| Plan | Implementation tasks, ask to start | 1 |

## PROTECTION RULE

Never write to files without explicit user consent. This skill is conversation-only.
