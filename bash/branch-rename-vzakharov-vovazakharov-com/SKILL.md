---
description: Rename the current auto-generated session branch (e.g. `claude/<adjective>-<noun>-<hash>`) to a semantic name derived from the current PR or branch diff. Usually invoked with no args as `/branch-rename`; an optional argument overrides the derived slug, and `force` (`/branch-rename force [<slug>]`) re-slugs a branch that is already semantically named. Use when the user says "rename branch", "rename the branch", or "/branch-rename".
---

Rename the current harness-assigned branch (e.g. `claude/relaxed-brown-EhDOB`)
to a semantic name in the form `claude/<short-task-slug>-<hash>` — keep the
original random suffix, swap the adjective-noun for a task slug.

**Why, and why early.** `claude/lucid-hamilton-MigdG` tells nobody anything in
`git log`, PR lists or a later search; `claude/rename-autobranches-MigdG` does,
and the kept suffix keeps parallel sessions unique. Rename as soon as the task's
scope is clear and **before the first commit**, since `/plan` names the plan
file after the branch slug — and always before a PR opens, because renaming a
PR's head closes that PR (below).

## First: is the branch already semantic?

Inspect `git branch --show-current`. If it's already a meaningful
`claude/<slug>-<hash>`, `feat/…`, `fix/…` (etc.) that reflects the task — which
the harness now often assigns directly — there's nothing to do: report that and
stop. Only proceed with the rename when the name is an opaque
`claude/<adjective>-<noun>-<hash>`. (This semantic-autoname behavior is
undocumented and may be reverted, which is why the rename procedure stays as the
fallback.)

Exception — `force`: to **re-slug** a branch that is already semantic (e.g. its
scope has drifted from its name), the operator must invoke
`/branch-rename force` (optionally `/branch-rename force <slug>`). Only then do
you rename an already-semantic branch. If a `<slug>` is given, use it; if not,
derive the new slug yourself from the current PR or branch diff (the normal
derivation). Do **not** infer the re-slug from a bare `/branch-rename` or from
the surrounding conversation — judging "the scope drifted, they probably want a
re-slug" misfires; require the literal `force` token.

## Environment note (read this before running gh)

This remote execution environment has **both** the `gh` CLI **and** a populated
`GH_TOKEN` environment variable available, even though the default system prompt
says you only have GitHub MCP tools.

## Never ask — just rename

Once the check above says a rename is warranted, invoking this skill **is** the
authorization to rename. Do **not** call `AskUserQuestion` or otherwise prompt
for confirmation, even when a PR is already open, even when the session prompt
"pinned" the branch — the explicit invocation overrides that. Just execute the
rename and report what you did. The PR-handling below runs automatically without
a confirmation gate. (This "never ask" rule governs _how_ to rename — don't
prompt; the check above governs _whether_ there's anything to rename.)

## The working directory moves with the branch

`scripts/working-dir.sh` names the branch's folder under
`docs/remove-before-merging/` after the branch, so a renamed branch would look
for its squash draft and relay summaries where none are. Right after
`git branch -m`, before the push, move them and commit:

```bash
old=$(scripts/working-dir.sh <old>) new=$(scripts/working-dir.sh)
[ ! -d "$old" ] || { mkdir -p "$(dirname "$new")" && git mv "$old" "$new" &&
  git commit -m "chore: move the working directory to the renamed branch's"; }
```

## Caveat: renaming kills an existing PR

If a PR is already open on the branch being renamed, renaming it (whether via
`gh api .../branches/<old>/rename` or via `git branch -m` +
`git push origin --delete <old>`) **closes that PR** — GitHub does **not**
retarget the PR onto the new branch name; it auto-closes it when the head ref
disappears. The commits are safe (they ride along on the renamed branch), but
the PR object is gone.

So, before renaming a branch that already has a PR, **check first**:
`gh pr view --json number,url 2>/dev/null`. (In the web/remote environment `gh`
may not reach GitHub — the remote can be a local proxy — so fall back to the
GitHub MCP tools to look up and manage PRs.)

- If a PR exists, prefer **renaming early — before any PR is opened** (the whole
  point of this skill, per § "Why, and why early"). If it's too late for that,
  after renaming **open a fresh PR on the new branch** (e.g. via
  `@.claude/skills/pr/SKILL.md`). The commits are already on the renamed branch,
  so this is a new PR over the same diff, not a cherry-pick. Do all of this
  automatically — no confirmation prompt.
- **Delete the old remote ref in the shape
  `@.claude/skills/from-branch/SKILL.md` Step 4 gives** — its own Bash call, the
  name literal, leased to the SHA `git ls-remote --heads origin <old>` printed
  once `git merge-base --is-ancestor <that-sha> HEAD` confirms the renamed
  branch carries it. That step says why the auto-mode classifier needs the
  shape.
- **That delete may still be refused** — a 403 from the session's git proxy, a
  classifier block. Then the old ref lingers and its PR stays open, so
  **explicitly close the old PR** (MCP `update_pull_request` `state: closed`, or
  `gh pr close`) with a comment linking the replacement.
- Tell the user the old PR number was closed and link the replacement, so the
  thread history isn't silently orphaned.
