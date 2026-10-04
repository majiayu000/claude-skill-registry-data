---
name: defanging-and-sharing-iocs
description: 'Prepares indicators of compromise for safe sharing: defanging URLs, domains, IPs,
  and emails so they cannot be accidentally clicked or resolved, and formatting them into
  STIX/CSV/MISP-friendly output. Activates for requests to defang IOCs, sanitize indicators for
  a report, or export indicators for sharing.'
domain: cybersecurity
subdomain: lab-foundations
tags:
  - lab-foundations
  - ioc
  - defanging
  - sharing
  - stix
  - reporting
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1071
d3fend:
  - D3-DA
references:
  - 'STIX 2.1 specification — https://docs.oasis-open.org/cti/stix/v2.1/stix-v2.1.html'
  - 'OpenIOC / MISP indicator sharing — https://www.misp-project.org/'
---

# Defanging and Sharing IOCs

## When to Use

- You are about to put indicators in a report, ticket, chat, or email and must prevent accidental
  clicks or resolution.
- You need to export indicators in a structured format for a sharing platform (MISP/STIX) or feed.
- You are normalizing a messy indicator list before distribution.

**Do not use** raw, live indicators in any document a human or tool might auto-process — a clicked
URL or auto-resolved domain can tip off the adversary or infect a reader.

## Prerequisites

- A list of extracted indicators (from the IOC-extraction skill) and the target sharing format.

## Workflow

### Step 1: Normalize the indicators

Deduplicate and canonicalize (lowercase domains, strip trailing dots) so the output is clean.

### Step 2: Defang for safety

Apply standard defanging: `http`→`hxxp`, `.`→`[.]`, `@`→`[at]`, `://`→`[://]`. This blocks
hyperlinking and casual copy-paste resolution.

```bash
python scripts/analyst.py defang iocs.txt
```

### Step 3: Classify and structure

Tag each indicator by type (url, domain, ipv4, email, hash) and emit a structured form (CSV or a
minimal STIX-style bundle) for the target platform.

### Step 4: Add context

Attach the source, first-seen date, confidence, and related ATT&CK technique so consumers can
act on the indicator.

## Validation

- No output indicator is clickable or auto-resolvable (all are defanged).
- Each indicator is correctly typed and deduplicated.
- The structured export imports cleanly into the target platform.

## Pitfalls

- Defanging inconsistently, so some indicators remain live.
- Sharing indicators without context (source, confidence), reducing their value.
- Over-defanging hashes (no need) or mangling indicators so they cannot be re-fanged for use.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the defang/export helper.
- STIX 2.1 and MISP (linked in frontmatter).
