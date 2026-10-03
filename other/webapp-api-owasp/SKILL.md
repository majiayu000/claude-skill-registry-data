---
name: webapp-api-owasp
description: "Webapp Api Owasp."
domain: cybersecurity
---

|
| API1: BOLA | VULNERABLE | Critical | /api/v1/orders/{id} - IDOR confirmed |
| API2: Broken Auth | VULNERABLE | High | No rate limit on /auth/login |
| API3: BOPLA | VULNERABLE | High | User role modifiable via mass assignment |
| API4: Resource Consumption | VULNERABLE | Medium | No pagination limit enforced |
| API5: Function Level Auth | PASS | - | Admin endpoints properly restricted |
| API6: Unrestricted Sensitive Flows | VULNERABLE | Medium | OTP endpoint lacks rate limiting |
| API7: SSRF | PASS | - | URL parameters properly validated |
| API8: Misconfiguration | VULNERABLE | Medium | Verbose stack traces in error responses |
| API9: Improper Inventory | VULNERABLE | Low | API v1 still accessible without docs |
| API10: Unsafe Consumption | NOT TESTED | - | No third-party API integrations found |

### Critical Finding: BOLA on Orders API
Authenticated users can access any order by iterating order IDs.
Tested range: 1-1000, 847 valid orders accessible.
PII exposure: names, addresses, payment details.
```
