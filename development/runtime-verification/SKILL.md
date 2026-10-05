---
name: runtime-verification
description: "Verify code works at runtime through build verification (mandatory), LSP diagnostics, ad-hoc verification for projects without frameworks, E2E and smoke tests, and visual verification (screenshot-analyze-verify for UI changes). Skip whitelist strictly enforced (markdown-only, config-only, dependency-bump-only with evidence); all other skips require Proactive-Autonomy escalation. Use after quality checks pass to confirm the code actually runs. This skill MUST be consulted because no test framework is not an excuse to skip; build failure IS a finding and must be fixed."
allowed-tools: Bash, Read, Glob, Grep, LSP, TaskCreate, TaskList, TaskUpdate
agent: Explore
---

# Runtime Verification

## Contract

Iron law: **no completion until the code builds, runs, and behaves correctly; if you cannot verify it, build the infrastructure to verify it.** Invoked after quality checks pass by `/flow:start` Phase 4 step 2, `/flow:pr` Phase 4 via `Agent(integration-verifier)`, and the `address-pr`, `debug`, and `start-issue` workflows. Returns the Runtime Verification Results and Acceptance Criteria Verification tables, with failures as P1 findings (`category=runtime`). Permitted skips: only `markdown-only`, `config-only`, or `dependency-bump-only`, each with its listed evidence; any other skip needs an approved six-field escalation via `AskUserQuestion`.

## Skip Whitelist

| Category | Definition | Required evidence |
|----------|------------|-------------------|
| `markdown-only` | Only `.md`, `.markdown`, `.txt`, `.rst` files | `git diff --name-only origin/$DEFAULT_BRANCH..HEAD` showing only doc extensions |
| `config-only` | Only config files (`.json`, `.yaml`, `.yml`, `.toml`, `.ini`, `.env.example`, dotfiles) with no code-path change; syntax still validated (lint/schema, dry-run) | Full file list plus validation output |
| `dependency-bump-only` | Only lockfiles and manifest version strings (`package.json` version, `package-lock.json`, `poetry.lock`, `Gemfile.lock`, `go.sum`, `Cargo.lock`); no source, config semantics, or new dependencies; build still succeeds | Full file list plus build output |

Mixed diffs (a whitelisted category plus one `.py` file, a new dependency, or a behavior-changing config value) get full verification. "Small change", "CI-only", "tests cover this", "just a refactor" are not categories.

**Out-of-whitelist skips** (anything uncovered): raise a Proactive-Autonomy escalation per [`references/escalation-format.md`](../../references/escalation-format.md) via `AskUserQuestion` and wait for approval; Situation cites why the whitelist misses the change, Tried lists the fast-path, build, and smoke attempts. Blanket repo-wide authorization is never valid.

## Sequence

1. **Fast path**: an executable `verify.sh` or `scripts/verify.sh` is run and its results returned.
2. **Build** (mandatory, every project type; per-stack commands and tables in [`runtime-verification-probes.md`](../../references/runtime-verification-probes.md)). Build failure IS the finding: read errors, fix, rebuild up to `closedLoop.maxBuildIterations` (default 5).
3. **LSP diagnostics** when `lsp.enabled` and `lsp.diagnosticsAsQuality` (both default `true`): Error=P1, Warning=P2, Info/Hint=P3, deduplicated against CLI output, bounded by `lsp.timeout` (default 5000 ms); timeout or no server is N/A, never a block.
4. **Dev server**: use `capability-discovery` output. Won't start: read the error, fix, retry up to `closedLoop.maxServerRetries` (default 3); port busy: another port; startup wait `timeouts.devServerStartup` seconds (default 30).
5. **Smoke**: `curl` `/health` and `/`; non-200 is a P1 finding (`references/finding-schema.md`).
6. **E2E** when a framework exists, within `timeouts.e2eTest` (default 120); otherwise ad-hoc verification by project type (reference); "no test framework" is a problem to solve, not a skip.
7. **Acceptance criteria**: map each to a method (reference table) and record Pass/Fail/N/A.

On any failure: read the full error, root-cause it (`debugging-patterns`), fix, re-verify, up to `closedLoop.maxDebugIterations` (default 5), then escalate; the user never supplies logs.

## Completion

UI-relevant diffs (rules in `skills/visual-verification/SKILL.md`) also run `Skill(visual-verification)` in parallel; if the dev server cannot start, that skill returns `SKIP` ("dev server unavailable") and the server failure is the primary finding; tables render side by side. `visualVerification.*` settings belong there.

Complete only when every testable criterion has Pass/Fail/N/A with a reason and every failure, including a dev server that won't start, is a P1 finding.

## Output Format

```markdown
### Runtime Verification Results

| Check | Status | Details |
|-------|--------|---------|
| Dev server | {Running/Not found} | Port {N} |
| Health check | {Pass/Fail/N/A} | HTTP {status} |
| E2E tests | {Pass/Fail/N/A} | {framework} |
| Smoke tests | {Pass/Fail/N/A} | {details} |
| LSP diagnostics | {Pass/Fail/Skip/N/A} | {errors: N, warnings: N, files checked: N} |

### Acceptance Criteria Verification
| # | Criterion | Verified | Method |
|---|-----------|----------|--------|
| {n} | {ui criterion} | Pass/Fail | visual-verification `Observed:` blocks → bundle `### Visual analysis` |
```
