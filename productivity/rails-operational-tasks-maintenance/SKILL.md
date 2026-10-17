---
name: rails-operational-tasks-maintenance
description: Design and review Rails operational commands, custom Rake tasks, Rails runner jobs, maintenance workflows, cleanup operations, data repair tasks, and one-off production-safe automation.
license: MIT
---
# Rails Operational Tasks and Maintenance

## Purpose
Use this skill when Rails code introduces, modifies, reviews, or executes operational commands such as custom Rake tasks, bin/rails runner workflows, maintenance scripts, cleanup jobs, reconciliation tasks, data repair utilities, cache maintenance, backfills, or administrative commands.

## Activate when
Activate for custom Rake tasks, bin/rails runner, operational scripts, maintenance commands, data repair, reconciliation, cleanup, purge workflows, cache maintenance, recurring administrative tasks, backfills, production one-offs, dry-run tooling, task locks, progress reporting, or operational runbooks.

## Core contract
An operational task is production code with an operational interface. Give it explicit scope, preconditions, side-effect semantics, idempotency behavior, concurrency policy, observability, failure handling, and rollback or recovery guidance. Prefer a task or runner workflow that can be inspected, tested, and rerun safely over ad hoc console commands.

## Repository inspection
Resolve Ruby and Rails versions. Inspect Rakefile, lib/tasks, existing task namespaces, bin/rails runner usage, scheduled jobs, maintenance scripts, service objects, command conventions, database safety rules, deployment environment variables, logging, lock mechanisms, and runbooks. Check whether an operation already exists and whether an existing service can be reused.

## Task ownership and naming
Namespace tasks by bounded responsibility. Use names that reveal scope and mutation semantics, such as maintenance:reconcile or data:backfill_users. Keep task orchestration thin; business rules belong in reusable Ruby objects or services when they deserve independent testing.

## Preconditions and environment gates
Production maintenance must establish explicit preconditions. Gate destructive or production-only tasks by environment, required configuration, operator intent, or a dry-run confirmation mechanism. Never rely on a task name alone to prevent accidental execution against the wrong database.

## Idempotency and resumability
Design rerunnable operations. Process stable batches, record progress or durable checkpoints where useful, make repeats safe, and distinguish already-completed work from new work. Avoid a task that must finish in one uninterrupted invocation when the workload can be large or interrupted.

## Transactions and batch boundaries
Use transaction scope deliberately. Keep large maintenance operations out of one unbounded transaction when that creates lock, memory, or rollback risk. Combine bounded batches with database constraints and explicit progress semantics.

## Concurrency and locking
Maintenance tasks can race with application writes or with another operator. Choose one or more of application-level coordination, database locking, advisory locks, leases, or uniqueness constraints. Make ownership, timeout, and stale-lock recovery explicit.

## Mutation safety
Prefer explicit writes with clear invariants. Review callbacks, validations, authorization bypasses, touch behavior, counter caches, timestamps, audit events, and downstream jobs before using bulk SQL or update_all-style operations. A maintenance task must preserve the invariants it intentionally bypasses.

## Dry run and operator feedback
For destructive or high-volume tasks, support dry-run or preview behavior where practical. Report scope, counts, progress, skipped records, failures, and final totals without printing secrets or sensitive payloads.

## Failure handling and recovery
Handle partial failure intentionally. Decide whether to fail fast, continue and collect failures, retry selected records, or create a reconciliation report. Make rerun behavior safe and document any manual recovery steps.

## Scheduling and recurring operations
Scheduled maintenance must tolerate duplicate delivery, delayed execution, overlap, and deployment restarts. The task itself should enforce idempotency and concurrency rules rather than assuming the scheduler is perfectly reliable.

## Data repair and backfills
For data repair or backfills, define the source-of-truth rule, selection predicate, transformation, validation, batching, checkpointing, verification query, and rollback/reconciliation plan. Coordinate with database migration and release sequencing when schema changes are involved.

