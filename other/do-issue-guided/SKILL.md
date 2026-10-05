---
name: do-issue-guided
description: Work on a GitHub issue interactively with the user. Proceeds autonomously through routine work but pauses for confirmation at key decision points and when uncertain.
argument-hint: issue number (e.g., 123)
user-invocable: true
disable-model-invocation: false
---

# Work on GitHub Issue (Guided)

Work on GitHub issue `$ARGUMENTS` interactively. Follow every phase in order. Do not skip phases. Proceed autonomously through routine work, but pause for user confirmation at key decision points marked with **🔲 Checkpoint**.

## Preflight (mandatory)

Run this **first**. If it exits non-zero, halt and report the stderr output to the user verbatim. Do not proceed.

```bash
uv run maverick preflight do-issue-guided
```

The check verifies the project is initialised and required tools (`gh`, `git`, `uv`) are on PATH. PR code review runs locally as the `agent-code-reviewer` subagent (see Phase 8); the optional CI-side re-run described in `mav-bp-remote-code-review` is not required.

## Before You Begin

If `$ARGUMENTS` is empty or not a valid issue number, ask the user for the issue number before proceeding. Do not attempt any phase without it.

**Entry check:** run `uv run maverick coord read <repo> $ARGUMENTS`.
If another instance holds a live claim, or the issue carries a
`blocked-by:#N` label, stop and report to the user — guided mode does not
take a claim of its own, but it must not silently work an issue an
autonomous instance already owns.

State for this workflow lives in the `maverick-task-progress` marker on
the issue (see mav-github-issue-workflow); there is no local
state file.

## Phase 1-2: Understand the Issue and Solution Design (subagent)

Run Phases 1 and 2 as a subagent to keep the main context window clean for implementation.

1. Dispatch the **agent-issue-analyst** agent with:
   - Issue number: `$ARGUMENTS`
   - Mode: `guided`
2. When the agent returns, verify the design landed durably —
   `uv run maverick task-progress read <repo> $ARGUMENTS` shows
   `comments.design` set to a comment ID.
3. If the agent flagged ambiguities, present them to the user and wait for answers before continuing.

**🔲 Checkpoint — Design review:** Present a brief summary of the solution design to the user. Include the key approach, main components affected, and any trade-offs. Ask the user to confirm or suggest changes before proceeding. Do not continue until the user approves.

## Phase 3: Create Tasks (subagent)

Run Phase 3 as a subagent to keep the main context window clean for implementation.

1. Dispatch the **agent-github-issue-planner** agent with:
   - Issue number: `$ARGUMENTS`
   - Design comment ID from the task-progress marker (`comments.design`)
2. When the agent returns, verify the tasks landed durably —
   `uv run maverick task-progress read <repo> $ARGUMENTS` shows:
   - If < 5 tasks: `comments.tasks` set to a comment ID
   - If >= 5 tasks: sub-issues exist on the issue
3. If the agent flagged scope concerns, present them to the user.

**🔲 Checkpoint — Tasks review:** Present the task list to the user — each task title and description, their order, and any dependencies. Ask the user to confirm, reorder, add, or remove tasks. Do not continue until the user approves.

## Phase 4: Create Branch

1. Derive the branch name per the mav-github-issue-workflow skill (branching conventions).
2. Resolve the base branch from config:
   ```bash
   STORY_BASE=$(uv run maverick git-workflow story-base)
   ```
   Create the branch from `$STORY_BASE`.
3. Record it: `uv run maverick task-progress set <repo> $ARGUMENTS branch --branch <branch>`.

## Phase 5: Execute Tasks

1. Check for project-level skills in `docs/maverick/skills/`. For each topic directory that contains a `SKILL.md`, read it. These project skills provide codebase-specific guidance (libraries, patterns, configuration) that supplements the best-practice skills. If none exist, continue without them.

**If the tasks were created as sub-issues (>= 5 tasks):**

1. Read the tasks summary comment on the parent issue for the execution order
2. For each sub-issue in execution order:
   1. Read the sub-issue description
   2. Implement the change described
   3. Run verification (lint, typecheck, tests) per the mav-local-verification skill
   4. Commit with a conventional commit referencing the parent issue
   5. Update the tasks summary comment: mark the sub-issue as complete
   6. Close the sub-issue
3. After all sub-issues are complete, run the full verification suite

**Otherwise (checklist tasks):**

1. Read the tasks comment on the issue
2. For each task in order:
   1. Implement the change described
   2. Run verification (lint, typecheck, tests) per the mav-local-verification skill
   3. Commit with a conventional commit referencing the issue number
   4. Check the task off durably: `uv run maverick tasks check <repo> $ARGUMENTS <n>`
3. After all tasks are complete, run the full verification suite

Follow the mav-plan-execution skill for the execution loop, verification discipline (including the canonical retry budget), failure handling, and crash recovery. In guided mode, it will:
- Provide brief progress checkpoints every 3-4 tasks.
- Pause and ask the user when uncertain about an implementation approach.
- Pause and discuss with the user when a design assumption proves wrong.
- Ask the user for help when a task exhausts the retry budget.

## Phase 6: Documentation Review (mandatory)

This phase **always runs** before push. The agent decides whether any
docs work is needed; the workflow does not skip the analysis based on
its own heuristic.

