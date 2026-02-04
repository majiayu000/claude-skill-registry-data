---
name: looper-live-test
description: Run a live Looper smoke test by creating a temporary project (PROJECT.md + to-do.json), executing looper for one iteration, observing output, and reporting results. Use when verifying looper behavior or demonstrating a live run.
---

# Looper Live Test

## Overview

Run a real looper iteration in a fresh temp directory to validate task selection and summary application, then report what happened.

## Workflow

1. Locate a `looper.sh` executable. Prefer `looper.sh` on PATH; otherwise set `LOOPER_BIN` to a specific path (for example `~/looper/bin/looper.sh`).
2. Run the helper script: `~/.codex/skills/looper-live-test/scripts/run-live-test.sh`
3. Watch the output until it finishes; note the `Task:` line and `Summary:` line.
4. Inspect the temp project directory printed by the script; check `to-do.json` and any created files.
5. Report: selected task line, summary line, files created, and any errors or unexpected behavior. Mention the temp dir path.

## Manual fallback (only if the script cannot run)

1. Create a temp directory and `PROJECT.md`.
2. Create a `to-do.json` with tasks `T10` and `T2` (both priority 1).
3. Run: `CODEX_JSON_LOG=0 LOOPER_GIT_INIT=0 MAX_ITERATIONS=1 looper.sh to-do.json`
4. Observe output, then inspect `to-do.json` and created files.
