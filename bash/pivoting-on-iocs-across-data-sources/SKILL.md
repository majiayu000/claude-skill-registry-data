---
name: pivoting-on-iocs-across-data-sources
description: 'Pivots on indicators of compromise across multiple data sources by correlating a seed
  set of IOCs against logs to find co-occurring indicators, hosts, and timeframes that expand the
  investigation. Activates for requests to pivot on IOCs, correlate indicators across data sources,
  or expand an investigation from a seed indicator set.'
domain: cybersecurity
subdomain: threat-hunting
tags:
  - threat-hunting
  - ioc-pivoting
  - correlation
  - investigation
  - intel
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1071
  - T1041
  - T1105
d3fend:
  - D3-NTA
  - D3-IAA
references:
  - 'Pyramid of Pain (indicator pivoting) — https://www.sans.org/'
  - 'MITRE ATT&CK techniques — https://attack.mitre.org/techniques/'
---

# Pivoting on IOCs Across Data Sources

## When to Use

- You have a seed set of IOCs (IPs, domains, hashes, URLs) and multiple log sources, and you want
  to find co-occurring indicators, affected hosts, and the activity timeframe.
- You are expanding an investigation from initial indicators to the full scope.

**Do not use** raw, undeduplicated matching that floods on common indicators — anchor pivots on the
specific seed set and report co-occurrence, not every mention.

## Prerequisites

- A seed IOC list and one or more log sources (CSV/JSON) containing indicator fields.

## Workflow

### Step 1: Match seeds and gather co-occurrence

```bash
python scripts/analyst.py pivot --seeds iocs.txt --logs events.csv
```

Finds log records matching any seed IOC, then reports the hosts, additional indicators, and time
range co-occurring with the seeds.

### Step 2: Rank new indicators

Surface newly co-occurring indicators (not in the seed set) ranked by how often they appear
alongside seeds — candidates to add to the IOC set.

### Step 3: Confirm and expand

Validate promising new indicators and re-run the pivot to widen scope iteratively.

### Step 4: Document

Record matched hosts, the timeframe, and the expanded indicator set; defang in output.

## Validation

- Matches are anchored to the seed IOC set.
- Co-occurring hosts/indicators and the time range are reported.
- New indicators are ranked by co-occurrence with seeds; output is defanged.

## Pitfalls

- Common indicators (shared CDNs, OS update hosts) inflating co-occurrence — exclude allow-listed.
- Field/format mismatches (IP vs CIDR, defanged vs plain) missing matches.
- Time-zone inconsistencies skewing the activity window.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the pivot tool.
- Pyramid of Pain and ATT&CK references (linked in frontmatter).
