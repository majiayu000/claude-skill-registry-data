---
name: codex-session-history
slug: codex-session-history
version: 1.0.0
description: List and inspect local Codex session history by reading `~/.codex/session_index.jsonl`, `~/.codex/sessions/`, and `~/.codex/archived_sessions/`. Default to unarchived sessions in `~/.codex/sessions/`. Use when users ask what Codex sessions exist, want each session's id or title, need to know which project or workspace a session belongs to, or want to filter sessions by project name, session id, active versus archived status, or a local time window such as "today from 11:00 to 12:00".
metadata: {"openclaw":{"emoji":"🧭","requires":{"bins":["python3"]},"os":["darwin","linux"]}}
---

# Codex Session History

## Overview

Use this skill to enumerate local Codex sessions and map each session to its id, title, project, and workspace path.
Prefer the bundled script so the output stays consistent and works even when `session_index.jsonl` is incomplete.

## Workflow

1. Run the script to collect unarchived sessions by default.
2. Use `session_meta.payload.id` as the canonical session id.
3. Use `session_meta.payload.cwd` as the workspace anchor.
4. Derive the project from the Git root when possible; otherwise fall back to `cwd`.
5. Use `session_index.jsonl` only as enrichment for `thread_name` and `updated_at`.
6. Convert stored UTC timestamps into local time before display and time-window filtering.
7. If no `thread_name` is available, fall back to the first user message summary.

## Commands

List recent sessions:

```bash
python3 scripts/list_codex_sessions.py
```

List active and archived sessions together:

```bash
python3 scripts/list_codex_sessions.py --source all
```

List more rows:

```bash
python3 scripts/list_codex_sessions.py --limit 50
```

Filter by project:

```bash
python3 scripts/list_codex_sessions.py --project PlayGround
```

Filter by a local time window on today's date:

```bash
python3 scripts/list_codex_sessions.py --from 11:00 --to 12:00
```

Filter by a local time window on a specific date:

```bash
python3 scripts/list_codex_sessions.py --date 2026-03-19 --from 11:00 --to 12:00
```

Inspect one session id:

```bash
python3 scripts/list_codex_sessions.py --session-id 019ce206-aa11-7c81-a65a-fece3708ecf4 --details
```

Only show archived sessions:

```bash
python3 scripts/list_codex_sessions.py --source archived
```

Return JSON:

```bash
python3 scripts/list_codex_sessions.py --json
```

## Output

Default table columns:

- `id`
- `project`
- `started_at`
- `updated_at`
- `source`
- `title`

With `--details`, also show:

- `matched_from`
- `matched_to`
- `cwd`
- `project_path`
- `started_at`
- `session_file`
- `first_user_message`

## Notes

- Prefer the script over ad hoc `rg` because `session_index.jsonl` may be incomplete.
- Treat the session file itself as the source of truth for `id` and `cwd`.
- `started_at` and `updated_at` are displayed in local time, not raw `Z` time.
- Time-window filters match actual session events inside the requested interval, not only broad session span coverage.
- If a workspace no longer exists on disk, still report the recorded `cwd`.
- When the user only asks for "有哪些会话、id 是什么、属于哪个项目", the default table is enough.

## Script

Use:

```bash
python3 scripts/list_codex_sessions.py --help
```
