---
name: remotion-best-practices
description: Build programmatic videos with Remotion (React-based video framework). Covers compositions, animations, media, transitions, 3D, charts, captions, rendering, and Lambda deployment. Uses
  MCP server for real-time documentation lookup.
stacks:
  - remotion
packages:
  - remotion
  - "@remotion/renderer"
  - "@remotion/cli"
tags:
  - remotion
  - video
metadata:
  tags: remotion, video, react, animation, composition, rendering, lambda
---

## Use this skill when

- Creating videos programmatically with React and Remotion
- Building Remotion compositions, animations, and transitions
- Embedding media (video, audio, images, GIFs, Lottie) in compositions
- Creating charts, text animations, captions, and subtitles
- Rendering videos locally or on AWS Lambda
- Using Three.js/React Three Fiber inside Remotion
- Any task involving `remotion` or `@remotion/*` packages

## Do not use this skill when

- The task involves standard React without Remotion video output
- The user needs video editing of existing footage without programmatic generation

## Instructions

**Always use `mcp__remotion__remotion-documentation` for documentation lookups.** Query it with specific topics when you need API details, examples, or troubleshooting. Do not rely on memory for Remotion API signatures — always look up.

## Capabilities

### Project Structure
- Entry file (`src/index.ts`): calls registerRoot() with the Root component
- Root file (`src/Root.tsx`): registers one or more Composition components
- Component files: individual video components using Remotion hooks
- Defaults: fps=30, width=1920, height=1080

### Animation System
- ALL animations must be driven by `useCurrentFrame()` hook — no exceptions
- `interpolate(frame, inputRange, outputRange, options)` for linear mapping; always clamp with extrapolateRight/extrapolateLeft
- `spring({ frame, fps, config })` for natural physics-based motion
- Spring config presets: damping=200 (smooth), damping=20+stiffness=200 (snappy), damping=8 (bouncy), damping=15+stiffness=80+mass=2 (heavy)

### Forbidden Patterns
- CSS transitions and CSS animations — will NOT render correctly; Remotion renders frames out of order
- Tailwind `animate-*` and `transition-*` classes — same reason as CSS animations
- `Math.random()` — use `random('seed')` from remotion instead; random() is deterministic per seed
- Native `<img>` — use `<Img>` from remotion; native img may not wait for load
- `useFrame()` from @react-three/fiber inside Remotion — use `useCurrentFrame()` from remotion
- Third-party animation libraries (GSAP, Framer Motion, CSS keyframes) without disabling their animations

### Media Components
- Video and Audio: import from `@remotion/media`
- Images: import `<Img>` and `staticFile()` from `remotion`
- All assets: place in `public/` folder, reference with `staticFile('filename')`
- Video/Audio props: trimBefore, trimAfter (in frames), volume (0-1 or callback), playbackRate, loop, muted, toneFrequency

### Sequencing and Layout
- `<Sequence from={frame} durationInFrames={frames}>`: delays appearance; premountFor is important
- **Always premount Sequences**: use `premountFor={1 * fps}` to prevent pop-in artifacts
- `<Series>`: chains elements back-to-back without overlap
- `<AbsoluteFill>`: layers elements filling the full composition
- `<TransitionSeries>`: sequences with overlap transitions between scenes

### Transitions
- Install: `npx remotion add @remotion/transitions`
- Available: fade, slide, wipe, flip, clockWipe, iris, and custom presentations
- Timing: linearTiming or springTiming
- Transitions shorten total duration (overlap); use Overlay for non-shortening transitions
- `<TransitionSeries.Transition presentation={fade()} timing={linearTiming({ durationInFrames: 15 })} />`

### Fonts
- Google Fonts: `import { loadFont } from '@remotion/google-fonts/FontName'`; call loadFont() at module level
- Local fonts: `import { loadFont } from '@remotion/fonts'`; await loadFont() in calculateMetadata or root

### Parameterizable Videos
- Define Zod schema for video props
- Use `zColor()` from `@remotion/zod-types` for color inputs
- Pass schema to Composition; enables Remotion Studio GUI editing and type-safe renders

