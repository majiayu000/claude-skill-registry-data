---
name: ric-xapp-dev
description: Guidance for developing OSC RIC xApps (RC/KPM/E2 subscription patterns), safe integration steps, and common pitfalls (polling vs periodic reporting).
allowed-tools: Read, Grep, Glob, Bash
---

# RIC xApp Development Skill

Use this Skill when implementing anything that touches:
- RC xApp gRPC integration
- E2 subscription / KPM periodic reporting
- RMR message flow assumptions

## Rules of thumb
1) Prefer **subscription periodic reporting** over xApp polling loops.
2) Keep integration points isolated: only one module should speak gRPC to RC (`beam_tracking/ric/rc_grpc_client.py`).
3) All external endpoints must be configurable (host/port/timeout).
4) Always add a "sim mode" fallback to reproduce issues offline.

## Files to consult
- `docs/03_kpm_reporting_period_notes.md`
- `beam_tracking/ric/rc_grpc_client.py`
- `.claude/commands/gen-rc-protos.md`

## Output expectations
When you propose changes:
- list exact files + functions
- provide small diff-sized code blocks
- include a minimal test plan
