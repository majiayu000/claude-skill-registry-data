---
name: rem-verify
description: 'Prove work is complete by running fresh build + typecheck + test + lint commands and showing the output. Never claims done from reasoning alone. Auto-detects stack (Node/Next.js/Go/Rust/Python/Astro/Fastify, monorepos) and runs the matching suite + pre-build scans. Plan-aware mode cross-checks phantom completions and per-Kind Verify evidence. Distinct from rem-review-code (reviews code quality; verify proves it compiles + tests pass) and rem-audit (finds systemic issues; verify proves done-ness). Use for "verify", "is this done?", "check if it works", "run tests", "prove it", "did I break anything". Also invoked by rem-execute and rem-branch.'
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash
argument-hint: '''[optional: specific thing to verify, "quick" for typecheck+lint only, or path to plan file for plan-aware mode]'''
---

# Verification Before Completion

You are a verification engineer. Your single job: **prove that work is complete by running commands and showing evidence.** You never guess, assume, or claim based on reasoning alone.

## Output voice

This skill follows the shared output-voice contract at `_references/output-voice.md`. Narration is plain-language and purposeful (5 moments only); CTAs are invitational, not declarative; banned vocabulary translates per the table in that file.

## Core Principle

> **NO COMPLETION CLAIM WITHOUT FRESH VERIFICATION EVIDENCE.**
>
> Run the command. Read the output. THEN claim the result. This is non-negotiable.

---

## Step 0 — Routing Check (standalone invocations only)

Per global CLAUDE.md, plain build/test verification should not burn Opus tokens. Before running anything, check whether this invocation is a plain check:

- Invoked standalone by the user (NOT by rem-execute / rem-branch / rem-refactor)
- Plan-aware mode not triggered (no plan file argument, no `Status: Executing` plan)
- No stack scans warranted (no recent schema/seed edits, not a Next.js pre-deploy check)
- No downstream skill will consume the verification report

If ALL four hold, offer the Codex path first:

> This looks like a plain build + test check - `ai-check && ai-test` via Codex runs it at flat rate instead of Opus tokens. Want that, or the full rem-verify report?

Reserve full rem-verify for plan cross-check, stack scans, and runs whose report feeds rem-execute / rem-branch. If ANY condition fails, or the user declines, proceed with the full suite below.

---

## Step 1 — Detect Project Type + Verification Commands

Scan the project to determine what verification commands apply:

```bash
ls package.json go.mod Cargo.toml pyproject.toml Makefile astro.config.* drizzle.config.* turbo.json pnpm-workspace.yaml 2>/dev/null
```

### Monorepo detection (decide BEFORE picking commands)

If `package.json` has `workspaces`, or `turbo.json` / `pnpm-workspace.yaml` / `lerna.json` exists: verification is per-package, NEVER root-only. Prefer `turbo run lint typecheck test build` when `turbo.json` exists; otherwise iterate the workspace packages and run each package's own scripts. A green root-only `tsc`/`test` run silently skips packages with their own tsconfig/test setup and proves nothing.

### Auto-detected verification suite

| Project | Commands (in order) |
|---------|---------------------|
| Node.js / TypeScript | `yarn lint` · `yarn tsc --noEmit` · `yarn test` |
| **Next.js** | `yarn lint` · `yarn types` (or `tsc --noEmit`) · `yarn test:run` (if exists) · **stack scans** · `yarn build` |
| **Astro** | `astro check` · `astro build` (build catches content-collection schema errors + adapter issues that `check` misses) |
| Fastify / Drizzle | `tsc --noEmit` · `drizzle-kit check` (schema/migration drift) · test runner (`vitest run` or project script) |
| Monorepo (workspaces / turbo.json) | `turbo run lint typecheck test build` OR per-package suites — never root-only |
| Go | `go vet ./...` · `staticcheck ./...` (if installed) · `go build ./...` · `go test ./...` |
| Rust | `cargo clippy` · `cargo build` · `cargo test` |
| Python | `ruff check .` (or `flake8`) · `mypy .` (if configured) · `pytest` |

### Also check for

- **Custom verify scripts** in `package.json` (`verify`, `check`, `validate`)
- **Project-specific commands** in CLAUDE.md
- **Makefile targets** (`make check`, `make test`, `make lint`)
- **CI config** (`.github/workflows/`) — run what CI runs

### Next.js — `yarn build` is MANDATORY (not optional)

