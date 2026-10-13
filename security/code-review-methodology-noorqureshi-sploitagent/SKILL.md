---
name: code-review-methodology
description: >
  Systematic manual source-code security review — how to find bugs by reading code. Load on
  "review this code/repo", a source-available target, whitebox testing, or auditing a PR/app
  for vulnerabilities. Signals: a codebase in scope, "SAST", "secure code review", a language repo.
domain: code-review
type: methodology
stability: learning
modes: [bugbounty, defense]
severity: info
tools: [semgrep, ripgrep, git]
schema_version: 1
---

# Source-code security review — methodology

## When it applies
You have (some of) the source. Whitebox review finds classes that blackbox misses — it follows
data from where it enters to where it's dangerous, across the whole codebase at once.

## Why it works
Vulnerabilities are source → sink flows with missing sanitization in between. Reading code lets
you see the sink (dangerous function), trace back to a user-controlled source, and confirm
nothing safe happens on the path — far faster and more complete than guessing from outside.

## Method
1. **Map the app**: entry points (routes/controllers/handlers), auth/authz middleware, the ORM/
   DB layer, config, and where user input enters. Note the framework — its defaults decide a lot.
2. **Sink-first sweep**: grep for dangerous functions per language (see `code-review-dangerous-sinks`)
   and for each hit, trace the argument back to a source. `semgrep --config auto` for a fast first pass.
3. **Source-to-sink for each class**: injection (query/exec/template), authz (missing owner
   checks → IDOR/BOLA), deserialization, SSRF (URL fetchers), file ops (path traversal/upload),
   crypto misuse, secrets in code.
4. **Auth & access control**: verify every sensitive route re-checks identity AND object ownership,
   not just "logged in". This is where the highest-impact bugs hide.
5. **Track findings** with `file:line`, the data path, and a PoC request; confirm dynamically where possible.

## Gotchas
- A dangerous sink with a constant/allowlisted argument isn't a bug — confirm the source is user-controlled.
- Framework auto-escaping (ORM params, template autoescape) can neutralize an apparent sink — check config.
- Don't drown in `semgrep` noise; triage by exploitable source→sink, not raw hit count.

## Verify success
For each finding: a concrete source→sink path with missing sanitization, ideally reproduced
with a request/input that triggers it.

## References
OWASP Code Review Guide; Semgrep rules; "Micro-methodology for code review" (GitHub Security Lab).
