---
name: security-audit
description: Run OpenAlgo Desktop's periodic security review and write it up as a dated markdown report under docs/audit/<date>/. Use for the monthly review, before a release or a v* tag, after a dependency bump (Cargo.lock, package-lock.json), after adding a public route, webhook, broker callback, Tauri capability or secret store, or when asked for a security check, vulnerability scan, dependency audit or audit report.
---

# Security audit (desktop)

Threat model: single user, local machine. Whoever controls the OS account
controls the app. The job is to keep secrets off disk in usable form, out of
logs, and away from anything that is not the signed-in user: another local
process, a web page in the trader's browser, a LAN peer when the trader binds
beyond loopback, a forged broker callback. Weight triage accordingly; IDOR
and role bypass do not apply.

Apply the `verify` skill throughout: every control below is checked by
running it (a test, a request, a scanner), never by reading alone, and a tool
that did not run is reported as not run.

## 1. Dependency and secret scanners

Run each, record the command, the tool version and the result. CI runs the
same set in `.github/workflows/security.yml` (weekly and on lockfile
changes), `ci.yml` (gitleaks on every push) and `codeql.yml`.

```bash
# Rust advisories, licenses, bans, sources (the single place advisories are accepted)
cargo deny --manifest-path src-tauri/Cargo.toml --config .github/deny.toml --locked \
  check advisories bans licenses sources

# RustSec, with the ignores taken from deny.toml (exactly what security.yml does)
ignore_args=(); while IFS= read -r id; do ignore_args+=(--ignore "$id"); done \
  < <(grep -vE '^[[:space:]]*#' .github/deny.toml | grep -oE 'RUSTSEC-[0-9]{4}-[0-9]{4}' | sort -u)
cargo audit --file src-tauri/Cargo.lock "${ignore_args[@]}"

# JavaScript: production dependencies, fail on high or critical
npm audit --omit=dev --audit-level=high
npm audit --omit=dev --json > /tmp/npm-audit.json   # triage moderate and low too

# Secrets in the full history, and in a branch's own commits
gitleaks git --no-banner -c .github/gitleaks.toml --redact .
gitleaks git --no-banner -c .github/gitleaks.toml --log-opts="origin/master..HEAD" .

# Filesystem: lockfile vulnerabilities and secrets, with the accepted list
trivy fs --scanners vuln,secret --severity CRITICAL,HIGH,MEDIUM \
  --skip-dirs node_modules,src-tauri/target,dist --ignorefile .trivyignore .

# CodeQL (rust, javascript-typescript, actions): read the open alerts
gh api "repos/marketcalls/openalgo-desktop/code-scanning/alerts?state=open&per_page=100" \
  --jq '.[] | [.rule.security_severity_level, .rule.id, .most_recent_instance.location.path, .most_recent_instance.location.start_line] | @tsv'
```

`cargo-deny` and `gitleaks` are installed on the maintainer's Mac;
`cargo-audit` and `trivy` may not be. If one is missing, install it or read
the latest CI run's artifact (`gh run list --workflow security.yml`, then
`gh run download <id>`), and say which you did. An unrun scanner is a gap in
the report, not a pass. CodeQL config: `.github/codeql/codeql-config.yml`
excludes `src-tauri/tests/**`, `*.test.ts(x)` and `e2e/**`; an alert inside a
`#[cfg(test)]` module in `src-tauri/src` is dismissed as "used in tests" only
after checking it really sits in a test module.

## 2. The attack surface, control by control

For each, name the code, run the test that proves it, and try one hostile
request yourself against a test server (never the trader's running app, never
ports 5000/8765/5500/8766 on this machine; the integration harnesses bind
ephemeral ports).

