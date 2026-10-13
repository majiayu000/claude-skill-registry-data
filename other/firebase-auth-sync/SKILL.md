---
name: firebase-auth-sync
description: 'Implement and debug HIVMeet authentication flow between Firebase and Django JWT. Use for token exchange, Firebase token verification, user sync, middleware behavior, and session integrity.'
argument-hint: 'Describe auth flow step that fails (exchange, verify, sync, refresh, logout) and observed symptom.'
user-invocable: true
---

# Firebase Auth and JWT Sync

## Purpose
Keep identity flows consistent across Firebase Auth and Django backend tokens to avoid ghost users, auth drift, and session breakage.

## Use When
- Implementing firebase-exchange endpoints
- Debugging invalid token or user sync issues
- Fixing logout/refresh behavior
- Hardening middleware authentication behavior

## Mandatory Workflow

### 1. Auth Flow Mapping
- Map sequence: Firebase token -> backend verify -> Django user sync -> JWT issue -> protected endpoint access
- Identify exact failing step and expected artifact at each step

### 2. Verification and Sync Guarantees
- Verify Firebase token with server-side SDK
- Ensure user lookup/create is deterministic by firebase UID
- Ensure user profile bootstrap behavior is idempotent

### 3. JWT Session Rules
- Confirm access/refresh issuance policy
- Confirm refresh rotation/blacklist rules if enabled
- Confirm logout blacklists refresh token and invalidates expected session paths

### 4. Error Handling and Contract
- Map auth failures to stable statuses (400/401/403)
- Return safe error messages without exposing token internals
- Keep response payload aligned with contract

### 5. Security and Logging
- Never log full tokens
- Log contextual identifiers safely (user id if available, request path, reason code)
- Validate authentication middleware does not bypass checks

### 6. Regression Validation
- Test successful exchange and protected endpoint access
- Test expired/invalid Firebase token path
- Test refresh and logout behavior

### 7. Output Contract
1. Failing auth stage and root cause
2. Sync and token fixes applied
3. Contracted status behavior
4. Security/logging checks
5. Tests executed and remaining risk

## Quality Gates
- No duplicate user creation for same Firebase identity
- No success path without verified token provenance
- No token material leaked in logs
