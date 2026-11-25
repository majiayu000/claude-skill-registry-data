---
name: control-cli
description: Build or adapt a local harness to drive, inspect, and profile an interactive CLI or TUI without external services. Use for CLI UX checks, startup regressions, memory leaks, hangs, prompt flows, or terminal demos.
---

# Control CLI

Use a repeatable local harness to exercise an interactive CLI instead of poking at it manually. First reuse the repo's own test/demo harness if it exists; otherwise assemble a temporary harness from standard local tools.

## What It Is Used For

- Reproducing CLI/TUI bugs with deterministic input.
- Verifying keyboard flows, prompts, interrupts, resize behavior, and terminal layout.
- Capturing before/after transcripts for bug fixes.
- Profiling startup time, slow operations, hangs, or memory growth.
- Recording a short terminal demo when output is easier to show than explain.

## Harness Loop

1. Identify the command under test and the smallest reproducible workspace.
2. Discover existing local harnesses: package scripts, e2e tests, demo recorders, expect scripts, or PTY helpers.
3. If no harness exists, launch the CLI in an isolated terminal session with deterministic env vars.
4. Capture the current screen before interacting.
5. Send one action at a time: text, Enter, arrows, Escape, Ctrl-C, resize.
6. Wait for a concrete screen pattern or prompt before the next action.
7. Save the transcript and any profile artifacts.
8. Kill the session cleanly.

## Harness Options

- Repo-native harness: prefer checked-in scripts because they know the app's startup, env, and prompts.
- `tmux`: managed sessions, `capture-pane`, `send-keys`, attach/detach.
- PTY probe: use a short Python, Node, or Expect script when tmux is unavailable.
- Runtime inspector: use Node or Bun inspector for CPU profiles, heap snapshots, and live evaluation.
- Terminal recorder: use repo-local demo tools or asciinema-compatible tools when the user asks for a demo.

## Minimal tmux Harness

```bash
SESSION="cli-harness-$(date +%s)"
tmux new-session -d -s "$SESSION" -- <command-under-test>
tmux capture-pane -pt "$SESSION"
tmux send-keys -t "$SESSION" "help" Enter
tmux capture-pane -pt "$SESSION"
tmux kill-session -t "$SESSION"
```

For Node CLIs:

```bash
NODE_OPTIONS="--inspect=127.0.0.1:0" tmux new-session -d -s "$SESSION" -- <node-cli-command>
```

Read the terminal output to find the inspector URL, then use Chrome DevTools-compatible tooling if profiling is needed.

## Minimal PTY Harness

Use a PTY script when you need deterministic waits in a repo that does not have tmux or a demo harness. Keep it temporary unless the user asks to add a reusable test.

```python
import os
import pty
import select
import subprocess
import time

master_fd, slave_fd = pty.openpty()
proc = subprocess.Popen(
    ["<command>", "<arg>"],
    stdin=slave_fd,
    stdout=slave_fd,
    stderr=slave_fd,
    close_fds=True,
)
os.close(slave_fd)

deadline = time.time() + 30
buffer = b""
while time.time() < deadline:
    ready, _, _ = select.select([master_fd], [], [], 0.25)
    if not ready:
        continue
    chunk = os.read(master_fd, 4096)
    buffer += chunk
    if b"<ready text>" in buffer:
        os.write(master_fd, b"help\n")
        break

print(buffer.decode(errors="replace"))
proc.terminate()
os.close(master_fd)
```

If the CLI needs richer terminal control, use `pty.fork()` or an existing PTY library.

## Windows

On Windows, tmux and Python's `pty` module are not available. Inside a Herdr app terminal (`HC_TERMINAL_ID` is set), use an `hc` terminal as the session. A REPL or TUI that stays up until you end it starts with `--rm`, so `hc kill` also removes its terminal:

```bash
hc_until() {
  local deadline=$((SECONDS + 30))
  until hc read "$1" --lines 40 | grep -qF -- "$2"; do
    [ "$SECONDS" -ge "$deadline" ] && { echo "no '$2' in $1 after 30 s" >&2; return 1; }
    sleep 1
  done
}
hc run --bg --rm --name <session> --cwd "$PWD" -- <command-under-test>
hc_until <session> '<ready text>'
hc send <session> 'help'
hc_until <session> '<reply>'
hc read <session> --lines 120
hc kill <session>
```

`hc wait --output` matches only output printed after the wait starts. A fast program prints its ready text before `hc run --bg` returns, and after `hc send` the reply is often on screen already, so a wait started then times out. A timed-out `hc wait` still exits 0, so nothing reports the miss. Poll `hc read` until the text appears, with a deadline, as `hc_until` does.

`hc send` pastes the text and presses Enter. For a bare key, such as a pager advance or an interrupt, use `hc keys <session> <key>`. In Git Bash, prefix `hc send` and `hc keys` with `MSYS_NO_PATHCONV=1`, or an argument that starts with `/` arrives as a Windows path, so `/model` becomes `C:/Program Files/Git/model`. To an agent terminal, `hc send` wraps the text in `<hc from=...>`, so a slash command never reaches the TUI as typed. `hc keys` takes only key names, one per argument, and `hc keys <session> /model` fails with `unknown key`. Type a slash command into an agent TUI one character per key, then Enter: `MSYS_NO_PATHCONV=1 hc keys <session> / m o d e l enter`.

With `--rm`, the terminal is removed as soon as its program ends. `hc kill` on a `--rm` terminal reports `not_found` and exits 3 even when the program was still running, so after `hc kill` on any `--rm` terminal, `not_found` means done.

A program that can exit on its own, such as a one-shot command or a dev server that can crash at boot, starts without `--rm`. With `--rm`, its terminal is gone when it exits, and `hc read` fails with `not_found`. Read it after `hc wait` returns, then remove its terminal:

```bash
hc run --bg --name <session> --cwd "$PWD" -- <command-under-test>
hc wait <session> --output '<ready text>' --timeout 10 --json
hc read <session> --lines 120
hc kill <session>
hc rm <session>
```

`hc wait --output` also returns when the program exits. If the ready text printed before the wait started, the wait runs to `--timeout`, so judge the run by what `hc read` shows, not by the wait's `reason`. That is why the wait is short. If the screen shows neither the ready text nor an exit, run the wait and the read again, up to 12 waits in all. If `hc kill` reports `not_found` or a finished terminal, the program already ended. Run `hc rm` anyway, or the terminal stays listed.

## Profiling Recipes

- Startup regression: capture baseline and treatment startup timings under the same machine, env, and command.
- Slow operation: start a CPU profile, perform the operation, stop the profile, and compare top self-time functions.
- Memory leak: force GC if available, take a heap snapshot, perform the operation repeatedly, force GC again, and take another snapshot.
- Hang: capture the screen, active handles/resources, and a stack/CPU sample before interrupting.

## Guardrails

- Prefer deterministic waits over sleeps. If you must sleep, explain why.
- Do not send credentials or destructive commands into a controlled session.
- Keep the harness in `<temp>`, where `<temp>` is the system temp directory as an absolute path, unless the repo already has a testing/demo harness.
- Do not hard-code paths from another repository. Adapt commands to the current repo's scripts and runtime.
- Clean up tmux sessions, `hc` terminals, temp dirs, inspector processes, and demo artifacts unless the user asks to keep them.
