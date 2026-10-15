---
name: tmux
description: Run long-lived commands in detached tmux sessions; send keys; scrape pane output.
requires:
  bins: [tmux]
  env: []
---

# tmux

Use this skill when a command would block the agent loop: dev servers,
builds, watchers, SSH sessions, interactive tools. The agent creates a
detached session, feeds it keystrokes over time, and reads back
whatever is visible in the pane.

## Use when

- "Start the build in background and tell me when it's done"
- "Run the dev server and check for errors every 30s" (pair with heartbeat)
- "Tail this log" (periodic `capture_pane`)
- Interactive CLIs that need stdin (migrations, wizards)

## Do not use when

- A one-shot command — use a normal shell tool if you add one
- You need PTY reattach / interactive human control
- Running untrusted code — the session inherits the agent's own shell env

## Tools

### `status`
Returns bin path and socket location. Useful to confirm the extension is alive.

### `new_session { name, command? }`
Creates detached session. Names are `[A-Za-z0-9_-]{1,64}` — anything else
returns `-32602`. Initial command is optional.

### `send_keys { session, keys, enter? }`
Sends literal `keys`. `enter` defaults true (appends Enter). Useful for
feeding password prompts, REPL input, etc.

### `capture_pane { session, lines? }`
Reads the last N lines of the active pane (1..2000, default 200).
Returns one big string under `output`.

### `list_sessions`
Returns `[{name, created_unix, windows}, ...]`. Empty when the server
isn't running (not an error).

### `kill_session { session }`
Terminates the session. Idempotent-ish: calling twice errors on the second.

## Execution guidance

- Use short session names (`build`, `watch-42`) — makes operator
  inspection clean (`tmux -S <sock> attach -t build`).
- After `send_keys`, wait at least 200–500ms before `capture_pane` so the
  pane buffer has the response.
- `capture_pane` gives you *visible* text — ANSI escapes included. If the
  user only wants "did the build succeed?", grep for strings rather than
  dumping the whole buffer into the prompt.
- Kill old sessions explicitly: tmux doesn't auto-reap.
- The socket lives at `$TMUX_REMOTE_SOCKET` (default `/tmp/agent-rs-tmux.sock`);
  operator can tail with `tmux -S /tmp/agent-rs-tmux.sock ls`.
