---
name: convex-remote-mcp
description: >-
  Remote MCP server in an existing Convex backend, WorkOS AuthKit OAuth, anti-leak projections, prod rollout. Use for `convex-mcp-gateway`, "MCP gateway Convex", "un MCP pour ce projet Convex", "expose mes fonctions Convex à Claude", clock tool stale or off by timezone (getCurrentDate/isOverdue).
---

# Convex Remote MCP — production-ready, repeatable

This skill builds a **remote MCP server (Streamable HTTP, protocol `2025-06-18`)
hosted inside an existing Convex backend** — not a separate service. It mounts the
[`convex-mcp-gateway`](https://www.npmjs.com/package/convex-mcp-gateway) component in
one line, exposes `$CONVEX_SITE_URL/mcp`, authenticates clients with **WorkOS
AuthKit** (OAuth 2.1 + PKCE, DCR/CIMD), verifies the resource-bound JWT **locally
against the JWKS**, gates access by an **allowlist**, and — critically — wraps every
tool in an **anti-leak projection layer** so no raw Convex document, `_id`, or PII
reaches the LLM.

It is the distilled, reusable form of a real end-to-end build. The companion
**source of truth** is the playbook (read it once, in full, before you start):
`~/.claude/skill-drafts/convex-mcp-production-playbook.md`. If that file is absent,
tell the user and stop — do not guess its contents.

## When to use / not use

**Use** for: standing up a Convex-backed remote MCP connector, adding WorkOS OAuth
to one, fixing a leak/auth/projection issue in one, or rolling one to production.

**Don't use** for: a generic non-Convex MCP server (that's `mcp-builder`), a local
stdio MCP, or building the Convex *app* itself (that's `convex` / `convex-expert`).

## How to drive this skill

This is a **multi-phase build with hard verification gates**, not a single edit.
Work the phases in order. SKILL.md is the orchestrator; each phase points to one
reference file you read **just before** doing that phase (progressive disclosure —
don't preload all five). Bundled templates and scripts do the repetitive parts.

### Phase 0 — Collect the project parameters

Fill the parameter table in `references/parameters.md` **with the user** first (server name,
dev/prod `.convex.site` origins, AuthKit domain, allowlist table/index, timezone, mount
path, tool catalog). Every template uses them as `<PLACEHOLDERS>`; never hardcode the
example values. Also confirm the one-time prerequisites listed there.

### Phase 1 — Architecture & wiring  →  read `references/architecture.md`

Understand the topology (request-flow diagram included) and env-var contract, then install + wire the component:
`convex.config.ts` (`app.use(mcpGateway)`), instantiate the gateway, mount the HTTP
route on **both `<MCP_PATH>` and `<MCP_PATH>/`**, and add the well-known routes.
Templates: `assets/templates/convex.config.ts`, `http.ts`, `gateway.ts`. The single
source of truth for **environment variables** lives in this reference (§ env table) —
every later phase refers back to it instead of re-listing vars.

### Phase 2 — OAuth (WorkOS AuthKit)  →  read `references/auth-workos.md`

The full, self-contained OAuth contract: WorkOS dashboard config (enable DCR + CIMD,
register the resource indicator **with and without trailing slash**), the local JWKS
verify (`resolveIdentity` / `verifyAccessToken`), the `authorize` allowlist gate, the
`configureOAuth` one-shot internalMutation (defaults to the **issuer**, not
`CONVEX_SITE_URL`), and the well-known routes. Includes the bridge-mode requirements
for non-WorkOS IdPs and the OAuth pitfalls (`application_not_found`, `invalid_target`,
userinfo-rejects-token, wrong well-known path).

### Phase 3 — Anti-leak projection layer  →  read `references/anti-leak-projections.md`

The heart of the security model. Dispatch returns the handler value **VERBATIM**, so
**every** tool that could return a raw Convex doc needs an `internal*` projection
wrapper with **whitelisted fields only** (never `return ctx.db.get(...)`). Covers the
projection wrapper pattern, the read/detail vs list split, the **clock-in-action**
rule (clock values belong in `internalAction`, never `internalQuery`), `identityArg`
vs the `authorize`-time allowlist, and **audit redaction for reads AND writes**
(`writeRedacting` / `readRedacting`). Template: `assets/templates/mcp-functions.ts`.

### Phase 4 — Tests & verification  →  read `references/tests-verification.md`

The gate discipline — **never trust the typecheck alone**. Static validate →
`convex dev --once` (the real gate) → `configureOAuth` → **runtime READ-ONLY probes**
→ test-data hygiene (seed → probe → delete → drop the temp file) → smoke test →
**adversarial PR review** (the `adversarial-pr-review` skill; a PreToolUse hook blocks
`gh pr create` until it passes) → re-verify after fixes → commit. This reference also
carries the **anti-bug checklist** (the hard-won correctness traps: arg-boundary
non-ASCII keys, clock-in-query, emoji surrogate truncation, timezone, ICU "24", date
round-trip validation, shallow-merge, allowlist bypass, audience-empty, bash `set -u`,
406-vs-401). Scripts: `scripts/mcp-smoke-test.sh`, `scripts/verify-gates.sh`.

### Phase 5 — Production rollout  →  read `references/rollout-prod.md`

dev and prod are **separate DBs + env-stores**, so everything is re-done with `--prod`:
Vercel-coupled `convex deploy`, prod env vars (the §env table again), prod allowlist
seed, `configureOAuth --prod` (the easy-to-forget last brick), WorkOS resource
indicators for the prod URL (both slash forms), prod smoke test, then the claude.ai
connector. Includes the rollout pitfalls (orphan `_cleanup_tmp.ts`, circular type
inference sites, sentinel keyed on HEAD, multi-account git remotes).

## Bundled resources

Read references as you reach each phase (don't preload). Copy templates into the target
project and substitute the Phase-0 parameters.

- Templates in `assets/templates/`: `convex.config.ts`, `gateway.ts`, `http.ts`,
  `mcp-functions.ts`, `timezone.ts` (ICU-24 and date round-trip guards, drop if no date tools).
- Scripts: `scripts/mcp-smoke-test.sh` (auth + protocol smoke test), `scripts/verify-gates.sh`.

## Non-negotiables (the hard-won lessons)

These are the principles that distinguish a working build from a leaky/insecure one.
Each links to where the detail lives. Internalize them — they're *why* the skill exists.

- **Dispatch is VERBATIM ⇒ projection is mandatory.** The component returns the
  handler's value untouched to the LLM. Any tool that could return a raw doc leaks
  `_id`/`_creationTime`/PII — and an `_id` surfaced as e.g. `eventId` gets reinjected
  into an update tool and "can't be found". Wrap with whitelisted-field `internal*`.
  (Phase 3)
- **Projection ≠ audit redaction.** `auditArgs.redact` only scrubs the recorded
  *input args*; it never reshapes the *response*. A `WRITE`+redact tool is not
  response-safe. Redact audit for **reads and writes** that carry PII. (Phase 3)
- **Verify the JWT LOCALLY against the JWKS** (RS256 via `crypto.subtle`, no `jose`) +
  mandatory `iss`/`aud`/`exp`. **Never** call userinfo — a resource-bound token is
  rejected there. (Phase 2)
- **Trust only a VERIFIED email.** Management API (authoritative) or a token `email`
  with `email_verified === true`. No `preferred_username` fallback (spoofable); test
  each claim `typeof === 'string'` so a non-string can't short-circuit. (Phase 2)
- **Everything is `internal*`** and reachable only through the gateway after the
  allowlist check. A public function bypasses all MCP auth. (Phase 3)
- **Clock values live in `internalAction`, never `internalQuery`** — a query caches
  and freezes the date (notably across midnight). Split into a `*Rows` query + an
  action wrapper that reads the clock. (Phase 3 / anti-bug checklist)
- **Fail CLOSED everywhere.** A missing env var (`MCP_UPSTREAM_ISSUER`,
  `CONVEX_SITE_URL`) must DENY (→ 401), never silently disable a check; require
  `audiences.length > 0`; never negative-cache JWKS/email. (Phase 2)
- **Apply correctness fixes SYMMETRICALLY** to the MCP wrappers and the in-app tools
  via a shared helper, or behavior drifts between the two surfaces. (Phase 4)
- **Never commit on a red gate.** Static validate → `convex dev --once` → runtime
  probes → smoke test → adversarial review, in that order. The typecheck does not see
  codegen/validators/`internal.*` resolution; `convex dev --once` is the real gate.
  (Phase 4)
- **Run the adversarial review LAST**, after every fix is committed — its sentinel is
  keyed to HEAD, and any new commit re-blocks `gh pr create`. (Phase 4)

## Critical reminders

- **Read the playbook in full first.** It is the source of truth; this SKILL.md is the
  index over it. Parameterize, don't copy the COBACAM example values.
- **dev ≠ prod.** Separate DB and env store — re-seed the allowlist, re-run
  `configureOAuth --prod`, re-add WorkOS resource indicators, re-probe with `--prod`.
- **`configureOAuth` must run** (per deployment) or `/.well-known/oauth-protected-resource<MCP_PATH>`
  returns `"OAuth discovery not configured"` and login is impossible.
