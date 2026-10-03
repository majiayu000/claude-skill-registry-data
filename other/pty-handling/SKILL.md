---
name: pty-handling
description: PTY gotchas (SIGWINCH, ConPTY, OSC, DA filter, coalescing). Load when touching src-tauri/src/modules/pty/ or anything that reads/writes terminal escape sequences.
triggers:
  - pty
  - sigwinch
  - conpty
  - "OSC "
  - "device attributes"
  - "escape sequence"
  - resize
  - portable-pty
---

# PTY handling

Lessons extracted from analyzing `crynta/terax-ai`. Apply them; don't relearn them the hard way.

## SIGWINCH on Linux

Linux emits `SIGWINCH` only when the kernel detects a winsize *delta*. If you set rows back to the same value, TUI apps (vim, htop, btop) don't repaint.

**Pattern**: `kickPty()` bumps rows +1, then restores. Guarantees SIGWINCH. Use it on:

- Tab switch when the previously-released pane was in alt-screen.
- WebGL context restore (after sleep/wake).
- First bind from the renderer pool.

## Windows ConPTY race

ConPTY crashes if multiple PTYs spawn concurrently. Acquire a mutex around spawn. Also: `ClosePseudoConsole` can block indefinitely — do cleanup on a **detached** thread to prevent IPC stalls.

```rust
// pseudocode
let _lock = WINDOWS_CONPTY_LOCK.lock();
let pair = pty_system.openpty(size)?;
drop(_lock);
// ... use pair ...
```

## OSC 7 — current working directory

OSC 7 (`\e]7;file://host/path\e\\`) reports cwd. But: an attacker could `cat` a malicious file containing OSC 7 to hijack your shell context.

**Trust rule**: only honor OSC 7 updates **between commands**. Track `OSC 133 A/B` (prompt start) and `OSC 133 C/D` (command start/end). During C→D (command executing), ignore OSC 7 from the data stream. Update cwd only after D fires.

## OSC 133 — prompt markers

Shell integration emits:
- `OSC 133 A` — prompt start
- `OSC 133 B` — prompt end / command input start
- `OSC 133 C` — command executing
- `OSC 133 D[;exitcode]` — command finished

Use these for: block-style output grouping, AI command palette context, "rerun last command", cwd trust window.

## DA filter (Device Attributes)

TUI apps sometimes query `\e[c` (Device Attributes). If the response is wrong, some apps loop forever.

**Pattern**: intercept DA queries in a small state machine (3 states: Idle → AfterEsc → InsideCsi), cap buffer at 256 bytes, reply with `\e[?1;2c` (VT102-compatible). Don't forward DA queries to the frontend.

## Coalescing flusher

Reading PTY byte-by-byte and forwarding to the frontend is wasteful (1 IPC call per byte = death). Coalesce:

- Open a 4 ms window from the first byte received.
- Flush when the window expires OR after 50 ms idle (whichever first).
- Cap pending buffer at 4 MiB. Beyond that, drop and emit `OVERFLOW_NOTICE` (don't OOM on `yes | head -c 1GB`).

## Signal forwarding

- **Ctrl+C** (in input): send `\x03` to the PTY master (the shell handles SIGINT for the foreground process group).
- **Ctrl+Z**: send `\x1a` (SIGTSTP). Shell handles backgrounding.
- **Ctrl+\\**: send `\x1c` (SIGQUIT).
- **Window close**: send `SIGHUP` to the PTY foreground process group, then close the master fd.

Do NOT send `SIGINT` from the parent process directly to the child — pipe through the PTY so the line discipline does the right thing.

## Shell integration injection

Inject our prompt markers without touching user dotfiles. Pattern (from Ghostty/Terax):

- **zsh**: set `ZDOTDIR=~/.cache/nyxterm/shell-integration/zsh/`, drop our `.zshenv`/`.zshrc` there that sources the user's real dotfiles after our hooks.
- **bash**: launch with `--rcfile ~/.cache/nyxterm/shell-integration/bash/bashrc` that sources `~/.bashrc` last.
- **fish**: drop a file in `~/.config/fish/conf.d/nyxterm.fish` (atomic write + rename).

Atomic file writes always (temp + rename). Never half-write.

## Tests to add when this skill is used

- TUI flicker after pane switch (visual + automated).
- High-throughput stream (1 GB/s output) — no OOM, no IPC stall.
- ConPTY concurrent spawn (Windows) — 100 PTYs in parallel.
- OSC 7 trust during `cat` of crafted file.
