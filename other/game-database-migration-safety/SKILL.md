---
name: game-database-migration-safety
description: Use when planning a game MySQL schema or data migration that requires 3306 or 3307 isolation, recognized schema gates, dry-run review, backup, restore, human approval, and zero credential exposure.
version: 0.1.0
author: GameStudio-CodexKIT
license: MIT
compatibility:
  engines: [engine-agnostic]
  versions: [mysql-5.7+, mysql-8.0+]
  platforms: [windows, linux]
metadata:
  studio:
    type: safety
    lifecycle_stage: build
    risk_level: high
    packs: [cpp-lua-mmorpg]
    side_effects: database
    artifact: migration-safety-plan.json
    required_evidence: [schema-version, backup-plan, restore-plan, reviewer-approval]
    owner: HoaTV Studio
    reviewer: Network/Backend
    maturity: beta
    last_reviewed: 2026-08-07
    provenance:
      derived_from: none
      patterns_from: [AGENTS.md database safety, sanitized isolated database snapshot]
      copied_text: none
---
# Game Database Migration Safety

## Overview
Database changes remain plans until the target project, port, schema version, backup, restore, reviewer, and human approval are all verified.

## When to use
Use for MySQL schema migrations, data imports, stored procedure changes, seed changes, port moves, or cross-project database restoration.

## When NOT to use
Do not use to inspect static service topology only, and never apply when schema identity is unknown, backup is missing, restore is untested, or credentials would be exposed.

## Required inputs and context discovery
Require project owner, host, isolated port, database name, observed schema version, expected schema, migration source and hash, backup path, restore command, downtime plan, reviewer, human approval, and validation queries.

## Safety and risk level
This is high-risk. Unknown schema, ambiguous project ownership, unapproved ports, active production targets, missing backup, missing restore, missing reviewer, or missing human approval means `BLOCKED`.

## Workflow
1. Verify project ownership, host, port, database, and schema version using read-only queries.
   Completion criterion: unknown schema or target ambiguity is BLOCKED.
2. Review the migration source, expected before/after schema, affected rows, and idempotency.
   Completion criterion: destructive or irreversible statements are identified before execution.
3. Create backup and restore plans without printing passwords or tokens.
   Completion criterion: backup path, checksum, restore command, and validation query are documented.
4. Run a dry-run or disposable-fixture migration and capture output.
   Completion criterion: apply remains prohibited on the real DB until fixture evidence and reviewer approval exist.
5. Request explicit human approval for the exact target and maintenance window.
   Completion criterion: approval scope matches the reviewed plan.
6. Apply, validate, and restore on failure only through an authorized project-specific runbook.
   Completion criterion: real execution is PASS, FAIL, or BLOCKED with evidence; this kit never assumes it occurred.

## Evidence and output contract
Produce `migration-safety-plan.json` with target identity, port, schema, migration hash, dry-run, backup, restore, reviewer, approval status, validation queries, verdict, and limitations.

## Handoff contract
Record target, schema evidence, migration hash, backup and restore paths, dry-run result, reviewer, approval status, blocked conditions, and next authorized action.

## Pitfalls and anti-rationalization
- Port 3306 is not automatically the intended project database.
- A successful backup command without a validated file is insufficient.
- Unknown schema never becomes “probably compatible.”
- Never log or embed credentials in plans or evidence.

## Verification checklist
- [ ] Project, port, DB, and schema are recognized.
- [ ] Migration source and destructive statements were reviewed.
- [ ] Backup and restore are concrete.
- [ ] Dry-run evidence exists.
- [ ] Reviewer and human approval are explicit before apply.

## References and scripts
Read [references/commands.md](references/commands.md) for credential-safe inspection, backup, and restore patterns. Use the bundled [scripts/db_safety.py](scripts/db_safety.py) for no-write planning. Real DB commands remain project-specific and require explicit approval.
