---
name: clipboard-studio
description: Build, run, troubleshoot, or refine Context Assembly, especially the bundled `apps/clipboard-studio` macOS menu bar app. Use when Codex needs to work on clipboard-heavy context assembly, keep the panel compact, wire pasteboard or app-state capture, or validate the local Xcode workspace and tests without leaking sensitive data.
---

# Context Assembly (`clipboard-studio`)

Use this skill when the user wants to work on Context Assembly as a real macOS app, not just ideate about generic clipboard tooling. If the current repo contains `apps/clipboard-studio`, use that workspace by default.

Instead of manually doing Cmd+C, switching apps, and Cmd+V over and over, the goal is to keep the current page, window, or selection visible, capture related context once, and assemble one structured result that can be sent to another app, exported to Notes, or saved as Markdown in a remembered folder.

## Quick Start

1. If this repo contains `apps/clipboard-studio`, use that workspace first.
2. Run `bash scripts/run_clipboard_studio.sh doctor` to check workspace shape and tool readiness without failing on missing build tools.
3. Run `bash scripts/run_clipboard_studio.sh inspect`.
4. Use `bash scripts/run_clipboard_studio.sh generate` after changing `project.yml`.
5. Use `bash scripts/run_clipboard_studio.sh typecheck` for a fast source-level sanity pass before the full test bundle.
6. Use `bash scripts/run_clipboard_studio.sh test` after model, export, automation, or menu bar UI changes.
7. Use `bash scripts/run_clipboard_studio.sh run` when you need the local menu bar build relaunched.
8. Keep the main loop fast: capture, search, transform, and paste.
9. Default to local-first storage and explicit privacy boundaries.
10. Make the menu bar surface compact and action-first.

## Workflow

### Product Boundary

- Context Assembly owns:
  - clipboard history
  - multi-source context assembly
  - pinned snippets and reusable slots
  - quick send and export actions
  - app-aware or context-aware recall
- Keep it focused on faster cross-app context handoff. Do not bloat it into a full knowledge base.

### Work The Bundled App First

- Read `references/workspace-map.md` before editing the bundled app.
- If the task changes project settings or app metadata, inspect `apps/clipboard-studio/project.yml` and `apps/clipboard-studio/ClipboardStudioApp/Info.plist` first.
- Prefer the local runner script before typing `xcodegen` or `xcodebuild` manually.
- Keep the app menu-bar-first:
  - compact popover
  - explicit settings window
  - fast send or export actions
  - minimal scroll friction
- Use `typecheck` when you only need a quick source-level sanity pass or when you want feedback before the full test bundle.
- Run `test` after changes to:
  - clipboard capture or dedup logic
  - focus snapshot capture
  - export formatting or remembered export paths
  - automation or permissions flows
  - menu bar state presentation

### Workspace Lanes

- `clipboard-studio-workspace`: extend the bundled `apps/clipboard-studio` app and validate the local scheme.
- `product-shaping`: define the user-facing capture, assembly, send, and export flow when the request is still exploratory.
- `app-integration`: wire AppleScript, browser, Notes, or automation touches into the existing app without weakening privacy boundaries.

### UX Guidance

- The first screen should answer:
  - what is in the current assembly
  - what was copied most recently
  - what can be sent or exported next
- Prefer search, keyboard-first actions, and one-tap send or export over deep settings.
- Use compact previews that make text, links, code, and file paths easy to scan.
- If transformations exist, show the transformed result before overwriting the clipboard.

### Privacy And Safety

- Treat clipboard contents as sensitive by default.
- Avoid persisting likely secrets, tokens, passwords, or one-time codes unless the user explicitly asks for that behavior.
- Prefer local-only storage unless the user asks for sync.
- Make it obvious when the app is reading, pinning, pausing, or clearing clipboard history.
- Keep any OpenAI key in the process environment or the app's existing Keychain flow. Do not add plain-text secret storage.

### Editing Guidance

- Keep data models deterministic:
  - history item
  - pinned snippet
  - transform preset
  - quick action or hotkey
- Separate pasteboard polling, persistence, and panel state so each piece can be tested cleanly.
- If the app supports quick paste into other apps, fail gracefully when permissions are missing.
- Preserve responsive menu bar behavior: fast launch, minimal scrolling, and clear empty states.
- Preserve the current split between:
  - clipboard and focus models
  - automation services
  - export and formatting
  - menu bar and overlay views

### Required Deliverables

- A clear clipboard capture and retrieval loop.
- One obvious "send now", "copy assembly", or export action.
- Safe handling rules for sensitive clipboard content.
- A compact icon and visual direction that reads as fast duplication, transfer, and control.

## Resources

- `scripts/run_clipboard_studio.sh`: local doctor, inspect, generate, open, build, test, and run helper for `apps/clipboard-studio`.
- `references/workspace-map.md`: bundled app target map, main files, and validation checkpoints.
- `references/workflow-map.md`: product boundary, icon language, panel structure, and safe-default clipboard rules.
- `agents/openai.yaml`: UI metadata and default invocation prompt.
- `assets/`: branded icons for repo listings and skill chips.
