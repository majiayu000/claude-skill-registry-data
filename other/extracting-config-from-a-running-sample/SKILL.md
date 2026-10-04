---
name: extracting-config-from-a-running-sample
description: 'Extracts an embedded malware configuration (C2 hosts, ports, campaign IDs, keys) from
  a process memory dump by locating decrypted config structures and decoding common obfuscation
  layers. Activates for requests to extract malware config from a memory dump, recover C2 settings
  from a running sample, or decode an in-memory configuration block.'
domain: cybersecurity
subdomain: malware-analysis
tags:
  - malware-analysis
  - config-extraction
  - memory
  - c2
  - dynamic-analysis
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1027
  - T1140
  - T1071
d3fend:
  - D3-SDA
  - D3-DA
references:
  - 'MITRE ATT&CK T1140 Deobfuscate/Decode Files or Information — https://attack.mitre.org/techniques/T1140/'
  - 'MITRE ATT&CK T1027 Obfuscated Files or Information — https://attack.mitre.org/techniques/T1027/'
---

# Extracting Config From a Running Sample

## When to Use

- You have a process memory dump of a detonated sample whose config is decrypted in memory.
- You need to recover C2 endpoints, ports, campaign/botnet IDs, mutexes, and keys.

**Do not use** this to detonate the sample — it consumes a dump already captured in an isolated
sandbox. For static-only config decryption, use the dedicated config-decryptor workflow.

## Prerequisites

- A process memory dump (`.dmp`/raw region) captured after the config was decrypted.

## Safety & Handling

- Treat the dump as malicious data; read it inertly and defang recovered endpoints.

## Workflow

### Step 1: Hunt config indicators

```bash
python scripts/analyst.py hunt process.dmp
```

Scans for URLs, IPv4:port pairs, mutex-like tokens, base64 blobs, and printable key/value
candidates in decrypted regions.

### Step 2: Decode obfuscation layers

For candidate blobs, try common transforms (single-byte XOR brute force, base64) and re-scan the
decoded output for endpoints.

### Step 3: Structure and validate the config

Assemble recovered fields into a structured config and sanity-check (valid hosts, plausible
ports, consistent campaign IDs).

### Step 4: Defang and report

Defang hosts/URLs and document the offsets where the config was recovered.

## Validation

- Recovered endpoints are real, parseable hosts/ports — not random byte noise.
- XOR/base64 decode is confirmed by the decoded output containing new endpoints/strings.
- The final config is defanged before sharing.

## Pitfalls

- Mistaking unrelated in-memory URLs (browser, OS) for C2 — corroborate with the sample's region.
- Single-byte XOR brute force producing coincidental strings; require multiple corroborating hits.
- Reporting raw, live C2 endpoints without defanging.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the hunter/decoder.
- ATT&CK T1140 and T1027 (linked in frontmatter).
