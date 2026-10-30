---
name: spark-change-scope
description: Use when a Spark change needs its authoritative owner, affected boundaries, risks, acceptance criteria, and smallest verifiable slice established before implementation or review.
---

# Spark change scope

Establish the change boundary from live repository evidence before recommending edits.

## Procedure

1. Read the nearest `AGENTS.md`, `architecture/packages.json`, the owning specification, package README, and nearby tests.
2. Identify one authoritative owner for every state transition, protocol, policy, and persisted field in scope.
3. Trace callers and consumers far enough to find cross-package, compatibility, public-documentation, and migration effects.
4. Separate required behavior from adjacent cleanup. Choose the smallest slice that can prove the requested outcome.
5. Turn the request into observable acceptance criteria, including failure and compatibility cases.

Do not choose an owner from directory names or prompt prose when an enforced inventory or runtime path contradicts it. Resolve ambiguity from those sources first. If a new state owner or unresolved product choice requires an architecture decision, report the specific decision and continue independent scoped work.

Return `owner`, `surfaces`, `invariants`, `risks`, `acceptanceCriteria`, `outOfScope`, and `blockers`, citing paths and symbols.
