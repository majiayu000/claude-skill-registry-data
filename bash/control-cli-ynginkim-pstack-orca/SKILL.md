---
name: control-cli
description: Drive, inspect, and profile an interactive CLI or TUI on this computer with a repeatable harness. Use for CLI UX checks, startup regressions, memory leaks, hangs, prompt flows, or terminal demos.
disable-model-invocation: true
---

> Names in backticks, such as `drive-app` and `inspect-runtime`, are capabilities, not commands. Read `../resolve-capability/SKILL.md` before the first step. It says how each one is done here.

# Control CLI

Exercise an interactive CLI with a repeatable harness instead of trying it by hand. `drive-app` says which terminal tool this environment has. This skill says how to drive the program one input at a time, and how to build a temporary harness from standard tools when the environment has none.

## Use it for

- Reproducing a CLI or TUI bug with fixed input.
- Checking keyboard flows, prompts, interrupts, resizing, and terminal layout.
- Capturing before and after transcripts for a bug fix.
- Profiling startup time, slow operations, hangs, or memory growth.
- Recording a short terminal demo when the output is easier to show than to explain.

## Harness loop

1. Name the command under test and the smallest workspace that reproduces the behavior.
2. Look for a harness the repository already has, such as package scripts, end-to-end tests, demo recorders, expect scripts, or PTY helpers.
3. If there is none, start the CLI in its own terminal session with fixed environment variables. Use the tool `drive-app` resolves to, or one of the temporary harnesses below.
4. Capture the screen before you send anything.
5. Send one action at a time: text, Enter, an arrow key, Escape, Ctrl-C, or a resize.
6. Wait for a specific screen pattern or prompt before the next action.
7. Save the transcript and any profile artifacts.
8. End the session cleanly.

## Harness options

- **The repository's own harness.** Prefer checked-in scripts, because they know the app's startup, environment, and prompts.
- **`tmux`.** Managed sessions with `capture-pane`, `send-keys`, attach, and detach.
- **A PTY probe.** A short Python, Node, or Expect script, when `tmux` is not installed.
- **A runtime inspector.** The Node or Bun inspector for CPU profiles, heap snapshots, and live evaluation. `inspect-runtime` says how to attach here.
- **A terminal recorder.** The repository's demo tools, or an asciinema-compatible recorder, when the user asks for a demo.

`<scratch>` below is a folder from `mktemp -d`.

## A minimal tmux harness

Run it as one block. The subshell stops at the first failed step, and its `trap` kills the session however it ends. tmux names the session, so two harnesses started together never share one. `wait_for` polls the screen until a pattern appears, so no step waits a fixed time, and it fails at once when the program has exited and taken its session with it. `capture-pane` drops trailing spaces, so match a prompt such as `> ` as `^>$`.

```bash
(
  set -euo pipefail
  SESSION=$(tmux new-session -d -P -F '#{session_id}' -- <command-under-test>)
  trap 'tmux kill-session -t "$SESSION" 2>/dev/null || true' EXIT
  wait_for() {
    for _ in $(seq 100); do
      screen=$(tmux capture-pane -pt "$SESSION") || return 1
      grep -q -- "$1" <<<"$screen" && return 0
      sleep 0.1
    done
    echo "timed out waiting for: $1" >&2
    return 1
  }
  wait_for "<ready pattern>"
  tmux capture-pane -pt "$SESSION" > <scratch>/before.txt
  tmux send-keys -t "$SESSION" "help" Enter
  wait_for "<pattern the answer prints>"
  tmux capture-pane -pt "$SESSION" > <scratch>/after.txt
)
```

For a Node CLI, set the inspector in the session's own environment. A variable put in front of `tmux` does not reach the program when a tmux server is already running.

```bash
SESSION=$(tmux new-session -d -P -F '#{session_id}' -e 'NODE_OPTIONS=--inspect=127.0.0.1:0' -- <node-cli-command>)
```

Read the inspector URL from the terminal output, then profile with a tool that speaks the Chrome DevTools Protocol.

## A minimal PTY harness

Use a PTY script when you need exact waits and the repository has no `tmux` or demo harness. Keep it temporary unless the user asks for a reusable test. A PTY carries terminal escape codes such as `ESC[3G`, so pick a pattern they cannot contain, such as `b"\r\n3\r\n"` rather than `b"3"`.

```python
import os
import pty
import select
import subprocess
import time


def read_until(fd, pattern, timeout=30):
    buffer = b""
    deadline = time.time() + timeout
    while time.time() < deadline:
        ready, _, _ = select.select([fd], [], [], 0.25)
        if not ready:
            continue
        try:
            chunk = os.read(fd, 4096)
        except OSError:
            chunk = b""
        if not chunk:
            break
        buffer += chunk
        if pattern in buffer:
            return buffer
    raise RuntimeError(f"never saw {pattern!r}. Output so far: {buffer.decode(errors='replace')}")


master_fd, slave_fd = pty.openpty()
proc = subprocess.Popen(
    ["<command>", "<arg>"],
    stdin=slave_fd,
    stdout=slave_fd,
    stderr=slave_fd,
    close_fds=True,
)
os.close(slave_fd)

try:
    print(read_until(master_fd, b"<ready text>").decode(errors="replace"))
    os.write(master_fd, b"help\n")
    print(read_until(master_fd, b"<text the answer prints>").decode(errors="replace"))
finally:
    try:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait()
    finally:
        os.close(master_fd)
```

If the CLI needs richer terminal control, use `pty.fork()` or a PTY library the project already has.

## Profiling

- **Startup regression.** Time the baseline and the change on the same computer, environment, and command.
- **Slow operation.** Start a CPU profile, run the operation, stop the profile, and compare the functions with the most self time.
- **Memory leak.** Force garbage collection if you can, take a heap snapshot, run the operation many times, force garbage collection again, and take another snapshot.
- **Hang.** Capture the screen, the active handles and resources, and a stack or CPU sample before you interrupt.

## Rules

- Wait for a pattern, not a fixed time. If you must sleep, say why.
- Do not send credentials or destructive commands into a session you drive.
- Keep a temporary harness in a `mktemp -d` folder, unless the repository already has a test or demo harness.
- Do not copy paths from another repository. Adapt commands to this repository's scripts and runtime.
- Remove `tmux` sessions, temp folders, inspector processes, and demo artifacts when you are done, unless the user asks to keep them.
