---
name: validate-secrets
description: Validate SOPS encryption on secret files before committing. Use when staging secrets, committing encrypted files, or checking if secrets are properly encrypted. Prevents committing unencrypted secrets.
allowed-tools: Bash Read Grep Glob
---

# Validate Secrets

Ensure secret files are properly SOPS-encrypted before commit.

For SOPS configuration and encryption details, see [reference.md](reference.md).

## Instructions

1. Identify files matching secret patterns in staged/modified files
2. Check if files are SOPS-encrypted (look for `sops:` metadata)
3. Report any unencrypted secrets that should be encrypted
4. Block commit recommendation if unencrypted secrets found
5. **DO NOT automatically run `sops --encrypt` or `sops --decrypt` commands** - inform the user to run these manually

## Secret File Patterns

Files that MUST be encrypted:

| Pattern | Description |
|---------|-------------|
| `*.sops.yaml` | SOPS encrypted files |
| `*sopssecret*.yaml` | SopsSecret CRDs |
| `*/secrets/*.yaml` | Files in secrets directories |
| `*secret*.yaml` | Files with "secret" in name |

## Validation Check

A file is SOPS-encrypted if it contains:
```yaml
sops:
    kms: []
    age:
        - recipient: age1...
```

Or for SopsSecret CRDs:
```yaml
kind: SopsSecret
spec:
    secretTemplates:
        ...
sops:
    ...
```

## Output

**Safe to commit:**
- List encrypted files that passed validation

**BLOCKED - Unencrypted secrets found:**
- List files that match secret patterns but lack SOPS encryption
- Inform user to manually encrypt: `sops --encrypt --in-place <file>`
- **DO NOT run the encryption command automatically**

## Integration

This skill is called by `commit-workflow` before staging secret files.
