---
name: auth-and-authz
description: Authentication & Authorisation control plane for Yuzu — the canonical entry point for any work on RBAC, OIDC SSO, SAML, SCIM, MFA/TOTP, AD/Entra integration, API tokens, session lifecycle, enrollment, and the audit/evidence chain. Use when the user says "/auth-and-authz", "/auth", "/iam", asks to plan or implement an enterprise A&A feature, asks "what's our auth gap to enterprise readiness", asks to audit current auth state against SOC 2 CC6.x / Workstream B, or starts work that touches `auth_*`, `rbac_*`, `oidc_*`, `api_token_*`, `enrollment_*`, or `cert_store.*`. The skill bundles current-state inventory, required-features inventory, gap matrix, the canonical workflow for adding a new A&A feature, and the load order for the routed reference docs.
---

# Authentication & Authorisation skill

The single entry point for any A&A work in Yuzu. Bundles three things:

1. **Current state** — what's shipped today and where it lives.
2. **Required state** — the enterprise/SOC 2 feature set we owe customers.
3. **Gap matrix + workflow** — what's missing and the standard procedure for
   closing a gap.

This skill does NOT replace the routed docs or specialist agents. It tells
you which to load, in which order, and what questions to ask before you
start cutting code.

---

## Usage

```
/auth-and-authz                # default: print gap matrix + suggested next gaps
/auth-and-authz audit          # produce a compliance-ready snapshot of A&A state
/auth-and-authz plan <feature> # plan-only walk-through for a single feature (e.g. SAML, SCIM, TOTP)
/auth-and-authz implement <feature>  # full workflow: plan → governance → implement → test → docs
```

If the user invokes the skill without a subcommand, default to printing the
**gap matrix** (Section 3) and asking which gap they want to work on.

---

## 1. Current state — what's shipped

Authoritative reference: `docs/auth-architecture.md`. Read it before this
skill claims anything is "done."

### Shipped capabilities

