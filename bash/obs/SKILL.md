---
$schema: https://gist.githubusercontent.com/remorses/9f3737a6f516c01f4bdb612045c64072/raw/agent-skill.schema.json
name: obs
description: >
  Control OBS Studio via CLI using obs-cmd and obs-websocket v5.
  Covers streaming, recording, window/screen capture, audio control,
  scene management, and RTMP configuration on macOS.
  Load this skill when automating OBS, setting up live streams,
  or controlling OBS from scripts or agents.
---

# OBS Studio CLI Control

Control OBS Studio programmatically via its built-in WebSocket server using `obs-cmd`.

## References

- **obs-websocket protocol**: https://github.com/obsproject/obs-websocket/blob/master/docs/generated/protocol.md
- **obs-cmd CLI**: https://github.com/grigio/obs-cmd
- **OBS launch parameters**: https://obsproject.com/wiki/Launch-Parameters

## Setup

### Install OBS

```bash
brew install --cask obs
```

### Install obs-cmd

Download the latest arm64 macOS binary from GitHub releases:

```bash
gh release download --repo grigio/obs-cmd --pattern 'obs-cmd-arm64-macos.tar.gz' --dir /tmp
tar xzf /tmp/obs-cmd-arm64-macos.tar.gz -C /tmp
cp /tmp/obs-cmd /opt/homebrew/bin/obs-cmd
chmod +x /opt/homebrew/bin/obs-cmd
```

### Enable WebSocket server

OBS 28+ ships with obs-websocket built in. Enable it once:

1. Open OBS → **Tools → WebSocket Server Settings**
2. Check **Enable WebSocket server**
3. Set a password or disable auth for local use
4. Default port: 4455

### Connection

```bash
# Set once per shell session
export OBS_WEBSOCKET_URL='obsws://localhost:4455/'

# With password
export OBS_WEBSOCKET_URL='obsws://localhost:4455/yourpassword'

# Or pass per-command
obs-cmd --websocket 'obsws://localhost:4455/' info
```

Always verify the connection works before sending commands:

```bash
obs-cmd info
```

## macOS capture source types

| Input kind | What it captures | Notes |
|---|---|---|
| `screen_capture` | ScreenCaptureKit-based. Can capture a specific window, app, or display. **Preferred on macOS.** | Uses `desktopIndependentWindow` internally; captures even from other Spaces |
| `window_capture` | Legacy window capture | Less performant on macOS, prefer `screen_capture` |
| `display_capture` | Entire display | Captures whatever Space is active |
| `sck_audio_capture` | ScreenCaptureKit audio only | System audio without video |

**Always use `screen_capture` on macOS** for window-level capture. It uses ScreenCaptureKit under the hood and can capture a specific window even if it's on another Space or behind other windows.

## Streaming to X (Twitter)

### Configure stream service

```bash
obs-cmd stream-service set \
  --service-type rtmp_custom \
  --server 'rtmps://ca.pscp.tv:443/x' \
  --key 'YOUR_STREAM_KEY'
```

X's RTMP endpoints (from Creator Studio → Go Live):

| Protocol | URL |
|---|---|
| RTMP | `rtmp://ca.pscp.tv:80/x` |
| RTMPS | `rtmps://ca.pscp.tv:443/x` |

### X streaming requirements

```bash
obs-cmd video-settings set \
  --base-width 1920 --base-height 1080 \
  --output-width 1920 --output-height 1080 \
  --fps-num 30 --fps-den 1
```

| Setting | Value |
|---|---|
| Video codec | H.264/AVC |
| Resolution | 1920x1080 |
| Framerate | 30 fps |
| Video bitrate | 9000 kbps (max) |
| Keyframe interval | 3 seconds |
| Audio codec | AAC |
| Audio sample rate | 44100 Hz |
| Audio bitrate | 128 kbps |
| Audio channels | 2 (stereo) |

Video bitrate and encoder settings must be configured in OBS output settings (not exposed via obs-cmd). Set these in **Settings → Output → Streaming**: encoder = Apple VT H264 Hardware Encoder, bitrate = 9000 kbps, keyframe interval = 3.

### Start/stop streaming

```bash
obs-cmd streaming start
obs-cmd streaming stop
obs-cmd streaming status
obs-cmd streaming toggle
```

## Scene management

```bash
# List scenes
obs-cmd scene list

# Get current scene
obs-cmd scene current

# Switch scene
obs-cmd scene switch 'My Scene'

# Create a new scene
obs-cmd scene create 'Stream Scene'
```

## Input (source) management

### List inputs and available kinds

```bash
# List all current inputs
obs-cmd input list

# List available input types
obs-cmd input list-kinds
```

### Create a window capture source (macOS)

