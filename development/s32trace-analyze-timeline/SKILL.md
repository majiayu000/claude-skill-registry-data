---
name: s32trace-analyze-timeline
description: >
  Analyze an S32DS Timeline view .timeline export together with an optional ELF binary
  and project source tree to answer questions about execution hotspots, function-level
  sample distributions, time-window analysis, execution sequences, and source-annotated
  hot lines.
  Use when the user mentions a .timeline file, timeline view, PC sampling, execution
  hotspots from a timeline, or wants to know where the CPU spends time.
  Trigger phrases: "analyze timeline", "load .timeline", "where does the CPU spend time",
  "which function is the hotspot", "show me the hot functions", "what is the execution
  sequence", "show function transitions", "annotate source with samples",
  "timeline hotspot analysis", "execution profile from timeline",
  "what happened between tick X and tick Y", "zoom into a time window",
  "open timeline file", "show me the call order".
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  product: s32trace
  tags: '[s32trace, timeline, profiling, hotspot, pc-sampling, elf, dwarf, performance]'
---

# S32Trace Timeline Analysis

Answers execution-profile questions from an S32DS Timeline view export using up to three
local inputs: the `.timeline` file, an optional ELF binary (with DWARF debug info), and
an optional project source tree.

## When to use

Trigger this skill when the user wants to:
- load a `.timeline` file and get an overview of CPU time distribution
- find which functions consume the most CPU cycles (hotspot analysis)
- understand the execution sequence - which functions were called in what order
- zoom into a specific time window (by tick range) and see what ran there
- drill into a single function: per-address sample breakdown and source location
- view a source snippet annotated with per-line sample counts
- understand inlined function instances (`clamp_i32_0x33d83d24` etc.)

Do not use this skill to configure S32Trace (use `s32trace-create-configuration`),
analyze decoded trace CSV events (use `s32trace-analyze-trace`),
or analyze code coverage from a Flat Profiler export (use `s32trace-analyze-coverage`).

## Available Capabilities

| Type | Name | Purpose |
|------|------|---------|
| MCP tool | `search_actions` | discover available actions, their input schemas, and descriptions |
| MCP tool | `execute_action` | validated dispatcher -- pass `action_name` + action-specific `params` |

All timeline operations are routed through `execute_action`:

| Action name | Required params | Optional params |
|---|---|---|
| `timeline.load` | `timeline_path` | `elf_path`, `source_root`, `extra_source_roots`, `label`, `snippet_window` |
| `timeline.summary` | `session_id` | `source_name`, `top_k` |
| `timeline.hotspots` | `session_id` | `sort_by` (`samples`/`time`), `top_k`, `source_name` |
| `timeline.function` | `session_id`, `name` | `source_name`, `include_source` |
| `timeline.window` | `session_id` | `start_tick`, `end_tick`, `source_name`, `top_k` |
| `timeline.sequence` | `session_id` | `source_name`, `limit` |
| `timeline.source` | `session_id` | `symbol`, `file_hint`, `line`, `source_name`, `snippet_window` |

Call `search_actions` first (or with a focused query such as `"timeline load"`)
to get the full parameter documentation before calling `execute_action`.

## Typical workflow

```
timeline.load        -> returns session_id + load summary
  -> timeline.summary   (top functions, total samples, timestamp range)
  -> timeline.hotspots  (ranked by samples or time)
  -> timeline.function  (per-function detail + source location)
  -> timeline.window    (zoom into a tick range)
  -> timeline.sequence  (ordered list of function transitions)
  -> timeline.source    (source snippet annotated with samples)
```

## Quickstart

1. Call `search_actions(query="timeline load")` to confirm the action name and input schema.
2. Ask the user for the `.timeline` path; ELF and source root are optional but enable
   richer queries (`timeline.function` source location, `timeline.source`).
3. Call `execute_action(action_name="timeline.load", params={...})`.
   Record `session_id` -- it is required by every subsequent call.
4. Unless the user has a specific question, call
   `execute_action(action_name="timeline.summary", params={"session_id": ...})`
   and present `total_samples`, `timestamp_range`, and `top_functions_by_samples`.

## Workflow

1. **Identify inputs.** Confirm from the user:
   - Absolute path to the **`.timeline`** file (`timeline_path`).
     Typically at `<workspace>/.AnalysisData/<session>/<name>.timeline`.
   - (Optional) Absolute path to the **ELF** with DWARF debug info (`elf_path`).
     Required for `timeline.function` source location and `timeline.source`.
   - (Optional) Absolute path to the **project source root** (`source_root`).
     Required for `timeline.source` to return annotated source text.

