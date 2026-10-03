---
name: vibe-bluetooth
description: Build, run, troubleshoot, or extend the VibeWidget macOS SwiftUI app and widget. Use when Codex needs to work on a VibeWidget or VibeBluetooth workspace, especially the repo app at `apps/vibe-widget`; regenerate the Xcode project; launch it in Xcode; run local doctor, build, or typecheck checks; or modify the HomeKit, Spotify, widget, voice panel, or shared-core flows.
---

# VibeBluetooth

Use this skill for the VibeWidget app workspace. If the current repo contains `apps/vibe-widget`, use that by default. Otherwise, pass `--workspace /path/to/vibe-widget` to the runner script.

## Quick Start

1. Use `bash scripts/run_vibe_bluetooth.sh doctor` from the repo root, or pass `--workspace /path/to/vibe-widget` if the app lives elsewhere.
2. Use `bash scripts/run_vibe_bluetooth.sh inspect` before editing so the app, widget, and core-test layout stay visible.
3. Use `bash scripts/run_vibe_bluetooth.sh generate` after project spec changes.
4. Use `bash scripts/run_vibe_bluetooth.sh open` to open the Xcode project.
5. Use `bash scripts/run_vibe_bluetooth.sh typecheck` for a lightweight local sanity pass.
6. Use `bash scripts/run_vibe_bluetooth.sh test` after core, widget, parser, or shared-state changes.
7. Use `bash scripts/run_vibe_bluetooth.sh build` only after the Xcode license has been accepted on the machine.
8. Use `bash scripts/run_vibe_bluetooth.sh run` when you need the built app relaunched from the local build output.

## Workflow

### Before Editing

- Read `references/project-map.md` for the current target layout and main files.
- If the task changes app or widget targets, inspect `project.yml` in the target workspace first.
- If the task is UI-heavy, preserve the existing visual direction: dark glass, low chrome, strong type, and a compact high-signal layout.

### Running The App

- Prefer the local runner script before manually typing `xcodegen` or `xcodebuild`.
- If `doctor` reports the Xcode license is not accepted, stop and tell the user to run `sudo xcodebuild -license`.
- Use `test` after changes to `VibeWidgetCore`, widget intents, or app orchestration when you want the repo's unit coverage before a full build.
- Use `run` after app UI or launch-path changes so you can verify the relaunch path from the local build output.
- If `generate` succeeds but `build` fails only under Command Line Tools, switch to full Xcode and rerun.

### Editing Guidance

- Keep the project Apple-only for speaker flow. Do not add private Bluetooth automation.
- Keep secrets in Keychain only. Do not move OpenAI or Spotify tokens into files or defaults.
- Shared models and snapshot state belong in `VibeWidgetCore`.
- Widget actions should enqueue shared actions and let the app process them.
- HomeKit code must keep the compile-safe fallback path for environments that only expose Command Line Tools.

## Resources

- `scripts/run_vibe_bluetooth.sh`: local doctor/inspect/generate/open/build/test/typecheck runner for the VibeWidget workspace.
- `references/project-map.md`: target map, key files, and run/build caveats.
