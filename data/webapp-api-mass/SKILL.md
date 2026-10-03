---
name: webapp-api-mass
description: "--|"
domain: cybersecurity
---
--|
| 1 | PATCH /api/users/me | role | "user" | "admin" | Privilege Escalation |
| 2 | POST /api/orders | price | 99.99 | 0.01 | Financial Loss |
| 3 | PATCH /api/users/me | email_verified | false | true | Verification Bypass |

### Remediation
- Implement allowlist (strong_parameters) for all model update operations
- Use DTOs/ViewModels to decouple API input from database models
- Apply field-level authorization checks on sensitive attributes
- Log and alert on attempts to modify restricted fields
```
