---
name: uefn-profiling
description: Measures a UEFN map's performance through the MCP (Spatial Profiler metrics and hotspots, Insights trace captures and memory snapshots) and turns the numbers into a short list of fixes. Use when the owner says lag, fps, hitch, performance, memory, profile, budget, hotspot, or before a publish that must stay under budget.
kind: discipline
last_reviewed: 2026-11-03
sources: [UEFN 43.00 MCP tools read in the editor; Epic's 43.00 release notes]
---

# Profiling a map through the MCP

Two families exist. **Spatial Profiler** samples quantity metrics per area of the map and compares them with their budget: it answers "where is the map over budget". **Insights** records a trace file (or a memory snapshot) from a running client or server: it answers "what took the time". Both need a running play session to give real data; without one they only list what is ready.

What was checked in the editor: the listing tools answer without a session (sources, metrics, sampling state, targets). Starting a sampling, a capture or a snapshot has **not** been run yet: treat those steps as untested and say so in the report.

## When to use
- The owner reports lag, hitches or memory trouble, or the delivery gate warns about the budget.
- Before a publish of a map with many devices, props or effects.

**When not to use:** a rule-of-thumb review of a plan (use `performance-uefn-checklist`), a Verse logic error, anything that can be answered by reading the map.

## Workflow
1. Ask for a play session: nothing real is measured in edit mode. Do not start one yourself without the owner's word; use the editor's own play button or the session tools only when the owner asked.
2. List first, read only: sources (`ListSources`, `ListClients`), the metrics a source reports (`ListMetrics`: name, budget, enabled), the sampling state (`GetSamplingStatus`), the Insights targets (`ListTargets`: call it twice, the first call only starts the discovery).
3. Choose few metrics and enable only those (`SetEnabledMetrics`), then start sampling, play the heavy part of the map for a minute, stop sampling.
4. Read the result: `GetMetricStats` for the totals, `GetMetricHotspots` for the worst areas, worst first. Hotspots can be large: ask for a small `maxResults`.
5. For a time problem record a trace (`StartCapture`, `StopCapture`, read `GetCaptureStatus`); for memory take a snapshot (`TakeSnapshot`). The files go to the profiling folder (`ListSavedCaptures` shows them). Reading a trace is done by a person in the Insights window; say where the file is.
6. Report: the metric, the number, the budget, the area, one suggested fix (fewer devices there, a lighter effect, fewer simultaneous AI). Never change the map because of a measurement without the owner's yes.

## Rules (symptom, cause, remedy)
- `ListTargets` says discovery just started: call it again.
- Empty lists: no session is running; ask for one.
- Samples from an older run mix in: clear them (`ClearSamples`) before a new run, and say you did.
- `GetMetricHotspots`: it was the last call before the editor stopped in one lab run (cause not proven). Call it only with the owner ready, a session running and a small `maxResults`; if the editor stops answering, do not repeat it and tell the owner.
- A trace or snapshot is a file on disk: do not paste its content, give its path.
- Memory is judged in MB against the budget the editor shows (see `uefn-version-upgrade`), not in a percent.

Metric and tool names change between releases: look them up with `mcp_map.py --find profil` before you call them.
