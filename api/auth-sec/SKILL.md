---
name: auth-sec
description: >-
  Entry P1 category router for authentication and authorization. Use when
  testing login flows, sessions, object authorization, JWT, OAuth, CORS, CSRF,
  and enterprise SSO weaknesses before any deeper auth topic skill.
---

# Authentication and Authorization Router

This is the routing entry point for authentication, sessions, and authorization boundaries.

Use it to decide whether the issue is mainly login mechanics, object-level authorization, browser trust boundaries, or identity protocols such as OAuth/JWT/SAML before going deeper.

## When to Use

- The target includes login, registration, password reset, 2FA, sessions, JWT, OAuth, or SSO
- You suspect object authorization flaws, cross-tenant access, cross-origin reads, CSRF, or protocol misconfiguration
- You need to decide whether to test authentication or authorization first

## Skill Map

- [Authentication Bypass](../authbypass-authentication-flaws/SKILL.md): login bypass, password reset, 2FA, enumeration, brute-force protections
- [IDOR Broken Object Authorization](../idor-broken-object-authorization/SKILL.md): IDOR, BOLA, BFLA, missing object permissions
- [JWT OAuth Token Attacks](../jwt-oauth-token-attacks/SKILL.md): algorithm confusion, key trust issues, claim abuse, token forgery
- [OAuth OIDC Misconfiguration](../oauth-oidc-misconfiguration/SKILL.md): redirect URI, state, nonce, PKCE, account binding
- [CSRF Cross Site Request Forgery](../csrf-cross-site-request-forgery/SKILL.md): CSRF tokens, SameSite, JSON CSRF, login CSRF
- [CORS Cross Origin Misconfiguration](../cors-cross-origin-misconfiguration/SKILL.md): reflected Origin, credentialed cross-origin reads, allowlist bypass
- [SAML SSO Assertion Attacks](../saml-sso-assertion-attacks/SKILL.md): assertion wrapping, signature validation, audience, ACS boundaries

## Recommended Flow

1. First confirm the authentication model and session boundaries
2. Then confirm object-level and function-level authorization
3. Then move to token, cross-origin, and protocol details
4. If enterprise federation exists, continue with OAuth, OIDC, or SAML topics

## Related Categories

- [api-sec](../api-sec/SKILL.md)
- Default credentials, username variants, wordlist sizing, and port focus are consolidated in [authbypass-authentication-flaws](../authbypass-authentication-flaws/SKILL.md)
## 1. CONFIRMING THE ROUTE

A router produces **one** artefact: the correct destination for an observed behaviour. Confirming a route
means the destination was reached by a **resolved link** and that the destination's own dispatch table was
then consulted - never that a technique was recalled from memory.

| Step | Question | What it proves |
|---|---|---|
| 1 | Is the **observed behaviour** recorded before the route is chosen? | routing is decided by the sink, not by the parameter's name |
| 2 | Is there a **negative control**: a benign value leaving the response unchanged? | the difference is caused by your input, not application noise |
| 3 | Was the destination **loaded by resolving its link**, and did the load succeed? | a route that 404s makes the agent proceed from memory |
| 4 | Was the destination's **own dispatch table** then applied? | the destination re-decides between authentication, session, and authorisation before a technique is chosen |
| 5 | Is the **interpreter/sink named**, not the payload family? | the technique, severity, and fix all follow from the interpreter |
| 6 | Is **one interpreter at a time** observed, with a probe that distinguishes it? | probing the wrong sink burns the endpoint's error budget and teaches nothing |
| 7 | If no row matches, was the **non-coverage statement** followed? | absence of a route is information |

**A resolved link, a named sink, and a negative control.** A route chosen from the input's appearance rather
than its sink is the single most expensive mistake in this domain, because the wrong subtree is probed, comes
back clean, and the finding is recorded as "no issue".

---

## 2. EVIDENCE STANDARD

The router's evidence is **the route and the observation that justifies it**, plus the dispatch trail.

