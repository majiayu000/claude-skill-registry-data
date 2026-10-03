---
name: net-ids-snort
description: "--| | Attempted Recon | 342 | 1:2100498 (ICMP ping) | | Trojan Activity | 12 | 1:1000001 (Reverse shell) | | Policy Violation | 87 | 1:1000004 (FTP cleartext) | | Web Application Attack | 23 | 1:2100654 (SQL injection) |  ### Tuning Actions Taken - Suppressed SID 2100498 for 10."
domain: cybersecurity
---

--|
| Attempted Recon | 342 | 1:2100498 (ICMP ping) |
| Trojan Activity | 12 | 1:1000001 (Reverse shell) |
| Policy Violation | 87 | 1:1000004 (FTP cleartext) |
| Web Application Attack | 23 | 1:2100654 (SQL injection) |

### Tuning Actions Taken
- Suppressed SID 2100498 for 10.10.1.100 (monitoring server legitimate ICMP)
- Thresholded SID 1000004 to 5 alerts per source per hour
- Added 3 custom rules for PHI exfiltration detection
```
