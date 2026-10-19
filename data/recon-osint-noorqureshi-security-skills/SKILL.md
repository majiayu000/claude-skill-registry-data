---
name: recon-osint
description: >
  Passive OSINT to expand attack surface without touching the target: dorks, code/secret leaks,
  Shodan/Censys, cloud assets, employees. Load at recon start, on "OSINT", "google/github dorks",
  "shodan", or gathering intel on an org. Signals: org name, root domain, "find leaks/exposed".
domain: recon
type: technique
stability: learning
modes: [bugbounty]
severity: info
mitre: [T1593, T1596, T1589]
tools: [github-search, shodan, censys, google-dorks, trufflehog]
schema_version: 1
---

# Passive OSINT

## When it applies
Early recon, and anytime you want surface/intel without sending traffic to the target — safest,
often highest-signal (leaked keys, forgotten hosts, exposed services).

## Why it works
Organizations leak everywhere but their own site: search-engine indexes, public code, internet
scan databases, cloud metadata, and employee footprints. Aggregating these finds assets and
secrets the target doesn't know are exposed.

## Method
1. **Search dorks**: Google (`site: inurl: filetype: intitle:` for panels, configs, docs) and
   GitHub dorks (`org:target "api_key"`, `"target.com" password`) for code/secret leaks.
2. **Code leaks**: `trufflehog github --org=<org>`, gist/pastebin search — validate live keys (in scope).
3. **Internet scan DBs**: Shodan/Censys/FOFA by org/cert/favicon-hash to find exposed services,
   forgotten hosts, and origin IPs behind CDNs.
4. **Cloud & DNS assets**: CT logs, reverse-DNS, ASN ranges, bucket name guessing (→ `cloud-s3-exposure`).
5. **People/tech**: employees (LinkedIn) for username formats/phishing scope (if allowed), and
   job posts/stack sites for the tech stack.

## Gotchas
- Confirm everything you find is in program scope before *active* testing — OSINT surfaces out-of-scope acquisitions too.
- Report leaked secrets by location, validate minimally, never exfiltrate.
- Origin-IP discovery via Shodan/cert often bypasses the WAF later (→ `payloads-waf-bypass`).

## Verify success
New in-scope assets, exposed services, or validated leaked secrets — feeding active recon and hunting.

## References
Google Hacking DB; GitHub dorks lists; Shodan/Censys docs; trufflehog.
