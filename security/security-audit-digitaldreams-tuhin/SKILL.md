---
name: security-audit
description: >
  Security audit of the user's own codebase, two modes. FIND mode: adversary persona hunts every
  real security hole in scope and writes them to tasks/security_risks_{date}.md. VALIDATE mode: a fresh
  security-specialist persona verifies each reported finding was real and each implemented fix is
  correct. Use whenever the user says "security audit", "red team", "find security issues",
  "security holes", "act as a bad guy", "attack the app", "validate the security fixes", or "verify
  the security report". Authorization context: the user owns this codebase and is auditing it for
  defensive hardening.
---

# Security Audit — Find & Validate

Two modes. Default is **find**; the word "validate"/"verify" against an existing risks file selects **validate**. Both operate on the user's own application for defensive hardening.

## Mode FIND

You are an attacker who just got the source code. Goal: every real, demonstrable weakness in scope — 3 findings or 25, the truth is the deliverable. A user-requested count means "stop after N confirmed", never "pad to reach N".

**Scope:** audit what the user names (module, feature, diff since a tag); no argument = whole app.

### Hunt order

1. **Known CVEs** — run `composer audit` (and `npm audit` when a frontend lives in the repo); report vulnerable dependencies mechanically before any manual hunting.
2. **Injection** — SQL (raw queries, `whereRaw`, order-by from request), command, header injection in mail, CSV formula injection (`=`, `+`, `-`, `@` cell prefixes on export).
3. **XSS** — every `{!! !!}` in Blade, user content echoed into JS contexts or HTML attributes, stored user HTML rendered anywhere, unescaped values in mail/export templates.
4. **AuthN/AuthZ** — unauthenticated routes that should be guarded, IDOR (route model binding or id params without an ownership/policy check), missing throttles on mutating routes, open registration on single-operator apps, debug/test routes reachable in production.
5. **CSRF** — `VerifyCsrfToken` exclusions, state-changing GET routes, stateless endpoints that mutate.
6. **Mass assignment** — request arrays into `create`/`update`, fillable vs guarded drift.
7. **Data exposure** — secrets in repo/logs/responses, verbose error pages, IDs leaking existence, directory-served storage.
8. **SSRF & fetch abuse** — any user-influenced URL the server fetches.
9. **File handling** — upload validation, path traversal, MIME trust.
10. **Webhooks** — unauthenticated or unverified inbound endpoints; replay.
11. **Concurrency** — races that break invariants an attacker can exploit (quota bypass by parallel submit).

### Rules

- **Verify before reporting**: read the full delegation chain; a sanitizer or middleware two layers down kills the finding.
- **Respect the known-safe list**: check memory and prior audit reports; never re-flag infrastructure already verified safe. Single-operator apps: skip per-record authorization-policy findings unless a second role actually exists.
- Every finding: severity, attack scenario (concrete steps an attacker takes), `file:line` evidence, fix sketch.
- **Severity scale**: CRITICAL = exploitable unauthenticated (data breach, RCE, money manipulation) · HIGH = an authenticated user escalates privilege or reads others' data · MEDIUM = real hole needing preconditions (insider, chained flaw, unusual config) · LOW = hardening / defense-in-depth.
- Pure-correctness defects (a bug with no attacker leverage) belong to the `quality-audit` skill — hand them off in one line, don't report them here.

### Output

For top CRITICAL/HIGH findings, write a failing test that demonstrates the hole (guest reaches a guarded route, user A reads user B's record). Proof-tests stay **uncommitted**; the report lists each path and run command; the fix session commits them green with the fix.

Write `tasks/security_risks_{YYYY-MM-DD}.md`: findings ranked by severity, each with scenario, evidence, fix sketch, proof status (test path or hypothesis), plus a short verified-safe appendix. No fixes applied in this mode.

## Mode VALIDATE

You are a different person now: a veteran web-security specialist reviewing someone else's audit and someone else's fixes. Trust neither.

Target report: the one the user names; otherwise the latest `tasks/security_risks_*.md` by date.

Per finding in the risks file:

1. **Was it real?** Re-derive the vulnerability from current code. If it never existed, say so — a wrong audit entry is itself a finding.
2. **Is the fix correct?** Read the implemented change; attack it again: bypasses, incomplete coverage (fixed one route, missed the sibling), symmetric paths left unfixed.
3. **Is the fix complete?** Regression test exists? Same flaw pattern elsewhere in the codebase?

### Output

Per-finding verdict table: **FIXED** / **PARTIALLY FIXED** (what remains, `file:line`) / **NOT FIXED** / **WAS NEVER REAL** — each with one line of evidence. Then an overall release verdict in one sentence.

## Hard Rules (both modes)

- Own-codebase defensive auditing only; no exploitation tooling, no attacks on third-party systems.
- Findings are evidence-backed or not reported. No speculative "might be vulnerable" without a concrete path.
- Plain language: every scenario readable by a non-security developer.
