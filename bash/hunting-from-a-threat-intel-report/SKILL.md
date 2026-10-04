---
name: hunting-from-a-threat-intel-report
description: 'Operationalizes a threat intelligence report into hunts: extracting IOCs and TTPs,
  mapping behaviors to ATT&CK and available telemetry, prioritizing durable behavioral
  indicators over volatile atomic ones, and producing concrete hunt queries. Activates for
  requests to hunt from a threat report, operationalize CTI, or turn an intel report into
  detections.'
domain: cybersecurity
subdomain: threat-hunting
tags:
  - threat-hunting
  - threat-intelligence
  - ioc
  - mitre-attack
  - pyramid-of-pain
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1059
  - T1071
  - T1547
d3fend:
  - D3-DA
  - D3-NTA
references:
  - 'MITRE ATT&CK — https://attack.mitre.org/'
  - 'The Pyramid of Pain (David Bianco) — https://detect-respond.blogspot.com/2013/03/the-pyramid-of-pain.html'
---

# Hunting from a Threat Intel Report

## When to Use

- You received a CTI report (vendor writeup, ISAC bulletin, IR report) and must operationalize it.
- You want to convert narrative TTPs and IOC lists into concrete hunts against your telemetry.
- You need to prioritize which indicators are worth hunting given they age at different rates.

**Do not use** an IOC blocklist as the whole engagement — atomic indicators (hashes, IPs) are
trivially changed; durable value comes from hunting the behaviors (TTPs).

## Prerequisites

- The report and a way to extract its IOCs and behavioral claims.
- Knowledge of your telemetry coverage to judge which TTPs are huntable.

## Workflow

### Step 1: Extract IOCs and TTPs

Pull atomic indicators (hashes, IPs, domains, URLs) and the behavioral TTPs (the report's
"how"). Defang/normalize indicators for safe handling.

```bash
python scripts/analyst.py extract report.txt
```

### Step 2: Map to ATT&CK and the Pyramid of Pain

Tag behaviors with techniques and rank indicators by the Pyramid of Pain — prioritize TTPs and
tools over hashes/IPs because they cost the adversary more to change.

### Step 3: Check telemetry feasibility

For each TTP, confirm you have the data source to hunt it; note gaps as detection-engineering
work.

### Step 4: Build concrete hunts

Translate the high-value TTPs into queries (Sysmon, DNS, proxy, EDR), and sweep atomic IOCs as a
quick first pass for current presence.

### Step 5: Execute, document, and feed back

Run the hunts, record findings/gaps/negatives, escalate hits to IR, and convert durable logic
into detections (Sigma).

## Validation

- Both atomic IOCs and behavioral TTPs are extracted, not just the indicator list.
- Hunts target the highest-pain indicators feasible with your telemetry.
- Each TTP maps to a real data source or is logged as a coverage gap.

## Pitfalls

- Stopping at IOC sweeps; the adversary rotates them and you miss the campaign.
- Hunting TTPs you have no telemetry for, producing false confidence.
- Failing to defang indicators, risking accidental execution/clicks.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the IOC/TTP extractor.
- MITRE ATT&CK and the Pyramid of Pain (linked in frontmatter).
