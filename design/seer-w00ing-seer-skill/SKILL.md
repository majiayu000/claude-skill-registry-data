---
name: seer
description: Visual feedback capture for any running macOS app window via osascript + screencapture. Use when the user wants UI verification or a fresh screenshot.
---

# Seer

## Overview
Capture a precise screenshot of a visible app window, annotate it for quick UI mockups, then compare against baselines to keep visual state in the agent loop.

## Quick start
1. Ensure the target app is running and Screen Recording + Accessibility are enabled for your terminal. (Automation -> System Events required for typing.)
2. Run the script:
   - `bash scripts/capture_app_window.sh` (defaults to frontmost app, output `.seer/capture/app-window-<app>-YYYYMMDD-HHMMSS-<pid>-<rand>.png`)
   - `bash scripts/capture_app_window.sh /path/to/out.png "Promptlight"` (custom output + process name)
3. (Optional) Record video + extract frames:
   - `bash scripts/record_app_window.sh --duration 3 --frames --fps 20`
   - `bash scripts/extract_frames.sh /path/to/video.mov --fps 20`
4. (Optional) Create a mockup with annotations:
   - `bash scripts/mockup_ui.sh --spec spec.json`
   - `bash scripts/mockup_ui.sh --spec spec.json --json`
5. (Optional) Store + compare in the visual loop:
   - `bash scripts/loop_compare.sh /path/to/out.png web-home`
   - First run creates a baseline under `$SEER_LOOP_DIR` (default `.seer/loop`)
6. Attach the current image (and diff image, if generated) with `view_image`.

## Usage
- `bash scripts/capture_app_window.sh --help`
- `bash scripts/capture_app_window.sh [out_path] [process_name]`
  - `out_path` default `.seer/capture/app-window-<app>-YYYYMMDD-HHMMSS-<pid>-<rand>.png`
  - `process_name` default frontmost app
  - set `SEER_OUT_DIR` to change default output root (falls back to `SEER_TMP_DIR` for legacy behavior)
- `bash scripts/type_into_app.sh --help`
- `bash scripts/type_into_app.sh --app "Promptlight" --text "hello" --enter`
- `bash scripts/type_into_app.sh --app "Promptlight" --click-rel 120,180 --text "hello"`
- `bash scripts/type_into_app.sh --text "hello" --no-activate`
- `bash scripts/record_app_window.sh --help`
- `bash scripts/record_app_window.sh --duration 3 --frames --fps 20`
- `bash scripts/extract_frames.sh --help`
- `bash scripts/extract_frames.sh /path/to/video.mov --fps 20`
- `bash scripts/mockup_ui.sh --help`
- `bash scripts/mockup_ui.sh --spec spec.json`
- `bash scripts/mockup_ui.sh --spec spec.json --json`
- `python3 scripts/excalidraw_from_text.py --help`
- `python3 scripts/excalidraw_from_text.py --text "header: Settings; list: Account, Notifications, Privacy; button: Log out"`
- `python3 scripts/excalidraw_from_text.py --text $'screen: Home\nheader: Home\nbutton: Get started\n\nscreen: Settings\nheader: Settings\nlist: Account, Notifications\nbutton: Log out' --theme classic --fidelity medium`
- `cat prompt.txt | python3 scripts/excalidraw_from_text.py --name settings`
- `python3 scripts/excalidraw_from_text.py --text "lib: Search field | Search" --json` (explicit Excalidraw library item)
- `python3 scripts/annotate_image.py input.png output.png --spec spec.json`
- `python3 scripts/annotate_image.py --spec-help` (prints JSON spec schema)
- `annotate_image.py` supports top-level `defaults` (e.g., `auto_scale`, `outline`, `text_bg`), `spotlight` annotations to dim the background, `fit` (enabled by default) to auto-adjust rect/spotlight bounds, and `anchor`/`from`/`to` for auto-anchoring labels and arrows.
- `bash scripts/loop_compare.sh --help`
- `bash scripts/loop_compare.sh [--loop-dir <path>] [--resize] [--update-baseline] <current_path> <baseline_name>`
  - set `SEER_LOOP_DIR` to change default loop directory (default `.seer/loop`)
  - consider adding `.seer/` to `.gitignore`

## Workflow
1. **Capture**
   - `scripts/capture_app_window.sh`
   - If it fails, rerun with explicit process name or verify permissions.
2. **Record (optional)**
   - `scripts/record_app_window.sh --duration 3 --frames --fps 20`
   - Use frames for granular UI change analysis.
3. **Compare (optional)**
   - `scripts/loop_compare.sh <current_path> <baseline_name>`
   - Stores `baselines/`, `latest/`, `history/`, `diffs/`, `reports/` under `.seer/loop` (or `$SEER_LOOP_DIR`)
4. **Inspect**
   - Use `view_image` to load the current image and diff image.
5. **Iterate**
   - Repeat after UI changes or window repositioning.

## Resources
### scripts/
- `capture_app_window.sh`: grabs window bounds via System Events and runs `screencapture -x -R`.
- `record_app_window.sh`: records a window region to `.mov` via `screencapture -v` (optionally extracts frames).
- `extract_frames.sh`: extracts frames from a video via `ffmpeg`.
- `type_into_app.sh`: focuses app and types text via System Events keystrokes.
- `excalidraw_from_text.py`: converts a natural-language-ish prompt into a `.excalidraw` scene file under `.seer/excalidraw/` (supports `screen: Name` for multi-screen; uses the bundled Excalidraw library when present).
- `annotate_image.py`: draws arrows, rectangles, and text on an image (requires `python3 -m pip install pillow`).
- `mockup_ui.sh`: capture window (optional) then annotate using a JSON spec.
- `compare_images.py`: compares baseline vs current and emits diff metrics + optional diff image (requires `python3 -m pip install pillow`).
- `loop_compare.sh`: manages baselines, history, and diff outputs for visual regression loops.

### assets/
- `assets/excalidraw/wireframe-ui-kit.excalidrawlib`: default Excalidraw UI library used by `excalidraw_from_text.py` when present (override with `--library` or disable with `--no-library`).
- `assets/excalidraw/basic-ux-wireframing-elements.excalidrawlib`: fallback library (smaller) if the UI kit is missing.

## Output layout (default)
Under `.seer/`:
- `capture/` window screenshots
- `record/` window recordings + extracted frame folders
- `mockup/` annotated mockups + their capture/spec/meta (also writes `latest-*` convenience copies)
- `excalidraw/` generated `.excalidraw` scenes (also writes `latest-*.excalidraw`)
- `loop/` visual regression loop storage (baselines/latest/history/diffs/reports)
