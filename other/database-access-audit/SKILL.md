---
name: database-access-audit
description: Read-only database access audit for batch operations, looped DB I/O, bulk writes, relation attach/detach, N+1, transactions, scope isolation, rowcount, concurrency, constraints, and indexes across any stack.
---

# Database Access Audit

Audit repository database-access behavior without assuming a language, framework, ORM, driver, migration tool, or database engine. Balance correctness, security, data isolation, performance, operational safety, and maintainability.

Default to a static, read-only audit. Requests to check, audit, review, find, evaluate, inspect, or assess do not authorize business-code changes, staging, commits, or publication. Enter fix mode only when the user explicitly asks to fix, patch, edit, refactor, or implement.

## Navigation

Load only the reference needed for the current phase:

| Need | Read |
| --- | --- |
| Concrete pattern searches, behavior distinctions, batch/relation/N+1/transaction/raw-SQL checks, or operation-shape decision rules | [Audit pattern catalog](references/audit-pattern-catalog.md) |
| Five-minute triage, evidence collection checklist, report templates, compactness rules, tone, or maintainer questions | [Triage and reporting guide](quick-reference.md) |

Read the pattern catalog before reporting any finding whose exact operation shape or semantic tradeoff is material. Read the reporting guide before producing the final audit report. Do not load detailed catalogs merely to orient to a narrow known path.

## Scope And Inputs

Establish or infer from repository evidence:

- requested scope: repository, service, domain, layer, endpoint, job, migration, model, schema, or tests;
- execution mode, read-only unless fixes were explicitly authorized;
- user-specified and repository-confirmed ORM, database, driver, framework, runtime, migration tool, and deployment target;
- documented or observed batch bounds and whether input is user-controlled;
- exposure and frequency: public/hot, internal, admin-only, job-only, migration-only, or test-only;
- atomicity and retry contract: all-or-nothing, best-effort, partial success, retryable, idempotent, or unknown;
- response behavior for missing, forbidden, invalid-state, duplicate, already-deleted, failed, or skipped IDs;
- tenant, project, organization, account, owner, user, permission, soft-delete, status, and lifecycle scopes;
- reliance on hooks, validators, setters, cascades, defaults, triggers, identity maps, events, caches, indexes, counters, notifications, webhooks, or downstream sync;
- available SQL logs, query-count tests, explain plans, benchmarks, traces, slow-query evidence, and migration/index checks.

Record unconfirmed inputs as unknown and lower priority or confidence accordingly.

Keep main findings inside the requested scope. Inspect shared persistence infrastructure, models, migrations, tests, and config when needed, and list those files as evidence. Report a severe out-of-scope P0 separately as an **Out-of-scope but high-risk note**; do not mix it into main findings. A whole-repository request removes this scope restriction.

## Required Workflow

1. Confirm scope and read-only or fix-authorized mode.
2. Inspect dependency, lock, runtime, deployment, migration, schema, persistence, test, and documentation evidence to infer the actual stack. Verify, but do not silently replace, a user-specified stack.
3. Identify project-specific database primitives: session/connection/unit-of-work providers, repositories/DAOs/gateways, query and command helpers, transaction/retry/locking helpers, models, migrations, constraints, fixtures, and query-logging hooks.
4. Trace real caller-to-database paths using those primitives before using broad generic searches. Distinguish in-memory construction from database execution.
5. Read the [audit pattern catalog](references/audit-pattern-catalog.md) for the relevant surfaces and inspect batch APIs, repositories, services, endpoints, jobs, serializers/mappers, persistence helpers, transactions, scope predicates, rowcount handling, side effects, constraints, and indexes.
6. For every candidate, record its location, scope status, current operation shape, estimated complexity, evidence strength, empty-batch behavior, rowcount semantics, side-effect boundary, risk, fix direction, maintainability tradeoff, validation need, priority, and confidence when applicable.
7. Run the disproof pass below through an evidence path different from the one that generated the candidate.
8. Reject invalid candidates; downgrade behavior that depends on unconfirmed scale, runtime semantics, or business contract; preserve uncertainty explicitly.
9. Group repeated survivors so recurrence does not hide the highest-risk issues. Keep useful rejected candidates as non-issues to prevent repeated false positives.
10. Read the [triage and reporting guide](quick-reference.md), then deliver a read-only report unless fixes were explicitly requested.
11. If fixes are requested, apply the fix-mode guardrails before modifying code.

