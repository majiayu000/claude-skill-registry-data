---
name: commit-push-release
description: >
  Commit, push, bump package.json, tag vX.Y.Z, push the tag. CI publishes. Use
  for /commit-push-release, "commit push release", "release". Must push. Never
  force-push. No npm/gh publish.
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

## Release

Ask if off default, or patch/minor/major is unclear. Do not guess semver. Do not tag until answered.

On default + clear bump:

1. Set `package.json` `version` to `X.Y.Z` (keep lockfile in sync if it records version).
2. Commit the bump with the same subject rules (`chore(release): vX.Y.Z` unless the user gave a subject).
3. Push the branch per **Branch**.
4. `git tag vX.Y.Z` then `git push origin vX.Y.Z`.

Do not `npm publish`. Do not `npm pack` as publish. Do not `gh release create`. CI publishes from the tag.

Retag only if asked. Unprompted: never `git tag -f`, never delete a tag, never force-push a tag. If asked to retag: move that tag only; still never force-push a branch.

Protocol: `.rulesync/reference/cascade.md`. Do not paste cascade.
