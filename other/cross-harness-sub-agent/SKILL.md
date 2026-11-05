---
name: cross-harness-sub-agent
description: spawn a cross harness sub-agent
---

## route

- from codex, follow [claude-subagent.md](claude-subagent.md)
- from claude code, follow [codex-subagent.md](codex-subagent.md)
- from another harness, try claude code first, fallback to codex if it failed
- the calling agent invokes the selected route directly
- an explicit user target, model or effort wins
- never use this for same harness sub-agents

## checkout

`<checkout>` is an absolute path you reuse literally in every later command:

- current checkout: the output of `git rev-parse --show-toplevel`
- separate worktree: the last output line of `bin/wt-run HEAD -- pwd`

max 1 writer per checkout

## task

give the sub-agent a self-contained prompt with the objective, scope, completion condition, edit permission and any context it can't discover

require the sub-agent to read `~/.agents/AGENTS.md` when present and applicable repository/project `AGENTS.md` before starting

unless the user gives another review scope, compare the current branch with `origin/develop` and include committed branch changes plus staged, unstaged and untracked changes

for an exact-SHA read-only review, stop once the evidence supports a verdict; require the final report to include the reviewed SHA, compact read-only verification evidence, and either concrete `file:line` findings with the smallest remedy or a verdict line containing exactly `NO_ISSUES_FOUND`

for read-only reviews, require the report as the final response; the launcher persists it, so the reviewer needs no file writes

require no further cross-harness delegation, and a token-efficient verification command for you to run

for a direct cli route, pick a short unique `<slug>` and write the exact task with the file-writing tool to `<checkout>/playground/cross-harness/<slug>-prompt.md` (`<prompt-file>`). create its parent directory in a separate call. retain `<checkout>`, `<slug>` and `<prompt-file>` until completion; files under `playground/` stay out of git

## misc

read [troubleshooting.md](troubleshooting.md) if something goes wrong
