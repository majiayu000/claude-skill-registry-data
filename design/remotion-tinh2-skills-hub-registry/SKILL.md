---
name: remotion
description: Build programmatic videos with Remotion (React). Covers compositions, animations, sequencing, transitions, audio/video embedding, spring physics, text animations, voiceover generation with ElevenLabs TTS, FFmpeg integration, captions/subtitles, 3D with Three.js, charts, and rendering. Based on official Remotion best practices.
version: 1.0.0
category: build
platforms:
  - CLAUDE_CODE
  - CURSOR
permissions:
  - filesystem
  - shell
---

# Remotion -- Video Creation in React

Use this skill when working with Remotion code. Remotion lets you create videos programmatically using React components.

## Project Setup

```bash
npx create-video@latest my-video
cd my-video
npm start        # Preview in browser
npm run render   # Render to MP4
```

## Compositions

A `<Composition>` defines a renderable video with dimensions, fps, and duration.

```tsx
import { Composition } from "remotion";
import { MyVideo } from "./MyVideo";

export const RemotionRoot = () => (
  <Composition
    id="MyVideo"
    component={MyVideo}
    durationInFrames={300}
    fps={30}
    width={1920}
    height={1080}
    defaultProps={{ title: "Hello World" } satisfies MyVideoProps}
  />
);
```

Use `type` declarations for props (not `interface`) for `defaultProps` type safety.

Use `<Folder>` to organize compositions in the sidebar. Use `<Still>` for single-frame outputs (thumbnails, OG images).

## Animations

All animations MUST use `useCurrentFrame()`. CSS transitions and Tailwind animation classes are FORBIDDEN -- they will not render correctly.

```tsx
import { useCurrentFrame, useVideoConfig, interpolate } from "remotion";

export const FadeIn = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const opacity = interpolate(frame, [0, 2 * fps], [0, 1], {
    extrapolateRight: "clamp",
  });

  return <div style={{ opacity }}>Hello World!</div>;
};
```

### Spring Animations

Springs provide natural motion. They animate from 0 to 1.

```tsx
import { spring, useCurrentFrame, useVideoConfig } from "remotion";

const frame = useCurrentFrame();
const { fps } = useVideoConfig();

const scale = spring({ frame, fps });
// With config:
const smooth = spring({ frame, fps, config: { damping: 200 } }); // No bounce
const snappy = spring({ frame, fps, config: { damping: 20, stiffness: 200 } });
const bouncy = spring({ frame, fps, config: { damping: 8 } });
const heavy  = spring({ frame, fps, config: { damping: 15, stiffness: 80, mass: 2 } });
```

Use `delay` parameter to delay spring start:
```tsx
const entrance = spring({ frame, fps, delay: 20 });
```

### Interpolation

```tsx
// Linear interpolation with clamping
const opacity = interpolate(frame, [0, 100], [0, 1], {
  extrapolateRight: "clamp",
  extrapolateLeft: "clamp",
});

// Multi-step interpolation
const y = interpolate(frame, [0, 30, 60, 90], [100, 0, 0, -100]);
```

## Sequencing

### Sequence

Use `<Sequence>` to delay when elements appear. Always use `premountFor` to preload components.

```tsx
import { Sequence } from "remotion";

const { fps } = useVideoConfig();

<Sequence from={1 * fps} durationInFrames={2 * fps} premountFor={1 * fps}>
  <Title />
</Sequence>
<Sequence from={2 * fps} durationInFrames={2 * fps} premountFor={1 * fps}>
  <Subtitle />
</Sequence>
```

Use `layout="none"` to prevent absolute positioning wrapper.

### Series

Use `<Series>` for sequential playback without overlap:

```tsx
import { Series } from "remotion";

<Series>
  <Series.Sequence durationInFrames={45}><Intro /></Series.Sequence>
  <Series.Sequence durationInFrames={60}><MainContent /></Series.Sequence>
  <Series.Sequence durationInFrames={30}><Outro /></Series.Sequence>
</Series>
```