## Evidence Hierarchy

Prefer evidence in this order when sources conflict:

1. Actual code paths and call relationships.
2. Dependency manifests, lock files, runtime/build/deployment config.
3. Migrations, schemas, indexes, and constraints.
4. Tests, fixtures, factories, and integration setup.
5. SQL logs, query-count results, explain plans, benchmarks, traces, and metrics.
6. Documentation, ADRs, runbooks, and nearby comments.
7. Naming and inference.

Do not make a high-confidence finding from names or comments alone. Do not assert ORM, query-builder, driver, client, unit-of-work, lazy-loading, flush, batching, or rowcount behavior without versioned documentation, repository configuration, tests, SQL logs, or runtime evidence. Mark unverified behavior inferred, possible, or unknown and name the evidence needed.

## Core Audit Semantics

- A loop is not itself a defect. Report looped database I/O only when an iteration performs or triggers a query, write, repository/driver execution, lazy load, flush, commit, or round trip.
- Object-level mutation does not prove one statement, round trip, transaction, or connection per object. Verify unit-of-work, flush, driver, and database behavior.
- Prefer a set-based operation for same-value multi-row changes when object-level semantics and side effects are not required. For different per-row values, evaluate framework bulk APIs or parameterized multi-set execution before complex dialect-specific SQL.
- Do not assume bulk update/delete is safer. It may bypass hooks, validators, cascades, identity-map synchronization, defaults, triggers, audit/outbox events, cache invalidation, search indexing, counters, notifications, webhooks, permission caches, lifecycle behavior, or downstream sync.
- Put applicable tenant, project, organization, owner, user, permission, soft-delete, and current-status scope in the database write, not only in payload prechecks or application memory.
- For all-or-nothing behavior, deduplicate input and verify affected or returned rows against the expected set. Distinguish missing, forbidden, duplicate, already-deleted, and invalid-state rows when the contract requires it.
- Do not assume `rowcount` means matched, changed, or reliable rows across stacks. Verify the current driver/database semantics; use returned IDs/rows or another safe mechanism when required.
- Relation attach/detach must account for duplicate payload IDs, database-backed uniqueness, conflict/upsert behavior, concurrent inserts, and restoration of soft-deleted relations.
- Do not share a session, connection, transaction, or unit-of-work across concurrent tasks unless the current stack explicitly supports it.
- Treat an empty batch as a safe no-op unless the established contract says otherwise. Verify generated predicates and guards; never assume an empty list is safe or unsafe across stacks.
- Raw SQL is not inherently unsafe. Judge value binding, identifier allowlists, scope, rowcount/partial-success semantics, tests, and maintainability. User-controlled SQL injection or cross-scope access is P0.
- Evaluate large batches for parameter limits, lock scope, index support, chunking, timeout, retry, deadlock, rollback cost, and operational scheduling.
- Recommend the simplest safe operation shape. Do not force dialect-specific single-statement SQL without scale, hot-path, or measured evidence and explicit acceptance of dialect coupling.

## Finding Disproof Pass

Treat every finding as a hypothesis. For each candidate:

1. Search code, callers, tests, migrations, constraints, config, docs, logs, and intentional-debt notes for counter-evidence.
2. Re-check through a different path such as caller tracing, schema evidence, test behavior, configuration, or runtime output.
3. Verify whether bounds, early returns, deduplication, existing bulk APIs, database constraints, indexes, object semantics, side effects, generated predicates, or stack batching invalidate the risk.
4. Use `survived` only when evidence still supports the risk; use `downgraded` when a concern remains with lower priority or confidence; use `rejected` when evidence invalidates it.
5. State what would prove or disprove any remaining uncertainty.