1. **Build the diff and candidate-doc shortlist** in one deterministic step:
   ```bash
   uv run maverick docs shortlist --base "$(uv run maverick git-workflow story-base)"
   ```
   This writes `/tmp/diff.patch`, `/tmp/changed-paths.txt`, and
   `/tmp/doc-shortlist.txt`. An empty shortlist is valid — the agent is
   dispatched with a pre-filtered shortlist rather than an open-ended
   "audit every doc" brief (which cost ~6 min of wall clock on a
   15-file diff on prior issues).
2. Dispatch the **agent-tech-docs-writer** agent with:
   - **Mode:** `update` (per `do-docs`)
   - **Diff:** `/tmp/diff.patch`
   - **Candidate docs:** the contents of `/tmp/doc-shortlist.txt`. If
     the file is empty, pass the literal string
     `<empty — scan only for gaps requiring new coverage>`.
   - **Instructions:**
     - Read each candidate doc. Update only sections rendered stale by
       the diff; do **not** refactor unrelated content.
     - If the diff introduces a component, subsystem, or architectural
       change with no coverage anywhere in `docs/`, create the new
       document.
     - If you find a doc **outside the candidate list** that you
       believe is impacted, **list its path in your return payload —
       do not edit it.** One-pass dispatch: no widen-and-retry; the
       caller surfaces these as a follow-up note for the user.
     - Returning "no doc changes required" is a valid outcome and must
       be reported explicitly.
3. **🔲 Checkpoint — Review docs outcome with the user:** show what was
   updated or created (or the explicit no-op decision), surface any
   out-of-shortlist docs the agent flagged, and confirm. If updates are
   inaccurate or out of scope, push back and ask the agent to revise.
4. Commit any doc changes with a `docs:` conventional commit.

## Phase 7: Pre-push Cybersecurity Review (mandatory)

This phase **always runs** before push. Any changed code AND any code that could be impacted by the changes (callers, importers, dependents) must be reviewed by `do-cybersecurity-review` before the push proceeds.

1. Compute the full diff: `git diff $(uv run maverick git-workflow story-base)...HEAD`.
2. Dispatch the **do-cybersecurity-review** skill with:
   - **Mode:** `update`
   - **Diff:** the output of step 1, passed via stdin or as a file path
   - **Instructions:** review the changed code AND the impact set (callers, importers, dependents — bounded to one or two hops). Return the structured outcome (verdict + findings).
3. **🔲 Checkpoint — Review security outcome with the user:** show the verdict and any findings. If BLOCKING, halt and route the user back to Phase 5 (implement) to resolve the issues before re-running this phase. If FINDINGS or PASS, confirm with the user before proceeding.
4. If FINDINGS, fold the security findings into the PR description draft so they are visible to the human reviewer.

## Phase 8: Code Review

The review runs **after** docs and security so the diff the reviewer
approves is the diff that ships — reviewing before those phases meant
their commits landed unreviewed.

1. Dispatch the agent-code-reviewer agent with the issue requirements and the diff (`git diff $(uv run maverick git-workflow story-base)...HEAD`).
2. The reviewer performs two-stage review: spec compliance first, then code quality. Its reply ends with a `MAVERICK_VERDICT: PASS|FAIL` marker line — that line is the verdict. If the marker is missing or ambiguous, treat the review as FAIL; do not infer a verdict from the prose.
3. If spec compliance fails, stop — fix the gaps before requesting re-review.
4. Process code quality feedback per the do-pullrequest-review skill:
   - Read all items before acting.
   - Clarify unclear items before implementing any.
   - Verify each suggestion against the codebase.
   - Push back with reasoning when a suggestion is incorrect.
   - Implement valid fixes one at a time, verifying after each.
5. If fixes changed the implementation approach, update the tasks comment on the issue.
6. Request re-review if there were critical or spec compliance issues — and re-run this phase whenever review fixes produced new commits, so the approved diff stays the shipped diff. Repeat until approved.
7. **Checkpoint**: `uv run maverick task-progress set <repo> $ARGUMENTS review`.

**🔲 Checkpoint — Review results:** Present a summary of the review outcome to the user — what was flagged, what was fixed, and what was pushed back on. If there were significant changes during review, highlight them.

## Phase 9: Push and Verify CI

1. Run pre-push verification per the mav-local-verification skill (lint, typecheck, tests). Fix any failures before pushing.
2. Push the branch to remote.
3. Monitor CI per the mav-bp-cicd skill. If CI fails, read the failure logs, fix locally, and push again. Do not proceed until CI passes. (After the PR exists, `uv run maverick pr wait <repo> <pr-num> --checks --timeout 30m` gives a bounded wait.)

## Phase 10: Update Issue and Create PR

1. Post a completion comment: `uv run maverick issue comment post <repo> $ARGUMENTS --kind completion --body-file <file>`.
2. Create a pull request per the mav-github-issue-workflow skill (PR pattern — the body must carry `Closes #$ARGUMENTS`).
3. **Checkpoint**: `uv run maverick task-progress set <repo> $ARGUMENTS complete`.

**🔲 Checkpoint — Done:** Present the PR URL to the user and summarise what was delivered.

## Rules

- **Pause at checkpoints** — every phase marked with 🔲 requires user confirmation before continuing.
- **Work autonomously between checkpoints** — do not ask for permission on routine implementation work. Only ask when uncertain, blocked, or at a checkpoint.
- **Run verification** after each task and after all tasks. Do not declare success if checks fail.
- **Never commit directly** to the story base branch.
- **Use conventional commits** that reference the issue number (e.g., `feat: add rubric export (#42)`).
- **Always create a PR** at the end — deliver a complete result.

<!-- maverick-plugin-version: 4.0.2-dev -->
