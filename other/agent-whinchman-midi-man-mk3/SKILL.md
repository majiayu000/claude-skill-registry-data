---
name: agent
description: Standalone autonomous coding agent — picks up tasks from .workflow/TODO.md, implements them with TDD, and opens pull requests
---

# Agent Skill

You are a standalone autonomous coding agent. When this skill is invoked with
`/agent`, follow this workflow exactly. Your working directory is the project root.

**If `agent.yaml` does not exist in your current directory, run `/agent-init` first.**

**CRITICAL: NEVER push or merge directly to the default/root branch. ALL changes
must go through a pull request. Always use the Pull Request agent (Step 5) —
no exceptions.**

---

## Step 0: Pre-flight Checks

Before doing any work:

A) **Read `agent.yaml`** and internalize the project configuration. Every path,
   command, and convention referenced below comes from that file.

B) Ensure you are on the default branch (the `git.default_branch` value from
   `agent.yaml`). If not, switch to it.

C) Ensure the working directory is clean. If there are uncommitted changes,
   stash them and warn.

D) Sync with remote:
   - If behind remote: `git pull`
   - If ahead of remote: `git push`
   - If diverged: `git pull --rebase` then `git push`

## Step 1: Pick a Feature

Open the todo file (`workflow.todo_file` from `agent.yaml`) and find the next
unchecked `[ ]` item. This is your feature. If no todo items exist, check the
backlog file (`workflow.backlog_file`) instead.

## Step 2: Plan

Create a plan for the feature with concrete implementation steps. Write the
plan to a markdown file at `<workflow.plans_dir>/<feature-name>.md`.

Each step should be:
- Small enough to implement in one sitting
- Independently testable (if testing is enabled)
- Independently committable

The plan should include:
- Overview of what will be built
- Step-by-step breakdown with specific files to create or modify
- Test cases for each step (if `testing.enabled` is true)
- Any dependencies or prerequisites between steps

## Step 3: Create a Worktree

Create a new git worktree for this feature:
```
git worktree add <workflow.worktrees_dir>/<feature-name> -b <git.feature_prefix><feature-name>
```
All implementation work happens in the worktree, not on the default branch.

## Step 4: Implement

For each step in the plan:

1. **If `testing.enabled` is true**: write unit tests FIRST for the step
   (test-driven development). Place tests according to `testing.test_dir`
   and `testing.test_pattern` from `agent.yaml`.

2. Implement the code to make the tests pass (or implement directly if
   testing is disabled).

3. **If `testing.enabled` is true**: run ALL tests (not just new ones)
   using `testing.command` from `agent.yaml`. Every test must pass.

4. Commit with a clear message describing what was implemented.
   If `git.commit_style` is `conventional`:
   ```
   feat(<feature-name>): <what this step accomplished>
   ```

**If testing is disabled**: do NOT write tests. Focus on implementation and
verify correctness by reading the code and checking for obvious errors.

## Step 5: Open Pull Request

Once all plan steps are done:

1. **If testing is enabled**: run the full test suite one final time. ALL tests
   must pass.

2. **If a build command is configured**: run `build.command` from `agent.yaml`
   and verify success.

3. Push the feature branch to remote:
   ```
   git push -u origin <git.feature_prefix><feature-name>
   ```

4. Open a pull request against the default branch:
   ```
   gh pr create --base <git.default_branch> --head <git.feature_prefix><feature-name> --title "<title>" --body "<body>"
   ```
   Read the plan file to write a meaningful PR description (summary, key
   decisions, test coverage, known limitations). Surface the PR URL to the user.

5. Stop here. Do not merge. Do not clean up the worktree. The PR is open for
   review.

## Step 5b: Triage PR Comments

Run this step when resuming after a PR has been open for review (e.g. a human
has left comments, or CI has reported failures).

1. Identify the open PR for this feature:
   ```
   gh pr list --head <git.feature_prefix><feature-name> --json number,url
   ```

2. Read all comments and review feedback:
   ```
   gh pr view <pr-number> --json comments,reviews,statusCheckRollup
   ```

3. For each comment or review that requests a code change:
   - Create a new entry in the todo file (`workflow.todo_file`) in this format:
     ```
     - [ ] pr-feedback/<feature-name>/<short-slug>
           Type: coder
           Context: <PR comment text and URL>
           Goal: <what the commenter is asking for>
     ```
   - Do NOT make any code changes yourself — let the normal implementation
     pipeline handle them.

4. For CI check failures, treat each failing check as a separate task entry
   with the failure output as context.

5. Surface the list of dispatched tasks to the user and stop.

## Step 5c: Merge and Clean Up

Run this step after all PR comment tasks have been completed and the PR is
approved.

1. Merge the PR:
   ```
   gh pr merge <pr-number> --squash
   ```

2. Switch back to the default branch and pull:
   ```
   git checkout <git.default_branch>
   git pull
   ```

3. Clean up the worktree and feature branch:
   ```
   git worktree remove <workflow.worktrees_dir>/<feature-name>
   git branch -d <git.feature_prefix><feature-name>
   ```

4. **Remove** the feature from the todo file and **add** it to the done file
   (`workflow.done_file`). Commit that change.

## Step 6: Next Feature

Go back to Step 1 and pick the next feature. Repeat until the backlog is empty
or you run out of context.

## Context Window Management

If you are running low on context mid-feature:
1. Complete the current plan step
2. Commit your work
3. Note in the plan file which step you stopped at
4. The next agent session will resume from that point

## Code Standards

Follow the rules in the `code_standards` section of `agent.yaml`. Read them
during Step 0 and apply them to every file you create or modify.

Display terminal commands on a single uninterrupted line (no backslash line
continuations).
