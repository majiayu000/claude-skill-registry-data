---
name: ha:perf
description: Analyze Home Assistant performance — blocking I/O on the event loop, coordinator fan-out at fleet scale, Lit render bloat, memory leaks. Use when slowness, timeouts, or high memory reported.
effort: high
argument-hint: "[integration|module|component] [--focus coordinator|lit|asyncio]"
---

# Performance Analysis

Analyze code for performance issues across the coordinator (data-fetch), Lit
render, and asyncio runtime layers. Prioritize findings by impact and effort.

## Usage

```
/ha:perf                          # Analyze full project
/ha:perf homeassistant/components/mealie/coordinator.py    # Analyze specific module
/ha:perf --focus coordinator      # Coordinator fetch / fan-out only
/ha:perf --focus lit              # Lit component re-render bloat only (ha-frontend)
/ha:perf --focus asyncio          # Event-loop blocking / memory bottlenecks only
```

## Arguments

`$ARGUMENTS` = Optional module/component path and `--focus` flag.

## Iron Laws

1. **MEASURE BEFORE OPTIMIZING** — Never optimize without evidence of a problem
2. **EVENT LOOP FIRST** — the majority of HA performance problems are blocking
   I/O on the single event loop (P4), not raw CPU cost
3. **ONE CHANGE AT A TIME** — Isolate optimizations to measure impact
4. **NEVER measure a debug-mode instance** — Take timings against a normal
   `hass -c config` run, not one with the component's `logger` set to `debug`
   or the `profiler` integration's verbose tracing left on; debug logging and
   the runtime blocking-call detector's warnings add overhead that invalidates
   results. Enable the blocking-call detector to *find* violations; disable the
   extra logging to *measure* them.

## Workflow

### Step 1: Identify Scope

Check specific file if provided. Otherwise scan full project:

```bash
# Find hot paths: coordinators, entity platforms, service handlers
find homeassistant/components -name "*.py" | grep -v "/tests/" | head -50
```

### Step 2: Run Analysis Tracks

Spawn analysis agents in parallel based on focus:

**Coordinator Track** (default or `--focus coordinator`):

Spawn `home-assistant:coordinator-specialist` with prompt:
"Analyze the coordinator for performance at fleet scale: blocking I/O inside
`_async_update_data` (P4), sequential library calls that could be one
`asyncio.gather` — or a burst of parallel calls hammering one rate-limited
device/hub; an `update_interval` shorter than the data actually changes
(over-polling); per-entity refreshes that should be a single batched
coordinator fetch; parent/child coordinator fan-out that multiplies requests
as the number of devices grows. Check: library calls inside loops, `gather`
fanning N requests at one small device, missing batching, refresh cadence."

**Lit Track** (default or `--focus lit`):

Spawn `home-assistant:lit-architect` with prompt:
"Analyze `ha-*` Lit components for render bloat: work in `render()`/`willUpdate`
that fires on every unrelated `hass` change instead of being gated on
`changedProps.has(...)` (FS1); objects/arrays/schemas/functions built inside
`render()` instead of hoisted to module constants or memoized (F2); over-broad
`@state`; heavy objects stored directly in reactive properties; lists rendered
without `repeat()` and stable keys; large lists without `@lit-labs/virtualizer`;
memoization that reads `this.*` outside its arguments or is fed freshly-built
objects that defeat the cache (FS2)."

**Asyncio Runtime Track** (only with `--focus asyncio`):

Spawn `home-assistant:asyncio-advisor` with prompt:
"Analyze for event-loop and memory bottlenecks: blocking I/O on the loop (P4) —
sync library calls, `open()`, `requests.*`, `time.sleep`, `json.load` on a file,
module imports or `Path.exists` inside `async def`; CPU-heavy work that should
move to `hass.async_add_executor_job` (batched into one job, never many
concurrent); a coroutine that never awaits and should be `@callback` (PS19);
unbounded in-memory caches/dicts that grow without a cap; uncancelled
`async_track_time_interval`/listeners not torn down via `async_on_remove` (PS4)."

### Step 3: Prioritize Findings

Score each finding on a 2x2 matrix:

| | Low Effort | High Effort |
|---|---|---|
| **High Impact** | DO FIRST | PLAN |
| **Low Impact** | QUICK WIN | SKIP |

High impact = affects event-loop responsiveness, memory growth, or the number
of requests per update cycle. Low effort = single file change, no config-entry
migration needed.

### Step 4: Present Top 5

Present findings sorted by priority:

```markdown
## Performance Analysis: {scope}

### 1. {Finding} — DO FIRST
**Impact**: {what improves}
**Location**: {file}:{line}
**Current**: {problematic pattern}
**Fix**: {optimized pattern}
**Estimated gain**: {e.g., "moves blocking parse off the loop, unblocks all entities during refresh"}

### 2. {Finding} — PLAN
...
```

### Step 5: Offer Next Steps

Always end with actionable next steps — findings without follow-up
get lost. Present options based on severity:

```
How would you like to proceed?

- `/ha:plan` — Create a plan from these findings (recommended for 3+ fixes)
- `/ha:quick` — Apply top priority fix directly (1-2 simple fixes)
- `/ha:investigate` — Deep-dive into a specific finding
```

## Dev Instance Integration

If a dev instance is available (`hass -c config`, devcontainer):

- Enable the runtime blocking-call detector to surface P4 violations while
  exercising a code path — HA logs a warning with the offending frame when
  blocking I/O runs on the loop
- Attach `py-spy` to the running process (`py-spy top --pid <pid>`,
  `py-spy dump --pid <pid>`) to see where wall-clock time goes without editing code
- Inspect coordinator/cache sizes and `entry.runtime_data` live from the dev
  instance while reproducing the slow path

## References

- `${CLAUDE_SKILL_DIR}/references/benchmarking.md` — timeit / pytest-benchmark patterns, py-spy / cProfile profiling, blocking-call detection, flame graphs