### Dynamic Metadata
- `calculateMetadata` function on Composition for dynamic duration, dimensions, or props
- Use for: fetching data from APIs, computing duration from audio/video length, data-driven props
- Returns: `{ durationInFrames, fps, width, height, props }`

### 3D Content
- Install: `npx remotion add @remotion/three`
- `<ThreeCanvas width={width} height={height}>`: wrapper for React Three Fiber scene
- Use `useCurrentFrame()` for all 3D animations — not useFrame() from @react-three/fiber
- `<Sequence>` inside `<ThreeCanvas>` must have `layout="none"`

### Charts and Data Visualization
- Use SVG or HTML/CSS for charts; drive all animations with useCurrentFrame()
- Disable any third-party animation library's built-in animations
- Path drawing animation: use `evolvePath(progress, pathD)` from `@remotion/paths`
- Bar charts: interpolate bar heights from 0 to final value using spring or interpolate

### Captions and Subtitles
- `@remotion/captions`: parse SRT/VTT, render word-by-word or line-by-line
- Sync captions to audio timing using frame-based calculations

### Rendering (Local)
- `npx remotion render CompositionId` — renders video
- `npx remotion still CompositionId` — renders single frame as image
- Transparent video: ProRes with yuva444p10le pixel format and prores-profile=4444
- Transparent WebM: VP9 codec with yuva420p pixel format

### Lambda Rendering
- Setup: deploy function and site with Lambda CLI commands
- Programmatic: `deployFunction()`, `deploySite()`, `renderMediaOnLambda()`, `getRenderProgress()`
- Always call `getRenderProgress()` in a loop until done — Lambda renders are async

## Behavioral Traits
- Always queries `mcp__remotion__remotion-documentation` before writing any Remotion API calls
- Uses `useCurrentFrame()` for every animation — never CSS transitions or third-party animation libs
- Always sets `extrapolateRight: 'clamp'` and `extrapolateLeft: 'clamp'` on interpolate calls
- Adds `premountFor={1 * fps}` to every Sequence to prevent visual pop-in
- Places all assets in public/ and references with staticFile()
- Uses `<Img>` from remotion, never native `<img>`
- Chooses spring for natural motion, interpolate for precise linear mapping

## Knowledge Base

### Frame Math
- Convert seconds to frames: `seconds * fps` (e.g., 2 seconds at 30fps = 60 frames)
- Convert frames to seconds: `frames / fps`
- Composition total duration in frames: `durationInSeconds * fps`
- Audio/video trimming: trimBefore and trimAfter are in frames

### Spring vs Interpolate Decision
- Spring: when the motion should feel physical and natural (elements entering/exiting)
- Interpolate: when precise timing and values are required (progress bars, percentage readouts)
- Combine: use spring for entry, interpolate for hold/exit

### Common Mistakes
- Forgetting premountFor on Sequence: causes flash/pop-in at sequence start
- Using Math.random(): produces different frames on each render pass; use random('seed') instead
- Native img tag: may not finish loading before frame is captured; always use Img from remotion
- CSS animations: Remotion renders frames out of order; CSS animations assume sequential time
- Missing clamp on interpolate: values extrapolate beyond intended range causing visual artifacts

### Render Quality Settings
- Default: H.264 MP4, yuv420p — good for web playback
- High quality: ProRes 4444 with transparency support — good for compositing
- Lossless: PNG image sequence — maximum quality for post-processing
- Lambda: parallelizes rendering across Lambda functions; much faster for long videos

## Constraints
- NEVER use Math.random() — always use random('seed') from remotion
- NEVER use CSS transitions, CSS animations, or Tailwind animate-*/transition-* classes
- NEVER use native `<img>` — always use `<Img>` from remotion
- ALWAYS drive animations with useCurrentFrame()
- ALWAYS clamp interpolate extrapolation
- ALWAYS premount Sequences with premountFor
- ALWAYS query mcp__remotion__remotion-documentation for API details before implementing

## API Reference

Detailed API documentation: [references/REFERENCE.md](references/REFERENCE.md).

**When to read**: when you need exact method signatures, configuration options, type definitions, or implementation details not covered above.

**How to use**: search or read the reference for specific APIs before writing code. Don't read the entire file — look up only what you need.
