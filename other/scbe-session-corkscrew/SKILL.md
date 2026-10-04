---
name: scbe-session-corkscrew
description: Manage SCBE multi-agent session continuity with timestamped callsigns, append-only cross-talk packets, Obsidian handoffs, and verification roll-forward. Use when starting or rotating an agent session, sending AI-to-AI updates, acknowledging packets, marking work verified or retired, or stabilizing coordination across repo bus and Obsidian.
---

# SCBE Session Corkscrew

Use this skill to keep multi-agent work traceable and non-destructive across both lanes:
- machine lane: repo packet bus
- human lane: Obsidian Cross Talk + Sessions

## Workflow

1. Start or rotate a session.
2. Emit append-only cross-talk packets as work progresses.
3. Mirror key packets to Obsidian for human readability.
4. Mark session status as `verified` when deliverables are validated.
5. Optionally mark old sessions as `retired` and keep spiraling forward.

## Commands

Run from `C:\Users\issda\SCBE-AETHERMOORE`.

### Start a new session (new codename + session id)
```powershell
powershell -ExecutionPolicy Bypass -File scripts/system/terminal_crosstalk_emit.ps1 `
  -NewSession `
  -TaskId "SESSION-START" `
  -Summary "Session kickoff" `
  -Where "terminal:pwsh" `
  -Why "coordinate multi-agent work" `
  -How "append-only packet bus + Obsidian mirror"
```

### Continue existing session (reuse saved state)
```powershell
powershell -ExecutionPolicy Bypass -File scripts/system/terminal_crosstalk_emit.ps1 `
  -TaskId "NEXT-TASK" `
  -Summary "Progress update" `
  -NextAction "handoff to agent.claude"
```

### Explicit session sign-on (callsign + timestamped tracker)
```powershell
powershell -ExecutionPolicy Bypass -File scripts/system/session_signon.ps1 `
  -Agent "Codex" `
  -Callsign "Helix Warden" `
  -Status active `
  -Summary "Session start"
```

### Mark session verified after validated work
```powershell
powershell -ExecutionPolicy Bypass -File scripts/system/session_signon.ps1 `
  -Agent "Codex" `
  -Callsign "Helix Warden" `
  -SessionId "<same-session-id>" `
  -Status verified `
  -Summary "Deliverables validated"
```

### Mark old session retired
```powershell
powershell -ExecutionPolicy Bypass -File scripts/system/session_signon.ps1 `
  -Agent "Codex" `
  -Callsign "Helix Warden" `
  -SessionId "<old-session-id>" `
  -Status retired `
  -Summary "Superseded by newer verified session"
```

## Required Fields For Every Packet

Include these fields in every major handoff:
- `task_id`
- `status`
- `summary`
- `next_action`
- `risk`
- `proof`
- `session_id`
- `codename`
- `where`
- `why`
- `how`

## Files This Skill Maintains

- `artifacts/agent_comm/github_lanes/cross_talk.jsonl`
- `artifacts/agent_comm/session_signons.jsonl`
- `notes/session_signons.md`
- `AI Workspace/Cross Talk.md`
- `AI Workspace/Sessions/*.md`

## Operating Rules

- Keep all logging append-only.
- Never overwrite old packets.
- Reuse the same `session_id` until you intentionally rotate.
- Use `-NewSession` only when starting a new session lane.
- Mark `verified` only after tests, review, or evidence validation.
- Keep summaries short, concrete, and action-oriented.

## Reference

Load [references/commands.md](references/commands.md) for minimal command templates.
