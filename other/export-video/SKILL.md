---
name: export-video
description: Export video in multiple formats including MP4, WebM, GIF, transparent video, SCORM, and interactive HTML. Covers codec selection and layer composition.
argument-hint: <format>
---

# Export Video

Export a ProAnimate composition to a video file. Supports MP4 (H.264), WebM (VP8), GIF, transparent video (VP9 alpha / PNG sequence), SCORM packages, and interactive HTML bundles.

## Purpose

Render all composition layers frame-by-frame to an offscreen canvas, encode the frames using browser codecs, mix multi-track audio (dialogue + music with auto-ducking), and produce a downloadable file.

## Steps

1. **Choose the export format** based on target use case:
   - `mp4` -- H.264 via WebCodecs + mp4-muxer. Best compatibility. Requires Chrome 94+ or Safari 16.4+.
   - `webm` -- VP8 via WebCodecs + webm-muxer. Fallback on Firefox via MediaRecorder.
   - `gif` -- Animated GIF via gifenc. Supports frame-skip, max-width cap, and dithering.
   - `webm-alpha` -- VP9 WebM with alpha channel for transparent video overlays.
   - `png-sequence` -- PNG image sequence bundled into a ZIP (universal).
   - SCORM -- LMS-compatible package with imsmanifest.xml and video player.
   - Interactive HTML -- Standalone HTML bundle with click/hover triggers and scroll-driven animation.

2. **Configure export options** via `ExportOptions`:
   - `width`, `height` -- output resolution (can differ from canvas resolution; scaling is automatic).
   - `fps` -- frames per second (typically 30).
   - `durationInFrames` -- total frames to render.
   - `quality` -- 0.0 to 1.0, controls bitrate multiplier (MP4: 0.15x, WebM: 0.12x).
   - `startFrame` -- for partial exports.
   - `gifSettings` -- `frameSkip` (1/2/3), `maxWidth`, `dithering`, `loop`.

3. **Understand the rendering pipeline**:
   - Asset preloading: images, Lottie animations, video elements, Three.js scenes, HTML templates, rigged characters, motion graphics -- all loaded in parallel.
   - Keyframe index is pre-built for O(1) property lookup per frame.
   - Each frame is drawn to an offscreen `<canvas>` using the Canvas2D renderer.
   - Optional GPU path: if WebGL2 is available, PixiJS renderer is used instead.
   - Layer draw order: background fill, background Lottie, media images, shapes, video layers, characters, text overlays, overlay Lottie, captions.

4. **Understand audio mixing**:
   - `collectAudioSources()` gathers dialogue audio (single or multi-character) and background music.
   - `mixTracks()` from `audioMixer.ts` mixes all tracks with per-track volume and auto-ducking of music under dialogue.
   - Audio is encoded directly into the muxer via WebCodecs AudioEncoder (AAC for MP4, Opus for WebM).

5. **Understand encoding paths**:
   - **WebCodecs path** (Chrome/Safari): hardware-accelerated, non-realtime. VideoFrames submitted as fast as they render. Backpressure handled via `encodeQueueSize`. Keyframes every 2 seconds.
   - **MediaRecorder fallback** (Firefox): captures from canvas stream. Audio mixed via AudioContext and added to stream. Real-time encoding.
   - **GIF path**: gifenc with per-frame 256-color palette quantization. Uses `prequantize` for better dithering.

6. **Handle transparent export** (if needed):
   - VP9 WebM alpha: `canvas.clearRect()` before each frame, `renderFrame()` with `{ alpha: true }`, codec `vp09.00.10.08` with `alpha: 'keep'`.
   - PNG sequence: renders each frame to PNG, bundles into ZIP.
   - Safari does not support VP9 encoding -- falls back to PNG sequence.

7. **Handle specialized exports** (if needed):
   - SCORM: packages video with `imsmanifest.xml`, `scormAPI.js`, and launcher HTML. Reports completion to LMS. Supports SCORM 1.2 and 2004.
   - Interactive HTML: converts composition to `InteractiveManifest` with scenes, layers, and keyframes. Bundles a lightweight player runtime supporting click/hover triggers and scroll-driven animation.

## Key Files

| Purpose | Path |
|---------|------|
| Main export orchestrator | `src/services/videoExport.ts` |
| Canvas2D frame renderer | `src/services/canvas2dRenderer.ts` |
| PixiJS GPU renderer | `src/services/pixiExportRenderer.ts` |
| Multi-track audio mixer | `src/services/audioMixer.ts` |
| GIF encoder | `src/services/gifExport.ts` |
| Transparent export | `src/services/transparentExport.ts` |
| SCORM exporter | `src/services/scormExporter.ts` |
| Interactive exporter | `src/services/interactiveExporter.ts` |
| Composition engine | `src/services/compositionEngine.ts` |
| Auto-reframe service | `src/services/autoReframe.ts` |
| Remotion composition | `src/remotion/VideoComposition.tsx` |
| Export panel UI | `src/components/panels/ExportPanel.tsx` |
| Multi-export panel | `src/components/panels/MultiExportPanel.tsx` |

## Common Issues

- **Black frames**: Canvas2D renderer failed to draw a layer. Check that all image URLs in `preloadImages()` are valid. Look for CORS errors in the console.
- **No audio in export**: `collectAudioSources()` returned empty. Verify `props.audioUrl` or `props.dialogueCharacters[].dialogueLines[].audioUrl` are populated.
- **MP4 not supported**: On Firefox, WebCodecs is unavailable. The system auto-falls back to WebM via MediaRecorder. Check `ExportResult.didFallback`.
- **Export OOM (out of memory)**: Large resolutions (4K+) with many layers can exhaust memory. Reduce resolution or use `startFrame` for partial exports.
- **GIF too large**: Increase `frameSkip` (2 or 3), reduce `maxWidth` (480 or 320), disable `dithering`.
- **Transparent export fails on Safari**: VP9 encoding is not supported. The system falls back to PNG sequence.
- **Audio out of sync (MediaRecorder)**: The MediaRecorder path is real-time -- frame rendering delays accumulate. WebCodecs path does not have this issue.

## Examples

Export as MP4 at 1080p:
```ts
import { exportVideo } from '@/services/videoExport'
const result = await exportVideo(compositionProps, {
  width: 1920, height: 1080, fps: 30,
  durationInFrames: 900, format: 'mp4', quality: 0.8,
}, (progress) => console.log(progress.percentage))
```

Export as GIF with frame skip:
```ts
const result = await exportVideo(compositionProps, {
  width: 480, height: 854, fps: 30,
  durationInFrames: 300, format: 'gif', quality: 0.7,
  gifSettings: { frameSkip: 2, maxWidth: 480, dithering: false, loop: true },
}, onProgress)
```

Batch export for multiple aspect ratios:
```ts
import { exportBatch } from '@/services/videoExport'
const blobs = await exportBatch(compositions, options, (p) => console.log(p))
```
