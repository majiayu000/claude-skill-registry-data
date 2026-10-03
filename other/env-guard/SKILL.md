---
name: env-guard
description: Check the trading-bot workspace for secret leakage and unsafe environment handling across tracked files, docs, panel settings flows, logs, scripts, and build/startup artifacts. Use after touching .env templates, config, logging, operator panel settings, startup helpers, or Windows packaging paths.
---

# Env Guard

## Binding sources

- **`AGENTS.md`** — secrets must not leak; **live** trading not enabled by default; testnet flags explicit.
- **`docs/IMPLEMENTATION_GAP.md`** — optional context on safe incremental rollout vs full vision.

## Purpose

Use this skill to verify that configuration and secret handling stay safe across the expanded workspace.

The guard now covers:
- `.env` and `.env.example`
- docs and skill text
- PowerShell scripts and startup helpers
- operator panel settings writes
- logs, research-run artifacts, and build outputs

## Use When

Use this skill when:
- editing `.env.example`, config parsing, or README
- editing operator panel settings or settings persistence
- editing logging, startup, EXE build, or report scripts
- credentials were pasted into chat or local files during the task

## Do Not Use When

Do not use this skill for:
- isolated math or layout changes that cannot touch config, docs, scripts, or logs

## Required Checks

- Confirm `.env` is not tracked.
- Scan tracked files for secret-like values or copied credentials.
- Confirm docs and skills use placeholders, not filled values.
- Confirm operator panel settings never expose secrets in responses or UI.
- Confirm logs, startup helpers, and packaging paths do not echo secrets.
- Confirm local data or build folders are not treated like tracked config.

## Expected Output

- `Tracked Env:` pass/fail.
- `Leak Scan:` findings or `clean`.
- `Unsafe References:` list or `none`.
- `Guard Verdict:` safe / unsafe.
