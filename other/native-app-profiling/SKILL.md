---
name: native-app-profiling
description: Profile native macOS/iOS apps for CPU hotspots, hangs, and hitches using Instruments traces. Use when asked to identify performance hotspots, profile CPU usage, or diagnose slow code paths without opening Instruments.
---

# Native App Performance Profiling

**This is a redirect skill.** This lacquer's Instruments trace recording and analysis workflow lives in `swiftui-expert-skill` — see its "Record a new Instruments trace" and "Trace-driven improvement" task-workflow sections, backed by `scripts/record_trace.py` and `scripts/analyze_trace.py` and documented in full in `references/trace-recording.md` and `references/trace-analysis.md`. That workflow already covers everything this skill used to teach manually: template selection by device kind, attach/launch/stop-file recording modes, and analysis with automatic symbolication, window scoping, main-thread coverage (`main_running_coverage_pct`), and SwiftUI cause-graph fan-in (`--fanin-for`).

Do not use raw `xcrun xctrace`, `atos`, `vmmap`, or `pgrep` for this. FlowDeck's ban on raw Apple CLI tools (`xcodebuild`, `xcrun`, `simctl`, `devicectl`) extends to Instruments tooling in this lacquer for the same reason — `record_trace.py`/`analyze_trace.py` wrap `xctrace` and handle symbolication automatically, so the manual `atos`/`vmmap` load-address dance this skill used to document is no longer part of the workflow.

## When this applies

Any request to profile CPU usage, find performance hotspots, or diagnose hangs/hitches in a native iOS/macOS app — whether or not the code under investigation is SwiftUI. `swiftui-expert-skill`'s trace workflow is not SwiftUI-specific for recording or the Time Profiler/Hangs/Animation Hitches lanes: only the `swiftui` and `swiftui-causes` analysis lanes are SwiftUI-specific, and they simply report `available: false` on non-SwiftUI code paths.

## Gotchas not covered elsewhere

These are the two items from the old manual workflow that remain relevant and aren't already documented in `swiftui-expert-skill`'s trace references:

- **Idle time produces empty data.** Trigger the slow code path *during* the recording window — profiling an idle app yields empty or low-signal traces regardless of capture duration.
- **Instruments permissions.** `xctrace` (wrapped by `record_trace.py`) may prompt for Developer Tools access or Full Disk Access on first use on a given machine, or require elevated privileges for certain system-wide captures. This is separate from the per-device signing/trust failure mode already documented in `references/trace-recording.md`.

Everything else — device/template selection, starting or stopping a recording, scoping analysis to a time window, interpreting coverage percentages, and mapping findings back to source files — is `swiftui-expert-skill`'s job. Follow its workflow directly rather than duplicating it here.

## Deprecation note

Every capability this skill used to teach (record, export, symbolicate, analyze) now has a strictly better equivalent in `swiftui-expert-skill`. This skill was kept as a short redirect rather than deleted outright, since removing a skill entirely is a bigger call than trimming its content — flagged here for a human decision on whether to fully retire `native-app-profiling` in a future pass.
