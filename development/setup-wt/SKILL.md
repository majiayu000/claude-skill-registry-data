---
name: setup-wt
description: Set up a task worktree in any Git repository from a task description or optional issue link, then open Herdr with hsw or bind a T3 Code thread to the checkout.
---

# Set up a worktree

Turn a setup request into a named worktree in any Git repository, ready for the user to work in. Accept a repo name, path, or the current repository. A ticket is optional. Default to a Herdr workspace with the existing `~/dotfiles/scripts/hsw` layout. Honor requests for worktree only, a different app, or a particular base branch. Setup alone does not start implementing the task.

Example requests:

```text
/setup-wt add search to my-api
/setup-wt fix the login redirect in ~/dev/personal/my-app, worktree only
/setup-wt update dependencies in the current repo, create a new T3 thread
/setup-wt refactor caching in the current repo, move this T3 thread into the new worktree
/setup-wt Let's work on https://emsmc1.atlassian.net/browse/AM-12345 in E2
```

## Resolve the task

- Resolve an explicit path first. For a repo name, locate matching repositories in the user's known workspace roots, such as `~/dev` and `~/sandboxes`; ask if the name is ambiguous. Use the current repository when no other repo is specified. Do not assume an EMS location for other repos.
- For EMS work only, read the `ems` skill for repository paths and aliases. E2 alone means the `ems2` backend; `front` or E2 frontend means `front`. Create both only when requested. EMS is an optional shortcut, not a prerequisite.
- Use the user's task description. If an issue link or key is supplied, read its title and relevant context through the available tool for that tracker. For Jira, use the `jira` skill. If the issue cannot be read, proceed with a supplied description or identifier and mention the missing title. Do not require a ticket or tracker connection for a plain task.
- Follow the selected repo's branch naming conventions. Otherwise use a short descriptive kebab-case name, adding the ticket key when supplied, such as `AM-12345-fix-tlo-retry`. Respect an explicit branch or directory name. Use the same name for the branch and directory by default; replace slashes with hyphens in the directory if the requested branch contains slashes.
- If T3 Code is selected without a conversation choice, clarify early whether to move the current thread or create a new one. Continue repository discovery while waiting; resolve this before creating the checkout because current-thread handoff creates it through T3.
- Ask only when the repo, requested task variant, or base cannot be determined. Show the selected repo, branch, path, and base in a brief update before creating them.

## Prepare the worktree

1. Resolve the repository's Git common directory and inspect `git -C "$task_repo" worktree list --porcelain`. For the user's bare layout, use the container holding `.bare/` as `task_repo` and create a sibling worktree there, wherever the repository lives. For an existing conventional checkout, preserve its layout and place the new worktree beside the primary checkout. Inspect the relevant checkout's `AGENTS.md` for setup or branch conventions.
2. Check for the exact branch and destination path before creating anything. Reuse a worktree already checking out that branch, even if its directory has another name. Preserve its working changes. An unrelated directory, a conflicting branch, multiple task variants, or a missing/prunable checkout needs inspection rather than forced replacement.
3. For a new branch, honor the requested base. Otherwise select the repo's primary remote, preferring `origin` when present, and use its default from `git -C "$task_repo" symbolic-ref "refs/remotes/$task_remote/HEAD"`. If missing, discover it with `git -C "$task_repo" ls-remote --symref "$task_remote" HEAD`. Fetch that remote before branching from its default or another remote branch. With no remote, use the documented local default branch or ask if unclear. If fetching fails, report it and ask before substituting a stale ref. Do not infer the base from a directory named `master` or `main`, or from the caller's current branch.
4. Validate the branch with `git check-ref-format --branch "$task_branch"`. For an explicitly requested current-thread T3 handoff, follow [references/t3-code.md](references/t3-code.md) before creating the checkout; T3 creates it and continues setup in the next turn. Otherwise create the worktree at the selected sibling path, using absolute paths:

   ```sh
   git -C "$task_repo" worktree add --no-track -b "$task_branch" "$task_worktree" "$task_base"
   ```

   For an existing branch without a checkout, omit `-b`, `--no-track`, and the base:

   ```sh
   git -C "$task_repo" worktree add "$task_worktree" "$task_branch"
   ```

5. Read the selected worktree's `AGENTS.md` before running its setup. If it has submodules, initialize its pinned versions with `git -C "$task_worktree" submodule update --init --recursive`. Run required setup documented for that checkout. Report setup failures separately from successful worktree creation.

Use the existing `clone-wt` helper only if the user requested a repository that needs cloning and its URL is known. Keep the repository's Git administration data in `.bare/`. Do not move it, force checkout a branch, reset working changes, or prune worktrees to make setup succeed.

Aspire setup is optional. If requested, follow the EMS skill and selected repo's Aspire docs; do not automatically cherry-pick `aspire-local` commits into every new branch.

## Open the workspace

- Default or explicit Herdr: follow [references/herdr.md](references/herdr.md). This uses the existing `hsw` script inside the target pane.
- T3 Code: follow [references/t3-code.md](references/t3-code.md). Honor the conversation choice resolved before checkout creation. Create a top-level thread only when the user explicitly asks for a new thread or conversation.
- Worktree only: finish after repository setup.

Verify the registered worktree path and checked-out branch, then the selected app's setup. Finish with the path, branch/base for new branches, and workspace label or T3 thread link. Say whether anything was reused and identify any incomplete step. If an app is unavailable, retain the worktree and give the next concrete action instead of silently switching apps.
