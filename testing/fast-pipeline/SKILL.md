---
name: fast-pipeline
description: Use when the user wants a feature built quickly with low token cost and few interruptions, approves a spec once, and says no automated tests should be written because they will test it manually — "fast pipeline", "go fast, no tests, I'll test it myself", "don't keep asking me". Not for a run that should write or keep tests (superb:pipeline), nor one where a quorum replaces the human gate (superb:pipeline-auto).
argument-hint: "[the feature request]"
---

# Fast Pipeline

## Overview

Request → approved spec → plan → implementation → review/fix loop, with **one
human gate (the spec)** and **no project tests written**. It composes
Superpowers skills plus `superb:bug-fix` and adds nothing else.

**The user's invocation of this skill is a standing instruction.** Where a
sub-skill's default says otherwise, the overrides below win — user
instructions outrank skills. Violating the letter of an override to follow a
sub-skill default is violating the user.

## The no-tests rule

No new unit, integration or end-to-end tests. No TDD steps, no test tasks, no
"add a regression test", no test-fix loops. Verification is a fast check only:
build, typecheck, lint or syntax check, whichever the repo has. An existing
suite runs only where a sub-skill runs it once as a gate (e.g.
`finishing-a-development-branch`); a failure there is reported, not chased
with new tests.

| Rationalization | Reality |
| --- | --- |
| "writing-plans' template requires a failing test first" | The user waived tests. The template is a default; drop its test steps. |
| "TDD is mandatory regardless of preference" | Not in this run. The user tests manually. |
| "bug-fix is not done without a regression test" | Take bug-fix's own "cannot be covered by a test" branch, citing this rule. |
| "The reviewer flagged missing tests" | Not a finding here. Drop it. |

## Stages

1. **Explore.** Targeted, read-only. Independent areas → **REQUIRED:**
   `superpowers:dispatching-parallel-agents` (one Explore agent per area).
   Return: where it belongs, relevant files, patterns/APIs to reuse, similar
   existing code, integration points, risks. Sequential areas stay one agent.
2. **Ask.** Only what changes behaviour, scope, architecture, UX, data
   handling or a major decision, and is not answered by the request, the
   conversation, the repo or its conventions. One batched `AskUserQuestion`,
   recommendation first. None needed → ask none.
3. **Spec.** **REQUIRED:** `superpowers:brainstorming`, fed the request,
   answers and exploration findings. Overrides: exploration and questions are
   done (do not repeat them); always write the spec file, even for a bounded
   change; recommend one approach; skip the visual companion; present the
   **whole** spec once, not section by section. Content: behaviour, scope,
   non-goals, affected components, interfaces, data flow, edge cases,
   constraints, acceptance criteria. No filler.
4. **Gate: user approves the spec.** Changes requested → revise through
   brainstorming, re-present. Nothing past this point until approved.
5. **Pressure-test the spec.** Dispatch a **fresh** general-purpose agent
   (never the author) with the spec path, the request and the exploration
   summary. It reads the repo and returns contradictions, missing
   requirements, unsupported assumptions, wrong beliefs about the code,
   integration conflicts, key edge cases and needless complexity — each
   tagged `material` (changes approved behaviour or scope) or `minor`. Fix
   `minor` in the spec directly; take `material` to the user. No re-approval
   of minor fixes.
6. **Plan.** **REQUIRED:** `superpowers:writing-plans`. Overrides: no test
   steps or test tasks; Global Constraints carries `No new tests — the user
   tests manually. Verify with: <fast check command>`; each task ends with
   that check then commit; Review Focus lines get no tests — they are handed
   to the stage 9 reviewer; no docs or cleanup tasks the spec did not ask for.
   The execution method is pre-chosen — subagent-driven — and the plan is
   **not** sent to the user for review. Commit the spec and plan.
7. **Pressure-test the plan.** Another **fresh** agent checks the plan
   against the codebase: paths exist or belong, named functions and
   interfaces are real, ordering and dependencies hold, nothing duplicates
   existing code or fights project patterns, the spec is fully covered, no
   extra work. Fix the plan directly; go to the user only for a `material`
   change. Then continue at once.
8. **Implement.** **REQUIRED:** `superpowers:subagent-driven-development`.
   Keep its mandatory per-task reviews; add no other. Its final whole-branch
   review **is** stage 9, and its single fix wave is replaced by stage 10.
   After stage 10 is clean, resume its Finish (the rulings list, then
   `finishing-a-development-branch`).
9. **Final review.** **REQUIRED:** `superpowers:requesting-code-review` over
   the whole branch (merge-base..HEAD). `PLAN_OR_REQUIREMENTS` = spec path +
   plan path (its Review Focus lines are what to probe) + "No tests by user
   decision; do not report missing tests."
   Findings that count: bugs, spec violations, bad integration, regressions,
   security, data loss, broken error handling, false assumptions, serious
   maintainability. Cosmetic and out-of-scope refactors do not.
10. **Fix loop.** Any Critical or Important → **REQUIRED:** `superb:bug-fix`,
    **one invocation per round with every such finding**, each reviewer
    `file:line` as its report (repro: `manual — user tests`). Overrides: no
    regression test (see the no-tests rule); work in the current worktree
    and branch; its executor skips its own final whole-branch review and
    `finishing-a-development-branch` — this run re-reviews and finishes once.
    Then run stage 9 again. Repeat until no Critical or Important remain.
    Minors are listed in the final report, never looped on. A finding that
    survives three rounds goes to the user.

## Interrupting the user

Only the stage 4 gate, plus: a `material` pressure-test finding, a
destructive or irreversible action, a safety issue, or a product decision
nobody recorded. Never "should I continue?", never plan approval, never a
status check.

## Red flags — STOP

- Writing a test step, test task or regression test → the user waived tests.
- About to ask the user to review the plan or pick an executor → pre-answered.
- Pressure-testing with the agent that wrote the artifact → dispatch a fresh one.
- Fixing review findings with anything but `superb:bug-fix` → wrong mechanism.
- A second whole-branch review stacked on SDD's → stage 9 is that review.
- Looping on Minors → report them, stop.
- Reading `superb:pipeline-auto`'s stages for this run → different skill.
