---
name: hack
description: >-
  Entry P0 primary router for HackSkills. Use when the task involves web
  application testing, API security assessment, recon, vulnerability triage,
  exploit path planning, or choosing the right next category skill before any
  deep topic skill.
---

# HACKING SKILLS / HackSkills

> **AI LOAD INSTRUCTION**: This is the **P0 entry router**. Its entire job is to pick the
> right domain in **one step** — nothing else. Read the routing table, name the observed
> behaviour, and load exactly one P1 category router from it (`recon-for-sec`, `api-sec`,
> `auth-sec`, `injection-checking`, `file-access-vuln`, `business-logic-vuln`) or one deep
> topic skill. **The most common mistake — and the one this file exists to prevent — is
> loading technique playbooks before identifying the actual surface.** An XSS payload list
> against an SSRF sink, or a JWT spray against a login that was never reachable, produces a
> session of clean results on the wrong component. Identify the surface, then dispatch;
> a router that emits payloads has already failed. If two rows fit, take the one that matches
> **observed behaviour** (what the server does), not the one that matches the feature's
> marketing name.


## Overview

This is a top-level routing skill for **bug bounty, web security, API security, and authorized penetration testing**.

Its core role is not to replace all specialized techniques, but to help the agent:

1. First determine the testing phase (Recon / Validation / Privilege Escalation / Chain building)
2. Then select the correct vulnerability category
3. Avoid relying only on baseline model memory; prefer structured methodology
4. Prioritize boundary conditions AI often misses but that matter in real engagements

## Trust Model

- This knowledge base emphasizes content safety and auditability.
- Use this only within **authorized targets**, **legitimate research**, **defensive validation**, and **bug-bounty-approved rules**.
- Do not use these techniques for unauthorized attacks.

## When to Use This Skill

Use this skill first in the following scenarios:

- You just received a new bug bounty target and do not know where to start
- You need to decide whether to load XSS / SQLi / SSRF / IDOR / JWT / API tracks first
- You want the agent to perform Web/API security testing with a more stable methodology
- You need to route scattered findings to the right attack surface
- You want AI to miss fewer critical test points in security work

## Operating Model

### Step 1: Start with Recon and context validation

Collect first:

- Target type: classic web, REST API, mobile backend, admin panel, payment flow, file upload, GraphQL
- Identity and permission model: anonymous, regular user, admin, multi-tenant
- Input locations: URL, query parameters, JSON, headers, cookies, filenames, imported files, templates, reflection points
- Output locations: HTML, attributes, JS, PDF, email, logs, background tasks, mobile endpoints

### Step 2: Route by observed behavior

| Signal | Priority direction |
|---|---|
| Input reflects into HTML / JS | XSS / SSTI |
| Server actively fetches URL / hostname | SSRF |
| Accepts XML / Office / SVG | XXE |
| Path, filename, or download endpoint is controllable | Path Traversal / LFI |
| Many object IDs appear in APIs | IDOR / BOLA / BFLA |
| Login, reset password, 2FA, sessions | Auth Bypass / JWT / OAuth |
| Multi-step transactions, coupons, pricing, inventory | Business Logic |
| MongoDB / JSON query syntax exposure | NoSQL Injection |
| CLI tools, image processing, importers | Command Injection |
| HTTP parsing anomalies / front-back framing mismatch | Request Smuggling |
| Node.js JSON handling / controllable `__proto__` | Prototype Pollution |
| PHP weak comparison / 0e hash / loose conditions | Type Juggling |
| Repeated parameter names / WAF-app parsing mismatch | HTTP Parameter Pollution |
| One-time operations (coupon/inventory/reset) | Race Condition |
| XML/XSLT template processing | XSLT Injection |
| Accessible .git/.svn/.env paths | Insecure SCM |
| CSV/Excel export features | CSV Formula Injection |
| WebSocket protocol upgrades | WebSocket Security |
| Internal package names / supply-chain inventory | Dependency Confusion |

### Step 3: Use the most likely-hit testing order

