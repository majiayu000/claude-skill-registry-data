---
name: clawflow
description: >
  Protocol for multi-agent collaboration via OpenClaw's message-passing and recursive
  task DAGs. Use this skill whenever the user wants to coordinate work across multiple
  OpenClaw agents, decompose complex tasks into subtasks with dependencies, or build
  any kind of multi-agent pipeline. Also trigger when the user mentions "agent
  orchestration", "task DAG", "multi-agent", "dispatch", "agent pipeline", "delegate
  tasks", "agent collaboration", or wants to break a project into parallelisable steps
  handled by different agents. Use it even if the user just says "I need multiple
  agents to work together."
---

# Clawflow

A protocol for OpenClaw agents collaborating through messages and recursive task DAGs.

**Mental model**: Think of a consulting firm. Anyone can receive a project. If they can
do it alone, they do. If it's too big, they break it into pieces, hand each piece to a
colleague, collect the results, and synthesise. Those colleagues might do the same.
There are no fixed "managers" and "workers." Every agent speaks the same protocol.

## When to Read References

- Message formats, task file structure, status codes → `references/schemas.md`
- The decision loop every agent runs → `references/agent-loop.md`
- DAG decomposition, context passing, synthesis → `references/coordinating.md`

---

## Core Principles

1. **One protocol, fluid roles** — every agent is structurally identical. Any agent can
   execute work directly *or* decompose and delegate. The role emerges from the task.
2. **OpenClaw is the backbone** — agent identity comes from `openclaw.json` config,
   peer discovery from `openclaw agents list`, and message transport from
   `openclaw agent --agent <id> --message "..."`. No custom identity or peer files.
3. **Recursive DAGs** — an agent that delegates becomes a coordinator for that sub-DAG.
   Its parent doesn't know or care. DAGs nest naturally.
4. **Workspace = working memory** — each agent's OpenClaw workspace is its private
   scratchpad. Task state lives in workspace files. No agent reads another's workspace.

---

## How It Works

```
Agent A receives a task
  → Can I do this alone?
     YES → Execute, reply with results
     NO  → Decompose into sub-DAG
           → Dispatch subtasks to Agents B, C via openclaw agent
           → Agent B receives its subtask
              → Can I do this alone?
                 YES → Execute, reply to A
                 NO  → Decompose further, dispatch to D, E...
           → Agent C executes, replies to A
           → A collects all replies, synthesises, replies to *its* parent
```

Every level looks the same. An agent at any depth follows the same loop.

---

## Integration with OpenClaw

### Agent Identity

Comes from the OpenClaw configuration. Do NOT create custom identity files.

- **Config source**: `openclaw.json` → `agents.list[].id`, `agents.list[].identity`
- **Workspace source**: `IDENTITY.md` in the agent's workspace root
- **Read with**: `openclaw agents list` or from injected bootstrap context

Each agent already knows who it is — its `id`, `name`, `emoji`, and `theme` are
injected into the session context on every turn via the workspace bootstrap files
(`IDENTITY.md`, `SOUL.md`, `AGENTS.md`).

### Peer Discovery

Discover available agents from OpenClaw configuration. Do NOT maintain a separate
peers file.

```bash
# List all configured agents
openclaw agents list

# The config defines them:
# agents.list[].id        → agent identifier (used in --agent flag)
# agents.list[].workspace → their workspace path
# agents.list[].model     → their model
```

An agent's `subagents.allowAgents` config controls which agents it can delegate to.
`["*"]` means it can reach any agent.

### Sending Tasks to Peers

Use the OpenClaw CLI to send a task message to another agent:

```bash
# Send a task to a specific agent
openclaw agent --agent data-extractor --message "Extract Q3 sales from sales.csv"

# The receiving agent gets this in its session, processes it,
# and the response comes back through the same mechanism
```

For structured task dispatch with metadata, write the task message to a file and
reference it:

```bash
openclaw agent --agent data-extractor \
  --message "$(cat workspace/tasks/task-abc/dispatch-st-extract.md)"
```

### Workspace Layout for Clawflow

