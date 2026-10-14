---
name: sdd-requesting-code-review
description: Use when a feature or branch is complete and before merging, to get an independent two-axis review (Spec + Standards); in subagent-driven or inline plan execution this is the final whole-branch review seat
disable-model-invocation: true
metadata:
    opencode/autoinvoke: false
---

# Requesting Code Review

Dispatch the `sdd-final-reviewer` agent to catch issues before they cascade. The reviewer gets precisely crafted context for evaluation — never your session's history.

**Core principle:** Review early, review often. Findings come back on two axes — Spec (does it match what was asked) and Standards (is it well-built) — and the axes are never merged or reranked into one list.

## When to Request Review

**Mandatory:**

- The whole-branch final review after the last task of a subagent-driven or inline plan execution. SDD's per-task review is a different seat (`task-reviewer-prompt.md`); this skill is the broad review that follows all tasks.
- After completing major feature
- Before merge to main

**Optional but valuable:**

- When stuck (fresh perspective)
- Before refactoring (baseline check)
- After fixing complex bug

**Not this skill:** in-flight doubt about a single claim is the Falsification Pass in `sdd-verification-before-completion`; this skill is the post-hoc review of a finished artifact. Never dispatch both over the same artifact.

## How to Request

**1. Pin the range and check it:**

```bash
# <base-branch> is the branch's fork point: the local default branch
# (main/master) in a local-only repo, origin/<default> when pushed
BASE_SHA=$(git merge-base <base-branch> HEAD)  # single task: git rev-parse HEAD~1
HEAD_SHA=$(git rev-parse HEAD)
git rev-parse --verify "$BASE_SHA" "$HEAD_SHA"
git diff --stat "$BASE_SHA".."$HEAD_SHA"     # must be non-empty
```

A bad ref or an empty diff fails here, not inside the reviewer. Never
assume `origin/main` exists — a local-only repo has no remote ref, and
sdd-finishing-a-development-branch confirms the same base. Commit or stash
tracked changes first (`git status --porcelain -uno` empty): uncommitted
work is not in the range.

**2. Assemble the package:**

When executing a plan, run the `sdd-subagent-driven-development` skill's
`review-package` by absolute path from the repo root —
`bash "$SDD_DIR/scripts/review-package" PLAN_FILE BASE_SHA HEAD_SHA`, where
`SDD_DIR` is that skill's directory. It writes the commit list, stat
summary, and full diff to one uniquely named file and prints the path.
Pass that path as the reviewer's diff input so the diff never enters your
own context. Exit 3 means no package was written (empty or unrooted
range, or an empty net diff) — fix the cause before dispatching.

**3. Dispatch code reviewer subagent:**

Dispatch the `sdd-final-reviewer` agent, filling the template at [code-reviewer.md](code-reviewer.md) — the final whole-branch review is a judgment task, and the agent definition pins its model and thinking variant (see SDD's Agent Selection).

**Placeholders:**

- `[DESCRIPTION]` - Brief summary of what you built
- `[PLAN_OR_REQUIREMENTS]` - What it should do
- `[BASE_SHA]` - Starting commit
- `[HEAD_SHA]` - Ending commit
- `[DIFF_FILE]` - Path the review package was written to (preferred diff input)

**4. Act on feedback:**

- Fix Critical issues immediately
- Fix Important issues before proceeding
- Note Minor issues for later (in SDD, they go to the ledger for the final review to triage)
- Fix across both axes — a clean Spec axis never excuses Standards findings, or the reverse
- Push back if reviewer is wrong (with reasoning)

## Example

```
[All plan tasks complete — dispatching the final whole-branch review]

BASE_SHA=$(git merge-base main HEAD)
HEAD_SHA=$(git rev-parse HEAD)
[review-package writes the range's commit list, stat, and diff to one file]

[Dispatch sdd-final-reviewer]
  DESCRIPTION: Verification subsystem — verifyIndex() and repairIndex(), 4 issue types
  PLAN_OR_REQUIREMENTS: docs/superpowers/plans/index-repair-plan.md
  BASE_SHA: a7981ec
  HEAD_SHA: 3df7661

[Subagent returns]:
  Spec: 1 Important (progress reporting missing from the spec's CLI contract)
  Standards: 1 Important (possible Feature Envy in formatReport), 1 Minor
  Assessment: With fixes

You: [fix pass; one scoped re-review; residual findings adjudicated and ledgered]
[Delete this plan's workspace; use sdd-finishing-a-development-branch]
```

## Common Rationalizations

| Excuse                                                                 | Reality                                                                                                                                                                                                                               |
| ---------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| "I'll just review the diff myself instead of dispatching a reviewer"   | You're the coordinator — reviewing the diff inline burns the context window you need to keep driving the work. Dispatch a reviewer subagent: the diff and the evaluation live in its context, and only the findings come back to you. |
| "The reviewer needs my whole session history to understand the change" | Hand it precisely crafted context, never your session's history. That keeps the reviewer on the work product, not your thought process.                                                                                               |
| "Tests pass, so the review will be clean"                              | Passing tests is the Standards axis at best. The Spec axis asks whether each requirement was implemented as asked; check both, and never let one axis stand in for the other.                                                         |

## Red Flags

**Never:**

- Skip review because "it's simple"
- Ignore Critical issues
- Proceed with unfixed Important issues
- Argue with valid technical feedback
- Accept a review that covered only one axis, or one that merged the axes into a single reranked list

**If reviewer wrong:**

- Push back with technical reasoning
- Show code/tests that prove it works
- Request clarification

See template at: [code-reviewer.md](code-reviewer.md)