| Item | Why |
|---|---|
| The observed behaviour, verbatim, before any routing decision | The route is a conclusion about this observation; record the premise |
| The benign request and the probe request, both verbatim, plus both responses | Routing on a difference requires both sides of the difference |
| The negative control value and its unchanged response | Separates your input's effect from "this endpoint fails on everything" |
| The **sink/interpreter identified**, with the observation that established it | The destination is derived from the sink, so the sink is the load-bearing fact |
| The destination domain **actually loaded**, and that its link resolved | A resolved link is the router's own correctness condition |
| The probe that **distinguished** the chosen sink from the neighbouring candidates | the probe that separates an authentication failure from an authorisation failure |
| Any route **not taken** and why it was excluded | The eliminated branches are half the routing argument |
| The return path when nothing matched | the instruction to return to the parent router is present and followed |

### Route failures - how they mislead

| Route failure | How it misleads |
|---|---|
| Routed on the parameter's **name** rather than the sink | The wrong subtree is probed, returns clean, and a real finding is closed as "no issue" |
| Routed on a **500 or an error page** | Many parsers fail on any malformed value; an error is not a reachable sink |
| **Two plausible interpreters**, only one row taken | The untested one is silently marked clean and coverage is claimed for a sink never reached |
| Route followed **from memory** after a dead link | The agent believes it loaded doctrine while proceeding without it |
| **No negative control** | Application noise is reported as input-coupled behaviour |
| **In-band assumption on a blind sink** | Timing and out-of-band channels are never attempted, so a real vulnerability is reported as not reproducible |
| A **destination consolidated away** while its row survives | The router looks complete while dispatching into nothing |
| A **workflow-only domain** routed as a technique | Phantom coverage: the file loaded never describes a testing procedure |

---

---

## 3. DISPATCH VERIFICATION

Authentication and authorization are different bugs with different proofs. Verify which one
you are chasing, and confirm the credential actually reaches the boundary you intend to test.

| Step | Question | What it proves |
|---|---|---|
| 1 | Does the target have a login, registration, reset, 2FA, session, or token-issuing flow? | Login *mechanics* are in scope → [authbypass-authentication-flaws](../authbypass-authentication-flaws/SKILL.md) |
| 2 | Does an authenticated identity address objects it may not own (orders, invoices, files, tenants)? | The bug is authorization, not authentication → [idor-broken-object-authorization](../idor-broken-object-authorization/SKILL.md) |
| 3 | Can you create or obtain **two** accounts at the same privilege level? | Every authorization claim below needs a differential; without two identities you cannot test this domain |
| 4 | Is the credential a self-contained token (JWT, SAML assertion, opaque key) rather than a server-side session? | Token trust is the boundary → [jwt-oauth-token-attacks](../jwt-oauth-token-attacks/SKILL.md) or [saml-sso-assertion-attacks](../saml-sso-assertion-attacks/SKILL.md) |
| 5 | Does a third party (Google, Entra, Okta) issue the identity, with a redirect or `state` parameter? | The federation boundary is in scope → [oauth-oidc-misconfiguration](../oauth-oidc-misconfiguration/SKILL.md) |
| 6 | Does the response to a cross-origin `fetch` carry both `Access-Control-Allow-Credentials: true` and a reflected/wildcard origin? | Browser-mediated reads are possible → [cors-cross-origin-misconfiguration](../cors-cross-origin-misconfiguration/SKILL.md) |
| 7 | Is a state-changing route protected only by `SameSite`/implicit cookie scope, with no token or origin check? | Forgery is testable → [csrf-cross-site-request-forgery](../csrf-cross-site-request-forgery/SKILL.md) |
| 8 | Are the endpoints consumed by a client that is not a browser (mobile app, CLI, service)? | CSRF/CORS are structurally irrelevant; the real route is object-level authorization in [api-sec](../api-sec/SKILL.md) |

**Order matters: authentication first, then authorization.** Testing IDOR on a session whose
authentication you have not characterised means you cannot tell a broken lookup from a
mis-scoped session. Confirm the session boundary before you vary the object.

**One account is not a test.** A 200 for a request you made against your own object proves
nothing about enforcement. The dispatch gate for this whole domain is the existence of a
second identity.

## 4. OUTPUT STANDARD

