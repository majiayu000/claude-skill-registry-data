---
name: database-backups
description: "Use when taking a database backup, validating a dump, or planning recovery before a migration; not for deleting data."
capability: "Use when taking a database backup, validating a dump, or planning recovery before a migration"
side_effect_level: local_write
approval_required: false
requires_tools: "Project-documented tools; see body."
output_schema: "Evidence, changes and verification report."
risk_class: medium
---

# database backups

Determine the engine/version, database identity, configured backup tool, allowed destination and retention policy. Keep credentials in environment or the engine's protected credential mechanism.
Prefer an existing verified project runner. Select a format with the required schema/data/large-object coverage and inspect exit status, size and digest. For PostgreSQL custom-format dumps, list the archive with the matching pg_restore; listing alone does not prove restorability.
Prove recovery in an isolated disposable database when the task requires a verified backup. Never restore over the source or production database as a test. Record source identity, versions, timestamp, digest, restore result and omitted content in a private receipt.
Preserve existing backups and report incomplete coverage. Do not delete backup generations or expose connection strings in reports.


Resolve helper paths from this skill directory. Run project commands from the target workspace.
