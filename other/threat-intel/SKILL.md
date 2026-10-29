---
name: threat-intel
description: "Use when working with cyber threat intelligence on a defensive team: collecting IOCs, evaluating feeds, running a MISP instance, writing STIX/TAXII sharing packages, scoring and aging indicators, and turning intel into detections and blocks. Use when the SOC needs to know which threat actors and campaigns matter to the organization, when deciding whether to block an indicator, or when sharing intel with peers under TLP rules."
version: 1.0.0
domain: osint
lifecycle: stable
last_verified: "2026-10-23"
requires: []
extends: []
relates: [osint-methodology, recon-passive]
tools:
  - name: MISP
    version: "2.5"
  - name: Python
    version: "3.12"
---
Threat intelligence turns raw indicators and reports into decisions:
what to block, what to hunt, what to patch first. This skill covers
the defensive intel workflow: requirements, collection from feeds and
open sources, evaluation and scoring, storage in MISP, sharing with
STIX/TAXII under TLP, and operationalizing intel into detections.
Collection stays on public and licensed sources; respect feed terms of
service and privacy law.

## Quick Workflow

1. Write priority intelligence requirements (PIRs): which actors,
   sectors, and techniques matter to this organization.
2. Inventory your feeds (commercial, open source, ISAC, internal) and
   map each to the PIRs it serves.
3. Ingest into MISP with source tags, TLP markings, and first-seen
   dates on everything.
4. Score and age indicators: confidence, relevance, and expiry per
   type (IPs age fast, hashes age slow).
5. Correlate new intel against your telemetry before blocking (does
   this IP talk to our hosts).
6. Operationalize: push high-confidence IOCs to blocks and detections,
   write hunts for TTPs.
7. Share finished intel with peers under the correct TLP marking.
8. Review feed value quarterly: precision, overlap, and cost per true
   positive.

## 1. Priority intelligence requirements

Intel without requirements is noise. Write PIRs like:

- PIR-1: Which ransomware affiliates are targeting our sector in
  Europe this quarter, and what are their initial access TTPs.
- PIR-2: Are any of our domains, IPs, or executive names appearing in
  stealer logs or underground forums.
- PIR-3: Which vulnerabilities in our internet-facing stack have
  public exploits and active exploitation in the wild.

Each PIR gets an owner, a review date, and a list of feeds and
collection tasks that serve it. If a feed serves no PIR, drop it.

## 2. Feed inventory and evaluation

Common feed types: commercial intel platforms, open source blocklists,
ISAC/ISAO sharing groups, government advisories (CISA AA reports),
internal telemetry (your own incidents are your best intel).

Evaluate a feed before trusting it:

```bash
# Measure overlap and freshness of two IP feeds with Python (stdlib)
python3 << 'EOF'
a = set(l.strip() for l in open('feed_a.txt') if l.strip())
b = set(l.strip() for l in open('feed_b.txt') if l.strip())
print("A:", len(a), "B:", len(b), "overlap:", len(a & b))
print("A unique:", len(a - b), "B unique:", len(b - a))
EOF
```

Track per feed: ingestion volume, true positive rate on your
telemetry, mean indicator age at ingest, and cost. A free feed with
90 percent stale IPs is more expensive than it looks once analyst
time is counted.

## 3. MISP operations

MISP is the standard open platform for storing and sharing intel.
Core concepts: events (containers), attributes (IOCs with types),
objects (structured entities like vulnerabilities), galaxies (actor
and tool taxonomies), tags, and TLP markings.

```bash
# Search MISP for an indicator via the API (needs your API key)
curl -sk -H "Authorization: $MISP_KEY" \
  -H "Accept: application/json" -H "Content-Type: application/json" \
  -d '{"returnFormat":"json","value":"198.51.100.23"}' \
  https://misp.internal/attributes/restSearch

# Add a simple IOC event via API
curl -sk -H "Authorization: $MISP_KEY" \
  -H "Accept: application/json" -H "Content-Type: application/json" \
  -d '{"Event":{"info":"Phishing infra 2026-10-23","distribution":1,
    "threat_level_id":2,"analysis":1,
    "Attribute":[{"type":"domain","value":"evil.example",
    "to_ids":true,"comment":"phishing kit host"}]}}' \
  https://misp.internal/events
```

Hygiene rules:

- Every attribute gets a first-seen date, a source tag, and a TLP.
- `to_ids` true only for indicators you would actually block on.
- Expire aggressively: IPs 30 days, domains 90 days, hashes 1 year,
  unless re-observed.
- Link events to MITRE galaxies (actor, technique) so analysts can
  pivot from IOC to TTP.

## 4. Scoring and aging

Not all IOCs deserve a block. Score on:

- Confidence: how sure is the source (confirmed malicious vs
  suspicious).
- Relevance: does it match your PIRs and your technology stack.
- Freshness: when was it last observed active.
- Corroboration: how many independent sources report it.

