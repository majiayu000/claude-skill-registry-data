---
name: dftracer-trace-utils
description: TOP PRIORITY — always use dftracer MCP utils tools for any trace work; never use raw bash/python/gzip scripts to read or process .pfw/.pfw.gz files
priority: critical
---

# TOP PRIORITY: Use MCP Tools for All Trace Work

**This rule overrides any default tendency to use `cat`, `python3 -c`, `gzip.open`,
`json.loads`, `grep`, or bash pipelines on trace files.**

Every time you need to read, query, filter, or count events in a `.pfw` or `.pfw.gz`
file — reach for `mcp__dftracer__view` first.  Only fall back to bash if the tool
is genuinely down or cannot do the specific task.

---

## Primary tool: `mcp__dftracer__view` — for all reading and querying

`dftracer_view` is the correct tool for **every** trace read operation.  It uses
bloom-filter indices for fast chunk-skipping, correctly resolves FH hash→filename
mappings, and handles cross-chunk events transparently.

### Query DSL — field reference

| Field | Type | Example |
|-------|------|---------|
| `cat` | string | `cat == "POSIX"` |
| `name` | string | `name == "open"` |
| `dur` | int (µs) | `dur > 1000` |
| `ph` | string | `ph == "X"` |
| `pid` | int | `pid == 1234` |
| `tid` | int | `tid == 1235` |
| `ts` | int (µs) | `ts > 1000000` |
| `args.comp` | string | `args.comp == "io"` |
| `args.fhash` | string | `args.fhash == "abc123"` |
| `args.flags` | int | `args.flags == 66` |

**Operators:** `==`  `!=`  `>`  `<`  `>=`  `<=`

**Boolean:** `and` (lowercase) · `OR` (uppercase)

**CRITICAL — strings are case-sensitive:** `"POSIX"` ✓ · `"posix"` ✗

### Confirmed working query examples

```python
# All POSIX events
mcp__dftracer__view(directory=SPLIT, query='cat == "POSIX"')

# POSIX opens only
mcp__dftracer__view(directory=SPLIT, query='cat == "POSIX" and name == "open"')

# POSIX OR STDIO
mcp__dftracer__view(directory=SPLIT, query='cat == "POSIX" OR cat == "STDIO"')

# Slow events only (> 1 ms)
mcp__dftracer__view(directory=SPLIT, query='cat == "POSIX" and dur > 1000')

# C_APP spans annotated as I/O
mcp__dftracer__view(directory=SPLIT, query='cat == "C_APP" and args.comp == "io"')

# Everything except dftracer metadata
mcp__dftracer__view(directory=SPLIT, query='cat != "dftracer"', no_metadata=True)
```

### Presets

```python
mcp__dftracer__view(directory=SPLIT, preset="io")       # STDIO-level I/O events
mcp__dftracer__view(directory=SPLIT, preset="compute")  # C_APP compute spans
mcp__dftracer__view(directory=SPLIT, preset="dlio")     # deep-learning I/O
```

### Time and duration filters

```python
# Events in first 500 ms (time in microseconds)
mcp__dftracer__view(directory=SPLIT, time_range="0,500000")

# Events longer than 10 ms
mcp__dftracer__view(directory=SPLIT, min_duration=10000)

# Events shorter than 1 ms
mcp__dftracer__view(directory=SPLIT, max_duration=1000)
```

### Output control

```python
# Default: no_metadata=True — strips ph=M hash-mapping events, returns only span events
mcp__dftracer__view(directory=SPLIT, query='cat == "POSIX"')

# Include FH (file-hash→path) events for filename resolution
mcp__dftracer__view(directory=SPLIT, query='cat == "POSIX"', no_metadata=False)

# Save to file instead of stdout
mcp__dftracer__view(directory=SPLIT, query='cat == "POSIX"', output_file="/tmp/posix.ndjson")

# Stream events as they match (good for large traces)
mcp__dftracer__view(directory=SPLIT, query='cat == "POSIX"', stream=True)
```

### Output format

Returns NDJSON — one JSON object per line:
```json
{"id":45,"name":"open","cat":"POSIX","pid":3112,"tid":3117,"ts":1781809100984435,"dur":3,"ph":"X","args":{"hhash":"96567aa8c9616994","flags":2,"fhash":"ba42359754857e43"}}
```

The summary line (`View: custom | Files: 1 | Chunks: scanned=1 skipped=0 | Events: matched=3 scanned=1190`)
goes to stderr and is not returned.

---

## Full tool mapping

| Task | USE THIS tool | Never do this |
|------|--------------|---------------|
| **Read / query events** | `mcp__dftracer__view` | `gzip.open` + `json.loads` loop |
| **Count events by category** | `mcp__dftracer__event_count` | `grep -c` or gzip+json loop |
| **Compare two runs** | `mcp__dftracer__comparator` | pandas scripts |
| **Summarise I/O stats** | `mcp__dftracer__info` | `dftracer_info` via bash |
| **Per-function / per-file stats** | `mcp__dftracer__stats` | manual aggregation |
| **Diagnose bottlenecks** | `mcp__dftracer__diagnose` | reading parquet directly |
| **Aggregate across files** | `mcp__dftracer__aggregator` | looping over .pfw.gz |
| **Show call tree** | `mcp__dftracer__call_tree` | reconstructing spans manually |
| **Split raw traces** | `mcp__dftracer__split` | `dftracer_split` CLI directly |
| **Merge trace directories** | `mcp__dftracer__merge` | `cp` + manual rename |
| **Build index** | `mcp__dftracer__index` | skipping and scanning raw |
| **Plot timeline** | `mcp__dftracer__plot` | matplotlib scripts |

---

## comparator — key patterns

```python
# Always use group_by_dims as a SINGLE comma-separated string
mcp__dftracer__comparator(
    baseline=PREV_SPLIT,
    variant=CUR_SPLIT,
    query='cat == "POSIX" OR cat == "STDIO" OR cat == "C_APP"',
    group_by_dims="cat,name",   # single string — NOT multiple args
    output_format="table",      # "table" for display, "json" for programmatic
    threshold_pct=5.0,
)
```

Significance: `~`=NEGLIGIBLE · `*`=SMALL · `**`=MEDIUM · `***`=LARGE (Cohen's d).
Single-run comparisons always show `~` — run multiple reps for statistical power.

The `session_optimization_iteration` tool automatically compares `opt{N-1}/traces_split`
vs `opt{N}/traces_split` and saves the result to `opt{N}/comparison.json` — no manual
comparator call needed inside the optimization loop.

---

## Known bugs / fixes

| Bug | Fix applied |
|-----|-------------|
| `--group-by` duplicate flags | `dftracer_utils_service.py` now passes `--group-by "cat,name"` as single arg |
| `no_metadata` parameter ignored in `view` | Fixed — `no_metadata=True` is now the default and is correctly forwarded |
| Direct gzip parsing shows `?` for filenames | Use `mcp__dftracer__view(no_metadata=False)` to get FH events with filename resolution |

---

## Fallback rule

Only use bash/CLI to process traces if:
1. The required MCP tool is explicitly unavailable (server down, tool missing), AND
2. You inform the user of the fallback

Even then, prefer `dftracer_view` / `dftracer_comparator` CLI binaries over raw
`gzip.open` + `json.loads` parsing.
