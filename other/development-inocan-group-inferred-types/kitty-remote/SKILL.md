---
name: kitty-remote
description: Control kitty terminal via remote protocol and kitty-test-harness; launch panels/windows, send keys, capture screen, manage sockets, and debug remote-control failures when testing TUIs.
license: MIT
metadata:
  triggers:
    type: domain
    enforcement: suggest
    priority: high
    keywords:
      - kitty
      - kitty test
---

# Kitty Remote Control

Drive kitty instances via the remote control protocol and kitty-test-harness.

## Prerequisites

- Ensure kitty is installed and on PATH.
- Enable remote control (`allow_remote_control=yes` in kitty.conf or via `-o`).
- Run under an active Wayland or X11 session.

## Quick start

1. Launch kitty with a unix socket (`--listen-on unix:/abs/path.sock` or `KITTY_LISTEN_ON`).
1. Wait for `@ ls` to succeed before sending input.
1. Send input with `send-text` and capture output with `get-text --extent screen`.
1. Close with `close-window` and remove the socket.

## Harness usage

- Prefer `kitty +kitten panel` on Wayland; fall back to windows on X11/WSL
- Use absolute socket paths; delete stale sockets before launch
- Send `ESC` to normalize modal state before `:` commands
- Socket disappearance = app exit/crash; capture with `@ ls`, `get-text --ansi`, logs
- Source [scripts/kitty-harness.sh](scripts/kitty-harness.sh) for ready-to-use harness

## References

- [harness-notes.md](references/harness-notes.md) - internals, failure signatures, debug flow
- [escape-codes.md](references/escape-codes.md) - byte-level key sequences and modifiers
