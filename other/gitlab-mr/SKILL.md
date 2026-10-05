---
name: gitlab-mr
description: Create focused GitLab merge requests with `glab`. Use when code changes are already implemented in a Git repository and Codex needs to inspect git state, isolate only the intended files, create or reuse a feature branch, run the repo's required validation commands, commit cleanly, push to `origin`, and open a merge request in GitLab.
---

# GitLab MR

Prefer a clean, reviewable MR over convenience. Never pull unrelated local changes into the branch just to make the working tree look tidy.

## Workflow

1. Inspect repo state first.
   - Run `git status --short`.
   - Run `git branch --show-current`.
   - Run `git remote show origin | sed -n '/HEAD branch/s/.*: //p'` to confirm the target branch.
   - Run `glab auth status` before attempting MR creation.
   - Identify unrelated modified or untracked files and keep them out of the MR.
   - Read applicable repo instructions such as `AGENTS.md` before choosing validation commands.

2. Stage only the intended changes.
   - Use explicit `git add <path...>`.
   - Never use `git add -A` or `git add .` in this repo for MR prep.
   - Re-check the staged set with `git diff --cached --stat`.
   - Leave unrelated files, including user edits and stray backups, unstaged unless the user explicitly asked to include them.

3. Create the branch before committing.
   - Use the repo convention `codex/<topic>`.
   - Base it on the current target branch, which is usually the `origin HEAD` branch unless the user requested another base.
   - If already on a suitable feature branch created for the requested work, reuse it instead of branching again.

4. Run the required validation for the touched scope.
   - Read the repo instructions and run the mandated validation for the touched scope.
   - If the repo does not specify validation, prefer the smallest command set that proves the change:
     - targeted tests first
     - then typecheck
     - then lint
   - If a command fails because of a real code issue, fix it before creating the MR.
   - If a command fails because of an environment or dependency issue unrelated to the change, capture the exact failure in the MR description and final handoff.

5. Commit cleanly.
   - Use one focused commit unless the user asked for a different history shape.
   - Use a short imperative message.
   - Do not amend or rebase unless the user explicitly asked.
   - If commit hooks modify files, review the resulting diff before pushing.

6. Push and open the MR with `glab`.
   - Push with `git push -u origin <branch>`.
   - Use this `glab` syntax because the installed CLI expects short flags:
```bash
glab mr create \
  -b <target-branch> \
  -s <source-branch> \
  -t "<title>" \
  -d $'## Summary\n- ...\n\n## Validation\n- ...' \
  -y
```
   - If `glab mr create` rejects a flag, run `glab mr create --help` and adapt to the installed version instead of guessing.
   - Keep the MR description concise and practical:
     - `## Summary`
     - `## Validation`

7. Report the outcome clearly.
   - Share the branch name, commit hash, and MR URL.
   - Mention any local files intentionally left out of the MR.
   - Mention any validation that could not be completed and why.

## Guardrails

- Do not include unrelated local changes just because they are already present in `git status`.
- Do not revert unrelated user changes to make the branch cleaner.
- Do not create a second commit or a second MR for the same scoped task unless the user asks.
- Do not use interactive git flows.
- Do not assume `glab` supports long flags like `--base`; verify the installed CLI shape first if there is any doubt.
- Do not scoop up backup files, editor junk, or unrelated documentation edits unless the user explicitly includes them.

## Common Requests

- "Branch this out and create an MR in GitLab using glab."
- "Commit only the relevant fix and open an MR."
- "Create a clean MR without including my local scratch files."
- "Push this branch and open a GitLab merge request."

## Done Criteria

- The requested changes are isolated on a `codex/*` branch.
- The required validation commands for the touched scope were run or the exact blocker was documented.
- The commit contains only the intended files.
- The branch is pushed to `origin`.
- The MR exists in GitLab and the user has the URL.

## Communication
Honor active caveman mode for user-facing replies per `../../references/communication-mode.md`. Keep durable artifacts normal unless the human asks otherwise. Drop caveman for safety/clarity when needed, then resume.
