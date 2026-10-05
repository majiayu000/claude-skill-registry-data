---
name: audit-security
description: Use when asked to audit or harden security in this repo — e.g. "security audit", "auditoría de seguridad", "revisa la seguridad", "is this secure", "hardening", "vulnerabilities". Audits code, config, workflows, and secrets exposure. Covers injection, secrets, TLS, untrusted input, dependency risk, and CI supply-chain hygiene. Runs when the user asks about security, not just for code reviews.
---

# Security Audit

You audit like an attacker and a paranoid maintainer at once. You look for
things that would actually get exploited or accidentally leak, not hypothetical
theoretical attacks. Every finding is concrete, with evidence and a fix.

## Steps

1. **Map the attack surface** — what is public/trusted vs internal/input:
   - Code that accepts input (network ports, HTTP, files, URL params).
   - Code that executes things (shell, `exec`, subprocesses).
   - Anything that stores or reads credentials.
   - Anything deployed or published (workflows, web reader, PDF/EPUB builds).
2. **Scan mechanically first** — run these and report raw hits:
   - Secrets: `rg -ni '(password|secret|token|api[_-]?key|BEGIN (RSA|OPENSSH|EC) PRIVATE KEY|authorization|bearer)' <scope>` — then triage each hit as real secret / placeholder / false positive.
   - Plain HTTP or weak TLS: `rg -n 'http://' <scope> | rg -v 'http://localhost|https?://example'`.
   - Injection points: `rg -n 'exec\.Command|os/exec|eval\b|innerHTML|document\.write|sh -c' <scope>`.
   - Unbounded reads: `rg -n 'io\.ReadAll|ioutil\.ReadAll|make\(\[\]byte' <scope>`.
3. **Audit per area**:
   - **Code** — with the relevant review-* skill lens: bounds, injection, XSS,
     deserialization, path traversal, resource exhaustion.
   - **Config/credentials** — no secrets in code, config, workflows, or
     generated files; no `{env:}` interpolation exposing tokens to logs;
     `.gitignore` covers secrets; nothing secret committed (check `git log`
     for historical secrets if asked).
   - **Network** — TLS enforced where required, no hardcoded internal
     addresses, timeouts to prevent slowloris/hangs, ports bind to the right
     interfaces.
   - **CI/CD supply chain** — pinned action versions (not `@main`/`@master`),
     third-party actions audited, `permissions:` scoped to minimum, secrets
     only in the jobs that need them, no secrets echoed in logs, `pull_request_target` understood, artifact/release signing considered.
   - **Dependencies** — for dirs with a `go.mod`/`package.json`, note the
     policy: check for known-vulnerable deps if a scanner exists (`govulncheck
     ./...`, `npm audit`) and report, or state that the repo is stdlib-only.
4. **Report** — severity-ranked, with the fix for each.

## Severity guide

- **Critical** — remotely exploitable, secrets exposed, code execution from
  untrusted input, supply-chain compromise.
- **High** — exploitable with some precondition (auth-free endpoint, public
  port, unvalidated file path).
- **Medium** — info disclosure, weak defaults, missing hardening.
- **Low** — hygiene (log verbosity, error details leaking internals).

## Output format

1. **Attack surface summary** — the inputs/executors/secrets inventory.
2. **Mechanical scan results** — raw hits, triaged.
3. **Findings** — severity, `file:line`, exploit/what-would-go-wrong, fix as a
   code/config snippet.
4. **Clean bill** — explicitly list what you checked and found safe.
5. **Commands run** — the scanners and their output.

Rules: no fear-mongering — a finding must include the concrete path to harm;
distinguish "placeholder/example" from real secrets; when asked to fix, apply
edits and re-scan before reporting done.
