---
name: codex-session-recovery
description: Diagnose, privately back up, compact, verify, and hand off stalled or extremely slow Codex CLI sessions through the official app-server protocol. Use when a Codex resume/thread appears frozen, cold-loads a huge JSONL history, has excessive context or inline-image payloads, needs safe context compaction, or must preserve unfinished work without rewriting rollout JSONL or SQLite state.
---

# Codex Session Recovery

Recover the existing thread conservatively. Treat the rollout as private append-only evidence, not as a file to repair manually.

## Non-negotiable safety rules

- Read every applicable `AGENTS.md` before inspecting the project named by the thread.
- Never truncate, replace, reformat, or open a rollout JSONL for writing.
- Never update, copy, restore, or vacuum the live shared `state_*.sqlite` database.
- Never kill a Codex, tmux, IDE, or app-server process that already owns the rollout.
- Never bypass an unknown ownership result, missing backup, checksum failure, schema mismatch, or invalid JSON tail.
- Keep raw rollouts, backups, database files, prompts, tokens, and generated images outside Git repositories and skill folders.
- Change model or reasoning effort only when the user explicitly requests that exact change.
- Do not retry authentication, quota, or failed-compaction errors automatically.

## Use the bundled tool

Set the skill path once:

```bash
SKILL_DIR="${CODEX_HOME:-$HOME/.codex}/skills/codex-session-recovery"
RECOVERY="$SKILL_DIR/scripts/codex_session_recovery.py"
```

Run global options before the subcommand.

### 1. Check protocol compatibility

```bash
python3 "$RECOVERY" --json doctor
```

Require the generated app-server schema contract to pass. Treat the app-server as version-sensitive and fail closed when required methods or fields change.

### 2. Inspect without reading prompt text

```bash
python3 "$RECOVERY" --json inspect THREAD_UUID
python3 "$RECOVERY" --json inspect THREAD_UUID --scan
```

Use `--scan` only when aggregate rollout counts are useful; it streams the file without loading giant image lines into memory. Check:

- exact rollout path and size;
- newline and tail-JSON validity;
- active file owners;
- model, effort, and numeric token counters;
- generated-image footprint;
- optional compaction, abort, and inline-image counts.

If `ownership.owners` is non-empty, stop. Ask the user to finish, interrupt, close, or detach that session themselves, then inspect again.

### 3. Preview the mutation plan

```bash
python3 "$RECOVERY" --json recover THREAD_UUID --dry-run
```

The tool must resolve one active, regular, non-symlink, non-hardlinked rollout whose filename exactly matches the UUID under `$CODEX_HOME/sessions`.

### 4. Recover through supported APIs

```bash
python3 "$RECOVERY" --json recover THREAD_UUID --yes
```

This guarded sequence:

1. locks the recovery helper for that UUID;
2. proves that no external process owns the rollout;
3. creates a new private `0700` backup directory outside Git;
4. compresses the rollout and verifies both compressed and decompressed SHA-256 evidence;
5. re-attests device, inode, size, mtime, and SHA-256 immediately before resume;
6. resumes with `excludeTurns: true` through `codex app-server --disable hooks --stdio` and verifies the returned thread ID;
7. rechecks that only the tool-owned process group opened the rollout;
8. requests `thread/compact/start`;
9. requires the matching `contextCompaction` item start/completion and completed turn;
10. interrupts a known in-flight turn on timeout or protocol failure;
11. always proves the original file prefix is unchanged and only append-only data was added, including after an operation failure.

Backups default to:

```text
$CODEX_HOME/session-recovery-backups/THREAD_UUID/TIMESTAMP/
```

Do not put `--backup-dir` inside a repository.

### 5. Change effort only explicitly

When the user chooses a lower sticky effort to reduce subsequent latency:

```bash
python3 "$RECOVERY" --json recover THREAD_UUID --yes --effort medium
```

Report that the setting persists. If a later phase fails, report the partial setting change rather than pretending it rolled back.

JSON failures include a structured `partial` object with the verified backup, observed effort change, lifecycle result, interruption evidence, and postflight result when available.

### 6. Verify responsiveness

Cold-load without adding a model turn:

```bash
python3 "$RECOVERY" --json probe THREAD_UUID
```

Append a model canary only with explicit mutation consent:

```bash
python3 "$RECOVERY" --json canary THREAD_UUID --yes --expected SESSION_OK
```

Or add `--canary` to `recover`. A canary consumes quota and appends a user/assistant turn. Prompt instructions reduce tool risk but cannot make a model turn equivalent to a read-only operation.

### 7. Recheck a backup later

```bash
python3 "$RECOVERY" --json verify-backup \
  "$CODEX_HOME/session-recovery-backups/THREAD_UUID/TIMESTAMP/manifest.json"
```

Verify against the manifest, not against the now-appended live rollout.

## Interpret the result correctly

Supported compaction reduces model-visible history. It does not shrink the append-only rollout file. A recovered multi-gigabyte thread can answer normally after loading yet still take minutes to cold-open.

When cold-start latency remains unacceptable:

1. preserve the original thread as the archive;
2. write a curated handoff that contains only current tasks, verified facts, paths, and next actions;
3. keep raw private history in ignored/private storage;
4. continue in a fresh thread using the handoff.

Use `aginti-agentlink` conventions when multiple sessions or machines share the handoff.

## Stop conditions

Stop and report evidence when:

- the rollout is active, ambiguous, archived, symlinked, hardlinked, outside the active session root, or has an invalid tail;
- private backup creation or decompressed SHA verification fails;
- disk space is insufficient;
- the generated app-server schema is incompatible;
- resume, compaction lifecycle, or append-only verification fails;
- Codex returns authentication, authorization, quota, rate-limit, interrupted, or failed status.

Do not convert these failures into manual JSONL or SQLite surgery.

## Detailed reference

Read [references/recovery-playbook.md](references/recovery-playbook.md) when diagnosing a failure, reviewing protocol events, handling version drift, or preparing a safe handoff. Run the isolated fixture suite after changing the tool:

```bash
python3 -m py_compile "$SKILL_DIR/scripts/"*.py
python3 "$SKILL_DIR/scripts/test_codex_session_recovery.py"
```
