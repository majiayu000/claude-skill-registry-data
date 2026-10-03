---
name: architecture
description: Overall stack and module shape for nyxterm. Load when touching Tauri commands, PTY wiring, frontend↔backend IPC, or xterm rendering.
triggers:
  - tauri
  - xterm
  - pty
  - "src-tauri/"
  - "src/modules/terminal/"
  - ipc
  - webview
---

# Architecture

## Stack

- **Backend**: Rust 2021+, [Tauri 2](https://v2.tauri.app/), [`portable-pty`](https://crates.io/crates/portable-pty).
- **Frontend**: React 18 + TypeScript 5 + [xterm.js](https://xtermjs.org/) (with `fit`, `search`, `webgl`, `web-links`, `serialize` addons).
- **IPC**: Tauri `invoke()` for commands; Tauri channels for binary streams (no JSON encoding of PTY output).

## Module shape (target)

```
nyxterm/
├── src-tauri/src/
│   ├── modules/
│   │   ├── pty/          # spawn, reader, flusher, waiter, signals, OSC filter
│   │   ├── multiplex/    # panes, splits, sessions
│   │   ├── shell/        # shell init (ZDOTDIR injection like Ghostty/Terax)
│   │   ├── fs/           # file ops for the AI harness
│   │   ├── theme/        # palette emit + theme reload
│   │   └── ai/           # provider routing, MCP client
│   ├── lib.rs            # app init, command registration
│   └── main.rs
└── src/
    └── modules/
        ├── terminal/     # TerminalPane, xterm wiring, renderer pool
        ├── multiplex/    # pane grid UI
        ├── ai/           # chat panel, tool calls
        ├── command-palette/
        └── settings/
```

## PTY wiring (the pattern we copy from terax-ai)

Three concurrent threads per PTY session:

- **Reader**: blocking read of 16 KiB chunks, push through a DA filter, buffer with backpressure cap (4 MiB).
- **Flusher**: coalesces bursts (4 ms window, 50 ms idle ceiling). Emits `ArrayBuffer` chunks to the frontend channel.
- **Waiter**: blocks on child exit, drains the reader, emits final buffer + exit code.

See [`pty-handling`](../pty-handling/SKILL.md) for the gotchas (SIGWINCH, ConPTY, OSC 7 trust).

## IPC contract

Commands (frontend → backend):

```rust
#[tauri::command] fn pty_open(cols: u16, rows: u16, cwd: Option<String>, env: WorkspaceEnv) -> SessionId
#[tauri::command] fn pty_write(session_id: SessionId, data: String)
#[tauri::command] fn pty_resize(session_id: SessionId, cols: u16, rows: u16)
#[tauri::command] fn pty_close(session_id: SessionId)
```

Channels (backend → frontend):

- `data: ArrayBuffer` — raw PTY bytes, no encoding.
- `exit: i32` — exit code on child termination.

Frontend receives `ArrayBuffer` and writes directly into xterm via `term.write(bytes)`. Do NOT base64-encode — that doubles bandwidth and burns CPU.

## Rendering

- xterm.js with **WebglAddon** for GPU rendering. Handle context-loss with a 250 ms re-attach (terax-ai pattern).
- **Renderer pool**: up to 5 reusable xterm instances kept off-screen. When releasing a slot, track `altScreenAtRelease` so we can SIGWINCH-kick the next bind for clean TUI repaint.

## What lives where

| Concern | Layer |
|---|---|
| PTY syscalls, signals | Rust (`src-tauri/src/modules/pty`) |
| Theme palette source-of-truth | Rust emits, frontend listens |
| Pane layout state | Frontend (Zustand or similar), persisted via Engram |
| AI tool execution (Read/Write/Edit/Bash) | Rust (sandboxed where possible) |
| AI chat UI | React |
| MCP client | Rust |

## When you change this

Update this skill and `AGENTS.md`'s skills table. Architectural changes are SDD-tracked (proposal → design → ...).
