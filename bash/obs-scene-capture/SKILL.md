---
name: obs-scene-capture
description: Use OBS as a generic screenshot API. List scenes, inspect scene sources, and capture still images from scenes or sources via obs-websocket.
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [OBS, obs-websocket, Screenshot, Scene Capture, Source Capture, API]
---

# OBS Scene Capture API

Use this skill to treat OBS like a local screenshot API for any scene or source you have configured.

## What this gives you

- List all scenes currently available in OBS
- List sources inside a specific scene
- Capture PNG stills from a scene or source on demand
- Save captures to `TMP/obs/` for downstream analysis or sharing

## Prerequisites

- OBS is running
- OBS WebSocket server is enabled (default port `4455`)
- Python package `obsws-python` is installed in the active environment

Install dependency:

```bash
pip install obsws-python
```

If a local `venv` exists, activate it first.

## Quick start

List scenes:

```bash
python skills/integrations/obs-scene-capture/scripts/obs_still.py --list-scenes
```

List sources in a scene:

```bash
python skills/integrations/obs-scene-capture/scripts/obs_still.py --list-sources --scene "Main Monitor"
```

Capture a scene:

```bash
python skills/integrations/obs-scene-capture/scripts/obs_still.py --scene "Main Monitor" --output TMP/obs/main-monitor.png
```

Capture a source:

```bash
python skills/integrations/obs-scene-capture/scripts/obs_still.py --source "Browser Capture" --output TMP/obs/browser-capture.png
```

Optional explicit resolution:

```bash
python skills/integrations/obs-scene-capture/scripts/obs_still.py --scene "Main Monitor" --output TMP/obs/main-monitor-1440p.png --width 2560 --height 1440
```

## Connection options

Defaults:

- `--host localhost`
- `--port 4455`
- `--password ""`

Environment variable overrides:

- `OBS_HOST`
- `OBS_PORT`
- `OBS_PASSWORD`

## API-oriented workflow

1. Call `--list-scenes` to discover valid scene names.
2. Call `--list-sources --scene "..."` to inspect precise source names.
3. Capture the exact scene or source needed.
4. Return the saved file path (for example, `TMP/obs/main-monitor.png`) as an artifact for the next step in your flow.

## Notes

- Scene and source names are exact-match and case-sensitive.
- Scenes are valid screenshot targets, so scene capture is a good default when source names are unknown.
- The script writes PNG files and handles UTF-8-safe paths.

## More setup details

If OBS connection setup is the blocker, read `references/obs-websocket.md`.
