---
name: vuln-guard
description: Use when reviewing changes or committing ANY Go code in this project — catches security vulnerabilities that scanners miss (auth/crypto logic, unsafe API use, injection). Pairs with the gosec + govulncheck pre-commit gates and the CI SBOM/grype scan.
---

# Vuln Guard

Goal: **no exploitable vulnerability reaches the repo.** Layers:

- **Deterministic, pre-commit** — `gosec` (Go SAST, 30+ rules) and `govulncheck`
  (reachable dependency/stdlib CVEs) run in the git `pre-commit` hook
  (`mise run scan:code:staged`) and block the commit on a finding.
- **Deterministic, CI** — `syft` builds a CycloneDX SBOM and `grype` scans it for
  CVEs (`mise run sbom` + `mise run scan:sbom`), as a dependency safety net.
- **AI review (this skill)** — before you (Claude) `git commit`, the PreToolUse hook
  injects this checklist so you reason about logic-level security the scanners can't.

## Review the staged diff for:

- **Crypto**: `math/rand` for anything security-relevant (use `crypto/rand`), weak
  hashes (MD5/SHA1) for security, hardcoded keys/IVs, `tls.Config{InsecureSkipVerify:true}`,
  outdated TLS versions, ECB/static-IV modes.
- **Injection & untrusted input**: building SQL/commands/paths from user input,
  `os/exec` with a shell or interpolated args, `text/template` (not `html/template`)
  for HTML, path traversal (`..`), unvalidated deserialization.
- **AuthN/AuthZ logic**: missing permission checks, `==` for secret comparison
  (use `subtle.ConstantTimeCompare`), JWT alg/signature not verified, predictable
  tokens/IDs, auth bypass on error paths.
- **Memory/DoS**: unbounded reads/allocations from input, missing size limits on
  request bodies, integer overflow in size math, `ReadAll` on untrusted streams.
- **Resource handling**: missing `defer Close()`, leaking file descriptors,
  TOCTOU on files, world-writable file perms (`0666`/`0777`).
- **Errors that leak**: returning internal errors/stack traces to clients,
  logging secrets or PII.

## How to act

1. Run `git diff --cached` and check the categories above.
2. On a finding: fix it, or if it is a deliberate false positive, annotate narrowly
   (`//nolint:gosec // reason`) — never silence whole files.
3. For a flagged dependency CVE (govulncheck/grype): bump the module, or if no fix
   exists, confirm the vulnerable symbol is unreachable and document why.

## Notes

- gosec/govulncheck are the hard gates; this skill is the logic-level safety net.
- SBOM/grype run in CI (heavier, network) — see `mise run ci`.
