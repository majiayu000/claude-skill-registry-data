---
name: dynamic-programming-analysis
description: Break overwhelming problems, decisions, or plans into DP-style sub-problems (base cases, dependencies, reused parts) and solve bottom-up. Use when user says "I don't know where to start", "break this down", "what's the best way to...", or asks for a step-by-step plan, decision matrix, project roadmap, or architecture decomposition.
metadata:
  author: Ronnasayd Machado - github.com/Ronnasayd
  version: "1.1.0"
---

# Dynamic Programming Analysis

Breaks any complex problem into DP-style sub-problems: **optimal substructure** (solution depends on smaller solutions) + **overlapping sub-problems** (recurring parts, solve once, reuse). Applies to business, personal decisions, architecture, research, learning, projects.

## Protocol

| #   | Step                | Action                                                                              | Gate                                                  |
| --- | ------------------- | ----------------------------------------------------------------------------------- | ----------------------------------------------------- |
| 1   | Define main problem | Restate precisely, final state, explicit/implicit constraints                       | —                                                     |
| 2   | Decompose           | Break into smaller parts; recurse until **base cases** (directly solvable)          | tree structure, see `references/response-template.md` |
| 3   | Identify overlaps   | Which sub-problems recur across branches? Which partial solutions reuse?            | mark explicitly — biggest efficiency win              |
| 4   | Resolution order    | Base cases first, then by dependency (prereq before dependent)                      | execution sequence                                    |
| 5   | Solve each          | Smallest → largest; compare options if multiple; note which parent problem it feeds | —                                                     |
| 6   | Compose             | Combine sub-solutions into original problem; validate fit                           | —                                                     |
| 7   | Verify              | Edge cases, external dependencies, optimal vs. good-enough                          | —                                                     |

Respond using the template in `references/response-template.md`.

## Adaptations by problem type

| Type                   | Sub-problem                | Base case                            | Overlap                                     | Composition               |
| ---------------------- | -------------------------- | ------------------------------------ | ------------------------------------------- | ------------------------- |
| Decision               | each criterion             | verifiable facts, not opinions       | criteria affecting multiple options         | decision table/matrix     |
| Planning/Project       | each deliverable/milestone | atomic task (1 person, 1 day)        | shared deps between phases                  | schedule/roadmap          |
| Technical/Architecture | each component/module      | primitive functions/services         | reusable utilities/patterns                 | integration diagram       |
| Learning               | each prerequisite concept  | needs-no-prerequisite knowledge      | fundamentals unlocking multiple topics      | ordered learning path     |
| Business/Strategy      | each strategic lever       | observable metrics, concrete actions | capabilities supporting multiple strategies | integrated strategic plan |

## Quality principles

- Granular: each sub-problem has a clear, direct answer.
- No pseudo-decomposition: genuinely break down, don't just rename the problem.
- Name dependencies explicitly (what depends on what).
- Bottom-up only — solving big before small causes rework.
- State reuse explicitly when one solution supports another.

## Reference files

- `references/response-template.md` — verbatim markdown response template + sub-problem tree text format.
- `references/example.md` — worked example (career transition into AI).
