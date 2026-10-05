---
name: s32trace-analyze-trace
description: >
  Analyze a decoded S32Trace Trace-view export (.csv) together with its ELF
  binary and optional project source tree to answer questions about instruction
  addresses, timing, hot functions, code snippets, and potential improvements.
  Use when the user mentions a trace CSV, an ELF file, or a project source
  folder in the context of trace analysis.
  Trigger phrases: "analyze this trace", "load the trace CSV", "which function
  is the hottest", "where did instruction X execute", "how long between these
  lines", "why is my ISR slow", "show me the code at this address", "how long
  did foo take", "my code is in <path>", "can you look at the source", "what
  happened between these two events", "suggest optimizations for this capture".
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  product: s32trace
  tags: '[s32trace, analysis, csv, elf, dwarf, trace-view, optimization]'
---

# S32Trace Trace Analysis

Answers application-specific questions from a decoded S32Trace Trace-view
capture using three local inputs: the decoded CSV, the ELF binary (with DWARF
debug info), and an optional project source tree.

## When to use

Trigger this skill when the user wants to:
- load a decoded S32Trace CSV + ELF and get an overview
- find which functions dominate execution time or instruction count
- look up what function / file / line a specific PC address belongs to
- measure the time delta between two code locations or events
- retrieve a source code snippet for a function or file:line reference
- identify optimization opportunities from trace data
- answer "what happened between t1 and t2?"

Do not use this skill to configure S32Trace (use `s32trace-create-configuration`),
compile or flash firmware, or start a debug session.

## Available Capabilities

| Type | Name | Purpose |
|------|------|---------|
| MCP tool | `search_actions` | discover available actions, their input schemas, and descriptions |
| MCP tool | `execute_action` | validated dispatcher -- pass `action_name` + action-specific `params` |

All analysis operations are routed through `execute_action`:

| Action name | Required params | Optional params |
|---|---|---|
| `analysis.load_trace` | `csv_path`, `elf_path` | `source_root`, `extra_source_roots`, `label`, `time_unit_ns`, `snippet_window` |
| `analysis.summary` | `trace_id` | `top_n` |
| `analysis.find_event` | `trace_id`, `selector` | `limit`, `include_source` |
| `analysis.address_at` | `trace_id` | `pc` (hex string), `symbol` (name) |
| `analysis.time_between` | `trace_id`, `from_selector`, `to_selector` | `occurrence` (`first`/`all`) |
| `analysis.range_events` | `trace_id` | `time_range`, `from_selector`, `to_selector`, `limit` |
| `analysis.get_source` | `trace_id` | `file_hint`, `line`, `symbol`, `snippet_window` |

Call `search_actions` first (or with a focused query such as `"analysis load"`)
to get the full parameter documentation before calling `execute_action`.

## Typical workflow

```
analysis.load_trace        -> returns trace_id + load summary
  -> analysis.summary      (overview: hot functions, duration, cores)
  -> analysis.find_event   (filter events by symbol, address, type, ...)
  -> analysis.address_at   (resolve a PC to symbol + file:line + snippet)
  -> analysis.time_between (measure delta between two code locations)
  -> analysis.range_events (roll up all events in a time or selector window)
  -> analysis.get_source   (fetch a source snippet by symbol or file:line)
```

## Quickstart

1. Call `search_actions(query="analysis load trace")` to confirm the action
   name and input schema.
2. Ask the user for the CSV and ELF paths.  When the user provides a folder
   such as `C:\..\.AnalysisData\trace_0`, look for `*.csv` and `*.elf` inside.
   Ask for `source_root` separately; never guess it.
3. Call `execute_action(action_name="analysis.load_trace", params={...})`.
   Record `trace_id` from the result -- it is required by every subsequent call.
4. Unless the user has a specific question, call
   `execute_action(action_name="analysis.summary", params={"trace_id": ...})`
   and present `top_functions_by_events`, `duration_ns`, and `cores`.
5. Answer follow-up questions using the action table above.
6. For optimization questions, combine `analysis.range_events` to find the
   dominant symbols with `analysis.get_source` to retrieve the code, then
   reason about inefficiencies.

## Workflow

1. **Identify inputs.** Confirm from the user:
   - Absolute path to the decoded **CSV** (`csv_path`).
   - Absolute path to the **ELF** with DWARF debug info (`elf_path`).
   - Optional absolute path to the **source root** (`source_root`); enabling it
     makes every answer show the matching source snippet.
   - `time_unit_ns`: multiplier to convert raw timestamps to nanoseconds
     (e.g. `1.0` if already in ns; `1000.0` if in microseconds).

