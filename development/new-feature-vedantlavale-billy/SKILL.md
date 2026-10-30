---
name: new-feature
description: Start a task. Clarify the issue with the user when it is unclear, then branch off the latest origin/main after checking no open PR already owns the files. Use at the start of every feature, fix or task, before writing code.
allowed-tools:
  - Bash(git:*)
  - Bash(gh pr list:*)
  - Bash(gh pr diff:*)
  - Bash(gh issue view:*)
  - Bash(gh issue comment:*)
  - Bash(lsof -i:*)
  - Read
  - Grep
  - Glob
---

# Start a task

One task, one branch, off the latest `origin/main`. Never build on `main`.

Adapted from michaelshimeles/skills. The worktree mechanics are dropped: most
agent harnesses manage worktrees themselves. What matters here is the sync and
the scope check.

## 0. Understand the task before touching git

Read the issue, its comments, any linked PRs, and the code it points at. Then
decide: could you write down, in two sentences, what "done" looks like and how
you would prove it?

If not, **ask the user before building.** Guessing costs a full build-review
loop; a question costs a minute. Ask when any of these is unclear:

- **The outcome.** What should a user see or be able to do when this is done?
- **The scope.** What is explicitly out of it?
- **The reproduction.** For a bug: steps, account, expected vs actual.
- **The acceptance check.** How will the user judge it finished?
- **A conflict.** The issue contradicts the code, another issue, or `AGENTS.md`.

Rules for asking:

- Never ask what you can read. Check the issue thread, code and git history
  first, and come with a draft: "I read this as X, done means Y. Right?"
- Ask everything in one short batch, at most five questions, most important
  first. Offer choices when there are obvious options.
- Write the answers back onto the issue as a comment, so the next agent does
  not have to ask again.
- A small, unambiguous task needs no questions. Do not interrogate a typo fix.
- If it needs more than one round of questions, or you cannot reproduce the
  bug, stop here and run `/triage` on the issue instead. It verifies the claim
  and leaves an agent brief with acceptance criteria, which `deep-review` later
  checks the PR against.

## 1. Sync

```bash
git fetch origin
git branch --show-current
```

If you are on `main`, branch before touching anything.

## 2. Scope check

More than one agent works this repo. Before you start, find out whether an open
PR already owns the files you are about to change.

```bash
gh pr list --state open --json number,title,headRefName
gh pr diff <n> --name-only
git status --porcelain
```

If another open PR touches your files, stop and ask which way to go. Do not
start and hope the merge works out. If the working tree has uncommitted changes
you did not make, stop, another session may be mid-task.

## 3. Branch

```bash
git checkout -b <prefix>/<short-task-name> origin/main
git branch --show-current   # must not print main
```

Match the names already in the repo: `feature/…`, `fix/…`, `feat/…`, or
`<yourname>/<task>`. Keep it lowercase with hyphens.

## 4. Before you run anything

A branch does not isolate anything outside the file tree. These are the shared
resources in this repo that a second agent can collide with.

- **Databases.** None. Billy is fully client-side. `supabase/` is dead code;
  never run its migrations or point anything at a Supabase project.
- **Browser storage.** Every agent driving `localhost:3000` in the same browser
  profile shares one `localStorage` draft (`billy_invoice_data`, plus
  `billy_profession_preset`). One agent's test invoice overwrites another's. Use
  your own browser profile or context per agent.
- **Ports.** `bun run dev` serves on 3000. Next picks another port if 3000 is
  taken, so read the port it prints, then confirm it is your process:
  `lsof -i :3000`.
- **Lockfiles.** `bun.lock` at the repo root. Resolve a conflict with
  `bun install`, never by hand.
- **Caches and build output.** `bun run build` writes `apps/web/.next` and
  `apps/web/out`, and Turbo caches in `.turbo/`. Running a build while
  `next dev` is up can leave the dev server serving a broken tree. Restart it
  after.
- **Watchers.** If an edit does not show up in `next dev`, compare the server
  start time against the file's mtime before debugging, and restart.

## 5. Rules that hold for the whole task

- Never commit to `main`, never force-push to `main`.
- Only `--force-with-lease`, only on your own branch.
- Keep the change scoped to the task.
- Do not commit unless you are asked to. Finish the work and leave it staged or
  uncommitted; committing is the user's call.
- If a conflict cannot be resolved confidently, stop and report instead of
  guessing.

## Cleanup

After the PR merges:

```bash
git checkout main && git pull
git branch -D <branch>
```

`-D` is expected. After a squash merge, `-d` refuses even though the work landed.
