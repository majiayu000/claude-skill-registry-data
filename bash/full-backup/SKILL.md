---
name: full-backup
description: Creates a complete backup of the project files to the parent directory.
---

# Full Backup Skill

This skill creates a complete backup of your current project workspace.

## Capabilities

- **Full Filesystem Backup**: Copies all files from the current project to a timestamped folder in the parent directory.
- **Smart Exclusions**: Automatically excludes `node_modules` and `.git` to save space and time.

## Usage

Run the backup script (optionally add a description):

```bash
node .agent/skills/full-backup/scripts/backup.js "my_backup_description"
```

## Examples

**Standard Backup:**
```bash
node .agent/skills/full-backup/scripts/backup.js
# Creates: backup_full_2023-10-27T10-00-00
```

**Backup with Note:**
```bash
node .agent/skills/full-backup/scripts/backup.js "added_payment_gateway"
# Creates: backup_full_2023-10-27T10-00-00_added_payment_gateway
```

## Restore

To restore a backup created with this skill, use the `restore-backup` skill.