1. Recon / Methodology
2. API Security / Auth / IDOR
3. XSS / SQLi / SSRF / SSTI / XXE
4. Business Logic / Race Condition
5. Chained exploits and privilege-escalation paths

## Core Skill Map

If you have the full repository, prioritize using these topic documents together:

- [Recon and Methodology](../recon-and-methodology/SKILL.md)
- [XSS Cross Site Scripting](../xss-cross-site-scripting/SKILL.md)
- [SQLi SQL Injection](../sqli-sql-injection/SKILL.md)
- [SSRF Server Side Request Forgery](../ssrf-server-side-request-forgery/SKILL.md)
- [XXE XML External Entity](../xxe-xml-external-entity/SKILL.md)
- [SSTI Server Side Template Injection](../ssti-server-side-template-injection/SKILL.md)
- [IDOR Broken Object Authorization](../idor-broken-object-authorization/SKILL.md)
- [CMDi Command Injection](../cmdi-command-injection/SKILL.md)
- [Path Traversal LFI](../path-traversal-lfi/SKILL.md)
- [CSRF Cross Site Request Forgery](../csrf-cross-site-request-forgery/SKILL.md)
- [API Security Router](../api-sec/SKILL.md)
- [JWT OAuth Token Attacks](../jwt-oauth-token-attacks/SKILL.md)
- [OAuth OIDC Misconfiguration](../oauth-oidc-misconfiguration/SKILL.md)
- [CORS Cross Origin Misconfiguration](../cors-cross-origin-misconfiguration/SKILL.md)
- [SAML SSO Assertion Attacks](../saml-sso-assertion-attacks/SKILL.md)
- [Authentication Bypass](../authbypass-authentication-flaws/SKILL.md)
- [Business Logic Vulnerabilities](../business-logic-vulnerabilities/SKILL.md)
- [Upload Insecure Files](../upload-insecure-files/SKILL.md)
- [NoSQL Injection](../nosql-injection/SKILL.md)
- [Request Smuggling](../request-smuggling/SKILL.md)
- [Prototype Pollution](../prototype-pollution/SKILL.md)
- [Type Juggling (PHP)](../type-juggling/SKILL.md)
- [HTTP Parameter Pollution](../http-parameter-pollution/SKILL.md)
- [Race Condition](../race-condition/SKILL.md)
- [XSLT Injection](../xslt-injection/SKILL.md)
- [Insecure Source Code Management](../insecure-source-code-management/SKILL.md)
- [CSV Formula Injection](../csv-formula-injection/SKILL.md)
- [WebSocket Security](../websocket-security/SKILL.md)
- [Dependency Confusion](../dependency-confusion/SKILL.md)
- [Ghost Bits Cast Attack](../ghost-bits-cast-attack/SKILL.md)

Previously separate mini skills such as payload-selection and brute-selection were merged back into their main skills to avoid router overload and selection noise.

## High-Value Expert Intuitions

These are points many baseline models miss, but they are frequently effective in real bug bounty work:

1. **The same filtering logic is often reused across multiple pages**: if one point is bypassable, similar pages usually are too.
2. **Parameter names are an attack surface too**: WAFs often inspect values but not names.
3. **Second-order vulnerabilities are common**: safe at storage time does not mean safe when later read into a dangerous context.
4. **BOLA is fundamentally 'authenticated but unauthorized'**: replaying with account A/B switching is critical.
5. **Older API versions are most likely to miss patches**: fixing v2 does not mean v1 was retired.
6. **Business-logic vulnerabilities often bring highest impact**: scanners miss them and they persist longer.
7. **Race conditions should prioritize one-time actions**: coupon redemption, claims, resets, invites, trials, inventory deduction.
8. **For JWT attacks, check key and algorithm context first**: do not blindly spray payloads; verify `alg`, `kid`, JWKS, and key source first.

## Suggested Prompts

Use this skill as a router to make the agent clarify phase and goal first:

- "First, plan the testing route for this target using bug bounty methodology.
- "This is a REST API; prioritize BOLA, BFLA, Mass Assignment, and JWT angles.
- "This parameter triggers server-side requests; list key validation points from an SSRF perspective.
- "This feature is a payment/coupon/inventory flow; prioritize business logic and race-condition analysis.
- "I only see login and password-reset flows; analyze via Auth Bypass + OAuth/JWT + CSRF.

