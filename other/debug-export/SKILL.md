---
name: debug-export
description: Troubleshoot video export failures including codec issues, layer rendering problems, audio sync errors, and browser compatibility.
---

# Debug Export

Diagnose and fix video export failures in ProAnimate, covering codec compatibility, layer rendering pipeline issues, audio mixing errors, and browser-specific problems.

## Purpose

Video export involves rendering hundreds of frames via Canvas2D or PixiJS, encoding them with WebCodecs or MediaRecorder, and muxing with audio. Many things can go wrong at each stage. This skill helps systematically identify and fix export issues.

## Steps

1. **Check the export progress status**:
   - `idle` -- export not started.
   - `preparing` -- loading assets (images, Lottie, Three.js, templates). If stuck here, an asset failed to load.
   - `rendering` -- frame-by-frame rendering. If stuck, a specific layer is hanging.
   - `encoding` -- flushing the encoder. If stuck, the encoder is backpressured or errored.
   - `complete` -- export finished. Check `outputUrl` and `outputSize`.
   - `error` -- fatal failure. Check `progress.error`.

2. **Diagnose asset loading failures** (stuck in `preparing`):
   - `preloadImages()` loads all character sprites, media URLs, and background images. CORS errors cause failures -- check console for `Access-Control-Allow-Origin` errors.
   - `preloadLottieAnimations()` initializes Lottie instances. Invalid JSON or missing lottie-web causes failures.
   - `preloadThreeScene()` creates a headless Three.js renderer for 3D characters. WebGL context creation can fail if too many contexts exist.
   - `preloadHTMLTemplates()` creates offscreen iframes for HTML templates. CSP violations or template errors cause failures.
   - `preloadRiggedCharacters()` loads rigged character mesh data and bone animations.

3. **Diagnose frame rendering failures** (black frames, wrong content):
   - **Black frames**: The Canvas2D renderer (`renderFrame()`) draws layers in order: background fill, Lottie, media, shapes, video, characters, text, overlay Lottie, captions. If a layer throws, subsequent layers may not render.
   - **Missing characters**: Check that `imageCache` contains the sprite URLs. Character rendering uses `drawImage()` with the cached `HTMLImageElement`.
   - **Wrong viseme/emotion**: The renderer looks up viseme and emotion at the current frame from `visemeTimeline` and `emotionTimeline`. Verify these timelines have correct frame ranges.
   - **Missing text overlays**: Text rendering uses `ctx.fillText()`. Check font loading -- custom fonts must be loaded before rendering starts.
   - **Missing templates**: HTML template layer renders from iframe screenshots. If the iframe did not load in time, the frame is blank.
   - **Scale issues**: When export resolution differs from canvas resolution, `scaleX/scaleY` is applied. Check `needsScale` computation.

4. **Diagnose GPU renderer failures** (PixiJS path):
   - If `isWebGL2Supported()` returns true, the export tries the PixiJS renderer.
   - If PixiJS init fails (e.g., WebGL context lost), it falls back to Canvas2D with a console warning.
   - Check: `[videoExport] GPU renderer init failed, falling back to Canvas2D`.
   - Force Canvas2D by disabling GPU: set `isWebGL2Supported` to return false.

5. **Diagnose codec / encoder errors**:
   - **WebCodecs path**: `VideoEncoder.configure()` can fail with unsupported codec. H.264 (`avc1.640028`) requires Chrome 94+. VP8 (`vp8`) is more broadly supported.
   - **Encoder error callback**: Check for `[videoExport] Video encoder error:` in console. Common: encoder closed unexpectedly (usually from memory pressure).
   - **Backpressure**: If `encodeQueueSize > 8`, the export waits. If this persists, the encoder is too slow for the frame rate.
   - **MediaRecorder path**: Falls back when WebCodecs unavailable (Firefox). Uses `canvas.captureStream(0)` with manual frame requests. VP8 preferred over VP9 for quality.

6. **Diagnose audio issues**:
   - **No audio**: `collectAudioSources()` returned empty. Check `props.audioUrl` and `props.dialogueCharacters`.
   - **Audio mixing failed**: `mixTracks()` threw. Check console for `[videoExport] Audio mixing failed:`. Common cause: invalid audio URL (404 or CORS).
   - **Audio out of sync**: In MediaRecorder path, audio plays in real-time via `AudioBufferSourceNode` but frames render at variable speed. WebCodecs path does not have this issue since audio is encoded separately.
   - **Audio encoding failed**: `AudioEncoder` error. AAC (`mp4a.40.2`) for MP4, Opus for WebM. Check browser support.

7. **Diagnose memory issues**:
   - Large exports (4K, long duration) can exhaust browser memory.
   - `VideoFrame` objects must be `close()`d after encoding. A leak here causes rapid memory growth.
   - Three.js resources must be disposed via `disposeThreeScene()`.
   - HTML template iframes must be removed via `disposeHTMLTemplates()`.

## Key Files

| Purpose | Path |
|---------|------|
| Main export function | `src/services/videoExport.ts` |
| Canvas2D frame renderer | `src/services/canvas2dRenderer.ts` |
| PixiJS GPU renderer | `src/services/pixiExportRenderer.ts` |
| Audio mixer | `src/services/audioMixer.ts` |
| GIF export | `src/services/gifExport.ts` |
| Transparent export | `src/services/transparentExport.ts` |
| Remotion composition | `src/remotion/VideoComposition.tsx` |
| Composition builder | `src/services/compositionBuilder.ts` |
| Export panel UI | `src/components/panels/ExportPanel.tsx` |

## Common Issues

- **"Encoder was closed unexpectedly"**: Memory pressure caused the browser to close the VideoEncoder. Reduce resolution or export fewer frames.
- **Export produces 0-byte file**: The muxer was finalized without any video chunks. Check that the encoder received at least one frame.
- **Black frames on first few frames**: Asset preloading did not complete before rendering started. This should not happen since preloading is awaited, but check for race conditions.
- **"Export cancelled (AbortError)"**: User cancelled or the `AbortSignal` was triggered. Expected behavior.
- **Firefox exports as WebM when MP4 requested**: Firefox does not support WebCodecs. `resolveMediaRecorderMime()` falls back to WebM. Check `ExportResult.didFallback === true`.
- **GIF file too large**: Reduce quality: increase `frameSkip` to 3, lower `maxWidth` to 320, disable `dithering`.
- **Canvas tainted**: An image loaded without CORS was drawn to the canvas, making `getImageData()` fail. Ensure all image URLs have proper CORS headers.

## Examples

Check WebCodecs support:
```ts
import { isWebCodecsSupported, isMp4Supported } from '@/services/videoExport'
console.log('WebCodecs:', isWebCodecsSupported())
console.log('MP4:', isMp4Supported())
```

Force Canvas2D renderer (bypass GPU):
```ts
// In pixiExportRenderer.ts, temporarily return false:
export function isWebGL2Supported(): boolean { return false }
```
