---
name: writing-suricata-and-snort-rules
description: 'Writes and validates Suricata/Snort IDS rules for network-based malware detection,
  covering rule anatomy, content/pcre matching, flow and threshold options, and common mistakes
  that cause false positives or no matches. Activates for requests to write a Suricata rule, create
  Snort signatures, or build network detection rules from IOCs or C2 patterns.'
domain: cybersecurity
subdomain: threat-hunting
tags:
  - threat-hunting
  - suricata
  - snort
  - ids
  - network-detection
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1071.001
  - T1095
  - T1571
d3fend:
  - D3-NTA
  - D3-NTPM
references:
  - 'Suricata rules documentation — https://docs.suricata.io/en/latest/rules/intro.html'
  - 'Snort 3 rule writing — https://docs.snort.org/'
---

# Writing Suricata and Snort Rules

## When to Use

- You need to author IDS rules to detect C2 traffic, malware downloads, or exploit attempts from
  observed network indicators.
- You want to validate rule syntax and avoid the patterns that cause false positives or silent
  non-matching.

**Do not use** broad `content` matches on common substrings that will flood alerts — anchor with
flow direction, ports, offsets, and uniqueness. This skill builds and lints rules; deploy them
through your IDS change process.

## Prerequisites

- The indicators to detect (URI, host header, TLS SNI/JA3, byte pattern) and a target IDS
  (Suricata or Snort).

## Workflow

### Step 1: Draft the rule

Choose action, protocol, addresses/ports, direction, and a unique `msg`, `sid`, and `rev`. Add
`content`/`pcre` matches anchored with `http.uri`, `tls.sni`, `flow:established,to_server`, and
offsets/depths.

### Step 2: Lint the rule

```bash
python scripts/analyst.py lint rules.rules
```

Checks for required fields (`msg`, `sid`, `rev`, `classtype`), balanced quotes/parentheses,
non-anchored overly short `content`, and duplicate SIDs.

### Step 3: Tune to reduce noise

Add `threshold`/`detection_filter`, `flowbits`, and specific buffers (`http.host`, `dns.query`)
to scope matches.

### Step 4: Document and stage

Record what each rule detects and stage it for testing against a pcap before production.

## Validation

- Every rule has `msg`, a unique `sid`, and a `rev`.
- `content` matches are anchored (buffer/offset/flow) rather than free-floating short strings.
- Rules parse without unbalanced quotes/parentheses.

## Pitfalls

- Free-floating `content:"GET"` style matches creating massive false positives.
- Duplicate or reused SIDs causing rule-load conflicts.
- Forgetting `flow:established` and matching on unrelated traffic directions.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the linter.
- Suricata and Snort rule docs (linked in frontmatter).
