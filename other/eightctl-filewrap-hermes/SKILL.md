---
name: eightctl
description: "Control Eight Sleep pods: status, temperature, alarms."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Eight Sleep, Sleep, Health, Smart-Home]
    category: health
prerequisites:
  commands: [eightctl]
---

# eightctl Skill

Control Eight Sleep pods with the `eightctl` CLI: status, temperature, alarms, schedules, audio, and base position. Requires an Eight Sleep pod, an Eight Sleep account, and the `eightctl` binary. The API is unofficial and rate-limited.

## When to Use

- User asks for the pod status, temperature, or to turn the pod on or off
- Managing alarms or schedules on the pod
- Checking base info or angle, or controlling pod audio

## Prerequisites

- An Eight Sleep pod and account, with auth configured.
- Install `eightctl`: `go install github.com/steipete/eightctl/cmd/eightctl@latest`
- Auth: config file `~/.config/eightctl/config.yaml`, or environment `EIGHTCTL_EMAIL` and `EIGHTCTL_PASSWORD`. Credentials live in the Hermes `.env` (secrets only) or the config file; never print them and never paste a password into chat.
- Run commands with the `terminal` tool.

## How to Run

1. Check `eightctl` is on `PATH` with the `terminal` tool and auth is configured; if either is missing, say so and stop.
2. Run the read or control command for the task.
3. Report back the pod state that changed.

## Quick Reference

```bash
eightctl status
eightctl on
eightctl off
eightctl temp 20
```

Alarms and schedules:

```bash
eightctl alarm list
eightctl alarm create
eightctl alarm dismiss
eightctl schedule list
eightctl schedule create
eightctl schedule update
```

Audio and base:

```bash
eightctl audio state
eightctl audio play
eightctl audio pause
eightctl base info
eightctl base angle
```

## Procedure

1. Run `eightctl status` first to confirm the pod is reachable and to see the current state.
2. Temperature: `eightctl temp <degrees>` for the target temperature.
3. Power: `eightctl on` or `eightctl off`.
4. Alarms: list with `eightctl alarm list` before creating or dismissing one, so the change lands on the right alarm.
5. Schedules: list with `eightctl schedule list` before creating or updating one.
6. Report back the new state from a fresh `eightctl status` where it applies.

## Pitfalls

- The API is unofficial and rate-limited. Avoid repeated logins; authenticate once and reuse the session. Do not hammer `status` in a loop.
- A failed command after a long idle period usually means the session expired: re-authenticate once, then retry the command.
- Temperature changes and alarms affect a real bed. Confirm the target temperature and the alarm time with the user before applying, and never set an alarm as a joke or a guess.
- Never print the account email and password together, and never print the password at all.

## Verification

- After any change, run `eightctl status` and confirm the reported state matches what was asked.
- After creating an alarm or schedule, list it again and confirm the time and settings match.
- After a temperature change, confirm the reported target temperature in the status output.
