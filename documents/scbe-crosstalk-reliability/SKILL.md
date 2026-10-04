---
name: scbe-crosstalk-reliability
description: Audit and repair SCBE cross-talk packet delivery across JSON packets, JSONL lane bus, and markdown mirrors.
---

# SCBE Cross-Talk Reliability

Use this skill when packet delivery feels inconsistent across agents or mirrors.

## Reliability surfaces
1. `artifacts/agent_comm/<day>/*.json`
2. `artifacts/agent_comm/github_lanes/cross_talk.jsonl`
3. `notes/_inbox.md`
4. `notes/_context.md`
5. `agents/codex.md`

## Commands

Run from `C:\Users\issda\SCBE-AETHERMOORE`.

### Audit today
```powershell
python scripts/system/crosstalk_reliability_manager.py
```

### Audit + repair
```powershell
python scripts/system/crosstalk_reliability_manager.py --day 20260304 --repair
```

## Success criteria
- zero missing lane entries
- zero missing markdown mirrors
- report artifact written in `artifacts/agent_comm/<day>/`

## Reference
- `docs/system/CROSSTALK_RELIABILITY_RUNBOOK.md`