Negative `offset` creates overlapping transitions:
```tsx
<Series.Sequence offset={-15} durationInFrames={60}>
  <SceneB />
</Series.Sequence>
```

## Transitions

```bash
npx remotion add @remotion/transitions
```

```tsx
import { TransitionSeries, linearTiming } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";
import { slide } from "@remotion/transitions/slide";
import { wipe } from "@remotion/transitions/wipe";

<TransitionSeries>
  <TransitionSeries.Sequence durationInFrames={60}>
    <SceneA />
  </TransitionSeries.Sequence>
  <TransitionSeries.Transition
    presentation={fade()}
    timing={linearTiming({ durationInFrames: 15 })}
  />
  <TransitionSeries.Sequence durationInFrames={60}>
    <SceneB />
  </TransitionSeries.Sequence>
</TransitionSeries>
```

### Light Leak Overlays

```tsx
import { LightLeak } from "@remotion/light-leaks";

<TransitionSeries>
  <TransitionSeries.Sequence durationInFrames={60}>
    <SceneA />
  </TransitionSeries.Sequence>
  <TransitionSeries.Overlay durationInFrames={20}>
    <LightLeak />
  </TransitionSeries.Overlay>
  <TransitionSeries.Sequence durationInFrames={60}>
    <SceneB />
  </TransitionSeries.Sequence>
</TransitionSeries>
```

An overlay cannot be adjacent to a transition or another overlay.

## Audio

```bash
npx remotion add @remotion/media
```

```tsx
import { Audio } from "@remotion/media";
import { staticFile } from "remotion";

// Basic audio
<Audio src={staticFile("audio.mp3")} />

// With trimming (values in frames)
<Audio src={staticFile("audio.mp3")} trimBefore={2 * fps} trimAfter={10 * fps} />

// Volume control
<Audio src={staticFile("audio.mp3")} volume={0.5} />

// Dynamic volume (callback receives frame)
<Audio src={staticFile("audio.mp3")} volume={(f) =>
  interpolate(f, [0, 30], [0, 1], { extrapolateRight: "clamp" })
} />

// Speed change
<Audio src={staticFile("audio.mp3")} playbackRate={1.5} />

// Delay audio start
<Sequence from={1 * fps}>
  <Audio src={staticFile("audio.mp3")} />
</Sequence>
```

Multiple `<Audio>` components layer automatically.

## Video Embedding

```tsx
import { Video } from "@remotion/media";

// Basic video
<Video src={staticFile("video.mp4")} />

// With trimming
<Video src={staticFile("video.mp4")} trimBefore={2 * fps} trimAfter={10 * fps} />

// Speed, volume, looping
<Video src={staticFile("video.mp4")} playbackRate={2} volume={0.5} loop />

// For rendering performance, use OffthreadVideo
import { OffthreadVideo } from "remotion";
<OffthreadVideo src={staticFile("video.mp4")} />
```

ALWAYS use `<OffthreadVideo>` for better rendering performance. Use `<Video>` only during preview.

## Voiceover with ElevenLabs TTS

Generate speech per scene, then use `calculateMetadata` to size the composition dynamically.

### Generate Audio

```ts
const response = await fetch(
  `https://api.elevenlabs.io/v1/text-to-speech/${voiceId}`,
  {
    method: "POST",
    headers: {
      "xi-api-key": process.env.ELEVENLABS_API_KEY!,
      "Content-Type": "application/json",
      Accept: "audio/mpeg",
    },
    body: JSON.stringify({
      text: "Welcome to the show.",
      model_id: "eleven_multilingual_v2",
      voice_settings: { stability: 0.5, similarity_boost: 0.75, style: 0.3 },
    }),
  },
);
const audioBuffer = Buffer.from(await response.arrayBuffer());
writeFileSync(`public/voiceover/scene-01.mp3`, audioBuffer);
```

### Dynamic Duration

```tsx
import { CalculateMetadataFunction, staticFile } from "remotion";