2. **Load the trace session.** Call:

   ```
   execute_action(
     action_name = "analysis.load_trace",
     params = {
       "csv_path":    "<absolute path to .csv>",
       "elf_path":    "<absolute path to .elf>",
       "source_root": "<optional source tree root>",
       "time_unit_ns": 1.0,
       "label":       "trace_0"
     }
   )
   ```

   Verify: `parent_event_count > 0` and `elf_arch` is non-empty.
   If `source.available` is `false` and the user supplied a source root,
   report the path as unresolved and offer to retry with a corrected path.

3. **Get an overview.** Call `analysis.summary` unless the user has a precise question.
   Use `top_functions_by_events` to orient the conversation toward actual hot spots.

4. **Answer specific questions.**

   | User question | Action to call | Key params |
   |---|---|---|
   | "Which function ran the most?" | `analysis.summary` | `top_n` |
   | "Where did function X execute?" | `analysis.find_event` | `selector={"symbol":"X"}` |
   | "What is at address 0x...?" | `analysis.address_at` | `pc="0x..."` |
   | "How long between A and B?" | `analysis.time_between` | `from_selector`, `to_selector` |
   | "What happened between t1 and t2?" | `analysis.range_events` | `time_range=[t1,t2]` |
   | "Show me the code for function X" | `analysis.get_source` | `symbol="X"` |
   | "More context around line N in file F" | `analysis.get_source` | `file_hint=F, line=N, snippet_window=10` |

5. **Suggest improvements.** When the user asks "can I improve this?" or "why is X slow?":
   1. Call `analysis.range_events` with selectors around the slow region to get
      `top_symbols` and `top_files`.
   2. Call `analysis.get_source` for each dominant symbol to retrieve the code.
   3. Reason about the code: tight loops, redundant memory accesses, missed
      inlining, cache-unfriendly access patterns, repeated function call overhead.
   4. Present a prioritized list of specific suggestions with file + line
      references.

## Guardrails

**Scope**
- All analysis actions are read-only; no file is written, no project is
  modified, and no S32 Design Studio process is started.
- Do not call configurator actions (`configurator.*`) from this skill.

**Destructive actions**
- None.  `analysis.load_trace` writes only to an in-memory session cache
  keyed by `trace_id`; it does not touch any file.

**Secrets**
- No secrets or PII are involved; no redaction required.

**Refuse-and-escalate**
- `load_trace` returns `error`: report the message verbatim and ask the user to
  verify the file paths.
- `elf_arch` is empty after load: DWARF information may be absent; warn that
  address-to-symbol mapping will be unavailable.
- `summary` returns empty `top_functions_by_events`: the CSV may contain only
  Info/Context rows with no Linear events; report and stop.
- `address_at` or `get_source` returns `resolved: false` with a source root
  supplied: DWARF paths do not match the local tree; ask the user for the
  correct `source_root` or `extra_source_roots`.
- Path escape: `get_source` will refuse to read files outside the declared
  source roots; do not attempt to bypass this by constructing absolute paths
  that leave the root.
- Stale `trace_id`: if an action returns "trace_id not found", the MCP server
  was restarted; call `analysis.load_trace` again and report the new `trace_id`.

**Resource limits**
- Default `limit` for `find_event` and `range_events` is 20 rows.  Increase
  only when the user explicitly asks for more; never return unbounded results.
- `get_source` hard-limits snippets to 50 lines regardless of `snippet_window`.

## Validation loop

1. After `load_trace`, verify `parent_event_count > 0`, `elf_arch` non-empty,
   and (when `source_root` was given) `source.available: true`.
2. After `summary`, confirm at least one entry in `top_functions_by_events`.
3. Pass criterion: `trace_id` is in hand and the load summary matches the
   user's expectations (correct core, event count, time range).

## Out of scope

- Creating or editing S32Trace configuration XML (use `s32trace-create-configuration`).
- Installing or updating S32 Design Studio.
- Compiling, flashing, or debugging firmware.
- Generating code from a `.mex` file (use `s32ct-generate-code`).
- Timeline, Code Coverage, Performance, and Call Tree view analysis.

## See Also

- `search_actions(query="analysis")` -- returns the full parameter schema for
  all 7 `analysis.*` actions.
- `s32trace-analyze-coverage` -- sibling skill for code-coverage analysis from a `.flatprofiler` export.
- `s32trace-create-configuration` -- sibling skill for configuring the trace
  capture (before analysis).

## Selector schema

Used by `analysis.find_event`, `analysis.time_between`, and `analysis.range_events`:

```json
{
  "symbol":            "<regex or exact function name>",
  "pc_range":          ["0xLO", "0xHI"],
  "event_type":        "Linear | Info | Software Context",
  "core":              "R52_0_0",
  "time_range":        [t_start_raw, t_end_raw],
  "instruction_regex": "<regex matched against disassembly text>"
}
```
