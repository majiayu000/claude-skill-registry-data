---
name: "Authentication — Complete Deep Dive"
description: "Complete PortSwigger deep-dive with exact payloads for every lab variant including zero-day techniques"
domain: cybersecurity
subdomain: bug-hunting
version: "1.0.0"
category: "bug-hunting/deep-dive-labs"
tags: [portswigger, deep-dive, exploitation, zero-day, lab-solutions]
mitre_attack: ["T1110"]
tools: [burp-suite, curl, sqlmap, ffuf, python, hashcat, ysoserial]
difficulty: "advanced"
---

# Authentication — Complete Deep Dive

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

### Lab 1: Username enum different responses 🟢 APPRENTICE
Burp Intruder with username wordlist. Check response length/content difference: `Invalid username` vs `Incorrect password`.
---

### Lab 2: 2FA simple bypass 🟢 APPRENTICE
After login, skip `/login2` (2FA page) and navigate directly to `/my-account`.
---

### Lab 3: Password reset broken logic 🟢 APPRENTICE
```http
POST /forgot-password?temp-forgot-password-token=TOKEN HTTP/1.1

temp-forgot-password-token=TOKEN&username=carlos&new-password-1=hacked&new-password-2=hacked
```
Change `username` to victim. Token validation doesn't check user ownership.
---

### Lab 4: Subtly different responses 🟡 PRACTITIONER
Check for trailing period: `Invalid username or password` vs `Invalid username or password.`
---

### Lab 5: Response timing 🟡 PRACTITIONER
Long password → longer response time for valid usernames (bcrypt hash computed). Use `X-Forwarded-For: 1.1.1.§1§` to bypass IP lock.
---

### Lab 6: Broken brute-force IP block 🟡 PRACTITIONER
Login with valid creds every 2 attempts to reset the IP counter. Alternate: valid→attack→valid→attack.
---

### Lab 7: Username enum via account lock 🟡 PRACTITIONER
Locked account = account exists. Send 5 attempts for each username. Locked response = valid user.
---

### Lab 8: 2FA broken logic 🟡 PRACTITIONER
```http
POST /login2 HTTP/1.1
Cookie: verify=carlos

mfa-code=§1234§
```
Change `verify` cookie to victim, brute force 4-digit MFA code.
---

### Lab 9: Stay-logged-in cookie crack 🟡 PRACTITIONER
Cookie = Base64(`username:MD5(password)`). Decode, crack MD5 hash.
---

### Lab 10: Offline password cracking 🟡 PRACTITIONER
Steal cookie via XSS → decode Base64 → crack MD5 hash offline with hashcat.
---

### Lab 11: Password reset poisoning middleware 🟡 PRACTITIONER
```http
POST /forgot-password HTTP/1.1
X-Forwarded-Host: EXPLOIT-SERVER

username=carlos
```
Reset link sent to carlos uses your host → steal reset token.
---

### Lab 12: Brute-force via password change 🟡 PRACTITIONER
Password change function reveals different errors for wrong vs correct current password. Brute force current password via this oracle.
---

### Lab 13: Multiple credentials per request 🔴 EXPERT
```json
{"username":"carlos","password":["123456","password","qwerty",...]}
```
Send password array — server tries all in one request, bypassing rate limiting.
---

### Lab 14: 2FA brute force 🔴 EXPERT
Macro in Burp: auto-login → auto-get 2FA page → brute force code → repeat. Set session handling rule to use macro.
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
