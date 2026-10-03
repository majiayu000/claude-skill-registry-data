---
name: webapp-tls-ssl
description: "--| | banking.example.com | Chrome (cached) | Active | BLOCKED | | banking."
domain: cybersecurity
---

--|
| banking.example.com | Chrome (cached) | Active | BLOCKED |
| banking.example.com | Chrome (fresh) | Preloaded | BLOCKED |
| banking.example.com | Mobile App | Not Enforced | VULNERABLE |
| api.banking.example.com | Chrome (fresh) | Not Preloaded | VULNERABLE (first visit) |

### Recommendations
1. Implement TLS certificate pinning in the mobile banking app (Critical)
2. Submit api.banking.example.com to HSTS preload list separately
3. Add Content-Security-Policy: upgrade-insecure-requests header
4. Implement certificate transparency monitoring for the domain
```
