---
name: subagent-safety
description: Decide which work is safe to delegate to worker agents. Use before delegating tasks that may require user interaction, approval, authentication, external writes, or shared-state mutation.
user-invocable: false
---

## Delegation Boundary

Worker agents may be unable to surface approval prompts, authentication failures, or
user questions to the active conversation. Delegate bounded work that can complete
without those interactions.

**Generally safe to delegate:**

- Code reading, file searching, analysis, and review
- Focused documentation lookup
- Local edits within an explicitly assigned worktree and file scope
- Builds and tests whose dependencies and permissions are already available
- Read-only external queries after the conversation-owning agent has verified access

**Keep with the conversation-owning agent:**

- Questions or decisions that require the user
- Approval or escalation requests
- Authentication setup and recovery
- Push, fetch, pull, PR creation, ticket changes, comment replies, and other external
  mutations unless the client explicitly supports delegated authorization
- Operations that mutate shared branches, shared worktrees, or global configuration
- Any task whose likely failure can only be resolved interactively

Before delegating an authenticated read, verify access in the current session. Give
the worker an exact objective, owned paths, allowed side effects, required output, and
a stopping condition.

## Client Notes

### Claude Code

`AskUserQuestion` is main-agent-only. Claude Code subagents can silently stall on
permission or authentication prompts, so keep mutating `gh` commands and authenticated
git operations with the main agent. In the cenci-sandbox container,
skip-permissions removes permission prompts but does not remove authentication or
user-interaction failures.

Claude Code 1M-context sessions can reject `Task` delegation when subagents are not
pinned to a 200K model. cenci configures
`CLAUDE_CODE_SUBAGENT_MODEL=claude-sonnet-5` as an optional workaround. Do not infer
or announce the active model/context size. If delegation fails with the documented
usage-credit error, tell the user to run `/cenci:configure` and restart, or use a
standard-context session.

### Codex

Use Codex worker/subagent tools only for concrete, bounded tasks that can run
independently. Keep user-input tools and escalation in the root conversation. Do not
assume a connector authorized in the root agent can be mutated safely by a worker;
prefer read-only connector work unless the delegated tool contract explicitly
guarantees authorization and error delivery.
