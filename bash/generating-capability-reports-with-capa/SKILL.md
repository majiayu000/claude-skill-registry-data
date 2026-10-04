---
name: generating-capability-reports-with-capa
description: 'Uses capa to identify malware capabilities from a binary: running rule-based
  detection over disassembly, mapping matched capabilities to MITRE ATT&CK and MBC, and
  interpreting results to focus deeper analysis. Activates for requests to run capa, generate a
  capability report, or map a sample''s behaviors to ATT&CK automatically.'
domain: cybersecurity
subdomain: malware-analysis
tags:
  - malware-analysis
  - capa
  - capability
  - static-analysis
  - mitre-attack
  - mbc
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1059
  - T1106
  - T1027
d3fend:
  - D3-FCR
  - D3-DA
references:
  - 'capa (Mandiant FLARE) — https://github.com/mandiant/capa'
  - 'Malware Behavior Catalog (MBC) — https://github.com/MBCProject/mbc-markdown'
---

# Generating Capability Reports with capa

## When to Use

- You want an automated, rule-based read of what a binary can do before manual reversing.
- You need capabilities mapped to MITRE ATT&CK and the Malware Behavior Catalog (MBC).
- You are prioritizing which functions to reverse based on detected capabilities.

**Do not use** capa results as a behavioral guarantee — it detects *potential* capabilities from
code patterns; packed samples must be unpacked first or capa sees only the stub.

## Prerequisites

- `capa` installed; the sample handled inertly in the lab.
- For packed samples, an unpacked dump (see the unpacking skills) before running capa.

## Safety & Handling

- capa performs static analysis; it does not run the sample. Still handle the sample inertly.
- Keep the sample password-protected at rest and reference it by hash.

## Workflow

### Step 1: Confirm the sample is analyzable

Verify it is not packed (entropy/imports). If packed, unpack and run capa on the dump, not the
stub.

### Step 2: Run capa and capture results

Generate the capability report, ideally in JSON for programmatic use plus the human view.

```bash
capa -j sample.exe > capa.json
python scripts/analyst.py summarize capa.json
```

### Step 3: Map to ATT&CK and MBC

Group matched rules by ATT&CK technique and MBC behavior to see the sample's capability profile
(e.g., persistence, injection, C2, anti-analysis).

### Step 4: Prioritize deeper analysis

Use the function addresses capa reports to jump straight to the most interesting code in your
disassembler.

## Validation

- capa was run on unpacked code, not a packer stub.
- Detected capabilities are corroborated by imports/strings before being trusted.
- The ATT&CK/MBC mapping focuses subsequent manual reversing on real functionality.

## Pitfalls

- Running capa on a packed sample and concluding "few capabilities".
- Treating a capa match as confirmed behavior rather than potential capability.
- Ignoring the reported addresses that pinpoint where to reverse.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the capa summarizer.
- capa and MBC (linked in frontmatter).
