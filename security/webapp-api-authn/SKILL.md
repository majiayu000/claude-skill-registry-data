---
name: webapp-api-authn
description: "| | **Broken Authentication** | OWASP API2:2023 - weaknesses in authentication mechanisms that allow attackers to assume identities of legitimate users | | **JWT (JSON Web Token)** | Self-contained token format with header."
domain: cybersecurity
---

|
| **Broken Authentication** | OWASP API2:2023 - weaknesses in authentication mechanisms that allow attackers to assume identities of legitimate users |
| **JWT (JSON Web Token)** | Self-contained token format with header.payload.signature structure, used for stateless API authentication |
| **Token Revocation** | Server-side mechanism to invalidate tokens before their expiration, critical for logout and password change |
| **Credential Stuffing** | Automated attack using leaked username/password pairs against authentication endpoints |
| **Account Enumeration** | Determining valid usernames through different error messages or response times for valid vs invalid accounts |
| **Refresh Token Rotation** | Security practice where each use of a refresh token generates a new one, preventing token reuse attacks |

## Tools & Systems

- **Burp Suite JWT Editor**: Extension for decoding, editing, and re-signing JWT tokens with various attack modes
- **jwt_tool**: Python tool for JWT testing with 12+ attack modes including alg:none, key confusion, and JWKS spoofing
- **hashcat**: GPU-accelerated password cracker supporting JWT HMAC secret brute-forcing (mode 16500)
- **Hydra**: Network login brute-forcer supporting HTTP form-based and API authentication testing
- **Nuclei**: Template-based scanner with authentication bypass detection templates

## Common Scenarios

### Scenario: SaaS Platform API Authentication Assessment

**Context**: A SaaS platform uses JWT tokens for API authentication. The JWT is issued upon login and used for all subsequent API calls. A refresh token mechanism is also implemented.

**Approach**:
1. Authenticate and capture the JWT: algorithm is HS256, expiration is 7 days, payload contains user role
2. Test alg:none bypass: server rejects the token (secure)
3. Brute force the HMAC secret: discover the secret is "company-jwt-secret-2023" (found using hashcat with custom wordlist)
4. Forge a JWT with admin role using the discovered secret: gain admin access to all endpoints
5. Test token revocation: tokens remain valid after logout and password change (no blacklist)
6. Test refresh token: refresh token has no expiration and can be reused indefinitely
7. Find that the password reset endpoint returns different messages for valid vs invalid emails
8. Discover that the `/health` and `/metrics` endpoints are accessible without authentication

**Pitfalls**:
- Only testing the login endpoint and missing authentication weaknesses in password reset, MFA, and token refresh flows
- Not checking if the JWT secret is the same across all environments (dev, staging, production)
- Ignoring the token lifetime: a 7-day JWT with no revocation means a stolen token is valid for a week
- Not testing for token leakage in server logs, URL parameters, or error messages

## Output Format

```
## Finding: JWT HMAC Secret Brute-Forceable and Token Not Revocable

**ID**: API-AUTH-001
**Severity**: Critical (CVSS 9.1)
**OWASP API**: API2:2023 - Broken Authentication
**Affected Components**:
  - POST /api/v1/auth/login (token issuance)
  - All authenticated endpoints (token validation)
  - POST /api/v1/auth/logout (ineffective)

**Description**:
The API uses HS256-signed JWT tokens with a brute-forceable secret
("company-jwt-secret-2023"). An attacker who discovers this secret can
forge tokens for any user with any role, including admin. Additionally,
tokens are not revocable - logout does not invalidate the token server-side,
and the 7-day expiration means stolen tokens remain valid for extended periods.

**Attack Chain**:
1. Capture any valid JWT from authenticated session
2. Brute force the HMAC secret using hashcat: hashcat -a 0 -m 16500 jwt.txt wordlist.txt
3. Secret recovered in 3 minutes: "company-jwt-secret-2023"
4. Forge admin JWT: modify "role" claim to "admin", re-sign with discovered secret
5. Access admin endpoints: GET /api/v1/admin/users returns all 50,000 user accounts

**Remediation**:
1. Replace HS256 with RS256 using a 2048-bit RSA key pair
2. Use a cryptographically random secret of at least 256 bits if HMAC must be used
3. Implement token blacklisting using Redis for logout and password change events
4. Reduce token TTL to 15 minutes with refresh token rotation
5. Add `iss` and `aud` claims validation to prevent token misuse across services
```
