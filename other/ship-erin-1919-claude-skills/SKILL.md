---
name: ship
description: Use when the user asks to commit and push changes (e.g. "commit and push changes in <dir>", "commit this and push", "ok commit and push", "publish to Pages", "push to the remote repo"). Runs the standard commit-and-push ritual, optionally scoped to a directory, with README refresh, org-repo creation, and GitHub Pages build-poll.
---

# ship — commit and push ritual

Stage, commit, and push the current changes. The user asking to ship IS their authorization to commit and push, so do not ask "should I commit?" Just run the ritual, confirming only for the consequential extras noted below.

`$ARGUMENTS` (or any directory the user named, e.g. "commit and push changes in `ref/`") is an optional path scope: a subfolder like `ref/`, `prototype/`, `meeting_notes/`, or an absolute path the user pasted. If none was given, operate on the whole repo from the current working directory.

## Workflow

### 1. Locate and inspect
- Resolve the target: `TARGET` = the named path if there is one, else the current working directory.
- Find the repo root: `git -C <TARGET> rev-parse --show-toplevel`. If not a git repo, report that and stop (offer `git init` only if the user asks).
- Show what changed, scoped to TARGET: `git -C <root> status --short -- <TARGET>` and `git -C <root> diff --stat -- <TARGET>` (include untracked).
- If there is nothing to commit under TARGET, say so and stop. Do not create an empty commit.
- Note the current branch: `git -C <root> rev-parse --abbrev-ref HEAD`.

### 2. README refresh (only when code changed)
- If the diff touches code or config (not just docs) AND a README in scope looks stale relative to the change, briefly offer to update it and show the proposed edit. **Edit only after the user confirms.** Skip silently for doc-only or trivial changes, and do not nag.

### 3. Commit
- Stage only the scoped changes: `git -C <root> add -- <TARGET>` (or `git add -A` when TARGET is the repo root).
- Write a **short imperative subject line** summarizing the change (e.g. "Rename sandbox to GridMind in web UI title", "Add reference sources: Gottweis et al., Yang et al."). Add a brief body only if the change needs it. End the message with the `Co-Authored-By` trailer for the model you are running as, matching whatever the environment reports (for example `Co-Authored-By: Claude <noreply@anthropic.com>`).
- Commit with a HEREDOC so the message formats correctly (Bash tool). Do not use `--no-verify`; if a hook fails, fix the cause.

### 4. Push
- Push to the current branch: `git -C <root> push`. If it has no upstream, `git -C <root> push -u origin <branch>`.
- If on `main`/`master`, note that in your report (the user usually works on a feature branch like `prototype`) but proceed, since they asked to ship.

### 5. No remote → offer org repo (confirm first)
- If the repo has **no remote** (`git remote -v` empty), offer to create one under the user's group org **github.com/UbiSensingAILab** and push. **Confirm before creating**, since repo creation is consequential and outward-facing. On yes:
  `gh repo create UbiSensingAILab/<repo-name> --private --source=<root> --remote=origin --push`
  (ask private vs public if unclear; default private).

### 6. GitHub Pages build-poll (when applicable)
- If the pushed repo publishes GitHub Pages (detect: repo named `*.github.io`, a `gh-pages` branch, or a Pages config), poll the deployment after pushing until it finishes:
  `gh api repos/<owner>/<repo>/pages/builds/latest --jq .status`, repeated until status is `built` (or `errored`), with short waits between checks. Report the final status and the live URL.
- Only poll when the change actually affects the published site.

### 7. Report
- One concise summary: commit hash and subject, branch, remote or URL, and Pages status if polled. If any step was skipped (for example a declined README refresh), say so plainly.

## Guardrails
- Never force-push, never skip hooks, never bypass signing unless the user explicitly asks.
- Scope staging to TARGET. Do not sweep unrelated changes into the commit.
- Report failures with the actual git or gh output rather than papering over them.
