---
name: using-opm
description: Establishes how to find and invoke OPM skills before taking any other action, including clarifying questions. Use when starting any conversation or task, before exploring the codebase, answering a question, entering plan mode, or writing code.
---

# Using OPM

This file is injected at SessionStart by the OPM plugin hook, so it stays short. Subagents dispatched to execute a single task: ignore this skill.

## The Rule

If there is even a small chance a skill applies to what you are about to do, invoke it BEFORE any other action: before clarifying questions, before exploring the codebase, before checking files. If it turns out wrong for the situation, you do not have to use it.

Then announce "Using opm:<name> to <purpose>" and follow the skill exactly. If it has a checklist, create a todo per item.

## How to Invoke

- Skill tool: `Skill(skill: "opm:<name>")`, or the slash command `/opm:<name>`.
- Process skills come first (they set the approach); implementation skills carry it out.
- "Let's build X" -> `opm:brainstorming` first. "Run this plan" -> `opm:executing-plans`.
- Before entering plan mode: if you have not brainstormed yet, invoke `opm:brainstorming` first.

## Workflow Map

1. `opm:brainstorming` - classify (spike / bounded / architectural), design, get approval. Architectural work writes `docs/specs/YYYY-MM-DD-<topic>.md`.
2. `opm:writing-plans` - turn the approved spec into bite-sized TDD tasks in `docs/plans/YYYY-MM-DD-<topic>.md`.
3. `opm:executing-plans` - fresh subagent per task, reviewer gate, progress ledger. Every task follows `opm:tdd-workflow`.
4. `opm:verification-before-completion` - fresh evidence before any "done", commit, or PR.
5. `opm:compound-learnings` - capture anything non-obvious learned along the way.

Scope larger than about a week, or several phases: use `opm:milestone-planning` between steps 1 and 2.
New project from a single brief: `opm:jump-start <project-name> <brief>` runs the whole loop.
Idea not settled yet: `opm:brew-idea <brief>` has four agents argue it out and returns a ranked feature list and plan to feed step 1.
Explainer video of a spec or document: `opm:explainer-video <path>` makes a narrated slideshow (MP4) from it.

## Red Flags

These thoughts mean STOP - you are rationalizing:

| Thought | Reality |
|---------|---------|
| "This is just a simple question" | Questions are tasks. Check for skills. |
| "I need more context first" | Skill check comes BEFORE clarifying questions. |
| "Let me explore the codebase first" | Skills tell you HOW to explore. Check first. |
| "I can check git/files quickly" | Files lack conversation context. Check for skills. |
| "This doesn't need a formal skill" | If a skill exists, use it. |
| "I remember this skill" | Skills evolve. Read the current version. |
| "This doesn't count as a task" | Action = task. Check for skills. |
| "The skill is overkill" | Simple things become complex. Use it. |
| "I'll just do this one thing first" | Check BEFORE doing anything. |
| "I know what that means" | Knowing the concept is not using the skill. Invoke it. |

## Precedence

User instructions (CLAUDE.md, rules files, direct requests) override skills; skills override default behavior. Skip a skill workflow only when the user has explicitly told you to.

<!-- Adapted from obra/superpowers (MIT) -->
