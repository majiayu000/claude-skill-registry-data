---
name: kakaotalk-windows-cli
description: Install, diagnose, and use the unofficial kakaocli-win tool for local KakaoTalk UI automation on Windows. Use for setup, open-room inspection, visible-message reading, or deliberate single-message sending; do not use for bulk messaging or remote account access.
---

# KakaoTalk Windows CLI

Use the repository's `install.ps1` for setup. Run `scripts/diagnose.ps1` from this skill when sharing diagnostics because it omits chat-room titles and local executable paths.

Before reading or sending, require KakaoTalk to be installed, signed in, and the target room to be open as a separate window. Treat room names and copied messages as private data; do not save or publish them unless the user explicitly asks.

For sending, use `--dry-run` first. Keep the interactive confirmation enabled unless the user explicitly authorizes bypassing it for the exact room and message. Do not add bulk, repeated, hidden, or unsolicited messaging behavior.

UI selectors can change with KakaoTalk releases. If an operation fails, run `inspect` locally, redact text and titles from its output, and use only the control-class and geometry information needed for diagnosis.
