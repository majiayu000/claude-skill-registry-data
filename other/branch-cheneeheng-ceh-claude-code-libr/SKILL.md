---
name: branch
description: >-
  Load this skill when creating or naming a git branch, or starting new work from main: the prefix
  (feat/, fix/, chore/, docs/, test/, refactor/) and the short description.
disable-model-invocation: false
user-invocable: false
compatibility: >-
  Requires the git CLI on PATH and a git working tree. No network access, GitHub CLI, or language
  runtime is needed.
license: Apache-2.0
---

# Branch

Trunk-based development. `main` is always deployable. Branch from `main` only — never from
another feature branch. Delete branches after merge.

## Procedure

1. Start new work from an up-to-date `main`:

   ```bash
   git checkout main
   git pull origin main
   git checkout -b <type>/<short-description>
   ```

2. For anything long-lived, keep the branch current by rebasing on `main` rather than merging
   `main` in — it keeps history linear and the eventual PR diff clean:

   ```bash
   git fetch origin
   git rebase origin/main
   git push --force-with-lease     # your own branch only; --force-with-lease, never --force
   ```

   Do this before opening the PR and again if `main` moves ahead while the PR is in review.

3. When work runs alongside another session or agent in the same checkout (a multi-task plan
   while the user keeps editing, or a second, independent task started next to one in progress),
   isolate it in a worktree before the first edit. Two routes keep the user in the session:
   - To isolate this session, call the `EnterWorktree` tool.
   - For a second parallel session, tell the user to open another terminal and run
     `claude --worktree <name>`, and to open it in its own editor window
     (`code .claude/worktrees/<name>`). Never launch it yourself: a `claude -p` run from Bash is
     headless, so the user cannot talk to it and it skips the cleanup prompt on exit.

   Prefer these over a raw `git worktree add`, because Claude Code tracks the worktree and offers
   to remove it on exit. It names the branch `worktree-<name>`: rename it with
   `git branch -m <type>/<short-description>` before the first push. A Claude Code worktree
   branches from the default branch, not from the current `HEAD`, unless `worktree.baseRef` is
   `"head"` in `settings.json`, so check its base before building on unmerged work.

### Naming

```
<type>/<short-description>
```

| Prefix      | When to use                                    | Example                            |
| ----------- | ---------------------------------------------- | ---------------------------------- |
| `feat/`     | New feature                                    | `feat/session-replay`              |
| `fix/`      | Bug fix                                        | `fix/token-expiry-edge-case`       |
| `chore/`    | Maintenance, tooling, dependency updates       | `chore/update-dependencies`        |
| `docs/`     | Documentation only                             | `docs/add-onboarding-guide`        |
| `test/`     | Test additions or fixes with no source changes | `test/reasoning-engine-invariants` |
| `refactor/` | Code changes without feature or bug changes    | `refactor/extract-auth-middleware` |

Short description: lowercase, hyphen-separated, 3–5 words.

## Rules

- Branch from `main` only, so every branch starts from a deployable state and its diff stays
  scoped to one concern — branching off another feature branch entangles unmerged work and bloats
  the eventual PR.
- Rebase is fine locally during development.
- Force-push is allowed only on your own feature branch (never on `main`).
