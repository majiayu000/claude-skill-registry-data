---
name: flight-scout
description: Build, run, troubleshoot, or extend the Flight Scout macOS menu bar app. Use when working in `apps/flight-scout`, regenerating the XcodeGen project, running local doctor/typecheck/build/test checks, or editing route watching, live fare signals, booking deeplinks, travel-risk scoring, or the board and menu bar UI.
---

# Flight Scout

Use this skill for the bundled `apps/flight-scout` workspace. If the repo contains that app, use it by default.

## Quick Start

1. Run `bash scripts/run_flight_scout.sh doctor`.
2. Run `bash scripts/run_flight_scout.sh inspect` before editing.
3. Use `bash scripts/run_flight_scout.sh generate` after changing `project.yml`.
4. Use `bash scripts/run_flight_scout.sh open` to open the Xcode project.
5. Use `bash scripts/run_flight_scout.sh typecheck` for a fast source-level sanity pass across the app and shared framework.
6. Use `bash scripts/run_flight_scout.sh build` for a plain build check.
7. Use `bash scripts/run_flight_scout.sh test` after model, service, or UI changes.
8. Use `bash scripts/run_flight_scout.sh run` when you need the menu bar app relaunched from `.build-debug`.

## Workflow

### Before Editing

- Read `references/project-map.md` for the target layout and validation path.
- If the task changes project settings or app metadata, inspect `project.yml` and `FlightScoutApp/Info.plist` first.
- Keep Flight Scout menu-bar-first and compact. The board can be richer, but the status item and popover should stay the default path.
- Treat `VibeWidgetCore` as a shared framework target inside this workspace; do not rename or delete it without updating the scheme and imports.
- Keep source coverage honest: route scores, advisory data, and price signals should reflect real inputs and clearly show freshness or fallback states.

### Validation

- Prefer the runner script over manual `xcodegen` or `xcodebuild` commands.
- If `doctor` reports Xcode is not ready, stop and use the exact fix it prints.
- Run `typecheck` after changes to the shared framework or app sources when you want the fastest local sanity pass.
- Run `build` or `test` after changes to models, ranking, route resolution, risk feed parsing, persistence, or menu bar and board UI.
- Run `run` after changes that affect the menu bar panel, board window, or app lifecycle.

## Example Prompts

- `Use $flight-scout to inspect the Flight Scout workspace, regenerate the project if needed, and run the app checks.`
- `Use $flight-scout to tighten the route ranking flow and validate the Flight Scout tests.`
- `Use $flight-scout to update the menu bar and board UI without breaking the travel-risk scoring pipeline.`

## Resources

- `scripts/run_flight_scout.sh`: local doctor, inspect, generate, open, typecheck, build, test, and run helper for `apps/flight-scout`.
- `references/project-map.md`: target map, main files, shared framework target, and validation notes.
