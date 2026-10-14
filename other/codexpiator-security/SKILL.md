---
name: codexpiator-security
description: Security guidance - secure coding checklist, authn/authz threat-model and hardening (MFA, IDOR/BOLA, session fixation, password-reset abuse - see codexpiator-backend for base auth implementation), input validation and injection defense, secrets and config management, dependency and supply-chain risk, infrastructure and access control, business-logic/webhook security, AI/agent security (prompt injection, excessive AI permissions), and security testing. Use for any security-sensitive question or before shipping anything that touches auth, user input, payments, AI/agent features, or infrastructure config.
---

# Codexpiator Security

Single-purpose reference files for security concerns. This skill is a
fast, always-available baseline — it is not a substitute for a real
specialized security audit when one is available.

| File | Read this when... |
|---|---|
| `secure-coding-checklist.md` | Quick OWASP-Top-10-mapped pass over any change |
| `authn-authz-patterns.md` | Login, sessions, MFA, password reset, IDOR/BOLA, privilege checks |
| `input-validation-and-injection.md` | Anything touching user input: SQL/NoSQL injection, XSS, CSRF, uploads, path traversal, SSRF, mass assignment, command injection, deserialization |
| `secrets-and-config-management.md` | Credentials, `.env` files, secrets in git/JS/logs, cookies, browser storage |
| `dependency-and-supply-chain.md` | Vulnerable/malicious packages, CI/CD supply-chain risk |
| `infrastructure-and-access-control.md` | Cloud/DB permissions, admin routes, debug tools, headers, CORS, rate limits, monitoring, backups |
| `business-logic-and-webhooks.md` | Payments, webhooks, business-logic abuse, race conditions |
| `security-testing.md` | How to actually test security controls, not just implement them |
| `external-skills-map.md` | When `security-review` should lead instead of this skill |

## Mandatory: consult the specialized skill first, not as a fallback

For any security-sensitive work (auth, payments, user input handling,
infrastructure config, anything pre-merge on a security-critical
path), attempt to invoke `security-review` (see
`shared/external-skills-registry.md` for the confirmed install path)
**before** finalizing the change — this skill's own checklists are the
fast baseline and the fallback when that specialized skill genuinely
isn't available, not a substitute you reach for by default instead of
checking.

## Every principle here needs to actually be applied, not just known

Read the relevant checklist(s) for the surface being touched and
verify each applicable item against the actual code — don't treat this
skill's content as background knowledge that informs a general sense
of caution. A checklist item that isn't checked against the real diff
provides no protection.

## Ask when useful; suggest an audit after significant work

See `shared/collaboration-and-audit-practice.md` — ask a targeted
clarifying question (via `AskUserQuestion` when available) when a
security trade-off genuinely needs the user's input, and suggest
`/codexpiator-audit` after significant security-sensitive work.
