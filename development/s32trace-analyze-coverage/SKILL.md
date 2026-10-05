---
name: s32trace-analyze-coverage
description: >
  Analyze an S32DS Flat Profiler code-coverage export (.flatprofiler) together with
  its ELF binary and project source tree to answer questions about coverage percentages,
  uncovered code paths, execution hotspots, and annotated source.
  Use when the user mentions a .flatprofiler file, code coverage, uncovered functions,
  or wants to know how well their application was tested.
  Trigger phrases: "how well is my code covered", "which functions were never called",
  "show me uncovered lines", "what is the coverage percentage", "why is coverage low",
  "which functions take the most time", "show me the hotspot", "annotate source with
  coverage", "load coverage data", "open flatprofiler", "analyze .flatprofiler",
  "what code did not execute", "dead code", "partially covered function".
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  product: s32trace
  tags: '[s32trace, coverage, flatprofiler, elf, dwarf, code-coverage, hotspot]'
---

# S32Trace Coverage Analysis

Answers coverage questions from an S32DS Flat Profiler export using three local inputs:
the `.flatprofiler` file, the ELF binary (with DWARF debug info), and the project source tree.

## When to use

Trigger this skill when the user wants to:
- load a `.flatprofiler` + ELF + source tree and get a coverage overview
- find which functions were never executed or are only partially covered
- identify which source lines were not reached during the test run
- rank functions by execution time (flat profile hotspot view)
- view a source snippet annotated with per-line coverage state and hit counts
- understand inline function coverage (multiple instances at different addresses)
- answer "what percentage of my code ran?"

Do not use this skill to configure S32Trace (use `s32trace-create-configuration`),
compile or flash firmware, or start a debug session.

## Available Capabilities

| Type | Name | Purpose |
|------|------|---------|
| MCP tool | `search_actions` | discover available actions, their input schemas, and descriptions |
| MCP tool | `execute_action` | validated dispatcher -- pass `action_name` + action-specific `params` |

All coverage operations are routed through `execute_action`:

| Action name | Required params | Optional params |
|---|---|---|
| `coverage.load` | `flatprofiler_path`, `elf_path`, `source_root` | `extra_source_roots`, `label`, `snippet_window` |
| `coverage.summary` | `session_id` | `core`, `top_k`, `include_no_source_info` |
| `coverage.function` | `session_id`, `name` | `core`, `include_source_rows` |
| `coverage.file` | `session_id`, `file_hint` | `core` |
| `coverage.uncovered` | `session_id` | `granularity` (`function`/`line`/`asm`), `sort_by`, `top_k`, `core`, `include_no_source_info` |
| `coverage.hotspots` | `session_id` | `sort_by`, `granularity` (`function`/`line`), `top_k`, `core`, `include_no_source_info` |
| `coverage.get_source` | `session_id` | `symbol`, `file_hint`, `line`, `core`, `snippet_window` |

Call `search_actions` first (or with a focused query such as `"coverage load"`)
to get the full parameter documentation before calling `execute_action`.

## Typical workflow

```
coverage.load          -> returns session_id + load summary
  -> coverage.summary   (overview: coverage %, uncovered count, hotspots)
  -> coverage.function  (per-function detail + per-line breakdown)
  -> coverage.file      (file-level stats + uncovered function list)
  -> coverage.uncovered (ranked list of uncovered functions/lines/asm)
  -> coverage.hotspots  (most-executed functions or lines by time)
  -> coverage.get_source (source snippet annotated with coverage + time)
```

## Quickstart

1. Call `search_actions(query="coverage load")` to confirm the action name and input schema.
2. Ask the user for the `.flatprofiler`, ELF, and source root paths.
3. Call `execute_action(action_name="coverage.load", params={...})`.
   Record `session_id` from the result -- it is required by every subsequent call.
4. Unless the user has a specific question, call
   `execute_action(action_name="coverage.summary", params={"session_id": ...})`
   and present `overall.asm_coverage_pct`, `overall.src_coverage_pct`, function counts,
   `top_by_time`, and `top_uncovered_by_size`.
5. Answer follow-up questions using the action table above.

## Workflow

1. **Identify inputs.** Confirm from the user:
   - Absolute path to the **`.flatprofiler`** file (`flatprofiler_path`).
     Typically at `<workspace>/.AnalysisData/<session>/<name>.flatprofiler`.
   - Absolute path to the **ELF** with DWARF debug info (`elf_path`).
     Must be the exact binary that was profiled.
   - Absolute path to the **project source root** (`source_root`).
     Needed for `coverage.get_source` to return annotated source text.

2. **Load the coverage session.** Call:

   ```
   execute_action(
     action_name = "coverage.load",
     params = {
       "flatprofiler_path": "<absolute path to .flatprofiler>",
       "elf_path":          "<absolute path to .elf>",
       "source_root":       "<absolute path to project src/>",
       "label":             "my_coverage_session"
     }
   )
   ```

   Verify: `file_count > 0`, `function_count > 0`, `source.available: true`.
   If `source.available` is `false` and the user supplied a source root,
   report the path as unresolved and offer to retry with a corrected path.

