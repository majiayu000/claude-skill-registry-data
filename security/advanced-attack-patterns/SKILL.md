---
name: advanced-attack-patterns
description: Advanced attack classes beyond the OWASP Top 10 baseline including state desynchronization, cache poisoning, replay attacks, and timing-attack side.
---

# Advanced Attack Patterns

Four attack classes that a baseline OWASP Top 10 review routinely misses because they depend on architectural properties (distributed state, HTTP caching, protocol guarantees, observable timing) rather than on input validation. Each class is gated on an applicability check: if the architectural precondition is absent, skip the class and document why. The goal is a high-signal findings table, not a scripted walkthrough.

## When to Use This Skill

Use this skill when:

- Running `/run-penetration-test --depth=deep` (this skill is half of the Business Logic & Advanced Attacks hunter)
- Reviewing distributed systems with eventual consistency, event sourcing, or multi-service state
- Auditing HTTP caching architectures (CDNs, reverse proxies, application-layer caches)
- Assessing authentication or high-value endpoints where replay semantics matter
- Investigating user-enumeration or timing-leak reports

Do NOT use this skill for:
- Generic input-validation bugs (use `security-review` or baseline `/run-penetration-test`).
- Business-logic rule violations (use `business-logic-abuse` - it partners with this skill but covers a different axis).

**Trigger phrases**: "state desync", "state desynchronization", "cache poisoning", "cache deception", "replay attack", "nonce validation", "idempotency replay", "timing attack", "user enumeration", "token binding", "side channel", "Vary header", "CDN cache", "WSTG deep".

## What This Skill Does

Provides a four-class advanced-attack audit procedure:

- **State Desynchronization**: Client/server divergence, cache-vs-DB divergence, step-skip via direct endpoints.
- **Cache Poisoning**: Unkeyed inputs, missing Vary entries, header-injection into cache keys, cache deception via path confusion.
- **Replay Attacks**: Missing nonces, absent timestamp windows, absent token binding, idempotency replay outside the intended window.
- **Timing Attack Surfaces**: Enumeration via response-time delta, token-lookup timing, crypto branch timing beyond the classic `==` password comparison.

Each section starts with an **applicability check**. If the precondition does not hold, the class is skipped with a one-line justification in the output. This keeps the audit high-signal and avoids false-positive noise on architectures the class cannot reach.

## Instructions

### Step 1: State Desynchronization

**Applicability check**: Does the system have any of the following?
- Distributed components (multiple services, microservices, or separate read/write stores)
- Eventual-consistency stores (DynamoDB, Cassandra, eventually-consistent Redis replication, cross-region databases)
- Multi-step workflows where client and server each track state
- Caching layers that hold state that can diverge from the source of truth

If all answers are no, skip to Step 2 with justification "No distributed-state surface."

**Attack patterns**:

