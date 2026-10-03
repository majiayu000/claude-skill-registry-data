---
name: telebar
description: Build, run, troubleshoot, or extend the TeleBar macOS menu bar app. Use when Codex needs to work on a TeleBar workspace, especially the repo app at `apps/telebar`; regenerate the Xcode project; launch the app; run local doctor or build checks; or modify the Telegram inbox, AI writing, setup links, keychain storage, or compact macOS popover UI.
---

# TeleBar

Use this skill for the TeleBar menu bar app. If the current repo contains `apps/telebar`, use that by default. Otherwise, pass `--workspace /path/to/telebar` to the runner script.

## Quick Start

1. Use `bash scripts/run_telebar.sh doctor` from the repo root, or pass `--workspace /path/to/telebar` if the app lives elsewhere.
2. Use `bash scripts/run_telebar.sh inspect` before editing so the app layout stays visible.
3. Use `bash scripts/run_telebar.sh generate` after changing `project.yml`.
4. Use `bash scripts/run_telebar.sh open` to open the Xcode project.
5. Use `bash scripts/run_telebar.sh typecheck` for a lightweight source check before a full build.
6. Use `bash scripts/run_telebar.sh run` to build and relaunch the menu bar app locally.
7. Use `bash scripts/run_telebar.sh build` for a plain xcodebuild pass when you only need validation.

## Workflow

### Before Editing

- Read `references/project-map.md` for the current app layout and the main files.
- If the task changes project settings or app metadata, inspect `project.yml` and `TeleBarApp/Info.plist` first.
- Keep the app menu-bar-only. Do not turn it into a regular dock app unless the user asks.

### Editing Guidance

- Favor a compact, native macOS popover over a dashboard look.
- Keep the palette restrained: dark neutrals with a subtle blue accent.
- Reduce cognitive load before adding more controls. Prefer grouped rows, short labels, and hover help.
- Telegram bot tokens and OpenAI keys stay in Keychain only.
- Inbox behavior must stay honest: only show chats the bot can actually access.
- Bot creation and permission flows should go through Telegram's supported links and BotFather, not fake autonomous setup.

### Running The App

- Prefer the local runner script before typing `xcodegen` or `xcodebuild` manually.
- Use `inspect` for quick orientation and `typecheck` when you want a faster source-level sanity pass than a full build.
- If `doctor` reports the Xcode license is not accepted, stop and tell the user to run `sudo xcodebuild -license`.
- Use `run` after UI changes so the new menu bar popover is relaunched from the built app bundle.

## Example Prompts

- `Use $telebar to open the TeleBar app project, inspect the compact menu bar UI, and improve the setup flow.`
- `Use $telebar to run doctor, rebuild TeleBar, and relaunch the menu bar app.`
- `Use $telebar to make the Telegram chat list easier to scan and add better hover help for first-time users.`

## Resources

- `scripts/run_telebar.sh`: local doctor/generate/open/build/run runner for the TeleBar workspace.
- `references/project-map.md`: target map, key files, and Telegram/UI constraints.
