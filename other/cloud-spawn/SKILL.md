---
name: cloud-spawn
description: "Cloud-only: spawn a worker/probe cloud session with an admissible brief and report channel."
version: 1.0.0
allowed-tools: ["Read", "Bash", "ToolSearch"]
---

# Cloud Spawn — a Worker Session From a Cloud EM

Cloud-only. A cloud EM starts another cloud session with `create_session` (claude-code-remote
MCP). That call works in auto mode. What the classifier refuses is the **brief**: a prompt telling
the child to create triggers aimed at the parent, publish artifacts, or push speculative branches
reads as an external write, and the whole spawn is denied. Tripwire:
`A-SPAWN-BRIEF-THAT-ASKS-FOR-SIDE-CHANNELS-IS-REFUSED-WHOLE`.

Children sit behind the same egress proxy: they add build throughput, never publish capability
(binary release uploads are refused from cloud). Don't spawn children for publish-bound work.

## Spawn it

1. **Pick the creation source by the work, never by the tooling.** `source_url` is the child's
   only work-repo slot: a session created from one repo cannot attach another with push access in
   auto mode. Name the repo the child must write to. The coordinator plugin and engine arrive on
   every source; project-rag's red-carpet install is tracked as its own work, so don't pick
   project-rag as the source just to get its tools.
2. **Omit `environment_id`** so the child inherits this environment.
3. **Write a narrow brief:**
   - Name the parent (`CLAUDE_CODE_REMOTE_SESSION_ID`) and state the one question.
   - List reads, not writes: shell probes, `ToolSearch`, `get_session`, `ListAgents`, `read_documentation`.
   - Name exactly **one** report write: a single comment on this EM's channel PR (`coordinator:cloud-channel`).
   - Mark untested items UNTESTED and stop.
   - Leave out trigger creation, artifact publishing, extra branches and `add_repo` grants. If a
     capability needs one of those tested, ask the user for that one first.
4. **Wait for the comment.** The channel PR's subscription wakes this EM when the child posts. Never
   poll `get_session` on a timer; read it only when the comment is overdue by a real signal.

## Why a PR comment on the source repo is the channel

A cloud child cannot reach its parent through `ListAgents` or `SendMessage`, because each runs in a
separate container. The child can read the parent with `get_session`, but it cannot write to it.
What the child can write to is a PR comment, and only on a repo in its GitHub scope. That scope is
its creation source, plus anything attached with `add_repo`. So the parent's channel PR must live
on the child's source repo; a shared comms repo outside that scope is unreachable.
`coordinator:cloud-channel` makes the PR and subscribes to it.

A child's own subagents have no `Workflow` tool, so fan-out stays with a top-level session.