| Surface | Control | Code | Proof to run |
| --- | --- | --- | --- |
| `/api/v1/*` | 503 with the locked sentence before any key check while nobody is signed in (KEY-01); API key in the JSON body (the `X-API-KEY` header alone is a 400, as on the web); HMAC index plus Argon2 with the web's caches (verified 10 h, invalid 5 min); 403 on a bad key; failures (a key in the URL included) throttled per network address (never this computer, per key behind a tunnel) in the budget `/mcp` and the feed share (`middleware::credential_locked`); cross-site requests refused before anything counts; 100/s per IP | `server/api_v1/`, `services/apikey_service.rs`, `security/hashing.rs`, `server/ratelimit.rs` | `cargo test --lib server::tests::bad_api_keys_are_throttled_per_ip`, `api_rate_limit_is_100_per_second_per_ip_with_flask_body`, `server::tests::security::s02`; `tests/it/api_v1_contract.rs` |
| Sign-in `/auth/login`, `/auth/login/totp`, reset and 2FA codes, current password | from the app's own page only (`sign_in_origin_ok`), refused before counting; per-address request limit (5/min, 25/h); failure budget per source and account, claimed before the password is checked, 30 s doubling to 5 min; unknown names cost the same Argon2 work | `server/routes/auth.rs`, `server/middleware.rs`, `server/ratelimit.rs` `LoginBackoff` | `cargo test --lib server::tests::security::s02`, `server::ratelimit` |
| Callers and bans | `middleware::classify` once per request, stored as `Source`: a loopback peer is local only with no forwarding header and the app's own `Host`; no forwarding header is ever read as an address; tunnel callers share one identity, never banned, matching no allowlist; bans and allowlists apply to network peers by canonical address, on every surface including the feed | `server/middleware.rs`, `server/addr.rs`, `services/monitor.rs`, `feed/auth.rs` | `cargo test --lib server::tests::security::s03`, `server::addr` |
| `/api/v1/telegram/notify`, `/api/v1/whatsapp/notify` | the only endpoints that also read `X-API-KEY` (web parity) | `server/api_v1/notify.rs` | the notify tests in `tests/it/messaging.rs` |
| Browser session routes | every route declared in `server/routes/mod.rs` `table()` with an `Access` level; `require_user` / `require_user_for_json`; cookie `HttpOnly`, `SameSite=Lax`; CSRF token (`X-CSRFToken` or form `csrf_token`) plus `sec-fetch-site` same-origin check on every write; `csrf_exempt` list in `server/middleware.rs` | `server/middleware.rs`, `server/form.rs`, `session/web.rs` | `every_user_route_rejects_without_a_signed_in_session`, `public_route_list_is_exactly_the_reviewed_one`, the CSRF tests in `server/tests.rs` |
| Broker callbacks `/{broker}/callback`, `/{broker}/initiate-oauth`, `/auth/broker/oauth/manual` | single-use hashed `state` (10 min), state-less brokers matched to the same browser session (3 min), account binding (`catalog::configured_account`), XTS POST callback needs `state` | `services/broker_auth_service.rs`, `db/sqlite/oauth_state.rs`, `server/routes/broker.rs`, `brokers/catalog.rs` | `every_way_to_create_a_broker_session_refuses_a_forged_attempt`; the table in `docs/security/known-residuals.md` must match it |
| Strategy webhook `POST /strategy/webhook/{token}` | the URL token is the credential; rate limit and lockout | `strategy/webhook.rs`, `server/ratelimit.rs` | `cargo test --locked --test it strategy::strategy_module_webhook strategy::webhook_security` (`src-tauri/tests/it/strategy/`) |
| Chartink webhook `POST /chartink/webhook/{webhook_id}` | constant-time id compare, per-locator rate limit, lockout after repeated wrong addresses | `chartink/webhook.rs` | `tests/it/chartink.rs` |
| Telegram, WhatsApp | no inbound HTTP: Telegram long-polls (the webhook is deleted), WhatsApp is a client session; the Telegram bot's `gate` (`messaging/telegram/bot.rs`) answers only the linked user in a private chat | `messaging/telegram/`, `messaging/whatsapp/` | `cargo test --lib messaging::telegram`, `tests/it/messaging.rs` |
| `/mcp` (HTTP) and the `mcp` subcommand | bearer `oamcp_` token, only its SHA-256 stored, shown once; scopes; per-token rate limit; failed tokens counted like bad API keys; `OPENALGO_MCP_TOKEN` read by the subcommand only, never logged or on the command line | `mcp/http.rs`, `mcp/store.rs`, `mcp/stdio.rs` | `tests/it/mcp_security.rs`, `mcp_subcommand.rs` |
| OpenScript runner host `/openscript/runner/host/{run}/*` | each call carries its run's secret (handed to the runner page in its URL fragment) | `server/routes/openscript_runner.rs`, `trading/runner/` | `tests/it/trading_runner.rs` |
| Custom indicators `/custom-indicators/*` | signed-in user, `.js` names only, regular files inside the folder (no symlink escape), 4 MiB cap; the module runs with the app's privileges by design | `server/routes/custom_indicators.rs`, `trading/indicators.rs` | `cargo test --lib trading::indicators`, `tests/it/trading_files.rs` |
| Feed server `ws://127.0.0.1:8765` | `authenticate` with the API key (constant-time), failed keys counted like bad API keys; the upgrade's `Host` must name this computer, an own interface address (LAN on) or the public host, and a browser `Origin` the app's live page (S-10); 4401 close on auth timeout, nothing but `ping` before auth | `feed/auth.rs`, `feed/server.rs`, `feed/mod.rs` | `tests/it/feed_conformance.rs`, `feed_behaviour.rs`, `feed_app.rs` |
| Bind host and LAN toggle | loopback by default; binding beyond it is an explicit setting | `config.rs`, `server/mod.rs` | settings tests; confirm with `lsof -iTCP -sTCP:LISTEN -P` on a test instance |
| Tauri shell | CSP in `src-tauri/tauri.conf.json` (`default-src 'self'`, `frame-ancestors 'none'`, `object-src 'none'`), `withGlobalTauri: false`; capabilities `src-tauri/capabilities/default.json` (bundled start page) and `remote-app.json` (the local server's UI, `http://127.0.0.1:*` and `http://localhost:*` only: window basics and `shell:allow-open`); devtools off in release | `tauri.conf.json`, `capabilities/` | read the diff of both files since the last audit; any new permission needs a reason |

When a route is added as public, `public_route_list_is_exactly_the_reviewed_one`
fails until the list in `server/tests.rs` is updated; the review of that
change is part of this audit. A public route that changes state needs its
own credential (a URL secret, a bearer token, a verified `state`). A CSRF
token is not one: `GET /auth/csrf-token` hands it to anyone.

For a surface that takes limits (MCP fan-out, batch sizes, history ranges),
check the pattern that closed three rounds of MCP findings: each input parsed
once into a typed value, limits checked on that value with checked
arithmetic, and one shared budget reserved before any work starts.

## 3. Secrets at rest, in logs, on the wire

- **Keys (KEY-01, maintainer decision 2026-10-13).** The data-encryption
  key and the API-key pepper are wrapped with Argon2id(login password) in
  the one-row `key_vault` table of `openalgo.db`
  (`db/sqlite/key_vault.rs`, `docs/port/no-keychain.md`). No OS keychain on
  any platform: the keychain (`security/keystore.rs`) is read only once, by
  the first sign-in of an install from an earlier build, and its entries are
  then deleted. Check:
  - a new install makes zero keychain calls
    (`a_new_install_never_touches_the_keychain`) and a moved one never reads
    the keychain again;
  - the keys are in memory only between a sign-in that issued a session and
    the logout (a sign-in waiting for its authenticator code installs
    nothing), and while locked `/api/v1`, `/mcp`, the feed and the webhooks
    refuse with the locked sentence and decrypt nothing;
  - a password change writes the hash and the wrapping in one transaction
    (the fault test), and a fresh start (forgotten password, unreadable
    keychain) runs only from the desktop window and leaves no value
    encrypted under the old key;
  - every new encrypted column is listed in `key_vault::drop_encrypted_values`
    and `key_vault::witness`;
  - a sign-in that did not prove its password tells nobody but the app
    window anything: every failure is the same 401 "Invalid credentials"
    to a browser, a local program, another device or a tunnel, after the
    same Argon2 work (`hashing::pad_argon2_runs`); only a sign-in carrying
    the window proof (`security::window`, `middleware::sign_in_from`)
    reads an earlier build's keychain, moves keys or hears why keys could
    not be opened; the key state is read before the name and the password
    (`nobody_but_the_app_window_can_tell_a_right_password_from_a_wrong_one`,
    `the_ways_out_need_the_password_and_the_app_window`,
    `every_sign_in_costs_the_same_work_whatever_it_finds`);
  - what the keychain says reaches neither an answer nor a WARN or ERROR
    line (the error log the Diagnostics page serves:
    `the_error_log_never_carries_what_the_keychain_said`), and key material
    travels as `Secret`/`SecretBytes` only.
  Never a hard-coded or obfuscated key.
- **Caches.** Every cache is bounded with a TTL and follows the web's
  `LockedTTLCache` rules through `crate::cache::TtlCache`: readers fill
  through the generation read before their query, writers clear after their
  commit, and logout, a password change or reset, a key rotation and a
  broker switch clear them. A new cache gets a race test (a read in flight
  across a clear cannot repopulate it) and a row in the cache table of
  `docs/port/no-keychain.md`.
- **Ciphertext.** Broker credentials and tokens are AES-256-GCM with
  associated data binding each ciphertext to its row and column
  (`security/crypto.rs` `encrypt(plaintext, &Aad)`). Check a ciphertext
  copied to another row or column fails to decrypt (the crypto tests).
- **Nothing returns a stored secret** except the two the web shows too. No
  endpoint or Tauri command returns a saved broker secret or password
  (`/auth/broker-config` returns `broker_api_key: null`; broker keys are
  masked). The OpenAlgo API key (`/apikey`, `/auth/session-status`,
  `/playground/api-key`, `/api/websocket/apikey`) and the TOTP enrollment
  seed (`/auth/profile-data`) go to the signed-in session only, with
  `Cache-Control: no-store` (`sec06_key_bearing_answers_are_never_cached`).
- **Logs.** `Secret` (`security/secret.rs`) prints `[REDACTED]`; broker
  errors go through `brokers::common::redact`; request bodies stored in
  `logs.db` go through `db::sqlite::logs::redact`; client-reported URLs
  through `services::error_log::sanitize_url`; `lib.rs::log_filter` pins
  `tungstenite` at info. Drive a failing login and a feed reconnect with
  sentinel credentials and scan the output and a test data directory's
  `logs.db` with `.claude/skills/verify/leak_scan.py`.
- **Files.** Database files are owner-only (`security/fsperm.rs`
  `restrict_db_files`).
- **Fixtures.** Only `<APIKEY>`, `<USER_ID>`, `<EMAIL>` placeholders; gitleaks
  enforces it.

## 4. Accepting a residual

A finding that is reduced but not closed, or a scanner hit that is
unreachable, is accepted in writing, never by silence:

- **Code-level residual** (a control with a known gap): an entry in
  `docs/security/known-residuals.md` naming the entry point, the protection,
  the code that carries it, the test that proves it, and what remains.
- **Rust advisory**: an `ignore` entry in `.github/deny.toml` `[advisories]`
  with `{ id = "RUSTSEC-...", reason = "<why unreachable>; review by YYYY-MM-DD" }`.
  `security.yml` takes the cargo-audit ignores from that file, so it is the
  single place.
- **Trivy finding**: the id in `.trivyignore` with a comment above it saying
  why it is accepted and what would let it be removed, plus a review date.
  An advisory accepted in `deny.toml` carries the same GHSA ids in
  `.trivyignore`, and its Dependabot alert is dismissed as "not used" with the
  same reason. Accept only when the vulnerable code provably never runs.
- **CodeQL alert**: dismissed in GitHub with the reason, only after the check
  in section 1.
- **npm advisory** in a production dependency at high or critical: not
  accepted; upgrade or replace. Moderate and low: list them in the report.

Every review date that has passed is a finding in the next audit.

## 5. The report

Write `docs/audit/<YYYY-MM-DD>/security.md` (one file; add more only for a
large audit, following `docs/audit/2026-10-03/` and its `README.md`):

```markdown
# Security audit <YYYY-MM-DD>

Commit: <sha>. Scope: <what changed since the last audit>. Auditor: <who>.

## Summary
<counts by severity; what is fixed, what is accepted, what is open>

## Scanners
| Tool | Version | Command | Result |
<one row each: cargo deny, cargo audit, npm audit, gitleaks, trivy, CodeQL; "not run" with the reason>

## Findings
### <ID>. <title> (<Critical|High|Medium|Low>)
- Where: <file:line>
- What an attacker needs and gets: <one paragraph>
- Evidence: <the command or test that showed it; output trimmed>
- Fix: <change, with the test that fails without it> | Accepted: <link to the residual entry>

## Controls verified
<surface -> test run -> result, for the table in section 2>

## Residuals reviewed
<each entry in known-residuals.md, deny.toml and .trivyignore: still valid? review date?>
```

Severity: what an attacker on this machine, on the LAN (when bound beyond
loopback) or behind a web page the trader visits can do with it. A secret in
a log or a forged session is high; a missing header on a loopback-only route
is low.

**Hold the report off master until its findings are fixed.** Commit it on a
branch (`audit/<date>`), fix the findings there or on their own branches,
and merge the report with the fixes (`docs/audit/2026-10-03/README.md`: "The
security report is held back until its findings are fixed."). A published
open finding in a public repository is a how-to.
