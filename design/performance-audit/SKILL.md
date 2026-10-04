---
name: performance-audit
description: Profile and optimize ProAnimate's canvas frame rates, export times, memory usage, and store subscription overhead. Use when adding new layers, stores, or heavy computations.
user-invocable: true
argument-hint: [component or area to profile]
---

# Performance Audit

## When to Use

- Before adding a new canvas layer type (particles, crowd, audio-reactive)
- After modifying the animation engine (interpolate, spring, CompositionPlayer)
- When users report slow preview playback or long export times
- When adding new Zustand stores that canvas layers subscribe to
- Before any release

## Frame Budget

Target: **60fps preview, 30fps minimum acceptable**

| Budget | Time per frame | What fits |
|--------|---------------|-----------|
| 60fps | 16.6ms | Canvas render + all layer compositing |
| 30fps | 33.3ms | Degraded but usable |
| <30fps | >33.3ms | Unacceptable — find the bottleneck |

## Profiling Steps

### 1. Canvas Frame Rate
```tsx
// Add to CompositionPlayer.tsx tick loop temporarily
const start = performance.now()
// ... render frame ...
const elapsed = performance.now() - start
if (elapsed > 16.6) console.warn(`Frame budget exceeded: ${elapsed.toFixed(1)}ms`)
```

### 2. Store Subscription Audit
134 Zustand stores exist. Check which ones cause canvas re-renders:
```bash
grep -r "useFrame\|usePlaybackStore\|useCanvasStore" src/remotion/ src/components/canvas/ --include="*.tsx" -l
```
Every store subscription in a canvas component re-renders at playback fps. Minimize subscriptions using selectors:
```tsx
// BAD: subscribes to entire store, re-renders on any change
const store = useCanvasStore()

// GOOD: subscribes only to what's needed
const zoom = useCanvasStore(s => s.zoom)
```

### 3. Memory Profiling
Watch for leaks in:
- **Three.js**: geometries, materials, textures not disposed on scene change
- **PixiJS**: GPU textures not destroyed
- **Audio buffers**: ElevenLabs TTS blobs held after dialogue changes
- **Lottie**: animation instances not stopped/destroyed
- **Stores**: 134 stores loaded eagerly — check which ones hold large data

```tsx
// Check memory in DevTools Console
performance.measureUserAgentSpecificMemory().then(r => console.log(r))
```

### 4. Export Performance
The export pipeline renders frame-by-frame to offscreen canvas via WebCodecs + mp4-muxer.
- Profile: `console.time('frame-N')` around each frame render in videoExport.ts
- Bottlenecks: Three.js scene render, PixiJS canvas capture, SVG filter application
- Target: export should not exceed 3x realtime (30s video exports in <90s)

## Red Flags

- Any `useEffect` without cleanup in canvas/remotion components
- Any `setInterval` or `requestAnimationFrame` without cancellation
- Stores with `subscribe()` calls that never unsubscribe
- Large arrays (viseme timelines, keyframe data) copied on every frame
- CSS `filter` or `backdrop-filter` on elements that re-render at fps
