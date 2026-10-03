---
name: threat-intel-fusion
description: Threat intelligence fusion skill for collecting, normalizing, deduplicating, enriching, and operationalizing IOCs and TTPs from OTX, MISP, abuse.ch, VirusTotal, Shodan, GreyNoise, Censys, CISA KEV, NVD, vendor blogs, and internal telemetry. Use to build STIX/TAXII feeds, ATT&CK-mapped actor profiles, prioritized blocklists, and detection-ready intel packages.
---

# Threat Intel Fusion

## Operating Rules

- Separate observation, assessment, and recommendation. Tag every claim with source, date, and confidence.
- Prefer structured formats: STIX 2.1 objects, MISP events, ATT&CK technique IDs, CVE IDs, CPE strings.
- Decay IOC value over time; mark sightings, first/last seen, and TLP.

## Fusion Workflow

1. Collect: pull feeds with idempotent connectors; record raw payloads with hash and timestamp.
2. Normalize: map to STIX SDOs and SROs (`indicator`, `malware`, `intrusion-set`, `attack-pattern`, `relationship`).
3. Deduplicate: canonical-form domain/url/hash; merge by `id` + `pattern`, keep all sightings.
4. Enrich: passive DNS, WHOIS, ASN, geo, VT, GreyNoise tags, sandbox verdicts, KEV/EPSS scores.
5. Prioritize: score by exploitability, exposure in our environment, actor relevance, and decay.
6. Operationalize: emit firewall/EDR/SIEM-ready artifacts plus Sigma rules and hunt queries.

## Actor Profiling

- Aliases, motivations, sectors, geographies, observed TTPs (ATT&CK), tooling, infrastructure patterns, recent campaigns, and likely next moves with confidence.

## Output Contract

- `feeds/`: raw + normalized snapshots.
- `iocs.stix.json`: deduped STIX bundle with relationships.
- `priority.csv`: `indicator, score, reason, action, ttl`.
- `actors/<name>.md`: profile with sources.
- `detections/`: Sigma, YARA, Suricata, KQL, SPL exports.
- `report.md`: executive summary, what changed, what to action this week.
