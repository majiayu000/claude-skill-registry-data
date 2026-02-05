---
name: axe
description: iOS Simulator automation and interaction using the AXe CLI tool. Use when working with iOS simulators for UI automation, testing, accessibility verification, or screen recording. Specific use cases include simulating touches and gestures (tap, swipe), entering text, pressing hardware buttons (home, lock, Siri), recording or streaming simulator video, extracting UI accessibility information, or automating iOS simulator interactions. Assumes axe CLI is already installed.
---

# AXe - iOS Simulator Automation

Automate iOS Simulator interactions using the AXe command-line tool, which leverages Apple's Accessibility APIs for UI testing, automation, and verification.

## Quick Start

All AXe commands require the simulator UDID. Get it first:

```bash
# List available simulators
axe list-simulators

# Store UDID in variable for convenience
UDID=$(axe list-simulators | grep "iPhone 15 Pro" | awk '{print $NF}')
```

## Core Operations

### Touch & Gesture Automation

**Tap at coordinates:**
```bash
axe tap -x 100 -y 200 --udid $UDID
```

**Swipe between points:**
```bash
axe swipe --start-x 300 --start-y 200 --end-x 100 --end-y 200 --udid $UDID
```

**Use gesture presets:**
```bash
# Common gestures
axe gesture scroll-down --udid $UDID
axe gesture swipe-from-left-edge --udid $UDID

# Available: scroll-up, scroll-down, scroll-left, scroll-right,
#            swipe-from-left-edge, swipe-from-right-edge,
#            swipe-from-top-edge, swipe-from-bottom-edge
```

### Text Input

```bash
# Direct text
axe type 'Hello World!' --udid $UDID

# From stdin
echo "Test message" | axe type --stdin --udid $UDID

# From file
axe type --file message.txt --udid $UDID
```

### Hardware Buttons

```bash
axe button home --udid $UDID
axe button lock --udid $UDID
axe button siri --udid $UDID

# Long press
axe button lock --duration 2.0 --udid $UDID
```

### Video Recording & Streaming

**Direct recording:**
```bash
# Press Ctrl+C to stop and finalize the MP4
axe record-video --udid $UDID --fps 30 --output recording.mp4
```

**Streaming:**
```bash
# Pipe to ffmpeg
axe stream-video --udid $UDID --fps 30 --format ffmpeg | \
  ffmpeg -f image2pipe -framerate 30 -i - output.mp4
```

### UI Accessibility Information

```bash
# Entire UI tree
axe describe-ui --udid $UDID

# Element at specific point
axe describe-ui --point 150,300 --udid $UDID
```

## Automation Workflow Patterns

### Sequential Actions with Timing

Use `--pre-delay` and `--post-delay` for reliable automation:

```bash
# Wait for animation before tap
axe tap -x 150 -y 300 --pre-delay 0.5 --udid $UDID

# Allow UI to respond after tap
axe tap -x 150 -y 300 --post-delay 1.0 --udid $UDID

# Chain actions with timing
axe tap -x 100 -y 200 --post-delay 0.5 --udid $UDID
axe type 'username' --post-delay 0.3 --udid $UDID
axe tap -x 100 -y 300 --post-delay 0.5 --udid $UDID
axe type 'password' --post-delay 0.3 --udid $UDID
axe button home --udid $UDID
```

### Multi-Step Test Scenarios

```bash
# Example: Login flow automation
UDID=$(axe list-simulators | grep "iPhone 15" | head -1 | awk '{print $NF}')

# Tap username field
axe tap -x 187 -y 300 --post-delay 0.5 --udid $UDID

# Enter username
axe type 'testuser@example.com' --post-delay 0.5 --udid $UDID

# Tap password field
axe tap -x 187 -y 400 --post-delay 0.5 --udid $UDID

# Enter password
axe type 'password123' --post-delay 0.5 --udid $UDID

# Tap login button
axe tap -x 187 -y 500 --post-delay 2.0 --udid $UDID
```

## Command Reference

For complete command documentation including all options and parameters, see [commands.md](references/commands.md).

**Quick reference of available commands:**
- `tap`, `swipe`, `touch` - Touch and gesture simulation
- `gesture` - Pre-configured gesture presets
- `type` - Text input with automatic shift handling
- `button` - Hardware button simulation (home, lock, siri, apple-pay)
- `key`, `key-sequence` - Low-level keyboard control with HID keycodes
- `stream-video`, `record-video` - Video capture and streaming
- `describe-ui` - Extract accessibility information
- `list-simulators` - List available simulators

## Tips

**Get UI coordinates:** Use `describe-ui` to find element positions before automating taps.

**Simulator state:** Ensure the target simulator is booted before running commands.

**Timing strategy:** Start with longer delays (0.5-1.0s) and reduce as needed for reliable automation.

**Video recording:** Always press Ctrl+C to properly finalize MP4 files. The output path is printed to stdout.

**UDID management:** Store UDID in a variable for cleaner scripts and reusability.
