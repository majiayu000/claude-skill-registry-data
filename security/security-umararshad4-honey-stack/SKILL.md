---
name: security
description: "Use when touching auth, sessions, permissions, secrets, payments, user data, DB writes, webhooks or deploy config, or when asked for a security audit."
license: MIT
metadata:
  reviewed: "2026-10-18"
  sources: "MCT (local) ~/.claude/skills/security-sanity; garrytan/gstack 1.60.1.0 cso/SKILL.md.tmpl (phases 0-1, 12-13: confidence gate, false-positive rules, findings format, leaked-secret playbook), cso/sections/audit-phases.md (phases 2-11); cursor/plugins pstack 0.15.25 skills/principle-boundary-discipline"
---

# Security

Think like an attacker and report like a defender: every finding names the exploit path, then the fix.

| Ask | Branch |
|---|---|
| A change touches a sensitive surface | Sanity check (below) |
| "Security audit", "threat model", "OWASP", "pentest review", a pre-launch review | Full audit: read `references/audit.md` |

On Claude Code, the built-in `/security-review` command reviews the pending changes on the current branch. Suggest it as a second opinion before a PR that touches these surfaces. On Codex, use the `review` skill.

## 1. Map the trust boundary

Name where untrusted data enters the changed code: request params, body and headers, cookies, webhooks, file uploads, fetched URLs, third-party API responses, LLM output. Then name where it reaches something privileged: the database, a shell, the filesystem, rendered HTML, redirects, outbound requests, money, or another user's records.

Done when: you can list each entry point and each privileged sink the diff touches.

## 2. Check the change

Read the diff and its callers against each line that applies:

- **Authorization on every route.** Each route, handler, server action, RPC method and GraphQL resolver checks on the server that the caller is authenticated *and* allowed to act on this specific record (owner, tenant or role check against the object id). "Logged in" is not "allowed". A new route copies the guard its siblings use. Client-side checks are UX, not security.
- **Input validated at the trust boundary.** Parse input into typed data with the repo's schema library (zod, pydantic, and so on) where it enters. Allowlist the fields a write may set; never spread a request body into an ORM update. Inside the boundary, trust the types instead of re-checking at every layer.
- **Secrets stay out of code, logs and clients.** No keys in source, committed `.env` files, URLs, error messages, logs or client bundles (`NEXT_PUBLIC_*`, `VITE_*`). Read them from the environment or a secret store. A secret that reached git is leaked: rotate it, because removing the commit doesn't un-leak it.
- **Webhooks verify signatures.** Verify the provider signature over the raw request body with a constant-time compare, reject stale timestamps to stop replays, and dedupe on the event id so a retry can't apply twice.
- **Payments trust the server.** Amounts, prices, currency and paid status come from the server or the provider, never from the client.
- **SQL is parameterized.** Use bound parameters or the ORM's query builder. No string interpolation into SQL, shell commands, templates or `eval`. Raw HTML sinks (`dangerouslySetInnerHTML`, `v-html`, `innerHTML`) get sanitized input only.
- **Outbound requests and redirects are allowlisted.** A user-supplied URL is checked against allowed schemes and hosts before the server fetches it (SSRF). Redirect targets are relative paths or allowlisted hosts.
- **Sessions and tokens.** Cookies are `HttpOnly`, `Secure` and `SameSite`. Rotate the session id on login and privilege change, and invalidate it on logout and password change. JWTs: verify the signature with a pinned algorithm and check `exp`. Cookie-authenticated writes need CSRF protection.
- **Least privilege.** DB roles, API keys, OAuth scopes, IAM policies and CI tokens get only what this feature needs. No wildcard actions. Service-role keys stay server-side.
- **Safe defaults.** Deny by default and fail closed: an error in an auth check denies. No `*` CORS origin on credentialed routes, debug mode off in production, generic error messages to clients with detail kept in server logs. Login, sign-up, password reset and OTP endpoints are rate-limited.
- **User data.** Responses carry only the fields this caller may see: no password hashes, tokens, or other users' emails. PII stays out of logs and analytics.
- **LLM features.** User text stays out of system prompts and tool schemas. Model output is untrusted: never `eval` it or render it as raw HTML. Tool calls are validated before they run, and spend per user is capped.

Done when: every applicable line is checked, and each failure is fixed or recorded as a finding.

## 3. Prove the negative path

Positive tests show the feature works; negative tests show it's safe. For each boundary touched, run at least one check that must be refused:

- unauthenticated request: 401
- another user's or tenant's id: 403 or 404
- invalid or extra-field payload: 400 with nothing written
- bad or replayed webhook signature: rejected with nothing applied

Scan the staged diff for secrets with the repo's scanner (gitleaks, trufflehog) when one is installed, otherwise grep for known key shapes:

```bash
git diff --staged | grep -nE 'AKIA[0-9A-Z]{16}|sk_live_|sk-ant-|ghp_|github_pat_|xox[abp]-|-----BEGIN [A-Z ]*PRIVATE KEY-----'
```

Done when: each touched boundary has a negative check that ran this turn and was refused as expected, and the secret scan is clean.

## 4. Report

One line per finding: severity (critical, high, medium), `file:line`, the exploit path in one sentence, and the fix. A finding without a concrete exploit path is a note, not a finding. For a leaked secret, include the playbook in `references/audit.md`.
