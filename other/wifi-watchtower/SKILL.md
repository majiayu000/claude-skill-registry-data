---
name: wifi-watchtower
description: Build, run, troubleshoot, or refine the WiFi Watchtower macOS menu bar app in `apps/wifi-watchtower`. Use when Codex needs the exact app workspace, repo-native doctor/typecheck/build/test flows, or menu bar and dashboard changes for local Wi-Fi trust scoring.
---

# WiFi Watchtower

Use this skill when the user wants the native WiFi Watchtower app in `apps/wifi-watchtower`. If the request is about the portable Network Studio workspace or SwiftBar plugin, use `$network-studio` instead.

Default product shape: a compact macOS `MenuBarExtra` utility with a trust-grade popover, an optional dashboard window, and local-only Wi-Fi inspection.

## Quick Start

1. Read `references/project-map.md` before editing the app workspace.
2. Run `bash scripts/run_wifi_watchtower.sh doctor`.
3. Run `bash scripts/run_wifi_watchtower.sh inspect`.
4. Use `bash scripts/run_wifi_watchtower.sh generate` after changing `project.yml`.
5. Use `bash scripts/run_wifi_watchtower.sh typecheck` for a fast Swift source sanity pass.
6. Use `bash scripts/run_wifi_watchtower.sh build` after model, scoring, or view changes.
7. Use `bash scripts/run_wifi_watchtower.sh test` after logic or scoring changes when Xcode is ready.
8. Use `bash scripts/run_wifi_watchtower.sh run` when you need the menu bar app relaunched from the local build.
9. Keep the app menu-bar-first, compact, and honest about uncertainty.

## Workflow

### Before Editing

- Inspect `project.yml` and `WifiWatchtowerApp/Info.plist` before changing project settings or app metadata.
- Keep the menu bar surface compact and action-first.
- Preserve local-only Wi-Fi inspection and scoring. Do not add remote telemetry or account-bound sync by default.

### Product Boundary

- WiFi Watchtower owns:
  - the native `MenuBarExtra` app
  - current-network trust grading
  - nearby Wi-Fi risk context
  - dashboard explanations for why the grade changed
- WiFi Watchtower does not own:
  - the portable Network Studio workspace or SwiftBar plugin
  - any packet-sniffing or deep network inspection claims

### Editing Guidance

- Prefer `MenuBarExtra` and a compact accessory-style app surface.
- Keep the first screen action-oriented:
  - current trust grade
  - strongest reasons behind the grade
  - current gateway or DNS summary
  - nearby Wi-Fi risk summary
- Preserve clear distinction between current-network trust, nearby-network context, and subjective recommendation copy.
- Keep the app honest about uncertainty. A caution or avoid score should explain why in plain language.
- If you touch the refresh loop or scoring logic, keep the UI copy aligned with the actual signals being measured.

### Running The App

- Prefer the local runner script before typing `xcodegen` or `xcodebuild` manually.
- Run `inspect` for quick orientation and `typecheck` when you want a faster source-level sanity pass than a full build.
- Use `build` or `test` after changes to `WifiWatchtowerApp/Sources`, especially the inspector, scorer, or views.
- Use `run` after UI changes so the menu bar app relaunches from the built app bundle.
- If `doctor` reports that Xcode is not ready, stop and use the exact command it prints before trying `build` or `run`.

## Resources

- `scripts/run_wifi_watchtower.sh`: local doctor, inspect, generate, open, typecheck, build, test, and run helper for the app workspace.
- `references/project-map.md`: app target map, main files, and build notes.