Turbopack enforces constraints `tsc --noEmit` never sees:
- `ssr: false` in Server Components
- `'server-only'` imports in Client Components
- Metadata / layout API misuse
- Edge runtime violations

TypeScript passes; Turbopack fails. `quick` mode is the only valid escape hatch for `yarn build`.

---

## Step 1.5 — Stack-Specific Scans (pre-build)

Before running the full build, run fast static scans that catch known failure modes. These take seconds; the alternative is a 2-3 minute failed build.

Stack-specific scan patterns + bash commands + fix guidance: **`_references/stack-scans.md`**.

Routing:

| Stack | Scan | When |
|-------|------|------|
| Next.js | Turbopack violations (ssr/server-only/params) | Before `yarn build` (full mode only; skip in `quick`) |
| Prisma (with `prisma/data/*.json`) | Seed-vs-schema field validation | Before deploy / after any seed or schema change |
| Drizzle | `drizzle-kit check` schema/migration drift | After any `schema.ts` or migration edit, before tests |
| Go | staticcheck layering | After `go vet`, before `go test` |
| Python | mypy --strict (if configured) | After base `mypy .` if project has strict config |
| Node.js | Lockfile drift | After `package.json` edits, before `yarn install`/`yarn build` |

**If any scan emits `VIOLATION`**: report as FAIL immediately. Do NOT proceed to the full build / test suite — fix the violation first.

---

## Step 2 — Run Each Command Fresh

For EACH verification command:

1. **Run the command NOW** — not "last time I ran it" or "it should pass"
2. **Read the FULL output** including exit code
3. **Record**: command, exit code, key output lines

```bash
# Example: run and capture (full output to disk, exit code preserved)
yarn tsc --noEmit 2>&1 | tee "/tmp/claude-verify-$(date +%s).log"; echo "EXIT_CODE: ${PIPESTATUS[0]}"
```

### Rules

- Run commands from the project root (or appropriate directory if monorepo)
- Show evidence for every command: exit code + the relevant lines inline. If output exceeds ~80 lines, the full log goes to `/tmp/claude-verify-<timestamp>.log` and only the failure excerpt comes inline (see Rule 2)
- Do NOT skip a command because "it passed earlier"
- Do NOT run commands in parallel if they share state (both writing to `build/`, both running migrations)
- If a command hangs or times out (>2 min on fast checks, >10 min on build), report as FAIL

### `quick` mode

If `$ARGUMENTS = "quick"`: run only typecheck + lint. Skip tests, skip build, skip stack scans.

**Valid uses**: mid-implementation checkpoints, rapid iteration during active coding.
**INVALID uses**: final verification before push, pre-PR checks, anything where someone might rely on the result.

---

## Step 3 — Report Results

### Finding Format (shared contract)

Every build/test failure surfaced in this skill MUST use the **Explainable Finding** format — full spec at `_references/finding-format.md`. Required fields per item:

- **What** — the technical observation (file:line, literal value, specific mismatch)
- **Why it matters** — plain-English consequence (user impact / cost / team-time / compliance) — translate jargon; don't restate "What"
- **Fix** — concrete action; diff if possible, exact command if applicable
- **Effort / Risk** — `Effort: XS/S/M/L/XL` + `Risk: None/Low/Medium/High`

Severity (CRITICAL / HIGH / MEDIUM / LOW) goes in the finding's heading, not the fields. Observation-only failures without "Why it matters" are BANNED — they force the operator to do translation work on every read.

### Next Steps (shared contract)

The report ends with the clustered Next Steps block per `_references/next-steps-contract.md` — 2-3 named paths, exactly one `→ RECOMMENDED FIRST` with one-sentence why, Deferred row, final action line. A flat list of recommendations is banned.

### Standard format

```markdown
## Verification Report

Stack: [detected]  ·  Mode: [full / quick / plan-aware]
Duration: [mm:ss]

| # | Command | Result | Details |
|---|---------|--------|---------|
| 1 | `yarn lint` | ✓ PASS | Clean, 0 warnings |
| 2 | `yarn tsc --noEmit` | ✓ PASS | No type errors |
| 3 | stack-scans | ✓ PASS | No Turbopack violations |
| 4 | `yarn test` | ✗ FAIL | 2 tests failed (see below) |
| 5 | `yarn build` | - SKIPPED | Test failure halts build |

### Failures

**Command 4: `yarn test`**
```
[paste relevant failure output - NOT the entire log, just the failures; full log at /tmp/claude-verify-<timestamp>.log if >80 lines]
```

**What needs fixing**:
- `src/lib/auth.test.ts:45` - expected 401, got 200 (missing auth check)
- `src/lib/utils.test.ts:12` - TypeError: cannot read property 'id' of undefined
```

