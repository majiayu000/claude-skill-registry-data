---
name: tdd
description: "The red → green loop for any stack: seams, what a good test is, and the anti-patterns to refuse. Use when building features test-first or when another skill needs the loop."
---

# TDD

The red → green loop, for whatever test framework the project already uses. Consult before and during the loop, not after.

Read `GLOSSARY.md` (or the older `CONTEXT.md`) if it exists so test names and interface vocabulary match the project's domain language, and respect ADRs in the area you're touching.

Before writing or reviewing tests, read
[`references/testing-best-practices.md`](references/testing-best-practices.md)
and apply its value gate and rejection rules throughout the loop.

**Stack references.** Identify the stack from its manifests (`composer.json`, `package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, `Gemfile`). If a matching file exists below, read it before the first cycle: it maps the seams and rules here onto that stack's test tooling. Otherwise apply the rules through the suite's existing conventions.

- Laravel (`laravel/framework` in `composer.json`): [`references/laravel.md`](references/laravel.md)

## Rules of the loop

- **Red before green.** Write the failing test first, watch it fail for the right reason (a missing route 404s, not a typo'd import), then write only enough code to pass. No speculative features.
- **One slice at a time.** One seam, one test, one minimal implementation per cycle. Each next test responds to what the last cycle taught you: never all tests up front, then all implementation (bulk tests verify *imagined* behavior and go insensitive to real changes).
- **Refactoring is not part of the loop.** It belongs to the review step (`code-review`).

## What a good test is

Tests verify behavior through public interfaces, not implementation details. Code can change entirely; tests shouldn't. A good test reads like a specification (`user cannot view another users invoice` says exactly what rule exists) and survives refactors because it doesn't care about internal structure.

## Seams: where tests go

A **seam** is the public boundary you test at (`codebase-design` holds the full deep-module vocabulary). Test at the chosen seams: the caller (`to-spec` or `implement`) picks them from the ranking below and states the choice rather than asking; test at the highest seam that can observe the behavior, prefer a seam the codebase already has over cutting a new one, and use as few as possible, one is the target. Ask only on a genuine fork the rules rank equally.

Highest first:

1. **Transport boundary**: send the request an outside caller would (HTTP, RPC, GraphQL) through the app's real routing, as an authenticated user where it matters, and assert the response plus the persisted state. Default for anything with an endpoint.
2. **UI component**: the framework's component test harness, when behavior lives in the component itself.
3. **CLI command**: invoke it, assert the exit code plus its side effects.
4. **Background job / event handler**: run its handler, or dispatch it with real execution, asserting side effects.
5. **Domain service / action**: a direct test at its public API, for logic shared by several entry points.
6. **Model / data type**: non-trivial queries, conversions, and derived values only.

## Rules for any stack

- **Database**: reuse the isolation the suite already has (transactions rolled back per test, a database rebuilt per run, a fresh container), don't introduce a second convention. Never point tests at a real environment's database.
- **Test data**: build it through the suite's factories or builders; encode meaningful variants as named states (an "overdue" invoice), not inline attribute soup repeated across tests.
- **Side effects via fakes**: replace queues, mail, notifications, storage, and outbound HTTP with the framework's fakes or a faithful in-memory adapter, then assert the effect (a message queued to this address), not the internal call path. Fake the boundary, never mock your own classes' internals.
- **Time**: freeze or move the clock through the framework's time helpers or an injected clock for anything date-dependent; never sleep.
- **Authorization is behavior**: for every "user can X" test, write the "user cannot X on someone else's record" test, record-level scoping is the most error-prone rule in a multi-tenant app.
- **Fast loops**: run only the focused test, or the impacted set when the runner supports it, each cycle; run the suite in parallel when it supports that. When the runner has a watch mode, run it on the focused test under `Monitor` where available, so each save reports red or green; otherwise rerun the focused test each cycle. A user message to stop the tests ends test commands for the rest of the run: the last focused result stands, and the code change they asked for continues. Tests must be order-independent and not share database state, which the isolation and test-data rules above already guarantee. CI still runs the full suite.
