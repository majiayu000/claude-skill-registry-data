---
name: analyzing-authenticode-signatures
description: 'Analyzes Windows Authenticode signatures on PE files: checking for a signature,
  reading the signer certificate chain, detecting revoked/expired/stolen certs, and recognizing
  signature-stripping and catalog-signing abuse. Activates for requests to analyze a code
  signature, verify Authenticode, or assess signer trust on a PE.'
domain: cybersecurity
subdomain: malware-analysis
tags:
  - malware-analysis
  - authenticode
  - code-signing
  - pe
  - certificates
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1553.002
  - T1036.001
d3fend:
  - D3-FCR
references:
  - 'Windows Authenticode PE signature format — https://learn.microsoft.com/windows-hardware/drivers/install/authenticode'
  - 'Microsoft PE/COFF specification (security directory) — https://learn.microsoft.com/windows/win32/debug/pe-format'
---

# Analyzing Authenticode Signatures

## When to Use

- You need to know whether a PE is signed and whether the signer is trustworthy.
- You suspect a stolen/abused code-signing certificate or a forged/invalid signature.
- You are distinguishing legitimately signed software from signed malware.

**Do not use** "is signed" as "is safe" — adversaries use stolen certs, abuse catalog signing,
and append invalid signatures; a valid signature only attests the signer, not benignity.

## Prerequisites

- Access to the PE security directory (Python `struct`/`pefile`); on Windows, `signtool`/PowerShell
  `Get-AuthenticodeSignature` for authoritative verification.

## Safety & Handling

- Parse the signature statically; never execute the sample.
- Keep the sample password-protected at rest and reference it by hash.

## Workflow

### Step 1: Check for a signature

Read the PE security directory (certificate table). Absent entry = unsigned; present = embedded
PKCS#7. Note that valid signing can also be via a catalog file (not embedded).

```bash
python scripts/analyst.py check sample.exe
```

### Step 2: Extract signer details

Parse the PKCS#7 to read the signer certificate: subject, issuer, validity dates, and serial.
Cross-reference against known-abused/stolen certs.

### Step 3: Verify, do not just read

On Windows, verify the signature cryptographically and check revocation
(`Get-AuthenticodeSignature`). A present-but-invalid signature is a strong red flag.

### Step 4: Assess trust in context

Weigh signer reputation, certificate age, and whether the signed file's behavior matches the
purported publisher. Treat anomalies (recently issued cert, mismatched publisher) as suspicious.

## Validation

- Signature presence is determined from the security directory, and verified (not just read) on
  Windows.
- Signer certificate details are extracted and checked against abuse intel.
- The trust conclusion accounts for revocation/validity, not mere presence.

## Pitfalls

- Equating a present signature with safety; stolen-cert malware is common.
- Missing catalog-signed files by only checking embedded signatures.
- Reading the signature without cryptographically verifying it.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the signature checker.
- Authenticode format and the PE/COFF security directory (linked in frontmatter).
