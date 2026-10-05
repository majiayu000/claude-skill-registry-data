---
name: ha:trace
description: Trace Python call trees from entry points via grep/python -c import analysis. Use when debugging data flow, planning signature changes, or understanding how a bug reaches code.
effort: medium
---

# Call Tracing

Build call trees showing how functions are reached from entry points.

## Iron Laws - Never Violate These

1. **Always try a caller lookup first** - grep the import graph to narrow the search space, `python3 -c "import ..."` to confirm it resolves, then grep for the actual call sites; grep-for-the-symbol alone is the fallback
2. **Stop at entry points** - config-flow steps, service handlers, dispatcher/websocket subscribers, coordinator update paths, time-interval listeners, setup/lifecycle hooks
3. **Track visited symbols** - Prevent infinite loops from circular calls
4. **Extract argument patterns** - Just knowing "who calls" isn't enough; HOW they call matters
5. **Max depth 10** - Deeper trees indicate architectural issues, not useful traces

## When to Build Call Tree (Use Proactively)

| Condition | Why Call Tree Helps |
|-----------|---------------------|
| Unexpected `None`/value at runtime | Trace where the value originates |
| Bug can't reproduce locally | See all entry points that reach the code |
| Changing a method signature | Find all callers and their argument patterns |
| Incomplete traceback | Get full path context |
| "Where does X come from?" | Visual answer to data flow question |

## Quick Trace

Grep-based import analysis works at file/module granularity, not function
granularity — there is no built-in per-function caller index. Combine two steps:

1. Run `grep -rln "from homeassistant.components.awesome.coordinator import \|from .coordinator import" homeassistant/components tests` to find which files even import the module (narrows the search space).
2. Run `grep -rn "async_set_mode(" homeassistant/components/awesome tests/components/awesome` to find the actual call sites and their argument expressions within those files.

For precise, function-level results (not just "this file imports that file"), use a small `ast`-based caller search or your editor's "Find All References" (Python language server) — see `${CLAUDE_SKILL_DIR}/references/argument-extraction.md`.

## Entry Points (Stop Here)

| Pattern | Type |
|---------|------|
| `async_step_user`/`async_step_reauth`/`async_step_reconfigure` in `config_flow.py` | Config flow |
| Service handlers registered via `hass.services.async_register` / `async_setup_services` (P18) | Service action |
| `async_dispatcher_connect` callbacks; `websocket_api` command handlers; `hass.bus.async_listen` listeners | Dispatcher / websocket / event bus |
| `_async_update_data` / `async_set_updated_data` push callbacks | Coordinator update path |
| `async_track_time_interval` / `async_track_point_in_time` listeners | Scheduler |
| `async_setup`/`async_setup_entry`/`async_unload_entry`/`async_migrate_entry`; `async_added_to_hass` | Setup / lifecycle |

## Delegate to call-tracer Agent

For full recursive tree with argument extraction and **parallel category tracing**:

```
Agent(subagent_type: "call-tracer", prompt: "Build call tree for AwesomeDataUpdateCoordinator.async_set_mode")
```

The call-tracer agent uses **parallel subagents** for each entry point category:

- Config Flow / Service Handler subagent (flow steps, service actions)
- Dispatcher / WebSocket subagent (dispatcher signals, WS commands, event bus)
- Coordinator Update Path subagent (`_async_update_data`, push callbacks)
- Setup / Lifecycle subagent (`async_setup_entry`, time-interval listeners)

Each gets fresh 200k context for deep exploration.

## Output Location

`.claude/plans/{slug}/research/call-tree-{function}.md`

## References

For detailed patterns:

- `${CLAUDE_SKILL_DIR}/references/depgraph-usage.md` - Full grep / `python -c` / pylint / pydeps import-tracing commands and options
- `${CLAUDE_SKILL_DIR}/references/entry-points.md` - All Home Assistant entry point patterns
- `${CLAUDE_SKILL_DIR}/references/argument-extraction.md` - `ast` parsing for argument patterns
