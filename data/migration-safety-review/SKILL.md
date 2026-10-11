---
name: migration-safety-review
description: Review database migrations before they are applied to prevent data loss, downtime, broken deployments, unsafe constraints, rollback failures, and application-code mismatches. Use when Codex needs to inspect schema changes that modify tables, rename/drop columns, change data types, add NOT NULL/UNIQUE/FOREIGN KEY/CHECK/ENUM constraints, add indexes, backfill data, alter relationships, introduce cascade behavior, modify production data, or affect auth, payments, orders, bookings, audit logs, or other business-critical records.
---

# Migration Safety Review

Use this skill as a safety gate before applying database migrations to real or production-like data.

## Core Rule

Do not apply or approve a migration until its data, compatibility, locking, rollback, backup, and application-code risks have been reviewed.

## Workflow

1. Identify migration scope:
   - file name, tables, columns, indexes, constraints, data transformations, models, APIs, frontend behavior, and whether existing data is modified
2. Classify risk level:
   - low, medium, high, or critical
3. Check destructive changes:
   - drops, deletes, truncates, irreversible transforms, unsafe renames, data type truncation, cascade deletes, enum removals
4. Check backward compatibility:
   - old code with new schema, new code with old schema, rolling deploys, background workers, mobile/old clients
5. Check existing data compatibility:
   - nulls, duplicates, orphan records, invalid enum values, type conversion, invalid dates/numbers
6. Check locking and downtime risk.
7. Review constraint safety and index strategy.
8. Check application code alignment:
   - models, validation, services, endpoints, frontend types, jobs, seeds, tests, docs
9. Decide if migration order should be split into staged rollout.
10. Review rollback plan and backup needs.
11. Review staging/dry-run and backfill strategy.
12. Pay extra attention to sensitive or financial data.
13. Produce a migration safety report with final recommendation.

Read `references/migration-review-checklist.md` for risk classification, pre-check queries, safe rollout patterns, and the report template.

## Non-Negotiable Rules

- Do not approve destructive migrations without warning.
- Do not assume existing data is clean.
- Do not add NOT NULL, UNIQUE, or FOREIGN KEY constraints without checking existing data.
- Do not ignore application-code compatibility.
- Do not ignore mobile or old client compatibility when API fields change.
- Do not ignore rollback planning.
- Recommend backup for medium or higher risk migrations.
- Do not run destructive SQL without explicit approval.
- Do not perform large backfills without batching/resume considerations.
- Do not add cascade delete behavior casually.

## Output Contract

When using this skill, provide:

1. Migration summary and risk level.
2. Tables/fields/indexes/constraints/data changes affected.
3. Destructive change check.
4. Backward compatibility and existing data compatibility.
5. Locking, constraint, and index review.
6. Application code alignment review.
7. Rollback, backup, and safe deployment recommendation.
8. Verification checklist and final recommendation.
