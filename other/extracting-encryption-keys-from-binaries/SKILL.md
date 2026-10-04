---
name: extracting-encryption-keys-from-binaries
description: 'Locates candidate encryption keys in a binary by finding high-entropy fixed-size
  regions (16/24/32 bytes) near cryptographic constants or crypto API references, and surfacing
  printable key/passphrase strings. Activates for requests to extract encryption keys, find an AES
  key in a sample, or recover hardcoded crypto material.'
domain: cybersecurity
subdomain: reverse-engineering
tags:
  - reverse-engineering
  - key-extraction
  - cryptography
  - entropy
  - config-extraction
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1027
  - T1573
  - T1486
d3fend:
  - D3-SDA
  - D3-DA
references:
  - 'FIPS 197 (AES key sizes) — https://csrc.nist.gov/publications/detail/fips/197/final'
  - 'MITRE ATT&CK T1573 Encrypted Channel — https://attack.mitre.org/techniques/T1573/'
---

# Extracting Encryption Keys From Binaries

## When to Use

- You have a sample with hardcoded crypto and want to surface candidate keys/IVs (16/24/32-byte
  high-entropy blocks) and passphrase strings.
- You are recovering material to decrypt config, C2 traffic, or ransomware test vectors.

**Do not use** entropy alone as proof a region is a key — corroborate with proximity to crypto
constants/APIs and by attempting decryption. This skill reads the binary statically and executes
nothing.

## Prerequisites

- The binary (read inertly). Pairs well with the crypto-constant scanner.

## Safety & Handling

- Read bytes statically; handle recovered keys as sensitive and store securely.

## Workflow

### Step 1: Find high-entropy key-sized regions

```bash
python scripts/analyst.py keys sample.bin
```

Slides a window of 16/24/32 bytes and reports regions whose entropy exceeds a threshold (likely
random key material), with offsets.

### Step 2: Surface printable secrets

Extract printable strings that look like passphrases/hex keys (e.g., 32/64-hex, base64 of 16/32
bytes).

### Step 3: Corroborate

Rank candidates by proximity to crypto constants/API references and confirm by decrypting a known
ciphertext.

### Step 4: Document

Record candidate keys, sizes, offsets, and the corroborating evidence.

## Validation

- Candidate regions are exactly key-sized (16/24/32 bytes) and high-entropy.
- Hex/base64 key strings are length-consistent with a real key size.
- A candidate is confirmed only by successful decryption, not entropy alone.

## Pitfalls

- Compressed/packed data producing many false high-entropy regions — unpack first.
- Keys derived at runtime (KDF) not present statically.
- Endianness/encoding of the key (raw vs hex vs base64) before use.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the extractor.
- FIPS 197 and ATT&CK T1573 (linked in frontmatter).
