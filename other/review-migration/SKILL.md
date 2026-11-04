---
name: review-migration
description: Analyze Mattermost schema migrations against best practices and generate a review report. Pass a migration number/name as argument or omit to auto-detect new migrations.
user-invocable: true
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
---

# Review Migration

Analyze a Mattermost schema migration against best practices and produce a filled-out review report.

## Step 1: Load the rules

1. Fetch the official [Mattermost DB Migration Guide](https://developers.mattermost.com/contribute/more-info/server/schema-migration-guide/). This is the authoritative source for migration rules, lock types, and best practices. Extract all rules, the lock types table, and the batch processing patterns.
2. Read [reference.md](reference.md) for supplementary internal knowledge not covered by the official guide (morph driver behavior, large table sizes, empty-table guidance).

## Step 2: Find the migration files

If `$ARGUMENTS` is provided, use it to locate the migration:

```
server/channels/db/migrations/postgres/$ARGUMENTS*.up.sql
server/channels/db/migrations/postgres/$ARGUMENTS*.down.sql
```

If `$ARGUMENTS` is empty, auto-detect new or modified migrations:

1. Run `git diff --name-only HEAD` and `git diff --name-only --cached` to find staged/unstaged migration files.
2. Run `git diff --name-only main...HEAD` to find migrations added on the current branch.
3. If nothing is found, ask the user which migration to review.

Read both the `.up.sql` and `.down.sql` files. If the down migration is missing, flag it.

## Step 3: Analyze against best practices

Check every SQL statement against the rules from the official guide and reference.md. Pay particular attention to:

- Whether CONCURRENTLY is used (and whether `morph:nontransactional` is present as the first line)
- Whether the migration mixes transactional and nontransactional statements in a single file
- Whether the table is empty/feature-flagged (relaxes some rules — see reference.md)
- Backwards compatibility with the previous ESR

## Step 4: Generate the review report

Output the following markdown template, filling in every section based on your analysis. Use the exact status values shown: ✅, ❌, or N/A.

If the table is empty or feature-flagged, add a context note at the top: `> **Context:** The table is gated by a feature flag and will be empty when this migration runs.`

~~~markdown
# Schema Migration Review: [version] — [description]

## Schema Changes
- [ ] New table(s): ...
- [ ] New column(s): ...
- [ ] New index(es): ...
- [ ] Modified column(s): ...
- [ ] Dropped object(s): ...

## Safety Analysis

| Check | Status | Notes |
|-------|--------|-------|
| No ALTER COLUMN TYPE | ✅/❌/N/A | ... |
| CREATE INDEX uses CONCURRENTLY | ✅/❌/N/A | ... |
| DROP INDEX uses CONCURRENTLY | ✅/❌/N/A | ... |
| No FOREIGN KEY via ALTER TABLE | ✅/❌/N/A | ... |
| No full-table DELETE/UPDATE | ✅/❌/N/A | ... |
| morph:nontransactional where needed | ✅/❌/N/A | ... |
| Down migration exists | ✅/❌ | ... |
| Transactional/nontransactional split correct | ✅/❌/N/A | ... |

## Backwards Compatibility
- Compatible with previous ESR: Yes/No
- Can previous Mattermost version run with new schema: Yes/No — [explain]
- Impact if not compatible: ...

## Table Locks & Impact
- Tables affected: ...
- Lock types acquired: ... (use lock types from the official guide)
- Impact to concurrent operations: ...

## Zero Downtime
- Possible: Yes/No
- Reason: ...

## Large-Dataset Testing Recommendation
- **Recommended: Yes/No**
- Reason: ...
- Tables to seed for testing: ...

## Test Results (fill manually if testing recommended)

| DB | Table Size | Row Count | Duration | Instance |
|----|-----------|-----------|----------|----------|
| PostgreSQL | | | | |

## SQL Queries
```sql
[contents of the .up.sql file]
```
~~~

## Step 5: Save the report

Ask the user if they'd like to save the report to a file. Suggest the path:
```
server/channels/db/migrations/reviews/<migration-name>.md
```
