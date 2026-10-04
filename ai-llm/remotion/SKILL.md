---
name: remotion
description: Programmatic video creation with React via Remotion — compositions, animations, motion graphics, rendered to MP4. Includes Stitch project walkthrough workflows, content-to-animation pipelines, and export/rendering. USE WHEN video, animation, motion graphics, video rendering, React video, intro video, YouTube video, TikTok video, video production, render video, content to animation, animate content, video overlay, walkthrough video, Stitch screens.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, "stitch*:*", "remotion*:*", web_fetch
---

Create programmatic videos using Remotion: $ARGUMENTS

$ARGUMENTS should include:
- What video to create (walkthrough, course video, social clip, trailer, presentation, animated explainer)
- Optionally: Stitch project name (for walkthrough videos)
- Optionally: duration in seconds or frames
- Optionally: resolution (1080p, 720p, 4K, vertical)
- Optionally: audio source (TTS text, audio file path, music)
- Optionally: video/image assets to composite
- Optionally: output format (mp4, webm, gif)
- Optionally: target composition path
- Empty — ask the user what they want to create

# Remotion

Create professional videos programmatically with React.

## Customization

**Before executing, check for user customizations at:**
`~/.claude/PAI/USER/SKILLCUSTOMIZATIONS/Remotion/`

## Workflow Routing

| Trigger | Workflow |
|---------|----------|
| "animate this", "create animations for", "video overlay" | Content-to-Animation (see below) |
| "walkthrough", "Stitch screens", "app demo" | Stitch Walkthrough (see below) |

## Quick Reference

- **Theme:** Always use PAI_THEME from `Tools/Theme.ts`
- **Art Integration:** Load Art preferences before creating content (see `ArtIntegration.md`)
- **Critical:** NO CSS animations — use `useCurrentFrame()` only
- **Output:** Always to `~/Downloads/` first

**Render command:**
```bash
npx remotion render {composition-id} ~/Downloads/{name}.mp4
```

## Authoritative Documentation

### Primary References
- Getting Started: https://www.remotion.dev/docs/
- The Fundamentals: https://www.remotion.dev/docs/the-fundamentals
- API Reference: https://www.remotion.dev/docs/api
- CLI Reference: https://www.remotion.dev/docs/cli
- Templates: https://www.remotion.dev/templates
- GitHub: https://github.com/remotion-dev/remotion

### Core Concepts
- Compositions: https://www.remotion.dev/docs/composition
- useCurrentFrame: https://www.remotion.dev/docs/use-current-frame
- useVideoConfig: https://www.remotion.dev/docs/use-video-config
- Sequence: https://www.remotion.dev/docs/sequence
- AbsoluteFill: https://www.remotion.dev/docs/absolute-fill
- Spring Animation: https://www.remotion.dev/docs/spring
- Interpolation: https://www.remotion.dev/docs/interpolate

### Media & Assets
- Audio: https://www.remotion.dev/docs/using-audio
- OffthreadVideo: https://www.remotion.dev/docs/offthreadvideo
- Img: https://www.remotion.dev/docs/img
- staticFile: https://www.remotion.dev/docs/staticfile
- Fonts: https://www.remotion.dev/docs/fonts
- Lottie Animations: https://www.remotion.dev/docs/lottie

### Rendering
- Rendering Overview: https://www.remotion.dev/docs/render
- renderMedia: https://www.remotion.dev/docs/renderer/render-media
- CLI Render: https://www.remotion.dev/docs/cli/render
- Lambda Rendering: https://www.remotion.dev/docs/lambda
- Cloud Run Rendering: https://www.remotion.dev/docs/cloudrun
- GPU Rendering: https://www.remotion.dev/docs/gpu
- Output Formats: https://www.remotion.dev/docs/encoding

### Player (Web Embedding)
- @remotion/player: https://www.remotion.dev/docs/player
- Player API: https://www.remotion.dev/docs/player/api
- Player Examples: https://www.remotion.dev/docs/player/examples

