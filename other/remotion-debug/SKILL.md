---
name: remotion-debug
description: Debug Remotion video compositions, rendering pipeline, and the Python-to-React bridge in ettametta. Use when troubleshooting render failures, prop validation errors, composition issues, asset staging, or video output quality. Covers all 3 compositions (ViralClip, CinematicMinimal, HormoziStyle) and 14 components.
---
# Remotion Debugging

Skill for diagnosing Remotion render issues in ettametta — from React composition bugs to the Python rendering bridge.

## Quick Diagnostics

### Render a composition locally
```bash
cd apps/remotion-studio
npx remotion render src/index.ts ViralClip output.mp4 --props '{"title":"Test","video_url":"https://example.com/video.mp4"}'
```

### Open Remotion Studio (visual preview)
```bash
cd apps/remotion-studio
npx remotion studio
```

### Check render logs
```bash
# Renders are logged with [job_id] prefix via JobIdAdapter
docker compose logs -f api | grep "remotion"
```

### Test specific frame range
```bash
cd apps/remotion-studio
npx remotion render src/index.ts ViralClip output.mp4 --props '{}' --frame-range=0-100
```

## Architecture Reference

### Compositions (3 registered in Root.tsx)

| ID | Component | Resolution | Schema |
|----|-----------|------------|--------|
| `ViralClip` | `Composition.tsx` | 1080x1920 (9:16) | `viralClipSchema` (Zod) |
| `CinematicMinimal` | `templates/CinematicMinimal.tsx` | 1080x1920 | `cinematicMinimalSchema` |
| `HormoziStyle` | `templates/HormoziStyle.tsx` | 1080x1920 | `hormoziStyleSchema` |

### ViralClip Style Variants (driven by `style` prop)

| Style | Special Behavior |
|-------|-----------------|
| `REDDIT_STORY` | RedditHook overlay, no cinematic overlay/progress bar |
| `BROADCAST_NEWS` | NewsTicker overlay, no cinematic overlay |
| `ULTIMATE_TUTORIAL` | Tutorial mode |
| `HEARTFELT_NARRATIVE` | Warm color grade, serif captions, BPM 75 |
| `TOP_LISTICLE` | Electric color grade, slide transitions, BPM 128 |
| `CINEMATIC_DOC` | Letterbox, chromatic aberration=4, cycling blur/zoom/fade |

### Component Library (14 components)

| Component | Purpose |
|-----------|---------|
| `BrandReveal` | Glass-morphism logo/name reveal (first 2.5s) |
| `CTAOverlay` | Call-to-action with spring animation |
| `ChapterOverlay` | Top-left chapter title bar |
| `CinematicOverlay` | SVG chromatic aberration, film grain, vignette, letterbox |
| `ColorGrade` | SVG color matrix filters (6 types) |
| `KenBurns` | Pan/zoom effect with 4 directions |
| `MultiVideoLayout` | Multi-clip layout (single/split/grid) |
| `NewsTicker` | Scrolling ticker for BROADCAST_NEWS |
| `ProgressTracker` | Bottom progress bar with glow |
| `RedditHook` | Reddit-style post card overlay |
| `SceneTransition` | Entry/exit transitions (zoom/blur/slide/fade) |
| `VFXShader` | VHS glitch, blueprint, green tint, monochrome grain |
| `WordCaptions` | Kinetic word-by-word captions with emoji triggers |

### Python Rendering Bridge

**Core:** `src/services/video_engine/remotion_service.py` — `RemotionService` class

**Flow:**
1. Validate props (schema, memory size 50MB ceiling, duration_in_frames > 0)
2. Acquire semaphore slot (default: 2 concurrent renders)
3. Stage assets to isolated sandbox (`public/assets/{job_id}/`)
4. Write props JSON atomically (temp file + `os.replace()` + fsync)
5. Execute `npx remotion render` as async subprocess (900s timeout)
6. Verify output exists and is non-zero
7. Cleanup sandbox

**Error types:**
- `RemotionFatalError` — invalid props, bad schema (non-retryable)
- `RemotionTransientError` — timeout, process crash (retryable, 2 attempts)
- `RemotionError` — base class

**Key settings** (in `src/services/video_engine/settings.py`):
- `REMOTION_APP_DIR` = `{project_root}/apps/remotion-studio`
- `REMOTION_OUTPUT_DIR` = `{project_root}/outputs`
- `REMOTION_CONCURRENCY_LIMIT` = 2
- `REMOTION_TIMEOUT_SECONDS` = 900

## Common Issues & Fixes

### Render fails with "Composition not found"

The composition ID must match exactly what's registered in `Root.tsx`. Valid IDs: `ViralClip`, `CinematicMinimal`, `HormoziStyle`.

### Props validation fails

Common causes:
- `duration_in_frames` must be a positive integer
- Props JSON must be a dict (not a list)
- Total props memory size must be under 50MB
- `composition_id` must be a non-empty string

### Asset staging LFI rejection

The sandbox rejects paths outside 8 allowed roots. Files are copied with `O_NOFOLLOW` (no symlinks). If a file is rejected, check:
- Is it inside an allowed root directory?
- Is it a symlink? Copy the actual file instead.

### Render hangs or times out

Default timeout is 900s. Check:
- Is Chromium consuming memory? Dynamic V8 heap is 60% of cgroup limit (1024-8192 MB)
- Is the video URL accessible from the container?
- Are there too many concurrent renders? Semaphore limit is 2.

### Silent render failure (output is 0 bytes)

Post-render verification checks file existence and non-zero size. If 0 bytes:
- Check stderr output (streamed via async drain tasks)
- Check Chromium crash logs
- Try with `--scale=0.25` to reduce memory pressure

### Voice file 404 during render

Known bug: silent staging failure + path mangling + inconsistent types. Bypassed by running single-voiceover renders. See team memory `remotion-voice-file-404.md`.

### Beat sync is off

`framesPerBeat` is calculated from the `style` prop's BPM. `HEARTFELT_NARRATIVE` uses 75 BPM, `TOP_LISTICLE` uses 128 BPM. Default is 120 BPM. The global `scale()` transform pulses on every beat.

### WordCaptions showing wrong words

Words are synced to the `words` array in props (from transcription). Each word has `start`, `end`, `confidence`. 3 words are shown at a time. If timing is off, check the transcription output.

## Integration Points

| Caller | File | How it calls Remotion |
|--------|------|----------------------|
| API route | `src/api/routes/remotion.py` | `POST /remotion/render` → background task |
| VideoProcessor | `src/services/video_engine/processor.py` | `base_remotion_service.render_video()` with FFmpeg fallback |
| MotionGraphics | `src/services/video_engine/motion_graphics.py` | `base_remotion_service.render_video()` for title sequences |
| Agent Zero | `src/services/agent_zero/tools/remotion_render.py` | Direct `npx remotion render` subprocess |
| OpenClaw | `src/services/openclaw/skills/render_remotion.py` | CLI wrapper with GPU toggle |

## Style Variance (StochasticModulator)

`src/services/video_engine/stochastic_modulator.py` generates deterministic random parameters from a seed (job_id). Three presets: `AMBER_WARM`, `NEON_CYBER`, `MONOCHROME_DARK`. Parameters control: typography, slow_motion, vfx, auto_zoom, beat_sync, zoom_intensity, transition_duration_seconds.

## References

- [ViralClip Schema Reference](references/viralclip-schema.md)
- [Rendering Pipeline Details](references/rendering-pipeline.md)
