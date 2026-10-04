---
name: profiling-a-threat-actor-from-ttps
description: 'Profiles a threat actor by aggregating observed ATT&CK techniques into a TTP profile
  and comparing it against known-group technique sets to estimate similarity and candidate
  attribution. Activates for requests to profile a threat actor, compare observed TTPs to known
  groups, or estimate attribution from technique overlap.'
domain: cybersecurity
subdomain: threat-hunting
tags:
  - threat-hunting
  - threat-actor
  - attribution
  - ttp
  - mitre-attack
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1059
  - T1071
  - T1583
d3fend:
  - D3-IAA
  - D3-NTA
references:
  - 'MITRE ATT&CK Groups — https://attack.mitre.org/groups/'
  - 'ATT&CK Navigator (technique comparison) — https://github.com/mitre-attack/attack-navigator'
---

# Profiling a Threat Actor From TTPs

## When to Use

- You have a set of observed ATT&CK techniques from an intrusion and want to build a TTP profile
  and compare it against known-group technique sets for candidate attribution.
- You are estimating similarity, not asserting attribution.

**Do not use** technique overlap as confirmed attribution — many groups share common techniques.
Present candidates with similarity scores and the need for corroborating intel.

## Prerequisites

- Observed technique IDs from the intrusion and a reference of group→techniques (CSV/JSON).

## Workflow

### Step 1: Build the observed TTP profile

Collect the deduplicated set of observed ATT&CK technique IDs (including sub-techniques).

### Step 2: Compare against known groups

```bash
python scripts/analyst.py compare --observed observed.txt --groups groups.json
```

Computes Jaccard and overlap-coefficient similarity between the observed set and each group's
technique set, ranking candidate groups.

### Step 3: Weigh distinctive techniques

Prioritize matches on less-common techniques (shared rare TTPs are stronger signals than ubiquitous
ones).

### Step 4: Document

Report ranked candidates with similarity scores, the overlapping techniques, and an explicit
low/medium confidence — never definitive attribution from TTPs alone.

## Validation

- Similarity is computed on technique-ID sets (sub-techniques included).
- Candidates are ranked by both Jaccard and overlap coefficient.
- Output states confidence and lists the overlapping techniques.

## Pitfalls

- Over-attributing on common techniques (T1059, T1027) shared by most groups.
- Reference group data being incomplete or out of date.
- Treating a single high overlap as proof without corroborating intel.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the comparison tool.
- ATT&CK Groups and Navigator references (linked in frontmatter).
