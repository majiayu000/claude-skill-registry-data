---
name: establishing-telemetry-baselines
description: 'Establishes behavioral baselines from historical telemetry (process, network, or
  logon events) so hunts can flag rare and first-seen activity instead of relying on static
  signatures. Activates for requests to build a telemetry baseline, find rare or first-seen
  activity, or compute frequency baselines for anomaly hunting.'
domain: cybersecurity
subdomain: threat-hunting
tags:
  - threat-hunting
  - baselining
  - anomaly-detection
  - frequency-analysis
  - telemetry
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1059
  - T1071
  - T1204
d3fend:
  - D3-PSA
  - D3-NTA
car:
  - CAR-2013-05-002
references:
  - 'The ThreatHunting Project — https://www.threathunting.net/'
  - 'MITRE ATT&CK Getting Started with Threat Hunting — https://attack.mitre.org/resources/'
---

# Establishing Telemetry Baselines

## When to Use

- You want to hunt for rare or first-seen behavior (uncommon process names, parent/child pairs,
  destinations) by comparing current activity to a historical baseline.
- You are reducing noise by establishing what "normal" looks like before alerting on outliers.

**Do not use** a baseline built from a compromised period as "normal" — seed it from a known-good
window. This skill computes statistics from telemetry and executes nothing.

## Prerequisites

- Historical telemetry (CSV/JSON) with a categorical field to baseline (e.g., process name,
  parent-child pair, destination host).

## Workflow

### Step 1: Build the baseline

```bash
python scripts/analyst.py baseline history.csv --field Image
```

Computes per-value counts, frequency (stacked-rank), and the set of values seen, saved as a JSON
baseline.

### Step 2: Score new activity against the baseline

```bash
python scripts/analyst.py compare new.csv --field Image --baseline baseline.json
```

Flags values not present in the baseline (first-seen) and values below a rarity threshold.

### Step 3: Triage outliers

Investigate first-seen and rare values; many will be benign-but-new — corroborate with context.

### Step 4: Maintain

Refresh the baseline on a rolling known-good window to avoid drift.

## Validation

- The baseline captures counts and the value set from the historical window.
- First-seen values in new data are correctly identified as absent from the baseline.
- Rarity thresholds are explicit and tunable.

## Pitfalls

- Baselining a compromised window, normalizing malicious activity.
- Too-short baseline windows making common items look rare.
- High-cardinality fields (full command lines) needing normalization before baselining.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the baseliner.
- The ThreatHunting Project and ATT&CK hunting resources (linked in frontmatter).
