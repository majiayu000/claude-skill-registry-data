---
name: manage-bap-backup
description: Manage BAP identity backups - list members, export member identities, and view backup details using the bap CLI. Works with encrypted .bep BAP identity files.
allowed-tools: "Bash(bun:*)"
---

# Manage BAP Backup

Manage BAP identity backups using the `bap` CLI.

## When to Use

- List all member identities in a master BAP backup
- Export a specific member identity to separate backup
- View backup metadata and structure
- Extract member keys for specific use cases

## Operations

**List Members**: View all member identities in master backup
**Export Member**: Extract a specific member to separate `.bep` file
**View Details**: Show backup type, identity count, metadata

## Usage

```bash
# List all members in backup
bun run /path/to/skills/manage-bap-backup/scripts/list.ts identity.bep

# Export specific member by index
bun run /path/to/skills/manage-bap-backup/scripts/export-member.ts identity.bep 0

# Export to custom output file
bun run /path/to/skills/manage-bap-backup/scripts/export-member.ts identity.bep 0 member-0.bep
```

## Requirements

- `FLOW_BACKUP_PASSPHRASE` environment variable
- `bap` CLI installed globally

## CLI Reference

```bash
# List members
bap list <backup.bep> --password <pass>

# Export member
bap member <backup.bep> --password <pass> --index <n> --output <output.bep>

# Export all members
bap export <backup.bep> --password <pass>
```
