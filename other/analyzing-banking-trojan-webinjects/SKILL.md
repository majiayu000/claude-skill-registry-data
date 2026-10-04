---
name: analyzing-banking-trojan-webinjects
description: 'Analyzes banking trojan webinject configurations to extract targeted institutions,
  injected JavaScript/HTML, and data-theft hooks, mapping the fraud workflow. Activates for
  requests to analyze banking trojan webinjects, parse a webinject config, or map targeted banks
  and credential-theft injections.'
domain: cybersecurity
subdomain: malware-analysis
tags:
  - malware-analysis
  - banking-trojan
  - webinject
  - fraud
  - credential-theft
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1185
  - T1557
  - T1056.001
d3fend:
  - D3-SDA
  - D3-DA
references:
  - 'MITRE ATT&CK T1185 Browser Session Hijacking — https://attack.mitre.org/techniques/T1185/'
  - 'Zeus/SpyEye webinject format (public malware research) — https://attack.mitre.org/software/S0259/'
---

# Analyzing Banking Trojan Webinjects

## When to Use

- You have a banking trojan webinject config (Zeus/Gozi/Dridex-style `set_url`/`data_before`/
  `data_inject` blocks) and want to extract targeted institutions and injected code.
- You are mapping the web-fraud workflow (form-grabbing, fake fields, MFA interception).

**Do not use** this to deploy or test injects against live banking sites. This skill parses the
config statically and executes nothing.

## Prerequisites

- The decoded webinject config text (decrypt the config first if needed).

## Safety & Handling

- Treat injected JS/HTML as malicious; do not render it. Defang any exfil URLs.

## Workflow

### Step 1: Parse webinject blocks

```bash
python scripts/analyst.py parse webinjects.txt
```

Parses `set_url`/`data_before`/`data_inject`/`data_after` blocks into structured entries with the
targeted URL pattern and the injected snippet.

### Step 2: Extract targets and exfil endpoints

List targeted institution URL patterns and any exfil endpoints referenced by the injected code.

### Step 3: Classify the injection technique

Identify form-grabbing, fake additional fields (SSN, PIN, card), and MFA/OTP interception from the
injected markup/JS.

### Step 4: Defang and report

Defang URLs and summarize targeted banks and theft techniques.

## Validation

- Each webinject block is parsed into target URL + injection.
- Exfil endpoints in injected code are extracted and defanged.
- Injection techniques are classified from the snippet content.

## Pitfalls

- Encrypted/packed configs needing decryption before parsing.
- Wildcard URL patterns matching broadly — note the scope.
- Obfuscated injected JS hiding the true exfil endpoint.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the parser.
- ATT&CK T1185 and webinject format references (linked in frontmatter).
