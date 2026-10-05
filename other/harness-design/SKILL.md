---
name: harness-design
description: Use when designing or reviewing PonyBunny as a harness-first system, especially around boundaries, evaluation flow, observability, and migration structure.
---

# Harness Design

## Use this skill when
- defining harness-first architecture
- reviewing whether a design is truly harness-oriented
- deciding where evaluation and handoff should live
- improving observability and recovery behaviour

## Goals
- enforce harness-first thinking
- keep evaluation separate from generation
- make progress measurable
- make failures diagnosable
- make future sessions easier to continue

## Core principles
- generation is not verification
- every important change needs an evidence path
- session handoff must be structured
- traces must support failure reconstruction
- contracts must be explicit
- migrations should be phased and safe

## Process
1. Define the target outcome.
2. Identify current weaknesses.
3. Define the desired role boundaries.
4. Define required artefacts and evidence points.
5. Define migration phases.
6. Define how correctness will be evaluated.
7. Define likely risks.

## Output contract
Return:
- harness-oriented design summary
- role boundaries
- required artefacts
- evaluation points
- migration steps
- risks and trade-offs
