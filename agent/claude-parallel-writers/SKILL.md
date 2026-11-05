---
name: claude-parallel-writers
description: run parallel claude code writers, such as PR owners or dependency workers, as desktop sessions in their own worktrees, with sub-agents as the fallback
disable-model-invocation: true
---

how a claude code orchestrator runs parallel writers, such as PR owners or dependency workers, each in its own worktree. codex does not use this skill: it runs parallel writers as new threads

- the app refuses `start_session` in any turn the user's own message didn't start, including turns a writer's message or note wakes. so start every writer your calling skill plans in the turn that invoked it
- `start_session` with `initiation: "user_asked"`, `use_worktree: true` and a short `name`
- a session's worktree can start from a stale local branch, so each prompt names the writer's base and tells it to reset its new branch to the freshly fetched base before it starts
- add your session id from `get_session` with `self` to each prompt, and tell the writer to send its result there with `SendMessage` before it ends its turn. the app's notes on writers' turns arrive only once every writer is idle and quote 400 characters, so read them as session status, never as results
- follow up with `SendMessage` to the writer's `local_…` session id
- for a writer that comes up later, or when `start_session` fails, use the first that works:
  1. `start_session` as above, in a turn the user's message started
  2. a writer session you started whose work has merged: send it the new task with its prompt values, and tell it to switch its worktree to a new branch from the freshly fetched base before it starts
  3. a sub-agent: read and follow [sub-agents.md](sub-agents.md)

complete when every planned writer has a session or a sub-agent, apart from writers your calling skill defers
