---
name: superpowers-sage:migrating
description: >
  WordPress migration to Sage/Acorn — migrate classic theme to Sage,
  incremental migration, 7-phase migration contract, rollback playbook,
  migration hard gates, functions.php to Service Providers, shortcodes to Blade,
  CPT registration to Poet, field groups to ACF Composer,
  safe migration reversible steps, migration output artifacts,
  legacy plugin to Acorn, wp-content to Bedrock structure,
  database migration, content migration
user-invocable: true
argument-hint: "<migration-name> [target-scope]"
---

# Migrating — Safe Destructive Data Operations

Execute data migrations with full safety harness: snapshot, dry-run, gate, apply, verify, confirm idempotency. Never destructive-first.

**Announce at start:** "I'm using the migrating skill for a safe data migration with snapshot/dry-run/gate/apply/verify/idempotency checks."

## When to Use

- `post_content` rewrites (injecting blocks, replacing shortcodes, updating markup)
- `wp_postmeta` cleanup (orphan keys, schema changes, re-computing derived values)
- Term taxonomy fixes (renaming, merging, re-assigning terms)
- Attachment regeneration (thumbnails, metadata, rewriting paths)
- User role migrations
- Bulk option updates with serialized data
- Any operation that could lose data if applied incorrectly

## When NOT to Use

- Developer-only refactors that don't touch DB data — use `/building` or direct edits
- Simple one-shot admin tasks — use `lando wp` directly
- Schema changes at the table level — use Laravel migrations or `acorn-eloquent`
- Long-running pipelines with failure-retry needs — use `acorn-queues` with jobs

## Input

$ARGUMENTS

Resolve to a migration name (used for snapshot filenames and logs) and target scope.

## Hard Gates

- **Never apply without snapshot-before.** If the snapshot step fails, STOP.
- **Never apply without human approval of the dry-run diff.** Autonomous apply is forbidden.
- **Never declare done without snapshot-after verification** proving row counts, field shapes, and spot-check samples match expectations.
- **Never leave the migration without idempotency proof.** Re-running must be a no-op (0 rows changed).

## The 7-Phase Contract

```
┌─────────────────────────────────────────────────────────┐
│  1. SNAPSHOT BEFORE    → /tmp/<migration>-before.xml    │
├─────────────────────────────────────────────────────────┤
│  2. DRY-RUN COMPUTE    → list affected rows + new shape │
├─────────────────────────────────────────────────────────┤
│  3. HUMAN APPROVAL     → show diff, pause, await 'y'    │
├─────────────────────────────────────────────────────────┤
│  4. PREFLIGHT CHECKS   → orphan meta, template validity │
├─────────────────────────────────────────────────────────┤
│  5. APPLY              → loop, log progress, wp_slash() │
├─────────────────────────────────────────────────────────┤
│  6. SNAPSHOT AFTER     → /tmp/<migration>-after.xml     │
│     + VERIFY           → count + shape + spot-check     │
├─────────────────────────────────────────────────────────┤
│  7. IDEMPOTENCY CHECK  → re-run, assert 0 rows changed  │
└─────────────────────────────────────────────────────────┘
```

> Full phase procedures (commands, scripts, validation criteria):
> `skills/migrating/references/phase-detail.md`

> Rollback procedures for all 3 tiers:
> `skills/migrating/references/rollback-playbook.md`

## Rollback (Summary)

If post-verification anything is wrong, use the lowest-impact tier:

- **Tier 1** — `lando wp post list --post_type=revision --post_parent=<ID>` then `lando wp post update <ID> --post_content="$(lando wp post get <REVISION-ID> --field=post_content)"` (single post, revisions enabled)
- **Tier 2** — `lando wp db import /tmp/<migration>-postmeta-before.sql` (table-level)
- **Tier 3** — `lando wp db import /tmp/<migration>-full-before.sql` (nuclear, last resort)

Always have the Tier 3 snapshot before applying.

## Anti-Drift — Don't Do This

| Wrong | Correct |
|---|---|
| Apply first, snapshot after | Snapshot BEFORE apply, always |
| Skip dry-run ("trust me") | Dry-run + diff always — no autonomous apply |
| Approve on silence | Explicit 'y' required; silence is not consent |
| Bulk `$wpdb->update()` without `wp_slash()` | `wp_slash()` for user content |
| One-shot script with no idempotency check | Re-run after apply, assert 0 updates |
| Delete target rows before apply | Never; update in place, rollback via snapshot |
| Skip `_wp_page_template` preflight | Check orphan meta before `wp_update_post` |
| Apply without Tier-3 snapshot | `lando wp db export` full DB before any destructive op |
