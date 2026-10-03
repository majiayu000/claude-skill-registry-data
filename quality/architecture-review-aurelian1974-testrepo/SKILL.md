---
name: architecture-review
description: Severity-ranked review checklist for code changes against the Architecture Profile and module recipes — dependency direction, module boundaries, slice hygiene, domain integrity, CQRS discipline, data safety, security, performance, and test sufficiency — with an exact verdict format. Use for any code review, PR review, "check my changes", plan conformance checks, or before merging architectural work.
user-invocable: false
---
# Architecture Review

## 0. Setup
1. Diff: list changed files; group by module and slice.
2. For each module, read its profile entry and the plan/ADR if referenced.
3. Build + run tests (including architecture tests). Red → BLOCKER, still complete the review.

## 1. Boundaries & dependencies
- [ ] No reference to another module except via its Contracts and only if listed in `consumes` — **BLOCKER**
- [ ] Contracts contain only primitives/SharedKernel types; no domain/EF types — **BLOCKER**
- [ ] Dependency direction respected for the recipe — **BLOCKER**
- [ ] No new public types outside Contracts / `{M}Module` — MAJOR
- [ ] No cross-schema writes or joins in write paths — **BLOCKER**

## 2. Placement & organization
- [ ] Each new file placed per `placement-rules.md` for the module's recipe — MAJOR
- [ ] New slices use business verbs, one use case each — MINOR (MAJOR for generic `Update{Entity}`)
- [ ] No slice depends on another slice's handler/types — MAJOR (BLOCKER in clean-sliced)
- [ ] No new Common/Shared/Helpers dumping grounds; rule of three respected — MAJOR
- [ ] No abstractions, packages or base classes absent from plan/profile — MAJOR

## 3. Domain integrity (domain-model modules)
- [ ] Every business rule in aggregate/domain service; none in handler, endpoint, EF config, SQL — **BLOCKER**
- [ ] No public setters; state changes through intent-named methods — MAJOR
- [ ] One aggregate modified per transaction, or ADR-backed exception — MAJOR
- [ ] Other aggregates referenced by id — MAJOR
- [ ] Expected failures return `Result`/`Error` (if profile says result) — MAJOR

## 4. CQRS discipline
- [ ] Queries never track, load aggregates, or save — MAJOR
- [ ] Commands return id/minimal response — MINOR
- [ ] Read-side authorization/scoping applied in the query — **BLOCKER** if missing on sensitive data

## 5. Data safety (with `sql-server-data-access`)
- [ ] Migrations follow expand/contract; destructive steps separate and approved — **BLOCKER**
- [ ] Rollback or explicit irreversible note — MAJOR
- [ ] Parameterized SQL only; dynamic identifiers whitelisted — **BLOCKER**
- [ ] Types match columns (no implicit conversions), SARGable predicates — MAJOR
- [ ] Concurrency: rowversion/locking strategy for contended writes — MAJOR

## 6. Security & privacy
- [ ] Endpoints have explicit authorization — **BLOCKER**
- [ ] No secrets, connection strings, personal identifiers (CNP, patient data) in code or logs — **BLOCKER**
- [ ] External input validated at the slice boundary; external payloads stopped at the adapter — MAJOR

## 7. Reliability & performance
- [ ] `CancellationToken` propagated; no sync-over-async; no `DateTime.Now` — MAJOR
- [ ] No external calls inside DB transactions; outbox used for cross-module/external effects — MAJOR
- [ ] N+1 patterns, unbounded queries, missing paging — MAJOR with evidence, MINOR otherwise
- [ ] Integration event consumers idempotent — **BLOCKER**

## 8. Tests
- [ ] Tests required by the recipe exist (see `architecture-fitness-tests` §3) — MAJOR
- [ ] Architecture tests updated when profile changed — MAJOR
- [ ] Bugfix has a test that failed before the fix — MAJOR

## 9. Code level (mandatory)
Walk skill `code-quality` for every changed file (tracked and untracked), whole file, every line. Architecture findings do not replace code findings.

## Verdict
`APPROVE` only with zero BLOCKER and zero MAJOR; minors are always listed. Output: reviewer OUT block.
Each finding: `path:line | rule id | problem | concrete fix`. No generic advice.