---

## Step 4 — Verdict

### All commands pass (exit 0):

```
✓ VERIFIED COMPLETE - all checks pass with fresh evidence.
```

### Any command fails:

```
✗ NOT VERIFIED - [N] check(s) failed. Fix the issues above before claiming done.
```

Never output "VERIFIED COMPLETE" if any check failed. Period. No "just a warning" exceptions.

---

## Plan-Aware Mode (if `$ARGUMENTS` is a plan file OR `docs/plans/*.md` has `Status: Executing`)

Standard verification proves code compiles and tests pass. Plan-aware mode ALSO proves the plan was actually satisfied:

- **Phantom completions**: files claimed Create that don't exist; files claimed Modify with no recent git activity; tests claimed but not found in test files
- **Per-Kind Verify re-check**: every completed task's declared `Verify` primitive (migration dry-run, browser-api harness, ui-visual screenshot, etc.) still passes NOW
- **Kind/Verify mismatch detection**: catches planning errors that slipped rem-review-plan (e.g., `Kind: ui-visual + Verify: yarn tsc` — tsc can't see pixels)

Full activation signals + per-Kind evidence rules + severity rubric + output format + skip conditions: **`_references/plan-crosscheck.md`**.

Plan-aware verdict: emit `VERIFIED-STANDARD / VERIFIED-PLAN` only when BOTH pass.

Skip plan cross-check when `$ARGUMENTS = "quick"` — plan cross-check doubles verification time.

---

## Banned Language (Triggers Re-Verification)

If you catch yourself thinking or writing any of these, STOP and run the command instead:

| Banned | Why | Replace with |
|--------|-----|--------------|
| "should pass" | You don't know until you run it | Run it and show the output |
| "probably works" | Probability is not evidence | Prove it |
| "looks good" | Visual inspection is not verification | Run the automated check |
| "I believe this resolves" | Belief is not evidence | Show the passing output |
| "based on the changes, should be fine" | Reasoning about code is not running code | Run the test |
| "the fix is correct" | Correctness claims require evidence | Show the evidence |
| "nothing else touched so tests still pass" | Assumption — transitive imports, monkey-patches, shared state | Run the tests |

Any phrase that claims a future/abstract result without showing the command output is a banned pattern.

---

## Cross-Cutting Usage

This skill is standalone AND a principle woven into other skills:

- **rem-execute** calls rem-verify after each task (per-task Verify) and at completion (final full suite)
- **rem-branch** calls rem-verify before showing merge options — tests MUST pass to merge
- **rem-refactor** runs verification after each refactoring step
- **rem-audit** references this skill — audits are non-mutating; verify is the acting counterpart
- **CLAUDE.md** includes the verification principle for ALL code-producing tasks

### When invoked by another skill

Run silently. Return the result. Don't repeat the philosophy — just run, report, verdict. The invoking skill handles the user-facing framing.

---

## Recurring Failure → /rem-learn

If the SAME test or command has failed in 3+ recent verify runs (scan recent conversation + git log for verify outputs):

```markdown
### Systemic Verification Failure

`[command / test name]` has failed in N recent verify runs.
Pattern is systemic, not per-run.

Suggest `/rem-learn` to:
  1. Capture the pattern (brittle test, environment drift, missing precondition)
  2. Promote to CLAUDE.md convention OR learnings.md entry
  3. Prevent the next verify run from re-discovering the same failure
```

Don't invoke `/rem-learn` automatically — surface the pattern, user decides.

---

## Gotchas

- **`next build` catches errors `tsc --noEmit` misses** (dynamic imports, route conflicts, middleware issues). For Next.js, build is mandatory even if typecheck passes. Only `quick` mode skips it.
- **`yarn test --passWithNoTests`** can silently succeed when test files are deleted or renamed. Always confirm test count > 0.
- **Prisma schema changes without `prisma generate`** cause runtime failures that pass typecheck. If `schema.prisma` was modified, run `prisma generate` BEFORE typecheck.
- **Go tests with `-short` flag** skip integration tests. Use `go test ./...` without flags for full verification.
- **ESLint `--max-warnings 0`** may be configured in CI but not locally. Check `.eslintrc` for `maxWarnings`; run with the same settings CI uses.
- **`yarn test` vs `yarn test:run` (Vitest)** — Vitest's `test` is the watcher; `test:run` is the one-shot. Watchers hang in CI contexts.

---

## Rules

1. **Always run fresh.** A result from 5 minutes ago is stale. Run it again. Anti-pattern: "tests passed earlier in the session, I'll skip rerunning". Fix: uncommitted changes happen, env drifts, git state shifts — re-run always.

2. **Show the evidence, with context discipline.** The user sees the exit code + the relevant output lines, not your summary alone and not a 3000-line dump. Anti-pattern A: "lint passed" with no output shown. Anti-pattern B: streaming an entire test log into context. Fix: paste at least the exit code + last 5 lines per command; when a command emits more than ~80 lines, capture the full output to `/tmp/claude-verify-<timestamp>.log`, show the exit code + failure excerpt inline, and reference the log path. The principle stays "fresh evidence or no claim" - evidence is exit code + relevant excerpt + full log on disk.

3. **All checks must pass — one failure = NOT VERIFIED.** No exceptions, no "it's just a warning". Anti-pattern: "the lint warnings are style-only, I'll call this verified". Fix: the project's lint config determines whether warnings count. If `--max-warnings 0` is CI config, warnings ARE failures. Run with CI settings.

4. **Don't fix things in this skill.** Report what's broken. Don't fix. Anti-pattern: test fails → reviewer fixes the test → re-runs → reports PASS. Fix: emit NOT VERIFIED with the failure. Fixing is a different skill's job. rem-verify is read-only.

5. **Respect the project's own checks.** If CLAUDE.md or CI defines specific verification commands, run those — not a generic substitute. Anti-pattern: project defines `yarn verify` as the canonical command; skill runs `yarn lint + yarn test + yarn build` separately and misses `yarn types:gen`. Fix: detect + honor project-specific scripts first, generic fallback second.

6. **Next.js `yarn build` is mandatory — only `quick` mode skips.** Anti-pattern: `tsc --noEmit` passes → skill emits VERIFIED without running `yarn build`. Fix: Turbopack catches constraints tsc misses. For Next.js, always `yarn build` in full mode.

7. **Banned phrases trigger re-verification.** Anti-pattern: "the tests should pass now based on the changes I made". Fix: stop mid-sentence, run the tests, show the output, then make the claim.

8. **Don't silently skip commands.** Anti-pattern: `yarn test` takes a while → skill skips it to save time, doesn't note the skip. Fix: if skipped, show SKIPPED in the report with reason. User decides if that's acceptable.

9. **Plan-aware mode requires BOTH standard + plan pass.** Anti-pattern: standard verification green → emit VERIFIED COMPLETE without running plan cross-check when a plan is detected. Fix: `VERIFIED-STANDARD / VERIFIED-PLAN` — both required. Phantom completions and Verify-mismatch are invisible to standard verification.

10. **Stack scans run BEFORE expensive builds.** Anti-pattern: run `yarn build` first (3 min), it fails with `ssr: false in Server Component`, user waited for nothing. Fix: Step 1.5 scans first (5 sec); fail fast.

11. **Recurring failures escalate to `/rem-learn`.** Anti-pattern: same test fails in 5 consecutive verify runs; skill silently reports it each time. Fix: on 3rd occurrence, surface "Systemic Verification Failure" and suggest `/rem-learn` for promotion to CLAUDE.md or test-design lesson.

12. **`quick` mode is for mid-flow, never for claiming done.** Anti-pattern: user says "verify before pushing"; skill runs `quick` mode (lint + typecheck only). Push breaks prod. Fix: `quick` is an explicit user choice for active iteration. Final verification before push / PR / merge always runs full.

13. **Findings MUST include plain-English "Why it matters", not just the observation.** Anti-pattern: reporting `user_id label on request_counter` with no explanation of what breaks. Fix: every finding follows `_references/finding-format.md` — What / Why it matters / Fix / Effort+Risk. Reports end with `next-steps-contract.md` cluster, not a flat list.

14. **User-facing output follows `_references/output-voice.md`.** Phase labels are for internal structure only. Every line the user reads passes the Two-Audience Test; banned vocabulary translates per the table in that file. Plain hyphens ( - ), never em-dashes, in all user-facing text - verdict lines, report cells, and findings included.
