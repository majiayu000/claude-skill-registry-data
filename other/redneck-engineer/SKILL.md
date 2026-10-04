---
name: redneck-engineer
description: Turns a vague idea into a clear build plan — short PRD, task list, user flows, constraints, and acceptance criteria — so Claude Code knows exactly what to build; invoke via /redneck-engineer when you know what you want but Claude keeps building the wrong thing.
---

# Redneck Engineer

You know what you want; the problem is getting it out of your head and onto paper before anyone starts welding. This skill drags a fuzzy idea into a tight, buildable spec so the next agent stops guessing and starts shipping the right thing.

## When to use
- You have an idea but Claude keeps building the wrong interpretation of it.
- You want a plan/spec before any code gets written.

## Behavior
1. Interrogate the idea first: ask the 3-5 sharpest clarifying questions that would change the build, and wait for answers before planning.
2. Write a short PRD — problem, goal, target user, in-scope and explicitly out-of-scope.
3. Lay out the primary user flows step by step, including the unhappy paths.
4. List hard constraints: stack, performance, data, deadlines, and anything that must not change.
5. Break the build into an ordered task list small enough that each item is unambiguous.
6. Define acceptance criteria — concrete, checkable conditions that mean "done" — for the whole thing and key tasks.
7. Call out open questions and assumptions so nothing silently gets decided wrong.

## Output
A compact, buildable spec — PRD, user flows, constraints, ordered task list, and acceptance criteria — ready to hand straight to an implementing agent.
