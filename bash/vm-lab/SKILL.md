---
name: vm-lab
description: >-
  Runs a clean Parallels macOS VM lab to test GUI automation, TCC permission prompts, screenshots,
  clicking, and typing, verifying from outside the guest (two-way validation). Use when a macOS
  automation tool must be tested on a fresh system.
source: "https://github.com/steipete/agent-scripts"
attribution: "steipete/agent-scripts by Peter Steinberger"
version: "1.0.0"
platform: macos
license: MIT
---

# VM Lab

> **Attribution:** Sourced from [steipete/agent-scripts](https://github.com/steipete/agent-scripts) by [Peter Steinberger](https://github.com/steipete).

Use this when the task needs a clean macOS VM to test GUI automation, TCC prompts, screenshot capture, clicking, typing, performance, or "two-way validation" of automation tools.

Core idea: run the tool under test inside the guest, but verify it from outside the guest with Parallels screenshots and host-side observations.

## Safety Rules

- Treat the VM snapshot as disposable, not the host.
- Never print secrets. If `op` is needed, run it only inside `tmux`.
- Prefer fresh app windows you create yourself: TextEdit, a local HTML test page, or a small test app.
- Avoid modifying host state except temporary screenshots under `/tmp`.

## VM Discovery

```bash
# List VMs
prlctl list --all

# Get VM status/IP
prlctl list --info "macOS Sequoia"

# Run guest command
prlctl exec "macOS Sequoia" 'sudo -u $USER -H /bin/zsh -lc "uname -a"'

# Host-side screenshot
prlctl capture "macOS Sequoia" --file /tmp/vm-reference.png
sips -g pixelWidth -g pixelHeight /tmp/vm-reference.png
```

## TCC / GUI Attribution

For macOS Screen Recording and Accessibility, the responsible process matters.

- `prlctl exec` is headless and can fail to produce useful Screen Recording attribution.
- Launch the test command from a visible terminal app in the guest when Screen Recording is involved.
- After a first failed capture, check `System Settings > Privacy & Security > Screen & System Audio Recording`.

## Two-Way Validation

For each GUI action, verify through two independent signals:

- **Tool-under-test output**: JSON, screenshot file, AX result, or app state.
- **External verifier**: `prlctl capture`, host-side image inspection, file content in guest, or process/window state.

Examples:
- Screenshot: compare tool image dimensions/content against `prlctl capture`.
- Click: use automation to click a test button, then verify both guest app state and host screenshot.
- Performance: wrap commands with `/usr/bin/time -p`; repeat cold/warm runs.

## Known Pitfalls

- macOS clipboard APIs may fail from `prlctl exec`; `pbcopy` and AppleScript clipboard can fail in headless guest context.
- `prlctl exec` may re-join argv through a guest shell; for complex payloads, create a script file first.
- For normal typing, use `prlctl send-key-event` — but it uses Parallels key values, not macOS virtual key codes.

## Reporting

When handing off, include only:
- VM name and OS build
- repo commit tested
- permission state
- commands that passed/failed
- independent verifier result
- product bugs discovered
