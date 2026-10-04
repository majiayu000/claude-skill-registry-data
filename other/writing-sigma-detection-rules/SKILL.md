---
name: writing-sigma-detection-rules
description: 'Converts hunt findings into portable Sigma detection rules: choosing the right
  logsource, expressing robust selection/filter logic, setting level and ATT&CK tags, and
  validating before converting to a SIEM query. Activates for requests to write a Sigma rule,
  convert a hunt to a detection, or create portable SIEM detection logic.'
domain: cybersecurity
subdomain: threat-hunting
tags:
  - threat-hunting
  - sigma
  - detection-engineering
  - siem
  - rules
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1059.001
  - T1547.001
d3fend:
  - D3-DA
references:
  - 'Sigma specification — https://github.com/SigmaHQ/sigma-specification'
  - 'Sigma rules repository — https://github.com/SigmaHQ/sigma'
---

# Writing Sigma Detection Rules

## When to Use

- A hunt produced reliable logic and you want a portable, SIEM-agnostic detection.
- You need to share or version a detection in a standard format and tag it to ATT&CK.
- You are translating a vendor query into Sigma for reuse across backends.

**Do not use** Sigma for stateful/correlation logic it cannot express well (complex sequence or
statistical detections) — keep those in the SIEM's native correlation engine.

## Prerequisites

- The `sigma` CLI / `sigma-cli` (pysigma) for validation and conversion.
- Knowledge of the target log source's field names and the Sigma taxonomy.

## Workflow

### Step 1: Define the logsource

Pin `category`/`product`/`service` precisely (e.g., `product: windows`,
`category: process_creation`) so the rule maps to the right pipeline.

### Step 2: Write robust selection logic

Express the detection on stable fields. Prefer multiple ANDed conditions over a single brittle
string; use `contains`/`endswith` modifiers thoughtfully to resist evasion.

```bash
python scripts/analyst.py scaffold --title "Encoded PowerShell" --category process_creation \
  --technique T1059.001 --level high
```

### Step 3: Add filters to cut false positives

Use a `filter` block (negated in the condition) to exclude known-good processes/paths rather
than narrowing selection until it misses variants.

### Step 4: Tag and document

Add `tags` (ATT&CK technique), `level`, `status`, `references`, and a `falsepositives` list so
consumers can tune.

### Step 5: Validate and convert

Lint the rule, then convert to the target backend and test against true/false-positive data
before deploying.

```bash
sigma convert -t splunk rules/encoded_powershell.yml
```

## Validation

- The rule passes Sigma schema validation (`sigma check`).
- It fires on the hunt's true positives and not on the documented benign cases.
- Conversion to the target backend produces a sensible, runnable query.

## Pitfalls

- Over-narrow selection that matches one sample and misses the technique.
- Wrong logsource, so the rule never sees the relevant events.
- No `falsepositives`/filter, producing a noisy alert that gets ignored.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the Sigma scaffolder.
- Sigma specification and rules repository (linked in frontmatter).