## Installation Notes

Recommended skill name:

- `hack`

Recommended search keywords:

- `HackSkills`
- `HACKING SKILLS`
- `bug bounty`
- `bug bounty hunter`

## Guidelines

- Prioritize routing by target type and observed behavior, not random payload enumeration.
- When payloads are needed, prefer quick-start / first-pass samples in the corresponding main skill instead of adding another intermediate router.
- Prioritize reusable filters, shared components, and cross-page reproduction paths.
- Confirm authentication, authorization, and version boundaries before deeper exploitation.
- Preserve explainable, auditable, reproducible testing processes.
- When full repository context is available, return to topic documents for finer exploitation details.
## 1. CONFIRMING THE ROUTE

This is phase 0. Its deliverable is **one named destination with one quoted reason**, and confirming it is a
mechanical check on the dispatch record - not a reading of the routing table until something looks right.

| Step | Question | What it proves |
|---|---|---|
| 1 | Are the **Step 1 facts** collected first: target type, identity model, input locations, output locations? | routing on evidence rather than on the feature's name |
| 2 | Does the selected row describe **observed server behaviour**, not an assumption? | a row matched by assumption dispatches to the wrong domain |
| 3 | Is there a **request/response pair** demonstrating that behaviour? | the dispatch is reproducible and re-derivable when contested |
| 4 | Does the destination **exist on disk** with a `SKILL.md`, and did its link resolve? | a dead route makes the agent fall back to memory |
| 5 | Is the **tie-break recorded** when a second row also matches? | two plausible routes is the normal case; an unrecorded tie-break is an arbitrary choice |
| 6 | Is **exactly one** next file named, with its reason? | the deliverable is a file, not an intention |
| 7 | If no row matches, was [recon-for-sec](../recon-for-sec/SKILL.md) loaded **instead of** guessing? | the commonest routing error is dispatching from an unmapped surface |
| 8 | Did the dispatch complete in **one pass**? | reading three routers to decide means Step 1 was skipped |

**A named domain, a quoted row, and the observed behaviour that justified it.** A dispatch that cannot name
its row and its evidence is a guess, and phase 0 turning into the whole engagement is a failed dispatch.

---

## 2. EVIDENCE STANDARD

This router produces **no findings** - it produces the precondition for one. Its evidence is therefore the
**dispatch record** that a downstream report traces back through.

| Item | Why |
|---|---|
| The selected routing-table row, quoted, and the domain it dispatched to | Makes the chain skill → router → finding auditable end to end |
| The observed behaviour that matched the row, with the request/response showing it | Distinguishes routing on evidence from routing on the feature's name |
| The P1 router or deep topic skill actually loaded, by resolved link | Proves exactly one domain was taken, so coverage claims are bounded |
| The **collect-first facts** (target type, identity model, input/output locations) | The premise the route rests on; without it the row is unmatched |
| The **tie-break** recorded when a second row matched, and the excluded row | The eliminated branches are half the routing argument |
| Any routing-table row that was **considered and rejected**, with the behaviour that rejected it | Shows the table was consulted rather than skimmed |
| The **return path** when nothing matched | Absence of a route is information; silence is not |
| That the destination's link **resolved** | The router's own correctness condition |

### Dispatch failures - how they mislead

| Dispatch failure | How it misleads |
|---|---|
| Routed on the feature's **name** rather than observed behaviour | The wrong domain is loaded, returns clean, and the surface is recorded as tested |
| **No request/response pair** behind the row | The dispatch is unreproducible and cannot be re-derived when the finding is contested |
| **Two rows matched**, no tie-break recorded | The choice becomes arbitrary and the agent's reasoning is unreviewable |
| Route followed **from memory** after a dead link | The agent believes it loaded doctrine while proceeding without it |
| **Surface never enumerated** | A category is guessed, which is the commonest routing error |
| Phase 0 **never terminated** | The router becomes the engagement instead of dispatching into one |
| A **workflow-only domain** routed as a technique | Phantom coverage: the file loaded never describes a testing procedure |
| A destination **consolidated away** while its row survives | The table looks complete while dispatching into nothing |

