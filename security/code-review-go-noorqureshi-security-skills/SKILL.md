---
name: code-review-go
description: >
  Security review of Go code — dangerous sinks and web-framework pitfalls. Load when reviewing a Go
  codebase/PR, on .go source in scope, or "review this Go". Signals: go.mod, net/http, os/exec,
  text/template, database/sql, gin/echo/fiber.
domain: code-review
type: reference
stability: learning
modes: [bugbounty, defense, pentest]
severity: info
cwe: [CWE-78, CWE-89, CWE-79, CWE-22, CWE-918]
tools: [gosec, semgrep, govulncheck, ripgrep]
schema_version: 1
---

# Go source review

## When it applies
Reviewing Go source (an API, a CLI, a microservice). Go is memory-safe, so the bugs are logic and
injection: command exec, the wrong template package, string-built SQL, and path/SSRF handling.

## Why it works
Go's stdlib gives a safe and an unsafe option side by side (`html/template` vs `text/template`;
parameterised `db.Query(?, x)` vs `fmt.Sprintf` into a query). Reviews find code that reached for the
unsafe one, or that shells out with `sh -c`.

## Sinks & patterns (grep, then trace to user input)
- **Command exec**: `exec.Command("sh","-c", …)` / `exec.CommandContext` with concatenated input
  (safe form passes args separately — flag the `sh -c` variant).
- **XSS**: `text/template` used to render HTML (no auto-escaping); manual `w.Write([]byte(userHTML))`.
- **SQLi**: `fmt.Sprintf`/string concat into `db.Query`/`db.Exec` instead of placeholders.
- **Path traversal**: `filepath.Join(base, userInput)` without `filepath.Clean` + prefix check;
  `http.ServeFile` with user paths.
- **SSRF**: `http.Get`/`http.NewRequest` on user-supplied URLs; missing host allowlist.
- **Other**: `text/template`/`html/template` injection from user-controlled template strings,
  unvalidated `Unmarshal` into structs (mass assignment), `unsafe` pointer use, weak `math/rand`
  for tokens (use `crypto/rand`).

## Framework specifics
- **gin/echo/fiber**: `c.Param`/`c.Query`/`c.Bind` sources; check bound structs for mass assignment
  and missing auth middleware on state-changing routes.
- **Templates**: confirm `html/template` (not `text/template`) for anything rendered to a browser.

## Method
1. Run `gosec` and `govulncheck` for a first pass; treat as leads, not verdicts.
2. `rg 'exec.Command|text/template|Sprintf.*Query|filepath.Join'` and trace to request input.
3. Check auth/authorization middleware coverage on each route group.
4. Confirm exploitable classes with the matching runtime skill.

## Gotchas
- `exec.Command(name, arg1, arg2)` (no shell) is safe — only the `sh -c "...user..."` form injects.
- `html/template` context-escapes; the bug is usually using `text/template` by mistake.
- Errors ignored with `_` can hide security-relevant failures (e.g. an auth check's error).

## References
Go security best practices; `gosec` rule set; OWASP Go SCP; `govulncheck` (known-vuln deps).
