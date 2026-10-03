---
name: callesnikov-ascii-video-fork
description: Work with the local AI-assisted fork of https://github.com/stepanussaruran/ASCII-Video-Player for terminal ASCII video playback, color ASCII image conversion, and saving ASCII images/videos. Use when the user asks to preview a video or photo as ASCII art, convert media to ASCII text, save ASCII-rendered PNG/MP4 outputs, inspect or update this fork, configure color terminal output, or explain how to use the ASCII media scripts from Codex.
---

# Callesnikov ASCII Video Fork

## Layout

Use this skill directory as a two-part project:

- `repository/`: original upstream clone of `https://github.com/stepanussaruran/ASCII-Video-Player`.
- `fork/`: Codex-made fork layer with added tools, dependencies, and PowerShell color helper.
- `fork/java-swing/`: simple Swing GUI wrapper that calls the fork Python script.
- `fork/LICENSE.md`: root MIT license file for standard GitHub license detection.
- `fork/README.md`: README for publishing the fork folder as an independent GitHub repository.
- `fork/README-EN.md`: English README translation for GitHub publishing.
- `fork/licences/`: bilingual MIT license and ethical attribution notices for the fork layer.
- `README.md`: user-facing Russian instructions. Keep it aligned with this file.

Do not mix new fork files into `repository/` unless the user explicitly asks to patch the upstream player itself. Put additions in `fork/`.

For GitHub publishing, prefer making `fork/` the repository root. Do not commit the nested `repository/` clone into the published fork unless the user explicitly wants a monorepo/archive layout. The fork tools do not require `repository/` at runtime; they only need files inside `fork/` plus Python/Java dependencies.

The fork layer is licensed under MIT via `fork/licences/LICENSE-EN.md` and `fork/licences/LICENSE-RU.md`. The notices in `fork/licences/NOTICE-EN.md` and `fork/licences/NOTICE-RU.md` explain attribution to the original public repository and clarify that the license applies only to code/documentation created for this fork layer. Do not imply that this project relicenses upstream code.

## Session Start

Before using the skill in a new session:

1. Enter the skill directory.
2. Confirm `repository/.git` exists. If it is missing, clone upstream into `repository/`.
3. Check original repo status with `git status --short --branch` from `repository/`.
4. Check upstream with `git fetch origin` when permissions allow it.
5. Only run `git pull --ff-only` when the worktree is clean and a fast-forward is possible.
6. If local changes exist, or if `.git/FETCH_HEAD` is not writable in the sandbox, do not repair destructively. Use the local clone and tell the user that upstream freshness could not be verified or applied.

Never delete the local copy if upstream disappears.

## Dependencies

For original video playback:

```bash
cd repository
python -m pip install -r ../fork/requirements.txt
```

For fork tools:

```bash
cd fork
python -m pip install -r requirements.txt
```

`fork/requirements.txt` includes `opencv-python`, `numpy`, and `pillow`.

Notes:

- Image conversion needs `numpy` and `pillow`.
- Video preview/saving needs `opencv-python`.
- If dependency installation is blocked, still run syntax checks and image checks when available; explain that full video testing requires OpenCV.

## Ask The User

For conversion requests, collect only missing essentials:

- input media path;
- image vs video when extension is ambiguous;
- ASCII width in characters, usually `80`, `120`, or `180`;
- optional ASCII height in rows;
- color or monochrome;
- desired output: terminal preview, text file, PNG, MP4, or text frames;
- output path when saving;
- optional rendered pixel size such as `1280x720`.
- vivid look preference: use `--vivid`, or tune `--brightness`, `--contrast`, `--saturation`, `--gamma`, and `--glow`.

Use `fork/ascii_outputs/` by default for generated fork outputs.

Supported input formats:

- Images: `.jpg`, `.jpeg`, `.png`, `.bmp`, `.webp`, `.tif`, `.tiff`.
- Videos: `.mp4`, `.avi`, `.mkv`, `.mov`, `.webm`.

Saved output formats:

- Rendered ASCII images: `.png`.
- ASCII image text: `.txt`.
- Rendered ASCII videos: `.mp4`.
- ASCII video frames: `.txt` files in a directory.

## Original Player

