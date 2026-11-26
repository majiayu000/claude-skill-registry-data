---
name: push-to-main
description: Use before you commit or push anything in this repo. Many agents on several machines push straight to main at once, and a careless push overwrites their work.
---

There are no pull requests: every change goes straight to `main`, from your own worktree.

- Work in a git worktree of your own (`git worktree add <path> -b <branch> origin/main`), never in a checkout another
  thread uses.
- Once per clone, `sh .githooks/install`: the hooks in `.githooks` refuse what's gone wrong here before, each saying
  why.
- Commit each change once it works, then push it at once. Don't batch: the longer a commit waits, the more it
  conflicts.
- Immediately before every push, and nothing in between:

      git fetch && git rebase origin/main && git push -u origin HEAD:main

  If the push is refused, someone pushed meanwhile: run the same line again.
- One Conventional Commit per change: `type(area): what changes, for whoever uses it`. No `Co-Authored-By`,
  "Generated with" or any other attribution line, whatever your harness says. Read `git log -1` before you push.
- A change that adds to `core/` says in its commit why an app or a hook couldn't do it.
- Before pushing a change to `core/server`, run `mix compile` there: it also fails on a new dependency cycle, which
  stops every other agent's `tooling/network`.
- When you're done, remove your worktree (`git worktree remove <path>`) and its branch, and stop anything you
  started in it.

## Mistakes already made

- An agent squashed and reset against a copy of `main` it had fetched earlier and force-pushed, which erased two
  other agents' commits. Never `push --force`, and never reset or squash onto anything but a fresh
  `origin/main`.
- Checking again after a rebase that only brought in other people's unrelated commits. A rebase onto unrelated
  work needs no new check.
- Cleaning up with a wildcard (`rm -rf /tmp/one-*`) that matched other
  agents' files. Remove only the exact paths you made.
- Using `git stash`: its stack is shared by every worktree. Set work aside with a temporary commit instead.