| Capability | Status | Source of truth |
|---|---|---|
| Local password auth (PBKDF2-SHA256) | Shipped (v0.10) | `auth.cpp:69` `pbkdf2_sha256()` (OpenSSL `PKCS5_PBKDF2_HMAC` + BCrypt path) |
| Persistent auth store (`auth.db`, SQLite) | Shipped (v0.12) | `auth_db.cpp:222-236` chmod 0600 + L402 `MigrationRunner::run`; agent-doc `.claude/agents/authdb.md` |
| Session-cookie auth (HTMX dashboard) | Shipped | `auth_routes.cpp:43,386` (`extract_session_cookie`, `Set-Cookie: yuzu_session=…`) |
| API tokens — Bearer + `X-Yuzu-Token` | Shipped | `api_token_store.cpp` (store); both header forms parsed at `auth_routes.cpp:108-119` |
| Owner-scoped token revocation (#222) | Shipped | `rest_api_v1.cpp:1058-1082` (owner-vs-admin check at L1060) |
| Granular RBAC — 6 roles × **19** securable types × 6 ops | Shipped (Phase 3) | `rbac_store.cpp:129-193` — types: Infrastructure, UserManagement, InstructionDefinition, InstructionSet, Execution, Schedule, Approval, Tag, AuditLog, Response, ManagementGroup, ApiToken, Security, Policy, DeviceToken, SoftwareDeployment, License, FileRetrieval, GuaranteedState; ops: Read/Write/Execute/Delete/Approve/Push |
| Self-target principal-destruction guard (#397/#403) | Shipped | `settings_routes.cpp:434,1830,2488-2504` (3 call sites); design in `docs/auth-architecture.md` §self-target |
| OIDC SSO — full PKCE flow, Entra discovery, JWT validation | Shipped | `oidc_provider.cpp:189` `generate_code_verifier()`, L194 `compute_code_challenge()`, L385 `code_verifier` post, L766 `/.well-known/openid-configuration` discovery, L542/L623 JWKS fetch + JWT signature verify |
| Directory Sync — AD/Entra users + groups + role mapping via Microsoft Graph v1.0 | Shipped | `directory_sync.cpp:336,509,556,608` calls `https://graph.microsoft.com/v1.0/users`, `/groups`, `/groups/{id}/members`; persisted `directory_group_role_mappings` + `directory_sync_status` tables (`directory_sync.cpp:147`). NOTE: `oidc_provider.cpp:248` only parses the JWT `groups` claim — Graph integration is the separate Directory Sync subsystem. |
| mTLS for agent ↔ server | Shipped | `main.cpp:111` `--ca-cert` flag; peer-cert identity match in `agent_service_impl.cpp:47,354` |
| Windows certificate-store mTLS (CryptoAPI/CNG) — **agent-side only** | Shipped | `agents/core/src/cert_store.cpp:78,84,199-201` (`CertOpenStore`, `NCrypt` CNG export) |
| HTTPS-by-default, secure bind default (127.0.0.1) | Shipped (hard invariant) | `main.cpp:100` 127.0.0.1 default, L216 `--no-https` opt-out; design in `docs/auth-architecture.md` |
| HTTP security headers — six (CSP, HSTS, X-Frame-Options, X-Content-Type-Options, Referrer-Policy, Permissions-Policy) | Shipped (SOC2-C1) | `security_headers.cpp:187-195` (HSTS conditional on HTTPS responses) |
| Cert hot-reload (HTTPS) with audit + metrics | Shipped | `cert_reloader.cpp:31` audit `cert.reload`, L80 watcher loop, L114-191 atomic `SSL_CTX` swap |
| Agent enrollment — pre-shared / platform-trust (auto-approve via attestation_provider) / admin-approval queue (3 tiers) | Shipped | `auth.cpp:717-948` + `agent_service_impl.cpp:67-189` (pre-shared L70, attestation auto-approve L101-136, pending-admin queue L138-189) |
| MCP token issuance + tier-before-RBAC ordering | Shipped | `mcp_server.cpp:556-557,591,599` (tier check at L591 precedes RBAC at L599); design in `docs/mcp-server.md` |
| `auth.admin_required` denied audit on every 403 | Shipped (gate) | `auth_routes.cpp:150` inside `require_admin` |
| Private-key permission validation | Shipped | `cert_reloader.cpp:120` `validate_key_file_permissions()` (helper in `file_utils.hpp`); called at startup from `server.cpp` and on hot-reload |
| Metrics endpoint localhost-only-no-auth | Shipped | `server.cpp:1621` (loopback always unauthenticated; remote behavior toggled by `cfg.metrics_require_auth`) |

---

## 2. Required state — enterprise / SOC 2 readiness

Source of truth: `docs/enterprise-readiness-soc2-first-customer.md`
**Workstream B — Identity, Access, and Administrative Security** (§3.2).
SOC 2 alignment: CC6.1 (logical access), CC6.2 (provisioning), CC6.3
(authentication), CC6.6 (privileged access), CC6.7 (change in role), CC6.8
(termination), CC7.2 (anomalies → audit).

### Required-but-not-yet-shipped feature inventory

| Feature | Workstream B line | SOC 2 link | Gap class |
|---|---|---|---|
| **MFA / 2FA / TOTP for high-risk approvals** | "2FA/TOTP for high-risk approvals" | CC6.6 | **MISSING** |
| **Hardened-mode local-password disable** | "Disable local-password fallback in hardened mode" | CC6.3 | **MISSING** |
| **Break-glass account policy** (constrained, audited, rotated) | "or tightly constrain break-glass account policy" | CC6.6 | **MISSING** |
| **SAML 2.0 SP** (some enterprises require SAML, not OIDC) | implicit ("SSO enforcement") | CC6.1 | **MISSING** |
| **SCIM v2 provisioning** (auto-provision/deprovision from IdP) | "Periodic access reviews" automation | CC6.2/6.8 | **MISSING** |
| **Just-in-time admin elevation** (time-boxed role promotion + audit) | "Role-based least privilege and separation of duties" | CC6.6 | **MISSING** |
| **Inactivity session timeout** — `auth_db.cpp:363` reserves `last_activity_at` column with DEFAULT but **no `UPDATE` writes anywhere** in the codebase; expiry-only today. Treat as from-scratch work, not a tweak. | "inactivity timeout" | CC6.3 | **MISSING (column reserved)** |
| **Session revocation REST surface** — DB primitive `AuthDB::invalidate_all_sessions()` shipped at `auth_db.cpp:740` / `auth_db.hpp:136`, fires only via `remove_user`/`update_role`. **No `DELETE /api/v1/sessions` route, no admin UI button.** | "expiration, revocation" | CC6.3 | **PARTIAL — DB only** |
| **API token rotation workflow** — UI-driven pair-of-tokens overlap. No `rotate` symbols in `api_token_store.{cpp,hpp}` today; only create + revoke. | "rotation process" | CC6.3 | **MISSING** |
| **API token inventory + last-used view** — data layer shipped (`api_tokens.last_used_at` written/read at `api_token_store.cpp:291,325-345`); dashboard inventory view missing. | "token inventory" | CC6.6 | **PARTIAL — UI only** |
| **Periodic access reviews** (export of role assignments + attestation flow) | "Periodic access reviews with manager/security attestation" | CC6.2 | **MISSING** |
| **Account lockout after N failed logins** | implicit (auth hygiene) | CC6.3 | **MISSING** |
| **Service-account governance** (separate principal type, no human login) | "Privileged access controls" | CC6.6 | **MISSING** |
| **Conditional access** (geo / IP / device posture, optional) | implicit ("MFA requirements") | CC6.1 | **MISSING (P3)** |
| **Sampled auth-log evidence export** for auditors | "sampled auth logs" | CC7.2 | **MISSING** |
| **Self-managed Certificate Authority** — issuer for (a) mTLS server + agent certs and (b) plugin code-signing certs. CSR API, lifecycle (issue / renew / revoke), audit chain. Today operators must bring their own PKI for both surfaces. | implicit ("certificate management lifecycle") | CC6.1 / CC6.7 | **MISSING** |
| **Plugin code-signing trust anchor** — operator-configured PEM trust bundle on the agent, CMS-verify of `<plugin>.sig` against it before `dlopen`. *Trust bundle accepts any X.509 root — Yuzu's self-managed CA (future) or any public CA / operator-internal CA today*. | implicit ("supply-chain integrity") | CC6.1 / CC7.1 | **PARTIAL — verifier shipped, CA upstream pending** |

### Hard invariants that must NOT regress when adding any of the above

These are pulled from `docs/auth-architecture.md` and
`.claude/agents/authdb.md`. Every PR adding a feature in Section 2 above
must check them:

- HTTPS by default; refuse to start without `--https-cert` + `--https-key`
  unless `--no-https` is passed.
- Web UI binds 127.0.0.1 by default; warn at startup if overridden.
- Private-key files must not be group/others-readable on Unix.
- Every error response uses the structured JSON envelope.
- Six security headers on every HTTP response.
- All SQL parameterised; no string interpolation.
- Self-target principal-destruction guard applied to any new
  destructive/demoting endpoint.
- `auth.db` 0600 / restricted ACL at create.
- `MigrationRunner::run` for any new schema migration.
- `unique_ptr<AuthDB>` lifetime spans `Server::create()`.
- `yuzu-server.cfg` is a one-shot first-boot seed, not a live source.
- `POST /api/settings/users` `role` field stays ignored; role changes only
  via the dedicated endpoint.
- `require_admin` emits `auth.admin_required` denied audit on every 403.
- New code never holds `AuthDB::mu_` while publishing to a sibling
  subsystem's bus.

---

## 3. Gap matrix — priority order

Recommended order for closing gaps. Each block stands alone; pick whichever
matches the customer ask.

### Priority 0 — needed for first enterprise customer

1. **MFA / TOTP for admin login + high-risk approvals.** Standard `oath-toolkit`
   compatible; secret generation + QR enrollment + step-up flow on
   privileged endpoints. Schema additions land via `MigrationRunner`. New
   audit actions: `mfa.enroll`, `mfa.verify`, `mfa.step_up.required`,
   `mfa.step_up.passed`.
2. **Account lockout after N failed logins.** Simple: per-user counter +
   timestamp in `auth.db`, reset on success, configurable threshold. Audit:
   `auth.lockout.applied`, `auth.lockout.cleared`. Closes a basic
   credential-stuffing surface. *Lowest-risk P0 to implement first — good
   workflow shake-out.*
3. **Hardened-mode local-password disable.** New CLI flag
   `--auth-mode=sso-only`; `auth_routes.cpp` rejects local-password login
   with a clear message and logs `auth.local_disabled`. Break-glass account
   policy: a single named principal exempt from the flag, with mandatory
   MFA + 24h auto-disable + every action logged at `critical`.
4. **Sampled auth-log evidence export.** New REST endpoint
   `GET /api/v1/audit/auth-sample?from=...&to=...&limit=N` admin-only,
   gated by `require_admin`, returning a pseudo-random sample. SOC 2 CC7.2
   evidence chain.
5. **Session revocation REST surface** *(promoted from P1 — DB primitive
   already shipped)*. `DELETE /api/v1/sessions?user=<name>` admin-only that
   calls the existing `AuthDB::invalidate_all_sessions()` (`auth_db.cpp:740`)
   plus an admin-UI "Revoke all sessions" button. Audit: `session.revoke_all`.
   Self-target guard applies (admin can't lock themselves out). Cheaper than
   MFA, same SOC 2 control box (CC6.3 / CC6.8).

### Priority 1 — enterprise-friction reducers

6. **SAML 2.0 SP** with metadata exchange + signed assertion validation.
   Mirrors OIDC's group-to-role mapping. Same enforcement surface as OIDC.
7. **SCIM v2 provisioning** — auto-create/disable users from the IdP.
   Reuses `auth.db` user table; new endpoint surface under `/scim/v2/`
   with bearer-token auth (separate from operator API tokens).
8. **Inactivity session timeout** — wire the reserved `last_activity_at`
   column at `auth_db.cpp:363` end-to-end: per-request `UPDATE` on every
   authenticated touch, expiry check inside `validate_session()` against
   `now - last_activity_at > inactivity_window`, configurable per
   deployment. Treat as from-scratch since no `UPDATE` writes exist today.
9. **JIT admin elevation** — `POST /api/v1/elevate` accepting a justification
   + duration; promotes the caller's effective role for the window, audits
   `role.elevation.requested|granted|expired`. Returns to base role on TTL.
10. **Self-managed Certificate Authority (mTLS + code signing).** A single
    PKI root, server-managed, that operators can use instead of standing up
    their own CA. Two consumers:
    - **mTLS** — issue server certs and per-agent client certs against the
      Yuzu CA so an out-of-the-box deployment doesn't require an external
      PKI. Today `--ca-cert` consumes whatever bundle the operator hands
      over; the new flow lets the server *be* the CA.
    - **Plugin code signing** — issue developer signing certs whose chain
      anchors at the same root, so the agent's `--plugin-trust-bundle`
      points at one PEM and the operator can sign their own plugins. The
      verifier (issue #80, shipped) is already deployment-format-agnostic:
      same code path accepts public-CA, internal-CA, and self-managed-CA
      issued certs. The CA closes the operator UX gap, not a security gap.

    Surface required:
    - Schema additions via `MigrationRunner`: `ca_root` table (root key +
      cert + lifecycle), `ca_issued` table (issued cert inventory + status
      + revocation reason), `ca_crl_versions` table.
    - REST: `POST /api/v1/ca/issue` (CSR in, cert chain out),
      `POST /api/v1/ca/revoke`, `GET /api/v1/ca/crl` (DER CRL stream),
      `GET /api/v1/ca/root` (root cert PEM, public).
    - Audit actions: `ca.root.created`, `ca.cert.issued`, `ca.cert.revoked`,
      `ca.crl.published`.
    - RBAC: gated under the existing `Security` securable type with
      `Read` (root + CRL) / `Write` (issue) / `Delete` (revoke) ops.
    - Hardening: root key encrypted at rest using existing
      `auth.db`-style 0600 file or, preferred, an HSM/keyring abstraction
      that today wraps OpenSSL `EVP_PKEY` and tomorrow can target PKCS#11.

    Plugin code-signing intersects this: when the CA ships, the agent's
    `--plugin-trust-bundle` simply points at `/var/lib/yuzu/ca/root.pem`
    and the operator's plugin build pipeline calls `POST /api/v1/ca/issue`
    to mint a signing cert. No verifier change required.

### Priority 2 — long-tail polish

10. **API token rotation workflow** — pair-of-tokens overlap window in the
    dashboard; "Rotate" creates a new token while the old keeps working
    until the operator confirms cutover.
11. **API token inventory view** — surface the existing `last_used_at` /
    owner / created_at columns from `api_token_store.cpp:325-345` into a
    sortable Settings → API Tokens UI. (Data layer already shipped; this
    is a dashboard-only PR.)
12. **Periodic access-review export** — JSON/CSV of `(user, role, last_login)`
    triples plus an attestation upload endpoint.
13. **Service-account principal type** — distinct from human users, no
    login surface, only token auth, mandatory rotation.

### Priority 3 — defer

14. **Conditional access policies** (geo / IP / device posture) — large
    scope, niche customer ask. Defer until specifically requested.

---

## 4. Standard workflow for adding an A&A feature

For every feature in Section 3:

1. **Read first.** In order:
   - This skill (current file) for the gap framing.
   - `docs/auth-architecture.md` for the existing auth surface and hard
     invariants.
   - `docs/enterprise-readiness-soc2-first-customer.md` §3.2 for the
     enterprise/SOC 2 framing.
   - `.claude/agents/authdb.md` if the feature touches `auth.db`.
   - `docs/mcp-server.md` if the feature touches the MCP surface.

2. **Plan.** Produce a short plan covering:
   - Schema changes (must use `MigrationRunner`).
   - REST surface additions and the RBAC permission required.
   - Audit actions (always emit on the `require_admin` gate side and on
     every state mutation).
   - Self-target guard implications (does this destroy/demote a principal?).
   - Test plan: unit (`tests/unit/`), integration if it touches multiple
     stores, a puppeteer smoke if it touches the dashboard.

3. **Implement** with a single PR per feature. Drive every change through
   `MigrationRunner` for schema, `HeaderBundle::make()`/`apply()` for any
   header touch, `require_admin` for the admin gate, and parameterised SQL
   throughout.

4. **Test.** Run `/test --quick` before commit. The
   `tests/unit/server/test_auth_db_pg.cpp` and
   `tests/unit/server/test_auth_routes.cpp` patterns are the reference. Their
   Postgres cases need `YUZU_TEST_POSTGRES_DSN`; without it they report SKIP,
   so set it before treating `/test --quick` as coverage.

5. **Governance.** Run `/governance dev..HEAD` before pushing — Gate 2
   (security-guardian + docs-writer mandatory deep-dive) plus the AuthDB
   review agent (`.claude/agents/authdb.md`) for any `auth_db.*` touch.
   CRITICAL/HIGH findings block merge.

6. **Docs.** docs-writer always picks up the user-manual + REST API
   updates during Gate 2; verify the change is in the findings report
   and ship the doc edit in the same PR (or the immediate follow-up).

7. **Compliance evidence.** For features that close a SOC 2 control gap,
   add an entry to `docs/security-reviews/` for the change record. The
   compliance-officer agent will catch this in Gate 6.

---

## 5. Cross-references

- **Routed reference doc:** `docs/auth-architecture.md`
- **AuthDB review agent:** `.claude/agents/authdb.md`
- **Security review agent:** `.claude/agents/security-guardian.md`
- **MCP token + tier policy:** `docs/mcp-server.md`
- **Enterprise readiness plan:** `docs/enterprise-readiness-soc2-first-customer.md`
- **SOC 2 evidence pattern:** `docs/security-reviews/*` and audit-log
  emission via `audit_store.cpp`.
- **Operator runbook:** `docs/ops-runbooks/auth-db-recovery.md`.
