---
name: webapp-auth-jwt
description: "Webapp Auth Jwt."
domain: cybersecurity
---

|
| **Algorithm Confusion** | Attack where the server trusts the alg header in the JWT, allowing an attacker to switch from RS256 to HS256 and sign with the public key as the HMAC secret |
| **alg:none Attack** | Setting the JWT algorithm to "none" to bypass signature verification entirely, if the library does not enforce algorithm selection |
| **JKU Injection** | Manipulating the jku (JWK Set URL) header to point to an attacker-controlled JWKS endpoint, allowing the attacker to supply their own signing keys |
| **KID Injection** | Injecting SQL, path traversal, or URL payloads into the kid (Key ID) header parameter to manipulate key selection or read arbitrary files |
| **Key Confusion** | Using the RSA public key as the HMAC secret when the server incorrectly switches from asymmetric to symmetric verification |
| **JWKS (JSON Web Key Set)** | A JSON structure containing the public keys used by the server to verify JWT signatures, typically hosted at a well-known endpoint |

## Tools & Systems

- **jwt_tool**: Python-based JWT testing toolkit with 12+ attack modes including alg confusion, none bypass, and kid injection
- **Burp Suite JWT Editor**: Extension for decoding, editing, and re-signing JWTs with algorithm manipulation capabilities
- **hashcat (mode 16500)**: GPU-accelerated HMAC secret brute-forcing for HS256/HS384/HS512-signed JWTs
- **John the Ripper**: CPU-based JWT secret cracking with wordlist and rule-based attacks
- **jwt.io**: Online JWT decoder and debugger for quick token analysis

## Common Scenarios

### Scenario: Algorithm Confusion on Banking API

**Context**: A banking API uses RS256-signed JWTs for authentication. The JWKS endpoint is publicly accessible. The API handles financial transactions requiring high assurance authentication.

**Approach**:
1. Obtain a valid JWT by authenticating as a regular user
2. Extract the RSA public key from the JWKS endpoint at `/.well-known/jwks.json`
3. Create a new JWT with `"alg": "HS256"` header and sign it using the RSA public key as the HMAC secret
4. Send the forged token to `GET /api/v1/users/me` - server accepts it (algorithm confusion confirmed)
5. Modify the payload to set `"role": "admin"` and `"sub": "admin@bank.com"` - sign with the public key
6. Access admin endpoints: `GET /api/v1/admin/transactions` returns all transaction history
7. Test alg:none: rejected by the server (partial mitigation)
8. Test kid injection with SQL payload: kid parameter is used in a SQL query to look up keys, enabling SQL injection

**Pitfalls**:
- Using the wrong format of the public key as the HMAC secret (PEM with/without headers, DER, raw bytes)
- Not trying multiple public key formats when the first one does not produce a valid signature
- Assuming the alg:none defense means algorithm confusion is also mitigated
- Not testing kid injection vectors when the kid parameter is present in the JWT header
- Missing JKU/x5u header injection when the server fetches keys from URLs

## Output Format

```
## Finding: JWT Algorithm Confusion Enables Authentication Bypass

**ID**: API-JWT-001
**Severity**: Critical (CVSS 9.8)
**CVE Reference**: CVE-2024-54150 (related pattern)
**Affected Component**: JWT authentication middleware

**Description**:
The API's JWT verification library trusts the algorithm specified in
the JWT header rather than enforcing a fixed algorithm. An attacker can
change the algorithm from RS256 to HS256 and sign the token using the
server's RSA public key (available from the JWKS endpoint) as the HMAC
secret. The server then uses the same public key to verify the HMAC
signature, which succeeds, allowing the attacker to forge tokens for
any user with any role.

**Attack Chain**:
1. Obtain public key: GET /.well-known/jwks.json
2. Create JWT: {"alg":"HS256","typ":"JWT"}.{"sub":"admin","role":"admin"}
3. Sign with HMAC-SHA256 using RSA public key PEM as secret
4. Access admin API: GET /api/v1/admin/transactions -> 200 OK

**Impact**:
Complete authentication bypass. An attacker can forge tokens for any
user including administrators, accessing all financial transactions,
user data, and administrative functions.

**Remediation**:
1. Enforce the expected algorithm at the server configuration level: jwt.verify(token, key, algorithms=["RS256"])
2. Never trust the alg header from the JWT for algorithm selection
3. Update the JWT library to the latest version with algorithm confusion protections
4. Consider using EdDSA (Ed25519) which does not have symmetric/asymmetric confusion risk
5. Implement token binding to prevent forged token acceptance
```
