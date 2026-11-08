---
name: peeku-windows
description: "Automate Windows UI/apps via peeku CLI/MCP: observe, act, wait, stream."
---

# Peeku Windows

## Overview
Capability map for `peeku`. Choose primitives by task intent, confidence, failure mode. No fixed step order.

## Operating Conventions
- JSON outputs for machine decisions: `--format json`.
- Daemon mode for iterative loops and `watch`.
- Selectors for replayability; refs for short-lived follow-up only.
- Action success = data-driven (`ok`, `warnings`, `evidence`), not assumed.

## Primitive Families

### 1) Targeting
Window targets: focused window, `hwnd`, window query (`titleContains`, `processName`, `processId`).
Surface targets: `start_menu`, `context_menu`, `active_popup`, `taskbar`, `notification_area`, `desktop_root`.
Pick window query/`hwnd` when focus drift likely. Pick surfaces for shell UI.

### 2) Observation
`windows list`, `windows focused`, `uia snapshot`, `see` (capture + snapshot), `capture image`, `observe` (events).
Shallow first (`depth 2`, `maxNodes 500`), increase only if required.

### 3) Selection
`find` (multi-match), `element get` (detail), selector DSL (`=`, `~=`), live evaluation (`--live` CLI / `preferCachedSnapshot=false` MCP).

### 4) Action
`click`, `invoke`, `set-value`, `type`, `scroll`, `hotkey`.
Prefer UIA semantics (`--method uia`) when controls expose patterns; input simulation (`--method input`) when UIA ineffective.

### 5) Time/Coordination
`wait` for condition arrival. `watch` for streaming updates (daemon required).

### 6) Composite
`start run` (open-start-search-enter), `context select` (menu-item), `batch` (deterministic multi-step, stop-on-error).

### 7) Performance
`perf gate` measures `find`, `click`, `set-value`, `type`, `watch`. Supports threshold checks + baseline updates.

## Reliability Rules
- Selectors = durable contract. `h:*`/`a:*` refs = ephemeral.
- Stale/unknown ref → re-resolve with selector, retry once.
- `set-value`/`type`: fail on `verificationMatched=false`.
- Transient surfaces (`start_menu`, `context_menu`, `active_popup`): refresh ids before actions.

## Selection Heuristics
- Broad context quickly → `see`
- Precise structure only → `uia snapshot`
- Candidate elements → `find`
- One element's capabilities → `element get`
- Deterministic multi-step → `batch`
- Launch/menu intents → `start run` or `context select`
- Reactive monitoring → daemon + `watch`
- Regression signal → `perf gate`

## Reference Files
- CLI templates: `references/02-cli-cheatsheet.md`
- MCP tools: `references/03-mcp-cheatsheet.md`
- Selectors/refs: `references/04-selectors-and-refs.md`
- Recovery: `references/05-recovery.md`
- Perf workflow: `references/06-metrics.md`

## Bootstrap Snippets

```powershell
peeku --format json doctor
peeku --daemon
peeku --format json see --depth 2 --maxNodes 500
peeku --format json find --selector "window/edit" --limit 20
peeku --format json set-value --selector "window/edit" --value "hello"
peeku --daemon --stop
```
