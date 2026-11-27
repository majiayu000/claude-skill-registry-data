---
name: session-save
description: Use when the user asks to save, snapshot, record or back up their open Claude Code sessions together with the tmux sessions, windows, panes and layouts they live in — typically before a shutdown, reboot or upgrade ("save my sessions", "snapshot my tmux layout"). The counterpart of session-restore.
user-invocable: true
argument-hint: "[--keep N]"
---

# session-save

Snapshot every open Claude Code session and its tmux surroundings so
`session-restore` can rebuild them after the machine restarts.

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/session-save.py" $ARGUMENTS
```

It writes:

| File | Purpose |
|---|---|
| `~/.claude-sessions.json` | the snapshot `session-restore` reads |
| `~/.claude-sessions.txt` | the same, human-readable, with a `claude --resume` line per session |
| `~/.claude/state/session-snapshots/<timestamp>.{json,txt}` | archive; newest 20 kept (`--keep N`) |

`--out-dir DIR` writes the two files to DIR instead and archives to
`DIR/session-snapshots/` (or `--archive-dir`), so a trial run never rotates
the real archive.

The script prints the files written, one line per Claude session
(`<tmux session>:<window> "<window name>": <title>`) and a summary line.
Relay those to the user. Do not paste the whole inventory unless asked.

## What gets recorded

Per tmux session → window (index, name, layout, active, zoomed) → pane
(index, cwd, active, position), each pane classified as:

- **lead** — a live Claude Code session: a registry entry
  `~/.claude/sessions/<pid>.json` whose `tmux` field
  (`<session>:@<window-id>.%<pane-id>`) ends in this pane's id AND whose
  process runs inside the pane (descends from the pane's process). Title is
  the transcript's last `customTitle`, else its last `aiTitle`, else the
  registry `name`.
- **teammate** — a process with `--agent-id`. Recorded, never restored: a
  teammate cannot be resumed on its own; its lead re-spawns what it needs.
- **dead** — a pane whose process exited but tmux kept it (`remain-on-exit`),
  e.g. a finished teammate. It has no pid; recorded, never restored.
- **pin** — a `/tmp/claude-pin` viewer pane. Transient, never restored.
- **shell** — anything else, with the command in the terminal's foreground
  (background jobs ignored; a pipeline recorded whole, `a | b`; empty for an
  idle shell).

Each window also gets an identity: the tmux window option `@restore_key`,
set on the first save if the window has none (the one thing save changes)
and recorded as `key`. `session-restore` re-applies it to the windows it
rebuilds, so it can tell a window is still open however it has since been
renamed or moved.

Claude sessions not in any tmux pane (or whose registry entry names a pane
they don't run in) are listed separately with their resume command. A window
shared by grouped sessions (`tmux new -t`) or `link-window` is recorded once,
under the session created first.

## Lessons from earlier snapshots

- The command "running in a pane" is the pane process itself unless that
  process is a shell; only then is it the shell's child. Reading the child
  of a non-shell pane mislabels teammates (their child is an MCP server).
- Window indexes are sparse (1, 2, 3, 9, 13); record them, don't renumber.
- A registry entry can outlive its process, and its pid can be reused: an
  entry counts only if the pid's executable is `claude`,
  `…/claude/versions/<ver>`, or node running `…/claude-code/cli.js`. A teammate also has a registry entry: skip
  pids whose command has `--agent-id`.
- Run it while the sessions are open: a closed session has no registry
  entry, so it is not recorded.
- Read everything with one `list-panes -a`: per-session/per-window calls
  race against windows closing (teammates come and go) and break on session
  names containing `.` or `:`, which tmux allows but cannot target.
- A registry pid can be reused by an unrelated process after a crash or
  reboot, and a second `claude` inherits `TMUX_PANE`: hence the
  descends-from-the-pane check rather than "pid is alive".
- The shell's "child" is not necessarily the foreground job: compare the
  process group with the terminal's (`pgid == tpgid`). tmux's
  `pane_current_command` names only a pipeline's first process.
- Record pane positions and sizes: restore needs them to keep a window's
  proportions when teammate or pin panes are dropped.
- Commands are recorded from `ps`, which drops argv quoting:
  `nvim "my file"` comes back as `nvim my file`. Restore only types it.

## Testing

`tests/test-session-save.sh` runs on a private tmux server (`tmux -L`) with a
fake `CLAUDE_HOME`; it never touches the real tmux server or `~/.claude`.
