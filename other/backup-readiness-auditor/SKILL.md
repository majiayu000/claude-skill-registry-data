---
name: backup-readiness-auditor
description: Evaluate supplied backup manifests and verification evidence before a migration or recovery decision. Identify incomplete coverage, stale checks, failed integrity checks, and unresolved recovery tests without collecting files, running backups, restoring data, or authorizing destructive maintenance.
---

# Backup Readiness Auditor

Separate a prepared backup procedure from evidence that the selected data can be recovered.

## Workflow

1. Ask for the intended scope, evidence cutoff, and an approved metadata-only evidence pack. Do not search personal drives or application profiles to fill gaps.
2. Read [the evidence contract](references/evidence-contract.md). Map each required dataset to its own verification evidence. Keep unknowns explicit; a missing row is not an exclusion.
3. Use the standard-library helper when the pack follows version 1:

       python scripts/audit_backup.py --input evidence.json --as-of 2026-10-14T12:00:00Z --json

   It reads only that JSON file and writes to stdout. Redirect output only to a user-approved private location. It does not inspect source/destination folders, fetch cloud files, or verify the claims independently.
4. Investigate gaps with the user. File counts, matching sizes, a healthy disk, a successful copy command, or an encrypted archive alone do not establish recoverability. Distinguish hash verification, stable snapshot evidence, coverage, and an isolated restore test.
5. Return the evidence verdict, reasons, required follow-up checks, and evidence cutoff. Use [the report template](assets/readiness-report-template.md) for a fuller handoff.

## Decisions and boundaries

- `BLOCKED`: supplied evidence reports a failed check or missing required dataset.
- `REVIEW`: no known failure, but evidence is incomplete, stale, future-dated, or untested.
- `EVIDENCE_COMPLETE`: the supplied pack satisfies these checks. This is not independent certification of a backup and never permission to format, delete, or retire an original.
- Do not infer credential portability, cloud synchronization, encryption, or application consistency from filenames or installation state.
- Do not open browser profiles, account exports, access files, databases, or configuration contents. Do not copy, decrypt, restore, mount, schedule, install, or change permissions.
- Keep real evidence packs and reports private. Public tests use fictional dataset IDs and synthetic counts, never actual inventories, account information, volume identifiers, or machine paths.

For software reinstall choices, use a separate inventory workflow. This skill evaluates backup evidence, not installed applications.
