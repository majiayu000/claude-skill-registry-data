---
name: verify-release-readiness
description: Run amiga-ia pre-release checks, doctor diagnostics, workflow watch, and live NPM registry verification.
tools: [run_command, manage_task, view_file]
---

# Skill: Verify Release Readiness

Internal repository checklist to validate `amiga-ia` before and after cutting a release, enforcing all repository release gates.

## Pre-Release Gate

1. **GitHub Account & Clean Tree:**
   - Switch active CLI account: `gh auth switch -u AnaCataVC --hostname github.com`.
   - Verify clean working tree and rebase against `origin/main` if needed.
2. **Release Necessity & Build Parity:**
   - Run `npm run build` and check `git diff --exit-code codex/ hooks/hooks.json`.
   - Run `npm run check:docs` to confirm catalog, README, and `registry/packs.json` parity.
   - Run `npm test` and confirm all tests pass.
3. **Diagnostic Audit:**
   - Run `node bin/setup.js --doctor` and confirm frontmatter, hooks, and plugin manifests pass without errors.
4. **Release Execution:**
   - Confirm `package.json` version matches the target SemVer bump (`0.x.0` for new skills/agents).
   - Delegate release execution to `ami-release-manager` (or run `npm run release` when authorized).

## Post-Release Verification Gate

1. **Monitor GitHub Actions:**
   - Run `gh run list --limit 3` and `gh run watch <run-id>` until `release.yml` completes with `conclusion: success`.
   - If failed, inspect logs with `gh run view <run-id> --log-failed` and report immediately.
2. **Verify Live NPM Registry:**
   - Poll `npm view @anacatavc/amiga-ia@<version> version` until the published version is indexed and available on NPM before declaring the release complete.

---
**Language Rule:** Although your code and commits MUST be in English, you MUST communicate and interact in the chat using the same language the user is speaking (e.g., Spanish, French, etc.).