| Item | Why |
|---|---|
| Which boundary failed, named precisely: authentication, session, object authorization, function authorization, or browser trust | The five have different owners, severities, and fixes; "auth issue" is not a finding |
| Both identities — the owner of the object and the requester — with how each was obtained | Authorization findings are differential by definition; one account cannot show enforcement |
| The exact request from each identity, verbatim, plus the two responses | The reviewer must be able to replay both directions |
| A negative control: a sibling object or route that correctly denies the same request | Proves enforcement is detectable and that you did not merely hit an endpoint that returns 200 to everything |
| For token bugs: the decoded header and payload, the verification key source, and what changed | A token finding is only meaningful as a statement about what the server failed to verify |
| For browser-boundary bugs: the exact `Origin`, the exact response headers, and whether credentials were sent | CORS/CSRF without these three details is unverifiable |
| The privilege delta actually achieved: anonymous → user, user → user' (cross-tenant), or user → admin | Separates medium correctness bugs from critical account-takeover chains |
| Reproduction after a fresh login and a new session cookie | Rules out stale-session and cache artefacts that mimic authorization bypass |

### Routing failures — how they mislead

| Routing failure | How it misleads |
|---|---|
| An authorization bug routed to login-bypass work | Password reset, brute-force protection, and lockouts are exhaustively tested and all pass; the report says "authentication is solid" while object authorization was never exercised |
| A login-mechanics bug routed to IDOR/BOLA | User enumeration, reset-token reuse, and 2FA weakness are never tested; the session layer is assumed sound because it issued a token |
| A JWT routed to SAML/OAuth work (or the reverse) | The assertion and the redirect flow are different verification paths; testing the wrong one produces a clean result on the wrong component |
| CSRF assessed on a non-browser client's endpoint | The finding is written up as unfixable or dismissed — but the endpoint is genuinely not CSRF-testable, so the *real* flaw there (missing object authz) stays invisible |
| CORS reported without `Access-Control-Allow-Credentials` | A permissive policy that leaks nothing is filed as a finding; reviewer credibility drops and the triage queue is polluted |
| IDOR claimed from a single account hitting its own object | The highest-frequency false positive in web testing: a 200 on a guessed ID is not evidence of a broken check |
| A session-token bug routed to CSRF | Token entropy, fixation, and revocation are never tested while same-site cookie behaviour is measured against a boundary that does not apply |
| The target uses enterprise SSO routed to password flows | There is no password; the domain is misrouted, nothing is testable, and the engagement stalls with no route back to [recon-for-sec](../recon-for-sec/SKILL.md) |

## 5. MAINTENANCE REFERENCE — KEEPING THIS ROUTER CORRECT

A router is a **map**, and a map is wrong the moment the terrain moves. Every item below is
a concrete, checkable fix — not advice. Run them after any edit under `skills/impl/`.

1. **Every link resolves.** A route that 404s is worse than no route: the agent believes it
   has loaded doctrine and proceeds from memory, which is precisely what the skill-invocation
   rule forbids. Assert this with a link check, not by reading.
2. **Every domain in the routing table exists on disk.** A domain can be renamed or
   consolidated away while its row survives, producing a dead route. Domains named here:
   `authbypass-authentication-flaws` `idor-broken-object-authorization` `jwt-oauth-token-attacks` `oauth-oidc-misconfiguration` `csrf-cross-site-request-forgery` `cors-cross-origin-misconfiguration` `saml-sso-assertion-attacks`.

3. **No duplicate routes.** The same observed behaviour must not appear twice with two
   different destinations. Where two domains genuinely overlap (the short `attack-*`
   methodology files and their long-form playbooks), the row must say so and instruct the
   agent to load both, rather than leaving two identical-looking entries.
4. **Coverage counts stay accurate.** Any count stated here must match the number of distinct
   deep topic skills actually routed. Counting prose mentions inflates coverage; counting only
   links that resolve to an existing `SKILL.md` is the correct denominator.
5. **Re-verify when a domain is added or removed.** Adding a domain under `skills/impl/` is an
   incomplete change until this router routes it or records it as deliberately unrouted.
   Removal is the same change in reverse — prune the row *and* the count in one commit.
6. **Prune dead domains.** A scheduled or CI link check that resolves every destination here
   prevents the slow rot where routes point at skills that were consolidated away and the
   router looks complete while dispatching into nothing.
