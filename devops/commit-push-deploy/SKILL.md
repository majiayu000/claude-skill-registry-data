---
name: commit-push-deploy
description: >
  Commit, push, then deploy only if allowlisted infra already exists. Use for
  /commit-push-deploy, "commit push deploy", "deploy this". Must push. Never
  force-push. Never invent infra.
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

## Deploy

After push. Detect **existing** repo-root (or listed) paths only — never create them:

`fly.toml` `vercel.json` `netlify.toml` `wrangler.toml` `wrangler.jsonc` `railway.toml` `railway.json` `render.yaml` `render.yml` `app.yaml` `Dockerfile` `docker-compose.yml` `docker-compose.yaml` `samconfig.toml` `serverless.yml` `serverless.yaml` `Pulumi.yaml` `terraform/` `.do/app.yaml`

This repo (`package.json` `name` `@lovrozagar/grunt`): skip deploy. Stop after push.

No allowlist hit: skip. Never invent infra, hosts, workflows, or config.

Hit: run only a deploy command already documented in-repo (scripts/CI/README). Do not guess a provider. Do not add files.

Protocol: `.rulesync/reference/cascade.md`. Do not paste cascade.
