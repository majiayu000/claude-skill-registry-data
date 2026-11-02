---
name: virtual-avatar
description: Give Lu (or any AI agent) a visible avatar presence in Discord video calls and streaming. Covers the full pipeline for avatar model acquisition, real-time rendering software, WebSocket API integration for programmatic control, OBS virtual camera setup, and Discord video configuration. Use when setting up, troubleshooting, or upgrading an avatar pipeline.
---

# Virtual Avatar Pipeline

## Overview

This skill covers the end-to-end process of giving an AI agent a visible, animated avatar in video calls and streams. The typical architecture:

```
AI Agent (Linux VM)
  → WebSocket API (local network)
    → Avatar Renderer (Windows PC: VTube Studio, etc.)
      → OBS Virtual Camera
        → Discord / Zoom / etc.
```

## Key Constraint: Platform Split

**VTube Studio is Windows-only.** If the AI agent runs on a Linux VM (headless, no display), the avatar rendering must happen on a separate Windows machine on the same local network. Plan accordingly.

## Architecture Options

### Option A: VTube Studio (Recommended for Live2D)

- **Renderer:** VTube Studio (free, Steam)
- **Model format:** Live2D Cubism
- **API:** WebSocket on `ws://<host-ip>:8001`
- **Python library:** `pyvts` (`pip install pyvts`)
- **Pros:** Full Live2D rigging, huge ecosystem, proven
- **Cons:** Windows-only, requires separate machine

### Option B: Web-Based Avatar (Linux-native)

- **Renderer:** Python + Pillow/Pygame generating frames
- **Output:** FFmpeg pipe → v4l2loopback (needs sudo + kernel module)
- **Pros:** Runs entirely on Linux VM
- **Cons:** No Live2D rigging, needs v4l2loopback, more custom code

### Option C: PNGtuber (Simplest)

- **Renderer:** Swap PNG images for expressions
- **Can run in browser** → OBS captures browser tab
- **Pros:** Dead simple
- **Cons:** Least expressive

## VTube Studio API Essentials

See `references/vtube-studio-api.md` for full API details.

**Key facts:**
- WebSocket: `ws://localhost:8001` (default, user-configurable)
- Must authenticate as a plugin first (one-time token, then reuse)
- Feed tracking data via `InjectParameterDataRequest`
- **Parameter data expires after 1 second** — must re-send at least once/sec
- Only one plugin can control a parameter at a time
- Custom parameters can be created via `ParameterCreationRequest`
- Values range: `-1000000` to `1000000` (float)
- Optional `weight` field (0-1) for blending with face tracking

## OBS → Discord Pipeline

1. Add VTube Studio window as OBS source (Window Capture)
2. Start OBS Virtual Camera (built-in for OBS 28+, or install plugin)
3. Discord → Settings → Voice & Video → Camera → select "OBS Virtual Camera"

## Avatar Model Sources

- **Free:** Live2D Cubism sample models, VTube Studio defaults
- **Marketplace:** Booth.pm (some free, mostly paid, Japanese)
- **3D alternative:** VRoid Hub (free 3D models, needs different renderer)
- **Custom commission:** $200-800 for a Live2D rigged model

## Common Pitfalls

1. **Token revocation:** If user revokes API access, all custom parameters are deleted. Store the token and re-authenticate automatically.
2. **Parameter timeout:** Forgetting to send data every 1 second causes the parameter to revert. Always maintain a heartbeat loop.
3. **Network latency:** Keep the renderer on the same LAN as the agent for minimal lag.
4. **OBS virtual cam:** On Windows, OBS 28+ has built-in virtual camera. On older versions, install the obs-virtualcam plugin separately.
5. **Live2D parameter mapping:** Custom parameters must be manually mapped to Live2D model parameters in VTube Studio's UI. This is a one-time setup per model.
6. **Firewall:** VTube Studio's WebSocket server may be blocked by Windows Firewall. Add an exception for the port.

## Future Enhancements

- Voice sync via desktop audio analysis
- Eye tracking based on active speaker
- Chat command → expression triggers
- Custom Live2D model based on agent's self-portrait
- Upgrade path to 3D (VRM) models
- Physical robot body with screen display (long-term)

## Related Skills

- `self-portrait` — Generate avatar reference images using AI image models
- `architecture-diagram` — Diagram the avatar pipeline architecture
- `petdex` (bundled) — Lightweight state-reactive pet sprites (CLI/TUI/desktop). Pets are simpler than full avatars — they react to agent activity state without face tracking. Good as a stepping stone to a full avatar body.
- `local-tts` — Install and benchmark local/offline TTS engines (Piper). Provides the voice half of digital presence; pair with avatar visual for full embodiment.
