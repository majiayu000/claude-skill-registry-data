---
name: cleanshot
description: Take screenshots, screen recordings, scrolling captures, and OCR text recognition using CleanShot X. Use when user requests screenshots, captures, screen recording, OCR, text extraction, or image annotation.
allowed-tools: [Bash]
---

# CleanShot X CLI

Use the `cleanshot` command to trigger CleanShot X actions.

## Basic usage

```bash
cleanshot <subcommand> [flags]
```

## Subcommands

### Query commands
- `latest` - Print path of most recent screenshot

### Capture commands
- `all-in-one` - Launch all-in-one capture tool
- `capture-area` - Area capture
- `capture-fullscreen` - Fullscreen capture
- `capture-window` - Window capture
- `capture-previous-area` - Repeat last screenshot
- `self-timer` - Self-timer capture
- `scrolling-capture` - Scrolling capture

### Recording
- `record-screen` - Screen recording

### OCR
- `capture-text` - OCR text recognition

### Utility
- `pin` - Pin image file
- `open-annotate` - Annotate image file
- `open-from-clipboard` - Annotate clipboard image
- `toggle-desktop-icons` - Toggle desktop icons visibility
- `hide-desktop-icons` - Hide desktop icons
- `show-desktop-icons` - Show desktop icons
- `add-quick-access-overlay` - Add quick access overlay
- `open-history` - Open capture history
- `restore-recently-closed` - Restore recently deleted
- `open-settings` - Open settings

## Flags

### Coordinate parameters
- `-x <int>` - X coordinate (origin at lower left)
- `-y <int>` - Y coordinate
- `-width <int>` - Width in pixels
- `-height <int>` - Height in pixels
- `-display <int>` - Display number (1=main, 2=secondary, etc.)

### Action parameters
- `-action <string>` - Post-capture action: `copy`, `save`, `annotate`, `upload`, `pin`
- `-filepath <path>` - File path for pin/annotate/OCR
- `-tab <string>` - Settings tab: `general`, `wallpaper`, `shortcuts`, `quickaccess`, `recording`, `screenshots`, `annotate`, `cloud`, `advanced`, `about`
- `-path <dir>` - Screenshot directory (default: `~/Downloads/screens`)

### Boolean flags
- `-start` - Auto-start scrolling capture
- `-autoscroll` - Enable automatic scrolling
- `-linebreaks` - Preserve line breaks in OCR text

## Examples

```bash
# Get latest screenshot
cleanshot latest
cleanshot latest -path ~/Pictures/screenshots

# Simple captures
cleanshot capture-area
cleanshot capture-fullscreen

# With coordinates
cleanshot capture-area -x 100 -y 120 -width 200 -height 150

# Save and print path
cleanshot capture-area -action save
cleanshot capture-fullscreen -action save -path ~/Pictures/screenshots

# Scrolling capture
cleanshot scrolling-capture -start -autoscroll

# Screen recording with region
cleanshot record-screen -x 0 -y 0 -width 1920 -height 1080 -display 1

# OCR
cleanshot capture-text -linebreaks
cleanshot capture-text -filepath ~/screenshot.png

# Annotate
cleanshot open-annotate -filepath ~/screenshot.png
cleanshot open-from-clipboard

# Settings
cleanshot open-settings -tab shortcuts

# Help
cleanshot help
```

## Key features

- Automatically detects and prints screenshot path when using `-action save`
- Default screenshot directory: `~/Downloads/screens`
- Boolean flags don't require values
- Waits up to 10 seconds for screenshot to appear

## Usage examples

When user requests:
- "what's my latest screenshot" → `cleanshot latest`
- "get the most recent screenshot path" → `cleanshot latest`
- "take a screenshot" → `cleanshot capture-area` or `cleanshot capture-fullscreen`
- "save a screenshot" → `cleanshot capture-area -action save`
- "record my screen" → `cleanshot record-screen`
- "extract text from image" → `cleanshot capture-text -filepath <path>`
- "annotate this image" → `cleanshot open-annotate -filepath <path>`
- "hide desktop icons" → `cleanshot hide-desktop-icons`
- "scrolling screenshot" → `cleanshot scrolling-capture`
- "capture this specific region" → use coordinate parameters

Always confirm which capture type the user wants if ambiguous.
