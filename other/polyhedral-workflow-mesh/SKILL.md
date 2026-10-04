---
name: polyhedral-workflow-mesh
description: Coordinate sub-agent communication, relay workflows, n8n-style automations, triggers, and cross-surface handoffs as one governed mesh. Use when a goal spans multiple agents, browser and terminal surfaces, automation hooks, or periodic and aperiodic work loops that need packets, scoreboards, relays, and proof-backed checkpoints instead of loose AI-to-AI chat.
---

# Polyhedral Workflow Mesh

Use this skill when one task is really many connected tasks moving across faces of the same system:

- browser
- terminal
- repo
- automation
- review
- publish

Treat each face as a local work surface. Treat edges as handoffs. Treat relays, triggers, and automations as pulleys and cranes that move work between faces without losing state.

## Core model

- Face: one operating surface or role
- Edge: a handoff path between surfaces
- Relay: a packet transfer that preserves intent and proof
- Trigger: an automation wake-up point
- Periodic loop: heartbeat, schedule, or review cadence
- Aperiodic loop: event-driven arrival, interrupt, or opportunistic follow-on
- Rendezvous: the buffer where periodic and aperiodic lanes meet safely

## Workflow

1. Frame the goal as a mesh, not one action.
- Define the faces involved.
- Define which face owns the final decision.

2. Choose the relay shape.
- Small baton handoff: use cross-talk packets.
- Multi-lane push: use a goal race.
- Triggered automation: use n8n-style or webhook nodes as supporting pulleys, not as the source of truth.

3. Generate the visible race/relay scaffold.
- `python C:\Users\issda\SCBE-AETHERMOORE\scripts\system\goal_race_loop.py --goal "<goal>" --mode <mode>`

4. Emit and verify packets.
- `python C:\Users\issda\SCBE-AETHERMOORE\scripts\system\crosstalk_relay.py emit --sender <agent> --recipient <agent> --intent <intent> --task-id <task> --summary "<summary>"`
- `python C:\Users\issda\SCBE-AETHERMOORE\scripts\system\crosstalk_relay.py verify --packet-id <id>`
- `python C:\Users\issda\SCBE-AETHERMOORE\scripts\system\crosstalk_relay.py ack --packet-id <id> --agent <agent>`

5. Add automation only where it carries weight.
- n8n/Zapier/webhooks should move or wake work, not replace the ledger.
- Keep the packet or scoreboard as the canonical state.

6. Join periodic and aperiodic flows through a rendezvous buffer.
- Scheduled loop owns cadence.
- Event loop owns interrupts and arrivals.
- Hand off through one shared checkpoint instead of forcing one lane to match the other's timing.

7. Verify mesh health.
- `python C:\Users\issda\SCBE-AETHERMOORE\scripts\system\crosstalk_reliability_manager.py`

## When to use which pattern

### Goal race

Use when:

- the work is sequential but multi-lane
- you want a scoreboard
- you want checkpoint visibility

### Direct relay

Use when:

- one agent needs to pass one bounded packet to another
- proof and next action matter more than orchestration

### Trigger mesh

Use when:

- a human or agent event should wake a connector, webhook, or automation
- the automation is a support system, not the whole workflow brain

### Cadence join

Use when:

- one team/lane runs on a recurring schedule
- another arrives irregularly
- both need a common drop zone

## Operator rules

- Never rely on freeform AI-to-AI chat when a packet, relay, or scoreboard will do.
- Keep one canonical state artifact per mesh:
  - scoreboard
  - packet lane
  - or both
- Keep automations downstream of the ledger, not upstream of it.
- Keep proof attached to each handoff.
- Treat repair as part of the mesh, not as an exception.

## Output contract

Return:

- faces
- relays
- trigger points
- checkpoint artifacts
- owner of final decision
- next action

## Resources

Load these only when needed:

- `references/flow-surface-map.md`
  - Load when deciding which surfaces, scripts, and logs belong in the mesh.
- `references/relay-and-cadence-patterns.md`
  - Load when shaping periodic, aperiodic, n8n-style, or cross-agent flows into one governed loop.