Use `screen_capture` kind for ScreenCaptureKit-based capture. The settings JSON controls what gets captured:

```bash
# Create a screen_capture source targeting a specific app/window
obs-cmd input create 'ChatGPT Window' screen_capture \
  --scene 'Scene' \
  --settings '{"type": 1, "window": 93}'
```

The `type` field in `screen_capture` settings:

| Value | Capture mode |
|---|---|
| 0 | Display capture (entire screen) |
| 1 | Window capture (specific window) |
| 2 | Application capture (all windows of an app) |

The `window` field takes the CGWindowID. Find it with:

```bash
swift -e '
import CoreGraphics
let windows = CGWindowListCopyWindowInfo(.optionAll, kCGNullWindowID) as! [[String: Any]]
for w in windows {
    let owner = w[kCGWindowOwnerName as String] as? String ?? ""
    let title = w[kCGWindowName as String] as? String ?? ""
    let id = w[kCGWindowNumber as String] as? Int ?? 0
    let layer = w[kCGWindowLayer as String] as? Int ?? -1
    let bounds = w[kCGWindowBounds as String] as? [String: Any] ?? [:]
    if layer == 0 && (bounds["Width"] as? Int ?? 0) > 100 {
        print("id=\(id) owner=\(owner) title=\(title) w=\(bounds["Width"] ?? 0)x\(bounds["Height"] ?? 0)")
    }
}
'
```

### Modify input settings

```bash
# Get current settings
obs-cmd input settings 'My Source' --get

# Update settings
obs-cmd input settings 'My Source' --set '{"key": "value"}'
```

### Remove an input

```bash
obs-cmd input remove 'Source Name'
```

## Scene items (show/hide sources in a scene)

```bash
# List items in a scene
obs-cmd scene-item list 'Scene'

# Disable (hide) a source
obs-cmd scene-item disable 'Scene' 'Webcam'

# Enable (show) a source
obs-cmd scene-item enable 'Scene' 'ChatGPT Window'

# Toggle visibility
obs-cmd scene-item toggle 'Scene' 'Source Name'
```

## Disabling audio, mic, and camera

### Mute all audio sources

```bash
# Mute desktop/system audio
obs-cmd audio mute 'Desktop Audio'

# Mute microphone
obs-cmd audio mute 'Mic/Aux'

# Or mute by input name
obs-cmd input mute 'Audio Input Capture' mute
obs-cmd input mute 'Audio Output Capture' mute

# Check mute status
obs-cmd audio status 'Desktop Audio'
obs-cmd input mute 'Audio Input Capture' status
```

### Disable camera and other sources

Hide them from the scene (they stay configured but invisible):

```bash
obs-cmd scene-item disable 'Scene' 'Cam'
obs-cmd scene-item disable 'Scene' 'Audio Input Capture'
obs-cmd scene-item disable 'Scene' 'Audio Output Capture'
obs-cmd scene-item disable 'Scene' 'Desktop Audio'
```

Or remove them entirely:

```bash
obs-cmd input remove 'Cam'
```

## Recording

```bash
obs-cmd recording start
obs-cmd recording stop
obs-cmd recording toggle
obs-cmd recording status

# Set recording directory
obs-cmd record-directory set '/path/to/recordings'
```

## Full workflow: stream a specific window to X

```bash
export OBS_WEBSOCKET_URL='obsws://localhost:4455/'

# 1. Create a clean scene
obs-cmd scene create 'X Stream'
obs-cmd scene switch 'X Stream'

# 2. Find the target window ID
# (use the Swift snippet from "Create a window capture source" section)

# 3. Add window capture source
obs-cmd input create 'App Window' screen_capture \
  --scene 'X Stream' \
  --settings '{"type": 1, "window": WINDOW_ID}'

# 4. Configure stream destination
obs-cmd stream-service set \
  --service-type rtmp_custom \
  --server 'rtmps://ca.pscp.tv:443/x' \
  --key 'YOUR_STREAM_KEY'

# 5. Set video output
obs-cmd video-settings set \
  --base-width 1920 --base-height 1080 \
  --output-width 1920 --output-height 1080 \
  --fps-num 30 --fps-den 1

# 6. Mute all audio (no mic, no system audio)
obs-cmd audio mute 'Desktop Audio' 2>/dev/null
obs-cmd audio mute 'Mic/Aux' 2>/dev/null

# 7. Start streaming
obs-cmd streaming start

# 8. Check status
obs-cmd streaming status
```

## macOS Spaces and window visibility

**Windows on other Spaces appear blank or black.** This is a known macOS limitation. The compositor doesn't render windows on inactive Spaces, so ScreenCaptureKit has nothing to capture. OBS will also not list these windows in its window picker.

