---
name: sk-review-and-fix
description: Closed-loop code review through review, triage, fix, and re-review until the latest pass is clean. Use when the user asks for sk-review-and-fix, /sk-review-and-fix, or review and fix.
---

# Review and Fix

Closed-loop diff review: **review → triage → fix → re-review** until the latest pass has zero valid findings.

## When to use

- User asks for `sk-review-and-fix`, `/sk-review-and-fix`, or fixing review findings.
- After implementation, when review and fixes should happen in one pass.

## Active PR handoff

When the root runbook is multi-PR, fetch refs before this phase and verify the checked-out branch and HEAD against the active PR row. Use the harness-supported sync workflow and record the resulting HEAD in the active PR runbook. If the branch or HEAD cannot be reconciled safely, mark the PR blocked and stop instead of reviewing or changing the wrong diff.

## Flow context

1. If the user provided a slug, use `.agents/flows/sk-<slug>/`.
2. Else inspect root runbooks. For a multi-PR runbook, use its exact `Active PR` and matching `Directory`; for a single-PR runbook, use the root. Require `3 - IMPLEMENTATION.md` and missing `4 - REVIEW.md` there.
3. If no flow exists and no slug is given, continue without a flow folder; `4 - REVIEW.md` is the only artifact.
4. If `4 - REVIEW.md` already exists, read its recorded `false_positive` findings and seed the first review with them.

## Input

- **Repository:** absolute path to repo root
- **Diff target:** `branch changes` (default), `uncommitted changes`, or explicit branch/PR
- **Base branch:** only when non-default
- **Custom focus / out of scope:** only when the user gave constraints
- **Active plan:** exact `2 - PLANNING.md` in the active flow or PR directory; never choose by glob or modification time
- **Known validation gaps:** list missing plan/spec/Figma/tests/browser; do not claim those areas verified
- **False positives from previous reviews:** carried from earlier passes in this run, plus any recorded in an existing `4 - REVIEW.md`. One per line as `file:line | tag | original finding | why it was dismissed`. File plus finding text is the identity: the line alone is not, since numbers drift and one line can yield several findings under the same tag.

## Output contract

The subagent is read-only and returns ONLY the findings block below.

```text
You are a read-only diff reviewer. Produce ONLY the findings block below; do not implement fixes.

Repository: <absolute path>
Diff: <branch changes | uncommitted changes>
Base branch: <only when non-default>
Custom focus: <only when user gave constraints>
Out of scope: <only when user excluded areas>
Known validation gaps: <only when context/capability missing — list each; do not claim those areas verified>
False positives from previous reviews: <only when earlier passes produced some; one per line as `file:line | tag | original finding | why it was dismissed`. A record matches only in the same file, on the same finding, while the recorded reason still holds — allow the line to have drifted, and never carry a record across files.>

Run the diff yourself (e.g. git diff <base>...<head> or git diff for uncommitted). Read changed files as needed.

Output ONLY in this format (no prose intro, no sections swapped).

### Review Findings

section:line: <emoji> <tag>: <problem/over-engineering>. <fix/replacement>.
totals: N🔴 N🟡 N✂️ N🪵 N⚡ N🔵 N❓ | net: -<N> lines possible

Or exactly when no findings:

### Review Findings

Lean & valid. Ship.

Rules for Review Findings:
- Sort findings file → line ascending
- One finding per line; problem then fix separated by ". "
- Location format: L<line>: for single line, L<start>-<end>: for span, or <file>:L<line>: when multiple files
- Action tags (literal after colon):
  - 🔴 bug: correctness bug, security risk, broken logic, regression
  - 🟡 gap: missing/error-prone test, error handling gap, maintainability defect
  - ✂️ cut: dead code, unused feature/dependency, speculative code (replacement: nothing)
  - 🪵 yagni: single-caller layer, unset config, premature abstraction (replacement: inline or drop)
  - ⚡ simplify: hand-rolled stdlib behavior, native platform duplicate, complex pattern (replacement: name function/type/feature or shorter form)
  - 🔵 nit: naming, minor style, formatting
  - ❓ question: unclear logic, missing spec/context (cite gap if missing)
- Do not report style-only nits outside project norms unless indicating real bugs.
- Do not flag a single smoke test, one assert-based self-check, or the smallest runnable check guarding changed logic.
- Do not re-report a finding listed under "False positives from previous reviews" when it recurs in the same file and the recorded reason still holds. Do report it if the reason no longer applies, or if the same problem appears in another file — note the changed premise.

Examples (tone only):
- L12-38: ⚡ simplify: 27-line email validator class. Use standard shape check or rely on confirmation mail.
- repo.py:L88: 🪵 yagni: AbstractRepository with one implementation. Inline until a second backend exists.
- L52-71: ✂️ cut: retry wrapper around an idempotent local call. Remove wrapper.

End with exactly one line:
- totals: N🔴 N🟡 N✂️ N🪵 N⚡ N🔵 N❓ | net: -<N> lines possible
- Or: Lean & valid. Ship.
```

