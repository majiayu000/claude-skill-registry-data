---
name: Screenshot
description: Capture screens, windows, and regions across platforms with the right tools.
metadata: {"clawdbot":{"emoji":"📸","os":["linux","darwin","win32"]}}
---

## macOS

- Use `screencapture` (built-in): `screencapture -x output.png` for silent capture, `-i` for interactive selection
- Capture specific window by PID: `screencapture -l$(osascript -e 'tell app "AppName" to id of window 1') out.png`
- For retina displays, output is 2x resolution by default — add `-R x,y,w,h` to capture exact pixel region
- iOS Simulator: `xcrun simctl io booted screenshot output.png` — faster and more reliable than screencapture

## Linux

- `gnome-screenshot` for GNOME, `spectacle` for KDE, `scrot` for minimal/headless
- Headless X11: `xvfb-run scrot output.png` — creates virtual display for CI environments
- Wayland sessions break X11 tools silently — use `grim` for Wayland, `slurp` for region selection

## Windows

- PowerShell built-in: `Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.Screen]::PrimaryScreen | ...` is verbose — prefer `nircmd savescreenshot`
- `nircmd savescreenshot output.png` works from CLI without dependencies on most Windows versions
- For programmatic capture, `python -m PIL.ImageGrab` works cross-platform but requires Pillow installed

## Web Pages

- Playwright: `npx playwright screenshot URL output.png --full-page` — handles JavaScript rendering and scrolling
- Always wait for network idle: `--wait-for-timeout=5000` or page never finishes loading dynamic content
- Full-page screenshots of long pages pixelate when viewed — split into viewport-sized chunks instead
- Puppeteer equivalent: `page.screenshot({fullPage: true})` after `networkidle0`

## Format and Quality

- PNG for UI/text (lossless), JPEG for photos (smaller files)
- JPEG quality 85-92 is optimal — below 80 shows artifacts on text, above 95 gains little
- WebP offers 25-35% smaller files than JPEG at same quality — supported everywhere except older Safari

## Automation Patterns

- Add timestamps to filenames: `screenshot-$(date +%Y%m%d-%H%M%S).png` — prevents overwrites in batch jobs
- For comparison testing, use identical viewport sizes — different resolutions create false diffs
- CI screenshot artifacts: compress with `pngquant` or `jpegoptim` before upload — saves storage and transfer time
