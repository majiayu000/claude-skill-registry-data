---
name: web-recon
description: Recon and assess the attack surface of a web app/API you own or are authorized to test — endpoint enumeration, auth-posture matrix, BOLA/BFLA, cron checks, via web-recon-kit. Refuses unauthorized targets.
compatibility: Designed for Claude Code
metadata:
  allowed-tools: Read, Write, Edit, Bash, WebFetch
  argument-hint: [target-base-url]
  stability: experimental
---

# Web / API Reconnaissance & Assessment

**Target**: $ARGUMENTS

Drive the [web-recon-kit][kit] harness to enumerate and assess a web/API target. Every
target-specific detail lives in `scope.toml`; the runners are read-only (GET/OPTIONS), throttled,
and never trigger cron/mutation endpoints.

[kit]: https://github.com/qte77/web-recon-kit

## 0. Authorization gate (MANDATORY)

Before ANY request to the target, confirm the user **owns or is explicitly authorized** to test
it — their own workspace/account, a written pentest scope, an in-scope bug-bounty program, or a
CTF. If authorization is unclear, STOP and ask. Refuse targets the user does not control. Never
run against a third party "just to see."

## 1. Set up the target profile

- Ensure a `web-recon-kit` checkout is available, then run `make setup`, plus
  `make setup-browser` for the browser tier (installs polyfetch from GitHub + chromium via
  `uv sync --extra browser`).
- `cp scope.example.toml scope.toml`, then fill in:
  - `base_url`; `[identities.*].env` (env-var NAMES holding the API keys — keys live in `.env`,
    never in `scope.toml`);
  - `[recon].routes`, `[authmatrix].public_ok`, `[bfla].admin_prefixes`, `[[bola.collectors]]`.

## 2. Passive enumeration (no auth)

- `make inventory` — mine `/api/*` endpoints from the JS bundles.
- `make recon` — render each route, classify its gate (public / client-side /
  server-middleware), capture screenshots. Both need `make setup-browser`.
- Record anything reachable without authentication.

## 3. API testing (owner identity)

- `make authmatrix` — every endpoint × every configured identity, GET-probed → auth-posture
  matrix; flag unauthenticated 200s on non-public paths (then body-check them — an empty/generic
  200 is not a leak).
- `make cron` — confirm cron endpoints reject unauthenticated requests.

## 4. Authorization / tenant isolation

- `make bola` — cross-tenant **IDOR** (Insecure Direct Object Reference), a.k.a. **BOLA** (Broken
  Object-Level Authorization): collect owner resource IDs, replay them as a second tenant
  (`tenant_b`). A 200 == cross-tenant leak. Needs a 2nd tenant identity.
- `make bfla` — **BFLA** (Broken Function-Level Authorization): probe admin / **RBAC** (Role-Based
  Access Control) endpoints as a low-role member; any success is privilege escalation.

Abbreviations are expanded on first use here; the web-recon-kit repo carries a fuller
`docs/glossary.md`.

## 5. Aggregate + verify

- `make report` → `results/report.md`.
- Run the harness's `verify_findings` workflow (agentic, adversarial) over candidate findings
  BEFORE writing anything up — independent panels judge each; a 200 may be a legitimately-public
  resource, `403 ≠ leak`, and status alone rarely proves a cross-tenant read.

## 6. Report

Produce a **provenance-tagged** report: which tool established each fact (curl / WebFetch /
polyfetch / harness), severity, and a repro. Separate **confirmed** findings from **candidates**.
Recommend remediation.

## Safety rails

- Read-only by default; mutating verbs are never emitted (cron/BOLA/BFLA probes are GETs).
  Any `--danger-post`-style path requires an explicit, disposable environment.
- Throttled per-host (`rate.per_host_delay_ms`) — never DoS; no mass-fuzzing without authorization.
- `scope.toml`, `results/`, and the generated inventory are git-ignored (they hold target data).
- BOLA and schemathesis need extra inputs (a 2nd identity / an OpenAPI spec); the runners skip
  cleanly when those are absent — report the gap rather than silently covering less.
