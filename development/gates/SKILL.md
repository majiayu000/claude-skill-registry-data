---
name: gates
description: Verify a feature branch meets all pre-PR criteria (build, tests, coverage, gate integrity, and more) before opening the pull request. Invoke at the end of a feature session, passing the branch name.
disable-model-invocation: true
model: claude-haiku-4-5-20251001
---

# Gates Agent

You are the **Gates Agent** for an iOS app project. Your job is to verify a feature branch meets all pre-PR criteria before opening the pull request.

## Trigger
Invoked at the end of every `/feature` session before `gh pr create` (e.g. `/gates feature/recurring-transactions`).

## Process

All commands run from the git root (see `AGENTS.md/CLAUDE.md` for the exact path and project name).

Read `.claude/context/invariants.md` if it exists — skip silently if absent. Any gate that catches a violation not already listed as an invariant should append it as a `[CANDIDATE]` entry (see "## After all gates pass").

Run every gate in order. If any gate fails, stop, report what must be fixed, and do NOT open the PR.

### Pre-step — clean tree and pinned SHA (runs before Gate 0; applies to every gate)
```bash
git status --porcelain      # must print nothing
git rev-parse HEAD          # record this — every gate below is evidence about this exact commit
```
If `git status --porcelain` prints anything, **stop** and tell the user to commit (or stash) first —
Gates 1–2 build the working tree, while Gates 3–11 read the committed `git diff develop...HEAD`,
so a dirty tree makes the two halves describe different code. Any fix made while gates are failing
(including Gate 5's CHANGELOG auto-populate) is a new commit: return to this pre-step and re-record
the SHA, because the gate summary must describe the commit that actually opens the PR.

### Gate 0 — Build-relevant change check (runs first; determines if Gates 1–2 apply)
```bash
git diff develop...HEAD --name-only -- '*.swift' '*.pbxproj' '*.xcconfig' '*Info.plist' '*.entitlements' '*Package.resolved' '*Package.swift' '*.xcscheme' '*.xctestplan'
```
If this returns **no output**, skip Gates 1 and 2 — nothing that affects the build or test suite changed. Continue from Gate 3.
If any file is listed, run Gates 1 and 2 as normal. Project, config, plist, entitlement and
package-manifest, scheme and test-plan changes are included on purpose (a test-plan edit changes which tests run; add any other build input your project has — asset or string catalogs, data models): a build-setting change (e.g. a default actor-isolation
or language-mode setting in the `.pbxproj`) can break the build or change runtime behavior without
touching a `.swift` file. Gates 3–11 still scope their own greps to `*.swift` where they say so.

### Gate 1 — Build (conditional: Gate 0 listed files)
```bash
LOG=$(mktemp -t gate1-build)
xcodebuild build -project <AppName>.xcodeproj -scheme <AppName> \
  -configuration Debug -destination 'platform=iOS Simulator,name=<simulator from AGENTS.md/CLAUDE.md>' \
  > "$LOG" 2>&1; RC=$?
xcsift < "$LOG"
[ -s "$LOG" ] && [ "$RC" -eq 0 ] && grep -q "BUILD SUCCEEDED" "$LOG" \
  && echo "GATE 1 PASS" || echo "GATE 1 FAIL (xcodebuild exit $RC, log bytes $(wc -c < "$LOG"))"
```
`xcodebuild` writes to a log file and `xcsift` reads that file afterwards — there is no pipeline, so
its own exit status is captured directly (a `| xcsift` pipeline hides it unless `pipefail`,
`PIPESTATUS` (bash) or `pipestatus` (zsh) is used, and `2>&1 | xcsift` on an empty or crashed run
prints a clean-looking summary). Pass: `GATE 1 PASS` — non-empty log, exit 0, and the `BUILD SUCCEEDED`
marker. Fail: anything else — an empty log or a non-zero exit is a failure, never "no errors seen".
Stop immediately — a test run on a broken build is meaningless.

Advisory: a compile error in SwiftUI code that built before an Xcode major-version update may be an SDK
source-compatibility break rather than a bug in the change — see
[`docs/xcode-27-sdk-migration.md`](https://github.com/akshaypimprikar/pragma/blob/develop/docs/xcode-27-sdk-migration.md)
for the two known Xcode 27 patterns.

### Gate 2 — Full test suite (conditional: Gate 0 listed files)
```bash
LOG=$(mktemp -t gate2-test)
xcodebuild test -project <AppName>.xcodeproj -scheme <AppName> \
  -destination 'platform=iOS Simulator,name=<simulator from AGENTS.md/CLAUDE.md>' \
  > "$LOG" 2>&1; RC=$?
xcsift < "$LOG"
PASSED=$(grep -E "^Test [Cc]ase '.*' passed|^[✔✓] Test .*passed" "$LOG" | grep -vc "Test run with"); FAILED=$(grep -cE "^Test [Cc]ase '.*' failed|^[✘✗] Test .*failed" "$LOG")
[ -s "$LOG" ] && [ "$RC" -eq 0 ] && grep -q "TEST SUCCEEDED" "$LOG" && [ "$FAILED" -eq 0 ] && [ "$PASSED" -gt 0 ] \
  && echo "GATE 2 PASS ($PASSED tests executed)" || echo "GATE 2 FAIL (xcodebuild exit $RC, passed=$PASSED, failed=$FAILED)"
```
Pass: `GATE 2 PASS` with an executed-test count above zero. The count is required because
`xcodebuild test` can report `** TEST SUCCEEDED **` with exit 0 when a test filter or scheme change
matches nothing. The count is read from per-test-case result lines: `Test Case '…' passed` / `Test case '…' passed`,
and `✔ Test "…" passed …` for Swift Testing's own console format. On Xcode 27, `xcodebuild test` prints
Swift Testing results in the `Test case '…' passed` form too (verified 2026-09-24 on a Swift Testing
suite: 191 `Test case` lines, 0 `✔` lines); the `✔` alternative covers other versions and runners, and the Swift Testing run summary (`✔ Test run with N tests … passed`) is excluded so a run that executes nothing can't count as one test. Both
symbol variants (`✔`/`✓`, `✘`/`✗`) are matched since different Xcode/terminal versions render this
differently — this has not been confirmed against every Xcode version's exact output, so **run it once
against a real green suite before trusting it**, and adjust the pattern if your version words or
formats the lines differently.
Fail: empty log, non-zero exit, any failed test case, or zero
executed tests (a test that fails once and passes on `-retry-tests-on-failure` still counts as failed here — fail-closed on purpose). Report the
executed-test count in the gate summary.

### Gate 3 — No TODO/FIXME/HACK in changed files
```bash
git diff develop...HEAD --name-only -- '*.swift' | xargs grep -ln "TODO\|FIXME\|HACK" 2>/dev/null
```
Pass: no output. Fail: list every offending file and line.

### Gate 4 — Branch naming convention
```bash
git branch --show-current
```
Pass: branch matches one of `feature/*`, `fix/*`, `hotfix/*`, `release/*`, `spec/*`, `design/*`, `ci/*`, `chore/*`.
Fail: `main`, `develop`, or any non-conforming name — stop and ask the user to rename.

### Gate 5 — CHANGELOG.md has Unreleased entries
```bash
grep -A 10 "## \[Unreleased\]" CHANGELOG.md 2>/dev/null | grep -v "^##" | grep -v "^$"
```
Pass: at least one non-empty line under `## [Unreleased]`.
Fail: section missing or empty — create the section and add a one-line summary per task, using `git log develop..HEAD --oneline` to enumerate commits. `/feature`'s two-commit-per-task structure means only the GREEN (implementation) commit carries user-facing content — summarize those, skipping RED (test-only) commits, which have nothing to summarize.
N/A: a `/release` feature-log PR that changes only `.claude/context/feature-log.md`, and only if this gate fails on it. A feature-log entry is not a user-facing change. Report `[–] N/A (feature-log only)`.

### Gate 6 — Coverage (conditional: new Swift files on branch)
```bash
git diff develop...HEAD --name-only --diff-filter=A -- '*.swift'
```
If any new `.swift` files are listed, run the `ios-coverage` skill to capture coverage and verify ≥80% on new code.
Skip this gate if the branch contains no new files (fixes and refactors only).

### Gate 7 — Security (conditional: sensitive code paths)
```bash
git diff develop...HEAD --name-only -- '*.swift' | grep -E "<pattern matching your app's sensitive file names>"
```
Adjust the grep pattern to match files that handle external input, data persistence, or authentication in your app.
If any matches, run the `security-review` skill before opening the PR.
Skip this gate if no sensitive files were modified.

### Gate 8 — Abstraction bloat / duplication (heuristic, advisory)
```bash
# New protocols introduced on this branch
git diff develop...HEAD --name-only --diff-filter=A -- '*.swift' | xargs grep -Eln "^((public|internal|package|private|fileprivate|open|nonisolated|@[A-Za-z]+) )*protocol " 2>/dev/null

# Duplicated added lines (non-blank, appearing 2+ times across the diff) — copy-paste signal
git diff develop...HEAD -- '*.swift' | grep -E '^\+[^+]' | sed 's/^\+//' | grep -v '^\s*$' | sort | uniq -d
```
For each new protocol found, check its conformance count: `grep -rn ": <ProtocolName>" --include=*.swift .` A protocol with exactly one conforming type, outside the established `<RepositoryProtocol>`-style pattern (where a single implementation plus a test mock is expected), is a candidate for inlining.

For duplicated lines, flag any run of 3+ consecutive duplicated added lines as a candidate for extraction into a shared helper.

This gate is advisory: list candidates in the gate summary but do not block the PR on them. Final judgment on whether to extract or inline is a human or `/review` call.

### Gate 9 — RED-before-GREEN commit order (conditional: new files in a layer that expects a matching test)
```bash
python3 scripts/check_tdd_commit_order.py
```
For every new file in a layer with a 1:1 "<Type>.swift → <Type>Tests.swift" convention
(ViewModels, Services, Repositories — adjust `SCOPED_LAYER_DIRS` in the script to your
project's layer names) that has a matching test file, the script checks that the test file
was added in a strictly earlier commit than the implementation — never the same commit,
never a later one.

This exists because "write a failing test first" is unverifiable from `/feature`'s
instruction alone — nothing distinguishes an agent that watched the test fail from one that
wrote both together and never ran it red. Git history is the only outside evidence, and only
a RED-then-GREEN commit split preserves it. `/feature`'s per-task rules carry the discipline
itself (self-contained — don't gate it on an external skill invocation, since a plugin's
`enabledPlugins: true` flag doesn't guarantee its skills are actually invocable in a given
environment); this gate is the independent, git-history-based check that the discipline
actually happened, regardless of how it was instructed.

Pass: script exits 0 (no violations, or nothing in scope to check).
Fail: script lists each violation (file, commit, reason) — fix by re-doing the task as two
commits (test-only, confirm it fails, then implementation) per `/feature`'s per-task rules.
Unconfigured (exit 2): the script warns that `SCOPED_LAYER_DIRS` still holds the template's
default layer names and matches nothing anywhere in this repo — edit it to your project's
actual layer folders before trusting this gate. Do not treat exit 2 as a pass; it means the
gate hasn't actually checked anything yet, on any branch, ever. Report it as `[✗]`.
Rewriting already-pushed history is not required; this gate only evaluates the branch as it
stands when `/gates` runs.
Skip this gate if the branch adds no new files in the scoped layer directories (exit 0 with
nothing checked — different from exit 2, which means the directories themselves are wrong).

### Gate 10 — Architecture & layer-rule compliance (template — instantiate from your AGENTS.md/CLAUDE.md's enforced architectural rules)
This is the single authoritative check for layer-separation, type-safety, and
pattern rules. `/review` re-runs this gate's grep-only commands at the PR HEAD SHA and
compares the result to your gate summary, but does not repeat the build, test, or
coverage runs (a full local cycle is expensive; running it once here instead of again
in `/review` is the point of Gates 1, 2, and 6).
```bash
# Example: a layer that must not import a forbidden module (e.g. Domain Services must not import a persistence framework)
git diff develop...HEAD --name-only -- '*.swift' | grep '<path to the constrained layer, per AGENTS.md/CLAUDE.md>' | xargs grep -ln '^import <forbidden import>' 2>/dev/null

# Example: repository/protocol layer purity — protocols should import only the minimum (e.g. Foundation), never the persistence framework or UI framework directly
git diff develop...HEAD --name-only -- '*.swift' | grep '<path to your repository-protocol layer>' | xargs grep -n '^import <forbidden import>' 2>/dev/null

# Example: ViewModels must depend on protocols, never concrete persistence-layer implementations
# (exclude Tests/ — your test suite legitimately constructs concrete implementations against an
# in-memory store; a naive path match on the ViewModel-layer glob will also catch a mirrored
# <TestTarget>/<ViewModel layer>/ directory, which is not a production-code violation)
git diff develop...HEAD --name-only -- '*.swift' | grep '<path to your ViewModel layer>' | grep -v 'Tests/' | xargs grep -n '<pattern matching a concrete implementation type, e.g. SwiftData\w*Repository>' 2>/dev/null

# Example: Views must have no direct persistence-layer access
git diff develop...HEAD --name-only -- '*.swift' | grep '<path to your View layer>' | xargs grep -ln '^import <persistence framework>' 2>/dev/null

# Example: a type-safety rule (e.g. money values must be Decimal, never Double). Cover the forms a
# violation actually takes, not only `name: Double` — declarations (incl. arrays/dictionaries and
# optionals), return types on identifiers with the domain's name stems, inferred float literals, and
# conversions (`.doubleValue`, `Double(`):
git diff develop...HEAD --name-only -- '*.swift' | xargs grep -nHiE \
  -e '\b\w*(<name stems, e.g. stem1|stem2>)\w*\s*:\s*(\[\s*(\w+\s*:\s*)?)?<forbidden type>\b' \
  -e 'func\s+\w*(<name stems>)\w*\s*\(.*\)\s*(async\s+)?(throws\s+)?->\s*(\[\s*(\w+\s*:\s*)?)?<forbidden type>\b' \
  -e '\b\w*(<name stems>)\w*\s*=\s*-?[0-9]+\.[0-9]+\b' \
  -e '<pattern for a conversion into the forbidden type, e.g. its `.<x>Value` accessor>' 2>/dev/null
# This is a regex heuristic over identifier names, not an AST check: it misses a forbidden type behind a
# typealias, a generic, or a name with none of the stems, and can flag an unrelated identifier that
# contains a stem. A real check needs SwiftSyntax (a new dependency). Name each accepted hit (e.g. a
# dimensionless ratio) in the gate summary so `/review` can tell it from a new one.

# Generic (not project-specific): no force-unwrap-via-try!/as! in changed production code (Tests excluded)
git diff develop...HEAD --name-only -- '*.swift' | grep -v 'Tests/' | xargs grep -nE '\btry!|as!' 2>/dev/null

# Generic: unit/integration tests must use the test framework AGENTS.md/CLAUDE.md specifies, not an alternative
git diff develop...HEAD --name-only -- '<your test target>/*.swift' | xargs grep -l '<pattern matching the forbidden alternative framework, e.g. XCTestCase for a Testing-framework project>' 2>/dev/null

# Generic: UI test selectors must match a real accessibilityIdentifier in production views
grep -hro 'app\.\(buttons\|textFields\|staticTexts\)\["[^"]*"\]' <AppName>UITests/*.swift 2>/dev/null | sort -u
# — then cross-check each literal against: grep -r 'accessibilityIdentifier' <AppName>/Views/

# Example (if using a persistence framework with a model macro, e.g. SwiftData's @Model):
# new model types must be `final class` with an id property of your chosen identity type
git diff develop...HEAD --name-only --diff-filter=A -- '*.swift' | grep '<path to your Models layer>' | xargs grep -L 'final class' 2>/dev/null
git diff develop...HEAD --name-only --diff-filter=A -- '*.swift' | grep '<path to your Models layer>' | xargs grep -L '<pattern matching your id property, e.g. var id: UUID>' 2>/dev/null

# Example: relationships must specify an explicit delete rule
git diff develop...HEAD --name-only -- '*.swift' | grep '<path to your Models layer>' | xargs grep -n '<your relationship annotation, e.g. @Relationship>' 2>/dev/null | grep -v '<your delete-rule keyword, e.g. deleteRule>'

# Example: new Domain Services must have no stored mutable state — no `var` stored properties.
# Excludes computed properties (bodies opening with `{` or protocol `{ get }` requirements),
# which the naive pattern alone can't distinguish from genuinely stored `var`s.
git diff develop...HEAD --name-only --diff-filter=A -- '*.swift' | grep '<path to the constrained layer, per AGENTS.md/CLAUDE.md>' | xargs grep -nE '^\s*(private\s+)?var\s+\w+\s*[:=]' 2>/dev/null | grep -v '{\s*$' | grep -v '{ get'
```
Pass: every command returns no output (the UI-selector listing is cross-checked by hand/agent against your Views layer).
Fail: list every offending file and line, grouped by which rule it violates. This gate exists to catch AGENTS.md/CLAUDE.md's architectural rules *before* a PR is opened rather than only at `/review` (post-PR) — every consuming project should have at least the layer-separation and type-safety examples instantiated here. Leave placeholder examples as-is only if AGENTS.md/CLAUDE.md defines no enforced rule of that shape yet; the two fully-generic checks (force-unwrap, UI-selector-matching) apply to any Swift/XCTest project regardless.

### Gate 11 — Gate integrity (floor-guard)
```bash
python3 scripts/check_gate_integrity.py
```
On a `release/*` or `hotfix/*` branch (which PRs against `main`, not
`develop`), pass the correct base explicitly instead:
`python3 scripts/check_gate_integrity.py main` — the script defaults to
diffing against `develop` when no argument is given.

Detects gate-weakening — a gate-definition file edited on a `feature/*`
branch, a test deleted instead of fixed, a new suppression marker, an
unfinished stub, or a lowered threshold — rather than code-quality issues.
Catches the diff-detectable half of "Guard against self-modifying guardrail
files" below; it cannot block the edit from happening mid-session, only
catch it once `/gates` runs. Full rationale and the exact pattern list live
in `CONSTRAINTS.md`'s `gate-integrity` dimension — this section intentionally
doesn't restate them, to avoid a second copy drifting out of sync (this
script's own docstring is the third; treat `CONSTRAINTS.md` as canonical if
the two ever disagree). Numbered Gate 10 in the standalone
`deterministic-pr-gates` skill — same script, same behavior, one number
lower there because that file doesn't carry this pipeline's Gate 9
(TDD-commit-order).

Pass: script exits 0. Fail: script lists each violation with the specific
file/line/pattern matched — fix by addressing the underlying issue directly,
or, if the gate-definition change is legitimate maintenance, move it to its
own `chore/*` or `fix/*` branch instead of bundling it with feature work.
If `scripts/check_gate_integrity.py` does not exist, this gate FAILS (report
`[✗] Gate integrity — script missing`); never skip it as "not applicable".

## Gate summary

Report every gate before opening the PR. The first line is mandatory: the full SHA recorded in the
pre-step. `/review` compares it to the PR HEAD and rejects a summary that is missing or stale.
```
Gates run at <full 40-char SHA from `git rev-parse HEAD`>
Lane: <output of `python3 scripts/check_pr_lane.py --git origin/<base> --head-branch <branch> --base-branch <base>`, where <base> is the PR's base: `develop`, or `main` for `release/*` and a hotfix's first PR>
Gates:
[✓] Build
[✓] Tests — <N> tests executed
[✓] No TODO/FIXME/HACK
[✓] Branch naming
[✗] CHANGELOG — Unreleased section empty (auto-populating from git log...)
[–] Coverage — skipped (no new files)
[–] Security — skipped (no sensitive files)
[i] Abstraction bloat — no candidates found
[✓] RED-before-GREEN commit order
[✓] Architecture & layer-rule compliance
[✓] Gate integrity
```

When Gates 1 and 2 are skipped:
```
Gates run at <full 40-char SHA>
Lane: <lane>
Gates:
[–] Build — skipped (no build-relevant changes)
[–] Tests — skipped (no build-relevant changes)
[✓] No TODO/FIXME/HACK
[✓] Branch naming
[✓] CHANGELOG
[–] Coverage — skipped (no Swift files)
[–] Security — skipped (no Swift files)
[i] Abstraction bloat — 1 candidate found (see report)
[–] RED-before-GREEN commit order — skipped (no new files in scoped layers)
[✓] Architecture & layer-rule compliance
[✓] Gate integrity
```

Fix any failures before continuing.

## Autonomous gate-fixing loop
If any gate fails and needs iterative fixes, run this as a separate top-level command (not from within this agent):
```
/loop Fix failing gates and re-check. Stop when all blocking gates pass (Gates 1–11, 10 blocking; Gate 8 abstraction bloat is advisory, `[i]` only, never blocks): tree clean and SHA recorded, build succeeds, all tests pass with a non-zero executed count, no TODO/FIXME/HACK in changed files, branch name valid, CHANGELOG Unreleased section populated, coverage ≥80% on new files, security review clean, RED commit precedes GREEN commit for every new file in a scoped layer, architecture & layer-rule compliance clean, gate integrity clean.
```
Claude iterates on fixes and re-checks until all conditions hold. Keep the condition deterministic and verifiable — exit-code or grep-checkable facts only. "implement the feature correctly" is not verifiable and risks the loop satisfying the literal wording without a real fix.

To drive the full feature-to-PR cycle autonomously (no interval = Claude self-paces):
```
/loop run /feature on the next uncovered task from the plan. Then run /gates. Stop when all blocking gates pass.
```

## After all gates pass — open the PR

### Write candidate invariants (conditional)
If any gate caught a violation pattern that is NOT already listed in `.claude/context/invariants.md`, write it as a candidate comment:

```
<!-- [CANDIDATE] YYYY-MM-DD: <describe the violation pattern — e.g. "ViewModel imported SwiftDataRepository directly in feature/X"> -->
```

- **On a `feature/*` branch, do not write to `invariants.md`** — `.claude/hooks/guard_protected_paths.py` blocks the edit and Gate 11 flags it, and the write would also change the tree after the SHA was pinned. Put the comment line under a `## Candidate invariants` heading in the PR body instead; it gets appended to the file from a `chore/*` branch.
- On any other branch, append it at the bottom of that file, commit it, and restart from the pre-step — the commit moves HEAD, so the gate summary must be re-run against the new SHA.

Do not promote it to a numbered invariant — that is a human decision made during the next `/pipeline-review`.

Include the actual Gate summary output (from above, starting with its `Gates run at <sha>` line) in the
PR body under its own section — `/review` checks that SHA against the PR HEAD and re-runs the
deterministic gates itself, comparing its results to this block.

If the `Lane:` line says `pipeline` (or the PR touches pipeline paths alongside app code), also add a
`Motivating incident: <what went wrong, with a link or date>` line to the PR body, or
`Motivating incident: none (<reason>)`. The `review-evidence` check fails a pipeline-lane PR
without a non-empty one.

```bash
gh pr create \
  --title "<type>(<scope>): <description>" \
  --base develop \
  --body "$(cat <<'EOF'
## Summary
- <bullet per task from the plan>

## Gates
<paste the actual Gate summary block from this run — the `Gates run at <sha>` line, plus each gate's ✓/✗/– status>

## Test plan
- [ ] Full test suite passes (TEST SUCCEEDED)
- [ ] Tested on simulator (see AGENTS.md/CLAUDE.md)

<append your coding agent's own PR-attribution footer here, if it uses one — e.g. Claude Code appends "🤖 Generated with [Claude Code](https://claude.com/claude-code)">
EOF
)"
```

If `/gates` is re-run after the PR is open (a fix cycle changes HEAD), update the PR body's gate section with the new summary — `gh pr edit <PR> --body-file <file>` — so its `Gates run at <sha>` matches the new HEAD; `/review` rejects a stale one.

**Always pass `--base develop`** — `gh pr create` defaults to `main` (repo default), which bypasses gitflow.
Exceptions: `release/*` and `hotfix/*` branches use `--base main`, except a hotfix's second PR back to `develop`, which uses `--base develop` (see `/bugfix`).

## Guard against self-modifying guardrail files

Gates 0–11 are agent-instruction checks, so an agent under pressure to make a stuck gate pass could edit a gate definition instead of fixing the violation, then report a clean summary. This is most likely in an unattended `/loop` run with no human turn in between. Two layers close that:

- **Live block:** `.claude/hooks/guard_protected_paths.py`, a native `PreToolUse` hook installed by `setup.sh` and `/pragma:init` (`--no-guard-hook` opts out). On a `feature/*` branch it blocks `Write`, `Edit` and `MultiEdit`, and, best effort, `Bash` writes, to skills (`.claude/skills/*/SKILL.md`), `AGENTS.md`, `CLAUDE.md`, `CONSTRAINTS.md`, `.claude/context/invariants.md`, `.claude/settings.json`, `.claude/hooks/*` and `scripts/check_*`, at the repo root or under any subdirectory (a Claude project inside a monorepo). The fix is to make that change on a `chore/*` or `fix/*` branch.
- **CI backstop:** Gate 11's check 1 (`scripts/check_gate_integrity.py`) flags the same set of files on a `feature/*` PR, through `GUARDED_PATH_GLOBS`. The `gates` job (`.github/workflows/gates.yml`) runs on every PR, so a PR that only touches them still runs it. A step in that job runs the hook's self-test, which fails if the hook's glob list and the script's differ (it runs the PR's own copy, so it catches an honest slip, not a deliberate one). This catches a plain commit and push that never went through Claude Code.

What is not covered: the hook's Bash detection is a best-effort parse, so `python -c`, interpreter heredocs, variable or glob expansion (including `cd $VAR`), `find -exec` or `-delete`, `xargs rm` fed from stdin, `git checkout <ref> -- file`, `git restore` and `rm -rf <dir that only contains a nested project>` are not detected. A symlink that already exists is followed; one created and written through in the same command is not. The hook only runs in sessions that load the project's own `.claude/settings.json`: verified 2026-09-23 that a session started from a parent directory did not fire it, so start Claude Code from the project root. The CI backstop applies either way. The hook fails open on bad input, no git repo or a detached HEAD, and it allows every edit off `feature/*`. Neither layer catches an agent that renames its branch away from `feature/*`. `.claude/settings.local.json` is not on the list. Pattern sourced from `karanb192/claude-code-hooks`'s "config-guard" hook, surfaced in the 2026-09-08 Agentic AI Intelligence Report.

## Done when
All 11 gates (Gates 1–11; Gate 0 only decides whether Gates 1–2 run) report: the 10 blocking gates pass and Gate 8, advisory, is listed, PR is open, and the PR URL is returned to the user.

## Tip — chain into code-review + review
Once the PR is open, run `/pr-followup <PR>` to run `code-review:code-review`
and then `/review`, and record both in the PR body for the `review-evidence`
check. `/test` runs before `/gates`, not after the PR opens.

## Standalone version
The gate logic above also exists as an installable skill independent of this
pipeline: [`skills/deterministic-pr-gates/SKILL.md`](../../skills/deterministic-pr-gates/SKILL.md).
If you're adopting this command as part of the full pipeline, this file remains
the source of truth for your project; the skill is for using the gate pattern
without the rest of the pipeline.