- **Client/server state divergence**: The client shows one state (e.g., "cart has 3 items") while the server records another. Attack path: the client re-submits state-carrying requests that the server trusts without corroborating against the server-side authoritative state. Classic example: client hides the "already applied discount" flag, re-applies the discount, and the server does not check.
- **Cache vs DB divergence**: A cached view lags the database. Attack path: an attacker reads from the cache a permission that has just been revoked, or writes through a stale cache that later overwrites a newer DB value. Includes the "thundering herd" pattern where cache eviction produces a window of DB-hitting requests that see inconsistent state.
- **Step-skip via direct endpoint**: The UI walks the user through A -> B -> C but each step is its own endpoint. A direct POST to C from a state where only A has been completed succeeds if the server does not re-verify the state-machine position. (This pattern also lives in the `business-logic-abuse` skill's workflow-bypass section - cross-reference both when auditing a multi-step flow.)

**Indicators in code**:
- State carried in the request payload that the server trusts without re-reading from persistence.
- Cache-first reads with long TTLs on authorization-sensitive data (permissions, roles, feature flags).
- Write-through caches without invalidation on related entities (user role change invalidates only `/users/:id`, not `/teams/:team/members`).
- Conditional UPDATE based on an in-memory read rather than a DB read (`UPDATE ... WHERE version = $stale_version`).

**Remediation**:
- Establish server-authoritative state for all authorization and financial decisions. Do not trust client-carried state beyond display.
- Use strong-consistency reads on the paths that make authorization decisions; weak consistency is acceptable only for display.
- Keep transactional boundaries tight: the read, the check, and the write for a single decision should be in one transaction.
- Cache invalidation must be driven by events, not TTL, for authorization-sensitive data.

### Step 2: Cache Poisoning

**Applicability check**: Does the system have any HTTP caching layer? This includes:
- CDNs (Cloudflare, Fastly, CloudFront, Akamai)
- Reverse proxies (nginx, HAProxy, Varnish)
- Application-layer caches that serve cached HTTP responses

If no HTTP caching layer exists, skip to Step 3 with justification "No HTTP cache surface."

**Attack patterns**:

- **Unkeyed inputs in the cache key**: A request header (e.g., `X-Forwarded-Host`, `X-Original-URL`) influences the response body but is NOT part of the cache key. Attacker sends a request that causes the origin to generate a malicious response, which the cache stores and serves to later victims who do not send the header.
- **Incorrect `Vary` headers**: The response varies by a header (e.g., `Accept-Language`, `Authorization`) but `Vary` does not list it. Cache serves one user's personalized response to another.
- **Cache-injection via header manipulation**: The origin reflects a header into the response body without encoding. If the cache keys on the URL only, a malicious header value ends up in responses to victims. Classic vector: `X-Host` reflected into absolute URLs or link tags.
- **Cache deception**: The attacker requests a URL that looks static (`/profile.css`) but the backend serves dynamic personalized content because the routing does not enforce extension-vs-route separation. The CDN caches the personalized response. Famously applied against Paypal.
- **Path normalization differences**: The cache and the origin normalize paths differently (e.g., `/foo/./bar` vs `/foo/bar`). An attacker crafts a path that the cache treats as distinct from the origin's interpretation, causing the wrong response to be stored under the attacker-controlled key.

**Indicators in code and config**:
- Responses that read request headers and include header-derived content without the header appearing in `Vary`.
- CDN / reverse-proxy configs that cache responses without an explicit allow-list of keyed headers.
- Application routes that serve dynamic content from paths with static-looking extensions.
- Absent or too-permissive `Cache-Control: private` / `no-store` on personalized endpoints.
- Frontends that expect a CDN-set header (`X-Original-URL`) but do not strip the client-sent version.

**Remediation**:
- Enumerate every input that influences the response body. Every one must be in the cache key or explicitly marked non-cacheable.
- `Vary` header must include every request header that changes the response. For authenticated responses: `Vary: Cookie, Authorization` at minimum, or `Cache-Control: private, no-store`.
- Strip client-sent headers that the origin interprets as trusted (`X-Forwarded-For`, `X-Original-URL`, `X-Rewrite-URL`) at the CDN/proxy boundary.
- Enforce route-to-extension separation: dynamic routes reject `/profile.css`-style paths.
- Normalize paths identically at the cache and origin (or disable caching for paths that could be interpreted differently).

### Step 3: Replay Attacks

**Applicability check**: Does the system accept requests that carry authentication or state-changing semantics? If the only endpoints are anonymous read-only, skip to Step 4 with justification "No state-changing request surface."

**Attack patterns**:

- **Missing nonce**: A signed request (e.g., OAuth, OIDC, webhook, SAML) does not carry a server-enforced one-time value, so capturing and replaying the request succeeds indefinitely.
- **Missing idempotency key (within window)**: Distinct from the business-logic double-spend: here the attacker replays a captured request to produce a second effect. Without an idempotency key, the server cannot tell the replay from a legitimate retry.
- **No timestamp window validation**: A signed request includes a timestamp but the server does not check `|now - timestamp| < skew`, or checks with an implausibly wide skew (hours or days). Attacker replays the request weeks later.
- **Token binding absent**: An access token is bearer-only (not bound to the client's TLS session, device, or channel). A leaked token from any transport can be replayed from anywhere.
- **Response replay**: Less common but worth checking - the server's response is signed/attested but the client does not bind the response to the original request, allowing cross-request confusion.

**Indicators in code**:
- Signature validation present but no nonce check.
- Timestamp fields in signed payloads that are logged but never validated.
- Bearer tokens with long expiry (days or weeks) and no DPoP / mTLS / per-request binding.
- Webhook handlers that verify signatures but do not dedup on `(event_id, event_version)`.
- Auth servers that accept any valid signature regardless of which endpoint the token was issued for (token audience not checked).

**Remediation**:
- Require a server-enforced nonce on every signed request. Store nonces with a TTL long enough to cover the signature validity window.
- Validate `timestamp` against a small skew (e.g., +/- 5 minutes). Reject outside the window.
- For high-value sessions, use token binding (DPoP, mTLS client certs, or per-request signatures over a server-issued challenge). Bearer-only tokens are a last resort.
- Webhooks: dedup at the boundary on `(event_id, event_version)`. Reject replays.
- Audience-check every token: the token's `aud` claim must match the endpoint's expected audience.

### Step 4: Timing Attack Surfaces

**Applicability check**: Does the system have any branch whose duration depends on a secret or a user-enumeration-sensitive input? If the only comparisons against secrets are already constant-time (bcrypt/scrypt/argon2 password comparisons using verify functions) and there are no user-existence-revealing code paths, skip with justification "No observable timing leak surface."

**Attack patterns beyond classic password `==`**:

- **User enumeration via login-response timing**: The login endpoint takes measurably longer when the username exists (because the password hash is computed) than when it does not. Attacker enumerates valid usernames by timing.
- **User enumeration via password-reset timing**: The password-reset endpoint takes longer when the email exists (DB write + email send) than when it does not. Same attack, different endpoint.
- **Token-lookup timing**: Session or API tokens are looked up in a data structure that short-circuits on the first mismatched byte. Attacker measures timing to reconstruct the token byte by byte.
- **Cryptographic side channels**: RSA decryption, ECDSA signing, or AES operations implemented without constant-time primitives leak the secret through observable timing variance. Applies mostly to custom crypto code; less common with vetted libraries but still present when libraries are misused (e.g., manual CBC-HMAC instead of AEAD).
- **Directory-traversal timing**: An endpoint that reads filesystem content takes longer when a path exists than when it does not; attacker enumerates filesystem via timing.
- **Regex-engine timing**: A regex with catastrophic backtracking gives the attacker observable timing differences for inputs that trigger backtracking; usable for both DoS and enumeration.

**Indicators in code**:
- `if user == known_username: bcrypt.check(password)` where the bcrypt call runs conditionally.
- `if user_exists(email): send_reset_email(...)` with an early return on absence.
- Token comparison using `==` rather than a constant-time comparator (`hmac.compare_digest` in Python, `crypto.timingSafeEqual` in Node).
- Any regex applied to user input that includes unbounded backtracking (`(a+)+$` pattern family).
- Paths that call `os.path.exists` or `os.stat` on user-controlled paths and branch on the result.

**Remediation**:
- For user enumeration: always perform the expensive work regardless of user existence. Run a dummy bcrypt check with a constant hash for missing users. Reply with a uniform response body and uniform latency.
- For token lookups: use `hmac.compare_digest` (Python), `crypto.timingSafeEqual` (Node), or `subtle.ConstantTimeCompare` (Go). Never compare secrets with `==`.
- For password-reset enumeration: reply with a uniform success message regardless of email existence; perform a no-op delay if absent; send the email asynchronously so the sync response time does not leak existence.
- For custom crypto: use vetted libraries (`libsodium`, `cryptography`, `tink`) exclusively; do not implement RSA or AES primitives in application code.
- For regex: bound backtracking with atomic groups, possessive quantifiers, or a bounded-backtracking engine (Rust's `regex`, Go's `regexp`, `re2`).

### Step 5: Output Format

Produce findings as a table. Include applicability decisions for classes that were skipped so the operator sees the complete audit shape:

| Attack Class | Applicability | Finding Severity | Code Reference | Exploit Sketch | Remediation |
|--------------|---------------|------------------|----------------|----------------|-------------|
| State desynchronization | YES (multi-service) | HIGH | `src/cart/discount.py:42-58` | Client re-applies discount by re-sending cart state with discount flag cleared | Re-read discount state from DB before applying |
| Cache poisoning | YES (Cloudflare CDN) | CRITICAL | `nginx.conf + src/views/home.py:88` | `X-Forwarded-Host` reflected into absolute URLs; not in cache key | Strip `X-Forwarded-Host` at CDN, add to cache key, switch to relative URLs |
| Replay attacks | NO | - | - | - | No signed requests outside webhooks; webhooks already dedup on event_id |
| Timing attacks | YES (login endpoint) | MEDIUM | `src/auth/login.py:31-49` | Timing delta ~120ms reveals valid usernames | Run dummy bcrypt for missing users |

Severity guidance:
- CRITICAL: attack is exploitable in default config, gives code execution, session hijack, or bulk data exposure.
- HIGH: attack is exploitable but requires a specific (common) precondition, gives account takeover or privilege escalation.
- MEDIUM: attack gives information disclosure, enumeration, or partial secret exposure.
- LOW: attack is theoretical or requires co-located attacker; defense-in-depth gap.

## Best Practices

- **Apply the applicability check first.** A five-line "not applicable" justification is better than a three-page false-positive write-up.
- **Trust the libraries, verify the usage.** Constant-time comparators exist in every mainstream language. Find the place `==` is used on a secret.
- **Every `Vary` header audit needs a test.** Cache bugs are invisible until someone else requests the same URL and gets the wrong response.
- **Replay-attack defenses stack.** Nonce + timestamp window + token binding is strictly stronger than any one defense.
- **User enumeration is the most common timing leak.** Always audit `/login`, `/register`, `/forgot-password`, and `/resend-verification` for timing differences.

## Common Patterns

### Pattern 1: Uniform-timing login

```python
# Constant-time login: run bcrypt for both existing and missing users
DUMMY_HASH = "$2b$12$" + "X" * 53  # valid bcrypt hash structure, matches no password

def login(email: str, password: str) -> Optional[User]:
    user = db.query(User).filter_by(email=email).one_or_none()
    stored_hash = user.password_hash if user else DUMMY_HASH
    # Always runs bcrypt; no branch on user existence
    if bcrypt.checkpw(password.encode(), stored_hash.encode()) and user is not None:
        return user
    return None  # uniform response path for both "no user" and "wrong password"
```

### Pattern 2: Nonce-enforced signed request

```python
def verify_signed_request(req, signature, timestamp, nonce) -> bool:
    # Window check
    if abs(time.time() - timestamp) > 300:  # 5 minutes
        return False
    # Nonce check (Redis with TTL covering the window + grace period)
    if not redis.set(f"nonce:{nonce}", "1", nx=True, ex=600):
        return False  # already used
    # Signature verification (timing-safe)
    expected = hmac.new(SECRET, f"{timestamp}:{nonce}:{req.body}".encode(), "sha256").hexdigest()
    return hmac.compare_digest(signature, expected)
```

### Pattern 3: Cache-safe personalized response

```python
# Correct headers for a personalized authenticated response
response.headers["Cache-Control"] = "private, no-store, max-age=0"
response.headers["Vary"] = "Cookie, Authorization"
# Or for a response that may be cached per-user at a shared CDN:
response.headers["Cache-Control"] = "private, max-age=60"
response.headers["Vary"] = "Cookie"  # Cookie includes the session
```

## Quality Checklist

- [ ] Every class explicitly either audited OR marked not-applicable with a one-line reason
- [ ] Cache-poisoning audit includes every request header the response depends on
- [ ] Every signed-request finding reports which defense is absent (nonce / timestamp / binding)
- [ ] Every timing-attack finding includes an observed timing delta or a code-level confirmation of the branch
- [ ] Remediation is architectural (constant-time comparator, strict Vary, server-authoritative state) rather than input-sanitization patches
- [ ] State-desync findings cross-reference the `business-logic-abuse` skill where the overlap exists (workflow bypass)

## Verification

- [ ] For each cache-poisoning finding, attempt the exploit from a second client to confirm cross-user impact
- [ ] For each timing finding, measure the timing delta from an unprivileged network position to confirm observability
- [ ] For each replay finding, capture and re-send the request; confirm rejection after the fix
- [ ] For each state-desync finding, write an integration test that triggers the divergence and asserts the post-fix invariant
- [ ] Confirm `Vary` headers by requesting the same URL with and without the relevant header from a CDN-adjacent tool (e.g., `curl -I` against the CDN, then the origin)

## Related Skills

- `business-logic-abuse` - Companion skill; state-desynchronization step-skip and workflow-bypass overlap heavily
- `security-patch-advisor` - Patch generation for XSS / SQL-i / SSRF fixes referenced in remediation
- `security-review` - Baseline OWASP Top 10 pass that this skill extends
- `authentication-patterns` - Token binding, session management, MFA flows referenced in replay attacks
- `fintech-engineer` - Financial replay and double-spend coverage in payment-specific contexts

---

**Version**: 1.0.0
**Last Updated**: April 2026

### Iterative Refinement Strategy

This skill is optimized for an iterative approach:
1. **Execute**: Apply each class's applicability check, audit where applicable, produce the findings table.
2. **Review**: For each "not applicable" decision, verify the precondition really is absent. For each finding, confirm severity against real exploit effort.
3. **Refine**: Downgrade theoretical findings; escalate any that carry a pre-auth exploit path.
4. **Loop**: Continue until every applicable class has a high-signal verdict (finding with exploit sketch, or documented clean audit).
