---
name: analyzing-ransomware-encryption-behavior
description: 'Analyzes how a ransomware sample encrypts files: identifying the crypto scheme
  (symmetric/asymmetric/hybrid), key handling, file targeting and extension/marker changes,
  shadow-copy deletion, and ransom-note artifacts. Activates for requests to analyze
  ransomware encryption, assess decryptability, or study ransomware behavior.'
domain: cybersecurity
subdomain: malware-analysis
tags:
  - malware
  - ransomware
  - cryptography
  - encryption
  - file-marker
  - impact
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1486
  - T1490
  - T1083
  - T1027
d3fend:
  - D3-FA
  - D3-DA
references:
  - 'No More Ransom project — https://www.nomoreransom.org/'
  - 'NIST cryptographic standards (AES/RSA) — https://csrc.nist.gov/'
---

# Analyzing Ransomware Encryption Behavior

## When to Use

- You need to understand how a ransomware sample encrypts data and whether recovery without
  the key is feasible.
- You are documenting file targeting, markers, and the ransom workflow for an IR report.
- You want to identify the crypto primitives to assess decryptability and detection points.

**Do not use** this to attempt key recovery on production data without backups; analyze in the
lab on disposable test files only.

## Prerequisites

- Isolated lab with disposable test files of varied types/sizes.
- Static/RE tools (see the Ghidra and crypto-identification skills) and the dynamic-analysis
  setup.
- A clean snapshot to revert.

## Safety & Handling

- Detonate only against **throwaway** files in the isolated victim VM; never real data.
- Treat the sample and any dropped components as live; revert after each run.

## Workflow

### Step 1: Identify the crypto scheme statically

Locate crypto constants and APIs to classify the scheme:

```text
Symmetric only (AES/ChaCha/RC4)  -> key may be derivable/recoverable if mishandled
Asymmetric (RSA/ECC) wrapping    -> per-file symmetric key wrapped with attacker pubkey
Hybrid (typical)                 -> AES per file, RSA-wrapped key in the encrypted file/footer
```

Look for AES S-boxes, ChaCha constants ("expand 32-byte k"), and `CryptImportKey`/`BCrypt*`.

### Step 2: Trace key generation and handling

Determine where the symmetric key comes from (CSPRNG vs weak source), whether it is stored,
and how it is protected. Weak/reused keys or keys left in memory are recovery opportunities.

### Step 3: Map file targeting

Identify which directories/extensions are targeted or skipped (allowlist of system paths),
size thresholds, and partial-vs-full encryption (many encrypt only the first N bytes/blocks
for speed).

### Step 4: Capture markers and metadata

Most families append an extension, write a per-file footer/magic marker, and store the
wrapped key or IV there. The script fingerprints before/after test files to extract markers.

```bash
python scripts/analyst.py compare plain/ encrypted/
```

### Step 5: Document recovery-relevant facts

Note shadow-copy/backup deletion (`vssadmin delete shadows`), the ransom note, and any
cryptographic mistakes that affect decryptability.

## Validation

- The identified scheme matches observed file changes (e.g. hybrid → high-entropy body + a
  fixed-size footer).
- File markers/extensions are consistent across encrypted test files.
- Shadow-copy deletion and note-drop are confirmed dynamically.

## Pitfalls

- Assuming decryptability from the algorithm name; correct AES/RSA usage is not recoverable.
  Recovery hinges on implementation flaws or leaked keys.
- Missing partial-encryption schemes, leading to wrong impact assessment.
- Running against real files instead of disposable test data.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the file-marker
  comparison tool.
- No More Ransom and NIST crypto standards (linked in frontmatter).
