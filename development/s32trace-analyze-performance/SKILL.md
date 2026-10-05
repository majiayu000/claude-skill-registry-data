---
name: s32trace-analyze-performance
description: >
  Analyze an S32DS Performance View .perf export together with its ELF binary
  and project source tree to answer questions about function timing, call counts,
  hot functions, call-graph structure, and annotated source.
  Use when the user mentions a .perf file, performance profiling, inclusive/exclusive
  time, call graph, hot functions, or wants to know where CPU time is spent.
  Trigger phrases: "analyze perf file", "load .perf", "where does the CPU spend time",
  "which function is slowest", "show me the call graph", "who calls X", "what does X call",
  "inclusive time", "exclusive time", "how many times was X called", "performance hotspot",
  "show source for hot function", "open performance view", "profile results".
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  product: s32trace
  tags: '[s32trace, performance, perf, callgraph, hotspot, profiling, elf, dwarf]'
---

# S32Trace Performance Analysis

Answers performance questions from an S32DS Performance View export using three
local inputs: the `.perf` file, the ELF binary (with DWARF debug info), and the
project source tree.

## When to use

Trigger this skill when the user wants to:
- load a `.perf` + ELF + source tree and get a performance overview
- identify which functions consume the most CPU time (inclusive or exclusive)
- understand the call graph: who calls a function, and what it calls
- rank functions by call count to find frequently executed code
- view a source snippet for a hot function
- answer "where does the CPU spend most of its time?"
- answer "how many times was function X called?"

Do not use this skill to configure S32Trace (use `s32trace-create-configuration`),
analyze raw trace events (use `s32trace-analyze-trace`), or examine code coverage
(use `s32trace-analyze-coverage`).

## Available Capabilities

| Type | Name | Purpose |
|------|------|---------|
| MCP tool | `search_actions` | discover available actions, their input schemas, and descriptions |
| MCP tool | `execute_action` | validated dispatcher -- pass `action_name` + action-specific `params` |

All performance operations are routed through `execute_action`:

| Action name | Required params | Optional params |
|---|---|---|
| `performance.load` | `perf_path`, `elf_path`, `source_root` | `extra_source_roots`, `label`, `snippet_window` |
| `performance.summary` | `session_id` | `core`, `top_k` |
| `performance.function` | `session_id`, `name` | `core` |
| `performance.hotspots` | `session_id` | `sort_by` (`inclusive`/`exclusive`/`calls`), `top_k`, `core` |
| `performance.callgraph` | `session_id`, `root` | `depth`, `direction` (`callees`/`callers`), `core` |
| `performance.get_source` | `session_id` | `symbol`, `file_hint`, `line`, `core`, `snippet_window` |

Call `search_actions` first (or with a focused query such as `"performance load"`)
to get the full parameter documentation before calling `execute_action`.

## Typical workflow

```
performance.load          -> returns session_id + load summary
  -> performance.summary   (overview: top functions by inclusive/exclusive time and call count)
  -> performance.function  (per-function detail + callers + callees)
  -> performance.hotspots  (ranked hotspot list by chosen metric)
  -> performance.callgraph (nested call-tree from a root function, up or down)
  -> performance.get_source (source snippet for a hot function)
```

## Quickstart

1. Call `search_actions(query="performance load")` to confirm the action schema.
2. Ask the user for the `.perf`, ELF, and source root paths.
3. Call `execute_action(action_name="performance.load", params={...})`.
   Record `session_id` -- it is required by every subsequent call.
4. Unless the user has a specific question, call `performance.summary` and present
   `top_by_inclusive_time` (where most wall-clock time is spent), `top_by_exclusive_time`
   (self-time hot functions), and `top_by_call_count`.
5. Answer follow-up questions using the action table above.

## Workflow

1. **Identify inputs.** Confirm from the user:
   - Absolute path to the **`.perf`** file (`perf_path`).
     Typically at `<workspace>/.AnalysisData/<session>/<name>.perf`.
   - Absolute path to the **ELF** with DWARF debug info (`elf_path`).
     Must be the exact binary that was profiled.
   - Absolute path to the **project source root** (`source_root`).
     Needed for `performance.get_source` to return annotated source text.

