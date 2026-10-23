---
name: jwt-verification
description: "Use when code verifies, issues or stores a JSON Web Token (a bearer-token guard, a JWT strategy, a login that signs one, a refresh or revocation path): pin the algorithm, issuer and audience, never let the token header choose, decode is not verify, and where keys and tokens live."
---

# jwt-verification

Step 6 of the pipeline (`WORKFLOW.md`), on the one place `skills/auth-session-conventions` leaves open: the
cryptographic verification of a JWT itself. That block owns the lifecycle (expiry, refresh, logout, storage
in a cookie, the login flow); this one owns what a verifier must check before it believes a token. The
principles hold in any language. The React/Next.js block carries a one-line version of the pin
(`skills/react-nextjs-conventions`, section 9, item 7); this block is the full statement it points at.

## When
A diff adds or changes code that parses a bearer token, configures a JWT library or strategy, signs a token,
rotates a signing key, or decides how a token is revoked. Also when reviewing an auth guard that "works"
because the tests pass with a token the test itself signed.

## Steps

### 1. Verify, with the expectations written in your code
1. **Pin the algorithm list in the verifier.** The verifier passes an explicit allowlist (one entry, in almost
   every service) and rejects everything else. RFC 8725 section 3.1 states the rule: the library must let the
   caller name the supported algorithms, and the `alg` header must match the operation actually performed.
   Verification that reads `alg` from the token and does what it says lets the attacker choose how their own
   token is checked.
2. **The header never selects the key type.** The classic break is an RS256 service whose verifier takes the
   header at its word: the attacker signs with HS256, using the public key as the HMAC secret, and a verifier
   that accepts both algorithms with one key variable validates it. The mechanism is that "the key" is a single
   value whose meaning changes with the algorithm. One allowlist, one key per algorithm, no shared variable.
3. **`none` is rejected, always.** An unsigned token is valid by its own header. RFC 8725 section 3.2 allows it
   only where something else already authenticates the token, which is never the case for a bearer token
   arriving over HTTP. A pinned allowlist removes it without a special case.
4. **Pin the issuer and the audience.** Both are checked against constants in your configuration, never
   against values found in the token. Without `iss`, a token signed by any party holding the same keys passes;
   without `aud`, a token minted for another service of the same issuer is accepted by yours (RFC 8725 sections
   3.8 and 3.9). When an identity provider signs every client's tokens with the same keys, the audience check
   is the only thing separating your users from every other client's.
5. **Decode is not verify.** Every JWT library exposes a call that base64-decodes the payload with no
   signature check, meant for inspecting a token. Used as the guard, it turns authentication into reading a
   claim the caller wrote. The tell in review: a function named `decode` or `parse` feeding `req.user`. Replace
   it with the verifying call and take claims only from its result.
6. **Check the claims you rely on, and treat absence as failure.** Require `exp` (reject a token without it)
   and `sub` if you key on it. Any custom claim (role, tenant) is read only from a token that already passed
   steps 1 to 4. A token whose `typ` or required claims differ from what this endpoint expects is refused, so an
   ID token or an email-confirmation token cannot be replayed as an access token (RFC 8725 sections 3.11 and
   3.12).
7. **Fail closed and uniformly.** Any exception from verification is a 401 that does not say which check
   failed; the cause goes to the server log, without the token (`skills/auth-session-conventions` section
   2.4). A `catch` that logs and continues is an open door that no happy-path test will ever flag.

### 2. Time
1. **Expiry is enforced by the verifier, and no option that disables it exists in your code.** A flag such as
   `ignoreExpiration` set to true "for tests" is the commonest way a token becomes eternal.
2. **Allow a small, named clock tolerance.** RFC 7519 allows leeway for `exp` and `nbf`, "usually no more than a
   few minutes". Set it in seconds, in one place, and never widen it to hide a clock problem: fix the clock.
   The client-side refresh margin lives in `skills/auth-session-conventions` section 1.4.
3. **Access tokens are short because they cannot be recalled** (section 4). The lifetime is the revocation
   delay you accepted.

### 3. Keys
1. **Prefer an asymmetric pair when anyone other than the issuer verifies.** A shared HMAC secret suits a
   service that issues and verifies its own tokens and shares the key with no one; the moment a second service
   verifies, it can also forge. Sign with the private key, verify with the public key or a JWKS endpoint.
2. **Secrets are long, random and out of the source.** An HMAC key comes from a CSPRNG at the length the
   algorithm demands (RFC 8725 section 3.5 rules out human-memorable passwords as MAC keys), is read from the
   environment or a vault, and the application refuses to start when it is missing or empty. A development
   default committed "for convenience" is a production default within a month. General secret handling is in
   `skills/security-hardening` section 4.
