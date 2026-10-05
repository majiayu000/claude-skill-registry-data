---
name: secrets-management
description: Handle secrets safely across the lifecycle — keep them out of source, load from env or a secret manager, scope to least privilege, encrypt in transit and at rest, rotate on a schedule, and respond fast when one leaks. Deep reference with runbooks, examples, and a runnable leak scanner.
type: skill
version: 2.0.1
updated: 2026-07-27
---
# Secrets Management

A secret committed to source control is **already compromised** — assume it is public the moment it lands
in history, even on a private repo. Git history, CI logs, container layers, backups, and forks all retain
it. The only safe response is rotation, not deletion. This skill is the deep reference for keeping secrets
out of code, supplying them safely at runtime, and reacting correctly when one escapes. Heavy detail lives
in `references/`; copy-paste material in `examples/`; a runnable leak scanner in `scripts/`.

## Mental model

Treat a secret as **runtime configuration**, never as code. Code is committed, reviewed, copied, and
shipped to laptops; secrets must not ride along. Separate three concerns and never collapse them:

| Concern | Question | Answer |
|---|---|---|
| Storage | where does the truth live? | a secret manager (Vault, cloud KMS/Secrets Manager) |
| Delivery | how does the app get it? | injected env var or a fetch at boot, over TLS |
| Lifecycle | how does it change? | rotation on a schedule + on suspected leak |

The application code should only ever *read* a secret from its environment — it should never know the
storage backend, the rotation cadence, or the raw value's origin. That decoupling is what lets you rotate
a leaked key with **zero code changes**.

## 1. Keep secrets out of source

1. Never hardcode keys, tokens, passwords, connection strings, or private keys in source — not even
   "temporarily". Temporary hardcodes are how most leaks happen.
2. Commit a placeholder template (`.env.example`) with **fake** values and key names only; add the real
   `.env` to `.gitignore` before the first commit.
3. Add a secret scanner to pre-commit hooks **and** CI so a leak is caught before it reaches the remote.
   Run `scripts/detect-hardcoded.mjs` over diffs or files as a zero-dependency gate.
4. Load and validate required secrets at startup; fail fast with a clear message naming the missing var.

```js
// Read from the environment; never embed the value. Validate at boot.
const required = ['DATABASE_URL', 'STRIPE_SECRET_KEY', 'JWT_SIGNING_KEY'];
const missing = required.filter((k) => !process.env[k]);
if (missing.length) {
  throw new Error(`Missing required secrets: ${missing.join(', ')}`);
}
const stripeKey = process.env.STRIPE_SECRET_KEY; // if this leaks, rotate the value — no code change
```

## 2. Environment variables vs secret managers

Env vars are the universal **delivery** mechanism, but they are not a secure **store** — they leak via
`/proc`, crash dumps, child processes, and accidental `console.log(process.env)`. For anything beyond a
single dev machine, the source of truth belongs in a manager.

| Approach | Good for | Watch out for |
|---|---|---|
| `.env` file (gitignored) | local dev only | easy to commit by accident; no rotation, no audit |
| Platform env vars (CI/PaaS) | small apps, single-tenant | visible to anyone with dashboard access; static |
| Secret manager (Vault, AWS/GCP/Azure) | production, teams | needs auth bootstrap; adds a runtime dependency |
| Cloud KMS (envelope encryption) | encrypting data + secrets | key policy mistakes are silent until exploited |

A manager buys you **dynamic, short-lived credentials** (e.g. Vault issues a DB credential that auto-expires
in 1 hour), centralized **audit logs**, and **rotation without redeploys**. See
`references/secret-managers.md` for the comparison and bootstrap-auth patterns.

## 3. Least privilege & short-lived credentials

- Scope every credential to the **minimum** resources and actions it needs; a build token does not need
  prod database write access.
- Prefer **short-lived** dynamic credentials over long-lived static keys. A credential that lives 15
  minutes limits the blast radius of a leak to 15 minutes.
- Use **distinct** credentials per service and per environment so revocation is surgical, not a blackout.
- Never share one "god" key across services — you lose the ability to attribute and revoke.

## 4. Encryption in transit and at rest

