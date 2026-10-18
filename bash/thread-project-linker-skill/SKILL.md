---
name: thread-project-linker
description: Reassign Codex threads to the correct project/workspace by updating both thread DB cwd metadata and rollout session metadata together. Use when a user asks to move one thread, bulk migrate active threads from an old folder/path to a new folder/path, or migrate selected deeplink thread IDs. Use --include-archived only when archived records must be moved too.
---

# Thread Project Linker

Migrate Codex thread-to-project mappings safely and repeatably.

Use the bundled script to keep both metadata stores in sync:
- `~/.codex/state_5.sqlite` (`threads.cwd`)
- thread rollout JSONL first line (`session_meta.payload.cwd`)

## Quick Start

Run from the skill folder:

```bash
cd "${CODEX_HOME:-$HOME/.codex}/skills/thread-project-linker"
```

Single thread to new project:

```bash
python3 scripts/reassign_thread.py \
  --thread codex://threads/<thread-id> \
  --project /absolute/path/to/new-project
```

Bulk migrate all threads from old project path:

```bash
python3 scripts/reassign_thread.py \
  --from /absolute/path/to/old-project \
  --to /absolute/path/to/new-project
```

Bulk migrate by previous folder name:

```bash
python3 scripts/reassign_thread.py \
  --from-name old-folder-name \
  --to /absolute/path/to/new-project
```

Bulk migrate only selected deeplink IDs:

```bash
python3 scripts/reassign_thread.py \
  --from-name old-folder-name \
  --to /absolute/path/to/new-project \
  --deeplink codex://threads/<thread-a> \
  --deeplink codex://threads/<thread-b>
```

Include archived threads too:

```bash
python3 scripts/reassign_thread.py \
  --from-name old-folder-name \
  --to /absolute/path/to/new-project \
  --include-archived
```

Dry run (no writes):

```bash
python3 scripts/reassign_thread.py \
  --from /absolute/path/to/old-project \
  --to /absolute/path/to/new-project \
  --dry-run
```

## Workflow

1. Parse thread IDs from `--thread` and `--deeplink`.
2. Resolve migration scope:
   - explicit IDs + `--project`
   - all threads from `--from` or `--from-name` + `--to`
   - active-only by default, unless `--include-archived` is provided
   - optional filtering by specified IDs in bulk mode
3. Validate each target thread and rollout file before writing.
4. Backup each rollout file.
5. Update rollout `session_meta.payload.cwd`.
6. Update DB `threads.cwd` in a transaction.
7. Verify DB + rollout values.
8. On failure, restore backups and restore DB cwd values.

## Guardrails

- Prefer `--dry-run` first on large bulk migrations.
- Use absolute paths for `--project`, `--from`, and `--to`.
- Archived threads are excluded unless `--include-archived` is passed.
- Keep generated backup files until you confirm the migration in Codex UI.
