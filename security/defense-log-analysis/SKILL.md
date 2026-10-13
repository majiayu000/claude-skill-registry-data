---
name: defense-log-analysis
description: >
  Hunt for attacker activity in logs — auth, web, cloud, endpoint — with concrete queries and what
  to look for. Load for blue-team log/SIEM hunting, "analyze these logs", "find the attack", triage
  of auth/web/cloud logs, or building hunts. Signals: log files/SIEM, "what happened", IOC hunting.
domain: defense
type: technique
stability: learning
modes: [defense]
severity: info
mitre: [T1078, T1110, T1190, T1059]
tools: [splunk, elastic, jq, zeek, sigma]
schema_version: 1
---

# Log analysis & threat hunting

## When it applies
You have logs (or a SIEM) and need to find attacker activity — during triage, IR, or proactive
hunting. Pairs with each offensive skill: know the attack, hunt its footprint.

## Why it works
Attacks leave patterns across log sources. Hunting hypothesis-first (pick a technique → query its
signature → pivot on hits) beats scrolling. The same ATT&CK technique shows up in auth, web, cloud,
and endpoint logs in characteristic ways.

## Method — by source, what to look for
1. **Authentication**: spikes of 4625/failed logins then a 4624 success (brute force → `web-rate-limit-bypass`);
   logins from new geos/ASNs/impossible travel; new/again-enabled accounts; MFA fatigue (many prompts).
2. **Web/proxy**: bursts of 401/403/500 on one param (fuzzing), suspicious user-agents, long/encoded
   query strings (SQLi/LFI/SSTI payloads), spikes to `/admin`, `/api`, `.git`, requests to metadata IPs (SSRF).
3. **Cloud (CloudTrail/Audit)**: `ConsoleLogin`/`AssumeRole` anomalies, IAM changes
   (`CreateAccessKey`, `AttachUserPolicy`, `setIamPolicy`), `GetSecretValue` bursts, unusual regions,
   `iam:PassRole` + deploy (→ `cloud-iam-privesc`).
4. **Endpoint/process**: suspicious parents (`w3wp`→`cmd`), `certutil`/`curl` downloads, encoded
   PowerShell, new services/scheduled tasks (→ `defense-dfir-triage`).
5. **Pivot & timeline**: on a hit, pivot by user/IP/host and build a timeline; correlate across sources.

## Gotchas
- Baseline first — "anomalous" only means something against normal; know what normal looks like.
- Watch timezones/clock skew when correlating sources.
- Turn confirmed patterns into durable detections (→ `defense-detection-sigma`), don't just eyeball once.

## Verify success
A concrete finding: an attacker action identified with the query that found it, pivoted to scope
(accounts/hosts/timeline), and IOCs extracted for detection/containment.

## References
Splunk/Elastic search docs; MITRE ATT&CK; SANS hunting; Sigma for portable detections.
