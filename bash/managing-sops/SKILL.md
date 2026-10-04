---
name: managing-sops
description: |
  Use when working with Sops — mozilla SOPS encrypted secrets management, key
  rotation, multi-provider encryption, and file-based secret operations. Covers
  encrypting and decrypting files, managing encryption keys (AWS KMS, GCP KMS,
  Azure Key Vault, PGP), auditing encrypted files, and comparing secret
  structures. Use when managing file-based encrypted secrets, rotating
  encryption keys, or auditing encrypted config files with SOPS.
connection_type: sops
preload: false
---

# SOPS Management Skill

Manage and analyze SOPS-encrypted secret files, encryption keys, and configurations.

## Tool Conventions

### Prerequisites
SOPS CLI (`sops`) must be installed. Encryption keys (KMS, PGP, or age) must be configured.

### Core Helper Function

```bash
#!/bin/bash

sops_info() {
    local file="$1"
    sops --output-type json -d "$file" 2>/dev/null
}

sops_metadata() {
    local file="$1"
    # Extract SOPS metadata without decrypting values
    cat "$file" | jq '.sops // empty'
}
```

## Output Rules
- **TOKEN EFFICIENCY**: Extract only needed fields
- Target <=50 lines per script output
- **NEVER** output decrypted secret values -- only output key names and metadata
- Never dump full decrypted files

## Discovery Phase

### Find Encrypted Files

```bash
#!/bin/bash
echo "=== SOPS Encrypted Files ==="
find "${1:-.}" -type f \( -name "*.enc.yaml" -o -name "*.enc.json" -o -name "secrets.yaml" -o -name "*.sops.yaml" \) | while read -r file; do
    if grep -q '"sops"' "$file" 2>/dev/null || grep -q 'sops:' "$file" 2>/dev/null; then
        provider=$(cat "$file" | python3 -c "import sys,json,yaml; d=yaml.safe_load(sys.stdin) if '$file'.endswith('.yaml') else json.load(sys.stdin); s=d.get('sops',{}); print(list(s.get('kms',[{}])[0].keys())[0] if s.get('kms') else s.get('pgp','pgp') if s.get('pgp') else 'age' if s.get('age') else 'unknown')" 2>/dev/null || echo "unknown")
        echo "$file\t$provider"
    fi
done | column -t | head -25

echo ""
echo "=== .sops.yaml Config ==="
if [ -f ".sops.yaml" ]; then
    cat .sops.yaml
else
    echo "No .sops.yaml found in current directory"
fi
```

### List Keys in Encrypted Files

```bash
#!/bin/bash
FILE="${1:?Encrypted file path required}"

echo "=== Secret Keys (names only) ==="
sops -d --output-type json "$FILE" 2>/dev/null | jq -r 'paths(scalars) | join(".")' | head -25

echo ""
echo "=== Encryption Metadata ==="
sops_metadata "$FILE" | jq '{version: .version, lastmodified: .lastmodified, mac: .mac[0:20], providers: ([if .kms then "kms" else empty end, if .gcp_kms then "gcp_kms" else empty end, if .azure_kv then "azure_kv" else empty end, if .pgp then "pgp" else empty end, if .age then "age" else empty end])}'
```

## Analysis Phase

### Key Rotation Status

```bash
#!/bin/bash
echo "=== Encryption Key Age ==="
find "${1:-.}" -type f \( -name "*.enc.*" -o -name "*.sops.*" \) | while read -r file; do
    if grep -q 'sops' "$file" 2>/dev/null; then
        lastmod=$(cat "$file" | jq -r '.sops.lastmodified // empty' 2>/dev/null || grep 'lastmodified:' "$file" | awk '{print $2}')
        echo "$file\t${lastmod:-unknown}"
    fi
done | column -t | head -20

echo ""
echo "=== Files Needing Rotation (>90 days) ==="
THRESHOLD=$(date -v-90d +%Y-%m-%d 2>/dev/null || date -d '90 days ago' +%Y-%m-%d)
echo "Files last modified before ${THRESHOLD} may need key rotation"
```

### Compare Secret Structures

```bash
#!/bin/bash
FILE1="${1:?First file required}"
FILE2="${2:?Second file required}"

echo "=== Keys in $FILE1 only ==="
KEYS1=$(sops -d --output-type json "$FILE1" 2>/dev/null | jq -r 'paths(scalars) | join(".")' | sort)
KEYS2=$(sops -d --output-type json "$FILE2" 2>/dev/null | jq -r 'paths(scalars) | join(".")' | sort)
comm -23 <(echo "$KEYS1") <(echo "$KEYS2")

echo ""
echo "=== Keys in $FILE2 only ==="
comm -13 <(echo "$KEYS1") <(echo "$KEYS2")
```

## Output Format
- Use tab-separated columns with `column -t`
- Limit lists to 15-25 items
- NEVER display decrypted values -- only key names and metadata
- Show summaries before details

## Anti-Hallucination Rules

1. **NEVER assume resource names** — always discover via CLI/API in Phase 1 before referencing in Phase 2.
2. **NEVER fabricate metric names or dimensions** — verify against the service documentation or `--help` output.
3. **NEVER mix CLI commands between service versions** — confirm which version/API you are targeting.
4. **ALWAYS use the discovery → verify → analyze chain** — every resource referenced must have been discovered first.
5. **ALWAYS handle empty results gracefully** — an empty response is valid data, not an error to retry.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |

## Common Pitfalls
- **Never expose values**: Only display secret key names, never decrypted values
- **Multiple providers**: SOPS supports AWS KMS, GCP KMS, Azure Key Vault, PGP, and age simultaneously
- **`.sops.yaml` config**: Creation rules in `.sops.yaml` determine which keys encrypt which file patterns
- **Key rotation**: Use `sops updatekeys` to rotate encryption keys without changing values
- **MAC verification**: SOPS includes a MAC to detect tampering -- never manually edit encrypted files
- **File formats**: Supports YAML, JSON, ENV, INI, and binary files