3. **Get an overview.** Call `coverage.summary` unless the user has a precise question.
   Key fields to present:
   - `overall.asm_coverage_pct` and `overall.src_coverage_pct`
   - `overall.fully_covered_functions`, `overall.partially_covered_functions`, `overall.fully_uncovered_functions`
   - `top_uncovered_by_size` -- the largest functions never executed
   - `top_by_time` -- where the CPU spent the most time

4. **Answer specific questions.**

   | User question | Action to call | Key params |
   |---|---|---|
   | "What is my overall coverage?" | `coverage.summary` | `top_k` |
   | "How much of `slow_path.c` is covered?" | `coverage.file` | `file_hint="slow_path.c"` |
   | "Show me coverage for `slow_leaf`" | `coverage.function` | `name="slow_leaf"` |
   | "Which functions were never executed?" | `coverage.uncovered` | `granularity="function"` |
   | "Show me uncovered lines in `workloads.c`" | `coverage.uncovered` | `granularity="line"` |
   | "Where does the CPU spend most of its time?" | `coverage.hotspots` | `sort_by="time"` |
   | "Show me `main` with coverage annotation" | `coverage.get_source` | `symbol="main"` |
   | "Show me the code around line 42 of main.c" | `coverage.get_source` | `file_hint="main.c", line=42` |

5. **Inline function handling.** The S32DS profiler reports inlined functions at multiple
   addresses under names like `clamp_i32_0x33d83d24`. When the user asks about `clamp_i32`:
   1. Call `coverage.uncovered` or `coverage.summary` to see all instances listed.
   2. Call `coverage.function` with the exact mangled name for detail on a specific instance.
   3. Note that different instances may have different coverage because they are separate
      copies of the inlined code placed at different call sites.

6. **Suggest improvements.** When the user asks "what code should I test?" or "why is coverage low?":
   1. Call `coverage.uncovered granularity=function` -- rank by `size` to find the most
      impactful untested functions.
   2. Call `coverage.file` on each low-coverage source file to identify the uncovered functions.
   3. Call `coverage.function` with `include_source_rows=true` for partially-covered functions
      to see which branches/lines were missed.
   4. Call `coverage.get_source` to view the actual uncovered code.
   5. Present a prioritized list of specific test-gap recommendations with file + line references.

## Guardrails

**Scope**
- All coverage actions are read-only; no file is written, no project is modified,
  and no S32 Design Studio process is started.
- Do not call configurator actions (`configurator.*`) from this skill.

**Destructive actions**
- None. `coverage.load` writes only to an in-memory session cache keyed by `session_id`;
  it does not touch any file.

**Secrets**
- No secrets or PII are involved; no redaction required.

**Refuse-and-escalate**
- `coverage.load` returns `error`: report the message verbatim and ask the user to
  verify the file paths.
- `source.available` is `false` after load: source paths in the `.flatprofiler` do not
  match the local tree; ask the user for the correct `source_root` or `extra_source_roots`.
- `coverage.function` returns `found: false`: confirm the exact symbol name using
  `coverage.uncovered` first.
- Path escape: `coverage.get_source` will refuse to read files outside the declared
  source roots; do not attempt to bypass this by constructing absolute paths that leave
  the root.
- Stale `session_id`: if an action returns "Coverage session ... not found", the MCP
  server was restarted; call `coverage.load` again and record the new `session_id`.

**Resource limits**
- Default `top_k` for `uncovered` is 20 and for `hotspots` is 10. Increase only when
  the user explicitly asks for more; never return unbounded results.
- `get_source` hard-limits snippets to 50 lines regardless of `snippet_window`.

**`_No source info` bucket**
- Functions with no DWARF source info (libc, newlib, startup, semihosting stubs) are
  grouped under `_No source info` and excluded from all aggregate queries by default.
  Set `include_no_source_info=true` to include them. Never include them unless the user
  explicitly asks about libc or runtime coverage.

## Validation loop

1. After `coverage.load`, verify `file_count > 0`, `function_count > 0`, and
   (when `source_root` was given) `source.available: true`.
2. After `coverage.summary`, confirm `overall.total_functions > 0`.
3. Pass criterion: `session_id` is in hand and the load summary matches the
   user's expectations (correct core, function count, source available).

## Out of scope

- Creating or editing S32Trace configuration XML (use `s32trace-create-configuration`).
- Trace event analysis from a decoded CSV (use `s32trace-analyze-trace`).
- Installing or updating S32 Design Studio.
- Compiling, flashing, or debugging firmware.
- Generating code from a `.mex` file (use `s32ct-generate-code`).

## See Also

- `search_actions(query="coverage")` -- returns the full parameter schema for
  all 7 `coverage.*` actions.
- `s32trace-analyze-trace` -- sibling skill for trace event / timing analysis.
- `s32trace-create-configuration` -- skill for configuring the trace capture.
