---
name: net-attack-mitm
description: "Net Attack Mitm."
domain: cybersecurity
---

|
| HTTPS Redirect | PASS | HTTP requests redirect to HTTPS with 301 |
| HSTS Header | PASS | max-age=31536000; includeSubDomains; preload |
| SSL Stripping (Browser) | BLOCKED | HSTS prevents downgrade in Chrome/Firefox |
| SSL Stripping (Thick Client) | VULNERABLE | Client follows HTTP redirect without HSTS |
| Cert Pinning (Browser) | N/A | Standard CA validation only |
| Cert Pinning (Thick Client) | VULNERABLE | Accepts MITM CA without validation |
| IDS Detection | PASS | Snort generated ARP spoof alert in 12 seconds |

### Recommendations
1. Implement certificate pinning in the thick client (high priority)
2. Add HSTS preload list submission for the domain
3. Enable DAI on access-layer switches for Layer 2 protection
4. Configure application to reject connections from non-pinned certificates
```
