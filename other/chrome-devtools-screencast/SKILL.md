---
name: chrome-devtools-screencast
description: Capture screenshots and record live screencasts from Chrome via DevTools MCP. Use for visual regression, agent state verification, bug reproduction capture, and frame-by-frame UI analysis.
origin: https://github.com/ChromeDevTools/chrome-devtools-mcp (Apache-2.0)
license: Apache-2.0
version: 1.0.0
compatibility: claude-sonnet-4-6, claude-opus-4-7
---

# Chrome DevTools Screencast

Capture visual output from a live Chrome browser using screenshot and screencast MCP tools.

## When to Use

- Verifying UI state during agent-driven test flows ("did the modal appear?")
- Bug reproduction: capture sequence of frames leading to a visual glitch
- Visual regression: screenshot before/after a code change
- Recording a screencast of an agent interacting with a web app (demo/audit trail)
- Capturing responsive layout at different viewport sizes

## Do NOT use for

- Video encoding for delivery (output is raw frames — use ffmpeg to encode)
- Replacing automated visual diff tools like Percy (for PR-level regression at scale)
- Screenshots of terminal / non-browser content

## MCP Tools

```
browser_screenshot          — capture current page as PNG (base64 or file path)
browser_start_screencast    — begin frame capture (configurable fps, quality)
browser_stop_screencast     — stop capture, returns frame sequence + metadata
```

## Usage Pattern

```yaml
# Single screenshot — state verification
1. browser_navigate: url: "https://app.example.com/dashboard"
2. browser_wait_for: selector: "[data-testid='dashboard-loaded']"
3. browser_screenshot:
     fullPage: true
     path: "./screenshots/dashboard.png"

# Screencast — record agent interaction
1. browser_start_screencast:
     fps: 10
     quality: 80          # 0–100 JPEG quality
     maxWidth: 1280

2. browser_navigate: url: "https://app.example.com"
3. browser_click: selector: "#open-modal"
4. browser_wait_for: selector: ".modal-visible"
5. browser_fill: selector: ".modal input", value: "test data"
6. browser_click: selector: ".modal .submit"

7. browser_stop_screencast:
   # → returns: frames[], duration, frameCount, outputDir
```

## Screenshot Response

```json
{
  "data": "<base64-encoded-PNG>",
  "path": "./screenshots/dashboard.png",
  "width": 1280,
  "height": 800,
  "timestamp": "2026-05-23T10:42:11Z"
}
```

## Visual Regression Workflow

```yaml
# Baseline capture
browser_screenshot: path: "./baselines/homepage-baseline.png"

# After code change
browser_screenshot: path: "./current/homepage-current.png"

# Compare (use pixelmatch or looks-same CLI)
pixelmatch baselines/homepage-baseline.png current/homepage-current.png diff.png
# → reports pixel difference percentage
# PASS if diff < 0.1%, REVIEW if 0.1–1%, FAIL if > 1%
```

## Device + Screenshot Combo

```yaml
# Test responsive layout at multiple breakpoints
for device in ["iPhone 14 Pro", "iPad Pro", "Desktop HD"]:
  browser_emulate_device: device: device
  browser_screenshot: path: "./screenshots/${device}.png"
```

## Anti-Fake-Pass Checklist

- [ ] Screenshot taken AFTER `browser_wait_for` — not immediately after navigate
- [ ] `fullPage: true` used when testing layouts (viewport-only misses below-fold)
- [ ] Screencast frame count > 0 before declaring recording successful
- [ ] Output path written to disk and verified readable (not just base64 in memory)
- [ ] Visual diff run against actual baseline — not "looks fine to me" manual review