## Cache and filesystem maintenance
Cleanup tasks for cache, tmp, uploads, or generated artifacts must understand ownership, age or retention rules, active references, and concurrent writers. Prefer framework-supported maintenance commands when they match the required semantics.

## Testing strategy
Test operational workflows as executable contracts. Cover environment gates, dry-run behavior, idempotency, batch boundaries, lock behavior, partial failure, logging, final summaries, and representative data. Avoid tests that depend on production credentials or production-only state.

## Anti-patterns / failure modes
Avoid giant Rake tasks containing all business logic, environment checks based only on human convention, one-shot non-resumable production scripts, unbounded transactions, silent destructive operations, broad rescue that hides failures, task overlap without coordination, unbounded logging, direct production console instructions as the only recovery mechanism, and maintenance code with no verification query or success criteria.

## Reference example

An operational task that is idempotent, dry-runnable, and bounded: safe to re-run, safe to stop.

```ruby
# lib/tasks/backfill.rake
namespace :backfill do
  desc "Backfill invoices.currency; DRY_RUN=1 to preview"
  task invoice_currency: :environment do
    dry_run = ENV["DRY_RUN"].present?
    batch_size = ENV.fetch("BATCH", "1_000").to_i

    Invoice.where(currency: nil).find_each(batch_size: batch_size) do |invoice|
      currency = invoice.customer&.currency || "usd"
      say "#{invoice.id} -> #{currency}"
      invoice.update_column(:currency, currency) unless dry_run # no callbacks by design
    end
  end

  def say(line)
    puts line
    $stdout.flush
  end
end

# bin/rails backfill:invoice_currency DRY_RUN=1 | head
# Re-runs converge: the where(currency: nil) guard makes completion idempotent.
```

## Agent review checklist
- [ ] task or command ownership is explicit
- [ ] production/environment gates are explicit
- [ ] scope and selection predicate are inspectable
- [ ] idempotency is proven
- [ ] batching/checkpointing is appropriate
- [ ] concurrency/locking is explicit
- [ ] mutations preserve required invariants
- [ ] dry-run or preview exists when warranted
- [ ] partial failure policy is explicit
- [ ] progress and result reporting are observable
- [ ] verification query or success criterion exists
- [ ] rerun/recovery behavior is documented

## Verification
Resolve versions -> inspect existing commands and reusable services -> define task scope and ownership -> define gates and safety checks -> define idempotency/batching/locking -> implement thin orchestration -> test representative and failure paths -> execute repository validation -> document runbook and verification evidence.

## Source foundation
- https://guides.rubyonrails.org/command_line.html
- https://guides.rubyonrails.org/active_record_migrations.html
- https://guides.rubyonrails.org/active_job_basics.html
- https://guides.rubyonrails.org/maintenance.html

## Rails operational task/maintenance changes

For custom Rake tasks, runner commands, maintenance, cleanup, backfill, repair, or reconciliation work:
- resolve Ruby/Rails versions and inspect existing task namespaces and operational conventions;
- classify the task's scope, owner, environment, mutability, workload size, and recovery requirements;
- keep task orchestration thin and reuse tested services/domain objects where business logic deserves a boundary;
- gate destructive or production-sensitive commands explicitly before side effects;
- make repeated execution converge safely; for large operations use deterministic batching and checkpoint/resume semantics;
- define transaction boundaries deliberately and avoid unbounded transactions for large maintenance workloads;
- choose an explicit concurrency/locking mechanism when overlap is unsafe;
- audit callbacks, validations, authorization, counters, timestamps, audit events, and downstream jobs before bulk writes;
- provide dry-run/preview behavior for destructive or high-blast-radius tasks when practical;
- define fail-fast, collect-and-report, selective retry, or reconciliation behavior for partial failures;
- emit bounded progress and final result evidence without logging secrets or sensitive payloads;
- design recurring tasks for duplicate, delayed, overlapping, and restarted execution;
- require a verification query/postcondition and document recovery or rerun behavior;
- test environment gates, idempotency, batching, lock contention, partial failures, and dry-run behavior;
- do not treat successful process exit as proof that the data repair or maintenance objective was achieved.
