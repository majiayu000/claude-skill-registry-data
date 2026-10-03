---
name: security-baseline
description: Secure-coding baseline to apply while writing code, not just when reviewing it — input validation, auth, secrets, dependencies. Use whenever code crosses a trust boundary (accepts user input, handles auth, talks to an external service, stores sensitive data). Complements reviewer-security, which audits after the fact.
---

# Security baseline

Prescriptive practices to follow *while writing* code — `reviewer-security`
(`.claude/agents/reviewer-security.md`) audits for violations after the fact; this
skill is how to avoid needing that audit to catch something.

## Input handling

- Treat all external input as untrusted: request bodies/params, file uploads,
  environment variables from an untrusted source, data read from another service.
- Never build a query/command/template by string-concatenating untrusted input —
  use parameterized queries, prepared statements, the templating engine's
  auto-escaping, or an argument array instead of a shell string.
- Validate shape and bounds at the boundary (type, length, range, allowed values) —
  reject early with a clear error rather than letting bad data flow deeper.
- Treat any user-controlled URL/path as a potential SSRF/path-traversal vector —
  validate against an allowlist rather than a denylist.

## Secrets & credentials

- Never commit secrets, even temporarily — this repo's gitleaks integration
  (`.gitleaks.toml`, `lefthook.yml`) catches most slips, but don't rely on it as the
  only line of defense.
- Read secrets from environment/secret-manager, never hardcode; never log them, and
  scrub them from error messages before they reach a log or an external caller.
- Rotate anything that touches a third-party API key the same way you'd rotate a
  password if it's ever exposed — don't assume a leaked key is fine because "it's
  probably not been noticed."

## AuthN/AuthZ

- Check authorization on every request that touches another user's data, not just
  authentication — "logged in" and "allowed to see this specific resource" are
  different checks.
- Default deny: a new route/handler with no explicit auth check is a bug, not an
  oversight to fix later.
- Use the platform's/library's vetted session, JWT, or OAuth implementation — don't
  hand-roll crypto, token generation, or password hashing (use the standard
  bcrypt/argon2/scrypt, never plain hashing or hand-rolled encryption).

## Dependencies & supply chain

- Prefer the smallest dependency that solves the problem; a new dependency is a
  standing trust decision, not a free abstraction.
- Keep dependencies current — this template's `renovate.json` automates the PRs;
  actually review and merge them rather than letting them pile up.
- Pin versions for anything security-sensitive (auth, crypto) rather than
  auto-accepting the latest on every install.

## Sensitive data at rest

- Encrypt genuinely sensitive data at rest (health data, financial data, anything
  where exposure would harm the user) rather than assuming filesystem/DB access
  control is enough — especially for local-first apps where "the database file"
  might end up in a backup, a synced folder, or a lost device.
- Minimize what's collected/stored in the first place — data that was never
  collected can't leak.

## When reviewing instead of writing

This is what `reviewer-security` checks for after the fact — use both: this skill to
avoid introducing the issue, that agent (or a review swarm, see
`.claude/skills/swarm/SKILL.md`) to catch what slipped through.
