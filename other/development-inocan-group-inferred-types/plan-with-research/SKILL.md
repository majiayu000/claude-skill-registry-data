---
name: plan-with-research
description: Build step-by-step plans grounded in evidence and research. Use when the user asks for a plan, roadmap, steps, or strategy for code, data, or pipeline work.
---

# Plan With Research

## Overview
Create concise, evidence-backed plans with explicit validation for each step.

## Workflow
1. Clarify goal, success criteria, constraints, and timeline.
2. Inspect the repo or data artifacts to confirm reality (prefer local files and logs).
3. Research gaps in docs or external sources only if needed.
4. Draft a plan with 3-7 steps, dependencies, and risks.
5. Include validation checks and rollback or fallback options.

## Plan Format
- Step: verb + concrete deliverable.
- Evidence: cite repo files, docs, or experiments.
- Validation: tests, dry runs, or metrics.

## Honesty Guardrails
- Separate evidence from assumptions; label unknowns explicitly.
- If confidence is low, say so and propose the smallest check to raise it.

## Gating
- If evidence is missing, state assumptions and ask one targeted question.

## Acceptance Criteria
- Each step has a deliverable, evidence note, and validation check.
- Research sources are listed or explicitly noted as not used.
- Risks and rollback/fallback are included.
