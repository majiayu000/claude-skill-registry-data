---
name: commit
description: >
  Inspect the diff and commit with a Conventional Commits subject line. Use for
  /commit, "commit this", "commit these changes". Never git push.
---

Inspect `git status` + `git diff` (staged and unstaged) before the message.

Diff pass on the hunks you will stage: delete narrating comments, unused defensive guards or try/catch on trusted paths, `any` casts that only silence types, dead compatibility, and unrelated hunks. Keep a comment only when it states a constraint the code cannot encode. Keep behavior otherwise. Do not spawn a reviewer.

Stage only user intent. Never blind `git add -A` / `git add .`. Split unrelated concerns into multiple commits.

If a unique in-progress file exists under `.tmp/grunt/implementations/`, its `## Files` is the default stage set. Still inspect `git status`.

Message = Conventional Commits **subject only**: `type(scope): subject` (scope optional).

Types: feat fix docs style refactor perf test build ci chore revert.

Subject: imperative lowercase no trailing period.

NO body. NO footer. NO `Co-Authored-By`. NO `Generated with`. NO 🤖. NO trailers. No AI attribution. Work belongs to the human.

Never git push. Never `git push`. This skill never pushes.

Protocol: `.rulesync/reference/cascade.md`. Do not paste.
