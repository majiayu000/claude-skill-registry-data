---
name: deterministic-pr-gates
description: Run deterministic, scriptable pre-PR verification gates (build, full test suite, coverage threshold, branch naming, changelog presence, force-unwrap/duplication heuristics, and project-specific architecture/layer rules via grep) before a PR is opened or before a human reviewer looks at the diff. Use when a user asks whether a branch is ready for PR, wants a pre-PR checklist automated, wants CI-equivalent checks run locally and fast, or wants pre-merge verification that doesn't depend on an LLM's subjective judgment of code quality. Works standalone in any project — no other skill or pipeline required.
---

# Deterministic Pre-PR Gates

## Why deterministic, not LLM-judged

Most "quality gate" agent skills work by asking an LLM to read a diff and judge it: is this good code, does it follow our conventions, is anything missing. That's a real capability, but it's non-deterministic — the same diff can pass on one run and get flagged on the next, and a confident-sounding judgment is not the same as a verified fact.

This skill does the opposite. Nearly every gate is a real command with a checkable outcome: an exit code, a grep match, a coverage percentage against a threshold. The two exceptions are Gate 7 (a security review, run by a dedicated skill or by hand when sensitive paths change) and Gate 8 (advisory: it surfaces abstraction and duplication candidates and a human decides). Everywhere else, if a gate passes, it passed because a build succeeded, a test suite went green, or a pattern genuinely didn't match — not because an LLM said it looked fine.

Use an LLM-judgment skill *in addition* to this one for things that are genuinely subjective (does this variable name communicate intent, is this abstraction premature). Use this skill for everything that has a yes/no answer, so the two never overlap and neither goes soft on the other's job.

## Trigger

Run before a PR is opened or before a human reviewer looks at the diff: when the user asks whether a branch is ready for a PR, wants a pre-PR checklist automated, or wants CI-equivalent checks run locally.

## Process

Run Gate 0 through Gate 10 below in order, then report the Gate summary. Not every gate applies to every project or every diff. Each gate below states its own condition — most are conditional on specific files having changed. Skip a gate outright if its condition isn't met; report it as skipped, not as passed.

## Gate 0 — Change scope check (runs first)

```bash
git diff <base-branch>...HEAD --name-only -- '<source file extension(s), e.g. *.swift or *.py *.ts>'
```

If this returns no output, no source code changed on this branch — skip the Build and Test gates below and continue from Gate 2. If source files are listed, run Build and Test as normal. This is what lets a docs-only or config-only PR skip an expensive build/test cycle without skipping it silently.

## Gate 1 — Build (conditional: source files changed)

```bash
<your project's actual build command>
```

Swift/Xcode example:
```bash
LOG=$(mktemp -t build)
xcodebuild build -project <AppName>.xcodeproj -scheme <AppName> \
  -configuration Debug -destination 'platform=<simulator platform>,name=<simulator>' \
  > "$LOG" 2>&1; RC=$?
xcsift < "$LOG"
[ -s "$LOG" ] && [ "$RC" -eq 0 ] && grep -q "BUILD SUCCEEDED" "$LOG" && echo "GATE 1 PASS" || echo "GATE 1 FAIL (xcodebuild exit $RC)"
```
Capture the log file instead of piping to `xcsift`: a pipeline hides `xcodebuild`'s exit status, so an empty or crashed run would print a clean-looking summary.

Node/TypeScript example:
```bash
npm run build
```

Python example: skip this gate entirely for interpreted projects with no build step, or substitute a type-check (`mypy`, `pyright`) if the project uses one.

Pass: build succeeds with no errors. Fail: stop immediately — running the test suite against a broken build wastes the run and produces misleading results.

## Gate 2 — Full test suite (conditional: source files changed)

```bash
<your project's actual test command>
```

Pass: the test runner reports all tests passed, zero failures. This gate is the one true "does the behavior still work" check — nothing else here substitutes for it.

## Gate 3 — No TODO/FIXME/HACK in changed files

```bash
git diff <base-branch>...HEAD --name-only -- '<source extensions>' | xargs grep -ln "TODO\|FIXME\|HACK" 2>/dev/null
```

Pass: no output. Fail: list every offending file and line — either resolve it or track it as a real issue instead of leaving it inline.

## Gate 4 — Branch naming convention

```bash
git branch --show-current
```

Pass: branch matches your project's naming convention (e.g. `feature/*`, `fix/*`, `hotfix/*`, `release/*`, `chore/*`). Fail: `main`, `master`, `develop`, or any non-conforming name — stop and ask before opening a PR from a branch that shouldn't have one.

## Gate 5 — Changelog has an unreleased entry

```bash
grep -A 10 "## \[Unreleased\]" CHANGELOG.md 2>/dev/null | grep -v "^##" | grep -v "^$"
```

Pass: at least one non-empty line under the project's "Unreleased" section. Fail: section missing or empty — add a one-line summary per commit on this branch (`git log <base-branch>..HEAD --oneline`) before opening the PR. Skip this gate entirely if the project doesn't maintain a changelog.

## Gate 6 — Coverage (conditional: new source files on this branch)

```bash
git diff <base-branch>...HEAD --name-only --diff-filter=A -- '<source extensions>'
```

If any new files are listed, capture coverage for this branch with your project's coverage tool and verify new code meets your project's threshold (a common baseline is ≥80%). Skip this gate if the branch contains no new files — fixes and refactors to existing, already-covered code don't need a fresh coverage capture.

## Gate 7 — Security (conditional: sensitive code paths touched)

