---
name: planner-generator-evaluator-pattern
description: Use when structuring work so that planning, candidate generation, and verification remain separate and explicit.
---

# Planner Generator Evaluator Pattern

## Use this skill when
- a task is large enough to require structured delegation
- implementation quality depends on explicit evaluation
- a migration needs safer control points
- you want to avoid generator self-approval

## Goals
- separate planning from implementation
- separate implementation from verification
- reduce false completion claims
- improve traceability and decision quality

## Responsibilities
- planner: defines phases, constraints, acceptance criteria, and verification points
- generator: produces candidate implementation for approved scope
- evaluator: determines whether the implementation is actually verified

## Process
1. Define the problem.
2. Ask planner to create the phased path.
3. Ask generator to implement only one approved phase.
4. Ask evaluator to assess the result against evidence.
5. Feed failures and weak spots into future planning or harness improvement.

## Output contract
Return:
- recommended delegation
- phase boundaries
- evidence boundaries
- stop/go points
