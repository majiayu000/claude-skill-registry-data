---
name: scbe-claude-crosstalk-workflow
description: "Use when two AI lanes (Codex and Claude) work in parallel and need deterministic handoff packets with session IDs, lane-bus appends, and repairable delivery checks."
---

# SCBE Claude Cross-Talk Workflow

Use this skill when two AI lanes (especially Codex and Claude) are working in parallel and you need deterministic handoff packets that can be audited and repaired.

## When To Use

- Starting a new coordinated Codex/Claude work session.
- Posting task updates, blockers, or handoffs without losing session identity.
- Verifying packet delivery across:
  - `artifacts/agent_comm/<day>/*.json`
  - `artifacts/agent_comm/github_lanes/cross_talk.jsonl`
  - `notes/_inbox.md`

## Workflow

1. Emit a packet (new session or existing session)

```powershell
& "C:/Users/issda/.codex/skills/scbe-claude-crosstalk-workflow/scripts/emit_crosstalk_packet.ps1" `
  -RepoRoot "C:/Users/issda/SCBE-AETHERMOORE" `
  -NewSession `
  -Sender "agent.codex" `
  -Recipient "agent.claude" `
  -TaskId "CROSSTALK-SESSION-START" `
  -Summary "Session started for shared workflow" `
  -Status "in_progress" `
  -NextAction "Claude ACK and claim first lane" `
  -Where "terminal" `
  -Why "avoid dual-writer collisions" `
  -How "append-only packet + lane bus"
```

2. Emit updates during work (same session)

```powershell
& "C:/Users/issda/.codex/skills/scbe-claude-crosstalk-workflow/scripts/emit_crosstalk_packet.ps1" `
  -RepoRoot "C:/Users/issda/SCBE-AETHERMOORE" `
  -Sender "agent.codex" `
  -Recipient "agent.claude" `
  -TaskId "CROSSTALK-WORK-UPDATE" `
  -Summary "Implemented change packet" `
  -Status "in_progress" `
  -NextAction "Claude verify and continue"
```

3. Verify and optionally repair mirrors

```powershell
python "C:/Users/issda/.codex/skills/scbe-claude-crosstalk-workflow/scripts/crosstalk_skill_audit.py" `
  --repo-root "C:/Users/issda/SCBE-AETHERMOORE"
```

```powershell
python "C:/Users/issda/.codex/skills/scbe-claude-crosstalk-workflow/scripts/crosstalk_skill_audit.py" `
  --repo-root "C:/Users/issda/SCBE-AETHERMOORE" --repair
```

## Guardrails

- Never include secrets or tokens in `Summary`, `NextAction`, `Why`, or `How`.
- Use append-only flow. Do not edit prior packet files.
- Use `status=blocked` instead of silent failure.
- Keep `TaskId` stable for a task lifecycle; change it only for a new unit of work.

## Resources

- `scripts/emit_crosstalk_packet.ps1`: session-aware packet emitter for Codex/Claude lanes.
- `scripts/crosstalk_skill_audit.py`: audit + optional repair for packet, lane bus, and notes mirror parity.
- `references/packet_schema.md`: packet field contract and status vocabulary.
