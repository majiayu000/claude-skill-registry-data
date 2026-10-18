---
name: system-check
agent: none
description: Read-only installation smoke test for skills, daemons, operational memory, cognitive runtime, nightly freshness, terminal evidence, and unique route ownership.
allowed-tools: Bash, Read
user-invocable: true
triggers:
  - system check
  - smoke test
  - check wiring
  - is everything wired
  - audit install
  - runtime check
  - nightly health
  - /system-check
---

# /system-check

Run from the aigent-OS root:

```bash
bash daemons/system-check.sh
```

The script is read-only. It prints one line per check, a final
`SUMMARY: N PASS / N FAIL / N INFO`, and exits `1` when any check fails.

## Path resolution

Framework code resolves from `AIGENT_ROOT`, defaulting to the parent directory
of `daemons/system-check.sh`.

Operational memory resolves in this order:

1. `AIGENT_STATE_HOME_DIR/vault/memory` when the state-home diversion is set.
2. `AIGENT_STATE_HOME_DIR/memory` as a compatibility fallback.
3. `AIGENT_ROOT/vault/memory` for a normal installation.
4. `AIGENT_ROOT/memory` only when the canonical vault path does not exist.

This is the same shape used by the nightly controller. Tests should set
`AIGENT_ROOT`, `AIGENT_STATE_HOME_DIR`, and date-sensitive environment values
explicitly so ambient state cannot change the result.

## Checks

- Required top-level skills exist, including the nightly close-parity skills.
- Shell and Python daemons parse.
- Every nightly daemon exists and passes `node --check`.
- The memory-heat daemon parses.
- Operational state files have their required schemas, including the generic
  sweep log and dispatch-fitness table.
- Capsules have valid frontmatter, identity, and status.
- Canonical cognitive JSON and JSONL inputs exist and parse. Missing canonical
  input is a failure, not an empty-success case.
- `DREAM_LOG.md` freshness comes from its newest valid dated header, never its
  file modification time.
- The newest `NIGHTLY_LOG.md` pass is current and has complete terminal
  evidence. A terminal `status: FAIL` remains red even when every checkpoint
  row is present.
- `/nightly` resolves through the unique `/nightly-close-parity` route.
- The eval directory contains at least one supported file.
- The local daemon error log is surfaced as INFO when it contains entries.

## Date configuration

All date-sensitive checks use one timezone and one cutoff:

```bash
export AIGENT_NIGHTLY_TIME_ZONE="America/Los_Angeles"
export AIGENT_NIGHTLY_CUTOFF_HOUR="4"
bash daemons/system-check.sh
```

`America/Los_Angeles` and hour `4` are the defaults. Tests may pin the current
instant with `AIGENT_SYSTEM_CHECK_NOW`.

## What it does not do

- It does not repair files or resolve alerts.
- It invokes the route checker with alerts disabled.
- It invokes the watchdog in check-only mode, so `/system-check` never appends
  to the nightly alert ledger.
- It does not inspect a message bus, task board, browser profile, or private
  machine configuration.
