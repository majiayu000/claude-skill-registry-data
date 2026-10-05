---
name: video-pipeline
description: Debug and troubleshoot ettametta's end-to-end video generation pipeline. Use when investigating render failures, asset staging issues, FFmpeg errors, MoviePy hangs, Remotion crashes, or storage problems.
---

# Video Pipeline Debugging

## Pipeline Overview

Four paths converge on shared rendering/storage:

- **Path A: Download & Transform** — yt-dlp -> VLM analysis -> Whisper transcribe -> AI strategy -> Remotion/FFmpeg render -> store
- **Path B: AI Video Synthesis** — Text prompt -> GenerativeService (GPU/cloud/Lite4K) -> store
- **Path C: Nexus Orchestrator** — Multi-clip assembly -> Dify vibe analysis -> Vision audit -> FFmpeg concat -> Remotion render -> store
- **Path D: Blueprint/DAG** — Node graph (ingress -> cognition -> synthesis -> egress) -> parallel/sequential execution

## Quick Diagnostics

```bash
curl http://localhost:8000/api/v1/video/jobs/{job_id}
docker compose exec api which ffmpeg
docker compose exec api ffmpeg -encoders 2>/dev/null | grep -E 'nvenc|qsv|libx264'
ls -la data/storage/outputs/ | head -20
```

## Key Files

| File | Purpose |
|---|---|
| src/services/video_engine/tasks.py | Celery tasks: download_and_process, generate_video, generate_story, narrative_fusion |
| src/services/video_engine/processor.py | VideoProcessor — MoviePy + OpenCV, Ken Burns, speed ramping |
| src/services/video_engine/remotion_service.py | RemotionService — Python-to-Remotion bridge, asset staging, circuit breaker |
| src/services/video_engine/downloader.py | VideoDownloader — yt-dlp with cookie injection |
| src/services/video_engine/synthesis_service.py | GenerativeService — T2V (GPU, cloud, Lite4K) |
| src/services/video_engine/ffmpeg_utils.py | FFmpegTransformer |
| src/services/video_engine/ffmpeg_optimizer.py | FFmpegGraphOptimizer — single filter_complex |
| src/services/video_engine/transcription.py | Fast-Whisper transcription |
| src/services/video_engine/quality_control.py | QualityControl (STUB — returns hardcoded 9.2) |
| src/services/nexus_engine/orchestrator.py | NexusOrchestrator — multi-scene assembly |
| src/services/nexus_engine/blueprints.py | Blueprint registry, DAG execution |
| src/services/storage/service.py | Storage provider (LOCAL / S3) |
| apps/remotion-studio/src/Composition.tsx | ViralClip composition (main render target) |

## Common Issues & Fixes

### MoviePy hangs on video load
Can hang on ARM64. Timeout -> OpenCV probe -> retry -> crash. OpenCV fallback incomplete.

### Remotion Chromium OOM
Protected by circuit breaker (2 failures -> 300s recovery) and concurrency semaphore. Dynamic V8 memory: 60% of cgroup limit (1024-8192MB).
```bash
docker compose exec api env | grep REMOTION_TIMEOUT
```

### FFmpeg missing
Pipeline degrades significantly. Check: `docker compose exec api which ffmpeg`

### Font resolution failure
MoviePy TextClip crashes without system fonts. Check: `docker compose exec api fc-list`

### yt-dlp download failures
Two attempts: explicit format, then auto-select. No Pexels fallback at downloader level.

### Asset staging LFI protection
Remotion validates paths with O_NOFOLLOW. Assets must be in allowed_roots.

### Props JSON too large (>10MB)
Large clip arrays can hit the 10MB cap.

### GPU queue blocks (Redis down)
GpuQueueManager uses Redis BLPOP. If Redis is down, all GPU synthesis blocks.

### QualityControl is a stub
`quality_control.py` line 37: sleeps 1s, returns hardcoded 9.2. Vision analysis not implemented.

## FFmpeg Encoder Selection

| Hardware | Encoder | Quality | Fast |
|---|---|---|---|
| NVIDIA | h264_nvenc | p4, CQ 19 | p4, CQ 28 |
| Intel QSV | h264_qsv | veryslow, GQ 18 | veryfast, GQ 28 |
| CPU | libx264 | superfast, CRF 23 | ultrafast, CRF 28 |

## Stock Fallback Chain

Pexels API -> Coverr API -> hardcoded CDN URLs -> `templates/safety/generic_space.mp4`

## Debugging Checklist

1. FFmpeg installed? `which ffmpeg`
2. Remotion available? `npx remotion --version`
3. Disk space? `df -h data/storage/`
4. Assets staged? `ls -la apps/remotion-studio/public/assets/`
5. Celery logs: `docker compose logs --tail=100 celery_worker`
6. OOM? `dmesg | grep -i "out of memory"`
7. Redis GPU queue: `redis-cli llen ettametta:gpu:slots`
