---
name: task-decomposition
description: Use when breaking PonyBunny work into small, ordered, verifiable tasks with explicit dependencies and acceptance criteria.
---

# Task Decomposition

## Use this skill when
- turning a plan into implementation tasks
- splitting a complex migration into phases
- preparing generator-ready work
- reducing ambiguity before coding

## Goals
- reduce scope creep
- improve sequencing
- produce clear acceptance criteria
- separate implementation from validation

## Process
1. Define the target outcome.
2. List invariants and constraints.
3. Split by dependency.
4. Separate design, implementation, and verification tasks.
5. Add acceptance criteria to each task.
6. Add handoff expectations.

## Output contract
For each task return:
- task name
- objective
- dependencies
- affected files/modules
- acceptance criteria
- risks
- required handoff notes
