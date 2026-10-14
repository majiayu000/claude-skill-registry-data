---
name: "screenshot"
description: "Use when the user explicitly asks for a desktop or system screenshot (full screen, specific app or window, or a pixel region), or when tool-specific capture capabilities are unavailable and an OS-level capture is needed."
agent:
  display_name: "Screenshot Capture"
  short_description: "Capture screenshots"
  default_prompt: "Capture the right screenshot for this task (target, area, and output path)."
---

# Screenshot Capture

Follow these save-location rules every time:

1) If the user specifies a path, save there.
2) If the user asks for a screenshot without a path, save to the OS default screenshot location.
3) If a tool needs a screenshot for its own inspection, save to the temp directory.

## Tool priority

- Prefer tool-specific screenshot capabilities when available (for example: a Figma MCP/skill for Figma files, or Playwright/agent-browser tools for browsers and Electron apps).
- Use this skill when explicitly asked, for whole-system desktop captures, or when a tool-specific capture cannot get what you need.
- Otherwise, treat this skill as the default for desktop apps without a better-integrated capture tool.

## macOS permission preflight (reduce repeated prompts)

On macOS, run the preflight helper once before window/app capture. It checks Screen Recording permission, explains why it is needed, and requests it in one place.

The helpers route Swift's module cache to `$TMPDIR/codex-swift-module-cache` to avoid extra sandbox module-cache prompts.

```bash
bash <path-to-skill>/scripts/ensure_macos_permissions.sh
```

To avoid multiple sandbox approval prompts, combine preflight + capture in one command when possible:

```bash
bash <path-to-skill>/scripts/ensure_macos_permissions.sh && \
python3 <path-to-skill>/scripts/take_screenshot.py --app "Codex"
```

For inspection runs, keep the output in temp:

```bash
bash <path-to-skill>/scripts/ensure_macos_permissions.sh && \
python3 <path-to-skill>/scripts/take_screenshot.py --app "<App>" --mode temp
```

Use the bundled scripts to avoid re-deriving OS-specific commands.

## macOS and Linux (Python helper)

Run the helper:

```bash
python3 <path-to-skill>/scripts/take_screenshot.py
```

Common patterns:
- Default location: `python3 <path-to-skill>/scripts/take_screenshot.py`
- Temp location: `python3 <path-to-skill>/scripts/take_screenshot.py --mode temp`
- Explicit path: `python3 <path-to-skill>/scripts/take_screenshot.py --path output/screen.png`
- App/window capture (macOS only): `python3 <path-to-skill>/scripts/take_screenshot.py --app "Codex"`
- Pixel region: `python3 <path-to-skill>/scripts/take_screenshot.py --mode temp --region 100,200,800,600`
- Active window: `python3 <path-to-skill>/scripts/take_screenshot.py --mode temp --active-window`
- List windows before capture: `python3 <path-to-skill>/scripts/take_screenshot.py --list-windows --app "Codex"`

The script prints one path per capture. When multiple windows or displays match, it prints multiple paths (one per line) and adds suffixes like `-w<windowId>` or `-d<display>`.

### Linux prerequisites

The helper selects the first available tool: `scrot`, `gnome-screenshot`, or ImageMagick `import`. Coordinate regions require `scrot` or `import`.

## Windows (PowerShell helper)

```powershell
powershell -ExecutionPolicy Bypass -File <path-to-skill>/scripts/take_screenshot.ps1
```

Patterns:
- Default: `-File <path-to-skill>/scripts/take_screenshot.ps1`
- Temp: `-File <path-to-skill>/scripts/take_screenshot.ps1 -Mode temp`
- Pixel region: `-File <path-to-skill>/scripts/take_screenshot.ps1 -Mode temp -Region 100,200,800,600`
- Active window: `-File <path-to-skill>/scripts/take_screenshot.ps1 -Mode temp -ActiveWindow`

### Direct OS fallbacks (when scripts unavailable)

**macOS:** `screencapture -x output/screen.png`, `screencapture -x -R100,200,800,600 output/region.png`, `screencapture -x -l12345 output/window.png`

**Linux:** `scrot output/screen.png`, `gnome-screenshot -f output/screen.png`, `import -window root output/screen.png`, `scrot -a 100,200,800,600 output/region.png`

## Error handling

- On macOS, run `ensure_macos_permissions.sh` first.
- If sandboxed, rerun with escalated permissions.
- If app/window capture returns no matches, run `--list-windows --app "AppName"` and retry with `--window-id`.
- If Linux capture fails, check `command -v scrot`, `command -v gnome-screenshot`, `command -v import`.
- Always report the saved file path in the response.

## Bundled Scripts

Copy the scripts to your project's `.ai_scripts/` directory:

```powershell
cp <skill-path>/screenshot/scripts/take_screenshot.py .ai_scripts/
cp <skill-path>/screenshot/scripts/take_screenshot.ps1 .ai_scripts/
```

Usage from project-local location:

```bash
python3 .ai_scripts/take_screenshot.py
powershell -ExecutionPolicy Bypass .ai_scripts/take_screenshot.ps1 -Mode temp
```

## Cross-references

- **playwright** — Screenshots complement Playwright-based browser automation.
- **todo-bootstrap** — Screenshots are useful for documenting progress in checklists.
- **security-best-practices** — Screenshots may capture sensitive info on screen; handle outputs securely.
- **os-awareness** — Platform-specific capture paths differ per OS.
- **skill-loader** — Apply the capped selection policy when deciding which capture-related skills should also be active.