```bash
git diff <base-branch>...HEAD --name-only -- '<source extensions>' | grep -E "<pattern matching files that handle external input, persistence, auth, or secrets>"
```

If any matches, run a security-focused review before opening the PR (a dedicated security-review skill, or a manual pass). Skip this gate if no sensitive files were modified.

## Gate 8 — Abstraction bloat / duplication (heuristic, advisory only)

```bash
# New protocols/interfaces introduced on this branch
git diff <base-branch>...HEAD --name-only --diff-filter=A -- '<source extensions>' | xargs grep -ln "<your language's interface/protocol declaration keyword>" 2>/dev/null

# Duplicated added lines (non-blank, appearing 2+ times across the diff) — copy-paste signal
git diff <base-branch>...HEAD -- '<source extensions>' | grep -E '^\+[^+]' | sed 's/^\+//' | grep -v '^\s*$' | sort | uniq -d
```

For each new interface found, check its implementation count. An interface with exactly one implementing type, outside an established one-implementation-plus-test-mock pattern, is a candidate for inlining rather than abstracting. For duplicated lines, flag any run of 3+ consecutive duplicates as a candidate for extraction into a shared helper.

This gate is advisory: report candidates, do not block the PR on them. Whether to actually extract or inline is a human judgment call — this gate exists to surface the question, not answer it.

## Gate 9 — Architecture & layer-rule compliance (instantiate from your own project's rules)

This is the gate that actually encodes what "correct" means for your project — everything above is generic; this one isn't. Read your project's own documented architecture rules (a `CLAUDE.md`, an `AGENTS.md`, a README's architecture section, whatever your project uses) and turn every enforced rule with a checkable shape into a grep here. Two examples that generalize to almost any codebase, worth including even before you've written the project-specific ones:

```bash
# Generic: no bare force-unwrap / unchecked-cast in changed production code (tests excluded)
git diff <base-branch>...HEAD --name-only -- '<source extensions>' | grep -v 'Tests\?/' | xargs grep -nE '<your language's force-unwrap or unsafe-cast syntax>' 2>/dev/null

# Generic: a concrete-implementation-in-place-of-abstraction check, scoped to your project's dependency-inversion boundary (exclude test directories — legitimate test fixtures construct concrete implementations directly)
git diff <base-branch>...HEAD --name-only -- '<source extensions>' | grep '<path to the layer that must depend on an abstraction, not a concretion>' | grep -v 'Tests\?/' | xargs grep -n '<pattern matching the concrete type it must not depend on>' 2>/dev/null
```

Add one grep per enforced rule your project actually has (forbidden imports between layers, a type-safety rule like "money values must use a decimal type, never floating point", a naming convention, a required annotation). A project with zero documented architecture rules can skip this gate — but if you find yourself explaining a convention in code review more than once, that's the signal it belongs here instead.

Pass: every command returns no output. Fail: list every offending file and line, grouped by which rule it violates.

## Gate 10 — Gate integrity (floor-guard)

```bash
python3 scripts/check_gate_integrity.py <base-branch>
```

Detects gate-weakening rather than code-quality issues — the gate that checks the checks themselves, on the diff-detectable half of that problem (it cannot block an edit from happening mid-session, only catch it once this gate runs; a native `PreToolUse` hook would be needed for the rest, a separate architecture piece). Full rationale and the exact pattern list live in `CONSTRAINTS.md`'s `gate-integrity` dimension if you're also adopting that file — this section intentionally doesn't restate them to avoid a second copy drifting out of sync. If you're using this skill standalone (no `CONSTRAINTS.md`), the script's own docstring is the canonical description.

Pass: script exits 0. Fail: fix the underlying issue directly, or — if the gate-definition change is legitimate maintenance — move it to its own `chore/*`/`fix/*` branch instead of bundling it with feature work.

## Gate summary

Report every gate before signaling the branch is ready:

```
Gates:
[✓] Build
[✓] Tests
[✓] No TODO/FIXME/HACK
[✓] Branch naming
[✗] Changelog — Unreleased section empty
[–] Coverage — skipped (no new files)
[–] Security — skipped (no sensitive files)
[i] Abstraction bloat — no candidates found
[✓] Architecture & layer-rule compliance
[✓] Gate integrity
```

Use `[✓]` pass, `[✗]` fail, `[–]` skipped with the reason, `[i]` informational/advisory. Fix every `[✗]` before opening the PR — this skill's entire value is that "ready for PR" means something verifiable, not a vibe.

## Done when

Every gate is reported as `[✓]`, `[✗]`, `[–]` with its reason, or `[i]`, each from a command that actually ran, and no `[✗]` remains before the PR is opened.

## Instantiating this for a new project

1. Copy this file into your project's skills directory (or keep it here and reference it).
2. Replace every `<placeholder>` with your project's real values: build/test commands, source extensions, branch-naming convention, layer paths.
3. Write Gate 9's project-specific greps from your own documented architecture rules. This is the only gate that requires real thought — everything else is copy-and-fill.
4. Copy `scripts/check_gate_integrity.py` alongside your project's other scripts — Gate 10 is the one gate here backed by a real script file rather than an inline command, since gate-weakening detection needs actual diff parsing, not a single grep.
5. Run it once against a deliberately-broken diff (an unhandled force-unwrap, a missing test) to confirm each gate actually catches what it claims to.

## Relationship to a full agentic pipeline

This skill runs standalone — it has no dependency on any other command, context file, or pipeline stage. If you're also running a fuller pipeline (spec → plan → feature → review → release), this is the gate that sits between "feature is written" and "PR is open," and a fuller pipeline's own gate step can simply invoke this skill rather than re-implementing it.