### Studio
- Remotion Studio: https://www.remotion.dev/docs/studio
- Input Props: https://www.remotion.dev/docs/visual-editing

### AI Integration
- Claude Code Integration: https://www.remotion.dev/docs/ai/claude-code
- AI Prompting Guide: https://www.remotion.dev/docs/ai
- Remotion Skills: https://www.remotion.dev/docs/ai/skills
- Remotion MCP: https://www.remotion.dev/docs/ai/mcp

### Advanced
- Data Fetching: https://www.remotion.dev/docs/data-fetching
- Transitions: https://www.remotion.dev/docs/transitions
- Tailwind in Remotion: https://www.remotion.dev/docs/tailwind
- Three.js (3D): https://www.remotion.dev/docs/three
- Noise & Motion: https://www.remotion.dev/docs/noise

### Pricing & Source
- Pricing: https://www.remotion.dev/pricing
- npm: https://www.npmjs.com/package/remotion
- Companies with under $25K annual revenue: free
- Rendering itself is free — you only pay for cloud if using Lambda/Cloud Run
- Lambda pricing: ~$0.01-0.05 per render (AWS costs)

## Before Starting

1. For new projects: `pnpm create video` (or `npx create-video@latest`)
2. For existing projects: `pnpm add remotion @remotion/cli @remotion/bundler`
3. Start Remotion Studio: `pnpm remotion studio` or `npx remotion studio`
4. Node.js 16+ required. Chrome/Chromium used for rendering.
5. For audio integration, have TTS files ready or generate with OpenAI TTS / ElevenLabs skills.

## Supporting Files

| File | Purpose |
|------|---------|
| `ArtIntegration.md` | Theme constants, color mapping from Art skill |
| `CriticalRules.md` | Remotion best practices and rules index |
| `Patterns.md` | Common code examples and presets |
| `Tools/Render.ts` | TypeScript wrappers for rendering, listing compositions, creating projects |
| `Tools/Theme.ts` | PAI theme constants derived from Art preferences |
| `Tools/Ref-*.md` | 28 detailed reference files for specific Remotion topics |
| `Workflows/ContentToAnimation.md` | Full content-to-animation pipeline |

## Core Concepts

### Frame-Based Thinking

Remotion videos are React components that render one frame at a time. Every frame is a function of `useCurrentFrame()`.

| Property | Typical Value | Description |
|---|---|---|
| `fps` | 30 | Frames per second |
| `durationInFrames` | 300 | Total frames (300 / 30 = 10 seconds) |
| `width` | 1920 | Output width in pixels |
| `height` | 1080 | Output height in pixels |

**Time math:** `seconds x fps = frames`. So 5 seconds at 30fps = 150 frames.

### Composition (the video definition)

```tsx
// src/Root.tsx
import { Composition } from "remotion";
import { MyVideo } from "./MyVideo";

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="MyVideo"
      component={MyVideo}
      durationInFrames={300}
      fps={30}
      width={1920}
      height={1080}
      defaultProps={{
        title: "Hello World",
      }}
    />
  );
};
```

### useCurrentFrame — The Heart of Animation

```tsx
import { useCurrentFrame, useVideoConfig, AbsoluteFill } from "remotion";

export const MyVideo: React.FC<{ title: string }> = ({ title }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames, width, height } = useVideoConfig();

  // Animate opacity: fade in over first 30 frames (1 second)
  const opacity = Math.min(1, frame / 30);

  return (
    <AbsoluteFill style={{ backgroundColor: "#0a0a0a" }}>
      <h1
        style={{
          color: "white",
          fontSize: 80,
          fontWeight: "bold",
          opacity,
          textAlign: "center",
          marginTop: height / 2 - 50,
        }}
      >
        {title}
      </h1>
    </AbsoluteFill>
  );
};
```

## Animation Primitives

### interpolate — Map frame ranges to value ranges

