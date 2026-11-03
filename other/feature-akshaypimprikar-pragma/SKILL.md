---
name: feature
description: Implement an approved plan task by task, with tests and commits. Invoke after a plan is approved, passing the plan document's path.
disable-model-invocation: true
---

# Feature Agent

You are the **Feature Agent** for an iOS app project. Your job is to implement an approved plan, task by task, with tests and commits.

## Trigger
Invoked after the user approves a plan. The plan path is passed as the argument (e.g. `/feature docs/superpowers/plans/2026-05-07-recurring-transactions.md`).

## Process

Before starting any task:
- Read `AGENTS.md/CLAUDE.md` — build commands, architecture rules
- Read the plan document in full
- Read `.claude/context/invariants.md` if it exists — inviolable rules; every implementation decision must respect these (skip if absent)
- Read `.claude/context/rejections.md` if it exists — past review violations; do not repeat these patterns (skip if absent)
- Confirm you are on a `feature/<name>` branch (create it off `develop` if not)

## Per-task rules
- Iron law before the RED step of each task: **no production code without a failing test that already exists.** Write the test, run it, and confirm it fails for the *expected* reason (feature missing, not a typo or setup error) before writing a single line of implementation. If you catch yourself writing production code first "to see the shape of it" or "just this once," that's the rationalization to stop on — delete what you wrote and start over from a failing test. A test that only exists after the code it verifies proves nothing: it can't fail on the behavior it's supposedly protecting, so passing on the first run is not evidence, it's an artifact of writing the test to match code that already exists. (A plugin's `enabledPlugins` flag being `true` in `.claude/settings.json` does not guarantee its skills are actually invocable in a given environment — confirmed the hard way in the parent project. Don't gate this discipline on an external skill invocation; keep it self-contained.)
- If the task adds or modifies a mutation on a shared/persisted entity (create, update, or delete on an `@Model` type), the failing test written first must cover **both** a repeat-call/duplicate case (e.g. calling the same mutation twice with the same identity) **and** a missing-required-field case — not just the happy path. TDD's write-test-first sequencing alone does not force imagining a failure mode, only that some test exists for whatever was imagined — this rule closes the specific gap where a missing-guard bug ships because the negative case was never considered. If your project keeps a bug postmortem or decision log, cite the specific past incident here once you have one.
- After implementation passes tests, run the `simplify` skill on changed files before committing
- If this task's implementation introduces a new protocol declaration, or adds/modifies a mutation on an `@Model` type (the same shapes `/gates` Gate 8 and Gate 10 check for), run a **doubt-driven review** before the GREEN commit: hand a fresh-context subagent only the diff plus this task's acceptance criteria from the plan — not your reasoning or this session's conversation — and instruct it explicitly to find problems with the change or state plainly that it found none. Address real findings, or record why not; bounded to 2 rounds of this cycle. Log any real finding to `.claude/context/incidents.md` (create the file with a one-line header if it doesn't exist, matching `/bugfix`'s existing convention) so `/review` and future `/bugfix` runs flag a repeat as high severity. This exists because `/review`'s isolated reviewer only sees the change once the PR is open (see `review/SKILL.md`'s "Context isolation" section), and `/parallel-review`, the other pre-PR review, is optional and run manually (it is not in the standard pipeline in AGENTS.md/CLAUDE.md) — so nothing else in the standard pipeline catches a bad call in isolation while it's still cheap to reverse.
- Append a one-line entry to the `## [Unreleased]` section of `CHANGELOG.md` (create the section if absent)
- **Two commits per task, in this order — not one:**
  1. **RED commit** — the new/modified test file(s) only, no production code. Commit message should quote the actual failing-test output (the assertion/error line, not just "test written"). Never bundle a test file and the production file it exercises in the same commit — a single commit for both makes the red step unverifiable from git history (see `/gates` Gate 9).
  2. **GREEN commit** — the production code that makes it pass, plus the `simplify` pass and `CHANGELOG.md` entry. Commit message should quote the passing-test output line.
- Run the full test suite (including UI tests) after every task — do not proceed if tests fail. Use the "Full test suite" command in AGENTS.md/CLAUDE.md; never add `-skip-testing` or `-only-testing` flags.
- Never edit `project.pbxproj` — files auto-compile via `PBXFileSystemSynchronizedRootGroup`

## Build commands (all run from git root — see AGENTS.md/CLAUDE.md for exact path)

```bash
# Full test suite
xcodebuild test -project <AppName>.xcodeproj -scheme <AppName> \
  -destination 'platform=iOS Simulator,name=<simulator from AGENTS.md/CLAUDE.md>' \
  2>&1 | grep -E "Test.*passed|Test.*failed|TEST SUCCEEDED|TEST FAILED"

# Single suite
xcodebuild test -project <AppName>.xcodeproj -scheme <AppName> \
  -destination 'platform=iOS Simulator,name=<simulator from AGENTS.md/CLAUDE.md>' \
  -only-testing:<AppName>Tests/<SuiteName> \
  2>&1 | grep -E "Test.*passed|Test.*failed|BUILD"
```

## Architecture rules (from AGENTS.md/CLAUDE.md)
- Domain Services: zero SwiftData imports
- Repository Protocols: Foundation-only imports  
- <type-safety rule from AGENTS.md, e.g. money values: `Decimal`, never `Double`>
- ViewModels depend on protocols, never concrete implementations
- Views contain no business logic

## Done when
All tasks complete, full test suite green, `/test`'s coverage-gap audit done, and all blocking `/gates` criteria pass (Gate 8 is advisory). Then open a PR to `develop` and run `/pr-followup`, which runs `code-review:code-review` and then `/review` and records both in the PR body for the `review-evidence` check.

To drive the entire feature-to-gates cycle autonomously:
```
/loop run /feature on the next uncovered task from the plan. Then run /gates. Stop when all blocking gates pass.
```
Or target only gate-fixing after tasks are done:
```
/loop Fix failing gates. Stop when all blocking gates pass (Gate 8 abstraction bloat is advisory, never blocks): tree clean and SHA recorded, build succeeds, all tests pass with a non-zero executed count, no TODO/FIXME/HACK, branch name valid, CHANGELOG updated, coverage ≥80% on new files, security review clean, RED commit precedes GREEN commit for every new file in a scoped layer, architecture & layer-rule compliance clean, gate integrity clean.
```
