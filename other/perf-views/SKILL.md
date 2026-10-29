---
name: perf-views
description: Show where time goes as an inline ASCII waterfall, with Perfetto, speedscope, and flamegraph exports.
disable-model-invocation: true
---

# Performance views

A view is only as honest as its spans. Capture first, then render, then say
what the numbers do and do not cover.

## 1. Capture spans

Pick the cheapest capture that sees every stage you will report. Read
[capture](references/capture.md) for the three patterns: wrapper tracing inside
the process, a relay at a process boundary, and repeated runs for launcher cost.

- Time in-process work and process launch separately. Launch (interpreter,
  `uv`, Node CLIs) has its own cold and warm numbers; record both.
- Measure live systems with read-only modes. A stage that would mutate state is
  estimated from a comparable measurement and marked `"estimated": true`.
- Warm caches with one throwaway run, then record at least five runs. Report
  the median, and keep the spread for step 5.

Done when every stage on the path has a span or an explicit estimate, and the
launcher has a cold and a warm figure.

## 2. Write the span JSON

One file, one time origin, one unit:

```json
{"title": "⌥F on a local pane (live Mac, warm)", "unit": "ms",
 "spans": [{"name": "launcher", "start": 0, "end": 51},
           {"name": "rpc aiVault.listSessions", "start": 85, "end": 770},
           {"name": "cli terminal split", "start": 770, "end": 940, "estimated": true}],
 "marks": [{"name": "focus captured", "at": 83}],
 "notes": ["cold uv start adds ~250 ms"]}
```

Spans on one `track` nest by time containment; put concurrent work (another
process, a server) on its own `track`. Marks are the moments a reader cares
about, such as "focus captured" or "first byte".

Time a parent spends outside its children is unattributed. When it is large,
add one `(unattributed)` child span per gap and report it as a finding.

Done when the file renders in step 3 without an error and every stage from
step 1 appears in it.

## 3. Render the waterfall

Set `SKILL_DIR` to this skill's directory and run from the project, so span
and export paths stay relative to it:

```sh
python3 -I "$SKILL_DIR/scripts/perf-view" spans.json   # ASCII view on stdout
python3 -I "$SKILL_DIR/scripts/perf-view" spans.json --width 80 --chrome trace.json --speedscope profile.json --folded stacks.folded
```

Paste the ASCII view in a fenced block. `█` is measured, `░` estimated, `│` a
zero-length span; marks render as `▲` under the axis. Done when the view shows every span, the marks,
and the notes for cold/warm and environment.

## 4. Export when the reader needs to explore

Choose by question; [formats](references/formats.md) has each format's contract
and how to open it:

- **Perfetto UI / chrome://tracing** (`--chrome`): timelines across tracks and
  marks; SQL over slices in Perfetto.
- **speedscope** (`--speedscope`): one profile per track, with time-order,
  left-heavy, and sandwich views.
- **Flamegraph** (`--folded`): aggregate self time by stack, for "which stage
  dominates" across many runs.

Sampled profiles (pprof, py-spy, perf) already carry stacks; open them in their
own viewers (`go tool pprof -http=:0 profile.out`, or drop them into
speedscope) rather than converting them to spans.

Done when each file the reader needs is written and its path is in the report.

## 5. Report

State with the view:

- what was measured, where (host, OS, versions), and how many runs;
- which spans are estimates and from what;
- the comparison baseline, when one exists (for example the trunk build);
- what the environment can hide. A Linux container does not reproduce macOS
  process-launch costs.
- the pacing: drive the path at the speed a person or real client does. A
  request fired 0 ms after the previous one measures a race nobody can hit.

Done when a reader could rerun the measurement from the report alone.
