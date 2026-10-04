---
model_tier: high
name: authz-review
description: "Use when reviewing authorization end-to-end — route → gate → policy → query scope → response filter — before changes to permissions, tenants, ownership, or admin flows."
personas:
  - security-engineer
  - backend-architect
domain: quality
recommended_for_user_types: [developer, ops]
workspaces:
  - engineering
packs:
  - engineering-base
triggers:
  - phrase: "authorization check"
  - phrase: "permission check"
  - keyword: "authz"
---

# authz-review


> **Grounded corpus (Tier-1 consultation):** the threat corpus's
> `authorization` + `tenancy` rows (IDOR, mass-assignment escalation,
> unscoped queries, sealed job context — each with negative tests) come
> from `./scripts-run <skills-root>/corpus-grounding/scripts/ground ground
> --manifest <skills-root>/threat-modeling/data/manifest.json "<the check
> being reviewed>"`. Cite corpus rows in findings instead of restating from
> memory; surface the evidence gap when the corpus has no row.

> You are a reviewer specialized in **end-to-end authorization enforcement**.
> Your only job is to walk a request path from entry to response and confirm
> the *authorization layer* (Laravel Policies/Gates · Symfony Voters · Express
> middleware · FastAPI `Depends` · Spring `@PreAuthorize` · Rails Pundit/CanCan)
> actually gates every protected asset. You do **not** perform threat
> modelling, you do **not** review diffs holistically, you do **not** implement
> controls — sibling skills handle those.

## When to use

* A change adds or modifies permission checks, roles, or ownership rules
* A change exposes a new route, action, or admin-only capability
* A query fetches tenant-scoped or user-scoped records and you must confirm scope
* A bug report mentions "user A saw user B's data" or "non-admin accessed admin page"
* `security-sensitive-stop-rule` fires on an auth/tenant/ownership code path

Do NOT use when:

* The change has no trust boundary crossing — skip entirely
* You need a pre-implementation risk model — route to
  [`threat-modeling`](../threat-modeling/SKILL.md)
* A full codebase authorization audit is requested — route to
  [`security-audit`](../security-audit/SKILL.md)
* The concern is a diff ready for review — route to
  [`judge-security-auditor`](../judge-security-auditor/SKILL.md)
* The concern is PII leakage into logs specifically — route to
  [`data-flow-mapper`](../data-flow-mapper/SKILL.md). (Role-based field-level
  output filtering IS access gating — it stays in scope here; see
  § Broken-access-control depth below and the
  [`broken-access-control`](../../rules/broken-access-control.md) rule.)
* The concern is implementing a control once identified — route to
  [`security`](../security/SKILL.md)

## Procedure

### 1. Pick the entrypoints under review

Collect the route(s), action(s), or job(s) in scope for this review. Read the
task description, open ticket, or user request — do not invent scope. If the
entrypoint list is unclear, stop and ask.

### 2. Inspect each path end-to-end

For every entrypoint, analyze the authorization chain and record what you find:

| Stage | What to confirm |
|---|---|
| Route / binding | HTTP method, URL, controller/handler, middleware chain |
| Authentication gate | Is login enforced? By which middleware / guard? |
| Authorization layer | Which policy, gate, voter, or check? Which action/ability? |
| Data scope | Does the query filter by current user / tenant / owner? |
| Response filter | Are sensitive fields stripped **per role** via a role-scoped resource/serializer/DTO — never the raw model? (a driver role must not receive `price`) |
| Tests | Are the three negative tests present — unauthenticated → 401, non-owner → 403/404, cross-tenant → 403/404 (404 hides existence)? |

Record **what is there**, not what should be there. Use file:line citations.

### 3. Surface the gaps

For every gap, answer:

- Which stage is missing or weak?
- Which actor can exploit it? (anonymous · authenticated non-owner · wrong tenant · lower role)
- Concrete impact? (cross-tenant read, privilege escalation, horizontal escalation)
- Minimum control to add? (policy method, scope, middleware, resource transform)
- Required negative test assertion?

