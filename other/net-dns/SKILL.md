---
name: net-dns
description: "--| | Zone Transfer | 347 | | Passive (subfinder + amass) | 89 | | Active Brute Force | 12 | | **Total Unique** | **412** |  ### Critical Findings 1."
domain: cybersecurity
---

--|
| Zone Transfer | 347 |
| Passive (subfinder + amass) | 89 |
| Active Brute Force | 12 |
| **Total Unique** | **412** |

### Critical Findings
1. **Zone Transfer Allowed** (High): ns2.example.com allows AXFR from any source
2. **Internal IP Disclosure** (Medium): 15 subdomains resolve to RFC1918 addresses
3. **Exposed Staging Environment** (High): staging.example.com accessible with default credentials
4. **Missing DMARC Policy** (Medium): No DMARC record found, enabling email spoofing
5. **Weak SPF Record** (Low): SPF uses ~all (soft fail) instead of -all (hard fail)
```
