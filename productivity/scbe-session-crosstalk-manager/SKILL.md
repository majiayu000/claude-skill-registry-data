---
name: scbe-session-crosstalk-manager
description: Manage SCBE terminal cross-talk sessions with collision-safe logs, persistent codenames, session IDs, and where/why/how metadata across repo packet lanes and Obsidian handoff notes. Use when starting a new AI work session, posting updates, handing off work, verifying lane sync, or closing a session.
---

# SCBE Session Cross-Talk Manager

Run session operations through the terminal wrapper so machine logs and Obsidian logs stay in lockstep.

## Core Commands

1. Start a new session (new `session_id` + codename).

```powershell
& C:/Users/issda/SCBE-AETHERMOORE/scripts/system/terminal_crosstalk_emit.ps1 -NewSession -TaskId "SESSION-START" -Summary "Session kickoff" -Status "in_progress" -Where "terminal:pwsh" -Why "coordinate multi-agent execution" -How "append-only packets + Obsidian mirrors" -Recipient "agent.claude"
```

2. Post an in-session update (reuses saved `session_id` and codename).

```powershell
& C:/Users/issda/SCBE-AETHERMOORE/scripts/system/terminal_crosstalk_emit.ps1 -TaskId "WORK-UPDATE" -Summary "Implemented workflow bridge update" -NextAction "agent.claude ACK and pick next task" -Status "in_progress" -Where "repo:SCBE-AETHERMOORE" -Why "keep lanes synchronized" -How "gateway packet + cross_talk_append"
```

3. Post a blocked update.

```powershell
& C:/Users/issda/SCBE-AETHERMOORE/scripts/system/terminal_crosstalk_emit.ps1 -TaskId "WORK-BLOCKED" -Summary "Blocked on missing API key" -NextAction "configure required key then retry" -Status "blocked" -Risk "medium" -Where "runtime:local" -Why "provider unavailable" -How "fail-closed packet escalation"
```

4. Close a task/handoff.

```powershell
& C:/Users/issda/SCBE-AETHERMOORE/scripts/system/terminal_crosstalk_emit.ps1 -TaskId "WORK-DONE" -Summary "Completed and verified" -NextAction "none" -Status "done" -Where "repo+vault" -Why "task complete" -How "proof paths logged"
```

## Verification Gate (Run After Each Critical Update)

```powershell
$day=(Get-Date).ToUniversalTime().ToString('yyyyMMdd'); Get-Content "C:/Users/issda/SCBE-AETHERMOORE/artifacts/agent_comm/github_lanes/cross_talk.jsonl" -Tail 5; Get-Content "C:/Users/issda/SCBE-AETHERMOORE/notes/_inbox.md" -Tail 5; Get-ChildItem "C:/Users/issda/OneDrive/Documents/DOCCUMENTS/A follder/AI Workspace/Sessions" | Sort-Object LastWriteTime -Descending | Select-Object -First 3 FullName,LastWriteTime
```

Success criteria:
- Latest packet appears in `cross_talk.jsonl`.
- Human mirror line appears in `notes/_inbox.md`.
- New Obsidian session handoff file exists in `AI Workspace/Sessions`.

## Session Identity Rules

- Use one codename per session unless intentionally rotated.
- Use `-NewSession` exactly once at session start (or when intentionally rotating).
- Include `where`, `why`, and `how` on meaningful updates.
- Keep `Summary` short and factual; put action in `NextAction`.

## Guardrails

- Never include secrets, raw tokens, or `.env` values in packets.
- Use `blocked` status instead of silent failures.
- Do not overwrite prior notes; rely on append-only packet and session logs.
- Keep packet evidence in `proof` paths when possible.