```tsx
import { interpolate, useCurrentFrame } from "remotion";

const frame = useCurrentFrame();

// Fade in from frame 0-30
const opacity = interpolate(frame, [0, 30], [0, 1], {
  extrapolateRight: "clamp",
});

// Slide up from frame 10-40
const translateY = interpolate(frame, [10, 40], [50, 0], {
  extrapolateLeft: "clamp",
  extrapolateRight: "clamp",
});

// Scale pulse from frame 20-50
const scale = interpolate(frame, [20, 35, 50], [0.8, 1.05, 1], {
  extrapolateLeft: "clamp",
  extrapolateRight: "clamp",
});
```

**Easing functions:**
```tsx
import { Easing } from "remotion";

const opacity = interpolate(frame, [0, 30], [0, 1], {
  easing: Easing.bezier(0.25, 0.1, 0.25, 1),
  extrapolateRight: "clamp",
});
```

### spring — Physics-based animation

```tsx
import { spring, useCurrentFrame, useVideoConfig } from "remotion";

const frame = useCurrentFrame();
const { fps } = useVideoConfig();

const scale = spring({
  frame,
  fps,
  config: {
    damping: 12,
    stiffness: 200,
    mass: 0.5,
  },
});

// Delayed spring (starts at frame 20)
const delayedScale = spring({
  frame: frame - 20,
  fps,
  config: { damping: 10, stiffness: 100 },
});
```

### Sequence — Time-based composition

```tsx
import { Sequence, AbsoluteFill } from "remotion";

export const MyVideo: React.FC = () => {
  return (
    <AbsoluteFill>
      {/* Title appears at frame 0, lasts 90 frames (3s) */}
      <Sequence from={0} durationInFrames={90}>
        <TitleCard text="Introduction" />
      </Sequence>

      {/* Content appears at frame 60 (2s), lasts 150 frames (5s) */}
      <Sequence from={60} durationInFrames={150}>
        <ContentSlide />
      </Sequence>

      {/* Outro appears at frame 180 (6s), lasts until end */}
      <Sequence from={180}>
        <OutroCard />
      </Sequence>
    </AbsoluteFill>
  );
};
```

**Key:** Inside a `<Sequence>`, `useCurrentFrame()` resets to 0. Frame 0 inside corresponds to the `from` frame of the parent.

## Media Integration

### Audio

```tsx
import { Audio, staticFile } from "remotion";

// From public folder
<Audio src={staticFile("narration.mp3")} />

// With volume control
<Audio
  src={staticFile("background-music.mp3")}
  volume={(f) =>
    interpolate(f, [0, 30], [0, 0.3], { extrapolateRight: "clamp" })
  }
  startFrom={0}
  endAt={300}
/>
```

### Video (OffthreadVideo — recommended)

```tsx
import { OffthreadVideo, staticFile } from "remotion";

<OffthreadVideo
  src={staticFile("hero-clip.mp4")}
  style={{ width: "100%", height: "100%" }}
  startFrom={0}
/>
```

### Images

```tsx
import { Img, staticFile } from "remotion";

<Img
  src={staticFile("hero-image.png")}
  style={{ width: "100%", height: "100%", objectFit: "cover" }}
/>
```

### Fonts

```tsx
// src/fonts.ts
import { staticFile } from "remotion";

const interFont = new FontFace("Inter", `url(${staticFile("Inter.woff2")})`);
document.fonts.add(interFont);

// Or use @remotion/google-fonts
import { loadFont } from "@remotion/google-fonts/Inter";
const { fontFamily } = loadFont();
```

## Transitions

```tsx
import { TransitionSeries, linearTiming, fade, slide } from "@remotion/transitions";

export const MyVideo: React.FC = () => {
  return (
    <TransitionSeries>
      <TransitionSeries.Sequence durationInFrames={90}>
        <SlideOne />
      </TransitionSeries.Sequence>

      <TransitionSeries.Transition
        presentation={fade()}
        timing={linearTiming({ durationInFrames: 15 })}
      />

      <TransitionSeries.Sequence durationInFrames={90}>
        <SlideTwo />
      </TransitionSeries.Sequence>

      <TransitionSeries.Transition
        presentation={slide({ direction: "from-right" })}
        timing={linearTiming({ durationInFrames: 20 })}
      />

      <TransitionSeries.Sequence durationInFrames={90}>
        <SlideThree />
      </TransitionSeries.Sequence>
    </TransitionSeries>
  );
};
```

