---
name: watch
description: Launch the Karkinos TUI to monitor worker progress in a new terminal window.
allowed-tools: Bash
---

# Watch Skill

Launch the Karkinos worker monitor TUI in a new terminal window.

## Usage

```
/karkinos:watch
```

## Instructions

When the user invokes `/karkinos:watch`, follow these steps:

### 1. Check if karkinos CLI is installed

```bash
which karkinos || echo "NOT_FOUND"
```

### 2. If installed, spawn the TUI

```bash
karkinos watch --spawn
```

This opens the TUI in a new Terminal window (macOS) or terminal emulator (Linux).

### 3. If not installed, provide instructions

Tell the user:

```
The karkinos CLI is not installed. Install it with:

  uv tool install karkinos

Or if you have the source:

  uv tool install /path/to/karkinos

Then run: karkinos watch --spawn
```

## Notes

- The TUI must run in a separate terminal from Claude Code
- Use `--spawn` to automatically open a new terminal:
  - **VS Code/Cursor**: Splits the current terminal pane
  - **Terminal.app**: Opens a new window
  - **Linux**: Opens gnome-terminal, xterm, or konsole
- Use `--no-crabs` to disable the animated crab header
- Use `--speed 0.2` for faster animation
