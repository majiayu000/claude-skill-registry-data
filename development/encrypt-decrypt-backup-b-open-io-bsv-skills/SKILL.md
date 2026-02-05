---
name: encrypt-decrypt-backup
description: Encrypt and decrypt BSV backup files (.bep format) using the bitcoin-backup CLI. Supports all backup types (BAP identity, wallet, ordinals, vault). Uses Flow's FLOW_BACKUP_PASSPHRASE and stores files in /.flow/.bsv/ following Flow's BSV convention.
allowed-tools: "Bash(bun:*)"
---

# Encrypt/Decrypt Backup

Encrypt and decrypt BSV backup files using the bitcoin-backup CLI (`bbackup`).

## When to Use

- Encrypt wallet JSON to secure `.bep` backup file
- Decrypt `.bep` backup to read wallet data
- Create BAP identity backups
- Secure ordinals keys and payment keys
- Store sensitive BSV data encrypted at rest

## Supported Backup Types

All backups use `.bep` format (AES-256-GCM encryption):

- **BapMasterBackup** - BAP identity (Type42 or Legacy)
- **BapMemberBackup** - Individual BAP member
- **WifBackup** - Single private key
- **OneSatBackup** - Ordinals + Payment + Identity keys
- **VaultBackup** - Encrypted vault
- **YoursWalletBackup** - Yours Wallet format
- **YoursWalletZipBackup** - Yours Wallet ZIP format

## Usage

Run the encrypt or decrypt scripts:

```bash
# Encrypt a wallet JSON file
bun run /path/to/skills/encrypt-decrypt-backup/scripts/encrypt.ts wallet.json output.bep

# Decrypt a backup file
bun run /path/to/skills/encrypt-decrypt-backup/scripts/decrypt.ts backup.bep

# Decrypt to specific output file
bun run /path/to/skills/encrypt-decrypt-backup/scripts/decrypt.ts backup.bep wallet.json
```

## Flow's BSV Convention

This skill follows Flow's BSV backup convention:

**Storage Location**: `/.flow/.bsv/`
- `backups/` - Encrypted .bep files
- `temp/` - Temporary decrypted files (auto-cleanup)
- `config.json` - Backup registry

**Security**:
- Uses `FLOW_BACKUP_PASSPHRASE` environment variable
- Never hardcodes passwords
- Auto-cleanup of temp files after operations
- 600k PBKDF2 iterations for strong encryption

## Requirements

- `FLOW_BACKUP_PASSPHRASE` environment variable must be set
- `bbackup` CLI installed globally: `bun add -g bitcoin-backup`

## CLI Reference

The bitcoin-backup CLI provides three commands:

- `bbackup enc <input> -p <password> -o <output>` - Encrypt JSON to .bep
- `bbackup dec <input> -p <password> -o <output>` - Decrypt .bep to JSON
- `bbackup upg <input> -p <password> -o <output>` - Upgrade legacy backups

## Error Handling

- Password too short (min 8 chars) - Returns error
- Invalid backup structure - Validation error
- Wrong password - Decryption fails with error
- Auto-detects backup type and iteration count