Each agent uses its existing OpenClaw workspace. Clawflow adds a `tasks/` directory:

```
<agent-workspace>/                   ← OpenClaw workspace root
  IDENTITY.md                        ← Agent identity (OpenClaw-managed)
  AGENTS.md                          ← Operating instructions (OpenClaw-managed)
  SOUL.md                            ← Persona (OpenClaw-managed)
  mailbox/                           ← Agent-level message log (all tasks)
    inbox/                           ← Incoming messages before processing
    outbox/                          ← Outgoing messages (dispatches + replies sent)
    archive/                         ← Processed messages (durable audit trail)
  tasks/                             ← Clawflow working directory
    {task-id}/
      task.md                        ← DAG definition + progress + results
  skills/
    clawflow/                        ← This skill
      SKILL.md
      ...
```

Clawflow adds two top-level directories to the workspace:

- **`mailbox/`** — agent-level message log, independent of any task. Every message
  the agent sends or receives is logged here. `inbox/` holds unprocessed arrivals,
  `outbox/` logs what was sent, `archive/` holds processed messages. This is the
  durable audit trail — OpenClaw session history compacts over time, the mailbox doesn't.
- **`tasks/`** — one subdirectory per task with a `task.md` tracking DAG state, subtask
  results, and the final synthesised output.

---

## The Agent Loop

When an agent receives a task (via `openclaw agent --message`):

```
1. Parse the message
2. Is it a TASK from a parent?
   → Create task.md in workspace/tasks/{task-id}/
   → DECIDE: execute directly or decompose?
     → Direct: do the work, reply with results
     → Decompose: build sub-DAG in task.md, dispatch subtasks via openclaw agent
3. Is it a REPLY from a peer I delegated to?
   → Update sub-DAG in task.md (mark subtask done, store results)
   → Dispatch any newly unblocked subtasks
   → If all subtasks done → synthesise results, reply to parent
```

Read `references/agent-loop.md` for the full decision logic and edge cases.

---

## Delegation Decision

When an agent receives a task, it decides: do it myself or delegate?

**Execute directly when:**
- The task is within the agent's own capabilities
- It's simple enough that decomposition adds overhead
- No relevant peer agents are configured

**Decompose and delegate when:**
- The task requires capabilities the agent doesn't have
- The task has naturally parallel parts
- The task is large enough that breaking it up reduces complexity

This is a judgment call. The protocol doesn't force it — the agent decides.

---

## DAG Dependency Resolution

When coordinating a sub-DAG, the agent tracks subtask status in `task.md`:

```python
def get_ready_subtasks(dag):
    """Subtasks whose dependencies are all done and haven't been dispatched yet."""
    return [
        sid for sid, st in dag.subtasks.items()
        if st.status == 'pending'
        and all(dag.subtasks[dep].status == 'done' for dep in st.depends_on)
    ]
```

Called after every reply. Newly unblocked subtasks get dispatched immediately.

---

## Error Handling (V1)

Fail-fast. No retries, no partial recovery.

| Scenario | Behaviour |
|---|---|
| Peer fails a subtask | Agent marks its own task failed, replies with error to parent |
| Duplicate message | Idempotency check — skip if task already in-progress or done |
| Agent crashes | Task file in workspace preserves state; restart resumes from task.md |

Errors propagate upward. Future versions will add retry and partial recovery.

---

## Implementation Checklist

1. **Verify agent configuration** — `openclaw agents list` to see available agents.
2. **Check subagent permissions** — ensure `subagents.allowAgents` includes target agents.
3. **Implement the agent loop** — follow `references/agent-loop.md`.
4. **Use message templates** — `scripts/message.py` generates structured task/reply messages.
5. **Test a 2-level chain** — agent A delegates to B, B executes and replies.
6. **Test fan-out** — agent A delegates to B and C in parallel.
7. **Test recursion** — agent A → B → C.

---

## Out of Scope (V1)

- Large result attachments (Google Drive layer)
- Task retry / partial DAG recovery
- Agent health checks
- Progress streaming
- Cross-agent workspace access (by design, forever)
