---
name: sync-pending-approvals
description: Code recipes and explanation for synchronizing Rust backend pending tool approvals (YOLO mode/manual approval) to the frontend React UI when a user resumes or opens an existing agent session. Use this skill when modifying the AgentSession state to maintain approval channels or when fixing UI bugs related to missing pending tool executions upon page reload/session switch.
---

# Sync Pending Approvals

This skill is designed to solve a synchronization issue where an agent spawns a tool requiring user approval, but the user switches away from the session in the UI, or the UI is reloaded. Because the approval request was sent while the session was not active in the UI, the frontend misses the event, and the backend blocks indefinitely waiting for the `oneshot::channel` response.

## Problem Context

When subagent sessions (or inactive sessions) require tool approval:

1. Rust backend emits a `ToolExecutionRequiresApproval` event and awaits a `oneshot` channel response.
2. The UI (`AgentSessionContext.tsx`) filters out events for inactive sessions.
3. The background task deadlocks.

## The Solution

To solve this, we must cache the approval details in the Rust session state and re-emit the event when the frontend resumes the session.

### 1. Update `AgentSession` State

Currently, `pending_approvals` only stores the `Sender<bool>`. It needs the context (`tool_name` and `arguments`) to recreate the event.

See [rust-state-changes.md](references/rust-state-changes.md) for the exact code modifications required for `AgentSession` and `ToolExecutionStarted`.

### 2. Re-emit Events on Session Resume

When the frontend explicitly opens a session, it calls `agent_resume_session`. We must hook into this phase to read the `pending_approvals` map and fire the events again.

See [rust-resume-logic.md](references/rust-resume-logic.md) for the exact code modifications.

### 3. Frontend Deduplication

The frontend needs to ensure that if these events fire again, they don't create duplicate entries in the pending list.

See [frontend-dedup.md](references/frontend-dedup.md) for the required changes.

---

### Instructions for the Agent applying this skill

1. Locate `AgentSession` struct definition (usually in `src-tauri/src/agent/state.rs` or similar). Apply the new struct and update all initialization sites.
2. Update the tool execution loop (`src-tauri/src/agent/llm/tool_execution.rs`) to store the struct instead of just the sender.
3. Update `src-tauri/src/commands/agent_commands.rs` (specifically the `agent_resume_session` handler) to re-emit the events.
4. Update `src/context/AgentSessionContext.tsx` to handle deduplicate insertions into the pending array.
5. Compile and test that the tool approval modal correctly appears when switching back to a session that was waiting for approval.