- **In transit:** fetch secrets only over TLS; reject plaintext transports. Never pass secrets as URL
  query params (they land in logs, proxies, and browser history) — use headers or the request body.
- **At rest:** the manager encrypts its store; for data you encrypt yourself, use **envelope encryption**
  (a KMS-held key encrypts per-record data keys) rather than a single static key in config.
- Keep secrets out of logs, error reports, and APM traces. Redact at the logging boundary — see the
  scanner's redaction logic and `references/leak-response.md`.

## 5. Rotation

Rotation is the difference between "we had an incident" and "we had a non-event." Two triggers:

1. **Scheduled** — rotate on a fixed cadence (e.g. 90 days for static keys) so no credential is ancient.
2. **Reactive** — rotate **immediately** on any suspected exposure, no matter how minor it looks.

The safe pattern is **overlap**: provision the new credential, deploy it, verify, then revoke the old —
so there is no downtime window. The full step-by-step is in
[`references/rotation.md`](references/rotation.md) and a fill-in incident checklist is in
`examples/rotation-runbook.md`.

## Common pitfalls (failure modes)

- **"It's a private repo, so it's fine."** Forks, clones, CI caches, and future open-sourcing all expose
  it. Private is not secret.
- **Deleting the commit instead of rotating.** `git rm` / force-push does not erase history from clones,
  caches, and PR mirrors. The credential is burned — rotate it.
- **Logging the whole environment.** `console.log(process.env)` or dumping config on a crash ships every
  secret to your log aggregator. Redact at the boundary.
- **Secrets in URLs.** Query-string tokens leak into access logs, referrer headers, and proxies.
- **One static key forever.** No rotation means a years-old leak is still valid today.
- **Over-scoped credentials.** A read-only reporting job holding admin keys turns a small leak into a
  full compromise.
- **Checking `.env.example` with real values.** The template must contain only obviously fake placeholders.

## When NOT to use / trade-offs

- **A full secret manager for a solo side project** is overkill — gitignored `.env` plus a pre-commit
  scanner is proportionate. Adopt a manager when you have a team, multiple environments, or compliance needs.
- **Short-lived dynamic credentials add operational complexity** (auth bootstrap, renewal, clock skew). If
  your platform can't renew reliably, a rotated static key with tight scope may be the pragmatic choice.
- **Client-side secrets don't exist.** Anything shipped to a browser or mobile app is public; never put a
  secret in front-end code — use a backend proxy or short-lived scoped tokens instead.
- **Encrypting everything** has key-management cost. Encrypt what's sensitive; don't build a KMS maze for
  non-secret config.

## Files in this package

- `references/secret-managers.md` — env vars vs Vault/cloud managers, bootstrap auth, dynamic creds
- `references/rotation.md` — scheduled & reactive rotation, zero-downtime overlap pattern
- `references/leak-response.md` — what to do in the first hour after a leak; redaction guidance
- `examples/env-example.md` — a model `.env.example` with safe placeholders and `.gitignore` notes
- `examples/rotation-runbook.md` — fill-in incident/rotation checklist
- `scripts/detect-hardcoded.mjs` — zero-dep scanner that flags & redacts hardcoded secrets (`--selftest`)

Pairs with the `secure-auth` skill (where signing keys and session secrets come from), the `owasp-top10`
skill (A07 identification/auth failures, A02 cryptographic failures), and the `security-auditor` agent for
a full credential-handling review.

## Worked micro-example

Drill: a Slack webhook URL just landed in a public repo commit.

```text
CLOCK STARTS:
  0-5m    revoke at the source (Slack app config) — rotation BEFORE cleanup;
          the secret is burned the moment it was pushed, not when found
  5-15m   sweep for siblings: same commit, same author, same week
          (leaks travel in packs — found: a Sentry DSN in the same PR)
  15-30m  history rewrite is OPTIONAL cleanup, revocation is the fix —
          scrapers saw it in seconds; git filter-repo only tidies appearances
  30-60m  close the hole: pre-commit scan hook + CI secret-scan gate
          (the same patterns scan-secrets.mjs ships)
POSTMORTEM Q: why was a live credential in an env a developer could paste
from? → move to short-lived tokens minted at deploy; the class dies.
```
