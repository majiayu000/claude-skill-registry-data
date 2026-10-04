---
name: api-sec
description: >-
  Entry P1 category router for API security. Use when choosing between API
  recon, authorization, token abuse, and hidden-parameter workflows before any
  deeper API topic skill.
---

# API Security Router

This is the routing entry point for API security testing.

Use this skill first to decide whether the API issue is mostly recon/docs, object authorization, token trust, or GraphQL/hidden parameters, then route to a deeper topic skill.

## When to Use

- The target exposes REST APIs, mobile backends, or GraphQL endpoints
- You need to define API testing order before going into specific topics
- You want to handle object authorization, JWT, GraphQL, and hidden fields as separate tracks

## Skill Map

- [API Recon and Docs](../api-recon-and-docs/SKILL.md): OpenAPI, Swagger, version drift, hidden documentation
- [API Authorization and BOLA](../api-authorization-and-bola/SKILL.md): BOLA, BFLA, method abuse, hidden writable fields
- [API Auth and JWT Abuse](../api-auth-and-jwt-abuse/SKILL.md): bearer token, header trust, claim abuse, rate-limit bypass
- [GraphQL and Hidden Parameters](../graphql-and-hidden-parameters/SKILL.md): introspection, batching, undocumented fields, hidden parameters

## Quick Triage

| Observation | Route |
|---|---|
| Swagger or OpenAPI is present | [api-recon-and-docs](../api-recon-and-docs/SKILL.md) |
| IDs appear in URL, JSON, headers, or GraphQL args | [api-authorization-and-bola](../api-authorization-and-bola/SKILL.md) |
| JWT token visible in traffic | [api-auth-and-jwt-abuse](../api-auth-and-jwt-abuse/SKILL.md) |
| `/graphql` or batched JSON arrays are present | [graphql-and-hidden-parameters](../graphql-and-hidden-parameters/SKILL.md) |
| Registration, login, or profile updates accept extra fields | [api-authorization-and-bola](../api-authorization-and-bola/SKILL.md) then [api-auth-and-jwt-abuse](../api-auth-and-jwt-abuse/SKILL.md) |

## Recommended Flow

1. Start with exposed endpoints and documentation assets
2. Then evaluate object-level and function-level authorization
3. Then evaluate token, header, signature, and rate-limit boundaries
4. If GraphQL or complex JSON is present, continue with hidden fields and schema abuse

## Related Categories

- [auth-sec](../auth-sec/SKILL.md)
- [business-logic-vuln](../business-logic-vuln/SKILL.md)
- [recon-for-sec](../recon-for-sec/SKILL.md)
## 1. CONFIRMING THE ROUTE

A router produces **one** artefact: the correct destination for an observed behaviour. Confirming a route
means the destination was reached by a **resolved link** and that the destination's own dispatch table was
then consulted - never that a technique was recalled from memory.

| Step | Question | What it proves |
|---|---|---|
| 1 | Is the **observed behaviour** recorded before the route is chosen? | routing is decided by the sink, not by the parameter's name |
| 2 | Is there a **negative control**: a benign value leaving the response unchanged? | the difference is caused by your input, not application noise |
| 3 | Was the destination **loaded by resolving its link**, and did the load succeed? | a route that 404s makes the agent proceed from memory |
| 4 | Was the destination's **own dispatch table** then applied? | the destination re-decides between transport, schema, and object-level concerns before a technique is chosen |
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
| The probe that **distinguished** the chosen sink from the neighbouring candidates | the probe that separates an object-level failure (BOLA) from a function-level one (BFLA) |
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

Confirm three things before loading a deeper skill: that this router is the right one, that
the target actually reaches the API domain, and that the sub-route you chose matches the
evidence rather than the client technology label.

| Step | Question | What it proves |
|---|---|---|
| 1 | Is the surface a machine-consumed interface (REST, GraphQL, gRPC-web, mobile backend) rather than a server-rendered page? | The target belongs to this router and not to [auth-sec](../auth-sec/SKILL.md) or [injection-checking](../injection-checking/SKILL.md) |
| 2 | Did a request that is not issued by the first-party UI (curl, Postman, mobile client) succeed? | The API is reachable outside the browser session, so the browser's same-origin protections are not the boundary you are testing |
| 3 | Does the response carry a machine-readable contract — JSON/XML body, `Content-Type: application/json`, an OpenAPI/Swagger document, or a GraphQL introspection/schema response? | You are on the documented-artefact route → [api-recon-and-docs](../api-recon-and-docs/SKILL.md) |
| 4 | Do object identifiers appear in the path, query, JSON body, headers, or GraphQL arguments? | Object-level authorization is testable → [api-authorization-and-bola](../api-authorization-and-bola/SKILL.md) |
| 5 | Is a bearer token, `Authorization` header, API key, or signed cookie the credential? | The token layer is in scope → [api-auth-and-jwt-abuse](../api-auth-and-jwt-abuse/SKILL.md) |
| 6 | Does `POST /graphql` (or any batched-array endpoint) respond to an introspection query? | A schema graph exists → [graphql-and-hidden-parameters](../graphql-and-hidden-parameters/SKILL.md) |
| 7 | Did step 3 return a *skeleton* rather than a body, or a `text/html` login page for every path? | You are not on an API at all — return to [recon-for-sec](../recon-for-sec/SKILL.md) and re-identify the surface |

**A JSON response is not proof of an API.** Marketing pages, error pages, and CDN edges all
return JSON. The proof is a *contract*: documented routes, typed fields, and identifiers that
a second account can address. Confirm the contract before you spend a session on it.

