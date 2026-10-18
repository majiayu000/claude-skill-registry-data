---
name: caddy-mute
agent: none
description: Mute a Caddy hint class for a window. Defaults to 4h auto-expiry. Classes — memory, context, body, routing, all.
allowed-tools: Read, Write, Edit, Bash
user-invocable: true
triggers:
  - caddy mute
  - mute caddy
  - silence caddy
  - shut up caddy
  - /caddy-mute
  - hint fatigue
  - too many caddy hints
---

# /caddy-mute

Suppress a Caddy hint class for a bounded window. State lives in `memory/CADDY_MUTES.json`. `daemons/caddy.sh` reads it on every UserPromptSubmit and skips matching class hints when active.

## Classes

- `memory` — `[CADDY:memory]` MEMDB, DIGEST hints
- `context` — `[CADDY:context]` CTX, CAPSULE hints
- `body` — `[CADDY:body]` BODY-CHECK hint
- `routing` — `[CADDY:routing]` ROUTE, /orient, STYLE, DICT hints
- `all` — nuclear; mutes every class

## Usage

```
/caddy-mute --class memory               # 4h default
/caddy-mute --class memory --hours 1     # 1h
/caddy-mute --class memory --forever     # explicit permanent (rare)
/caddy-mute --class all                  # nuclear
/caddy-mute --class memory --reason "design session, hint fatigue"
```

If no `--hours` and no `--forever`: default 4 hours.

## Implementation

Compute `muted_until` and Edit `memory/CADDY_MUTES.json`:

```json
{
  "memory": {
    "muted_until": "2026-05-03T18:00:00Z",
    "reason": "design session, hint fatigue",
    "default_duration_hours": 4
  }
}
```

For `--forever`: set `muted_until` to `9999-12-31T23:59:59Z`. Surface to the operator when setting forever ("muted memory class indefinitely — confirm?") so it doesn't drift into permanent silence by accident.

For `--class all`: write a single `all` block; caddy.sh `class_muted` checks `all` in addition to the requested class.

## Inverse

To unmute early, Edit `memory/CADDY_MUTES.json` and remove the class entry, or set `muted_until` to the past. There's no `/caddy-unmute` skill yet — the entry self-expires at `muted_until`, which is the point.

## When NOT to mute

- Standing rules (CTX heavy-bash, STYLE comms voice) exist because they prevent recurring drift. Muting them more than 4h means the rule isn't actually a standing rule and should be downgraded or deleted.
- Don't mute `all` for >24h. If you need `all` muted longer than that, the hint surface itself is broken and Caddy needs editing, not silencing.

## Doctrine link

Spec: [[concepts/Somatic v0.4.1 Wiring]] §6. Class taxonomy and 4h default were Codex+aigent-OS joint design decisions in the 2026-05-02 session.