## Tags

- `🔴 bug`: correctness bug, security risk, broken logic, regression
- `🟡 gap`: missing/error-prone test, error handling gap, maintainability defect
- `✂️ cut`: dead code, unused feature/dependency, speculative code
- `🪵 yagni`: single-caller layer, unset config, premature abstraction
- `⚡ simplify`: hand-rolled stdlib behavior, native platform duplicate, complex pattern
- `🔵 nit`: naming, minor style, formatting
- `❓ question`: unclear logic, missing spec/context

## Review criteria

- Correctness, security, and broken logic
- Tests and error handling
- Maintainability and dead code
- Unnecessary abstraction vs native/standard alternatives
- Naming and style
- Missing context (cite the gap)

## Loop

If the diff is empty, stop in one sentence.

1. **Review** — dispatch a new `readonly` `generalPurpose` Task subagent with the prompt above.
2. **Triage** — label each finding `valid`, `false_positive`, or `unvalidated` with a one-line reason. Count `valid` only. `unvalidated` items are recorded as validation gaps.
3. **Fix** — resolve every `valid` finding before the next review. Use a builder subagent for ≤2 surgical files; parent edits for 3+ files or cross-cutting changes.
4. **Repeat** — dispatch a new subagent on the current tree. Carry forward every `false_positive` in the record shape above into `False positives from previous reviews` in the next review prompt. Continue until the latest pass has zero `valid` findings after triage.

**Exit rule:** hand off when the latest pass is `Lean & valid. Ship.` or has zero `valid` findings after triage (all `false_positive` or all `unvalidated`).

**Stuck guard:** if the same `valid` finding persists after 3 fix passes, stop and report the blocker.

## Fix rules

- Minimal diff; match conventions; no scope creep.
- Do not silence linters — fix the root cause.
- Run relevant tests after non-trivial fixes; record failures as blockers.
- Do not guess UI layout, copy, or business rules without spec/Figma — record a gap.

## Output destination

When the exit rule is met (or blocked), write `4 - REVIEW.md` and update `RUNBOOK.md` row `4` with:

- Review rounds completed
- `valid` findings fixed (count and one-line summary)
- `false_positive` count
- `false_positive` findings from each round in the record shape above, under a `## False positives` heading, so future `sk-review-and-fix` runs can seed from them
- Any `unvalidated` items / validation gaps
- Test and browser/visual status, if available

## Rules

- Subagent-only reviews every iteration.
- Single-block action-tagged output every pass.
- Re-review after every fix batch.
- No drive-by refactors; do not treat 🔵 as auto-`false_positive`.
- Do not claim validation when plan, spec, Figma, tests, or browser are unavailable.
- Do not auto-fix gap-dependent ❓ by guessing intent.