To capture a specific window:

1. **Move the target window to the same Space** where OBS is running (or any active Space)
2. Use `screen_capture` with `type: 1` (window capture) to capture only that window
3. The stream will show only the window content, not the full screen or other apps

The window does NOT need to be in the foreground. It just needs to be on an active Space. Once selected, OBS captures only the window content regardless of what's on top of it.

If the app has multiple windows (e.g. a main window + small popups), make sure you select the correct one. OBS may list the popup instead of the main window.

## Using obs-websocket-js instead of obs-cmd

`obs-cmd input create` is marked experimental and often fails silently (says success but doesn't create the input). For reliable source creation, use `obs-websocket-js` via Bun/Node:

```bash
bun install obs-websocket-js
```

```typescript
import OBSWebSocket from 'obs-websocket-js'
const obs = new OBSWebSocket()
await obs.connect('ws://localhost:4455')

// Create a window capture source
await obs.call('CreateInput', {
  sceneName: 'Scene',
  inputName: 'My Window',
  inputKind: 'screen_capture',
  inputSettings: { type: 1, show_cursor: true, hide_obs: true },
})

// List available windows (OBS uses its own window IDs, not CGWindowIDs)
const props = await obs.call('GetInputPropertiesListPropertyItems', {
  inputName: 'My Window',
  propertyName: 'window',
})
for (const w of props.propertyItems as any[]) {
  console.log(`${w.itemValue}: ${w.itemName}`)
  // e.g. "1477: [ChatGPT] ChatGPT"
}

// Set the correct window
await obs.call('SetInputSettings', {
  inputName: 'My Window',
  inputSettings: { type: 1, window: 1477 },
})

// Fit source to 1920x1080 canvas
const items = await obs.call('GetSceneItemList', { sceneName: 'Scene' })
const item = (items.sceneItems as any[]).find((i: any) => i.sourceName === 'My Window')
await obs.call('SetSceneItemTransform', {
  sceneName: 'Scene',
  sceneItemId: item.sceneItemId,
  sceneItemTransform: {
    boundsType: 'OBS_BOUNDS_SCALE_INNER',
    boundsWidth: 1920,
    boundsHeight: 1080,
    boundsAlignment: 0,
    positionX: 0,
    positionY: 0,
  },
})

// Start streaming
await obs.call('StartStream')
obs.disconnect()
```

Prefer `obs-websocket-js` for: creating inputs, listing available windows/apps, setting transforms, and any operation where `obs-cmd` says "experimental".

## OBS window IDs vs CGWindowIDs

OBS uses its own window identification. The IDs from `CGWindowListCopyWindowInfo` (used in the Swift snippet) may not match what OBS expects. Always use `GetInputPropertiesListPropertyItems` with `propertyName: 'window'` to get the OBS-compatible window IDs. The property items include `itemName` (format: `[AppName] WindowTitle`) and `itemValue` (the ID to pass as `window` in settings).

## Why not ffmpeg for window capture on macOS

ffmpeg's `avfoundation` cannot capture a specific window. It always captures the entire physical display. For window-level capture on macOS, OBS with `screen_capture` (ScreenCaptureKit) is the only reliable option.

If using ffmpeg for full-screen capture:

- **Retina displays**: don't pass `-video_size`; let avfoundation capture at native resolution and scale down with `-vf 'scale=1920:1080'`
- **Pixel format**: use `-pixel_format uyvy422` (native avfoundation format). Forcing `yuv420p` at capture causes stripe artifacts
- **Encoder**: use `h264_videotoolbox` (hardware) instead of `libx264`. Software encoding with avfoundation causes visual corruption (stripes, random pixels)
- **Format pipeline**: explicit conversion chain `'format=nv12,scale=1920:1080'` avoids pixel format mismatch artifacts

## Gotchas

- **obs-cmd `input create` and `input settings` are experimental** and often fail silently. Use `obs-websocket-js` for reliable source management.
- **Video encoder and bitrate** are not configurable via obs-cmd. Set them in OBS GUI: Settings → Output → Streaming.
- **Screen recording permission** must be granted to OBS in System Settings → Privacy & Security → Screen Recording.
- **`screen_capture` is macOS-specific.** On Linux use `xshm_input` or `pipewire-screen-capture-source`. On Windows use `window_capture` or `game_capture`.
- **Window IDs change** when an app restarts. If the capture goes black after an app restart, re-detect the window ID and update the source settings.
- **First launch** requires manual WebSocket server enablement in OBS GUI. Subsequent launches remember the setting.
- **Windows on other macOS Spaces are invisible** to ScreenCaptureKit and will appear black. Move the target window to an active Space before capturing.
