---
name: codex-session-history
description: Search Codex local session history stored in SQLite and session_index.jsonl. Use this skill when the user wants to list, search, filter, or inspect locally saved Codex sessions by session id, provider, time range, preview text, thread name, or archived status.
---

# Codex Session History

Use the bundled CLI to inspect local Codex session history. The script reads:

- `state_*.sqlite` for persisted thread metadata
- `session_index.jsonl` for the latest user-facing thread names

The script auto-discovers the newest state database under `CODEX_SQLITE_HOME`, the configured `sqlite_home`, or `~/.codex`.

## Primary Command

Run:

```bash
python3 scripts/codex_session_history.py --limit 30
```

The default `cards` view shows:

- full `session_id`
- provider and source
- created and updated timestamps
- thread name, title, and preview
- cwd
- a ready-to-run `codex resume <session_id>` command

## Common Queries

Search by preview, title, id, provider, cwd, or thread name:

```bash
python3 scripts/codex_session_history.py --query "resume provider"
```

Show the newest sessions in a compact table:

```bash
python3 scripts/codex_session_history.py --view table --limit 50
```

Filter by provider:

```bash
python3 scripts/codex_session_history.py --provider openai --provider staticflow
```

Filter by time:

```bash
python3 scripts/codex_session_history.py --since 7d
python3 scripts/codex_session_history.py --sort-by created --since 2026-03-01 --until 2026-03-10
```

Include archived-only sessions:

```bash
python3 scripts/codex_session_history.py --archived only
```

Emit JSON for piping or ad hoc analysis:

```bash
python3 scripts/codex_session_history.py --view json --limit 200
```

## Time Filters

`--since` and `--until` accept:

- ISO timestamps like `2026-03-23T15:30:00`
- dates like `2026-03-23`
- epoch seconds
- relative values like `30m`, `12h`, `7d`, `2w`
- `today`, `yesterday`, `now`

## Notes

- `preview` is the stored first user message, not a generated conversation summary.
- `thread_name` comes from `session_index.jsonl` and may be missing.
- If the user wants to continue a session after locating it, run `codex resume <session_id>`.
- If auto-discovery fails, pass `--db /path/to/state_5.sqlite` or `--codex-home /path/to/.codex`.