Do **not** list generic findings ("should use policies") — always anchor to a
file:line and a specific actor who can reach the gap.

## Broken-access-control depth

Depth for the [`broken-access-control`](../../rules/broken-access-control.md)
rule (migrated here per P4 of `road-to-kernel-and-router.md`); the Iron Law and
the three negative tests stay in the rule.

Why this class dominates: the single most common — and most damaging — failure
in real systems and in AI-written code is that you log in as one user and see
another user's data. The login check passes, so the endpoint *feels* protected;
the per-object ownership/tenant check is a separate line that devs and AI omit —
especially when the object id comes straight from the request. Broken Access
Control is OWASP Web #1 (A01:2021) and API #1 (BOLA/IDOR), trivially
scriptable, and a recurring real-world breach class — e.g. First American
Financial (885M documents exposed via sequential ids with no ownership check).

### Non-optional controls (every data-returning surface)

- **Server-derived principal.** Ownership/tenant is derived from the session/token, **never** from a request header/param/body the caller controls. A matching id in the request is not authorization.
- **Ownership/tenant check on every request id** before returning data. `findById(params.id)` with no `where owner/tenant = currentPrincipal` is the canonical bug.
- **Tenant-scoped by construction.** Every query on a tenant table carries the tenant predicate; prefer a base scope that injects it so a forgotten clause can't leak. (German DSGVO: Mandantentrennung / Trennungskontrolle is a required TOM — a missing `tenant_id` filter is a compliance failure, not just a bug.)
- **Response minimization.** Return only the fields the caller is entitled to — no `SELECT *` / full-object serialization leaking PII "because the model has it" (Art. 25(2) by default).
- **Property-level authz (BOPLA / mass assignment).** Reject `role` / `user_id` / `tenant_id` / `is_admin` from the request body; explicit field allow-list, never whole-body binding.
- **Role/field-level output filtering (vertical BOPLA).** *Which* fields a principal receives depends on role + business rules — a driver role must not receive `price`; an office role must not receive the boss's `offer`. Serialize via a **role-scoped output DTO**, never the raw model / `to_json()`; sensitive fields (`price`/`cost`/`margin`/`salary`/`discount`/`offer`/internal notes) default-deny per role.
- **No guessable public ids** on sensitive resources — UUID/ULID, not sequential integers (turns one bug into full-DB enumeration).

### Role-based field-level access — both directions (vertical BOPLA + BFLA)

