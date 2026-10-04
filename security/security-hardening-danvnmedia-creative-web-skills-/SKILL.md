---
name: security-hardening
description: Use for auth, authorization, tenant/object access, sensitive data, uploads, secrets, provider keys, billing, destructive operations, or security findings; require threat boundaries, negative tests, exploit-path verification, and safe secret handling.
---
# Security Hardening

1. Identify assets, actors, trust boundaries, privileges, and destructive/sensitive actions.
2. Enforce authz server-side at the object/tenant/action boundary; never trust client visibility.
3. Validate and bound body/file/query sizes at trust boundaries.
4. Keep provider/API keys server-side and redact them from logs/evidence.
5. Minimize sensitive data and make retention/export/deletion behavior explicit.
6. Convert important boundaries into negative tests: cross-user/tenant IDs, non-admin admin route, duplicate request, expired session, malformed upload, direct API bypass.
7. Treat a vulnerability as a candidate until an exploit/data-loss/authorization path and preconditions are supported. Try to disprove it before assigning severity.
8. Record fresh `security-negative` evidence for security-sensitive tasks.
