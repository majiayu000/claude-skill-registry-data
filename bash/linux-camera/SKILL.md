---
name: linux-camera
version: 1.0.0
author: johnnynunez
description: Capture photos, record video clips, list cameras, and live stream on Linux. Uses V4L2 and ffmpeg. Supports USB webcams and RTSP/IP cameras.
triggers:
  - camera
  - photo
  - picture
  - take a photo
  - snapshot
  - webcam
  - video
  - record
  - stream
  - capture
  - front camera
  - back camera
tools:
  - exec
---

# Linux Camera Skill

Camera capture skill for Linux systems. Supports USB webcams (V4L2) and network cameras (RTSP).

> **Skill directory:** `~/.openclaw/workspace/skills/linux-camera/`

## Dependencies

```bash
sudo apt-get install -y ffmpeg v4l-utils
```

## Scripts

### 0. Quick photo (`camera_photo.py`) — simplest way to take a photo

No flags needed. Just run it.

```bash
uv run python scripts/camera_photo.py              # auto-detect camera, timestamped filename
uv run python scripts/camera_photo.py front         # use /dev/video0
uv run python scripts/camera_photo.py back          # use /dev/video2
uv run python scripts/camera_photo.py front pic.jpg # custom filename → /tmp/pic.jpg
uv run python scripts/camera_photo.py /dev/video4   # explicit device path
```

Camera aliases: `front` = `/dev/video0`, `back` = `/dev/video2`. Output goes to `/tmp/` by default.

### 1. List available cameras (`camera_list.py`)

Detects all V4L2 video devices and prints their names, paths, and supported formats.

```bash
uv run python scripts/camera_list.py
```

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--json` | Output as JSON | off |

### 2. Take a snapshot (`camera_snap.py`) — primary, recommended

Captures a single frame from a camera and saves it as a JPEG.

```bash
uv run python scripts/camera_snap.py --output /tmp/snapshot.jpg
```

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--device` | V4L2 device path | `/dev/video0` |
| `--rtsp` | RTSP URL (use instead of `--device` for IP cameras) | — |
| `--output` | Output file path | `/tmp/camera_snap.jpg` |
| `--width` | Capture width | `1280` |
| `--height` | Capture height | `720` |
| `--warmup` | Warmup frames to skip (for exposure adjustment) | `5` |
| `--quality` | JPEG quality (1–100) | `90` |

### 3. Record a video clip (`camera_clip.py`)

Records a video clip from a camera.

```bash
uv run python scripts/camera_clip.py --duration 5 --output /tmp/clip.mp4
```

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--device` | V4L2 device path | `/dev/video0` |
| `--rtsp` | RTSP URL (use instead of `--device` for IP cameras) | — |
| `--output` | Output file path | `/tmp/camera_clip.mp4` |
| `--duration` | Recording duration in seconds | `5` |
| `--width` | Capture width | `1280` |
| `--height` | Capture height | `720` |
| `--fps` | Frames per second | `30` |

### 4. Live streaming (`camera_stream.py`)

Multi-format live streaming server. Supports MJPEG (low-latency), HLS (adaptive, mobile-friendly), and RTSP re-streaming.

```bash
uv run python scripts/camera_stream.py --port 8090
```

Open `http://<device-ip>:8090` in a browser to view the MJPEG stream.

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--device` | V4L2 device path | `/dev/video0` |
| `--rtsp` | RTSP input URL (use instead of `--device` for IP cameras) | — |
| `--port` | HTTP server port | `8090` |
| `--width` | Capture width | `640` |
| `--height` | Capture height | `480` |
| `--fps` | Target frames per second | `15` |
| `--enable-hls` | Enable HLS output (adaptive bitrate, mobile-friendly) | off |
| `--enable-rtsp` | Enable RTSP re-stream output | off |
| `--rtsp-port` | RTSP server port (when `--enable-rtsp` is used) | `8554` |

**Endpoints:**

| URL | Description |
|-----|-------------|
| `http://<ip>:8090/` | MJPEG stream (works in `<img>` tags and browsers) |
| `http://<ip>:8090/snap` | Single JPEG snapshot |
| `http://<ip>:8090/hls` | HLS live page (requires `--enable-hls`) |
| `http://<ip>:8090/hls/stream.m3u8` | HLS playlist for VLC or mobile players |
| `rtsp://<ip>:8554/live` | RTSP stream (requires `--enable-rtsp`) |
| `http://<ip>:8090/status` | JSON status (frame age, size, active outputs) |

## Examples

```bash
# List cameras
uv run python scripts/camera_list.py

# Snapshot from default webcam
uv run python scripts/camera_snap.py

# Snapshot from a specific camera
uv run python scripts/camera_snap.py --device /dev/video2 --output /tmp/photo.jpg

# Snapshot from an IP camera
uv run python scripts/camera_snap.py --rtsp rtsp://user:pass@192.168.1.100:554/stream1

# Record 10 seconds of video
uv run python scripts/camera_clip.py --duration 10

# MJPEG stream (low-latency, view in browser)
uv run python scripts/camera_stream.py --port 8090

# MJPEG + HLS stream (adaptive bitrate for mobile / remote)
uv run python scripts/camera_stream.py --port 8090 --enable-hls

# Full streaming: MJPEG + HLS + RTSP re-stream
uv run python scripts/camera_stream.py --port 8090 --enable-hls --enable-rtsp

# Stream from an IP camera as input
uv run python scripts/camera_stream.py --rtsp rtsp://user:pass@192.168.1.100:554/stream1 --enable-hls

# High-res stream at 30fps
uv run python scripts/camera_stream.py --width 1280 --height 720 --fps 30
```

## Multiple cameras

If you have multiple cameras (e.g. `/dev/video0` and `/dev/video2`), specify the device:

```bash
# List all cameras
uv run python scripts/camera_list.py

# Snap from camera 0
uv run python scripts/camera_snap.py --device /dev/video0 --output /tmp/cam0.jpg

# Snap from camera 2
uv run python scripts/camera_snap.py --device /dev/video2 --output /tmp/cam2.jpg

# Stream camera 0 on port 8090, camera 2 on port 8091
uv run python scripts/camera_stream.py --device /dev/video0 --port 8090
uv run python scripts/camera_stream.py --device /dev/video2 --port 8091
```

## Coordinate with robot arm

Combine with the [soarm-control](https://clawhub.ai/yuyoujiang/soarm-control) skill to look at something and take a photo:

```bash
# Move arm to look at the desktop
uv run python ~/.openclaw/workspace/skills/soarm-control/scripts/soarm_set_joints.py \
    --shoulder-pan 1.626 --shoulder-lift -42.110 --elbow-flex 32.088 \
    --wrist-flex 78.242 --wrist-roll -95.077

# Capture what the camera sees
uv run python scripts/camera_snap.py --output /tmp/desktop.jpg
```