Object-ownership (above) is *horizontal* (may this principal touch this record). This is *vertical*: which **fields** and which **functions** a role may reach — the maintainer's case (driver ≠ price, office worker ≠ boss's offer). It depends on role + business rules, and **the server is the only boundary** — the frontend hiding a field does not protect it: the raw JSON on the wire is readable via `curl`/DevTools/a proxy (the 3Fun leak: a privacy toggle filtered only in the app; the server returned every user's location to a direct query).

- **Read side (CWE-213 / Excessive Data Exposure).** Build the response from a **role-scoped output DTO** — never serialize the ORM model directly. Sensitive fields default-deny per role. A client `?fields=` selection is ergonomics, not authorization — intersect it server-side with the role's read-allowlist.
- **Write side (CWE-915).** Bind input through a **role-scoped write-allowlist** — never the raw body. Read-allowed ≠ write-allowed: a role may *see* `status` but not *set* `status:"approved"`; the two allowlists are independent sets.
- **Function level (BFLA, OWASP API #5).** A role must not reach a function/verb reserved for a higher role. Gate **every mutating verb** (POST/PUT/PATCH/DELETE), deny-by-default — not just the GET you were asked about. The admin button being hidden is not a control.
- **Nested / GraphQL.** Field-level checks propagate to nested selections; a low-role token selecting a restricted field gets null/error, not data.
- **Negative tests, per (role × sensitive field), both directions:** lower-role token → the field is **absent from the raw response body** (assert the body, not the UI); lower-role setting the field on input → rejected/ignored, **verified by re-reading the persisted record**; every privileged verb → 403 for lower roles (403/404 on sensitive object reads).

### Defense-in-depth (so one miss can't leak)

Stack ≥2 independent layers on sensitive data — query-level ownership scoping, a centralized default-deny policy layer (a route with no policy is denied, not silently open), and DB row-level security as the backstop for a forgotten `WHERE tenant_id`. (Merged with the pre-existing Gotcha bullet "Defense-in-depth so one miss can't leak" below, which carries the concrete RLS configuration — that bullet is the stronger, operative statement.)

### GDPR / DSGVO — data protection by design

A cross-user data leak violates **Art. 5(1)(f)** (integrity & confidentiality — a principle → higher fine tier), **Art. 25** (by design/default: default-deny + least privilege + response minimization), and **Art. 32** — which also **mandates a process for regularly testing the effectiveness** of these controls (untested authz is a direct Art. 32 gap; this is why the three negative tests are non-optional). A discovered live exposure is a **notifiable breach** (Art. 33, 72 h from discovery) — surface it as "notify + remediate", never a silent patch. This is data-protection context, not legal advice → [`privacy-review`](../privacy-review/SKILL.md), `domain-safety-pii`.

### Backstop greps (authoring-time)

```bash
# Record fetched by request id with no owner/tenant predicate nearby (high-noise — a hit means read the line, not auto-fix)
rg -n '(findById|find|findOne|get)\(\s*(req\.|request\.|params\.|\$request|\$id)'
# Client-supplied tenant/user hint used as the scope (should come from the session)
rg -n '(tenant|tenantId|user_id|userId)\s*=\s*(req|request|params|headers|query)\.'
```

The full authoring-time grep set (mass-assignment, raw-serialization, secrets) lives once in [`ai-code-blindspots`](../ai-code-blindspots/SKILL.md).

A hit means read that line — is the ownership/tenant check present? Some are safe (already scoped); none should ship unchecked.

## Validation

Before finalizing the report, confirm:

1. Every entrypoint in scope is walked through **all six stages** of the table
2. Every 🔴 finding names: stage · actor · impact · missing control · required test
3. Every 🔴 finding cites at least one file path with line number
4. You have NOT listed stages that are already correctly enforced as findings
5. You have NOT confused authentication with authorization in any finding
6. You have NOT proposed exploit payloads, bypass chains, or offensive steps

## Output format

```
Skill:   authz-review
Targets: <routes / actions / jobs, one per line>

Per-entrypoint walk:
  <METHOD /route> — <controller@action>  (file:line)
    Auth gate:           <middleware/guard>   ✅/⚠️/❌
    Authorization:       <policy#ability>     ✅/⚠️/❌   (file:line)
    Data scope:          <scope/where>        ✅/⚠️/❌   (file:line)
    Response filter:     <resource/serializer> ✅/⚠️/❌  (file:line)
    Negative test:       <test path or "—">   ✅/⚠️/❌

Findings (prioritized):
  🔴  <name> — entrypoint · stage · actor
      Impact: <concrete damage>
      Missing control: <what to add, where>
      Required test: <negative assertion, test file>
  🟡  ...
  🟢  ...

Implementation plan:
  1. <control>, <file/layer>
  2. ...

Missing tests:
  1. <assertion>, <test file>
```

Severity: 🔴 reachable by external or cross-tenant/cross-user actor with
current privileges / 🟡 reachable only by elevated actor or requires
partial compromise / 🟢 defense-in-depth hardening, not a live exploit path.

Required fields (ordered):

1. **Skill** and **Targets** — entrypoints in scope
2. **Per-entrypoint walk** — six-stage table per entrypoint with file:line citations
3. **Findings** — prioritized, each with entrypoint · stage · actor · impact · missing control · required test
4. **Implementation plan** — ordered controls mapped to files/layers
5. **Missing tests** — ordered negative assertions

Runtime confirmation (e.g. *"reproduce the cross-tenant read against staging"*,
*"query the DB to prove scope leakage"*) is a follow-up for the implementer —
**this skill does not execute tools, run requests, or touch the database**.

## Gotcha

* **Authentication ≠ authorization.** A logged-in user is not an authorized
  user. Auth gate green does not make authorization green.
* **Implicit tenancy via current session** — `Auth::user()->posts` looks safe
  but breaks the moment an admin impersonation or service-account path bypasses it.
* **Query scope bypass through relations** — `$user->load('orders.customer')`
  can leak a sibling tenant if the `customer` relation has no scope.
* **Resource/serializer leakage** — the policy gated the action; the resource
  still exposed `internal_notes`. Response filter is a distinct stage.
* **"Route middleware covers it"** — middleware enforces auth, not per-record
  authorization. Still need the policy + scope.
* **Generic advice without file:line** — reject your own finding if you cannot
  cite the exact location.
* **The three negative tests are the security boundary.** Every protected
  entrypoint needs unauthenticated → 401, authenticated-non-owner → 403/404,
  and cross-tenant → 403/404. A happy-path 200 test proves nothing about access
  control (this is BOLA / IDOR — OWASP API #1). Untested authz is also a
  direct GDPR Art. 32 gap. See [`broken-access-control`](../../rules/broken-access-control.md).
* **Defense-in-depth so one miss can't leak** — stack ≥2 layers on sensitive
  data: query-level ownership scoping (base scope injects the predicate) + a
  centralized default-deny policy layer (a route with no declared policy is
  denied, not silently open) + DB row-level security (Postgres RLS `FORCE ROW
  LEVEL SECURITY`, tenant var via `SET LOCAL`) as the backstop for a forgotten
  `WHERE tenant_id`. A single layer is not enough.

## Do NOT

* NEVER return `clean` out of politeness when gaps exist — list them even if the change "probably works"
* NEVER silently fall back to generic advice when you cannot locate a stage — mark it `❌ not found` with the file you searched
* NEVER approve a 🔴 finding without a named required negative test
* NEVER propose exploit payloads, bypass chains, or offensive verification steps — if asked, stop per `never-help-build-offensive-cyber-capability`
* NEVER treat "only admins reach this" as a control without proof the admin gate is enforced at this stage for this request
* NEVER rubber-stamp authentication middleware as if it enforced per-record authorization

## References

- **OWASP ASVS v4.0.3** — Chapter V4 Access Control, especially V4.1
  (General Access Control Design) and V4.2 (Operation-level Access Control).
  [owasp.org/www-project-application-security-verification-standard/](https://owasp.org/www-project-application-security-verification-standard/)
- **OWASP Top 10 2021 — A01 Broken Access Control** — canonical failure modes
  (IDOR, missing function-level checks, forced browsing, metadata tampering).
  [owasp.org/Top10/A01_2021-Broken_Access_Control/](https://owasp.org/Top10/A01_2021-Broken_Access_Control/)
- **OWASP API Security Top 10 2023 — API1 BOLA** (Broken Object Level
  Authorization) and **API3 BOPLA** (property-level / mass assignment) — the
  API-layer names for the same object-ownership failures.
  [owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/](https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/)
- **NIST SP 800-53 AC family** — AC-3 Access Enforcement, AC-6 Least Privilege
  — rubric for "minimum control" recommendations.
  [csrc.nist.gov/projects/risk-management/sp800-53-controls](https://csrc.nist.gov/projects/risk-management/sp800-53-controls/release-search#!/800-53)
- [`threat-modeling`](../threat-modeling/SKILL.md),
  [`judge-security-auditor`](../judge-security-auditor/SKILL.md),
  [`security`](../security/SKILL.md),
  [`security-audit`](../security-audit/SKILL.md) — sibling review / implementation skills.
