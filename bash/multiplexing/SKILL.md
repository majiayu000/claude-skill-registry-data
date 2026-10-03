---
name: multiplexing
description: Native windows/splits/panes (absorb tmux). Load when touching multiplex module, keybinds, or session persistence.
triggers:
  - tmux
  - multiplex
  - split
  - pane
  - "copy mode"
  - session
  - "Ctrl+Space"
  - workspace
---

# Multiplexing

Goal: absorb tmux into the core. Users on this stack today run Ghostty → tmux → shell. We collapse that to nyxterm → shell.

## Keybind defaults

- **Prefix**: `Ctrl+Space`. Configurable. (Matches the user's tmux config.)
- **Splits**: `prefix |` = vertical, `prefix -` = horizontal. (Match tmux convention.)
- **Pane nav**: `Ctrl+Shift+h/j/k/l` (no prefix needed, like vim-tmux-navigator).
- **Pane resize**: `prefix H/J/K/L`.
- **Zoom pane**: `prefix z`.
- **New window**: `prefix c`.
- **Window nav**: `prefix 0..9`, `prefix n/p`.
- **Session picker**: `prefix s`.
- **Kill pane**: `prefix x` (with confirm).
- **Detach**: `prefix d`.
- **Copy mode**: `prefix [`. Vi keys. `v` = visual, `y` = yank to system clipboard (via `wl-copy` or platform equivalent).

**Critical**: NO keybinds may shadow xterm escape sequences (e.g., `Ctrl+M` is Enter, can't be rebound). Validate at config-load.

## Session persistence

- Autosave layout (tree of panes + cwd per pane + scrollback head per pane) every 60 s.
- Save on graceful shutdown.
- Persistence backend: Engram (preferred), local SQLite fallback.
- **Don't persist**: secrets in scrollback, pty fds, in-flight AI requests.

Reference: tmux-resurrect + tmux-continuum behavior, reimplemented natively.

## Pane grid model

```
Window
└── PaneTree (binary tree)
    ├── Split (vertical | horizontal, ratio: f32)
    │   ├── PaneTree (left/top)
    │   └── PaneTree (right/bottom)
    └── Leaf (Pane)
        ├── PtySession id
        ├── cwd
        ├── title
        └── ...
```

Leaf panes can be:
- **PTY** (default, terminal)
- **Webview** (Phase 3)
- **mpv** (Phase 3)

The grid logic is content-type agnostic. Only the leaf knows what it is.

## Vi copy-mode

State machine:
- `prefix [` enters copy mode → buffer cursor at last line.
- Vi motion: `h/j/k/l`, `w/b/e`, `0/$`, `gg/G`, `/?` search.
- `v` = char-visual, `V` = line-visual, `Ctrl+v` = block-visual.
- `y` = yank to system clipboard (wl-clipboard on Wayland, xclip on X11, OSC 52 fallback).
- `q` or `Esc` = exit copy mode.

## Tab title and statusline

- Tab title = window name OR auto-renamed from active pane's cwd (basename).
- Statusline (per window): branch (cached, see `git-status` epic), pane index, active count.
- Sessions list: shown in `prefix s` picker (fuzzy-filterable).

## Persistence-on-Engram topic keys

- `nyxterm/session/<session-id>/layout` — pane tree snapshot
- `nyxterm/session/<session-id>/cwd-map` — pane → cwd
- `nyxterm/session/<session-id>/last-active` — timestamp

Sessions are user-named (`prefix S` to rename) and survive restarts.

## What we DON'T copy from tmux

- The control mode / tmux-cli external scripting → use the Tauri command surface directly.
- Plugin manager (TPM) → plugins live in nyxterm's plugin API (epic #21), not tmux.
- Status-bar plugin ecosystem → native modules instead.
