---
name: operationalizing-a-hunt-into-a-detection
description: 'Converts a successful threat hunt into a durable detection by extracting the
  discriminating logic, defining data sources and thresholds, and emitting a Sigma rule plus a
  test and tuning plan. Activates for requests to operationalize a hunt, turn a finding into a
  detection rule, or productionize hunt logic as a Sigma detection.'
domain: cybersecurity
subdomain: threat-hunting
tags:
  - threat-hunting
  - detection-engineering
  - sigma
  - operationalization
  - automation
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1059
  - T1071
  - T1053
d3fend:
  - D3-PSA
  - D3-NTA
references:
  - 'Sigma rule specification — https://github.com/SigmaHQ/sigma-specification'
  - 'MITRE ATT&CK threat-hunting resources — https://attack.mitre.org/resources/'
---

# Operationalizing a Hunt Into a Detection

## When to Use

- A hunt surfaced malicious activity and you want to convert the discriminating logic into a
  repeatable detection (Sigma) with data sources, thresholds, and a tuning plan.
- You are closing the hunt→detect loop so the finding is caught automatically next time.

**Do not use** this to ship a rule without a false-positive review — operationalization includes
tuning. The script generates rule scaffolding, not a deployment.

## Prerequisites

- The hunt's discriminating fields/values, the data source/log channel, and the mapped ATT&CK
  technique.

## Workflow

### Step 1: Specify the detection

Define the logsource (category/product), the selection (field→value(s) that discriminated true
positives), optional filters, the condition, and the ATT&CK technique.

### Step 2: Generate the Sigma rule

```bash
python scripts/analyst.py generate --spec detection.json --out rule.yml
```

Emits a valid Sigma rule (title, status, logsource, detection, condition, level, tags) from the
spec.

### Step 3: Plan testing and tuning

Define how to validate (replay a known-true pcap/log, atomic test) and what benign sources may
cause false positives.

### Step 4: Document and stage

Record the rule's intent, expected FPs, and tuning levers; stage through your detection pipeline.

## Validation

- The generated rule has logsource, detection, and condition keys.
- The selection encodes the fields/values that discriminated the hunt's true positives.
- The rule is tagged with the relevant ATT&CK technique.

## Pitfalls

- Encoding incidental artifacts (one host's path) instead of generalizable logic.
- Omitting filters for known-benign sources, guaranteeing alert fatigue.
- No test plan, so regressions go unnoticed.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the rule generator.
- Sigma specification and ATT&CK hunting resources (linked in frontmatter).
