---
name: dl-code-review
description: Review a Rails change, file, or pull request for concrete correctness, authorization, data integrity, performance, and maintainability defects. Use for focused read-only code review. For an application-wide Rails security or Oracle/MariaDB audit, use the dedicated audit workflow if available. Do not implement fixes unless the user requests them.
---

# Rails code review

Review observable behavior and failure modes. A class size, missing service object, or unfamiliar style is not itself a bug. Keep the review read-only unless the user also requests changes.

## Establish scope and baseline

1. Read project instructions, Ruby/Rails versions, schema, test configuration, and existing authorization conventions. Do not assume Pundit, RSpec, PostgreSQL, or a particular service-object pattern.
2. For a working-tree review, inspect `git status --short`, unstaged and staged diffs. For a branch review, identify the intended base and compare from the merge base. Include untracked files only when part of the requested change.
3. Read full changed methods, their callers, callbacks, views/serializers, and relevant tests. Trace changed data from entry point to persistence or external effects.
4. Separate regressions introduced by the change from pre-existing problems. Review the requested scope first; expand only to establish a concrete impact.

## Review by failure scenario

| Area | Trace | Evidence needed before reporting |
|---|---|---|
| Authorization | actor → scope/policy → record → response | A reachable action permits another tenant's or role's operation; check inherited filters and policy scopes first |
| Writes | validation → transaction → constraints → external effects | A failure or concurrent request leaves invalid state, duplicates, or sends an effect before a rollback |
| Background jobs | enqueue → serialization → execution → retry | A retry duplicates an effect, the record can disappear, or a worker can observe an uncommitted change |
| Queries | relation construction → enumeration → association access | SQL/query count or a trace showing repeated queries; read the actual indexes and adapter before proposing one |
| Migrations | old app/new schema and new app/old schema | Locking, data conversion, incompatible nullability, or deployment ordering that can interrupt the running app |
| Cache | key → tenant/user scope → invalidation | Stale or cross-user values under a named update/request sequence |
| API/UI | input → status/serialization → consumer | A missing/changed field, escaping rule, failure status, or pagination contract breaks an existing caller |

For a possible N+1, inspect whether associations are already loaded. `any?` without a block can use an existence query on an unloaded relation; do not label it as loading every row without verifying the call shape. For uniqueness, inspect the database constraint, including tenant scope and soft-deletion conditions.

Transactions do not roll back HTTP calls. For a job or email, identify the outermost commit boundary and queue-adapter behavior before suggesting `after_commit`, explicit enqueueing, or an outbox. A method-level transaction may be nested inside a caller's transaction.

## Validate hypotheses

- Run existing focused tests and available project tools, for example `bundle exec rubocop --format json`, `bundle exec brakeman -q -f json`, or `bundle exec bundler-audit check` when installed and relevant. Do not auto-correct during a read-only review.
- Record command, exit status, and limitations. Missing tools or stale advisory data mean unverified, not clean. Do not hide failures with shell redirection or `|| true`.
- Prefer a minimal reproduction using fixtures or temporary data. Do not run a migration, deployment, or a destructive production query just to substantiate a finding.
- A scanner warning is a lead: follow the value to a reachable sink, check sanitization/allowlists, and eliminate false positives.
- For performance, name the workload and compare query count, latency, allocations, or memory with the same input. Distinguish measured results from predicted improvement.

## Findings and priority

For each confirmed finding provide:

- **Priority and title:** P0 for an immediate widespread blocker; P1 for a serious failure on a realistic path; P2 for a bounded defect; P3 for a small actionable issue. Severity follows impact and reachability, not category alone.
- **Location:** shortest useful `file:line` reference.
- **Trigger:** actor, input/state, and execution path required.
- **Actual vs expected:** what fails and who is affected.
- **Evidence:** minimal code/SQL/test evidence; distinguish observed and inferred results.
- **Fix direction:** smallest correction consistent with this project, plus the regression scenario to test.

Example: “P1 — Duplicate invoice delivery after retry. `jobs/send_invoice_job.rb:24` sends before recording delivery; failure of the update causes the retry to send again. Use the provider's idempotency key and test a failure after the provider accepts the request.” Do not assert this finding unless those operations actually appear in the reviewed code.

Lead with actionable findings ordered by priority. Follow with remaining uncertainties and checks performed. If none are confirmed, say so and identify the areas not exercised. Keep optional refactors separate from defects; do not inflate the report with praise or generic SOLID checklists.
