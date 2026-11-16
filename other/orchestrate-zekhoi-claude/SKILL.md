---
name: kit-orchestrate
description: Plan and run a multi-step engineering task by splitting it into steps, assigning each step to the installed kit skill or subagent that fits (for example kit-architect for design or kit-planner for a step plan, kit-feature-implementation to build, kit-test-writing, kit-documentation, kit-reviewer to review), running dependent steps in order and independent steps as parallel subagents with separate file scopes, and verifying the combined result. Use when a request spans several workflows (build, test, document, review), touches several independent modules or packages, or the user asks to orchestrate, delegate, plan and execute, split the work up, work in parallel, or use subagents. Do not use for a single focused change that one skill covers (use that skill; for a change across monorepo packages, kit-monorepo-change), for questions, or for code review alone (use kit-code-review).
---

# Orchestrate

## 1. Understand the whole task

- Restate the goal, the deliverables, and the constraints. Read project instructions and enough of the code to know which modules, packages, or services are involved.
- Ask only about decisions that change the plan (scope, target modules, whether to open a PR). Otherwise state assumptions and continue.

## 2. Plan

- Use the skills and subagents your tools show as available, so steps are only assigned to what exists. As a fallback, look for kit items in the project or home directory: `.claude/skills/kit-*` and `.claude/agents/kit-*` (Claude Code), `.agents/skills/kit-*` and `.codex/agents/kit-*.toml` (Codex), or the plugin's `agent-kit:` names. Use kit-architect for design trade-offs and kit-planner, when installed, for a step plan of a large or unclear task.
- Break the task into steps. For each, record: the goal, the owner (a kit skill, a kit subagent, or yourself; prefer the matching kit skill, such as kit-feature-implementation, kit-test-writing, or kit-documentation, even when steps run in order), the files or area it touches, what it depends on, and how it is verified.
- Group steps that can run in parallel: they must be independent and touch disjoint files, so their results apply cleanly. Steps that edit the same files, depend on each other's output, or change shared contracts (schemas, APIs, lockfiles) run in order.
- In a Git repository, every parallel group that edits files runs one subagent per Git worktree created from the current commit. Use the shared working tree only for read-only subagents, a single delegated step, a directory that is not a Git repository, or a group whose files have uncommitted changes (see below).
- Show the plan briefly before executing when it has more than three steps or any parallel group.

## 3. Execute

- For a step owned by a skill, invoke that skill and follow it. For a step owned by a subagent, give it a self-contained prompt: the goal, the working directory, the exact scope and files it may change, the files it must not touch, constraints from project instructions, and the verification to run and report. Tell every subagent not to commit, push, stash, check out, or reset, and not to touch any directory other than its own: the orchestrator owns Git state. In the shared tree, subagents also must not install dependencies or change lockfiles.
- Run a parallel group as separate subagents in one batch; keep groups small (two to four agents) and never let two of them edit the same file.
- After each step or group, check the result yourself: read the diff, run the step's verification, and fix or re-delegate failures before moving on. Do not trust a subagent's success claim without evidence.
- Stop and ask the user if a step reveals that the plan is wrong, needs a destructive or outward-facing action (pushing, publishing, deploying, deleting data), or conflicts with project instructions.

### Parallel groups in worktrees

- Before creating any worktree, run `git status --short` in the user's tree. Worktrees contain only committed work, so if files the group will touch have uncommitted changes, ask the user before committing anything, or run that group in the shared tree under the rules above.
- Create each worktree yourself from the user's current commit, not from the default branch. Run each step below as a single command so permission rules can approve it. Note the commit from `git rev-parse HEAD`, then run `git worktree add <dir> -b kit/<task>-<n> <commit>` with `<dir>` as the absolute path of `.claude/worktrees/kit-<task>-<n>` in the repository (add `.claude/worktrees/` to `.git/info/exclude` so it stays out of `git status` and tool scans), where Claude Code's sandbox allows writes (Codex may need approval for Git to write the worktree metadata). Do not use agent isolation options that branch from the remote default branch. Start the subagent with that directory as its working directory (Claude Code: the Agent `cwd` parameter) and tell it to read and write only inside it.
- Inside its worktree a subagent may install dependencies and run builds and tests; it must not commit.
- When a subagent finishes, review its worktree yourself (read the diff, run its verification). Then export only the step's paths to a patch file at the absolute path of `.claude/worktrees/kit-<task>-<n>.patch`: `git -C <dir> add -A -- <paths>`, then `git -C <dir> diff --cached --binary <commit> --output=<patch> -- <paths>` (diffing against the noted commit keeps work the subagent committed by mistake). Check that `git apply --numstat <patch>` lists only expected files: no lockfiles, dependency directories, or build output unless the step was meant to change them.
- In the user's tree run `git apply --check <patch>`, then `git apply <patch>`. Confirm the result by comparing `git apply --numstat <patch>` with `git status --short` and reading new files, which stay untracked. Never commit to the user's branch.
- If a patch does not apply, stop: keep the patch file and that worktree, and report both paths and the conflicting files instead of forcing the change.
- Clean up every other worktree before reporting: check that `git -C <dir> log --oneline <commit>..HEAD` is empty (or that its commits are in the patch), then run `git worktree remove --force <dir>`, `git branch -D kit/<task>-<n>`, and `git worktree prune`, and delete the patch files and the `.claude/worktrees` directory once it is empty. Report anything that could not be removed.

## 4. Integrate and verify

After the worktrees are removed, run the project's full checks (build, type check, lint, tests) on the combined changes in the user's tree, and use `kit-reviewer` or kit-code-review for an independent review when the change is substantial.

## 5. Report

Summarize the plan as executed (steps, owners, what ran in parallel), what changed, verification results, review findings and how they were handled, and anything skipped or left for the user.

## Examples

- Use: "Add due dates to todos, with tests and docs, and get it reviewed." "Add input validation to packages/api and packages/worker." "Plan and execute the migration to the new logger using subagents."
- Skip: "Fix the typo in README." "Add a POST /users endpoint." (kit-fastify-api or kit-feature-implementation) "Review my branch." (kit-code-review)
