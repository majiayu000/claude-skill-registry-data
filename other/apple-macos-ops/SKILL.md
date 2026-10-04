---
name: apple-macos-ops
description: "Use when operating Apple/macOS local apps and device workflows from Hermes: Notes, Messages/iMessage/SMS, Find My, GUI desktop automation, or other AppleScript/CLI-backed macOS tasks."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos]
---

# Apple macOS Operations

Class-level guide for local Apple ecosystem automation. Use live system tools and respect the user's desktop/session state.

## Shared prerequisites
- Confirm the host is macOS before relying on AppleScript, Notes.app, Messages.app, Find My, or desktop automation.
- Prefer dedicated CLIs when available; use GUI/screenshot automation only when no CLI/API exists.
- For privacy-sensitive actions like sending messages or reading personal notes, operate on the explicit target requested by the user.

## Apple Notes
Use `memo` for Notes.app create/search/edit workflows. Notes sync through iCloud. Install with Homebrew if missing, then verify the command works before claiming success.

## iMessage / SMS
Use `imsg` for reading and sending Messages.app iMessage/SMS. Requirements usually include Messages.app signed in and Full Disk Access for the terminal process. When sending to a specific person/channel, confirm the resolved target rather than guessing.

## Find My
Find My has no stable CLI API. Use AppleScript/app activation plus screenshots/computer-use as needed. Treat locations as sensitive personal data; only surface the device/AirTag information the user asked for.

## macOS Computer Use
When GUI work is required, use macOS computer-use tools in the background without stealing the user's cursor, keyboard focus, or Space. Prefer screenshot → decide → click/type loops, and verify visible state after each important action.

## Common pitfalls
- Do not assume Linux paths or tools for Apple app data.
- Sandboxed app data may live under `~/Library/Containers`.
- GUI automation can be brittle; verify by reading the screen or command output after actions.
- If permissions block access, report the exact permission needed rather than inventing data.
