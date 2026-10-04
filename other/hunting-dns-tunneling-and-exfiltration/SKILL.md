---
name: hunting-dns-tunneling-and-exfiltration
description: 'Detects DNS-based tunneling and data exfiltration in DNS logs: scoring high query
  volume to single domains, long/high-entropy subdomains, unusual record types, and encoded
  payload labels. Activates for requests to hunt DNS tunneling, detect DNS exfiltration, or
  analyze suspicious DNS query patterns.'
domain: cybersecurity
subdomain: threat-hunting
tags:
  - threat-hunting
  - dns
  - tunneling
  - exfiltration
  - network
  - entropy
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1071.004
  - T1048.003
  - T1572
d3fend:
  - D3-NTA
  - D3-DNSTA
references:
  - 'MITRE ATT&CK T1071.004 DNS — https://attack.mitre.org/techniques/T1071/004/'
  - 'MITRE ATT&CK T1048 Exfiltration Over Alternative Protocol — https://attack.mitre.org/techniques/T1048/'
---

# Hunting DNS Tunneling and Exfiltration

## When to Use

- You have DNS query logs (resolver, Zeek `dns.log`, Windows DNS) and want to find tunneling or
  exfiltration over DNS.
- You are testing a hypothesis that an implant uses DNS as a covert channel.
- You need to rank domains by tunneling indicators across many queries.

**Do not use** query length alone as a verdict — CDNs, antivirus lookups, and some SaaS use long
encoded labels legitimately; combine entropy, volume, and record-type signals.

## Prerequisites

- DNS logs with query name, query type, source, and timestamp, over a meaningful window.
- A way to whitelist known-benign high-volume domains (security vendors, CDNs).

## Workflow

### Step 1: Aggregate by registered domain

Group queries under their registered/parent domain so per-domain volume and subdomain diversity
are visible.

### Step 2: Score tunneling indicators

Weight: high unique-subdomain count, long average label length, high subdomain entropy (encoded
data), heavy `TXT`/`NULL`/`CNAME` usage, and high query rate to one domain.

```bash
python scripts/analyst.py hunt dns.json
```

### Step 3: Estimate exfiltration volume

Sum encoded bytes implied by query lengths per domain; sustained high volume to a single
nameserver suggests data egress.

### Step 4: Whitelist and pivot

Remove known-benign high-entropy domains; for survivors, check domain age/registration, the
authoritative nameserver, and the originating host.

### Step 5: Confirm and respond

Validate by decoding sampled labels where possible and correlating with host activity; escalate
confirmed tunnels and write a detection.

## Validation

- High-score domains combine multiple signals (entropy + volume + record type), not one alone.
- Benign high-volume domains are whitelisted, keeping the list reviewable.
- Confirmed tunnels tie to a specific host and a young/suspicious domain.

## Pitfalls

- Flagging long labels from CDNs and AV telemetry as tunneling.
- Aggregating by full FQDN instead of registered domain, hiding subdomain diversity.
- Ignoring record type; `TXT`/`NULL` carry far more data than `A` records.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the DNS hunt scorer.
- ATT&CK T1071.004 and T1048 (linked in frontmatter).
