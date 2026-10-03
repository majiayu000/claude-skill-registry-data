---
name: webapp-auth-bac
description: "Webapp Auth Bac."
domain: cybersecurity
---

--|
| GET /admin/dashboard | 200 | 200 | 200 | 302 | Admin only | FAIL |
| DELETE /api/users/{id} | 200 | 200 | 200 | 401 | Admin only | FAIL |
| GET /api/users/other/profile | 200 | 200 | 200 | 401 | Own only | FAIL |
| PUT /api/users/other/settings | 200 | 200 | 200 | 401 | Own only | FAIL |
| GET /api/org/other-tenant | 200 | 200 | 200 | 401 | Same tenant | FAIL |

### Critical Findings
1. **Vertical Escalation**: Regular users can access /admin/* endpoints
2. **Horizontal IDOR**: Users can read/modify other users' profiles
3. **Tenant Isolation**: Cross-tenant data access via header manipulation
4. **Mass Assignment**: Role escalation via profile update endpoint

### Impact
- Complete administrative access for any authenticated user
- Full user data access across all accounts (15,000+ users)
- Cross-tenant data breach affecting 200+ organizations
- Account takeover via profile modification

### Recommendation
1. Implement server-side authorization checks on every endpoint
2. Use a centralized authorization middleware/framework
3. Enforce object-level authorization (verify ownership before access)
4. Validate tenant context server-side, never from client headers
5. Use allowlists for mass assignment (only permit expected fields)
6. Implement audit logging for all access control decisions
```
