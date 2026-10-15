---
name: RTSP Snapshot
description: Capture JPG frames or short MP4 clips from RTSP/HTTP IP cameras via ffmpeg.
requires:
  bins: [ffmpeg]
  env: []
---

# RTSP Snapshot

Use to grab stills or short clips from IP security cameras (RTSP, HTTP
HLS) so Kate can report what is happening in a scene or store
evidence. All output stays under a sandbox dir (`RTSP_SNAPSHOT_OUTPUT_ROOT`,
default `$TMPDIR`).

## Use when

- "take a snapshot from the garage camera"
- "record 30s from the doorbell now"
- "is there motion? capture and send me a snapshot"

## Do not use when

- The camera is not reachable over LAN/public RTSP/HTTP URL
- Necesitas streaming continuo o WebRTC
- Clips > 5 minutes (hard cap by design)

## Tools

### `status`
ffmpeg bin + sandbox + limits.

### `snapshot { url, output_path, transport?, width? }`
- `url` — `rtsp://user:pass@host/stream`, `rtsps://`, `http://`, `https://` (NO `file://`, NO `concat:`)
- `output_path` — must stay under the sandbox root; `.jpg` recommended
- `transport` — `tcp` (default, estable sobre NAT) o `udp`
- `width` — resize manteniendo aspecto

Returns `{url, output_path, bytes, transport}`.

### `clip { url, output_path, duration_secs, transport? }`
- `duration_secs` 1..=300
- Uses stream copy (no re-encode) — very fast

Returns `{url, output_path, bytes, duration_secs, transport}`.

## Execution guidance

- Prefer TCP transport to avoid packet loss over Wi-Fi/VPN
- Credentials are inline in URL (`rtsp://user:pass@host/...`); store
  them in 1Password and read them with `read_secret` when reveal is enabled
- Output path outside sandbox → `-32034` IoError; adjust operator config
- Unreachable camera → `-32032` NonZeroExit with ffmpeg stderr included
- Motion detection is out of scope here — chain with a vision-enabled pipeline

## Pipelines

### Snapshot + vision

```
1. rtsp-snapshot.snapshot { url, output_path: "/sandbox/cam1.jpg" }
2. (futuro) vision-lm.describe { path: "/sandbox/cam1.jpg" }
```

### Clip + transcribe

```
1. rtsp-snapshot.clip { url, output_path: "/sandbox/ring.mp4", duration_secs: 30 }
2. video-frames.extract_audio { path, output_path: "/sandbox/ring.wav", codec:"wav", mono:true, sample_rate:16000 }
3. openai-whisper.transcribe_file { file_path: "/sandbox/ring.wav" }
```
