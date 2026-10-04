---
name: remotion-video
description: Generate videos programmatically using Remotion (React-based video framework). Use this skill whenever the user wants to create, render, or animate videos with code — including explainer videos, social media clips, data visualizations, motion graphics, title sequences, product demos, or any video content. Also trigger when the user mentions "remotion", "programmatic video", "video from code", "render video", "generate video", "animated video", "motion graphics", "video template", or wants to turn data/text/images into video. Even if they just say "make a video" or "create a clip", use this skill — Remotion is the tool for code-driven video generation.
---

# Remotion Video Generation

You are building videos with [Remotion](https://www.remotion.dev/) — a React framework where videos are React components rendered frame-by-frame. Every frame is a function of the frame number and props, giving you full programmatic control.

## Mental Model

A Remotion video is just a React component that receives a frame number. You render whatever you want for each frame using standard React + CSS. The framework captures each frame as an image and stitches them into a video file.

The four numbers that define every video:
- **width** / **height** — pixel dimensions
- **fps** — frames per second (typically 30)
- **durationInFrames** — total frame count (`seconds × fps`)

## Project Setup

### New Project
```bash
npx create-video@latest
```
This scaffolds a working project. Choose a template (blank, helloworld, TailwindCSS, etc.).

### Add to Existing Project
```bash
npm i remotion @remotion/cli react react-dom
```

### Minimum Project Structure
```
my-video/
  public/              # Static assets (images, fonts, audio, video files)
  src/
    index.ts           # Entry point — calls registerRoot()
    Root.tsx            # Registers all compositions via <Composition>
    MyVideo.tsx         # Your video component(s)
  remotion.config.ts   # Optional CLI configuration
  package.json
```

**Entry point** (`src/index.ts`):
```tsx
import {registerRoot} from 'remotion';
import {RemotionRoot} from './Root';
registerRoot(RemotionRoot);
```

**Root** (`src/Root.tsx`):
```tsx
import {Composition} from 'remotion';
import {MyVideo} from './MyVideo';

export const RemotionRoot: React.FC = () => (
  <Composition
    id="my-video"
    component={MyVideo}
    durationInFrames={300}
    fps={30}
    width={1920}
    height={1080}
    defaultProps={{title: 'Hello World'}}
  />
);
```

## Core Building Blocks

### Composition — Registering a Video

Each `<Composition>` in Root.tsx defines a renderable video. Think of it as a video template.

```tsx
<Composition
  id="my-video"           // Unique ID, used in render commands
  component={MyVideo}     // React component
  durationInFrames={300}  // 10 seconds at 30fps
  fps={30}
  width={1920}
  height={1080}
  defaultProps={{title: 'Hello'}}  // Fallback props
  schema={myZodSchema}             // Optional: enables visual editing in Studio
/>
```

Use `<Folder name="group">` to organize compositions in the Studio sidebar.

### useCurrentFrame() — The Animation Driver

Returns the current 0-indexed frame number. This is how you animate everything.

```tsx
import {useCurrentFrame} from 'remotion';

const MyVideo: React.FC = () => {
  const frame = useCurrentFrame();
  return <div style={{opacity: Math.min(1, frame / 30)}}>Fading in</div>;
};
```

**Inside a `<Sequence>`, frame resets to 0** relative to the sequence start.

### useVideoConfig() — Video Properties

```tsx
const {width, height, fps, durationInFrames} = useVideoConfig();
```

### AbsoluteFill — The Layout Primitive

Full-size absolutely positioned container. Use it as the root of every scene and for layering content (last child renders on top).

```tsx
import {AbsoluteFill} from 'remotion';

<AbsoluteFill style={{backgroundColor: 'white', justifyContent: 'center', alignItems: 'center'}}>
  <h1>Centered Title</h1>
</AbsoluteFill>
```

### Sequence — Time-shifting Content

Controls when content appears. Children's `useCurrentFrame()` resets to 0 at the sequence start.

```tsx
import {Sequence} from 'remotion';

// Title appears at frame 0, subtitle at frame 30
<Sequence from={0} durationInFrames={90} name="Title">
  <Title />
</Sequence>
<Sequence from={30} durationInFrames={60} name="Subtitle">
  <Subtitle />
</Sequence>
```

- `from` — start frame (negative trims the beginning)
- `durationInFrames` — how long to show (default: Infinity)
- Children unmount outside their time range

### Series — Sequential Scenes

Auto-calculates timing for back-to-back sequences:

```tsx
import {Series} from 'remotion';

<Series>
  <Series.Sequence durationInFrames={60}><Intro /></Series.Sequence>
  <Series.Sequence durationInFrames={120}><MainContent /></Series.Sequence>
  <Series.Sequence durationInFrames={45}><Outro /></Series.Sequence>
</Series>
```

Use `offset` prop for overlap (negative) or gap (positive) between sequences.

### Loop — Repeating Animation

```tsx
import {Loop} from 'remotion';

<Loop durationInFrames={30} times={5}>
  <PulsingDot />
</Loop>
```

## Animation

### interpolate() — Map Values

The core animation function. Maps an input range to an output range.

```tsx
import {interpolate, useCurrentFrame} from 'remotion';

const frame = useCurrentFrame();

// Fade in over 20 frames
const opacity = interpolate(frame, [0, 20], [0, 1], {
  extrapolateLeft: 'clamp',
  extrapolateRight: 'clamp',
});

// Slide from left
const translateX = interpolate(frame, [0, 30], [-200, 0], {
  extrapolateRight: 'clamp',
});

// Fade in AND out
const fadeInOut = interpolate(
  frame,
  [0, 20, 80, 100],
  [0, 1, 1, 0]
);
```

**Always clamp** to prevent values overshooting: `{extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}`.

**Easing** — apply easing curves:
```tsx
import {Easing} from 'remotion';

const value = interpolate(frame, [0, 60], [0, 1], {
  easing: Easing.bezier(0.25, 0.1, 0.25, 1),  // CSS ease equivalent
  extrapolateRight: 'clamp',
});
```

Available easings: `Easing.linear`, `Easing.ease`, `Easing.quad`, `Easing.cubic`, `Easing.bezier(x1,y1,x2,y2)`, `Easing.bounce`, `Easing.elastic()`, `Easing.back()`, `Easing.circle`, `Easing.sin`, `Easing.exp`. Modifiers: `Easing.in()`, `Easing.out()`, `Easing.inOut()`.

### spring() — Physics-based Motion

Returns a value (typically 0→1) with natural spring physics. Feels more organic than easing curves.

```tsx
import {spring, useCurrentFrame, useVideoConfig} from 'remotion';

const frame = useCurrentFrame();
const {fps} = useVideoConfig();

const scale = spring({frame, fps, config: {damping: 200}});
// Use: style={{transform: `scale(${scale})`}}
```

**Parameters:**
- `frame`, `fps` — required
- `from` / `to` — start/end values (default 0→1)
- `config.damping` — deceleration (default 10; use 200 for no bounce)
- `config.mass` — weight (default 1)
- `config.stiffness` — bounciness (default 100)
- `config.overshootClamping` — prevent overshooting
- `delay` — postpone start by N frames
- `durationInFrames` — stretch to exact duration
- `reverse` — play backwards

**Enter + exit pattern:**
```tsx
const enter = spring({fps, frame, config: {damping: 200}});
const exit = spring({fps, frame, delay: 60, config: {damping: 200}, reverse: true});
const scale = enter * exit;  // Or: enter - (1 - exit) depending on effect
```

**Combining spring with interpolate** to map spring output to any range:
```tsx
const driver = spring({frame, fps});
const x = interpolate(driver, [0, 1], [-100, 0]);
const rotation = interpolate(driver, [0, 1], [-45, 0]);
```

### Stagger Pattern

Offset animations for list items:
```tsx
{items.map((item, i) => (
  <Sequence key={i} from={i * 8}>
    <AnimatedItem text={item} />
  </Sequence>
))}
```

## Media

### Static Assets

Place files in `public/` and reference with `staticFile()`:
```tsx
import {staticFile} from 'remotion';
const logo = staticFile('logo.png');    // public/logo.png
const music = staticFile('music.mp3');  // public/music.mp3
```

### Images
```tsx
import {Img, staticFile} from 'remotion';
<Img src={staticFile('photo.png')} style={{width: 400}} />
<Img src="https://example.com/image.jpg" />
```
Use `<Img>` (not `<img>`) — it delays rendering until the image loads.

### Video
```tsx
import {OffthreadVideo, staticFile} from 'remotion';

// Preferred — uses FFmpeg for frame-accurate extraction during render
<OffthreadVideo src={staticFile('clip.mp4')} />
<OffthreadVideo src={staticFile('clip.mp4')} volume={0.5} muted />
<OffthreadVideo
  src={staticFile('clip.mp4')}
  startFrom={30}   // Skip first 30 frames
  endAt={120}       // End at frame 120
/>
```

For looping video, wrap in `<Loop>`.

### Audio
```tsx
import {Audio, staticFile, interpolate} from 'remotion';

<Audio src={staticFile('music.mp3')} volume={0.5} />

// Fade audio in:
<Audio
  src={staticFile('voice.mp3')}
  volume={(f) => interpolate(f, [0, 30], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})}
/>
```

### Fonts

**Google Fonts (recommended):**
```bash
npm i @remotion/google-fonts
```
```tsx
import {loadFont} from '@remotion/google-fonts/Inter';
const {fontFamily} = loadFont();
// Use: style={{fontFamily}}
```

**Local fonts:**
```bash
npm i @remotion/fonts
```
```tsx
import {loadFont} from '@remotion/fonts';
import {staticFile} from 'remotion';
loadFont({family: 'MyFont', url: staticFile('MyFont.woff2'), weight: '400'});
```

## Transitions

```bash
npm i @remotion/transitions
```

```tsx
import {TransitionSeries, linearTiming, springTiming} from '@remotion/transitions';
import {fade} from '@remotion/transitions/fade';
import {slide} from '@remotion/transitions/slide';
import {wipe} from '@remotion/transitions/wipe';

<TransitionSeries>
  <TransitionSeries.Sequence durationInFrames={90}>
    <SceneA />
  </TransitionSeries.Sequence>
  <TransitionSeries.Transition
    presentation={fade()}
    timing={springTiming({config: {damping: 200}})}
  />
  <TransitionSeries.Sequence durationInFrames={90}>
    <SceneB />
  </TransitionSeries.Sequence>
</TransitionSeries>
```

Available presentations: `fade()`, `slide()`, `wipe()`, and more.
Timing options: `linearTiming({durationInFrames})`, `springTiming({config})`.

## Data-Driven Videos

### Props (Parameterized Rendering)

Pass data to videos at render time:

```tsx
// Root.tsx
<Composition
  id="social-post"
  component={SocialPost}
  defaultProps={{username: 'demo', message: 'Hello!'}}
  // ...
/>
```

```bash
# CLI: pass JSON props
npx remotion render social-post --props='{"username":"alice","message":"Great day!"}'
```

### Fetching Data with calculateMetadata

For async data (API calls, dynamic duration):

```tsx
<Composition
  id="data-video"
  component={DataVideo}
  defaultProps={{apiUrl: 'https://api.example.com/data', data: null}}
  calculateMetadata={async ({props, abortSignal}) => {
    const res = await fetch(props.apiUrl, {signal: abortSignal});
    const data = await res.json();
    return {
      props: {...props, data},
      durationInFrames: data.items.length * 90,  // Dynamic duration
    };
  }}
  // ...
/>
```

### Async Loading with delayRender

For assets that must load before a frame renders (fonts, images, data):

```tsx
import {useCallback, useEffect, useState} from 'react';
import {continueRender, delayRender, cancelRender} from 'remotion';

const MyComp: React.FC = () => {
  const [data, setData] = useState(null);
  const [handle] = useState(() => delayRender('Fetching data...'));

  useEffect(() => {
    fetch('https://api.example.com/data')
      .then(res => res.json())
      .then(json => { setData(json); continueRender(handle); })
      .catch(err => cancelRender(err));
  }, [handle]);

  if (!data) return null;
  return <div>{data.title}</div>;
};
```

Always call `continueRender()` or `cancelRender()` — otherwise render hangs after 30s.

## Rendering

### CLI
```bash
# Render to MP4 (default)
npx remotion render my-video out/video.mp4

# Render with custom props
npx remotion render my-video --props='{"title":"Custom"}'

# Other codecs
npx remotion render my-video out/video.webm --codec=vp8
npx remotion render my-video out/video.gif --codec=gif

# Render a still image (single frame)
npx remotion still my-video out/thumbnail.png --frame=0

# Render a range of frames
npx remotion render my-video --frames=0-59

# Control quality
npx remotion render my-video --crf=18 --video-bitrate=8M

# Parallel rendering
npx remotion render my-video --concurrency=4
```

Key flags: `--codec` (h264, h265, vp8, vp9, prores, gif, mp3, aac, wav), `--crf`, `--scale`, `--muted`, `--fps`, `--width`, `--height`.

### Programmatic Rendering (Node.js)

```bash
npm i @remotion/renderer @remotion/bundler
```

```tsx
import path from 'path';
import {bundle} from '@remotion/bundler';
import {renderMedia, selectComposition} from '@remotion/renderer';

// 1. Bundle (do once, reuse for multiple renders)
const serveUrl = await bundle({
  entryPoint: path.resolve('./src/index.ts'),
});

// 2. Select composition
const composition = await selectComposition({
  serveUrl,
  id: 'my-video',
  inputProps: {title: 'Hello'},
});

// 3. Render
await renderMedia({
  composition,
  serveUrl,
  codec: 'h264',
  outputLocation: 'out/video.mp4',
  inputProps: {title: 'Hello'},
  onProgress: ({progress}) => {
    console.log(`${Math.round(progress * 100)}% done`);
  },
});
```

**Render a still:**
```tsx
import {renderStill} from '@remotion/renderer';

await renderStill({
  composition,
  serveUrl,
  output: 'out/thumbnail.png',
  frame: 0,
});
```

**Batch render from data:**
```tsx
for (const item of dataset) {
  const comp = await selectComposition({serveUrl, id: 'template', inputProps: item});
  await renderMedia({composition: comp, serveUrl, codec: 'h264', outputLocation: `out/${item.id}.mp4`, inputProps: item});
}
```

## Additional Packages

Install as needed:

| Package | Purpose |
|---------|---------|
| `@remotion/transitions` | Scene transitions (fade, slide, wipe) |
| `@remotion/animation-utils` | CSS animation helpers (`interpolateStyles`, `makeTransform`) |
| `@remotion/noise` | Simplex noise for procedural effects |
| `@remotion/shapes` | SVG shapes (`<Circle>`, `<Rect>`, `<Star>`, `<Triangle>`, `<Pie>`) |
| `@remotion/paths` | SVG path animation (`evolvePath`, `interpolatePath`, `getLength`) |
| `@remotion/layout-utils` | Text measurement (`measureText`, `fitText`) |
| `@remotion/google-fonts` | Type-safe Google Fonts |
| `@remotion/fonts` | Local font loading |
| `@remotion/tailwind-v4` | TailwindCSS v4 integration |
| `@remotion/media-parser` | Parse video/audio metadata without FFmpeg |
| `@remotion/install-whisper-cpp` | Local audio transcription for captions |
| `@remotion/player` | Embed Remotion preview in any React app |
| `@remotion/three` | React Three Fiber (3D) integration |
| `@remotion/lottie` | Lottie animation embedding |
| `@remotion/gif` | GIF embedding |

## TailwindCSS Setup

```bash
npm i -D @remotion/tailwind-v4 tailwindcss
```

In `remotion.config.ts`:
```ts
import {Config} from '@remotion/cli/config';
import {enableTailwind} from '@remotion/tailwind-v4';
Config.overrideWebpackConfig((config) => enableTailwind(config));
```

Create `src/index.css`:
```css
@import 'tailwindcss';
```

Import in `Root.tsx`:
```tsx
import './index.css';
```

Add to `package.json`:
```json
{"sideEffects": ["*.css"]}
```

## Common Patterns

### Fade In/Out Text
```tsx
const FadeText: React.FC<{text: string}> = ({text}) => {
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  const opacity = interpolate(
    frame,
    [0, 15, durationInFrames - 15, durationInFrames],
    [0, 1, 1, 0],
    {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}
  );
  return (
    <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', opacity}}>
      <h1 style={{fontSize: 80, fontWeight: 'bold'}}>{text}</h1>
    </AbsoluteFill>
  );
};
```

### Slide-in Element
```tsx
const SlideIn: React.FC<{children: React.ReactNode}> = ({children}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const progress = spring({frame, fps, config: {damping: 200}});
  const x = interpolate(progress, [0, 1], [200, 0]);
  const opacity = interpolate(progress, [0, 1], [0, 1]);
  return (
    <div style={{transform: `translateX(${x}px)`, opacity}}>
      {children}
    </div>
  );
};
```

### Animated Counter
```tsx
const Counter: React.FC<{from: number; to: number}> = ({from, to}) => {
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  const value = interpolate(frame, [0, durationInFrames - 1], [from, to], {
    extrapolateRight: 'clamp',
  });
  return <span style={{fontSize: 120, fontWeight: 'bold'}}>{Math.round(value)}</span>;
};
```

### Multi-scene Video
```tsx
const FullVideo: React.FC = () => (
  <TransitionSeries>
    <TransitionSeries.Sequence durationInFrames={90}>
      <AbsoluteFill style={{backgroundColor: '#1a1a2e', justifyContent: 'center', alignItems: 'center'}}>
        <h1 style={{color: 'white', fontSize: 80}}>Welcome</h1>
      </AbsoluteFill>
    </TransitionSeries.Sequence>
    <TransitionSeries.Transition presentation={fade()} timing={linearTiming({durationInFrames: 20})} />
    <TransitionSeries.Sequence durationInFrames={120}>
      <MainContent />
    </TransitionSeries.Sequence>
    <TransitionSeries.Transition presentation={slide()} timing={springTiming({config: {damping: 200}})} />
    <TransitionSeries.Sequence durationInFrames={60}>
      <Outro />
    </TransitionSeries.Sequence>
  </TransitionSeries>
);
```

## Workflow

When the user asks you to create a video:

1. **Clarify the content** — What should the video show? Duration? Resolution? Format?
2. **Set up the project** — Create or scaffold the Remotion project with required dependencies
3. **Build compositions** — Write the React components for each scene
4. **Add animations** — Use `interpolate()`, `spring()`, and `<Sequence>` for motion
5. **Handle media** — Import images, video, audio, fonts as needed
6. **Preview** — Run `npx remotion studio` for the visual preview
7. **Render** — Use CLI or programmatic rendering to output the final video

For more details on any API, read the reference files in `references/` or consult the [Remotion docs](https://www.remotion.dev/docs/).

## Lessons Learned (from production use)

### objectFit: contain breaks coordinate mapping

When using `objectFit: 'contain'` on `<Img>`, images with different aspect ratios than the canvas get margins. **Any overlay positioning (cursors, text, click effects) must account for the contain layout.**

```typescript
// Compute contain margins before mapping coordinates
function getContainLayout(imageWidth: number, imageHeight: number) {
  const imageAspect = imageWidth / imageHeight;
  const canvasAspect = 1920 / 1080;
  if (imageAspect > canvasAspect) {
    // Wider: fit width, bars top/bottom
    const displayHeight = 1920 / imageAspect;
    return { offsetX: 0, offsetY: (1080 - displayHeight) / 2, displayWidth: 1920, displayHeight };
  } else {
    // Taller: fit height, bars left/right
    const displayWidth = 1080 * imageAspect;
    return { offsetX: (1920 - displayWidth) / 2, offsetY: 0, displayWidth, displayHeight: 1080 };
  }
}
```

Always pass source image `{width, height}` to coordinate mapping functions. A 28px offset is clearly visible at 1080p.

### Reusable scenes must use proportional timing for ALL parameters

When a scene component is reused across compositions with different `durationInFrames`, every animation parameter must scale — not just keyframe positions.

**Bad:** `charsPerSecond={6}` — typing gets cut off in shorter compositions.
**Good:** `charsPerSecond = textLength / (availableRatio * durationInFrames / fps)`

Use `const t = (ratio: number) => Math.round(ratio * durationInFrames)` for keyframes, AND calculate rates dynamically for TypeWriter, scroll speed, etc.

### Self-check rendered output at full scale

Never declare a scene "passes" from small cropped images. Always:
1. Render stills at key frames via `npx remotion still`
2. Serve via `python3 -m http.server`
3. Open in Playwright browser at full viewport size
4. Compare cursor/text positions against original screenshot elements
5. Use before/after diff (stack vertically) to verify alignment

### Editing text out of JPEG screenshots

Don't paint solid rectangles — JPEG compression artifacts make them visible. Instead, clone pixels per-column from an adjacent empty region:

```python
# Clone from row above text, preserving JPEG block patterns per column
for x in range(text_x_start, text_x_end):
    source_pixel = img.getpixel((x, y_above_text))
    for y in range(text_y_start, text_y_end):
        img.putpixel((x, y), source_pixel)
```
