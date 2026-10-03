---
name: smoke-test-auth
description: Smoke-test authentication/authorization — login (password/OAuth/SSO), JWT issue/validate/refresh, sessions, access control.
when_to_use: Reach for this to validate the auth subsystem only (login works, tokens valid, RBAC enforced). For the full suite use smoke-test-runner; for general API endpoints use smoke-test-api; for full signup→checkout journeys use smoke-test-critical-paths. (This verifies a live auth system; for implementing Clerk auth use using-clerk.)
allowed-tools: Read, Bash, Grep, Glob
---

# Smoke Test Auth Skill

**Quick Reference** - Load this first for fast context (~2KB)

## Mission

Execute comprehensive authentication and authorization smoke tests to validate login flows, token validation, session management, and access control during release workflows.

## Core Capabilities

- **Login Flow Testing**: Validate email/password, OAuth, SSO authentication
- **Token Validation**: Test JWT generation, validation, and refresh
- **Session Management**: Verify session creation, persistence, expiration
- **Access Control**: Test role-based and permission-based authorization
- **Password Operations**: Validate password reset and change flows
- **Multi-Factor Authentication**: Test 2FA/MFA flows

## Quick Start

```javascript
const { SmokeTestAuth } = require('./scripts/test-auth-flows.js');

const tester = new SmokeTestAuth({
  baseUrl: 'https://staging.example.com',
  testCredentials: {
    email: 'test@example.com',
    password: process.env.TEST_USER_PASSWORD
  }
});

const result = await tester.executeTests({
  environment: 'staging',
  tests: ['login', 'token-validation', 'protected-resource']
});

if (result.passed) {
  console.log('✅ Auth smoke tests passed');
}
```

## Performance SLAs

```javascript
const SLA_TARGETS = {
  login: 2000,              // Login: ≤2s
  tokenValidation: 100,     // Token validation: ≤100ms
  sessionCheck: 50,         // Session check: ≤50ms
  protectedResource: 500,   // Protected resource: ≤500ms
  logout: 1000              // Logout: ≤1s
};
```

## Pass/Fail Criteria

**Pass**: All auth tests must pass
- ✅ Login successful with valid credentials
- ✅ Login fails with invalid credentials
- ✅ Tokens generated and validated correctly
- ✅ Protected resources accessible with valid auth
- ✅ Protected resources blocked without auth

**Fail**: Any auth test failure blocks deployment
- ❌ Login fails with valid credentials
- ❌ Login succeeds with invalid credentials
- ❌ Token validation failures
- ❌ Unauthorized access to protected resources
- ❌ Authorized access blocked

## Need More Detail?

**Load**: `skills/smoke-test-auth/REFERENCE.md` (~10KB)
