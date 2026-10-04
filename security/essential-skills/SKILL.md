---
name: "Essential Skills — Deep Dive"
description: "PortSwigger deep-dive with exact payloads for every lab variant including zero-day techniques"
domain: cybersecurity
subdomain: bug-hunting
version: "1.0.0"
category: "bug-hunting/deep-dive-labs"
tags: [portswigger, deep-dive, exploitation, zero-day, lab-solutions]
mitre_attack: ["T1595.002"]
tools: [burp-suite, curl, sqlmap, ffuf, python]
difficulty: "advanced"
---

# Essential Skills — Deep Dive

> **Deep-Dive Lab Playbook** — Every PortSwigger lab variant with exact payloads,
> bypass techniques, and zero-day extensions. 🟢 Apprentice 🟡 Practitioner 🔴 Expert

## When to Use
- BSCP certification prep
- Real-world bug bounty hunting
- Building exploitation chains

## Prerequisites
- Burp Suite Professional
- Browser with proxy configured


## Workflow
### Phase 1: Reconnaissance
- Identify input vectors, parameters, and application behavior.
### Phase 2: Exploitation
- Apply standard lab payloads.
### Phase 3: Zero-Day Escalation
- Fuzz filters, bypass WAFs, and chain with other vulns.

## Lab Playbooks

### Lab 1: Discovering vulnerabilities quickly with targeted scanning 🟡 PRACTITIONER
Use Burp Scanner's "Scan defined insertion points" feature on specific parameters rather than running a full crawl-and-scan which takes too long. Send a single request to Intruder or Scanner and only select the specific parameter (e.g., inside an XML node) to scan for vulnerabilities like XXE or SQLi. 

Zero-day tip: Targeted scanning minimizes noise and risk of burning accounts compared to full automated scans.
---

### Lab 2: Scanning non-standard data structures 🟡 PRACTITIONER
When dealing with custom or non-standard data (like a bespoke binary format or deep JSON encoding), use Burp extensions like JSON Web Tokens (JWT) or build a custom BApp. If standard insertion points don't work, use the "Bypass WAF" or "Hackvertor" extensions to auto-encode scanner payloads before they leave Burp.

Zero-day tip: Often, applications correctly sanitize standard form-data but fail to apply the same sanitization logic to Base64-encoded or custom-delimited data structures.
---


## Key Concepts
| Concept | Description |
|---------|-------------|
| PortSwigger Vectors | Standardized approaches to vulnerability classes. |
| Payload Encoding | Modifying payloads to bypass basic string matching WAFs. |


## Output Format
```
Vulnerability Deep-Dive Report
==============================
Target Vector: [Endpoint]
Bypass Technique: [Explanation of bypass]
Payload Used: [Payload]
Impact Explanation: [Impact]
```

## 🔵 Blue Team
- Deploy robust WAF rules to detect anomalies.
- Monitor logs for unusual access patterns.

## 🛡️ Remediation & Mitigation Strategy
- **Input Validation:** Sanitize and strictly type-check all inputs.
- **Least Privilege:** Constrain component execution bounds.


## 📚 Shared Resources
> For cross-cutting methodology applicable to all vulnerability classes, see:
> - [`_shared/references/elite-chaining-strategy.md`](../_shared/references/elite-chaining-strategy.md) — Exploit chaining methodology and high-payout chain patterns
> - [`_shared/references/elite-report-writing.md`](../_shared/references/elite-report-writing.md) — HackerOne-optimized report writing, CWE quick reference
> - [`_shared/references/real-world-bounties.md`](../_shared/references/real-world-bounties.md) — Verified disclosed bounties by vulnerability class

## References
- [PortSwigger Labs](https://portswigger.net/web-security/all-labs)
