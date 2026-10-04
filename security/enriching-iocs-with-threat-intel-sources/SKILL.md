---
name: enriching-iocs-with-threat-intel-sources
description: 'Enriches indicators with context from threat-intel sources: planning lookups against
  reputation, passive DNS, WHOIS, and sandbox/sample databases, scoring confidence, and avoiding
  operational-security mistakes that tip off adversaries. Activates for requests to enrich IOCs,
  add threat context, or plan indicator lookups safely.'
domain: cybersecurity
subdomain: lab-foundations
tags:
  - lab-foundations
  - ioc
  - enrichment
  - threat-intel
  - opsec
  - reputation
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1583
  - T1071
d3fend:
  - D3-DA
references:
  - 'MITRE ATT&CK — https://attack.mitre.org/'
  - 'Passive DNS and indicator enrichment concepts — https://www.first.org/'
---

# Enriching IOCs with Threat Intel Sources

## When to Use

- You have atomic indicators and need context: reputation, related infrastructure, first/last
  seen, and known associations.
- You are scoring indicator confidence before acting or reporting.
- You must plan lookups without leaking your investigation to the adversary.

**Do not use** active interaction (visiting a C2 URL, resolving a live domain from your own
network) for enrichment — use passive sources to avoid tipping off the adversary.

## Prerequisites

- Defanged indicators (from the defanging skill) and access to enrichment sources/APIs.
- Awareness of each source's operational-security implications.

## Safety & Handling

- Prefer passive sources (passive DNS, sample DBs, reputation feeds) over active probing.
- Never submit a customer/internal sample to a public sandbox without authorization — it becomes
  publicly retrievable and can expose sensitive data.

## Workflow

### Step 1: Group indicators by type

Separate hashes, domains, IPs, and URLs; each maps to different enrichment sources.

### Step 2: Plan the right lookups

Map each type to passive sources: hashes → sample/AV databases; domains → passive DNS, WHOIS,
reputation; IPs → ASN/geo, passive DNS, reputation; URLs → URL reputation/sandbox history.

```bash
python scripts/analyst.py plan iocs.json
```

### Step 3: Score confidence

Combine source agreement, age, and prevalence into a confidence score; a single hit on one feed
is weaker than corroboration across independent sources.

### Step 4: Annotate and pivot

Attach context (first seen, related infrastructure, family) and pivot on strong links (shared
registrant, hosting, certificate) to expand the picture.

### Step 5: Record provenance

Note which source provided each piece of context and when, so the enrichment is auditable and
re-checkable.

## Validation

- Each indicator is routed to type-appropriate, passive sources.
- Confidence reflects corroboration across independent sources, not a single feed.
- Every enrichment carries source and timestamp provenance.

## Pitfalls

- Actively resolving/visiting live infrastructure and alerting the adversary.
- Uploading sensitive samples to public services, leaking data.
- Treating one feed's verdict as ground truth without corroboration.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the lookup planner.
- MITRE ATT&CK and passive-DNS enrichment concepts (linked in frontmatter).