7. **Workflow-only domains stay excluded.** CORE.md records 36 of the 199 `impl/` domains as
   agent-workflow and meta-tooling skills (handoff, writing, TDD, setup) that are not
   kill-chain techniques. Routing them manufactures phantom coverage: the agent loads a file
   that never describes a testing procedure.
8. **Ordering and phase stay consistent with CORE.md.** This router is reached from the phase
   table and dispatch block in `CORE.md`. If phases are re-cut there, the recommended flow
   here must move with them, or the router will dispatch into a phase the kill chain no
   longer contains.
9. **A self-check script exists.** `sv_check.sh` at the repository root is the existing
   precedent: it asserts size, section count, a fenced block, link liveness, and topic
   keywords. A router check is the same shape — link resolution, domain existence, domain
   count, fence parity, and presence of the three closing sections.

    ```bash
    # router self-check — run from the repository root
    f=skills/impl/auth-sec/SKILL.md
    echo "bytes: $(wc -c <"$f")  numbered sections: $(grep -c '^## [0-9]' "$f")"
    d=$(dirname "$f")
    # 1. every relative link must resolve to a real file
    grep -oE '\]\(\.\./[^)]+\)' "$f" | tr -d '](' | sed 's/)$//' | sort -u |
      while read -r p; do [ -f "$d/$p" ] || echo "DEAD LINK $p"; done
    # 2. fence parity must be even
    n=$(grep -c '^\x60\x60\x60' "$f"); [ $((n % 2)) -eq 0 ] || echo "ODD FENCE COUNT: $n"
    # 3. the three closing sections must be present and numbered
    for s in 'DISPATCH VERIFICATION' 'OUTPUT STANDARD' 'MAINTENANCE REFERENCE'; do
      grep -q "^## [0-9]*\. $s" "$f" || echo "MISSING SECTION: $s"; done
    ```

10. **The router states what it does NOT cover.** Absence of a route is information; silence
    is not. A target that reaches this domain and matches no technique here must be told to
    return to the P0 router rather than told nothing. Update the non-coverage statement
    whenever the boundary moves.

---

## 6. REMEDIATION REFERENCE - CONFORMANCE OF THE ROUTE

1. **Fix the row when the authn/authz boundary moves.** A row that routes an authorisation failure to an
   authentication technique probes the wrong subtree and returns a false "no issue".
2. **Separate authentication, session, and authorisation in the table.** They are three different tests
   with three different observations, and a merged row cannot be verified.
3. **Require the distinguishing probe in the row.** A row must say how to tell an auth failure from an
   authorisation failure, because the response codes frequently look alike.
4. **Prune consolidated destinations with their counts.** A surviving row over a removed domain is a dead
   route that reads as coverage.
5. **Keep the "not covered here" statement and its return path current.** Silence reads as coverage.
6. **Re-run the link check after any `skills/impl/` edit.**

---

## 7. RELATED ROUTERS
- [authbypass-authentication-flaws](../authbypass-authentication-flaws/SKILL.md) — Login, reset, 2FA, session, and brute-force protections
- [idor-broken-object-authorization](../idor-broken-object-authorization/SKILL.md) — Object and function authorization — the non-router shape of the same class
- [jwt-oauth-token-attacks](../jwt-oauth-token-attacks/SKILL.md) — Token trust, algorithm confusion, and claim abuse
- [oauth-oidc-misconfiguration](../oauth-oidc-misconfiguration/SKILL.md) — Redirect URI, state, nonce, PKCE, and account binding
- [csrf-cross-site-request-forgery](../csrf-cross-site-request-forgery/SKILL.md) — Tokenless state changes and SameSite gaps
- [cors-cross-origin-misconfiguration](../cors-cross-origin-misconfiguration/SKILL.md) — Credentialed cross-origin reads
- [saml-sso-assertion-attacks](../saml-sso-assertion-attacks/SKILL.md) — Assertion wrapping, signature validation, audience, ACS
- [api-sec](../api-sec/SKILL.md) — When the authentication surface is an API contract rather than a login page
- [hack](../hack/SKILL.md) — the P0 master router; return here when no route above matches
- [CORE.md](../../../CORE.md) — the kill-chain phases this router dispatches into
