---
name: extracting-iocs-from-analysis-output
description: 'Extracts indicators of compromise from raw analysis artifacts: parsing strings
  dumps, sandbox reports, PCAP summaries, and logs for URLs, domains, IPs, hashes, mutexes, and
  file paths, then deduplicating and typing them. Activates for requests to extract IOCs from
  analysis output, pull indicators from a report, or harvest atomic indicators.'
domain: cybersecurity
subdomain: lab-foundations
tags:
  - lab-foundations
  - ioc
  - extraction
  - parsing
  - automation
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1071
  - T1583
d3fend:
  - D3-DA
references:
  - 'MITRE ATT&CK — https://attack.mitre.org/'
  - 'IOC types and indicator extraction patterns — https://github.com/InQuest/python-iocextract'
---

# Extracting IOCs from Analysis Output

## When to Use

- You have raw analysis output (strings, sandbox JSON, PCAP notes, logs) and need the atomic
  indicators out of it.
- You want a deduplicated, typed indicator set to feed enrichment, defanging, or detection.
- You are building the indicator section of a report from analysis artifacts.

**Do not use** naive substring matching that produces noise — validate indicator shapes and
filter obvious false positives (version strings that look like IPs, library domains).

## Prerequisites

- The analysis artifacts as text/JSON; the defanging skill for safe output.

## Workflow

### Step 1: Gather the artifacts

Collect strings output, sandbox report fields, network summaries, and relevant log excerpts into
text the extractor can scan.

### Step 2: Extract by pattern

Pull URLs, domains, IPv4 addresses, email addresses, and hashes (MD5/SHA-1/SHA-256) with
validated patterns; also capture host artifacts (mutexes, registry keys, file paths) where the
format allows.

```bash
python scripts/analyst.py extract analysis.txt
```

### Step 3: Filter and deduplicate

Drop benign noise (Microsoft/CDN domains, localhost, RFC1918 where irrelevant) and deduplicate;
keep a record of what was filtered and why.

### Step 4: Type and hand off

Tag each indicator with its type and pass the set to enrichment/defanging for reporting.

## Validation

- Extracted indicators match valid shapes (no malformed IPs/hashes).
- The set is deduplicated and obvious benign noise is filtered with a rationale.
- Each indicator is typed and ready for enrichment/defanging.

## Pitfalls

- Capturing version numbers as IPs or library hostnames as C2.
- Missing indicators split across lines or encoded (base64) in the artifacts.
- Not recording what was filtered, losing analyst auditability.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the IOC extractor.
- MITRE ATT&CK and indicator-extraction patterns (linked in frontmatter).