Available transitions: `fade()`, `slide()`, `wipe()`, `flip()`, `clockWipe()`, `none()`

## Template Patterns

### Pattern 1 — Title Card with Animated Text

```tsx
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";

export const TitleCard: React.FC<{ title: string; subtitle: string }> = ({ title, subtitle }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const titleOpacity = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: "clamp" });
  const titleY = spring({ frame, fps, config: { damping: 12, stiffness: 200 } });
  const subtitleOpacity = interpolate(frame, [15, 35], [0, 1], { extrapolateRight: "clamp" });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#0a0a0a",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <h1
        style={{
          color: "white",
          fontSize: 72,
          fontWeight: 800,
          opacity: titleOpacity,
          transform: `translateY(${interpolate(titleY, [0, 1], [40, 0])}px)`,
        }}
      >
        {title}
      </h1>
      <p
        style={{
          color: "#a0a0a0",
          fontSize: 28,
          marginTop: 16,
          opacity: subtitleOpacity,
        }}
      >
        {subtitle}
      </p>
    </AbsoluteFill>
  );
};
```

### Pattern 2 — Narrated Slide with Audio

```tsx
import { AbsoluteFill, Audio, Sequence, staticFile } from "remotion";

export const NarratedSlide: React.FC<{
  title: string;
  bulletPoints: string[];
  audioFile: string;
}> = ({ title, bulletPoints, audioFile }) => {
  return (
    <AbsoluteFill style={{ backgroundColor: "#0a0a0a", padding: 80 }}>
      <Audio src={staticFile(audioFile)} />

      <Sequence from={0} durationInFrames={30}>
        <AnimatedTitle text={title} />
      </Sequence>

      {bulletPoints.map((point, i) => (
        <Sequence key={i} from={30 + i * 30} durationInFrames={90}>
          <AnimatedBullet text={point} index={i} />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};
```

### Pattern 3 — Social Media Clip (Vertical)

```tsx
// In Root.tsx — register the vertical composition
<Composition
  id="SocialClip"
  component={SocialClip}
  durationInFrames={150}  // 5 seconds
  fps={30}
  width={1080}
  height={1920}
/>
```

### Pattern 4 — Video with Background Music + Narration

```tsx
export const CourseIntro: React.FC = () => {
  return (
    <AbsoluteFill>
      {/* Background video */}
      <OffthreadVideo src={staticFile("hero-background.mp4")} style={{ objectFit: "cover" }} />

      {/* Overlay for readability */}
      <AbsoluteFill style={{ backgroundColor: "rgba(0,0,0,0.5)" }} />

      {/* Content */}
      <Sequence from={0}>
        <TitleCard title="Course: Leadership Essentials" subtitle="Module 1 — Introduction" />
      </Sequence>

      {/* Narration from TTS */}
      <Audio src={staticFile("narration-intro.mp3")} />

      {/* Background music (low volume) */}
      <Audio
        src={staticFile("ambient-music.mp3")}
        volume={0.15}
      />
    </AbsoluteFill>
  );
};
```

### Pattern 5 — Interactive Hotspot (for walkthrough videos)

```tsx
import { interpolate, useCurrentFrame, spring } from 'remotion';

const Hotspot = ({ x, y, label }) => {
  const frame = useCurrentFrame();
  const scale = spring({
    frame,
    fps: 30,
    config: { damping: 10, stiffness: 100 }
  });

  return (
    <div style={{
      position: 'absolute',
      left: x,
      top: y,
      transform: `scale(${scale})`
    }}>
      <div className="pulse-ring" />
      <span>{label}</span>
    </div>
  );
};
```

