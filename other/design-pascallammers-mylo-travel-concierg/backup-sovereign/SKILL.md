---
name: backup-sovereign
description: >
  Create encrypted, verifiable backups with proof receipts (BLAKE3 + ROOT.txt)
  and mandatory restore drill. Uses age encryption for modern, simple UX.
  Designed for sovereign EU infrastructure. Use after node-hardening completes.
  Triggers: 'backup node', 'encrypted backup', 'create backup', 'restore drill',
  'generate proof receipts', 'verify backup', 'backup with proof'.
version: 1.0.0
---

# Backup Sovereign

High-risk Tier 1 skill for creating encrypted, verifiable backups. All backups include BLAKE3 proof receipts and require a mandatory restore drill to verify recoverability.

## Quick Start

```bash
# Set required parameters
export BACKUP_SOURCES="$HOME/infrastructure,$HOME/.claude/skills"
export AGE_RECIPIENT_FILE="$HOME/.config/age/recipients.txt"
export AGE_IDENTITY_FILE="$HOME/.config/age/identity.txt"

# Optional: customize
export NODE_NAME="node-a"
export BACKUP_LABEL="daily"

# Run preflight
./scripts/00_preflight.sh

# Plan phases (safe to run, shows what WILL happen)
./scripts/10_backup_plan.sh
./scripts/20_encrypt_plan.sh

# Apply phases (REQUIRES DRY_RUN=0 and confirmation)
export DRY_RUN=0
./scripts/11_backup_apply.sh    # Type confirmation phrase
./scripts/21_encrypt_apply.sh   # Type confirmation phrase

# Generate proof receipts
./scripts/30_generate_proof.sh

# Verify artifacts
./scripts/40_verify_backup.sh

# MANDATORY: Restore drill
./scripts/50_restore_drill.sh   # Type confirmation phrase

# Status and report
./scripts/90_verify.sh
./scripts/99_report.sh
```

## Workflow

### Phase 0: Preflight (00)
Check dependencies: tar, gzip, age, b3sum.
Verify BACKUP_SOURCES paths exist.
Check available disk space.

### Phase 1: Backup (10-11)
**Two-phase operation with DRY_RUN gate.**

Plan phase shows:
- Source paths to archive
- Exclude patterns
- Output directory and run ID
- Estimated archive size

Apply phase executes:
- Creates tar.gz archive
- Generates manifest.json with BLAKE3 hashes
- Records excludes.txt

### Phase 2: Encrypt (20-21)
**Two-phase operation with DRY_RUN gate.**

Plan phase shows:
- Encryption method (age)
- Recipient file location
- Output file path

Apply phase executes:
- Encrypts archive with age
- Creates archive.tar.gz.age

### Phase 3: Proof (30)
Generate cryptographic proof receipts:
- BLAKE3 hash of manifest.json
- BLAKE3 hash of encrypted archive
- ROOT.txt (composite hash for anchoring)
- PROOF.json (metadata receipt)

### Phase 4: Verify (40)
Verify all artifacts exist and ROOT.txt is valid.

### Phase 5: Restore Drill (50) **MANDATORY**
**DRY_RUN gate + CONFIRM_PHRASE**

This phase is required to validate backup recoverability:
- Decrypts archive to temp directory
- Extracts and verifies file count
- Records restore location

### Phase 6: Status + Report (90-99)
Generate JSON status matrix and markdown audit report.

## Inputs

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| BACKUP_SOURCES | Yes | - | Comma-separated paths to backup |
| AGE_RECIPIENT_FILE | Yes | - | File with age public key(s) |
| AGE_IDENTITY_FILE | Yes | - | File with age private key (for restore) |
| NODE_NAME | No | node-a | Node identifier |
| BACKUP_LABEL | No | manual | Label for this backup run |
| BACKUP_EXCLUDES | No | .git,node_modules,target,dist,outputs | Exclude patterns |
| OUTPUT_DIR | No | outputs | Output directory |
| DRY_RUN | No | 1 | Set to 0 to enable apply scripts |
| REQUIRE_CONFIRM | No | 1 | Require confirmation phrase |
| CONFIRM_PHRASE | No | I UNDERSTAND THIS WILL CREATE AND ENCRYPT BACKUPS | Safety phrase |

## Outputs

| File | Description |
|------|-------------|
| `outputs/runs/<run_id>/archive.tar.gz` | Unencrypted archive |
| `outputs/runs/<run_id>/archive.tar.gz.age` | Encrypted archive |
| `outputs/runs/<run_id>/manifest.json` | File list + sizes + BLAKE3 hashes |
| `outputs/runs/<run_id>/ROOT.txt` | BLAKE3 root (for anchoring) |
| `outputs/runs/<run_id>/PROOF.json` | Metadata receipt |
| `outputs/runs/<run_id>/excludes.txt` | Exclude patterns used |
| `outputs/status_matrix.json` | Verification results |
| `outputs/audit_report.md` | Human-readable audit trail |

## Safety Guarantees

1. **DRY_RUN=1 by default** - Apply scripts refuse to run without explicit DRY_RUN=0
2. **CONFIRM_PHRASE required** - Must type exact phrase to proceed
3. **Mandatory restore drill** - Untested backups are not trusted
4. **BLAKE3 hashes** - Cryptographic integrity verification
5. **ROOT.txt for anchoring** - Can be submitted to merkle-forest/rfc3161-anchor
6. **Per-run isolation** - Each backup is immutable once created
7. **All scripts idempotent** - Safe to run multiple times

## age Key Setup

If you don't have age keys yet:

```bash
# Generate identity (private key)
age-keygen -o ~/.config/age/identity.txt

# Extract public key to recipients file
age-keygen -y ~/.config/age/identity.txt > ~/.config/age/recipients.txt
```

## EU Compliance

| Aspect | Value |
|--------|-------|
| Data Residency | EU (Ireland - Dublin) |
| GDPR Applicable | Yes (depends on backup content) |
| Jurisdiction | Irish Law |
| Encryption at Rest | Yes (age) |

## References

- [Recovery Notes](references/recovery_notes.md)

## Next Steps

After completing backup-sovereign:
1. Store encrypted bundle off-node (secondary disk / object store)
2. Test restore on a different machine (recommended)
3. Optionally anchor ROOT.txt with rfc3161-anchor skill
4. Proceed to **disaster-recovery** skill