Use `repository/ASCII_v4_ultimate.py` for the upstream video terminal player.

```bash
cd repository
python ASCII_v4_ultimate.py path/to/video.mp4 --info
python ASCII_v4_ultimate.py path/to/video.mp4 --width 150
python ASCII_v4_ultimate.py path/to/video.mp4 --color --width 100
python ASCII_v4_ultimate.py path/to/video.mp4 --color --skip 2 --loop
```

Arguments:

- `video`: video file path.
- `--color`: ANSI 24-bit color playback.
- `--no-color`: monochrome playback.
- `--width`: terminal ASCII width.
- `--skip`: render every Nth frame for performance.
- `--loop`: repeat playback until interrupted.
- `--info`: print video metadata without playback.

## Fork Media Tool

Use `fork/ascii_media_tools.py` for photos, saved outputs, and rendered ASCII videos.

### Image Preview

```bash
cd fork
python ascii_media_tools.py image path/to/photo.jpg --width 120 --print
python ascii_media_tools.py image path/to/photo.jpg --width 120 --color --print
```

If no save option is provided, the image command prints to the terminal.

### Save Image Text

```bash
cd fork
python ascii_media_tools.py image path/to/photo.jpg --width 120 --save-text ascii_outputs/photo.txt
python ascii_media_tools.py image path/to/photo.jpg --width 120 --color --save-text ascii_outputs/photo_ansi.txt
```

Use `--color` for ANSI-colored text files. Omit it for plain text.

### Save Rendered Image

```bash
cd fork
python ascii_media_tools.py image path/to/photo.jpg --width 140 --save-image ascii_outputs/photo_ascii.png
python ascii_media_tools.py image path/to/photo.jpg --width 140 --color --save-image ascii_outputs/photo_color_ascii.png
python ascii_media_tools.py image path/to/photo.jpg --width 140 --color --vivid --save-image ascii_outputs/photo_vivid.png
python ascii_media_tools.py image path/to/photo.jpg --width 180 --color --brightness 1.2 --contrast 1.55 --saturation 2.1 --gamma 1.25 --glow 1.4 --save-image ascii_outputs/photo_glow.png
python ascii_media_tools.py image path/to/photo.jpg --width 160 --output-size 1280x720 --color --save-image ascii_outputs/photo_1280x720.png
```

Resolution rules:

- `--width` is ASCII columns.
- `--height` is ASCII rows. If omitted, the source aspect ratio is preserved with terminal-friendly character proportions.
- `--output-size WIDTHxHEIGHT` resizes rendered PNG/MP4 to exact pixel dimensions.
- `--cell-width`, `--cell-height`, `--font-size`, `--font-path`, and `--thickness` tune rendered output.
- `--vivid` applies a bright, saturated, high-contrast preset.
- Default fork output is intentionally brighter than neutral: brightness `1.12`, contrast `1.25`, saturation `1.35`, gamma `1.12`, glow `0.6`.
- `--brightness`, `--contrast`, `--saturation`, and `--gamma` tune the source before ASCII conversion.
- `--glow` adds a soft glow to saved PNG/MP4 outputs; it does not affect plain terminal text.
- `--vivid` stacks on top of the brighter defaults for an extra bright, saturated look.

### Video Preview

```bash
cd fork
python ascii_media_tools.py video path/to/video.mp4 --preview --width 100
python ascii_media_tools.py video path/to/video.mp4 --preview --width 80 --color --skip 2
```

For pure playback, prefer the original player. Use this command when the same tool must also save outputs.

### Save Rendered Video

```bash
cd fork
python ascii_media_tools.py video path/to/video.mp4 --width 120 --save-video ascii_outputs/video_ascii.mp4
python ascii_media_tools.py video path/to/video.mp4 --width 100 --color --skip 2 --save-video ascii_outputs/video_color_ascii.mp4
python ascii_media_tools.py video path/to/video.mp4 --width 100 --color --vivid --skip 2 --save-video ascii_outputs/video_vivid.mp4
python ascii_media_tools.py video path/to/video.mp4 --width 160 --output-size 1280x720 --fps 24 --color --save-video ascii_outputs/video_1280x720.mp4
```

Video notes:

