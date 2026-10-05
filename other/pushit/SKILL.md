---
name: pushit
description: "Commit and push completed changes with a focused, reviewable Git workflow; use when the user invokes $pushit or asks to commit and push work."
---

# Pushit

Commit and publish the user's completed change cleanly, with a history that tells a future
developer what changed, which bug or feature motivated it, and what was verified.

## Authorization boundary

The user's `$pushit` invocation authorizes a commit and push for the scoped work in the
current request. It does not authorize including unrelated dirty changes, force-pushing,
rewriting published history, deleting branches, or opening a pull request unless requested.
Preserve unrelated worktree changes and report them at the end.

## 1. Inspect before mutating

Read repository instructions that govern Git or release work, then inspect:

- `git status --short`
- current branch and its upstream
- `git remote -v`
- recent commit subjects
- staged and unstaged diffs (`git diff --cached` and `git diff`)

Identify the exact files and hunks belonging to the user's request. Check for secrets,
`.env*` files, credentials, private keys, generated output, dependency stores, and build
artifacts before staging. Never use `git add .` or `git add -A` as a shortcut when the
worktree is already dirty.

## 2. Choose the publishing workflow

An explicit user instruction wins. Otherwise classify the repository from evidence:

### Simple website: direct `main`

Push directly to the repository's default branch only when it is clearly a small,
single-website repository, with no meaningful branch/PR workflow, no project planning or
multi-package architecture, and the user treats it as a simple website. Confirm that the
default branch is actually `main`; never assume its name.

### Serious project: feature branch

Use a feature branch when the repository has signals such as a monorepo/workspaces,
`AGENTS.md` or planning contracts, multiple apps/packages, CI or review configuration,
protected-branch expectations, or the user describes it as a real project and says they
will merge it. If currently on the default branch, create a branch named
`codex/<type>-<scope>-<short-slug>` from the current checkout. If already on a non-default
feature branch, keep using it unless the user asks otherwise.

When classification is ambiguous, choose the feature-branch workflow. Do not bypass branch
protection or push directly to `main` merely because the remote permits it.

## 3. Isolate and verify the commit

Stage only the requested files or hunks. For mixed files, use patch/hunk staging and verify
that the staged diff contains no unrelated edits. Keep the index and worktree distinction
clear before committing.

Run the repository's required checks from its instructions. For a website, normally run
the relevant tests, lint/typecheck, and production build; use the narrowest trustworthy
checks when the repository documents a different contract. Always run `git diff --cached
--check`. Do not claim browser, deployment, device, credentials, or live-service success
from local checks alone. If a required check fails, stop before pushing unless the user
explicitly authorizes a knowingly failing push; record the exact failure in the commit
handoff.

Keep one logical requested task in one focused commit by default. Split independent changes
only when the user requests it or the separation is unambiguous and safe.

## 4. Write an industry-standard commit

Use Conventional Commits:

```text
<type>(<scope>): <imperative summary>

Why: <user-visible problem or requested capability>
Fix: <root cause and concrete implementation boundary>
Verification: <checks that passed, skipped, or remain blocked>
Notes: <migration, follow-up, or external gate when relevant>
```

Use `feat` for a new capability, `fix` for a bug correction, `refactor` for behavior-
preserving restructuring, `test` for test-only work, `docs` for documentation-only work,
and `chore`/`build`/`ci` for maintenance. Add a precise scope such as `mindmap`, `auth`,
or `web`. Keep the subject concise, imperative, specific, and free of emojis or vague
phrases such as “update stuff.” For bug fixes, name the symptom and the cause in the body
so another AI or developer can recover the reasoning from history.

Honor the repository's existing signing and hook configuration. Do not disable hooks with
`--no-verify`, invent a sign-off, amend a published commit, or rewrite history unless the
user explicitly asks and the operation is safe.

## 5. Push and prove the result

- Simple website workflow: push the focused commit to the default branch and its configured
  upstream.
- Serious project workflow: push the `codex/...` branch with `-u origin <branch>` and leave
  merging to the user. Do not create a PR unless asked.
- Never force-push. If `main` is protected or rejected, preserve the commit and push the
  feature branch when possible; report that a PR/merge is required.
- If authentication, network, or remote divergence blocks the push, do not claim success.
  Keep the local commit, state the exact blocker, and provide the next safe action.

After pushing, verify the local commit SHA equals the remote branch SHA, and report the
commit hash, branch, remote, included files, checks, and any remaining unstaged/untracked
work. A successful local commit is not a successful push until the remote ref is verified.

## References

- [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)
- [Git user manual: status, staged diffs, and commit messages](https://git-scm.com/docs/user-manual)
- [GitHub Docs: branches](https://docs.github.com/en/pull-requests/reference/branches)
- [GitHub Docs: pull request quickstart](https://docs.github.com/en/pull-requests/get-started/pull-request-quickstart)