---

---

## 3. DISPATCH VERIFICATION

This router is phase 0 in `CORE.md`. Its output is a **decision**, and a decision is only
valid if the surface behind it was actually observed. Verify the dispatch before any deep
skill is loaded — the checks below are cheap and they are the only thing standing between a
targeted session and a payload-spraying one.

| Step | Question | What it proves |
|---|---|---|
| 1 | Have you collected target type, identity model, input locations, and output locations (the Step 1 list above) before consulting the routing table? | You are routing on evidence rather than on the feature's name |
| 2 | Does the routing-table signal you selected describe **observed server behaviour** ("server actively fetches URL") rather than an assumption ("there is probably an API")? | The row is a fact, not a guess; assumptions are how a target gets routed to the wrong domain |
| 3 | Is there a request/response pair demonstrating that signal? | The dispatch is reproducible by the next agent, and re-derivable if the finding is contested |
| 4 | Does the selected row's domain exist as a directory under `skills/impl/` with a `SKILL.md` in it? | The route terminates in real doctrine rather than a dead link, so the agent does not fall back to memory |
| 5 | Does the target also match a *second* row, and have you written down the tie-break (observed behaviour wins)? | Two plausible routes is the normal case, not the exception; an unrecorded tie-break becomes an arbitrary choice |
| 6 | If the surface is unknown or unenumerated, have you loaded [recon-for-sec](../recon-for-sec/SKILL.md) instead of guessing a category? | Guards the single most common routing error: dispatching to a category from a surface you have not mapped |
| 7 | Can you state the one P1 router or deep topic skill you will load next, and why that one? | The router's deliverable is a named next file; "I will look into it" is a failed dispatch |
| 8 | If the answer to every row is no, have you routed to [recon-for-sec](../recon-for-sec/SKILL.md) rather than continuing to read this file? | Prevents phase 0 from becoming the whole engagement |

**The one-step rule.** A correct dispatch names a domain and a reason in a single pass. If you
find yourself reading three category routers to decide, the surface was never identified and
step 1 was skipped — go back to it.

## 4. OUTPUT STANDARD

This router does not produce findings; it produces the **precondition** for a finding. What a
downstream report must be able to trace back to is the dispatch record below. If a report
cannot show which row it came from and what behaviour justified it, the reviewer cannot tell
whether the technique matched the surface at all.

| Item | Why |
|---|---|
| The selected routing-table row, quoted, and the domain it dispatched to | Makes the chain skill → router → finding auditable end to end |
| The observed behaviour that matched the row, with the request/response that shows it | Distinguishes routing on evidence from routing on the feature's name |
| The P1 router loaded (or the deep topic skill, if no category router applies) | Proves exactly one domain was taken, so coverage claims are bounded and honest |
| The tie-break if a second row also matched, and why the taken row wins | Two-row matches are normal; an unrecorded choice looks arbitrary in review |
| What the target *did not* match, listed explicitly | The absence of a route is coverage information; silence reads as "not tested" at best and "tested clean" at worst |
| The phase this dispatch belongs to per `CORE.md` (0 router, 1 scout, 3 strike, …) | Aligns the router with the kill chain so the next phase loads the right files |
| The identity model and access level the dispatch assumed (anonymous / user / admin / multi-tenant) | Many rows are only valid at a specific access level; a privileged-only row applied anonymously tests nothing |
| The dependencies the dispatch creates (materials, additional targets, second accounts) | Lets the session fail fast if the required precondition cannot be obtained |

### Routing failures — how they mislead

