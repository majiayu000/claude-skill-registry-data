---
name: hub-spoke
description: >
  Implement a central Coordinator (Hub) that manages, distributes, and merges tasks
  performed by specialized worker sessions (Spokes). Spokes communicate only with the Hub
  and not with each other. Useful for ad-hoc project management and complex workflow distribution.
  Triggers: "허브 스포크", "중앙 통제", "작업 배분", "hub and spoke", "coordinator pattern", "centralized workflow".
---

# Hub-and-Spoke

The Hub-and-Spoke pattern designates a central Coordinator session (Hub) to manage planning, task distribution, progress checking, and final result merging. The Worker sessions (Spokes) execute their specific assignments independently and communicate only with the Hub.

## 5-Stage Workflow

```
         ┌───────────────┐
         │  Coordinator  │ ◄── Planning, task queue, and spoke bridging
         └───────┬───────┘
       ┌─────────┼─────────┐
       ▼         ▼         ▼
    Worker    Worker    Worker
     (A)       (B)       (C)
```

1. **Role Definition**: Spawn a dedicated Coordinator session (Hub) and define specialized Spoke Worker configs.
2. **Task Planning**: The Hub analyzes the goal, creates a task dependency list, and allocates work.
3. **Execution Routing**:
   - Before spawning, inspect `agent__listAgents(type="sessions")` for an Idle child with the same assistant ID and a compatible workspace contract. Route new work to a suitable child with `agent__messageToSession`; use `reset=true` only when its previous conversation and runtime state should be discarded.
   - The Hub spawns a new Spoke asynchronously using `agent__spawnSession(waitForResult=false)` only when no suitable child exists, a different role or workspace isolation is needed, or another parallel capacity slot is required.
   - Plain spokes get **isolated** workspaces by default. For repo/code work, pass `workspaceOverride` to the Hub's workspace (or a spoke-specific subdir). For research/write-ups, require the primary deliverable in the spoke's final text (`Result:`), not only a relative file path.
   - When sharing a workspace across parallel spokes, use unique filenames or per-spoke subdirectories to avoid collisions.
   - If inter-spoke coordination is needed, the Hub routes messages. See [routing.md](references/routing.md).
4. **Monitoring**: The Hub polls Spoke statuses via `agent__checkSession` and reads the Metadata `workspace` line (`SHARED` vs `ISOLATED`) before assuming files exist in the Hub root.
5. **Synthesis**: The Hub merges all finished spoke artifacts from Result text (and `agent__messageToSession` follow-ups when needed). For `ISOLATED` spokes, do not attempt parent `workspace__readFile` on the child Metadata path — ask the spoke for contents or require the deliverable in Result text. For `SHARED` spokes, relative paths in the Hub root are safe.

## 🛠️ MCP Tools Guide

- **Session Reuse**: Match on `assistantId`, status, and workspace compatibility before creating a Spoke. A reset reuses the session's identity and workspace files but closes its browser session; do not reuse a child whose prior workspace or runtime state is incompatible.
- **Context Management**: Do not let the Hub read all conversation logs from all Spokes to prevent context overflow. Instruct the Hub to only request **summarized status reports and file list results**.
- **Message Bridging**: If Worker B depends on Worker A's output, the Hub collects the artifact details from A and injects them to B via `agent__messageToSession`.

## References

- [Routing patterns](references/routing.md)
- [Status polling](references/status-polling.md)
- [Context budget](references/context-budget.md)
