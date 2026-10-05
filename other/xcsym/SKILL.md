---
name: xcsym
description: Symbolicate and triage iOS/macOS crash reports (.ips, MetricKit, legacy .crash, Xcode Organizer .xccrashpoint) via the `xcsym` CLI. Use when given a crash file to diagnose, when TestFlight/App Store Connect crashes need triage, when a crash comes back unsymbolicated, or when asked what kind of crash something is.
---

# xcsym — Crash Symbolication

`xcsym` parses a crash report end-to-end (detect format → discover dSYMs → symbolicate via `atos` → categorize into a `pattern_tag`) and emits token-lean JSON, so triage is one call instead of the manual `atos`/dSYM-hunting dance. Use it instead of raw `atos` or `symbolicatecrash` for any `.ips`, MetricKit, `.crash`, or `.xccrashpoint` input — this fleet has no other crash-symbolication path today; `native-app-profiling`/`swiftui-expert-skill` cover live Instruments profiling, not post-mortem crash files.

## Resolving the binary

`xcsym` is not bundled with FlowDeck or RocketSim and ships no Homebrew formula or GitHub release — it's a zero-dependency Go module distributed as source inside [CharlesWiltgen/Axiom](https://github.com/CharlesWiltgen/Axiom) (`tools/xcsym/`, MIT). Resolve it once per machine:

1. `command -v xcsym` — if found, use it.
2. If not found, stop and tell the user to build it: `git clone --depth 1 https://github.com/CharlesWiltgen/Axiom /tmp/axiom-src && cd /tmp/axiom-src/tools/xcsym && go build -o xcsym . && sudo mv xcsym /usr/local/bin/` (or any directory on `PATH`). Do not attempt this yourself unless the user has already agreed to installing new tooling.

Don't confuse this with the full Axiom Claude Code plugin — this fleet deliberately did not adopt that (see `docs/references.md`); only the standalone `xcsym` binary is in use here.

## Core workflow

`crash` is the default entry point — it does everything in one call:

```bash
xcsym crash path/to/report.ips
```

- Auto-detects `.ips` (v1/v2), MetricKit JSON, legacy `.crash` text, and `.xccrashpoint` bundles (walks `Filters/Filter_*/Logs/` automatically, picks the most recent).
- Output is compact single-line JSON by default; add `--human` for terse prose, or pipe through `jq` for pretty-printing.
- Only reach for `resolve` (single-address lookup), `find-dsym` (UUID-driven dSYM search), `list-dsyms` (inventory), or `verify` (per-image UUID/arch diagnostics) when `crash` fails or you need one specific sub-step — see `references/xcsym-reference.md` for their flags.

Read the JSON result for:

- **`pattern_tag`** — the crash category (e.g. `swift_forced_unwrap`, `watchdog_termination`, `zombie_or_heap_corruption`); pair with `pattern_confidence` and `pattern_reason`.
- **`images.missing` / `images.mismatched`** — why symbolication is incomplete, if it is.
- Exit code — 0 is clean; non-zero codes name the *reason* (missing dSYM, UUID mismatch, arch mismatch, timeout, partial match), not a generic failure. Full table in the reference.

For the full subcommand reference, exit-code table, all 19 pattern tags, and the dSYM discovery order, see `references/xcsym-reference.md` — inline that only when the triage above isn't enough to explain a result.

## Triage template

1. Get the crash file (from Xcode Organizer's "Show in Finder", a TestFlight/App Store Connect download, or MetricKit payload).
2. `xcsym crash <file>` — read `pattern_tag` first, then check `images` for symbolication gaps.
3. If `images.missing` is non-empty: `xcsym list-dsyms` to see what's discoverable locally, or `xcsym find-dsym --uuid <uuid>` for a specific image.
4. If sharing the crash outside this session (a bug report, a test fixture), run `xcsym anonymize` first — it scrubs bundle IDs, process names, user paths, IPs, device names, and account IDs while preserving dSYM UUIDs, so the scrubbed file still symbolicates.