Specifically, do not confirm N+1 without showing implicit relationship/deferred-field/serialization I/O or runtime repeated queries; do not condemn raw SQL without testing its safety properties; do not prefer a bulk rewrite until side effects are preserved; and do not escalate missing rowcount without establishing atomicity, idempotency, and driver semantics.

## Priority Model

Use priority for risk and urgency, not stylistic preference:

- **P0 — must fix:** demonstrated correctness, security, cross-scope/data-integrity, severe atomicity, unsafe concurrent-session, unguarded broad-write, destructive lifecycle, or SQL-injection risk.
- **P1 — should fix:** clear meaningful or unbounded scalability, performance, or operational risk such as confirmed looped I/O, meaningful same-value per-object writes without required semantics, relation row-at-a-time writes, confirmed/highly likely N+1, unnecessary mass object loading, missing scale-critical indexes, or uncontrolled high-volume input.
- **P2 — conditional:** the right choice depends on batch size, frequency, runtime behavior, object semantics, maintainability, portability, or unclear low-risk rowcount behavior.
- **P3 — observability and hardening:** missing query-count/SQL-log/explain/benchmark evidence, low-risk bounds documentation, or edge-case tests.

Correctness, security, isolation, and integrity outrank performance. A priority and confidence must reflect scope, exposure, batch size, evidence strength, runtime certainty, business contract, and counter-evidence.

## Validation Safety

- Keep the default audit static and read-only.
- Do not connect to production databases or run migrations, destructive commands, write/data-repair scripts, backfills, broad benchmarks, or load tests without explicit authorization.
- Prefer repository inspection, local tests, dry-run paths, existing logs, test databases, fixtures, and already captured query-count evidence.
- Before any potentially risky execution, state what would run, against which environment, and why.
- Keep EXPLAIN, query-count, and benchmark work safe and scoped; avoid production scans, locks, or mutation.
- When unsure whether a command touches live data, do not run it. Ask for confirmation or propose safe validation.

## Fix-Mode Guardrails

When fixes are explicitly requested:

- Plan phased work first unless the fix is small and unambiguous.
- Address P0 correctness, security, isolation, and integrity before performance-only P1/P2 work.
- Prefer the simplest safe set-based or framework bulk operation and avoid broad DAL/repository rewrites.
- Preserve scope, rowcount semantics, transaction boundaries, hooks, events, caches, indexes, counters, side effects, and object-level business behavior.
- State the intended operation-shape change for each fix.
- Add or recommend applicable tests for empty batches, duplicate/missing/forbidden IDs, partial success, atomicity, concurrent relation attach, and query count.

## Output Contract

The final audit must include:

- scope and mode;
- user-specified and inferred stack with unknowns called out;
- files, modules, endpoints, jobs, migrations, schemas, tests, configs, and evidence inspected;
- overall conclusion and high-priority count;
- prioritized evidence-backed findings with concrete locations, operation shape, evidence strength, disproof/counter-evidence, survival status, risk, recommendation, tradeoff, validation need, and confidence;
- empty-batch and rowcount semantics for batch update, delete, restore, purge, or archive findings;
- recommended fix order;
- useful non-issues or intentionally retained object-level patterns;
- open questions blocking stronger conclusions;
- sampling boundaries when the audit is not exhaustive;
- a clear statement that no business code changed, unless fixes were explicitly authorized and made.

Use the exact presentation and compactness rules in the [triage and reporting guide](quick-reference.md).

## Failure Behavior

If project-specific persistence primitives, stack versions, business semantics, or safe runtime evidence cannot be confirmed, do not invent them. Continue with bounded static evidence, lower confidence, list unknowns and validation needs, and omit claims that cannot survive the disproof pass. If safe evidence is insufficient for any finding, report that no evidence-backed finding survived rather than manufacturing one.
