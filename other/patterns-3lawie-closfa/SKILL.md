---
name: patterns
description: Discover and apply the project's established design patterns before writing any server function, data query, component, or auth-touching code. Use proactively BEFORE scaffolding any new module, service, validator, or endpoint — and whenever the user runs /patterns, asks "which pattern applies", mentions conventions/exemplars, or requests new backend code.
allowed-tools: Read, Grep, Glob, Bash
---

# Design Patterns Reference

Canonical sources: the project's architecture documentation (README, design-patterns docs, and any inline rules). This skill teaches you HOW to find and apply patterns — not what they are today, because the codebase is the living source of truth.

Read `learnings.md` beside this file before starting; append an entry when an exemplar search surprises you (missing exemplar, doc/code disagreement).

## Governing Principle

> **Convention over invention.** Every new piece of code must mirror an established exemplar. If no exemplar exists, propose a pattern explicitly BEFORE writing code — never silently introduce new architecture.

## Procedure

1. **Discover** the project's documented design rules — read the architecture rules in README and any design-patterns documentation. These are the governing constraints.
2. **Locate** the closest existing exemplar file for the kind of code you're writing (service, validator, middleware, component). Use grep to find structurally similar modules.
3. **Scaffold** the new code by mirroring the exemplar's structure — same module boundaries, same naming conventions, same middleware chain, same validation approach.
4. **Constrain** your implementation against the documented rules — validate that every server function has input validation, authorization, and proper error handling before considering the code complete.
5. **Instrument** — run the project's linter and type-checker to verify your code respects the established contracts.

## Pattern Categories to Discover

When joining or working in any project, **discover** these pattern categories by reading existing code:

| Category | What to grep for | Principle |
|---|---|---|
| **Auth boundary** | Middleware files, session handling | Authentication happens once; authorization is explicit per endpoint |
| **Data access layer** | Service/repository files, ORM usage | DB access is encapsulated — routes and components never query directly |
| **Input validation** | Schema files, validation middleware | Every external input is validated at the boundary before use |
| **Error contract** | Result types, error handling patterns | Expected failures return structured results; throws are for unexpected/infrastructure failures only |
| **Authorization checks** | Verifier/guard files, ownership checks | Pure functions that receive context as parameters; ownership verified before writes |
| **Rate limiting** | Middleware, rate-limit configuration | Abuse-prone endpoints carry explicit rate-limit tiers |
| **Runtime constraints** | Config files, deployment docs | Code respects the deployment target's limitations (edge, serverless, etc.) |

## When writing new code

1. **Discover** the closest exemplar file and mirror its structure.
2. **Scaffold** new modules following the project's established module triangle (service / authorization-check / validation-schema).
3. **Constrain**: new components must check the shared primitive library first — compose, don't duplicate.
4. If no existing pattern fits, **state so explicitly** and propose one BEFORE writing code — never silently invent architecture.

## Handoffs

- Architecture-level decisions before patterns → `/system-design`.
- App-flow and data-loading patterns → `/web-design-patterns`.
- Visual layer patterns → `/creative-ui`.
- Validate pattern conformance → `/full-review`.
