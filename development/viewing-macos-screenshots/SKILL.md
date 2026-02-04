---
name: viewing-macos-screenshots
description: View and analyze macOS screenshots. Use when the user mentions screenshots, asks to see what they captured, says "look at my screenshot", "examine my last X screenshots", or wants help with something they screenshotted.
---

# Viewing macOS Screenshots

## Instructions

When the user wants to see or discuss their screenshots:

1. **Determine how many screenshots** the user wants:
   - Default: 1 (most recent)
   - If user says "last 3 screenshots" or "last X screenshots", use that number

2. **Find the screenshot location**:
   ```bash
   defaults read com.apple.screencapture location 2>/dev/null || echo "$HOME/Desktop"
   ```

3. **Find the screenshot files** (sorted by most recent):
   ```bash
   # For N screenshots, use head -N
   ls -t "$SCREENSHOT_DIR"/Screenshot*.png "$SCREENSHOT_DIR"/"Screen Shot"*.png 2>/dev/null | head -N
   ```

4. **Read each image** using the Read tool with the file path(s).

5. **Describe and analyze** what you see, then ask if the user has questions or needs help with what's shown.

## Trigger Phrases

Activate this skill when the user says things like:
- "look at my screenshot"
- "see what I captured"
- "check this screenshot"
- "what's in my latest screenshot"
- "examine my last 3 screenshots"
- "show me my recent screenshots"
- "I just took a screenshot"
- "here's a screenshot" (without providing a path)
