---
name: sonos-cli
description: Inspect and control Sonos playback with room validation and confirmation for disruptive actions.
category: utilities
aliases:
- sonos
- music
- speaker
- playback
triggers:
- Control Sonos
- Play music on Sonos
- Sonos speaker
- Pause Sonos
keywords:
- sonos
- music
- speaker
- playback
- audio
- streaming
dependencies:
- optional:sonos-cli
risk: low
version: 1.0.0
source: custom
enabled: true
capabilities:
- sonos-cli
- utilities
inputs:
- task
- context
outputs:
- result
- report
lifecycle: enabled
author: Mr-Nobody-Anonymous
tags:
- cli
- music
- playback
- sonos
- speaker
- utilities
compatibility:
  claude-code: '>=1.0'
  skillhub: '*'
  cursor: '>=0.40'
  codex: '*'
network_access: false
filesystem_access: read
credential_access: false
destructive_operations: false
---

# Sonos Cli

## Purpose
Inspect and control Sonos speakers through the CLI with room validation and
confirmation required for disruptive actions like volume changes or playback
interruption. The skill enables hands-free speaker management.

## When to Use
- Controlling Sonos playback (play, pause, skip)
- Adjusting volume across rooms
- Checking what's currently playing
- Grouping or ungrouping speakers

## When NOT to Use
- For professional audio equipment
- When Sonos is unavailable on the network
- For streaming service configuration (use app)

## Capabilities
- Playback control (play, pause, skip, previous)
- Volume adjustment (per room or group)
- Queue management
- Room status and current track info
- Group management (add/remove rooms)
- Preset recall (favorites, playlists)
- Power control (standby, wake)

## Inputs
- `action` (required) — one of: status, play, pause, volume, skip, group
- `room` (required) — speaker or group name
- `value` (optional) — volume level, target room for grouping

## Workflow
1. **Discover** — Find available Sonos devices
2. **Validate** — Confirm room exists
3. **Execute** — Perform requested action
4. **Confirm** — Report result
5. **Interrupt** — Ask for disruptive actions first

## Tools
- Sonos CLI (sonos-cli, soco, or similar)
- Network access to Sonos devices

## Examples
**User:** "What's playing in the living room?"
**Response:**
```
Living Room:
- Status: Playing
- Track: Bohemian Rhapsody - Queen
- Artist: Queen
- Album: A Night at the Opera
- Duration: 5:55 / 5:54
- Volume: 35%
```

## Safety
- Always validate room name exists
- Confirm before disruptive volume changes
- Never auto-adjust to max volume
- Warn before grouping/ungrouping

## Source
Auto-generated from openclawskills.net description.

## Notes
Maintained as part of canonical utilities category.