```python
#!/usr/bin/env python3
"""Simple IOC scorer: blocks only high-confidence, fresh, relevant IOCs."""
from datetime import datetime, timedelta

def score(ioc):
    s = 0
    s += {"confirmed": 40, "probable": 20, "possible": 5}[ioc["confidence"]]
    s += 20 if ioc["relevant_to_us"] else 0
    age_days = (datetime.utcnow() - ioc["last_seen"]).days
    s += max(0, 20 - age_days)          # freshness decays
    s += min(20, 10 * ioc["source_count"])  # corroboration
    return s

# Example: block at >= 70, hunt at >= 40, ignore below
```

Automate expiry: a daily job flips `to_ids` off for indicators past
their TTL and tags them expired. Stale blocks cause outages and teach
everyone to distrust the blocklist.

## 5. Correlate before you block

An IOC is only actionable if it touches your environment:

```bash
# Check a suspicious IP against 30 days of proxy logs before blocking
index=proxy dest_ip="198.51.100.23" earliest=-30d@d latest=@d
| stats count by user, dest_ip | sort -count

# Check a hash against EDR telemetry
index=edr file_hash="d41d8cd98f00b204e9800998ecf8427e" earliest=-90d@d latest=@d
| stats values(host) as hosts count
```

Decision matrix:

- Seen in our telemetry plus high confidence: block and hunt for
  related activity.
- Not seen plus high confidence: block at the perimeter, low priority
  hunt.
- Seen plus low confidence: investigate as a hunt, do not block yet.
- Not seen plus low confidence: store for correlation, no action.

## 6. Operationalizing intel

Turn intel into controls:

- Push high-confidence network IOCs to firewall, proxy, and DNS
  blocklists with expiry dates.
- Convert TTPs into Sigma rules (see the sigma-rules skill) rather
  than blocking single hashes that change daily.
- Write threat-informed hunts: "actor X uses rundll32 with this
  pattern; hunt our fleet for it."
- Brief the SOC with a one-page intel note: who, what TTPs, what to
  look for, what is already blocked.

Track intel-driven outcomes: detections added, hunts run, incidents
found because of intel. That is how the intel function justifies its
budget.

## 7. Sharing under TLP

Traffic Light Protocol governs redistribution:

- TLP:CLEAR: share freely.
- TLP:GREEN: share within your community (peers, ISAC).
- TLP:AMBER: share within your organization and with clients on a
  need-to-know basis.
- TLP:RED: named recipients only, no forwarding.

When you receive TLP:AMBER intel, your MISP sync and your SIEM
blocklist must not leak it into a public feed. Tag at ingest, enforce
at export. For STIX/TAXII sharing, mark objects with the TLP marking
definition and filter collections by marking.

## Edge cases

- Feed poisoning: a feed lists a legitimate CDN IP and you block it.
  Always check an IOC against your own telemetry and an allowlist of
  critical services before blocking.
- Duplicate intel across feeds inflates confidence. Deduplicate on
  value plus first-seen before counting corroboration.
- Intel about your own infrastructure (your IP in a blocklist):
  investigate as a possible compromise or misattribution, and file a
  delist request with evidence.
- TLP violations by recipients: watermark shared reports per
  recipient so leaks are traceable, and remind the community of the
  rules before cutting access.
- MISP sync conflicts: decide which instance is authoritative per
  feed and document it; two writers to the same event cause merge
  pain.
- Intel overload: cap the number of active blocking IOCs and review
  the tail monthly. Ten thousand stale blocks help nobody.

## Escalation

- Intel indicates an imminent threat to the organization (named in a
  ransomware leak post): treat as an incident, activate the relevant
  playbook, and hunt immediately.
- A blocking action causes a business outage: roll back the block,
  add the service to the allowlist with a ticket, and review the
  scoring threshold that let it through.
- Sharing dispute (a partner publishes your TLP:AMBER intel):
  contact them directly with the marking evidence, then escalate to
  the sharing community lead.
- Feed goes dark or degrades: fall back to the next feed serving the
  same PIR and note the coverage gap in the quarterly review.
- You need classified or law enforcement intel: that flows through
  official liaison channels, not OSINT. Engage your legal and
  leadership chain.

## Detection and defender view

Threat intel is a defensive multiplier, and attackers adapt to it:

- Attackers rotate IPs and domains faster than feeds update, so
  prioritize TTP-based detections over IOC blocks for agile actors.
- Attackers test their infrastructure against public blocklists and
  rotate what gets listed. Assume listed IOCs are already burned and
  hunt for the next iteration.
- Attackers plant false flags (other actors' tools, misleading
  language). Treat attribution as probable at best unless you have
  multiple independent lines of evidence.
- Defenders should feed internal findings back into intel: your
  incidents, your phishing samples, and your hunt results are intel
  for the next shift.
- Measure intel by outcomes (incidents found, dwell time reduced),
  not by volume (IOCs ingested). Ten good indicators beat ten
  thousand stale ones.

## Key references

- MITRE ATT&CK (actor and technique context): https://attack.mitre.org/
- MISP 2.5 documentation: https://www.misp-project.org/documentation/
- STIX 2.1 and TAXII 2.1 specifications (OASIS):
  https://oasis-open.github.io/cti-documentation/
- CISA advisories (AA reports): https://www.cisa.gov/news-events/cybersecurity-advisories
- FIRST TLP 2.0 definitions: https://www.first.org/tlp/