2. **Load the timeline session.** Call:

   ```
   execute_action(
     action_name = "timeline.load",
     params = {
       "timeline_path": "<absolute path to .timeline>",
       "elf_path":      "<absolute path to .elf>",       // optional
       "source_root":   "<absolute path to project src>", // optional
       "label":         "my_timeline_session"
     }
   )
   ```

   Verify: `function_count > 0`, `data_row_count > 0`.
   Record `timestamp_range` for later use in `timeline.window`.

3. **Get an overview.** Call `timeline.summary` unless the user has a precise question.
   Key fields to present:
   - `total_samples` and `timestamp_range`
   - `top_functions_by_samples` -- where the CPU spent the most cycles

4. **Answer specific questions.**

   | User question | Action to call | Key params |
   |---|---|---|
   | "Where does the CPU spend most time?" | `timeline.hotspots` | `sort_by="samples"` |
   | "Show me the hottest functions by time" | `timeline.hotspots` | `sort_by="time"` |
   | "How many samples did `slow_top` get?" | `timeline.function` | `name="slow_top"` |
   | "Show all instances of `clamp_i32`" | `timeline.function` | `name="clamp_i32"` |
   | "What ran between tick 1000 and 50000?" | `timeline.window` | `start_tick=1000, end_tick=50000` |
   | "Show me the execution sequence" | `timeline.sequence` | `limit=200` |
   | "Show `slow_top` source with samples" | `timeline.source` | `symbol="slow_top"` |
   | "Show line 42 of workloads.c" | `timeline.source` | `file_hint="workloads.c", line=42` |

5. **Inline function handling.** The timeline function table lists inlined copies under
   names like `clamp_i32_0x33d83d24`. When the user asks about `clamp_i32`:
   1. Call `timeline.function(name="clamp_i32")` -- it matches all instances whose
      name is exactly `clamp_i32` or starts with `clamp_i32_0x`.
   2. Each instance in the `instances` list has its own `address`, `size`, and
      `total_samples`.
   3. Note that different instances may have very different sample counts because each
      is a separate copy of the inlined function placed at a different call site.

6. **Time-window drill-down.** Use `timestamp_range` from `timeline.summary` to
   orient the user:
   1. Present `[start, end]` range with the unit note that it is raw tick counts
      (unit depends on board timestamp generator configuration).
   2. Let the user pick a sub-range, then call `timeline.window` with those bounds.
   3. Compare the per-window hotspot list to the full-trace list to show what changed.

## Guardrails

**Scope**
- All timeline actions are read-only; no file is written, no project is modified,
  and no S32 Design Studio process is started.
- Do not call configurator actions (`configurator.*`) from this skill.

**Destructive actions**
- None. `timeline.load` writes only to an in-memory session cache keyed by `session_id`;
  it does not touch any file.

**Secrets**
- No secrets or PII are involved; no redaction required.

**Refuse-and-escalate**
- `timeline.load` returns `error`: report the message verbatim and ask the user to
  verify the file path.
- `timeline.function` returns `found: false`: confirm the exact function name using
  `timeline.summary` or `timeline.hotspots` first.
- `timeline.source` returns `error` about missing ELF or source root: ask the user to
  reload with `elf_path` and `source_root` provided.
- Stale `session_id`: if an action returns "Timeline session ... not found", the MCP
  server was restarted; call `timeline.load` again and record the new `session_id`.

**Resource limits**
- Default `top_k` for `hotspots` and `summary` is 10. Increase only when the user
  explicitly asks for more.
- `timeline.sequence` default `limit` is 100 transitions. Raise only on request.

## Validation loop

1. After `timeline.load`, verify `function_count > 0` and `data_row_count > 0`.
2. After `timeline.summary`, confirm `total_samples > 0`.
3. Pass criterion: `session_id` is in hand, function count and row count are
   non-zero, and the timestamp range is plausible.

## Out of scope

- Creating or editing S32Trace configuration XML (use `s32trace-create-configuration`).
- Trace event analysis from a decoded CSV (use `s32trace-analyze-trace`).
- Code coverage analysis from a Flat Profiler export (use `s32trace-analyze-coverage`).
- Installing or updating S32 Design Studio.
- Compiling, flashing, or debugging firmware.

## See Also

- `search_actions(query="timeline")` -- returns the full parameter schema for
  all 7 `timeline.*` actions.
- `s32trace-analyze-trace` -- sibling skill for trace event / timing analysis from CSV.
- `s32trace-analyze-coverage` -- sibling skill for code coverage from Flat Profiler.
- `s32trace-create-configuration` -- skill for configuring the trace capture.
