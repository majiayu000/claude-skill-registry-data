---
name: tauri-native-validation
description: Validate a Tauri desktop app in a real native window, especially when browser-only QA is not enough. Use when Codex needs to verify launch targets, native window sizing, desktop navigation semantics, URL-bar-free flows, screenshots from the actual Tauri shell, or other behavior that must be proven in the real app instead of a browser tab.
---

# Tauri Native Validation

Validate the native shell, not just the renderer. Use this skill when the claim depends on the real Tauri app window.

Keep the workflow split:
- use web automation first for deterministic seeding and renderer QA
- use native-window automation second for launch, resize, and desktop-specific evidence

## Use this skill for

- Tauri launch-target validation
- native-window screenshots
- resize and layout checks in the real app
- desktop-only navigation semantics
- focused-route round trips that must be understood without a browser URL bar
- debugging whether a problem is browser-only, desktop-only, or automation-only

Do not use this skill for routine web QA. Use [$playwright-interactive](../playwright-interactive/SKILL.md) first when a headed browser is sufficient.

## Key platform constraint

Read [references/official-notes.md](./references/official-notes.md) when you need the official rationale.

The short version:
- Tauri's official WebDriver support is for Linux and Windows.
- macOS does not currently have a desktop WebDriver client for WKWebView.
- On macOS, use a mixed strategy:
  - Playwright for browser seeding and renderer QA
  - `osascript` / `System Events` / `screencapture` for native-window evidence

## Workflow

1. Write the desktop QA inventory.
   - List the user-visible desktop claims you intend to sign off on.
   - Separate `browser-validatable` claims from `native-only` claims.

2. Validate the renderer first.
   - Use [$playwright-interactive](../playwright-interactive/SKILL.md) to seed sessions, authenticate, and verify the web surface.
   - Capture browser screenshots under `output/playwright/` before opening Tauri.

3. Launch Tauri in a persistent session.
   - Use the repo's real dev command, usually `pnpm tauri:dev`.
   - Keep it running in a TTY session while validating.
   - Wait for the app window to exist and the daemon/webview to settle before capturing evidence.

4. Validate the native shell.
   - Use `scripts/tauri_window.sh info --app <AppName>` to confirm the running window.
   - Use `scripts/tauri_window.sh capture ...` to activate, resize, and capture the app window.
   - Validate:
     - launch target
     - native layout at default size
     - resized layout
     - key desktop flows that do not rely on browser chrome

5. Treat synthetic keyboard shortcuts as advisory, not authoritative.
   - On macOS, injected `Cmd+K` or similar shortcuts can diverge from real human input in WKWebView-backed apps.
   - If an AppleScript-injected shortcut behaves differently from manual use, treat it as an automation artifact unless the user can reproduce it manually.
   - Prefer:
     - click-based validation
     - menu-based validation
     - manual confirmation for the final shortcut claim

6. Capture artifacts.
   - Save native screenshots under `output/playwright/tauri-validation/`.
   - Use stable names such as:
     - `tauri-terminal-default.png`
     - `tauri-terminal-resized.png`
     - `tauri-focused-session.png`

7. Clean up.
   - Stop `pnpm tauri:dev` when done.
   - Quit the app if it would otherwise leave a sidecar running.

## Decision rules

Use browser automation only when:
- the claim is about renderer behavior
- the URL bar is acceptable
- window-manager semantics do not matter

Add native validation when:
- the claim says "desktop", "Tauri", "native", "launches to", "real app", or "without URL bar"
- resizing or chrome-free navigation is part of the acceptance criteria
- the browser and desktop app may disagree

Escalate to manual confirmation when:
- a shortcut works for the human but fails under `System Events`
- click injection fails due to accessibility/UI-scripting limitations
- the webview focus model is ambiguous under automation

## Reliability rules

- Prefer `127.0.0.1` over `localhost` for web seeding.
- Keep Tauri launch and native capture as separate phases.
- Reuse the same artifact directory through the pass.
- Do not claim a shortcut is broken from scripted keystrokes alone on macOS.
- When a native action is flaky under automation, say so explicitly and separate:
  - `manually confirmed`
  - `automation confirmed`

## Scripts

### `scripts/tauri_window.sh`

Use this helper for the stable macOS-native actions:

```bash
scripts/tauri_window.sh info --app "kimojo"
scripts/tauri_window.sh capture \
  --app "kimojo" \
  --x 220 --y 80 --width 1280 --height 860 \
  --out output/playwright/tauri-validation/tauri-terminal-default.png
```

It supports:
- `info`: print window name, position, and size
- `capture`: activate the app, move and resize window 1, then capture the region

## References

- [references/official-notes.md](./references/official-notes.md)
  Read when you need the official Tauri/macOS constraint or the Apple UI-scripting fallback rationale.