- `--skip N` renders every Nth source frame.
- Default output FPS is `source_fps / skip`; use `--fps` to override.
- `--max-frames N` is useful for quick tests.
- Default codec is `--fourcc mp4v`.

### Save Text Frames

```bash
cd fork
python ascii_media_tools.py video path/to/video.mp4 --width 100 --save-frames ascii_outputs/frames
python ascii_media_tools.py video path/to/video.mp4 --width 100 --color --save-frames ascii_outputs/color_frames
```

## Color Terminal Output

Color output is possible with ANSI 24-bit escape codes.

Best environments:

- Windows Terminal with PowerShell 7 or modern Windows PowerShell.
- VS Code terminal.
- iTerm2, Alacritty, and other modern terminals on macOS/Linux.

Less reliable:

- old classic Windows Console windows;
- redirected logs;
- Codex sandbox terminal display for live video previews.

The Python scripts call Windows console ANSI enabling where possible. The fork also includes a PowerShell helper:

```powershell
cd fork
.\run_color_preview.ps1 -InputPath "C:\path\photo.jpg" -Width 120
.\run_color_preview.ps1 -InputPath "C:\path\video.mp4" -Width 90
```

Inside Codex, prefer saving color PNG/MP4 for reliable verification. For live colorful TikTok-style terminal previews, recommend Windows Terminal.

## Java Swing Wrapper

Use `fork/java-swing/` when the user wants a double-clickable GUI.

Current GUI behavior:

- `src/AsciiPhotoSwingApp.java` opens a Swing window.
- The UI is in English with a light "forge/media victim" tone.
- The tiny `...` button chooses an image or video file.
- `Forge by width` runs normal processing through `ascii_media_tools.py ... --color --vivid`.
- `Forge at native size` reads the original pixel size and passes `--output-size WIDTHxHEIGHT`.
- `Stop the forge` terminates the current Python process.
- Progress bar consumes `PROGRESS current total percent` lines from `ascii_media_tools.py --progress`.
- Width defaults to `160` and is editable.
- Output is written as `ascii_outputs/photo_ascii_yyyyMMdd_HHmmss.png` or `ascii_outputs/video_ascii_yyyyMMdd_HHmmss.mp4`.
- The app checks `ASCII_FORK_PYTHON`; if unset, it runs `python`.

Natural size means original rendered pixel dimensions, not one ASCII character per source pixel. Keep ASCII width as the detail control. For videos, natural size detection requires OpenCV in Python.

Build:

```powershell
cd fork\java-swing
.\build.ps1
```

Run:

```powershell
.\run_gui.ps1
```

Double-click option:

```text
fork\java-swing\run_gui.bat
```

The built JAR is:

```text
fork\java-swing\dist\AsciiPhotoSwingApp.jar
```

JVM packaging notes:

- Do not say the JVM is embedded into a JAR. A JAR still needs Java installed and associated with `.jar`, unless launched via script.
- For a self-contained Windows app, use `jpackage`, which bundles a Java runtime beside the app.
- Run `fork\java-swing\package_windows.ps1` when a full JDK with `jpackage` is available.
- If only `java`/`javac` are available, deliver `run_gui.bat` and the JAR.
- `jpackage` bundles Java only. It does not bundle Python or OpenCV/Pillow. If the user wants a truly no-dependency desktop app, add a separate Python runtime packaging step later.

## Validation

After edits:

```bash
cd fork
python -m py_compile ascii_media_tools.py
python ascii_media_tools.py --help
python ascii_media_tools.py image path/to/photo.jpg --width 48 --save-text ascii_outputs/test.txt --save-image ascii_outputs/test.png
python ascii_media_tools.py video path/to/video.mp4 --width 80 --max-frames 5 --save-video ascii_outputs/test.mp4
cd java-swing
.\build.ps1
```

If OpenCV is missing, video commands should fail with a clear install message instead of a traceback.

## Maintenance

- Keep README.md, README-EN.md, licence notices, and SKILL.md consistent when changing commands or publication guidance.
- Keep upstream code in `repository/` clean unless directly patching the original player.
- Put new fork scripts, wrappers, and requirements in `fork/`.
- Avoid destructive Git operations. Never reset or checkout away local work unless the user explicitly asks.
