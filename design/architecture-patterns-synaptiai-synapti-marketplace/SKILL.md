---
name: architecture-patterns
description: "Document system design decisions with mapped user flows, coupling analysis, failure modes, and explicit non-goals, proving the architecture can survive under unexpected conditions. Use when designing systems, evaluating structural changes, or reviewing architecture decisions. Proactively suggest when coupling analysis reveals circular dependencies, god objects, or hidden shared state."
allowed-tools: Read, Bash, Grep, Glob, TaskCreate, TaskList, TaskUpdate
context: fork
agent: Explore
---

# Architecture Patterns

## Contract

Iron law: **design architecture from functionality, not to functionality — a component that cannot be traced to a user, admin, or system flow is deleted.** Invoked by `/flow:design` Phase 1 (map flows), Phase 2 (C4 level, coupling review, design proposal), and Phase 4 (decision record). Returns the enumerated flows, a coupling analysis with red flags, a proposal (components, responsibilities, dependencies, data flow, API surface) at the right C4 level, and a decision record with context, options, trade-offs, decision, consequences, non-goals, and failure modes. Permitted skips: none — a record without non-goals and failure modes is incomplete and does not ship; failure modes may be deferred only where `/flow:design` marks them optional.

## Map Flows First

Track four tasks: map flows, coupling analysis, design proposal, decision documentation. First enumerate **user flows** (what the user does, step by step), **admin flows** (operator actions), and **system flows** (cron, webhooks, events). Each is trigger, steps, outcome; every component must serve at least one.

## C4 Level

Context, Containers, Components, or Code — start at the highest relevant level and zoom in only when needed; most design discussion happens at Components. Level guide in [`architecture-decision-record.md`](../../references/architecture-decision-record.md).

## Coupling Analysis

Check actual imports (`grep -rn "import\|require\|from " --include="*.{ts,js,tsx,jsx,py,rb}" -l`; look for A imports B and B imports A). Red flags:

- **Circular dependencies** — break with interfaces or events.
- **God objects** — one module imported by >50% of files; split by responsibility.
- **Hidden coupling** — shared mutable state, globals, implicit ordering.
- **Shotgun surgery** — one feature change touches 5+ unrelated files.

Dependencies flow one way: UI → Application → Domain, with Infrastructure depending inward; Domain depends on nothing. Never Domain → UI or Domain → Infrastructure. Endpoints follow user flows (one per user action, not per table), version only for unavoidable breaking changes, and validate at the boundary.

## Existing Patterns

Probe `src/ app/ lib/`, class/module/interface declarations, and entry-point history (commands in the reference). Follow existing patterns unless there is a documented reason to diverge.

## Non-Goals and Failure Modes (mandatory)

A design that only describes the success path fails at the first unexpected condition.

**Non-goals** are declarative negations in the decision record — what the design does not cover, guarantee (consistency, durability, ordering), replace, or optimize for. "Does not support multi-region writes" is a non-goal; "may eventually support" is a hedge and is not.

**Failure modes**: every component records its behavior for timeouts, partial failures, invalid input, missing context, dependency outage, and resource exhaustion — the design questions and what to record per mode are in the reference. A mode with no answer is a gap to close before proceeding, not an implementation detail. Modes captured now become test cases; discovered late they become rework.

## Decision Record

| Field | Content |
|-------|---------|
| **Context** | Situation and forces at play |
| **Options** | 2–4 distinct approaches (not "do it" vs "don't") |
| **Trade-offs** | Pros and cons per option, with evidence |
| **Decision** | Which option and why |
| **Consequences** | What changes, new constraints, risks accepted |
| **Non-goals** | Bulleted negations |
| **Failure modes** | Mode → expected behavior per component touched |

`TaskList` shows all four design tasks completed before implementation.

## Anti-Patterns

Design before mapping flows; patterns from trends ("microservices because everyone does" — monolith first); premature abstraction (an interface with one implementation is overhead); five layers for a CRUD app; "we might need this later" (YAGNI). Show the requirement a pattern serves or drop it.
