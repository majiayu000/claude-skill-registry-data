---
name: oncokb-database-review
description: Review changed database access for N+1 queries, SQL injection risks, deterministic pagination ordering, and related data integrity/performance concerns.
---

## Purpose

Use this skill to review database read/write code for correctness, security, and performance before merging.

## When to use this skill

- Use when a change adds or modifies SQL, ORM queries, repository/DAO logic, migrations, or API handlers that hit the database.
- Use during PR review whenever changed code can alter query shape, query count, ordering, or transaction behavior.

## Required checks

1. N+1 query risks
   - Detect loop-driven query patterns where one initial query triggers per-row follow-up queries.
   - Check ORM lazy-loading call sites inside loops or serializers.
   - Recommend batching, eager loading, join-based fetches, or precomputed maps when N+1 is found.
   - Completion criterion: every changed read path is either N+1-safe or has a concrete mitigation recommendation.

2. SQL injection risks
   - Require parameterized queries / prepared statements for all user-influenced input.
   - Flag string interpolation, concatenation, dynamic ORDER BY/WHERE clauses, and raw SQL fragments built from request values.
   - If dynamic SQL is required, require strict allowlists for identifiers and operators.
   - Completion criterion: no untrusted input reaches executable SQL without parameterization or an explicit allowlist.

3. Deterministic pagination ordering
   - For any paging query (`LIMIT/OFFSET`, cursor pagination, window paging), require ordering that includes at least one unique tie-breaker column.
   - Accept sorting by business fields, but require appending `id` or another unique key to guarantee deterministic order.
   - Flag ambiguous ordering where rows with equal sort keys can shift between pages.
   - Completion criterion: every paging query has deterministic ordering via a unique key in `ORDER BY`.

## Additional checks to suggest

- Verify supporting indexes exist for pagination/filter/sort keys used by changed queries.
- Check query select lists for overfetching (avoid `SELECT *` on large tables when only a subset is needed).
- Review transaction scope and isolation expectations (no unnecessary long transactions; writes that must be atomic are wrapped correctly).
- Validate lock behavior and contention risk (`FOR UPDATE`, upsert hot paths, high-contention counters).
- Check read-after-write assumptions against replica lag when read replicas are used.
- Ensure soft-delete, tenant, and authorization predicates are consistently applied where required.
- Confirm bulk updates/deletes include safe predicates and cannot accidentally touch full tables.
- For schema/index changes, check migration safety (backfill strategy, lock impact, rollback path).

## Workflow

1. Identify changed database surfaces.
   - Enumerate modified queries and data-access call sites from the diff.
   - Completion criterion: review set of changed DB interactions is explicit.

2. Run required checks.
   - Evaluate N+1, injection, and pagination determinism for each changed interaction.
   - Completion criterion: each changed interaction has pass/fail notes for all required checks.

3. Run additional checks based on risk.
   - Prioritize checks relevant to the change type (reads, writes, migrations, concurrency-sensitive flows).
   - Completion criterion: high-risk gaps have actionable recommendations.

4. Report findings.
   - Separate blockers from non-blocking improvements.
   - Include file/path references and exact query snippets when possible.
   - Completion criterion: reviewer can act on findings without additional investigation.

## Output format

- `Blockers`: issues that must be fixed before merge.
- `Non-blocking`: recommended follow-ups.
- `Checked`: list of required checks completed.

## Quality bar

- Never mark pagination as safe unless a unique tie-breaker is present in ordering.
- Never mark SQL as safe when untrusted input is concatenated into executable SQL.
- Prefer concrete remediation guidance over generic warnings.
