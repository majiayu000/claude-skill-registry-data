---
name: on-this-day-bar
description: Build, run, troubleshoot, or refine the native On This Day Bar macOS menu bar app in `apps/on-this-day-bar`. Use when Codex needs to work on the daily history bar app, regenerate the XcodeGen project, run doctor/build/test checks, or improve the compact cached-feed menu bar workflow.
---

# On This Day Bar

Use this skill when the user wants to work on the native menu bar app, not the web app. If the repo contains `apps/on-this-day-bar`, use that workspace by default.

## Quick Start

1. Run `bash scripts/run_on_this_day_bar.sh doctor`.
2. Run `bash scripts/run_on_this_day_bar.sh inspect` before editing.
3. Use `bash scripts/run_on_this_day_bar.sh generate` after changing `project.yml`.
4. Use `bash scripts/run_on_this_day_bar.sh test` after feed parsing, cache, date selection, or menu bar UI changes.
5. Use `bash scripts/run_on_this_day_bar.sh run` when you need the built app relaunched from the local `.build-debug` product.
6. Keep the app compact, source-grounded, and cache-aware.

## Workflow

### Product Boundary

- On This Day Bar owns:
  - the native `MenuBarExtra` app
  - cached fallback per date
  - settings for category and story depth
  - copyable daily briefs and article handoff
- Do not expand it into the web app; use `on-this-day` for the browser surface and helper flow.

### Work The App First

- Read `references/project-map.md` before editing.
- If the task changes project settings or app metadata, inspect `apps/on-this-day-bar/project.yml` and `apps/on-this-day-bar/OnThisDayBarApp/Info.plist` first.
- Prefer the local runner before typing `xcodegen` or `xcodebuild` manually.
- Run `build` or `test` after feed service, cache behavior, date navigation, or menu bar presentation changes.
- Keep any fallback messaging honest when cached data is being shown.

### Safety And Reliability

- Use the official Wikimedia feed.
- Do not invent historical facts or source links.
- Preserve explicit stale-data messaging when the cache is used.

## Resources

- `scripts/run_on_this_day_bar.sh`: local doctor, inspect, generate, open, build, test, and run helper for the On This Day Bar workspace
- `references/project-map.md`: native app target map, main files, and build notes
- `../../apps/on-this-day-bar/`: the matching native menu bar app codebase
- `scripts/fetch_on_this_day.py`: deterministic helper for official Wikimedia feed snapshots
