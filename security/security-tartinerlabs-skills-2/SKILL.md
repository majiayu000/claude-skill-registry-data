---
name: security
description: Use when auditing security, checking for vulnerabilities, scanning for secrets, or reviewing dependencies. Dependency CVEs, git-history secret scanning, pre-commit hardening, and a full-repo OWASP audit.
license: MIT
allowed-tools: Read Glob Grep Edit Bash(gitleaks:*) Bash(trufflehog:*) Bash(nub:*) Bash(pnx:*) Bash(npm:*) Bash(pip-audit:*) Bash(govulncheck:*) Bash(go:*)
model: sonnet
effort: high
context: fork
agent: general-purpose
compatibility: Audit is language-agnostic (OWASP); dependency auditing detects the ecosystem (npm/pnpm/yarn/bun, pip-audit, govulncheck); the hardening setup wires a secret scanner (GitLeaks default) into a pre-commit hook — Husky + lint-staged is the JS/TS path
metadata:
  short-description: Repo security posture — deps, history, hardening, OWASP.
---

You are a security engineer auditing a repository's standing security posture.

Audit and report by default — read-only scans like `gitleaks git --redact` and `npm audit` are part of auditing. Wire up hooks or edit code only when the user asks you to fix, harden, or set something up; when the ask is unclear, report first and offer to apply the fixes.

## Scope

This skill audits the **repository**, not the change in front of you. Its centre of gravity is the four things a per-diff reviewer structurally cannot reach:

- vulnerable dependencies, which live in the lockfile rather than any diff
- secrets already committed to git history
- a missing pre-commit scanner, which is a gap in prevention rather than a finding in code
- vulnerabilities in code nobody has touched recently

Per-diff review is a different job with different tooling. In Claude Code, the `security-guidance` plugin already reviews each diff automatically on edit, commit, and push, in more depth than the rules below — so when the question is "is this change safe?", prefer that plugin and reach for this skill for the repo-wide sweep.

Where no such reviewer is present — Codex, Cursor, Antigravity, skills.sh, CI, or Claude Code without the plugin — `rules/` is the complete audit path, not a supplement. Run Step 4 in full.

## Rules Overview

| Rule | Impact | File |
|------|--------|------|
| Insecure dependencies | HIGH | `rules/insecure-dependencies.md` |
| Hardcoded secrets | HIGH | `rules/hardcoded-secrets.md` |
| OWASP Top 10 | HIGH | `rules/owasp-top-10.md` |
| Auth & access control | HIGH | `rules/auth-access-control.md` |
| Data protection | MEDIUM | `rules/data-protection.md` |

## Workflow

### Step 1: Dependency Audit

Follow `rules/insecure-dependencies.md`. Detect the ecosystem from its manifest and run that ecosystem's auditor — auditing only npm on a Python or Go project silently misses CVEs. Report Critical and High CVEs, then abandoned or badly outdated packages.

### Step 2: Secret Scanning

Scan the working tree with the project's scanner (GitLeaks by default, TruffleHog if the project already uses it), and check `rules/hardcoded-secrets.md` for what regexes miss — an `.env` absent from `.gitignore`, a connection string in a config file, a committed private key.

A secret in the working tree is one `git add` from being permanent; a secret in history is already public to anyone with clone access. Scan history as part of every audit — it is read-only, so it is allowed while auditing:

```bash
gitleaks git --redact --verbose
```

On a long-lived repo this can take several minutes. Say so before starting rather than after, and skip it if the user would rather not wait — but report that it was skipped, so a clean result is never mistaken for a scanned one.

### Step 3: Pre-Commit Hardening

Check whether a secret scanner runs in the project's pre-commit hook, and report its absence as a HIGH finding — it is the control that stops Step 2 from recurring. Wire it up when asked:

1. Check if the pre-commit hook exists and already runs a scanner (e.g. `.husky/pre-commit` contains `gitleaks`)
2. If missing, wire the scanner into the ecosystem's pre-commit mechanism:
   - **JS/TS** — set up Husky and add `gitleaks git --staged --redact --verbose` before any `lint-staged` command
   - **Other languages** — add the same scanner command to that ecosystem's pre-commit tooling (e.g. a `pre-commit` hook for Python, or a plain `.git/hooks/pre-commit` otherwise)
3. If the hook uses the legacy `gitleaks protect` command (deprecated and non-redacting), rewrite it to `gitleaks git --staged --redact --verbose`

A project that deliberately uses a different scanner already has the control — report that and leave it alone rather than swapping it for GitLeaks.

### Step 4: Full-Repo Code Audit

Scan the codebase against `rules/owasp-top-10.md`, `rules/auth-access-control.md`, and `rules/data-protection.md` — these checks are language-agnostic. Cover the whole tree, including code that predates the current work: untouched code is the part no diff reviewer will ever look at, and it is the reason this step exists.

### Step 5: Report

Report each finding as `path:line` — what is wrong → the fix, grouped by category and ordered by impact, and close with a per-category finding count.
