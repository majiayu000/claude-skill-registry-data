---
name: app-screenshot
description: Cross-platform live desktop app UI control and window capture skill for LibrAgent. Supports Windows and Linux. Triggers on requests like '앱 화면 캡처', '앱 스크린샷', '앱 클릭 제어', 'capture app window', 'app screenshot', 'capture ui', 'click app button'.
---

# App Screenshot & UI Control Skill

Capture live, pixel-exact desktop screenshots of the running LibrAgent application window across **Windows and Linux**, with optional mouse click and UI interaction automation.

## Features

- **Window Focus & Screenshot**: Finds and focuses LibrAgent app window, then captures exact window geometry.
- **Relative Coordinate Mouse Click**: Automatically clicks buttons, menus, or cards relative to top-left of the app window before capturing (`--click X Y`).
- **Cross-Platform**: Zero extra native dependencies (uses Python `ctypes.windll.user32` on Windows, `Xlib` / `xwininfo` on Linux).

## Usage Examples

Paths are relative to this skill's Base Directory. Replace `<skill-base-dir>` with its absolute path in commands (or use `@system-skills/app-screenshot` when resolving via skill aliases).

### 1. Capture App Screenshot

```bash
python "<skill-base-dir>/scripts/capture_app.py" docs/user/assets/screenshots/getting-started/new-session.png
```

### 2. Click Relative Coordinate & Capture

Click inside the app window at relative `(X, Y)` (e.g. `X=710, Y=410` for Assistant card) and capture result:

```bash
python "<skill-base-dir>/scripts/capture_app.py" docs/user/assets/screenshots/getting-started/new-session.png --click 710 410
```