## Rendering

### CLI Rendering (recommended for scripts)

```bash
# Basic render
npx remotion render src/index.ts MyVideo out/video.mp4

# With options
npx remotion render src/index.ts MyVideo out/video.mp4 \
  --codec h264 \
  --props '{"title": "Hello World"}' \
  --concurrency 4

# Render specific frame range
npx remotion render src/index.ts MyVideo out/video.mp4 \
  --frames 0-150

# Still image (single frame)
npx remotion still src/index.ts MyVideo out/thumbnail.png \
  --frame 45
```

### Programmatic Rendering (Node.js)

```typescript
import { bundle } from "@remotion/bundler";
import { renderMedia, selectComposition } from "@remotion/renderer";

const bundled = await bundle({
  entryPoint: "./src/index.ts",
});

const composition = await selectComposition({
  serveUrl: bundled,
  id: "MyVideo",
  inputProps: { title: "Generated Video" },
});

await renderMedia({
  composition,
  serveUrl: bundled,
  codec: "h264",
  outputLocation: "out/video.mp4",
  inputProps: { title: "Generated Video" },
  onProgress: ({ progress }) => {
    console.log(`Rendering: ${Math.round(progress * 100)}%`);
  },
});
```

### Output Codecs

| Codec | Extension | Best For |
|---|---|---|
| `h264` | `.mp4` | General distribution (default) |
| `h265` | `.mp4` | Smaller files, wider device support |
| `vp8` | `.webm` | Web playback |
| `vp9` | `.webm` | Web playback (better quality) |
| `prores` | `.mov` | Professional editing |
| `gif` | `.gif` | Short loops, social |

### Resolution Presets

| Preset | Width | Height | Use Case |
|---|---|---|---|
| 1080p Landscape | 1920 | 1080 | Course videos, YouTube |
| 720p Landscape | 1280 | 720 | Social, drafts |
| 4K Landscape | 3840 | 2160 | High-end production |
| 1080p Portrait | 1080 | 1920 | Instagram Reels, TikTok, Shorts |
| Square | 1080 | 1080 | Instagram posts |
| Instagram 4:5 | 1080 | 1350 | Instagram portrait posts |

## Player — Web Embedding

```tsx
import { Player } from "@remotion/player";
import { MyVideo } from "./MyVideo";

export function VideoPlayer() {
  return (
    <Player
      component={MyVideo}
      inputProps={{ title: "Preview" }}
      durationInFrames={300}
      compositionWidth={1920}
      compositionHeight={1080}
      fps={30}
      style={{ width: "100%", maxWidth: 800 }}
      controls
      autoPlay
      loop
    />
  );
}
```

## Data-Driven Videos

### Input Props with Zod Schema

```tsx
import { z } from "zod";

const schema = z.object({
  title: z.string(),
  subtitle: z.string(),
  bulletPoints: z.array(z.string()),
  bgColor: z.string().default("#0a0a0a"),
});

// In Root.tsx
<Composition
  id="DataDrivenSlide"
  component={DataDrivenSlide}
  durationInFrames={300}
  fps={30}
  width={1920}
  height={1080}
  schema={schema}
  defaultProps={{
    title: "Default Title",
    subtitle: "Subtitle",
    bulletPoints: ["Point 1", "Point 2"],
    bgColor: "#0a0a0a",
  }}
/>
```

### calculateMetadata — Dynamic Duration

```tsx
import { CalculateMetadataFunction } from "remotion";

export const calculateMetadata: CalculateMetadataFunction<Props> = async ({ props }) => {
  const audioDuration = await getAudioDurationInSeconds(props.audioUrl);
  const fps = 30;

  return {
    durationInFrames: Math.ceil(audioDuration * fps),
    props,
  };
};

// In Root.tsx
<Composition
  id="NarratedVideo"
  component={NarratedVideo}
  calculateMetadata={calculateMetadata}
  fps={30}
  width={1920}
  height={1080}
/>
```

