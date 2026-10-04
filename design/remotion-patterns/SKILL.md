---
name: remotion-patterns
description: ProAnimate's custom Remotion-compatible engine API, layer component patterns, and composition architecture. Auto-applied when creating or modifying Remotion layers or the video export pipeline.
user-invocable: false
---

# ProAnimate Engine — Remotion-Compatible API

ProAnimate reimplements Remotion's core API in a custom engine. The actual `remotion` npm package is NOT installed. All imports come from `@/engine/` not `remotion`.

## API Mapping

| Remotion API | ProAnimate Equivalent | Import From |
|---|---|---|
| `useFrame()` | `useFrame()` | `@/engine/CompositionContext` |
| `useVideoConfig()` | `useComposition()` | `@/engine/CompositionContext` |
| `AbsoluteFill` | `Fill` | `@/engine/primitives` |
| `Sequence` | `Clip` | `@/engine/primitives` |
| `Audio` | `AudioTrack` | `@/engine/primitives` |
| `OffthreadVideo` | `VideoTrack` | `@/engine/primitives` |
| `Player` | `CompositionPlayer` | `@/engine/CompositionPlayer` |
| `interpolate()` | `interpolate()` | `@/engine/interpolate` |
| `spring()` | `spring()` | `@/engine/spring` |
| `measureSpring()` | `measureSpring()` | `@/engine/spring` |

**NEVER import from `remotion`. Always import from `@/engine/`.**

## Primitives

### `Fill` — Full-viewport cover (replaces `AbsoluteFill`)
```tsx
<Fill style={{ background: '#000' }}>
  {children}
</Fill>
```
Renders `<div>` with `position: absolute; inset: 0`.

### `Clip` — Frame-range visibility (replaces `Sequence`)
```tsx
<Clip from={30} durationInFrames={60}>
  {/* Only visible from frame 30 to 89 */}
</Clip>
```
Returns `null` if current frame is outside `[from, from + durationInFrames)`.

### `AudioTrack` — Synced audio playback
```tsx
<AudioTrack src={audioUrl} volume={0.8} />
```
Frame-syncs via `HTMLAudioElement.currentTime`. Drift threshold: 0.5 frames.

### `VideoTrack` — Synced video playback
```tsx
<VideoTrack src={videoUrl} style={{ width: '100%' }} muted={false} />
```

## Animation Functions

### `interpolate(value, inputRange, outputRange, options?)`
Multi-stop linear interpolation with optional easing.
```tsx
const opacity = interpolate(frame, [0, 30], [0, 1])
const x = interpolate(frame, [0, 30, 60], [0, 100, 0], { easing: easeInOut })
```
Options: `easing`, `extrapolateLeft: 'clamp' | 'extend'`, `extrapolateRight: 'clamp' | 'extend'`.

### `spring({ frame, fps, config?, from?, to?, durationInFrames? })`
Damped spring physics via RK4 integration. Results are cached per config.
```tsx
const scale = spring({ frame, fps: 30, config: { stiffness: 100, damping: 10 }, from: 0, to: 1 })
```
Config defaults: `damping: 10, mass: 1, stiffness: 100, overshootClamping: false`.

### `measureSpring(config?, options?)`
Returns frame count until spring settles (within threshold for 3 consecutive frames).
```tsx
const dur = measureSpring({ stiffness: 100 }, { fps: 30, threshold: 0.001 })
```

## Layer Component Pattern

All layer components in `src/remotion/` follow this structure:

```tsx
import { useFrame } from '@/engine/CompositionContext'
import { interpolate } from '@/engine/interpolate'

interface RemotionXXXLayerProps {
  items: XXXItem[]
  canvasWidth: number
  canvasHeight: number
  keyframeData?: KeyframeData
}

export function RemotionXXXLayer({ items, canvasWidth, canvasHeight, keyframeData }: RemotionXXXLayerProps) {
  const frame = useFrame()

  if (items.length === 0) return null

  return (
    <>
      {items.map(item => {
        // Frame-based transforms using interpolate/spring
        const opacity = interpolate(frame, [item.startFrame, item.startFrame + 10], [0, 1])

        return (
          <div key={item.id} style={{
            position: 'absolute',
            left: `${(item.x / canvasWidth) * 100}%`,
            top: `${(item.y / canvasHeight) * 100}%`,
            opacity,
          }}>
            {/* Render item content */}
          </div>
        )
      })}
    </>
  )
}
```

**Key rules:**
1. Always call `useFrame()` for frame-indexed rendering
2. Always check `items.length === 0` and return `null` early
3. Position using percentage-based layout relative to `canvasWidth`/`canvasHeight`
4. Use `interpolate()` or `spring()` for all animations — never CSS transitions
5. Accept `keyframeData` prop for shared transform synchronization

## Composition Architecture

`VideoComposition.tsx` is the master renderer. Layer stacking order (bottom to top):

```
Fill (background)
  └─ CameraTransformWrapper
       ├─ StyleEffectFilters (SVG defs: woodcut, cel-shade, neon, glitch, VHS)
       ├─ StyleFilter (CSS global filters)
       ├─ Background Lottie (zIndex < 0)
       ├─ RemotionVideoLayer
       ├─ RemotionMediaLayer (images)
       ├─ RemotionHTMLTemplateLayer
       ├─ RemotionShapeLayer
       ├─ RemotionArtCurveLayer
       ├─ RemotionCrowdLayer
       ├─ RemotionSVGObjectLayer
       ├─ Characters (Dialogue or Single mode)
       │   ├─ CharacterStyleEffectWrapper
       │   │   └─ RemotionCharacter (4-layer sprite composite)
       │   └─ AudioTrack via Clip (per dialogue line)
       ├─ RemotionRiggedCharacter
       ├─ RemotionPixelArtCharacter
       ├─ RemotionAvatarCharacter
       ├─ Remotion3DLayer (Three.js scene)
       ├─ RemotionTextOverlay
       ├─ RemotionAnnotationLayer
       ├─ RemotionParticleLayer
       ├─ RemotionAudioReactiveLayer
       ├─ Overlay Lottie (zIndex >= 0)
       └─ Background Audio (Clip + AudioTrack)
  ├─ RemotionCaptions (outside camera, fixed position)
  ├─ RemotionRetentionHookLayer
  └─ RemotionTransitionLayer
```

## Adding a New Layer

1. Create `src/remotion/RemotionXXXLayer.tsx` following the pattern above
2. Add types to `src/types/xxx.ts`
3. Add store at `src/stores/useXXXStore.ts` (Zustand + Immer)
4. Import and render in `VideoComposition.tsx` at the correct z-order position
5. Add prop to `VideoCompositionProps` interface
6. Pass data from store in the parent that mounts `CompositionPlayer`

## Dialogue Mode

Two rendering modes for characters:

**Sprite mode:** Direct `RemotionCharacter` — 4-layer composite (body, head, viseme mouth, hair)
**Rigged mode:** `RemotionRiggedCharacter` (Canvas2D mesh body) + `RemotionCharacter` overlay (sprite head/viseme/hair) with CSS scale from `boundsWidth / rigExportData.imageWidth`

Audio tracks per dialogue line:
```tsx
<Clip from={line.startFrame} durationInFrames={line.endFrame - line.startFrame}>
  <AudioTrack src={line.audioUrl} volume={1} />
</Clip>
```

Viseme/emotion events are offset: `event.startFrame + line.startFrame`

## Video Export Pipeline

Export uses WebCodecs + mp4-muxer/webm-muxer directly (NOT Remotion's rendering). See `src/services/videoExport.ts`. The composition is rendered frame-by-frame to an offscreen canvas.
