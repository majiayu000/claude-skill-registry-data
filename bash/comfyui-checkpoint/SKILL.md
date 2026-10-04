---
name: comfyui-checkpoint
description: Saves and restores ComfyUI workflow snapshots indexed by session_id. Use before every agent invocation to freeze workflow state, and after any rewrite/debug step to record a recoverable version.
---

# comfyui-checkpoint

SQLite-backed workflow version store. Schema ported directly from
ComfyUI-Copilot `backend/dao/workflow_table.py:54-176` (Level A, §11) — same
columns (`session_id`, `workflow_data`, `workflow_data_ui`, `attributes`,
`created_at`), namespace changed, dependency on SQLAlchemy stripped in favor
of stdlib `sqlite3`.

## When to use

- **Before every high-value agent action**: the
  `.claude/settings.json:PreToolUse` hook `checkpoint_pre.py` is wired to
  both the `Write|Edit|NotebookEdit` matcher (file edits under
  `projects/<id>/inputs/`) AND the `Skill|Bash` matcher (capability Skill
  executions via `compile.py` / `submit_prompt.py` per
  `HIGH_VALUE_NEEDLES`). The hook's internal `is_high_value` filter
  ensures it only snapshots real high-value calls; non-matching
  `Skill|Bash` invocations pass through with `allow("not high-value")`.
  Checkpointing is default infrastructure, not opt-in (`plan_v1.md §9`).
- **After any rewrite/repair step**: so `repairing-workflows` can roll back.
- **On demand**: manual `save()` call from the host bridge via
  `host/bridge/checkpoint_client.py`.

## Scripts

| Script | Input | Output |
|---|---|---|
| `scripts/save.py` | **stdin JSON only**: `{session_id, workflow_data, workflow_data_ui?, attributes?}` — **does not accept CLI arguments** | `{version_id, created_at}` |
| `scripts/restore.py` | CLI flags: `--session-id SID` (latest for session) or `--version-id N` (specific row) | `{version_id, session_id, workflow_data, workflow_data_ui, attributes, created_at}` |

> **Host callers**: do not shell out to these scripts directly — use the
> Python wrapper at `host/bridge/checkpoint_client.py` (`save()` /
> `restore()` / `CheckpointError`). It speaks the stdin-JSON contract for
> `save.py` and the CLI-flag contract for `restore.py`, and raises a
> structured exception on any failure. Passing CLI flags to `save.py` is a
> historical bug — argparse would reject them and the script would write
> nothing.

## Storage

Single SQLite file at `ComfyUI-Agent/host/.cache/checkpoint.sqlite` (override
via `COMFYUI_AGENT_CHECKPOINT_DB`). Table `workflow_version`:

```sql
CREATE TABLE IF NOT EXISTS workflow_version (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    workflow_data TEXT NOT NULL,
    workflow_data_ui TEXT,
    attributes TEXT,
    created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_workflow_version_session ON workflow_version(session_id);
```

## References

- `knowledge/plans/v1/todo.md` §5.3 (Track C), §11 master table.
- `knowledge/workflows/ComfyUI-Copilot_workflow.md` §5.2.