2. **Load the session.** Call:

   ```
   execute_action(
     action_name = "performance.load",
     params = {
       "perf_path":   "<absolute path to .perf>",
       "elf_path":    "<absolute path to .elf>",
       "source_root": "<absolute path to project src/>",
       "label":       "my_perf_session"
     }
   )
   ```

   Verify: `function_count > 0`, `source.available: true`.

3. **Get an overview.** Call `performance.summary` unless the user has a specific question.
   Key fields to present:
   - `top_by_inclusive_time` -- functions with the highest total accumulated time
   - `top_by_exclusive_time` -- functions with the highest self-time (ignoring callees)
   - `top_by_call_count` -- most frequently called functions

4. **Answer specific questions.**

   | User question | Action to call | Key params |
   |---|---|---|
   | "Where does the CPU spend time?" | `performance.summary` | `top_k` |
   | "Which function has the most self-time?" | `performance.hotspots` | `sort_by="exclusive"` |
   | "How many times was `crc16_step` called?" | `performance.function` | `name="crc16_step_..."` |
   | "Show me the call graph for `main`" | `performance.callgraph` | `root="main"` |
   | "Who calls `slow_leaf`?" | `performance.callgraph` | `root="slow_leaf", direction="callers"` |
   | "What does `slow_mid3` call?" | `performance.callgraph` | `root="slow_mid3"` |
   | "Show me the source for the hottest function" | `performance.get_source` | `symbol=<name>` |

5. **Inline/mangled function names.** S32DS names inlined copies as
   `funcname_0x<address>`. When the user asks about `clamp_i32`:
   1. Call `performance.hotspots` to list all instances.
   2. Call `performance.function` with the exact mangled name for per-instance detail.

6. **Call-graph exploration.** When the user asks "why is my main so slow?":
   1. Call `performance.callgraph(root="main", depth=3)` to see the full downward tree.
   2. Look for children with high `pct_inclusive`.
   3. Drill into those with `performance.function` for per-callee breakdown.
   4. Call `performance.get_source` to view the actual code.

## Guardrails

**Scope**
- All performance actions are read-only; no file is written and no S32DS process is started.
- Do not call configurator actions (`configurator.*`) from this skill.

**Destructive actions**
- None. `performance.load` writes only to an in-memory session cache; it does not touch any file.

**Secrets**
- No secrets or PII involved; no redaction required.

**Refuse-and-escalate**
- `performance.load` returns `error`: report the message verbatim and ask the user to
  verify the file paths.
- `source.available` is `false` after load: ask the user for the correct `source_root`.
- `performance.function` returns `found: false`: use `performance.hotspots` first to
  confirm the exact symbol name (mangled names include the hex address).
- `performance.callgraph` node marked `truncated=true`: increase `depth` parameter.
- Stale `session_id`: call `performance.load` again and record the new `session_id`.

**Resource limits**
- Default `top_k` is 10 for summary and hotspots. Increase only when explicitly requested.
- Default callgraph `depth` is 3. Values above 6 may produce very large responses.

## Validation loop

1. After `performance.load`, verify `function_count > 0` and (when `source_root` given)
   `source.available: true`.
2. After `performance.summary`, confirm `total_functions > 0`.
3. Pass criterion: `session_id` is in hand and the load summary matches expectations
   (correct core, function count, source available).

## Out of scope

- Creating or editing S32Trace configuration XML (use `s32trace-create-configuration`).
- Trace event analysis from a decoded CSV (use `s32trace-analyze-trace`).
- Code coverage analysis from a `.flatprofiler` (use `s32trace-analyze-coverage`).
- Timeline analysis from a `.timeline` (use `s32trace-analyze-timeline`).
- Compiling, flashing, or debugging firmware.

## See Also

- `search_actions(query="performance")` -- returns the full parameter schema for
  all 6 `performance.*` actions.
- `s32trace-analyze-coverage` -- sibling skill for code coverage analysis.
- `s32trace-analyze-timeline` -- sibling skill for timeline / sampling analysis.
- `s32trace-analyze-trace` -- sibling skill for trace event / timing analysis.
- `s32trace-create-configuration` -- skill for configuring the trace capture.
