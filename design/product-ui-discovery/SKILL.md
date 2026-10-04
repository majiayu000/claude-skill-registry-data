---
id: frontend.design.product-ui-discovery
name: Product UI Discovery
description: Translate a frontend request into a focused user outcome, task flow, content hierarchy, edge states, and measurable acceptance criteria.
stack:
  - Product
  - UX
  - Frontend
category: design
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - product intake
  - UX flow
  - user journey
  - empty state
  - microcopy
---

# Product UI Discovery

## Purpose

Prevent attractive but directionless frontend changes by making the user problem, primary task, state model, and success evidence explicit before implementation.

## When to Use

Use this skill when:

- a request describes screens or components but not a user outcome;
- a flow has permissions, loading, empty, error, confirmation, or recovery states;
- product copy or interaction choices could change completion, trust, or support load.

## Do

- Identify the primary user, their context, the desired outcome, and the smallest successful path.
- Map happy path and credible failure, empty, loading, permission, and destructive-action states.
- Write concise, action-oriented content that explains what happened and what can happen next.
- Convert decisions into observable acceptance criteria, including accessibility and responsive constraints.
- Keep design tools optional: diagrams, prototypes, and handoff systems can support discovery but are not required inputs.

## Do Not

- Do not start by copying a component library pattern without confirming it fits the user task.
- Do not invent business policy, analytics targets, personas, or legal requirements.
- Do not use a visual mockup as a substitute for state and content decisions.
- Do not couple the workflow to a named design vendor or collaboration platform.

## Review Checklist

- [ ] The problem, user outcome, and non-goals are stated.
- [ ] Primary, alternate, empty, loading, error, and permission states are covered where applicable.
- [ ] Copy uses clear nouns and verbs and explains recovery actions.
- [ ] Acceptance criteria are testable without relying on a particular design tool.
- [ ] Product decisions are separated from implementation choices.

## Expected Output

1. Produce a compact task-flow and state inventory.
2. List decisions, assumptions, and unanswered product questions.
3. Define testable frontend acceptance criteria.
4. Route component implementation to the relevant framework or design-system skill.