**The failure mode this section prevents:** treating every `fetch()` call in a browser network
tab as an API finding. Most are first-party calls whose authorization is enforced correctly;
the router exists to separate the four real sub-domains from the long tail.

## 4. OUTPUT STANDARD

A finding produced through this router must carry the elements below. Anything missing means
the finding is not yet ready for a report, regardless of how convincing it looks locally.

| Item | Why |
|---|---|
| The API inventory row for the affected endpoint (host, base path, method, route, parameters, auth required, role required, source of discovery) | Authorization is per-endpoint; a finding without its inventory row cannot be re-derived or de-duplicated |
| The exact request and the exact response, both verbatim | The reviewer must be able to replay it; a paraphrase is not evidence |
| Which of the four sub-domains it belongs to (recon / authorization / token / hidden-parameters) | Determines severity model and the correct deep skill to re-read |
| The identity used, and the fact that a *second* identity exists | Single-account BOLA reports are the most common false positive in API testing |
| A negative control — one sibling object or endpoint that correctly denies the same request | Proves you can detect enforcement rather than that you never hit it |
| The response body field that constitutes the sensitive data, quoted | A 200 with no sensitive payload is informational, not a vulnerability |
| The version path tested and whether older versions remain live | Version drift is where the unpatched authorization usually still is |
| Whether the issue reproduces after a fresh session and a fresh token | Rules out caching, replay, and stale-session artefacts |

### Routing failures — how they mislead

| Routing failure | How it misleads |
|---|---|
| A GraphQL endpoint routed to generic REST recon | Introspection, batching, and per-resolver authz are never tested; the schema graph stays invisible and the finding is written as "missing authz on /graphql" |
| An ID that appears in a JSON body routed to CSRF or injection work | Mass assignment and BOLA are missed entirely; the body field is treated as untrusted input to be encoded, not as an authorization decision to be replayed |
| An authenticated-only endpoint routed to [auth-sec](../auth-sec/SKILL.md) | Authentication succeeds and the report reads "no bypass found" — while the actual bug is *authenticated but unauthorized*, i.e. BOLA |
| A Swagger document treated as complete surface | Shadow endpoints in JS bundles and older live versions are never enumerated; coverage is over-reported at the exact moment it is wrong |
| A JWT that is visible in traffic routed to token forgery only | Claim abuse, `kid`/JWKS trust, and audience confusion inside a *valid* signature are skipped; the finding is written as "algorithm not broken" |
| A mobile backend treated as a web app | Certificate pinning, device attestation, and header trust are out of scope of the chosen route, so no bug is found on the surface that actually carries the risk |
| A `/graphql` path that returns 404 routed nowhere | The router silently stops; no route is taken and the agent falls back to memory instead of escalating to [recon-for-sec](../recon-for-sec/SKILL.md) |
| Two rows matching the same symptom with different targets | The agent picks one arbitrarily; the other technique is never attempted and duplicate findings are filed from two sessions |

## 5. MAINTENANCE REFERENCE — KEEPING THIS ROUTER CORRECT

A router is a **map**, and a map is wrong the moment the terrain moves. Every item below is
a concrete, checkable fix — not advice. Run them after any edit under `skills/impl/`.

1. **Every link resolves.** A route that 404s is worse than no route: the agent believes it
   has loaded doctrine and proceeds from memory, which is precisely what the skill-invocation
   rule forbids. Assert this with a link check, not by reading.
2. **Every domain in the routing table exists on disk.** A domain can be renamed or
   consolidated away while its row survives, producing a dead route. Domains named here:
   `api-recon-and-docs` `api-authorization-and-bola` `api-auth-and-jwt-abuse` `graphql-and-hidden-parameters`.

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
    f=skills/impl/api-sec/SKILL.md
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

1. **Fix the row when the object/function boundary shifts.** Object-level (BOLA) and function-level (BFLA)
   failures are different tests, and a row that conflates them hides the object-level case entirely.
2. **Require the separating probe in the row.** State which observation distinguishes a BOLA from a BFLA,
   since a 403 on both is the normal case.
3. **Route transport and schema defects to their own rows.** A misconfigured version or a mass-assignment
   issue is not an object-authorisation issue, and merging them loses both.
4. **Prune a removed destination with its count.** A dead route reads as covered surface.
5. **Keep the non-coverage statement current**, with its return path to the parent router.
6. **Re-run the link check after any `skills/impl/` change.**

---

## 7. RELATED ROUTERS
- [api-recon-and-docs](../api-recon-and-docs/SKILL.md) — API documentation, endpoint and version inventory — the consumer of this router's recon route
- [api-authorization-and-bola](../api-authorization-and-bola/SKILL.md) — Object and function authorization — the highest-yield API route
- [api-auth-and-jwt-abuse](../api-auth-and-jwt-abuse/SKILL.md) — Token, header, and rate-limit boundaries above the object layer
- [graphql-and-hidden-parameters](../graphql-and-hidden-parameters/SKILL.md) — Schema graph, batching, and undocumented fields
- [auth-sec](../auth-sec/SKILL.md) — When the boundary fails before authorization rather than after it
- [business-logic-vuln](../business-logic-vuln/SKILL.md) — When the API's flaw is in workflow rules, not in its contract
- [recon-for-sec](../recon-for-sec/SKILL.md) — When the surface is still unidentified
- [hack](../hack/SKILL.md) — the P0 master router; return here when no route above matches
- [CORE.md](../../../CORE.md) — the kill-chain phases this router dispatches into
