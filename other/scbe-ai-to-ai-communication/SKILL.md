---
name: scbe-ai-to-ai-communication
description: Standardize AI-to-AI coordination messages and exchange protocols across Codex, Claude, and other autonomous agents through Obsidian cross-talk and shared JSON packets.
---

# SCBE AI-to-AI Communication

Use this skill when multiple AI agents need reliable handoff, status updates, or synchronized execution.

## Use Cases
- Cross-agent task handoffs (Codex ↔ Claude).
- Sharing implementation state, blockers, and proof artifacts.
- Logging autonomous agent status in Obsidian without losing continuity.

## Message Standard
Create one JSON packet per handoff using the shared envelope:

```json
{
  "packet_id": "aid-20260301-0001",
  "created_at": "2026-03-01T14:20:00Z",
  "sender": "codex",
  "recipient": "claude",
  "intent": "handoff",
  "status": "in_progress|blocked|done",
  "repo": "SCBE-AETHERMOORE",
  "branch": "clean-sync",
  "task_id": "B1-HB",
  "summary": "short description",
  "proof": [
    "command output",
    "path/to/artifact"
  ],
  "next_action": "what to do next",
  "risk": "low|medium|high",
  "gates": {
    "governance_packet": true,
    "tests_requested": ["python -m pytest ..."]
  }
}
```

## Quick Operational Loop
1. Write/append short status in:
   - `notes/_context.md`
   - `agents/codex.md`
   - `notes/_inbox.md`
2. If a task starts or changes state, add a line to `notes/open_tasks_20260301_parallel.md`.
3. Store machine-readable packet files in:
   - `artifacts/agent_comm/<YYYYMMDD>/<packet-id>.json` (deterministic by date)
4. Keep packets small, evidence-first, and include file paths for every claim.

## Canonical Naming
- Keep packet IDs deterministic and grep-friendly:
  - `b1-hb-status-YYYYMMDD-HHMMSS`
  - `cross-talk-<agent>-<topic>-YYYYMMDD`

## Script (Optional)
- `scripts/emit_ai_comm_packet.py` (repo-local): generates the envelope and writes to `artifacts/agent_comm/`.

## Safety Rules
- Never include raw secrets, API keys, or `.env` contents.
- Include references to sensitive gates (`DQUAR/ALLOW/DENY`) as text, not raw payload data.
- If blocked, route through `_inbox.md` first with risk reason and impact before editing shared files.

## Notes
This is a lightweight communication layer for autonomous coordination. It is not a security boundary by itself.
