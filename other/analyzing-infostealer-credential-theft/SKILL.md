---
name: analyzing-infostealer-credential-theft
description: 'Analyzes infostealer samples by mapping the browser, credential store, wallet, and
  application paths they target, and the exfiltration channel used, from static strings and
  behavior. Activates for requests to analyze an infostealer, identify targeted credential stores,
  or map stealer collection and exfiltration behavior.'
domain: cybersecurity
subdomain: malware-analysis
tags:
  - malware-analysis
  - infostealer
  - credential-theft
  - exfiltration
  - triage
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1555.003
  - T1539
  - T1005
d3fend:
  - D3-FAPA
  - D3-DA
references:
  - 'MITRE ATT&CK T1555.003 Credentials from Web Browsers — https://attack.mitre.org/techniques/T1555/003/'
  - 'MITRE ATT&CK T1539 Steal Web Session Cookie — https://attack.mitre.org/techniques/T1539/'
---

# Analyzing Infostealer Credential Theft

## When to Use

- You have an infostealer sample and need to enumerate what it targets: browser credential/cookie
  stores, crypto wallets, FTP/VPN/messaging app configs, and the exfil channel.
- You are building detections from the file paths and endpoints a stealer references.

**Do not use** this to recover credentials yourself — it characterizes what the malware targets
from inert static analysis.

## Prerequisites

- The sample (read inertly), optionally with extracted strings.

## Safety & Handling

- Read bytes statically; defang exfil endpoints; never run the stealer.

## Workflow

### Step 1: Map targeted artifacts

```bash
python scripts/analyst.py profile sample.bin
```

Matches references to known browser paths (`Login Data`, `Cookies`, `Web Data`), wallet
directories, app config paths, and credential APIs, grouped by category.

### Step 2: Identify exfiltration channel

Detects HTTP(S) POST endpoints, Telegram bot tokens, Discord webhooks, and FTP/SMTP usage in
strings.

### Step 3: Build the target/exfil profile

Summarize targeted stores and the exfil channel, mapping to ATT&CK.

### Step 4: Defang and report

Defang endpoints and produce IOCs for detection.

## Validation

- Targeted artifacts are grouped (browsers, wallets, apps, system credential stores).
- The exfil channel is identified with a defanged endpoint where present.
- Findings map to ATT&CK credential-access/collection/exfiltration techniques.

## Pitfalls

- Generic browser paths can appear in benign tools — corroborate with theft behavior.
- Missing wallet/app targets that use obfuscated path strings.
- Reporting live exfil endpoints (webhooks, bot tokens) without defanging.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the profiler.
- ATT&CK T1555.003 and T1539 (linked in frontmatter).
