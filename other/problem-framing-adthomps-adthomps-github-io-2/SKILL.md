---
name: problem-framing
description: Use when work must frame the real problem, expose assumptions, compare meaningful options, and explain decisions in beginner-clear language.
kind: skill
status: active
owner: APT
last_updated: 2026-08-16
source: consolidated APT guidance
title: "Problem Framing"
domain: "thinking"
source_paths: ["apt-principles-agents/skills/thinking/problem-framing/SKILL.md"]
---

# Problem Framing

## Purpose

Produce a reviewable problem framing outcome that is grounded in repository evidence and explicit about uncertainty.

## When to Use

Use for planning, design, implementation review, migration, troubleshooting, or documentation where the task must frame the real problem, expose assumptions, compare meaningful options, and explain decisions in beginner-clear language.

## Inputs

- Goal, audience, scope, constraints, and success criteria.
- Relevant source files, contracts, examples, logs, and decisions.
- Known risks, assumptions, dependencies, and approval boundaries.

## Process

1. Separate the observed problem, requested solution, desired outcome, and affected audiences; flag where they do not logically align.
2. Build an evidence table that distinguishes verified facts, interpretations, assumptions, constraints, and unknowns with owners.
3. Define measurable success and failure signals plus the decision horizon, reversibility, and cost of delay.
4. Generate at least two viable options, including “do nothing” or a smaller experiment when appropriate, and compare tradeoffs against explicit criteria.
5. Seek disconfirming evidence for the leading option and identify which assumption would invalidate the recommendation.
6. Record the decision, rationale, rejected alternatives, validation step, review date, and unresolved questions without presenting assumptions as facts.

## Outputs

A concise recommendation, evidence map, required changes, risks, validation plan, support/documentation impact, and approval status.

## Quality Bar

The output is practical, source-backed, audience-aware, testable, reversible where possible, and does not state assumptions as facts.

## Domain Checklist

- Treat **Problem Framing** as an explicit decision with defined scope, evidence, owner, and validation.
- Required evidence: problem statement, assumptions, alternatives, decision, measurable outcome.
- Show how the proposed action changes the desired outcome; reject solution-first framing when that causal link is unsupported.
- Prefer the smallest reversible test that can resolve a consequential unknown before committing to broad implementation.
- State what is verified, what is assumed, and what requires specialist or human approval.

## Required Reading

Read the canonical Thinking principle hub, the closest enforceable standard, the applicable checklist, and exact target-repository evidence.
## References

- [Thinking principles](../../../principles/thinking/README.md)
- [Templates](../../../templates/README.md)
- [Agents](../../../agents/README.md)
