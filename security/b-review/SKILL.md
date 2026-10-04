---
name: b-review
description: >
  Pre-PR changed-code review for architect-style reads of a diff, commit
  range, or checkpoint after implementation. Do NOT invoke for PR-prose
  review, b-agentic repository or design-conformance audits, UI/design
  review, plan review, or research synthesis review. Routing signals: code
  review, review diff, review my diff, review changes, review these
  changes, working tree diff, pre-PR, "what would an architect".
  Delegated: runs only in the `b-reviewer` subagent; the main session
  never executes it itself.
metadata:
  phase: Validate
  execution_mode: subagent
  agent: b-reviewer
---

<!-- Generated from skills/registry.yaml and skills/b-review/prompt.md. Edit those sources, not this file. -->

# b-review

Independently review a frozen changed-code candidate for blockers, regressions, security risk, and missing evidence. Findings first. This skill runs in the `b-reviewer` subagent.

## Delegation boundary

`b-review` runs only in the `b-reviewer` subagent.

- Main session: reading this file prepares the handoff; it never authorizes running the steps below yourself. Gather the parent-owned evidence and confirm the effective `b-reviewer.md` (project `.pi/agents/` over the Pi agent directory's `agents/`) is readable and its parsed frontmatter `tools` value, normalized to a list (comma-separated scalar or YAML sequence), is explicit, non-empty, and contains neither `edit` nor `write` (a missing, blank, or null `tools` grants them), then call `subagent` with agent `b-reviewer` and a bounded task naming `b-review`. Do not do this skill's work with your own tools, even for a quick, small, or single-lookup request. If the subagent is unavailable or fails, or its result notes an unknown agent type or `general-purpose` fallback (discard that result), report the gap and ask the user; never fall back to self-execution. Evaluate the returned result before any user-facing or worktree action.
- `b-reviewer` child: execute the steps below read-only, return this skill's Output format to the main session, and do not delegate again.

## When to use

- The user requests changed-code review.
- The main session froze a candidate that needs its independent gate.

## When NOT to use

- PR title/description prose review or rewriting without changed-code review -> **b-pr-summary**.
- A b-agentic repository/design-conformance audit -> **b-agentic-audit**.
- Root-cause diagnosis -> **b-debug**.
- Writing or fixing tests -> **b-test**.

## Tool guidance

- Use the main session's frozen snapshot, metadata-only path list, targeted safe diff evidence, and native `read`. Read-only shell commands such as `git diff`, `git status`, and `rg` are available for independently inspecting the candidate; do not run mutating commands. If the handoff lacks necessary candidate evidence that inspection cannot supply, report that gap. In an indexed project, use `codegraph_explore` (read-only) on changed symbols to find callers or tests the candidate did not update; bounded specialized Brave tools may substantiate public semantics.

## Steps

1. Confirm the baseline and exact frozen candidate snapshot. Require the main session's identity: HEAD, SHA-256 digests of staged and unstaged binary diffs, and sorted relevant untracked paths, types, and content digests. Independently recompute at the start and end of review and report a mismatch. Prefer `b_candidate_snapshot` when available: compare only its `fingerprint`, and treat `complete: false` or a mismatch as blocking. The tool omits git-ignored files unless they are named in `include_ignored`: require the handoff's list of relevant ignored/derived paths, pass the same list at every checkpoint, and block the fingerprint handoff, reporting the uncovered paths, when a relevant ignored artifact cannot be named. Use one method at every checkpoint; never compare a tool fingerprint with a hand-computed identity, and report a gap if the handoff used the tool but it is unavailable to you. Otherwise use the manual procedure only after this fail-closed preflight, run from the repository root before any `git status` or `git diff` (which can execute programs); if any check fails or cannot be run, block the review (no verdict) and report why. Exit 0 means matches found and 1 means none; any other exit is a failure. (a) `git config --get-regexp '^(extensions\.partialclone|remote\..*\.promisor)$'` exits 1 (a partial clone could fetch objects during diff); (b) `git config --get-regexp '^filter\..*\.(clean|process)$'` exits 1: any configured clean/process program blocks the manual fallback, whichever paths use it; (c) `git ls-files -s -z` lists no mode `160000` entry (a submodule's own filters cannot be checked). Never accept executable-filter side effects for the main session. Run every git command, including these, as `GIT_NO_LAZY_FETCH=1 GIT_OPTIONAL_LOCKS=0 git -c core.fsmonitor=false ...`. Then hash raw stdout from `git diff --no-ext-diff --no-textconv --no-color --no-renames --ignore-submodules=none --submodule=short --binary --cached -- .` and `git diff --no-ext-diff --no-textconv --no-color --no-renames --ignore-submodules=none --submodule=short --binary -- .` (not rendered or truncated diff output); list untracked paths with `git ls-files --others --exclude-standard -z`, sort paths as bytes, and hash each file's bytes or a symlink's target bytes with its path and type. Include explicitly relevant ignored/derived paths. If protected content cannot be inspected or hashed with permission, block rather than claim an unchanged candidate. It must cover tracked plus relevant untracked/derived content; do not claim requirements coverage without a baseline.
2. Inspect the supplied metadata-only path list and targeted non-protected diff evidence. Read repository context only when it materially affects a finding. Review does not authorize staging or committing; `b-commit` separately inspects the exact staged paths and commit plan without repeating validation.
3. Independently assess the actual diff, acceptance, required check outcomes and freshness, edge cases, security, operability, and residual risk. Compare the candidate identity again before returning. Check that the solution choice is proportionate to the plan's quality criteria and project conventions; do not turn every review into an architecture report. A skipped or failed required check, changed snapshot, or material gap cannot be ready.
4. Bounded read-only research may substantiate a specific finding only. Keep the repository review read-only: do not edit, patch, run generators/fixers, or otherwise mutate the worktree. Return the structured disposition and findings to the main session; do not ask users questions, message peers, or implement a correction.
5. Report blocking findings with location, evidence, impact, violated baseline, minimal correction, and regression check. For `NEEDS FIXES`, name the next skill (`b-frontend`, `b-implement`, `b-test`, or `b-refactor`) where applicable. Corrections must return as a reverified, frozen candidate for another review.

## Output format

Findings, checked-and-clean areas, snapshot/verification coverage, and residual risk first. The response must end with exactly one standalone final line, with no text after it:
- `Verdict: READY FOR PR`
- `Verdict: READY WITH FOLLOW-UPS`
- `Verdict: NEEDS FIXES`

`READY WITH FOLLOW-UPS` requires explicit disposition and never waives required safety evidence. A verdict is not task acceptance, commit creation, or shipping.

## Rules

- Do not claim `READY FOR PR` without baseline, unchanged candidate, acceptance, fresh passing required checks, no blockers/material gaps, and valid independent review.
- Generic review cannot substitute for this loaded skill's actual review gate.
