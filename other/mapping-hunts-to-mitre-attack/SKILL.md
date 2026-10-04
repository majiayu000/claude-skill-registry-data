---
name: mapping-hunts-to-mitre-attack
description: 'Maps hunts and detections to MITRE ATT&CK for coverage analysis: tagging hypotheses
  with techniques, building a coverage matrix from completed hunts, and identifying high-risk
  gaps to prioritize next. Activates for requests to map hunts to ATT&CK, build a coverage
  heatmap, or find detection gaps by technique.'
domain: cybersecurity
subdomain: threat-hunting
tags:
  - threat-hunting
  - mitre-attack
  - coverage
  - detection-gaps
  - navigator
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1059
  - T1047
  - T1071
d3fend:
  - D3-DA
references:
  - 'MITRE ATT&CK Navigator — https://github.com/mitre-attack/attack-navigator'
  - 'MITRE ATT&CK techniques — https://attack.mitre.org/techniques/enterprise/'
---

# Mapping Hunts to MITRE ATT&CK

## When to Use

- You have a backlog of hunts/detections and want a coverage view by technique.
- You need to prioritize the next hunt by mapping current coverage against relevant adversary
  TTPs (e.g., from a threat profile).
- You want to produce an ATT&CK Navigator layer to visualize coverage and gaps.

**Do not use** technique counts as a quality metric — broad shallow coverage can hide weak
detections; pair the map with detection confidence.

## Prerequisites

- An inventory of hunts/detections with the data sources each uses.
- The ATT&CK enterprise matrix (technique IDs and tactics) for reference.

## Workflow

### Step 1: Tag each hunt with techniques

Annotate every hunt/detection with the ATT&CK technique(s) it covers and a confidence score
(e.g., high/medium/low based on telemetry quality and FP rate).

### Step 2: Build the coverage matrix

Aggregate tags into a technique → coverage map. Group by tactic to see where the kill chain is
strong or thin.

```bash
python scripts/analyst.py coverage hunts.json --out layer.json
```

### Step 3: Overlay your threat model

Weight techniques by relevance (actors targeting your sector, observed in incidents). A gap on
a high-relevance technique outranks a gap on an unlikely one.

### Step 4: Identify and prioritize gaps

Surface techniques with no coverage or low confidence; rank by threat relevance and data
availability to pick the next hunt.

### Step 5: Visualize and share

Emit an ATT&CK Navigator layer (scores/colors) for stakeholders and to track progress over
time.

## Validation

- Every hunt maps to at least one valid technique ID (`^T\d{4}(\.\d{3})?$`).
- Coverage reflects confidence, not just presence/absence.
- The Navigator layer loads and renders the intended scores.

## Pitfalls

- Counting a low-confidence hunt as full coverage.
- Mapping to overly broad parent techniques when a sub-technique is more accurate.
- Ignoring data-source feasibility when prioritizing gaps.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the coverage/layer
  generator.
- ATT&CK Navigator and enterprise techniques (linked in frontmatter).
