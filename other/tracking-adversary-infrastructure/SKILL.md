---
name: tracking-adversary-infrastructure
description: 'Tracks adversary C2 and staging infrastructure by clustering indicators on shared
  attributes (TLS/JARM, certificate fields, favicon hashes, ASN, registration patterns) to find
  related hosts. Activates for requests to track adversary infrastructure, cluster C2 servers, or
  pivot on infrastructure attributes to find related hosts.'
domain: cybersecurity
subdomain: threat-hunting
tags:
  - threat-hunting
  - infrastructure
  - c2-tracking
  - clustering
  - intel
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1583
  - T1583.001
  - T1071
d3fend:
  - D3-NTA
  - D3-IAA
references:
  - 'MITRE ATT&CK T1583 Acquire Infrastructure — https://attack.mitre.org/techniques/T1583/'
  - 'JARM TLS fingerprinting — https://github.com/salesforce/jarm'
---

# Tracking Adversary Infrastructure

## When to Use

- You have a set of suspected C2/staging hosts with attributes (JARM/JA3S, TLS cert fields, favicon
  hash, ASN, ports, registrar) and want to cluster them to find related infrastructure.
- You are expanding from a few known indicators to the adversary's broader footprint.

**Do not use** clustering as confirmed attribution — shared hosting/attributes can be coincidental.
Corroborate before attributing.

## Prerequisites

- Host records (CSV/JSON) with shared-attribute fields to cluster on.

## Workflow

### Step 1: Cluster on shared attributes

```bash
python scripts/analyst.py cluster hosts.json --attrs jarm,cert_cn,favicon_hash,asn
```

Groups hosts that share one or more pivot attributes into clusters, defanging host indicators.

### Step 2: Score cluster cohesion

Rank clusters by how many distinct attributes the members share (more shared attributes → stronger
relationship).

### Step 3: Expand and confirm

Use the strongest shared attributes (e.g., a unique self-signed cert CN or favicon hash) to pivot
in internet-scan data for more hosts; corroborate.

### Step 4: Document

Record clusters, the shared pivots, and confidence; feed confirmed indicators to detection.

## Validation

- Clustering keys on explicit shared attributes, not loose similarity.
- Cluster strength reflects the count of distinct shared attributes.
- Host indicators are defanged in output.

## Pitfalls

- Common CDN/cloud JARM/ASN values creating huge false clusters — exclude generic pivots.
- Default certificates shared by unrelated servers.
- Treating one weak shared attribute as a strong link.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the clustering tool.
- ATT&CK T1583 and JARM references (linked in frontmatter).
