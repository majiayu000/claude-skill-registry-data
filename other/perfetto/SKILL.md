---
name: perfetto
description: Use when the user wants to view, inspect, or share Perfetto/Chrome trace files -- triggered by words like "trace", "perf", "perfetto", "profiling", "trace viewer", or when dealing with trace JSON files from training runs.
version: 1.0.0
---

# Perfetto Trace Viewer

Generate links to the CharlieBot built-in Perfetto trace viewer, which can merge **cross-rank**
traces of the same time window into a single view.

## Endpoints

All URLs use `<base_url>` where `<base_url>` is the CharlieBot URL resolved from HOST MEMORY (look
for the **CharlieBot URL** entry).

### Merge cross-rank traces from a directory

```
<base_url>/perfetto?dir=<absolute-path>
```

Auto-discovers all `*.json` trace files in the directory, merges them client-side (labeling by
rank), and loads into an embedded Perfetto UI.

**Use `?dir=` only for cross-rank merging**, that is, when every file in the directory is a
different rank's trace of the **same** time window/step. The merger labels tracks by rank and
assumes one trace per rank; mixing multiple time windows of the same rank into one `?dir=` link will
produce a confusing/overlapping view.

If a directory contains multiple time windows (or multiple steps) for the same rank(s), generate
**separate** links, one per time window, each pointing at just that window's files. Use `?pattern=`
to scope a `?dir=` link to a single window, or list the per-rank files explicitly with repeated
`?trace=` params.

Optional params:
- `&pattern=<glob>`: file pattern to match (default: `*.json`); use this to isolate one time window
  in a mixed directory
- `&title=<text>`: custom page title

### View specific trace files

```
<base_url>/perfetto?trace=/absolute_filepath/<path1>&trace=/absolute_filepath/<path2>
```

Pass one or more `trace=` params, each naming a trace file the way the `file-server` skill writes a
file link.

### Single trace

```
<base_url>/perfetto?trace=/absolute_filepath/<absolute-path>
```

## Examples

| Scenario | URL |
|---|---|
| Cross-rank merge for one step | `<base_url>/perfetto?dir=/path/to/traces/step100` |
| Scope `?dir=` to one time window | `<base_url>/perfetto?dir=/path/to/traces&pattern=trace_rank*_step100.json` |
| Only rank 0 | `<base_url>/perfetto?trace=/absolute_filepath/path/to/traces/trace_rank000_step100.json` |
| Two time windows of rank 0 | generate **two separate links**, one per window, rather than one combined `?dir=` |

## Rules

- Only JSON traces can be merged; a protobuf trace shows only the first file.
