---
name: looper-live-test
description: Run a live Looper-Go smoke test by creating a temporary project (PROJECT.md + to-do.json), executing looper for one iteration, observing output, and reporting results. Use when verifying looper-go behavior or demonstrating a live run.
---

# Looper-Go Live Test

## Overview

Run a real looper-go iteration in a fresh temp directory to validate task selection and summary application, then report what happened.

## Workflow

1. Locate the `looper` binary. Prefer `looper` on PATH; otherwise set `LOOPER_BIN` to a specific path (for example `~/looper-go/bin/looper` or `go run github.com/nibzard/looper-go/cmd/looper`).
2. Run the helper script: `~/.codex/skills/looper-live-test/scripts/run-live-test.sh`
3. Watch the output until it finishes; note the `Task:` line and `Summary:` line.
4. Inspect the temp project directory printed by the script; check `to-do.json` and any created files.
5. Report: selected task line, summary line, files created, and any errors or unexpected behavior. Mention the temp dir path.

## Manual fallback (only if the script cannot run)

1. Create a temp directory and `PROJECT.md`.
2. Create a `to-do.json` with tasks `T10` and `T2` (both priority 1).
3. Run: `MAX_ITERATIONS=1 looper run`
4. Observe output, then inspect `to-do.json` and created files.

## Looper-Go Specific Notes

- Looper-Go uses `looper run` as the main command (not `looper.sh to-do.json`)
- Configuration is loaded from `.looper/config.json`, environment, or CLI flags
- Logs are stored in `looper-logs/runs/<run-id>/events.jsonl`
- Use `looper doctor` to check dependencies and configuration
