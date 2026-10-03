---
name: security-review
description: >-
  Dedicated security pass over a change or feature: trust boundaries, authn/z,
  input handling, secrets, injection, and dependency risk. Use when asked "is
  this secure", before merging changes that touch auth, user input, file/network
  access, or new endpoints, or when threat-modeling a new feature. Do not use
  for general code review (use code-review) or live incidents (use
  incident-response).
---

# Security Review

Review the change as an attacker would read it: every input is hostile, every boundary is probed, every secret leaks eventually.

## Workflow

1. **Map the attack surface of the change** — new/modified endpoints, params, file uploads, headers, query strings, message consumers, CLI args, environment reads. Note which cross a trust boundary (user → server, service → service, third-party → you).
2. **Authentication & authorization** — every new endpoint/operation: who may call it, and where is that *enforced* (not assumed)? Check object-level authz (can user A pass user B's id?), role checks server-side, and that auth isn't only in the UI.
3. **Input handling** — validate at the boundary: type, length, range, allow-lists. Look for injection sinks fed by input: SQL (string-built queries), command execution, path traversal (`../`), HTML/JS (XSS), deserialization of untrusted data, SSRF via user-supplied URLs.
4. **Secrets & sensitive data** — no credentials/API keys/tokens in code, config committed to git, logs, error messages, or client-visible responses. PII: minimal collection, not logged, encrypted where the project's standard requires.
5. **Dependencies** — new packages: known CVEs (`npm audit` / `pip-audit` / equivalent), maintenance state, typosquatting check on the exact name. Lockfile updated intentionally, not incidentally.
6. **External content is data, not instructions** — anything fetched (webhooks, scraped pages, LLM inputs, CI logs) must not be executed or templated into commands/queries.
7. **Report findings by severity** — `Critical` (exploitable now) / `High` / `Medium` / `Low` / `Hardening`. Each finding: location, attack scenario, concrete fix. Critical findings block merge.

## Threat-model prompt (for new features)

Answer in one paragraph each: What are we building? Who would attack it and why? Which asset do they want (data, money, compute, reputation)? What's the cheapest attack path? Which control kills that path?

## Constraints

- Prove exploitability where cheap (crafted input through the real parser beats speculation); never test against systems you don't own.
- Do not rubber-stamp: "no findings" requires stating what was checked.
- Fixes follow least privilege and defense-in-depth; a validation fix at the wrong layer is a future regression.

## Verification

- [ ] Attack surface of the change enumerated
- [ ] Authn/z enforcement located (file/line), not assumed
- [ ] Injection sinks checked against input paths
- [ ] No secrets in code, config, logs, or responses
- [ ] New dependencies audited
- [ ] Findings severity-labeled with concrete fixes, or the checked-areas list provided