| Routing failure | How it misleads |
|---|---|
| A deep technique playbook loaded before the surface was identified | The whole session is spent applying a correct technique to a sink that never reaches that interpreter; results come back clean and the real surface is never tested |
| A target routed to the wrong domain (SSRF signals read as upload) | The chosen domain's workflow runs to completion and finds nothing reportable, while the actual vulnerability class is never exercised |
| A surface dispatched to a domain that has no matching technique | The category router is loaded, matches none of its rows, and returns nothing — the session stalls with no stated route back to this table |
| A false-positive domain match (the word "API" in a marketing page routed to `api-sec`) | Recon of REST/GraphQL artefacts is attempted against an HTML page; every probe is a non-event and the dispatch looks like a negative result |
| A target that needs two domains routed to one | The composite chain (e.g. logic + authorization, or upload + traversal) is never assembled, and each half individually looks unexploitable |
| A row chosen from the feature's name rather than observed behaviour | "There is a file upload" routes to file access even when the pipeline only stores bytes and never serves them; the impactful surface (the callback URL, the parser) is skipped |
| Phase 0 used as a destination instead of a routing step | Time is spent re-reading this file and re-planning; no phase-1 or phase-3 skill is ever loaded |
| The router's own precedent ("load both overlapping families") ignored after dispatch | A short methodology file is loaded without its long-form companion, so procedure order is known but payloads and edge cases are not — and the session presents as complete |

## 5. MAINTENANCE REFERENCE — KEEPING THIS ROUTER CORRECT

A router is a **map**, and a map is wrong the moment the terrain moves. Every item below is
a concrete, checkable fix — not advice. Run them after any edit under `skills/impl/`.

1. **Every link resolves.** A route that 404s is worse than no route: the agent believes it
   has loaded doctrine and proceeds from memory, which is precisely what the skill-invocation
   rule forbids. Assert this with a link check, not by reading.
2. **Every domain in the routing table exists on disk.** A domain can be renamed or
   consolidated away while its row survives, producing a dead route. Domains named here:
   `api-sec` `auth-sec` `injection-checking` `file-access-vuln` `recon-for-sec` `business-logic-vuln`.
   The six P1 routers it dispatches to are listed in the RELATED ROUTERS section rather than in
   this table; the two counts are separate on purpose — 30 deep topic skills and six category
   routers — and both must be re-verified whenever the table above changes.
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
    f=skills/impl/hack/SKILL.md
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

This router is phase 0, and its output is a decision rather than a finding. Its remediation is
**route maintenance**, and every item below is a concrete, checkable change.

1. **Fix the dead link, not the routing row.** A route whose destination does not resolve is worse than no
   route, because the agent believes it has loaded doctrine and proceeds from memory. Resolve the link.
2. **Fix the row when the signal changes.** If a destination's observed behaviour no longer matches the
   row's signal text, the row is wrong and must be re-derived from the behaviour, not patched cosmetically.
3. **Record the tie-break in the row itself.** When two rows match, the tie-break rule (observed behaviour
   wins) belongs in the table, so the choice is reviewable rather than arbitrary.
4. **Prune a consolidated destination and its count in one change.** A row surviving a rename dispatches
   into nothing while the table looks complete.
5. **Keep workflow-only domains excluded.** Routing them manufactures phantom coverage: the loaded file
   never describes a testing procedure.
6. **Re-verify after any edit under `skills/impl/`.** Adding or removing a domain is an incomplete change
   until this router routes it or records it as deliberately unrouted.
7. **Prefer a route to `recon-for-sec` over a guess.** Where no row matches, the correct remediation is the
   return path, not a new row invented for an unmapped surface.

---

## 7. RELATED ROUTERS
- [recon-for-sec](../recon-for-sec/SKILL.md) — P1 router — unknown surface, enumeration, and methodology
- [api-sec](../api-sec/SKILL.md) — P1 router — REST, mobile, and GraphQL surfaces
- [auth-sec](../auth-sec/SKILL.md) — P1 router — authentication, sessions, and authorization
- [injection-checking](../injection-checking/SKILL.md) — P1 router — input reaching an interpreter
- [file-access-vuln](../file-access-vuln/SKILL.md) — P1 router — paths, downloads, and upload pipelines
- [business-logic-vuln](../business-logic-vuln/SKILL.md) — P1 router — workflow, state, and race windows
- [hack](../hack/SKILL.md) — the P0 master router; return here when no route above matches
- [CORE.md](../../../CORE.md) — the kill-chain phases this router dispatches into
