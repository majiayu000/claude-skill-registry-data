---
name: building-zeek-analytics-for-hunting
description: 'Builds Zeek-based network hunting analytics by writing scripts and analyzing Zeek logs
  (conn, dns, http, ssl, files) to surface long connections, rare JA3s, suspicious downloads, and
  beaconing. Activates for requests to build Zeek analytics, write a Zeek hunting script, or analyze
  Zeek logs for threats.'
domain: cybersecurity
subdomain: threat-hunting
tags:
  - threat-hunting
  - zeek
  - network-analytics
  - ja3
  - beaconing
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1071
  - T1095
  - T1571
d3fend:
  - D3-NTA
  - D3-NTPM
references:
  - 'Zeek documentation (scripts and logs) — https://docs.zeek.org/'
  - 'Zeek log formats (conn/dns/http/ssl) — https://docs.zeek.org/en/master/logs/index.html'
---

# Building Zeek Analytics for Hunting

## When to Use

- You have Zeek logs (conn.log, dns.log, http.log, ssl.log, files.log) and want to build hunting
  analytics: long-lived connections, rare JA3 fingerprints, suspicious file downloads, and
  beaconing.
- You want repeatable detections expressed as Zeek scripts or log-analysis queries.

**Do not use** Zeek to actively probe hosts — it is passive analysis of captured/sensor traffic.

## Prerequisites

- Zeek logs in TSV or JSON (or a running Zeek sensor). The script analyzes exported logs.

## Workflow

### Step 1: Analyze a Zeek log for anomalies

```bash
python scripts/analyst.py analyze conn.log --kind conn
```

For `conn`, surfaces long-duration and high-byte connections; for `ssl`, counts JA3 rarity; for
`http`, flags executable/script downloads and rare user-agents; for `dns`, flags long/high-entropy
queries.

### Step 2: Express the logic as a Zeek script (optional)

Translate a confirmed pattern into a Zeek script using the appropriate event
(`connection_state_remove`, `ssl_established`, `http_reply`).

### Step 3: Confirm

Corroborate anomalies with destination reputation and other logs (pivot by `uid`).

### Step 4: Operationalize

Stage the Zeek script or scheduled log query as a durable detection.

## Validation

- The analyzer parses both TSV (`#fields`) and JSON Zeek logs.
- Surfaced anomalies match the chosen log kind's fields.
- JA3 rarity and long-connection logic are computed correctly.

## Pitfalls

- TSV header (`#fields`) parsing — column order varies by deployment.
- Backups/updates producing benign long/large connections.
- JA3 collisions across legitimate clients.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the analyzer.
- Zeek docs and log-format references (linked in frontmatter).
