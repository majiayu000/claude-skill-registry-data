---
name: project-baseline
description: Check a repository against a baseline of engineering practices (validated env module, secret scanning, coverage ratchet and more) and propose each missing one as a backlog item, after approval; not a code audit (audit-to-backlog). Use when starting work in a repository or when the user asks what the project is missing; for example "what is the repo missing", "project baseline".
license: MIT
compatibility: "Claude Code"
---

# Project baseline

A presence check, not a code review: each practice has a probe, and a missing practice becomes a backlog item. Read-only until the user approves.

## 1. Context

- Detect the stack, the lockfile-selected package manager, the CI workflows, and the validation commands.
- Find the backlog paths exactly as audit-to-backlog does: a `Backlog: <todo path>, <done path>` line in `AGENTS.md` or `CLAUDE.md`, otherwise `TODO.md` and `TODO-done.md`. Read both if they exist and continue their category numbering under the ID prefix `BASE`.
- Read the project's `AGENTS.md`, `docs/pitfalls.md`, and decision records: a practice the project rejected or deferred on purpose is reported as `deliberate`, never proposed.

## 2. Probe each practice

| Practice | Present when | Missing → |
|---|---|---|
| Env read through one validated module | a single module parses `process.env` (or the stack's equivalent) with a schema (zod or similar), and `rg` finds no direct env reads elsewhere in app code | P2 |
| Agent deny-list for secrets | `.claude/settings.json` `permissions.deny` covers `.env*` and key files (`*.pem`, `*.key`) | P2 |
| Secret scanning in CI | a CI step runs gitleaks, trufflehog, or the host's secret scanning | P2 |
| Coverage floor that only rises | the test config sets coverage thresholds and CI enforces them | P2 |
| Additive-only migration guard | CI fails on destructive migrations (drop/rename) without an explicit marker | P2; skip without a database |
| Dependency/boundary rules | dependency-cruiser, eslint boundaries, or a layer test that fails CI | P3 |
| Real-database test tier | tests run against a real database (Docker or a CI service), not only mocks | P2; skip without a database |
| Safe error responses | API errors return one envelope with a code and a message (`details` optional), as error-handling-conventions defines; no stack traces or internal fields | P1 when a stack trace or internal error reaches a response, otherwise P2; skip without an API |
| CHANGELOG | `CHANGELOG.md` in Keep a Changelog format | P3 |
| Docs-vs-code consistency check | a script or CI step checks docs against code (commands, paths, versions) | P3 |
| Design system file | a project with a UI (components, pages or stylesheets in app code) has a root `DESIGN.md` in the DESIGN.md format (YAML tokens, then Overview … Do's and Don'ts) | P3; skip without a UI. When present, suggest `npx @google/design.md lint DESIGN.md` for the user to run; never run or install it |
| No runtime dependency two majors behind | the package manager's outdated report (`pnpm outdated --prod`, `npm outdated --omit=dev`, `yarn outdated`, `uv pip list --outdated` limited to the `pyproject.toml` dependencies, `bundle outdated`) lists no runtime dependency two or more major versions behind its latest release | P2 for a framework or runtime dependency, otherwise P3; skip when the report needs credentials or the network is unavailable, and say so; a nonzero exit from the outdated command alone is not a failure. `bundle outdated` evaluates the `Gemfile` and `yarn` runs the file a `.yarnrc*` names in `yarnPath`/`yarn-path`: both run repository code, so ask before either. Each item's `Done when` names the target version; its Check fails until the lockfile resolves that major, written for the lockfile's format (for example `rg -q '/next@15\.' pnpm-lock.yaml`). Dispatch nothing during the probe: the report offers upgrade plans (step 5) |
| Dependency release-age cooldown | the update bot or package manager enforces a minimum release age before a new version is taken (Dependabot `cooldown`, Renovate `minimumReleaseAge`, pnpm `minimumReleaseAge`, uv `exclude-newer`) | P3; skip without dependencies |
| After-edit lint hook | `.claude/settings.json` has a `PostToolUse` hook on `Edit\|Write` that reads `tool_input.file_path` from stdin, lints that file, and exits 2 with only the failures on stderr | P3; skip without a linter |
| Agent sandbox | `.claude/settings.json` sets `sandbox.enabled: true` and `~/.ssh` and `~/.aws` are denied to it, in `sandbox.filesystem.denyRead` or as `sandbox.credentials.files` entries with `"mode": "deny"` (the sandbox reads them by default); the guard and permission rules match text, the sandbox restricts every command | P2 |
| Pinned MCP servers | every stdio server in `.mcp.json` runs a pinned version (`npx -y pkg@1.2.3`, `uvx pkg==1.2.3`, an image digest), with no `@latest` and no bare package name; a server's tool descriptions reach the model, so a version bump is reviewed like a dependency | P2; skip without `.mcp.json` |
| Gate verdict in the exit code | every CI and validation script exits non-zero on failure (no `\|\| true`, no `continue-on-error` on gates) | P2 |

Record each probe and its result as the evidence: the command or file checked, and what it found. Unsure counts as unsure, not missing: list it under questions.

## 3. Decisions, not defaults

Never propose a default for these; when the repository is inconsistent (two lockfiles, two test runners, mixed commit languages), list the evidence and ask the user to choose:

- Package manager (npm vs pnpm)
- Test runner (Jest vs Vitest)
- Authentication library
- Monitoring stack
- Commit message language

## 4. Draft the backlog items

One item per missing practice, in audit-to-backlog's shape, filed under its severity section and deduplicated against both backlog files:

```markdown
- [ ] BASE-03 · P2 · Secret scanning in CI
  - Where: `.github/workflows/ci.yml:1`
  - Problem: no CI step scans for committed secrets.
  - Evidence: `rg -l 'gitleaks|trufflehog' .github/` → no match.
  - Fix: add a gitleaks step to the CI workflow that fails the job on a finding.
  - Size: S
  - Done when: CI fails on a commit that contains a secret.
  - Check: `rg -q 'gitleaks' .github/workflows/`
```

## 5. Report and ask

```
Project baseline — <repo>
Present: 6   Missing: 4 (P2 3, P3 1)   Deliberate: 1   Not applicable: 1
Needs your decision: test runner — package.json has both jest and vitest

Write the 4 items to TODO.md? A: all (recommended)  B: list IDs  C: none
Plan the 2 upgrades with dependency-upgrader first (reads changelogs on the web)? yes / no
```

The second question appears only when the dependency probe found items. On a yes, dispatch `developer-os:dependency-upgrader` once per dependency, for at most the three furthest behind, and put its steps into the item's Fix and its estimate into its Size before writing; mark its `ASSUMPTION:` lines as such in the item. The install commands in a plan are text for the user to run, never commands this skill runs.

If the backlog files do not exist yet, ask for the paths and record them as a `Backlog: <todo path>, <done path>` line in `AGENTS.md` (or `CLAUDE.md`), with its git-ignored path warning, as audit-to-backlog does.

## Stop point

Stop after the report and the question. After approval, merge the approved items into the backlog file with `Session N: <ID>, …` lines of 5–7 items each (fewer than 5 items: one session) under `## Implementation sessions`, grouped as audit-to-backlog groups them, show `git diff --stat`, and stop; implementation is implement-backlog's job.

## Never

- Write or create any file before the user approves.
- Pick a default for a "needs your decision" item.
- Install dependencies, add CI steps, or change configuration; this skill only proposes.
- Commit, push, or open a pull request.
- Propose a practice the project rejected on purpose.