const FPS = 30;
const SCENES = ["voiceover/scene-01.mp3", "voiceover/scene-02.mp3"];

export const calculateMetadata: CalculateMetadataFunction<Props> = async () => {
  const durations = await Promise.all(
    SCENES.map((file) => getAudioDuration(staticFile(file)))
  );
  const totalFrames = durations.reduce((sum, d) => sum + Math.ceil(d * FPS), 0);
  return { durationInFrames: totalFrames };
};
```

## Assets

Place files in `public/` and reference with `staticFile()`:

```tsx
import { staticFile, Img } from "remotion";

<Img src={staticFile("logo.png")} />
```

NEVER use `require()` or `import` for media files. Always use `staticFile()`.

### Fonts

```tsx
import { loadFont } from "@remotion/google-fonts/Inter";
const { fontFamily } = loadFont();

// Or local fonts
const { fontFamily } = loadFont({
  url: staticFile("fonts/MyFont.woff2"),
  display: "swap",
});
```

## FFmpeg in Remotion

FFmpeg is bundled -- no install needed:

```bash
bunx remotion ffmpeg -i input.mp4 output.mp3
bunx remotion ffprobe input.mp4
```

For trimming, prefer the `trimBefore`/`trimAfter` props over FFmpeg. Use FFmpeg for format conversion or operations Remotion cannot do natively.

When using FFmpeg to trim, MUST re-encode to avoid frozen frames:
```bash
bunx remotion ffmpeg -ss 00:00:05 -i public/input.mp4 -to 00:00:10 -c:v libx264 -c:a aac public/output.mp4
```

## Rendering

```bash
# Render specific composition
npx remotion render MyVideo output.mp4

# Render a still frame
npx remotion still MyVideo --frame=100 thumbnail.png

# With custom props
npx remotion render MyVideo output.mp4 --props='{"title": "Custom"}'

# Specific codec
npx remotion render MyVideo output.webm --codec=vp8
```

## Common Patterns

### Scene-Based Video

```tsx
const SCENES = [
  { component: TitleScene, duration: 90 },
  { component: ProblemScene, duration: 150 },
  { component: SolutionScene, duration: 120 },
  { component: CTAScene, duration: 90 },
];

export const MyVideo = () => {
  let offset = 0;
  return (
    <>
      {SCENES.map(({ component: Component, duration }, i) => {
        const from = offset;
        offset += duration;
        return (
          <Sequence key={i} from={from} durationInFrames={duration}>
            <Component />
          </Sequence>
        );
      })}
    </>
  );
};
```

### Background Music + Voiceover

```tsx
<>
  {/* Background music at low volume */}
  <Audio src={staticFile("music/bg.mp3")} volume={0.12} loop />

  {/* Scene voiceovers at full volume */}
  <Sequence from={0} durationInFrames={scene1Frames}>
    <Audio src={staticFile("voiceover/scene-01.mp3")} volume={1} />
  </Sequence>
  <Sequence from={scene1Frames} durationInFrames={scene2Frames}>
    <Audio src={staticFile("voiceover/scene-02.mp3")} volume={1} />
  </Sequence>
</>
```

## Key Rules

1. **No CSS animations** -- all motion via `useCurrentFrame()` + `interpolate()`/`spring()`
2. **No Tailwind animation classes** -- they don't render correctly
3. **Always `staticFile()`** for assets, never `require()`
4. **Always premount Sequences** with `premountFor`
5. **Use `<OffthreadVideo>`** not `<video>` for rendering
6. **Write durations in seconds** and multiply by `fps`
7. **Use `satisfies` keyword** for `defaultProps` type safety

Source: [remotion-dev/skills](https://github.com/remotion-dev/skills), [remotion.dev](https://www.remotion.dev)
