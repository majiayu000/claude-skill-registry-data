---
name: seeker-daemon-ops
description: "Use when the user wants to run, monitor, or debug the SolanaOS Seeker daemon and Telegram command flow"
version: "1.0.0"
emoji: "🦅"
requires:
  bins: ["go"]
  env: []
  config: []
allowed-tools: []
---

# Seeker Daemon Ops

Use this skill to operate the daemon quickly and safely.

## Standard run

```bash
go run ./cmd/solanaos daemon --seeker --pet-name SeekerClaw
```

## Common safe modes

- Disable Telegram for local testing:

```bash
go run ./cmd/solanaos daemon --seeker --no-telegram
```

- Keep daemon online but disable OODA trading loop:

```bash
go run ./cmd/solanaos daemon --seeker --no-ooda
```

## Telegram command validation checklist

1. `/status`
2. `/wallet`
3. `/trending`
4. `/research <mint>`
5. `/ooda`
6. `/sim` then `/live`
7. `/trades`

If Birdeye key is missing, `/trending` and `/research` should return a clear setup message.