3. **Rotate with a `kid`, accept the old key for one token lifetime.** The issuer stamps a key id in the
   header; the verifier looks it up in a set of keys it already trusts (a local map, or a JWKS fetched from a
   configured URL) and verifies with that key and the pinned algorithm. Publish the new key before signing with
   it, stop signing with the old one, and remove the old one after the longest-lived token it signed has
   expired. Without this, a rotation that swaps the key in place logs every user out at once.
4. **`kid` is an untrusted lookup string.** It is matched against the trusted set and nothing else: never
   interpolated into a file path or a query, and `jku`, `x5u` and an embedded `jwk` from the token are ignored
   (RFC 8725 section 3.10). Fetch a JWKS only from a configured HTTPS URL, cached, with a bound on refetches so
   a stream of unknown `kid` values cannot turn your service into a request amplifier.

### 4. Revocation and storage
1. **A signed token cannot be revoked by itself.** Until `exp`, it verifies. Logging out, banning a user or
   changing a role does not touch tokens already issued, which is why `skills/auth-session-conventions`
   section 1.5 asks for explicit invalidation.
2. **Revocation needs a store every instance reads.** A deny-list or a per-user "tokens issued before"
   timestamp held in process memory protects one instance out of N and is lost at each restart; the symptom is
   a banned user refused on one request and let through on the next. Use the database or cache the service
   already runs, keyed by `jti` or by user, with an entry that expires when the token would. A per-user
   timestamp compared with `iat` is cheaper than a list and covers "sign out everywhere".
3. **Refresh tokens are not JWTs by default.** An opaque random value, stored only as a hash on the server,
   single use, rotated at each refresh, with reuse of a spent one revoking its whole family, gives revocation
   without a deny-list. Keep the short-lived credential as the JWT and the long-lived one somewhere you can
   delete it.
4. **Where the client keeps the token is decided in `skills/auth-session-conventions` section 2**: a cookie
   with `Secure` and `SameSite`, never `localStorage`, never a URL, never a log. Do not restate it and do not
   contradict it; a service that must return a token in a JSON body says so as a stated exception.
5. **The payload is readable by anyone holding the token.** Signing is not encryption. No password hash, no
   personal data beyond an identifier, no internal flag the client should not see.

### 5. Verifying the verifier
1. Write the negative tests first, each expecting a 401: a token signed with the wrong key; `alg: none`; an
   HS256 token signed with the public key when the service expects RS256; an expired token; the wrong `iss`;
   the wrong `aud`; no `exp`; a tampered payload with the original signature; an unknown `kid`.
2. A guard that answers 401 only for malformed input has been tested on the one path that proves nothing. Run
   these against the real guard and the real library, not against a mocked `verify`.

## Output / checkpoint
For each verifier in the diff: the algorithm allowlist, the issuer and audience constants, where the key
comes from, the clock tolerance, and how revocation reads a shared store, with the section 5 negative-test
results as evidence. No pipeline checkpoint is claimed on the happy path alone.

## Guardrails
- Never accept the algorithm from the token, never disable expiry, never authenticate with the decode-only call.
- Never write custom cryptography or a home-made token format: use a maintained library and its verifying call.
- Never commit, print or paste a signing key into a prompt or a log; rotating a production key is a human
  decision.
- Option names differ across JWT libraries and major versions. Read the installed version's documentation for
  the exact spelling of the allowlist, issuer, audience and tolerance options rather than writing them from
  memory.
- Identity-provider configuration (realms, client registration) is infra reality and stays outside this repo.

## Origin
Written from RFC 8725 (JSON Web Token Best Current Practices), sections 3.1 to 3.12, and RFC 7519 (JSON Web
Token), sections 4.1 and 7.2, both public standards, read 2026-10-08. Cross-checked against the official NestJS
documentation (MIT, read 2026-10-08): its authentication chapter checks signature, `exp`, `iss` and `aud` on
each request, requires a signing key of at least 32 bytes, suggests an asymmetric key when other services
verify, offers a clock tolerance for another issuer's clock, and uses opaque, single-use, rotating refresh
tokens with family revocation; its Passport recipe signs with a literal development secret flagged as not for
production and shows no algorithm allowlist, which is why section 1 states it explicitly. Also cross-checked
against two MIT agent-skill catalogues (amirtaherkhani NestJS skills; HoangNguyen0403 agent-skills-standard,
read 2026-10-08), which list the same verification points in a line each. Two CC-BY-SA Node catalogues were
read for ideas only; no text was taken. The pin existed as a single line in the React/Next.js block, and
`skills/auth-session-conventions` names JWT as a gap in its own Origin.

🟡 Maturity: written, never run on a real service. Library-specific option names (jsonwebtoken, jose,
`@nestjs/jwt`) are left out on purpose: they were not verified against installed versions.
