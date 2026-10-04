---
name: scbe-overwatch-relay-swarm
description: "Run a baton-style multi-agent sequence with dedicated overwatcher gates, deterministic AI-to-AI packet passing, and terminal-first execution artifacts."
---

# SCBE Overwatch Relay Swarm

Use this skill when the user wants a guided AI team that passes work like a baton race with explicit checkpoint overseers (`overwatchers`).

## Why This Skill Exists

- Keeps multi-agent work coherent across long tasks.
- Prevents silent drift by forcing reviewer gates between lanes.
- Maintains packet continuity in:
  - `artifacts/agent_comm/<day>/*.json`
  - `artifacts/agent_comm/github_lanes/cross_talk.jsonl`
  - `notes/_inbox.md`

## Relay Model

1. `runner` lane executes a scoped packet.
2. Handoff packet is emitted to the lane bus.
3. `overwatch` lane verifies quality/safety/revenue gate.
4. If pass: baton moves to next runner. If fail: baton returns with blocker packet.
5. Final lane emits `done` packet back to orchestrator.

## Terminal Command (Generate + Emit Relay Packets)

```powershell
npm run overwatch:relay -- --task "Launch monetization ops with audited publish flow" --mode money
```

Research variant:

```powershell
npm run overwatch:relay -- --task "Deep research and publish with source integrity" --mode research
```

Dry-run:

```powershell
npm run overwatch:relay -- --task "Test baton plan" --mode money --dry-run
```

## Spawn Sequence (Agent Tooling)

Use the emitted packet order as the execution queue.

1. Spawn first runner using packet 1 `task_id` + `summary`.
2. Wait for result; post proof into a handoff packet.
3. Spawn corresponding overwatcher packet.
4. Continue until final packet returns to orchestrator.

## Guardrails

- Never put tokens/secrets in `summary`, `next_action`, or `proof`.
- Overwatch packets must include concrete pass/fail criteria.
- Keep each packet scoped to one deliverable and one owner.
- If a lane blocks, emit `status=blocked` and do not skip gate.

## Resources

- `scripts/run_overwatch_relay.ps1`: wrapper for fast command invocation.
- `references/packet_contract.md`: packet field contract and status vocabulary.
- Repo script used by this skill: `scripts/system/overwatch_baton.py`.
