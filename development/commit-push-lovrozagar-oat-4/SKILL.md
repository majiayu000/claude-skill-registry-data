---
name: commit-push
description: >
  Commit with a Conventional Commits subject, then push. Use for /commit-push,
  "commit and push", "commit this and push". Must push. Never force-push.
---

Inspect `git status` + `git diff` (staged and unstaged) before the message.

Diff pass on the hunks you will stage: delete narrating comments, unused defensive guards or try/catch on trusted paths, `any` casts that only silence types, dead compatibility, and unrelated hunks. Keep a comment only when it states a constraint the code cannot encode. Keep behavior otherwise. Do not spawn a reviewer.

Stage only user intent. Never blind `git add -A` / `git add .`. Split unrelated concerns into multiple commits.

If a unique in-progress file exists under `.tmp/grunt/implementations/`, its `## Files` is the default stage set. Still inspect `git status`.

Message = Conventional Commits **subject only**: `type(scope): subject` (scope optional).

Types: feat fix docs style refactor perf test build ci chore revert.

Subject: imperative lowercase no trailing period.

NO body. NO footer. NO `Co-Authored-By`. NO `Generated with`. NO 🤖. NO trailers. No AI attribution. Work belongs to the human.

Must `git push`. Do not load /commit. Ignore never-push.

## Branch

Current: `git rev-parse --abbrev-ref HEAD`

Default: `git symbolic-ref --quiet --short refs/remotes/origin/HEAD` (strip `origin/`). If that fails: ask. Never invent default.

Recent (frozen flags; do not change):

```
git reflog -n 30
git for-each-ref --count=8 --sort=-committerdate --format='%(refname:short) %(committerdate:unix)' refs/heads
```

Recent = unique existing non-default names from those two outputs whose `committerdate` unix is ≤7d (`now - 604800`). Never invent branch names. Unknown/ambiguous names → drop them, do not guess.

| state | action |
| current ≠ default | push current |
| default AND 0 recent | push default |
| default AND exactly 1 recent exists | `git checkout` that name; push it |
| else | ask; do not push yet |

No upstream (`git rev-parse --abbrev-ref @{upstream}` fails): `git push -u origin <branch>`. Else `git push`.

Never force-push. Never `--force`, `-f`, `--force-with-lease`, `+<branch>`.

Protocol: `.rulesync/reference/cascade.md`. Do not paste cascade.
