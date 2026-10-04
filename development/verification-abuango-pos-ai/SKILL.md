---
name: verification
description: "Run verification checklist before marking work complete. Use when verifying task completion, checking deployment success, or when user mentions 'verify', 'check work', 'confirm complete', 'verification'."
allowed-tools: Read, Bash, Glob, Grep
---

# Work Verification

Run verification checklist to confirm work is actually complete. **Never trust output alone.**

## Setup
Before starting: check `.handoff/sessions/` for active sessions, read context `status.yaml`, run `git status`. Follow `.rules/universal.md` (Plan -> Approve -> Execute).

<!-- Rules loaded from .rules/universal.md -->

## Commands

- `/verify task {files...}` - Verify task completion
- `/verify deploy {team} {service}` - Verify deployment
- `/verify pr` - Verify PR readiness
- `/verify tests {path}` - Verify tests pass

## Core Principle

Agent outputs can describe work without actually performing it. **Verification is mandatory.**

## `/verify task {files...}`

1. **File existence:** `ls -la {files}`
2. **File content:** Read each file, check syntax, logic, no placeholder TODOs
3. **Git status:** `git status && git diff --stat` — verify changes match claims
4. **Run tests:** `php artisan test` / `npm test` / `go test` / `flutter test`
5. **Report:** Files verified table, test results, git status, VERIFIED/NOT VERIFIED

## `/verify deploy {team} {service}`

1. Check deployment platform status (via MCP if configured)
2. Health endpoint: `curl -s -o /dev/null -w "%{http_code}" https://{url}/health`
3. Check logs for startup errors / exceptions
4. Version verification: `curl https://{url}/api/version`

## `/verify pr`

1. Branch status: `git log origin/main..HEAD --oneline`
2. Run tests
3. Run linting
4. Check for debug code: `grep -r "console.log\|debugger\|dd(\|dump(" .`

## Red Flags

- Perfect metrics (100% pass, 95%+ coverage) — suspicious
- Rapid completion of complex work
- Detailed docs without evidence
- No error mentions — real work always has hiccups

## Enforcement

**No verification = No completion.** Status should only show complete after files verified, tests run and passing, git status reviewed.

Full SOP: `docs/system/sops/verification-protocol.md`

## Self-Assessment (Internal)
Rate this skill execution 0-10. If < 8, write feedback to `.handoff/feedback/{date}-{skill-name}.yaml` with: skill, rating, friction, suggestion, context. Do not mention to user.