## Stitch Walkthrough Videos

For creating walkthrough videos from Stitch app designs.

### Prerequisites

- Access to the Stitch MCP Server
- A Stitch project with designed screens

### Stitch Workflow

1. **Discover MCP servers**: Run `list_tools` to find `stitch:` prefix
2. **Project lookup**: Call `[stitch_prefix]:list_projects` with `filter: "view=owned"`
3. **Screen retrieval**: Call `[stitch_prefix]:list_screens` with the project ID
4. **Screen metadata**: For each screen, call `[stitch_prefix]:get_screen` to retrieve:
   - `screenshot.downloadUrl` — Visual asset for the video
   - `htmlCode.downloadUrl` — Optional: for extracting text/content
   - `width`, `height` — Screen dimensions
   - Screen title and description for text overlays
5. **Asset download**: Use `web_fetch` or `curl` to download screenshots to `assets/screens/`

### Screen Manifest

Create a `screens.json` manifest:

```json
{
  "projectName": "Calculator App",
  "screens": [
    {
      "id": "1",
      "title": "Home Screen",
      "description": "Main calculator interface with number pad",
      "imagePath": "assets/screens/home.png",
      "width": 1200,
      "height": 800,
      "duration": 4
    }
  ]
}
```

### Walkthrough Architecture

1. **`ScreenSlide.tsx`** — Individual screen display with zoom/fade animations
2. **`WalkthroughComposition.tsx`** — Sequences slides with transitions
3. **Config** — Match dimensions to Stitch screen sizes

### Walkthrough Patterns

**Simple Slide Show:** 3-5 seconds per screen, cross-fade transitions, bottom title overlay, progress bar.

**Feature Highlight:** Zoom into specific regions, animated circles/arrows, slow-motion emphasis, side-by-side comparisons.

**User Flow:** Sequential screens with directional slides, numbered steps, animated connecting paths.

### Dynamic Text Extraction

Extract text from Stitch HTML for automatic annotations:
1. Download `htmlCode.downloadUrl` for each screen
2. Parse HTML for key text elements (headings, buttons, labels)
3. Generate automatic callouts as timed text overlays

### Voiceover Integration

1. Generate voiceover script from screen descriptions
2. Use text-to-speech or record audio
3. Import audio with `<Audio>` component
4. Sync screen timing with voiceover pacing

## Content-to-Animation Workflow

Transform any content into professional themed animations. Full pipeline documented in `Workflows/ContentToAnimation.md`.

### Triggers

- "animate this content"
- "create animations for"
- "video overlay for"

### Supported Input Types

| Input Type | Detection | Extraction Method |
|------------|-----------|-------------------|
| YouTube URL | `youtube.com`, `youtu.be` | Parser: ExtractYoutube |
| Article URL | HTTP(S) URL | Parser: ExtractArticle |
| Blog file | `.md` file path | Direct read |
| PDF file | `.pdf` file path | Parser: ExtractPdf |
| Tweet/Thread | `twitter.com`, `x.com` | Parser: ExtractTwitter |
| Raw text | No URL/path detected | Use directly |

### Content-to-Animation Steps

1. **Extract Content** — Detect input type and extract title, sections, key points, quotes, data
2. **Analyze Structure** — Map to `ContentStructure` interface
3. **Generate Animation Plan** — Map content to scenes with timing
4. **Verify Logical Coherence** (critical gate) — Check narrative flow, timing, scene selection
5. **Generate Remotion Components** — Create project at `/tmp/remotion-{timestamp}/`
6. **Render Output** — `npx remotion render {id} ~/Downloads/{name}.mp4`

### Timing Formula

- Title: 90 frames (3 seconds at 30fps)
- Per section: 120-180 frames (4-6 seconds)
- Conclusion: 90 frames (3 seconds)
- Total = 90 + (sections x 150) + 90

### Coherence Verification

