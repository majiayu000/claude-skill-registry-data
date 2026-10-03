---
name: webapp-api-bfla
description: "Webapp Api Bfla."
domain: cybersecurity
---

|
| **BFLA** | Broken Function Level Authorization (OWASP API5:2023) - regular users can invoke administrative or privileged API functions without proper authorization checks |
| **Vertical Privilege Escalation** | Accessing functions or data restricted to a higher privilege level, such as regular user accessing admin endpoints |
| **RBAC** | Role-Based Access Control - authorization model where permissions are assigned to roles and roles are assigned to users |
| **Function-Level Authorization** | Access control checks that verify whether the authenticated user has permission to invoke a specific API function |
| **Admin Endpoint** | API endpoints intended only for administrative users, typically managing users, settings, audit logs, and system configuration |
| **Forced Browsing** | Directly accessing URLs that are not linked in the application but exist on the server, bypassing UI-level access restrictions |

## Tools & Systems

- **Burp Suite Professional**: Intercept requests as admin, then replay with regular user token to test function-level authorization
- **OWASP ZAP**: Forced Browse scanner to discover hidden administrative endpoints and test access control
- **Autorize (Burp Extension)**: Automated BFLA detection by replaying admin requests with regular user credentials
- **ffuf**: Endpoint discovery tool: `ffuf -u https://api.example.com/api/v1/FUZZ -w admin-endpoints.txt -H "Authorization: Bearer user_token"`
- **Nuclei**: Template-based scanner with BFLA detection templates for common frameworks

## Common Scenarios

### Scenario: SaaS Multi-Tenant API BFLA Assessment

**Context**: A SaaS platform has user, moderator, and admin roles. The API serves a React frontend that conditionally renders admin features based on the user's role. The backend API should enforce the same restrictions independently.

**Approach**:
1. Map admin endpoints from the frontend JavaScript bundle: search for `/admin/`, `/manage/`, and role-check conditionals
2. Discover 12 admin endpoints including user management, billing, feature flags, and audit logs
3. Test each admin endpoint with regular user token:
   - `GET /api/v1/admin/users` returns 200 with all user data (BFLA - read)
   - `PUT /api/v1/admin/users/1002/role` accepts role change (BFLA - write)
   - `DELETE /api/v1/audit/logs` returns 200 (BFLA - destructive)
4. Test method-based bypass: `GET /api/v1/admin/settings` returns 403, but `PUT /api/v1/admin/settings` returns 200
5. Find that the moderator role can access all admin endpoints except `DELETE /api/v1/admin/billing`
6. Discover `/api/v2/admin/users` exists without any authorization (shadow API version)

**Pitfalls**:
- Only testing GET requests on admin endpoints while missing BFLA in POST/PUT/DELETE methods
- Not discovering admin endpoints because they are not linked in the UI (requires endpoint enumeration)
- Assuming RBAC is enforced consistently because one admin endpoint returned 403
- Missing BFLA in internal/undocumented API endpoints not listed in the OpenAPI specification
- Not testing with all available role levels (moderator may have partial admin access)

## Output Format

```
## Finding: Regular Users Can Access Admin User Management API

**ID**: API-BFLA-001
**Severity**: Critical (CVSS 9.8)
**OWASP API**: API5:2023 - Broken Function Level Authorization
**Affected Endpoints**:
  - GET /api/v1/admin/users (read all users)
  - PUT /api/v1/admin/users/{id}/role (change user roles)
  - DELETE /api/v1/audit/logs (delete audit trail)
  - PUT /api/v1/admin/settings (modify system config)

**Description**:
The API does not enforce function-level authorization on administrative
endpoints. A regular user can directly call admin API endpoints and
execute administrative functions including user management, role changes,
system configuration, and audit log deletion. The frontend hides admin
features based on role, but the backend API does not enforce the same
restrictions.

**Proof of Concept**:
1. Authenticate as regular user: POST /api/v1/auth/login
2. Call admin endpoint: GET /api/v1/admin/users -> 200 OK (returns all 50,000 users)
3. Elevate own role: PUT /api/v1/admin/users/me/role {"role":"admin"} -> 200 OK
4. Delete audit logs: DELETE /api/v1/audit/logs -> 204 No Content

**Impact**:
Any authenticated user can take full administrative control of the
platform, access all user data, modify roles, change system configuration,
and delete audit logs to cover their tracks.

**Remediation**:
1. Implement RBAC middleware that checks user role before executing any admin function
2. Apply authorization at the route/controller level, not just the frontend
3. Use decorator/annotation-based authorization (e.g., @RequireRole("admin"))
4. Add automated BFLA tests to the CI/CD pipeline that test every endpoint with every role
5. Implement immutable audit logging that admin users cannot delete
```
