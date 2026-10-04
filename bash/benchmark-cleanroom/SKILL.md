---
name: benchmark-cleanroom
description: >
  Installable benchmark cleanup skill bundle for OpenClaw / DebateClaw /
  ChemQA benchmark runs. Use when benchmark scripts need post-run process
  finalization after a run leaves behind OpenClaw, openclaw-agent, or driver
  processes. Session files, session stores, manifests, and run artifacts are
  retained for audit.
---

# Benchmark Cleanroom

This directory is an installable skill bundle.

Treat the directory containing this `SKILL.md` as `<skill-root>`.
All scripts and references needed to clean benchmark runtime state live inside
 this bundle.

## Purpose

Use this bundle to stop run-scoped benchmark processes after a benchmark run
finishes or fails:

- benchmark driver / worker processes
- detached `openclaw` / `openclaw-agent` runtime children

The cleaner intentionally preserves:

- OpenClaw session files and `sessions.json` entries
- run-scoped DebateClaw / ChemQA control and generated artifacts
- run-scoped ClawTeam task/team data
- manifests, leases, cleanup reports, and benchmark output directories

Default posture:

- clean only the current run
- use graceful terminate first, then hard kill on timeout
- fail closed when live processes remain
- retain runtime evidence so session isolation, tool use, and final answers can be audited after the run

## Main entrypoint

Preferred automatic entrypoint:

```bash
python3 <skill-root>/scripts/cleanup_benchmark_run.py --manifest <manifest.json> --json
```

Manual fallback entrypoint:

```bash
python3 <skill-root>/scripts/cleanup_benchmark_run.py \
  --run-id <run-id> \
  --kind chemqa \
  --output-root <output-root> \
  --json
```

## Runtime metadata

This bundle works from two runtime surfaces:

- cleanup manifest: one JSON file per benchmark run
- runtime leases: one JSON file per live run-scoped process

Read `references/runtime-surfaces.md` when you need the exact fields or process coverage.

## Operating rules

- Only target the run described by the manifest or explicit `run_id`.
- Do not remove shared agent/model configuration.
- Do not reset unrelated slot workspaces.
- Do not remove session stores, transcripts, run artifacts, manifests, leases, or cleanup reports.
- Consider cleanup failed if the target run still has live processes after post-check.
- Cleanup must stay idempotent. Re-running it should return a stable report.
