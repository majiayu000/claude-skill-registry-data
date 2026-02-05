---
name: orchestrate-subagents
description: Orchestrate parallel and/or sequential subagents working in separate git worktrees to deliver PR(s). Use when bundling multiple related GitHub issues into a single task, running best-of-3 identical attempts, monitoring runs, selecting the best PR, and closing/cleaning up the rest.
---

# Orchestrate Subagents

## Overview

Run coding subagents reliably: define a task bundle (often spanning several related issues), create isolated worktrees, spawn 1 or 3 identical attempts, then select the best PR and clean up the rest.

This skill is for the *orchestrator/PM agent*. Coding agents do implementation work and need not spawn subagents themselves.

## Workflow (Best-Of-3 Default)

### 1) Write a bundle spec

- Put the bundle spec in `/tmp/` (outside the repo), so you don’t create repo noise.
  - Example path: `/tmp/codex-bundle-spec-<date>-<slug>.md`
- Include:
  1. Issue list (IDs + titles).
  2. Acceptance criteria (bulleted, testable).
  3. Out of scope (explicit “DO NOT …” list).
  4. Required readings (exact file paths relative to worktree root).
  5. Definition of done (tests/checks to run, CI must be green).
  6. “Stop and ask” triggers (ambiguity, scope conflicts, failing tests that look unrelated).

### 2) Write the subagent prompt file

- Use one prompt file for all subagents (identical attempts):
  - Example path: `/tmp/codex-prompt-<date>-<slug>.md`
- Use an absolute prompt path in `codex exec` (e.g. a `/tmp/...` path).
- Transform the bundle spec into a prompt. Add instructions that are about how the subagent has to work, beyond the bundle spec.
  1. Work only in their current worktree (`pwd` reveals it).
  2. Run onboarding/sanity: `bash -lc scripts/hello.sh`. Subagents read `AGENTS.md` and will know what to do.
  3. Implement the full issue bundle (single PR).
  4. Run the relevant checks (at minimum: `npm run check`).
  5. Open a PR (with a clear title and issue-closing footer).
  6. Stop and report back if they hit non-trivial blockers (don’t “invent” scope).
Minimal prompt template (edit for the specific bundle):

```md
# Prompt
You are a coding sub-agent. Work only inside your current git worktree.
## Onboarding
- Run `bash -lc scripts/hello.sh`.
## Task bundle
- Solve issues: #<A>, #<B>, #<C> as ONE coherent PR.
### Acceptance criteria:
- (list)
### Out of scope:
- (list explicit NOTs)
## Constraints
- Do not do PM tasks. Do implementation only.
- Do not add temporary/demo files.
## Process
- If you find ambiguity or a likely typo in the issue text, STOP and write a short question in the PR description.
## Validation
- (list)
## Deliverable
- Push a branch and open a PR.
- PR description must:
  - Reference all issues with “Closes #…”. 
  - Include a short, skimmable summary and any tradeoffs/risks.
  - Inform the reviewer of any deviations from the acceptance criteria.
  - Inform the reviewer of any shortcomings or known issues you did not address, and why you did not address them.
```

### 3) Create Worktrees and Spawn Subagents

- For best-of-3, create 3 worktrees with 1 subagent each.
- See `.codex/skills/git-worktrees/SKILL.md` for worktree management.
  - Create: `scripts/worktree-new.sh <path> <branch> [--force]`
  - Remove: `scripts/worktree-remove.sh <path> [--force]`
- Recommended naming (deterministic, easy to filter in PR list):
  - Slug: `<yyyymmdd>-<short-bundle-name>`
  - Branches: `agent/<slug>/a`, `agent/<slug>/b`, `agent/<slug>/c`
  - Paths: `/workspaces/worktrees/<slug>-a` (and `-b`, `-c`)
- Start each subagent from inside its worktree directory (no backgrounding):
  - `cd /workspaces/worktrees/<slug>-a && codex exec "Prompt: /tmp/codex-prompt-<date>-<slug>.md" 2>/dev/null`

Important:

- Do **not** add `&` to the `codex exec` command.
- To run best-of-3 in parallel, run one subagent per terminal (three terminals total).

### 4) Monitor and Triage

- We suppress stderr because it is extremely verbose and not meant for orchestrator review.
- When the agent is done, it exits and prints its final message to stdout. It also ought to have opened a PR as per the prompt instructions.
- Wait for all three agents to finish (process exit) before proceeding to selection. Agents maybe will not write to stdout at all until they are done.
- If a subagent fails early, e.g. due to misspecified scope or unclear instructions or violated task assumptions, you should usually escalate to the owner instead of trying to salvage the run.
- If a subagent never even starts, e.g. due to a typo in the `codex exec` command, you can usually just restart it without escalating.

### 5) Select the winning PR (best-of-3)

- Once all three subagents have finished, review their PRs.
- Prefer the PR that:
  1. Meets the bundle acceptance criteria, including passing all tests.
  2. Has the highest quality in code architecture, code style, and test coverage.
  3. Is a solid foundation for the remaining project work.
- The PR text is useful commentary, but not a source of truth: the worktree contents are what will be merged and thus the only thing that matters.

### 6) Merge, Close, and Clean Up

- Merge the winning PR via GitHub CLI.
- If the merged PR fell short of acceptance criteria, create follow-up issues for the remaining work.
- Close losing PRs with a short note (“best-of-3; superseded by #<winner>”).
- Delete their remote branches.
- Pull in the main worktree so the merged result is reflected locally.
- Remove the winning and the losing local worktrees.
- Hand-off to the owner with a summary:
  1. Winner PR link + what it does.
  2. Which PRs were closed and why.
  3. Anything that needs owner review/decision.
  4. Follow-up issues suggested (if any).
