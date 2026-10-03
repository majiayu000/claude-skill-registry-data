---
name: intel-mitre-ttps
description: "The MITRE ATT&CK Navigator is a web application for annotating and visualizing ATT&CK matrices. Combined with the attackcti Python library (which queries ATT&CK STIX data via TAXII), analysts can programmatically generate Navigator layer files mapping specific threat group TTPs, compare multiple groups, and assess detection coverage gaps against known adversaries."
domain: cybersecurity
---
# Analyzing Threat Actor TTPs with MITRE Navigator

## Overview

The MITRE ATT&CK Navigator is a web application for annotating and visualizing ATT&CK matrices.
Combined with the attackcti Python library (which queries ATT&CK STIX data via TAXII), analysts
can programmatically generate Navigator layer files mapping specific threat group TTPs, compare
multiple groups, and assess detection coverage gaps against known adversaries.

## When to Use

- When investigating security incidents that require analyzing threat actor ttps with mitre navigator
- When building detection rules or threat hunting queries for this domain
- When SOC analysts need structured procedures for this analysis type
- When validating security monitoring coverage for related attack techniques

## Prerequisites

- Python 3.8+ with attackcti and stix2 libraries installed
- MITRE ATT&CK Navigator (web UI or local instance)
- Understanding of STIX 2.1 objects and relationships

## Steps

1. Query ATT&CK STIX data for target threat group using attackcti
2. Extract techniques associated with the group via STIX relationships
3. Generate ATT&CK Navigator layer JSON with technique annotations
4. Overlay detection coverage to identify gaps
5. Export layer for team review and defensive planning

## Expected Output

```json
{
  "name": "APT29 TTPs",
  "domain": "enterprise-attack",
  "techniques": [
    {"techniqueID": "T1566.001", "score": 1, "comment": "Spearphishing Attachment"},
    {"techniqueID": "T1059.001", "score": 1, "comment": "PowerShell"}
  ]
}
```