Before generating components, verify:
- **Narrative coherence**: Section connectivity (>=15% concept overlap), no forward references, transition bridges, story arc
- **Timing verification**: Reading speed <=4 words/second, content-density adaptation, data comprehension time
- **Scene type selection**: Correct template for content (DataScene for numbers, KeyPointsScene for lists, QuoteScene for quotes)

If checks fail, block rendering and report errors. See `Workflows/ContentToAnimation.md` for full verification logic and scene templates.

## Integration with Other Skills

### TTS Pipeline
1. Generate narration with OpenAI TTS or ElevenLabs skill
2. Save audio to `public/` directory
3. Use `<Audio src={staticFile("narration.mp3")} />`
4. Use `getAudioDurationInSeconds()` to match video duration

### Veo/Sora Pipeline
1. Generate video clips with Veo or Sora skill
2. Save to `public/`
3. Use `<OffthreadVideo src={staticFile("clip.mp4")} />`

### Nano Banana 2 Pipeline
1. Generate images with Nano Banana 2 skill
2. Save to `public/`
3. Use `<Img src={staticFile("hero.png")} />` with animation

### Remotion Agent Skills
Repository: https://github.com/remotion-dev/remotion/tree/main/packages/skills
Installation: `npx skills add remotion-dev/skills`

## Rules

- Every component is a pure function of `useCurrentFrame()` — no side effects, no state mutations during render
- NO CSS animations — they will not render. Drive all animation from frame number
- NO third-party animation libraries — they cause flickering
- Use `AbsoluteFill` as the root container — it is `position: absolute; inset: 0`
- Use `<Sequence>` for time-based composition — `useCurrentFrame()` resets to 0 inside each Sequence
- Always `extrapolateRight: "clamp"` on `interpolate` — prevents values overshooting
- Use `spring()` for physical animations, `interpolate()` for linear/eased transitions
- Use `OffthreadVideo` (not `Video`) — processes video in a separate thread for better performance
- Use `staticFile()` to reference assets in the `public/` directory
- Set `fps: 30` for general content, `fps: 24` for cinematic feel, `fps: 60` for smooth motion
- For data-driven videos, define a `z.object` schema for Input Props and type safety
- One `<Composition>` per video variant — use `defaultProps` for testable defaults
- Render with `--concurrency 4` (or auto) for faster multi-core rendering
- For long videos (>60s), use `calculateMetadata` to dynamically set duration from audio length
- Keep compositions modular — extract reusable sections (TitleCard, BulletSlide, Outro) as separate components
- Maintain aspect ratio: use actual screen dimensions or scale proportionally
- Preview thoroughly in Remotion Studio before final render
- Optimize assets: compress images appropriately (PNG for UI, JPG for photos)

## Troubleshooting

| Issue | Solution |
|-------|----------|
| **Blurry screenshots** | Ensure downloaded images are at full resolution |
| **Misaligned text** | Verify screen dimensions match composition size |
| **Choppy animations** | Increase frame rate to 60fps; use proper spring configurations |
| **Remotion build fails** | Check Node version compatibility; ensure all dependencies installed |
| **Timing feels off** | Adjust duration per screen in manifest; preview in Remotion Studio |

## Output Format

```
## Remotion Video Report

### Composition: MyVideo
### File: src/compositions/MyVideo.tsx

### Settings
- Resolution: 1920x1080 (1080p)
- FPS: 30
- Duration: 300 frames (10 seconds)
- Codec: h264

### Assets
- Audio: public/narration.mp3
- Video: public/hero-clip.mp4
- Images: public/hero-image.png

### Render Command
npx remotion render src/index.ts MyVideo out/video.mp4

### Next Steps
- Preview in Remotion Studio: npx remotion studio
- Adjust timing and animations
- Add transitions between sequences
- Render final output
```

## When to Use
Use this skill when tackling tasks related to programmatic video creation with React, including app walkthrough videos from Stitch projects, content-to-animation pipelines, course videos, social clips, presentations, or any motion graphics rendered to MP4/WebM/GIF.
