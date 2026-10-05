---
name: system-screenshot
description: Capture and verify screenshots of runtime apps, browser apps, Figma nodes, and the Windows desktop or individual desktop application windows. Use this skill whenever the user asks to take a screenshot, capture the screen, inspect a UI visually, verify that a local app/runtime app rendered correctly, screenshot an app connector view, or capture the desktop/window state, even if they do not mention this skill by name.
metadata:
  runtime_support_files: true
runtime_projection: true
source_of_truth: registry/skills/system-screenshot/SKILL.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/system-screenshot/SKILL.md`
> Source of truth: `registry/skills/system-screenshot/SKILL.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill`
# System Screenshot

Use this skill to choose the least invasive screenshot path that matches the target. Prefer app-native capture for browser/runtime apps, then connector-specific screenshot tools, and use the bundled Windows script for desktop or native app captures.

## Target Selection

1. For a browser, localhost, web app, or runtime app with a URL, use the available browser/app testing tool first. Capture both an accessibility snapshot and a screenshot when the visual state matters. If the user explicitly names Browser Use or the in-app browser, use that route.
2. For Figma, use the Figma screenshot tool with the file key and node id. If the user provides a Figma URL, extract `fileKey` and `nodeId` from it.
3. For native Windows desktop, a visible app window, or a general "desktop screenshot", run `scripts/capture_windows_screen.ps1`.
4. If a target cannot be captured because it is minimized, hidden, protected, elevated, or on another secure desktop, report that limitation and ask the user to bring the target onscreen.

## Output Rules

- Save screenshots as PNG unless the user asks for another format.
- Put temporary screenshots under a clear path such as `%TEMP%\codex-screenshots\` or a project-local diagnostics folder.
- Return the absolute file path, target type, and any limitation observed.
- When diagnosing UI rendering, include a short visual finding summary after capturing the image.
- Do not capture secrets or private account pages unnecessarily. If credentials, tokens, personal messages, or payment details are visible, prefer asking the user to hide them before capture.

## Windows Desktop Capture

Use the bundled script when the request is about the physical desktop or a native app window:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "$env:USERPROFILE\.codex\skills\system-screenshot\scripts\capture_windows_screen.ps1" -Mode Desktop
```

Capture a specific visible window by title:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "$env:USERPROFILE\.codex\skills\system-screenshot\scripts\capture_windows_screen.ps1" -Mode Window -WindowTitle "Notepad"
```

Capture a specific visible window by process name:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "$env:USERPROFILE\.codex\skills\system-screenshot\scripts\capture_windows_screen.ps1" -Mode Window -ProcessName "notepad"
```

The script prints JSON containing `outputPath`, `mode`, `width`, `height`, and target metadata. Use that JSON as the capture record.

## Verification Pattern

After capture:

1. Inspect the image when an image viewing tool is available.
2. Check that the target is not blank, offscreen, occluded, or the wrong window.
3. If the screenshot is for UI validation, mention concrete visible issues such as clipping, overlap, blank content, missing assets, or wrong viewport.
4. If the first capture is wrong because focus changed, retry once after activating or asking the user to foreground the target.
