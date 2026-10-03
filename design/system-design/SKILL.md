---
name: system-design
description: Architect a feature or subsystem BEFORE code exists — decompose requirements into data model, boundaries, data flow, and risk surface. Use when the user asks to plan, design, or architect anything, says "system design", or when a task crosses more than one module boundary.
allowed-tools: Read, Grep, Glob, Bash
---

# System Design

You are designing, not implementing. The output is a design document the user approves before a single line of code exists. This is the upstream twin of the `system-reviewer` agent (which validates finished work against these same principles).

Read `learnings.md` beside this file before starting; append an entry when a design decision later proved wrong or a section of the template earned its keep.

## Governing Principle

> **Separation of concerns + explicit boundaries.** Every feature decomposes into data, behavior, and presentation layers with declared contracts between them. No layer should assume the internals of another.

## Procedure

1. **Discover** the relevant slice of the existing system. Before proposing anything: read the current data model (schema + relations), the routes the feature touches, the closest existing service module, and any documented design patterns or architecture rules. Never design against an imagined codebase.
2. **State** the feature in one sentence — what the user can do afterward that they can't today. If ambiguous, ask before designing.
3. **Decompose** the feature into the design document structure below.

### Design document structure

- **Data model** — new/changed entities, fields, foreign keys, indexes for the queries you're about to define. Show the schema diff, not prose.
- **Data flow** — for each user action: route → server function (+ middleware chain) → authorization check → service → persistence. One line per hop. Name real files — existing or to-be-created — following the project's established module triangle.
- **Route plan** — new routes, loader vs component-level data, what streams vs what blocks, cache keys and invalidation strategy.
- **Boundary & risk table** — authorization rule per endpoint (who may call it, which check enforces it), rate-limit tier, input validation schema, worst-case abuse scenario.
- **Runtime constraints** — anything affected by the deployment target (edge runtime limits, stateless instances, cold starts, API restrictions).
- **Open questions** — decisions only the user can make (product behavior, tradeoffs). Max 3, concrete.

## Constraints (non-negotiable)

- **Discover before inventing.** Prefer extending existing modules over creating new ones; state explicitly when reuse was rejected and why.
- Every endpoint in the design MUST name its middleware, authorization check, and input validation schema — a design without its boundary column is incomplete.
- Keep it under ~1 page; a design that can't be read in 3 minutes won't be followed.

## Handoffs

- After the user approves the design → implementation follows `/patterns` (discover exemplar files per piece).
- UI surfaces in the design → hand the route plan to `/web-design-patterns` for data-loading/UX flow decisions and `/creative-ui` for the visual layer.
- After implementation → `/full-review` validates the built system matches this design; paste the design doc into the review context.
