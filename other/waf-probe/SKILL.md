---
name: waf-probe
description: Dynamically tests and adjusts TLS JA3 signatures and headers to bypass Web Application Firewalls (e.g., Cloudflare, Datadome, Akamai).
---

# WAF Probe Skill

This skill allows Hermes to rapidly iterate through network-level evasion parameters when target sites deploy new blocking rules. If the standard backend pool starts encountering a high rate of HTTP 403s or invisible captchas, this skill is invoked to discover a new baseline.

## How it works

When invoked, the WAF Probe:
1. Loads the target site (e.g., Joe Fortune, Ignition) using `httpcloak-forwarder.ts` or native TLS masking.
2. Iterates over known TLS JA3 signatures (`chrome-120-win`, `chrome-114-mac`, etc.).
3. Tests variations of `sec-ch-ua` headers to ensure they mathematically correlate with the selected JA3 cipher suite.
4. Monitors the response headers (looking for `cf-ray`, `Set-Cookie: datadome=`) and response codes (200 OK vs 403 Forbidden).
5. Promotes the first successful TLS/Header combination to the primary profile.

## Triggering

Run `/goal Perform a WAF probe on Joe Fortune to find a working TLS profile`.
Hermes will also autonomously execute this if the success rate drops below the configured minimum threshold in `ops-orchestrator.ts`.

## Constraints
- **Strict Isolation**: Execute all probes through isolated proxy circuits to prevent mass IP banning during the probing phase.
- **Verification**: Always confirm the bypass by navigating completely to the login page and ensuring the username/password fields are present in the DOM (not just checking for HTTP 200).
