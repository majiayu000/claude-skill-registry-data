---
name: project-backup-status
description: Create a timestamped project backup and inspect the repo's current status before making changes. Use when starting work in any project, before risky edits or refactors, when the user asks to back up or safeguard a codebase, or when continuity matters and code tools should read TODO/status docs before acting.
agent:
  display_name: "Project Backup Status"
  short_description: "Back up repos and read status first"
  default_prompt: "Use project-backup-status to inspect repo status, create a timestamped backup, and continue safely."
---

# Project Backup Status

## Overview

Protect the current state of a repo before significant work and make sure decisions are grounded in the project's actual status tracker. Prefer a local `backups/` folder inside the repo and a canonical TODO/status file such as `docs/TODO.md` or `TODO.md`.

## Workflow

## 1. Read Status First

Before making or planning changes, look for the project's source of truth in this order:

- `docs/TODO.md`
- `TODO.md`
- `docs/README.md`
- `docs/INDEX.md`
- `README.md`
- any explicit roadmap or tracker the user points to

If a TODO exists, use it to understand what is complete, incomplete, or intentionally deferred. Update it after meaningful work.

## 2. Create the Backup Folder if Needed

Prefer a repo-local `backups/` folder.

If it does not exist, create it before archiving anything.

## 3. Create a Timestamped Backup

Use a timestamped archive name:

- `<repo-name>-YYYYMMDD-HHMMSS.zip`

Default archive scope:

- include source, docs, config, and project files
- exclude large reproducible or recursive paths unless the user explicitly wants a full mirror

Default exclusions:

- `node_modules`
- `dist`
- `build`
- `.next`
- `coverage`
- `.git`
- `backups`

If the repo is tiny or the user explicitly wants everything, include more. State the assumption after the backup is created.

## 4. Prefer Native Archiving Tools

Use the current environment's native tooling.

Examples:

- PowerShell: `Compress-Archive`
- Unix-like shells: `tar`, `zip`, or equivalent

Use a single command flow where practical and avoid destructive file operations.

## 5. Report the Snapshot Clearly

After the backup completes, report:

- the backup path
- the backup name
- any exclusions or assumptions
- the status source you used

## 6. Keep Status Awareness Through the Task

When continuing work after the backup:

- align next steps with the status tracker
- avoid creating a separate tracker if one already exists
- update the TODO/status file after meaningful progress
- mark only verified work as complete

## 7. Use This as the Default Safety Pattern

When the user gives broad ownership of a repo, or asks for major feature work, refactors, or risky changes, prefer this pattern:

1. inspect status
2. create timestamped backup
3. proceed with implementation
4. update status tracker

## 8. Automated backup script

A bundled automation script is provided at `scripts/backup.ps1` (PowerShell):

```powershell
.\scripts\backup.ps1 -RepoPath ".\" -BackupDir "backups" -Exclude node_modules,dist,build,.next,coverage,.git
```

Options:
- `-RepoPath` — project root (required)
- `-BackupDir` — relative path for backups (default: `backups`)
- `-Exclude` — array of directories to exclude
- `-DryRun` — preview what would be backed up without creating the archive

To use this as a project-local tool, copy it to your project's `.ai_scripts/` directory:

```powershell
cp <skill-path>/project-backup-status/scripts/backup.ps1 .ai_scripts/
.ai_scripts\backup.ps1 -RepoPath "." -BackupDir "backups"
```

## Cross-references

- **self-validate** — Validate backups actually exist and are correct.

- **anti-premature-termination** — Backing up is a prerequisite before risky work.

- **audit-project** — Audit should check backup status as part of project health.

- **project-scripts** — Discover project scripts before backup to ensure all scripts are included in the backup scope.
- **toolchain-fallback** — Backups safeguard state before toolchain detection/install steps.
- **release-changelog** — Backup before starting a release to guard against accidental version bumps or destructive changelog rewrites.
- **skill-loader** — Apply the capped selection policy when deciding which validation or audit guardrails should also be active before and after backup operations.
- **shipping-and-launch** — Backup before launch to safeguard against destructive deployment mistakes.
