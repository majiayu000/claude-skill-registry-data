---
description: "Branch this Claude Code session into a new cmux split. Current pane keeps running; new pane resumes a clone of the transcript. Use when asked to 'branch this session', 'split this off into a new pane', or invoked as '/branch'."
user-invocable: true
---

# Branch Session

Branch the current Claude Code session into a new cmux split so two divergent threads can run side-by-side. The current pane keeps running the original session; the new pane resumes a clone of the transcript.

## Prerequisites

Must run inside a cmux terminal (script checks `CMUX_WORKSPACE_ID`). `cmux` CLI must be on `PATH`.

## Process

Run the worker script shipped with this plugin:

```bash
bash "${CLAUDE_PLUGIN_DIR}/scripts/branch.sh"
```

The script will:

1. Locate the current session transcript under `~/.claude/projects/<cwd>/<uuid>.jsonl` (most-recently-modified `.jsonl` in the project dir).
2. Clone the transcript to a fresh UUID and rewrite the inner `sessionId` field on every line.
3. Open a new cmux pane below the current one (`cmux new-pane --direction down`).
4. Send `claude --resume <new-uuid>` into the new pane.

After the script returns, report the original and branched session IDs to the user.

## Caveats

- Picks the most-recently modified `.jsonl` in the project dir as "the current session." If multiple concurrent Claude Code sessions write to the same project dir, the heuristic can pick the wrong one.
- The new pane's surface ref is parsed from `cmux new-pane` stdout. If the output format changes, the script falls back to sending to the focused surface (still correct because `--focus true` is set on the new pane).
