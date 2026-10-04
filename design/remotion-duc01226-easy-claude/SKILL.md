---
name: remotion
version: 3.1.0
description: '[User-Invoked] Use when creating, updating, or previewing Remotion videos.'
disable-model-invocation: true
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting. For simple tasks, ask user whether to skip.
> **MUST ATTENTION** wait for user approval of scene plan (Step 3.3) before writing any files — NEVER skip.
> **MUST ATTENTION** read existing project files before modifying — NEVER overwrite scenes blindly.
> **MUST ATTENTION** update `totalChapters` in ALL existing scene files when adding/removing scenes.

**Be skeptical. Apply critical thinking. Every claim needs traced proof, confidence >80% to act.**

---

## Quick Summary

**Goal:** Create new Remotion video project, add/update scenes in existing one, or launch local Remotion Studio preview server.

**Two Modes:**

| Mode                          | When                                                                | Action                                         |
| ----------------------------- | ------------------------------------------------------------------- | ---------------------------------------------- |
| **Create / Update** (default) | User describes video content OR asks to update/add scenes           | Scaffold new project or modify existing scenes |
| **Play**                      | User says "play", "preview", "open studio", "watch", "start server" | Find Remotion project → `npm run studio`       |

**Default project path:** `remotion/` (relative to workspace root). Respect any path user explicitly provides.

**Key Rules:**

- NEVER implement scenes before user approves the plan (Step 3.3)
- Always read existing project structure before adding/modifying scenes
- Keep `totalChapters` consistent across ALL scene files
- All animations MUST be driven by `useCurrentFrame()` — CSS transitions FORBIDDEN
- Always use Remotion components (`<Img>`, `<Video>`, `<Audio>`) instead of native HTML elements

**Implementing one of these? Copy from `refs/` — do NOT implement from memory:**

| Implementing...                            | Copy from                                                                                                     |
| ------------------------------------------ | ------------------------------------------------------------------------------------------------------------- |
| `{source-root}/components/Shared.tsx` (new scaffold) | `refs/Shared.tsx` — C palette, ProgressBar, ChapterBadge, CodeBlock, Pill, AnimRow                            |
| `{source-root}/utils/animations.ts` (new scaffold)   | `refs/animations.ts` — easeOut, easeInOut, pop, staggeredEaseOut, counter                                     |
| Typewriter or word-highlight text effect   | `refs/text-animations.tsx` — getTypedText, Cursor, TypewriterScene, Highlight                                 |
| TikTok-style captions with word highlight  | `refs/captions.tsx` — CaptionedVideo, CaptionPage, delayRender, createTikTokStyleCaptions                     |
| Video/audio duration, dimensions, frames   | `refs/mediabunny-utils.ts` — getVideoDuration, getAudioDuration, getVideoDimensions, canDecode, extractFrames |
| Mapbox map scene                           | `refs/maps-mapbox.tsx` — MapScene component, interactive:false, camera animation                              |
| ElevenLabs TTS voiceover generation        | `refs/generate-voiceover.ts` — TTS script + calculateMetadata integration                                     |

---

## Phase 0: Mode Detection

Classify prompt:

```
PLAY keywords   → "play", "preview", "open studio", "start server", "watch", "launch", "dev server"
CREATE/UPDATE   → everything else (default)
```

Ambiguous → proceed with **Create/Update** (safe default).

---

## Phase 1A: Detect Existing Project

Locate Remotion project before acting:

```bash
# Check default path
ls remotion/package.json 2>/dev/null

# Check if CWD is already a Remotion project
ls package.json 2>/dev/null | xargs grep -l '"remotion"' 2>/dev/null

# Check common paths
find . -maxdepth 3 -name "package.json" -exec grep -l '"remotion"' {} \; 2>/dev/null | head -5
```

**State after detection:**

- `PROJECT_EXISTS = true/false`
- `PROJECT_PATH = remotion/` (default) or detected path
- `HAS_STUDIO_SCRIPT = true/false` (check `package.json` `scripts.studio`)

---

## Phase 2: PLAY Mode

**When:** User explicitly asks to preview / open studio / launch dev server.

### Step 2.1 — Verify project exists

If `PROJECT_EXISTS = false`:

> "No Remotion project found. Run `/remotion <description>` to create one first."
> Exit.

### Step 2.2 — Find launch command

```bash
cat {PROJECT_PATH}/package.json | grep '"studio"'
# → use: npm run studio
# → fallback: npx remotion studio
```

### Step 2.3 — Start dev server (background)

```bash
cd {PROJECT_PATH} && npm run studio
```

> Remotion Studio launches at **http://localhost:3000**

Server runs in background. Report URL and composition IDs visible in `{source-root}/Root.tsx`.

### Step 2.4 — Optional: one-frame render check

```bash
npx remotion still [composition-id] --scale=0.25 --frame=30
# At 30fps, --frame=30 = one-second mark (zero-based)
```

---

## Phase 3: CREATE / UPDATE Mode

### Step 3.1 — New vs Update Decision

| Condition                | Action                                |
| ------------------------ | ------------------------------------- |
| `PROJECT_EXISTS = false` | **Scaffold** new project → Phase 3.2  |
| `PROJECT_EXISTS = true`  | **Read existing** project → Phase 3.4 |

---

### Step 3.2 — Scaffold New Project

**Only when no existing Remotion project found.**

#### 3.2.1 Bootstrap with create-video (preferred)

```bash
# Creates {PROJECT_PATH}/ with blank template (no Tailwind)
npx create-video@latest --yes --blank --no-tailwind {PROJECT_PATH}
cd {PROJECT_PATH}
npm install @remotion/transitions  # add transitions support
```

Replace generated `{source-root}/` with project structure below (keep `package.json` and `tsconfig.json` from scaffold).

#### Fallback (manual) — when `npx create-video` unavailable

```bash
mkdir -p {PROJECT_PATH}/{source-root}/compositions {PROJECT_PATH}/{source-root}/components {PROJECT_PATH}/{source-root}/utils
cd {PROJECT_PATH}
npm init -y
npm install remotion @remotion/cli @remotion/transitions react react-dom
npm install -D @types/react @types/react-dom typescript
```

#### Directory structure (both paths)

```
{PROJECT_PATH}/
  package.json          ← scripts: studio, render, still
  tsconfig.json
  {source-root}/
    index.ts            ← registerRoot
    Root.tsx            ← register compositions
    components/
      Shared.tsx        ← palette + reusable UI components
    utils/
      animations.ts     ← easeOut, staggeredEaseOut, pop, counter
    compositions/
      {CompositionName}.tsx
```

#### 3.2.3 Create `package.json` scripts (merge into existing after install)

```json
{
    "scripts": {
        "studio": "remotion studio",
        "render": "remotion render {CompositionId} out/video.mp4",
        "still": "remotion still {CompositionId} --frame=0 out/still.png"
    },
    "remotion": {
        "entryPoint": "{source-root}/index.ts"
    }
}
```

#### 3.2.4 Create `tsconfig.json`

```json
{
    "compilerOptions": {
        "target": "ES2020",
        "lib": ["dom", "ES2020"],
        "jsx": "react-jsx",
        "module": "commonjs",
        "moduleResolution": "node",
        "strict": true,
        "esModuleInterop": true,
        "skipLibCheck": true,
        "outDir": "dist"
    },
    "include": ["src"]
}
```

#### 3.2.5 Create `{source-root}/index.ts`

```ts
import { registerRoot } from 'remotion';
import { Root } from './Root';
registerRoot(Root);
```

#### 3.2.6 Create `{source-root}/components/Shared.tsx`

> Copy from `refs/Shared.tsx` — do NOT implement from memory. Exports: `C` (palette), `ProgressBar`, `ChapterBadge`, `CodeBlock`, `Pill`, `AnimRow`. Always create; all scenes import from here.

#### 3.2.7 Create `{source-root}/utils/animations.ts`

> Copy from `refs/animations.ts` — do NOT implement from memory. Exports: `easeOut`, `easeInOut`, `pop`, `staggeredEaseOut`, `counter`.

---

### Step 3.3 — Plan Composition Structure

**MUST ATTENTION wait for user confirmation before implementing any scenes.**

Plan composition before writing files:

1. **Parse intent** — What video about? What information to convey?
2. **Decide scene count** — 1 scene per major concept (30s → ~4 scenes, 60s → ~8, 90s → ~12)
3. **Assign durations** — Each scene: 6–12s (180–360 frames @ 30fps)
4. **Name scenes** — `Scene01Intro`, `Scene02{Topic}`, etc.
5. **Write scene brief** — what shown, key data, visual layout (left/right split, full-width, grid)

Present plan before writing files:

```
Proposed: {N} scenes, ~{total}s total
  Scene 01 ({Xs}) — {topic}: {layout description}
  Scene 02 ({Xs}) — {topic}: {layout description}
  …
Proceed? (or adjust)
```

---

### Step 3.4 — Read Existing Project (UPDATE path)

**MUST ATTENTION read existing project state before any modifications.**

When `PROJECT_EXISTS = true`:

```bash
# Read composition registry
cat {PROJECT_PATH}/{source-root}/Root.tsx

# List scene files
ls {PROJECT_PATH}/{source-root}/compositions/ 2>/dev/null || ls {PROJECT_PATH}/{source-root}/scenes/ 2>/dev/null

# Read main composition orchestrator
cat {PROJECT_PATH}/{source-root}/ClaudeAgentExplainer.tsx 2>/dev/null  # or equivalent
```

Identify:

- Existing scene count and names
- Current `totalChapters` / composition duration
- Where to insert / which scenes to modify

Target only scenes affected by user's request. Preserve all unchanged scenes.

---

### Step 3.5 — Implement Scene Files

#### Scene file anatomy (follow exactly)

```tsx
import { AbsoluteFill, useCurrentFrame, interpolate } from 'remotion';
import { C, ProgressBar, ChapterBadge } from '../components/Shared';  // adjust path
import { easeOut, staggeredEaseOut } from '../utils/animations';       // adjust path

// Data arrays at the top — keep out of component body
const ITEMS = [ ... ];

export const Scene{NN}{Name}: React.FC = () => {
    const frame = useCurrentFrame();

    return (
        <AbsoluteFill style={{ background: C.bg, fontFamily: 'system-ui, -apple-system, sans-serif' }}>
            <ChapterBadge index={NN} label="{Scene Name}" color={C.blue} />

            <div style={{ position: 'absolute', inset: 0, display: 'flex', gap: 48, padding: '68px 72px 44px' }}>
                {/* Content here */}
            </div>

            <ProgressBar chapterIndex={NN - 1} totalChapters={TOTAL} />
        </AbsoluteFill>
    );
};
```

#### Animation rules

| Element               | Pattern                                                   |
| --------------------- | --------------------------------------------------------- |
| Eyebrow label         | `opacity: easeOut(frame, 0, 14)`                          |
| Hero title            | `opacity: easeOut(frame, 8, 22)` + `translateY` from 28→0 |
| Subtitle              | `opacity: easeOut(frame, 22, 18)`                         |
| List items (stagger)  | `staggeredEaseOut(frame, i, startAt, 12, 16)`             |
| Cards (stagger up)    | `staggeredEaseOut` + `translateY(20→0)`                   |
| Cards (stagger right) | `staggeredEaseOut` + `translateX(28→0)`                   |
| Late callout boxes    | `easeOut(frame, 90+, 18)`                                 |

#### Layout patterns

**Left/Right split (most common):**

```tsx
<div style={{ position: 'absolute', inset: 0, display: 'flex', gap: 48, padding: '68px 72px 44px' }}>
    <div style={{ width: 400, flexShrink: 0, ... }}>  {/* Left panel */}
    <div style={{ flex: 1, ... }}>                     {/* Right panel */}
</div>
```

**Full-width column:**

```tsx
<div style={{ position: 'absolute', inset: 0, display: 'flex', flexDirection: 'column', padding: '68px 64px 44px', gap: 16 }}>
```

**Centered (title/CTA scene):**

```tsx
<div style={{ position: 'absolute', inset: 0, display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', padding: '72px 100px', textAlign: 'center' }}>
```

**Card grid:**

```tsx
<div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 12 }}>
```

#### Color and font guidelines

| Element          | fontSize | fontWeight | Notes                                                             |
| ---------------- | -------- | ---------- | ----------------------------------------------------------------- |
| Eyebrow label    | 14       | 700        | category color, `letterSpacing: 3`                                |
| Hero title       | 44–56    | 800        | `C.text`, `lineHeight: 1.1`                                       |
| Body text        | 17–21    | 400        | `C.dim`, `lineHeight: 1.6`                                        |
| Card label       | 15–16    | 700        | category color                                                    |
| Monospace detail | 12–14    | 400        | `fontFamily: 'Courier New'`                                       |
| Card container   | —        | —          | `C.surface`, `borderLeft: 3px solid color`, `borderRadius: 10–12` |

---

### Step 3.6 — Wire Root.tsx

#### Multi-scene composition (with transitions)

```tsx
import { TransitionSeries, linearTiming } from '@remotion/transitions';
import { fade } from '@remotion/transitions/fade';
import { Scene01Intro } from './compositions/Scene01Intro';
// ... other imports

const T = 18; // transition duration in frames

const D = {
    s01: 210, // 7s
    s02: 240 // 8s
    // ...
};

const SCENES = Object.values(D).length;
export const TOTAL_DURATION_FRAMES = Object.values(D).reduce((a, b) => a + b, 0) - (SCENES - 1) * T;

const tr = () => <TransitionSeries.Transition presentation={fade()} timing={linearTiming({ durationInFrames: T })} />;

export const {
    CompositionName
}: React.FC = () => (
    <TransitionSeries>
        <TransitionSeries.Sequence durationInFrames={D.s01}>
            <Scene01Intro />
        </TransitionSeries.Sequence>
        {tr()}
        <TransitionSeries.Sequence durationInFrames={D.s02}>
            <Scene02Next />
        </TransitionSeries.Sequence>
        {/* ... */}
    </TransitionSeries>
);
```

```tsx
// Root.tsx
import { Composition } from 'remotion';
import { {CompositionName}, TOTAL_DURATION_FRAMES } from './{CompositionName}';

export const Root: React.FC = () => (
    <Composition id="{CompositionId}" component={{{CompositionName}}} durationInFrames={TOTAL_DURATION_FRAMES} fps={30} width={1920} height={1080} />
);
```

#### Single-scene composition

```tsx
// Root.tsx
import { Composition } from 'remotion';
import { MyScene } from './compositions/MyScene';

export const Root: React.FC = () => <Composition id="MyVideo" component={MyScene} durationInFrames={300} fps={30} width={1920} height={1080} />;
```

---

### Step 3.7 — Post-scaffold: launch prompt

After creating/updating, report changed files and offer launch:

```
✅ Created {N} scene files in {PROJECT_PATH}/{source-root}/compositions/
   Total duration: ~{X}s ({FRAMES} frames @ 30fps)

To preview: run `/remotion play` — starts Remotion Studio at http://localhost:3000
To render:  cd {PROJECT_PATH} && npm run render
```

---

## Update Mode: Specific Scenarios

### Add a new scene

1. Read `Root.tsx` to find composition orchestrator and current scene count
2. Read `totalChapters` across existing scenes
3. Determine insertion point (end = safest)
4. Create new scene file following anatomy above
5. Update Root / composition orchestrator:
    - Add import
    - Add `D.sNN` entry
    - Add `<TransitionSeries.Sequence>` block
    - **MUST ATTENTION update `totalChapters` in ALL existing scene files (+1)**

### Modify an existing scene

1. Read specific scene file
2. Identify data array or JSX block needing change
3. Make surgical edits only — do not touch unrelated sections

### Change visual style / palette

1. Edit `{source-root}/components/Shared.tsx` → `C` object
2. Font changes: update `fontFamily` in `AbsoluteFill` style per scene (or add global in Shared)

---

## Remotion API Reference

> Authoritative Remotion API reference — apply when implementing beyond basic scene creation.

---

### Animations (Core Rules)

**MUST ATTENTION** ALL animations driven by `useCurrentFrame()`. Durations: seconds × `fps`.

```tsx
import { useCurrentFrame, useVideoConfig, interpolate, Easing } from 'remotion';

export const FadeIn = () => {
    const frame = useCurrentFrame();
    const { fps } = useVideoConfig();
    const opacity = interpolate(frame, [0, 2 * fps], [0, 1], {
        extrapolateRight: 'clamp',
        extrapolateLeft: 'clamp',
        easing: Easing.bezier(0.16, 1, 0.3, 1)
    });
    return <div style={{ opacity }}>Hello World!</div>;
};
```

**FORBIDDEN:** CSS `transition-*`, CSS `animation-*`, Tailwind `transition-*`/`animate-*` classes.

---

### Timing — interpolate & Bézier Easing

```ts
// With clamping + Bézier easing
const opacity = interpolate(frame, [0, 60], [0, 1], {
    easing: Easing.bezier(0.16, 1, 0.3, 1),
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp'
});
```

**Copy-paste curves:**

```tsx
easing: Easing.bezier(0.16, 1, 0.3, 1); // crisp UI entrance (strong ease-out)
easing: Easing.bezier(0.45, 0, 0.55, 1); // editorial / slow fade
easing: Easing.bezier(0.34, 1.56, 0.64, 1); // playful overshoot
```

**Composing multiple properties from one progress:**

```tsx
const slideIn = interpolate(frame, [start, start + dur], [0, 1], {
    easing: Easing.bezier(0.22, 1, 0.36, 1),
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp'
});
const overlayX = interpolate(slideIn, [0, 1], [100, 0]);
const opacity = interpolate(slideIn, [0, 1], [0, 1]);
```

---

### Sequencing & Trimming

**`<Sequence>`** delays element appearance. `useCurrentFrame()` inside = local frame (0-based). Always `premountFor`:

```tsx
<Sequence from={1 * fps} durationInFrames={2 * fps} premountFor={1 * fps}>
    <Title />
</Sequence>
```

**`<Series>`** for sequential without overlap:

```tsx
<Series>
    <Series.Sequence durationInFrames={45}>
        <Intro />
    </Series.Sequence>
    <Series.Sequence durationInFrames={60}>
        <MainContent />
    </Series.Sequence>
    <Series.Sequence offset={-15} durationInFrames={60}>
        <SceneB />
    </Series.Sequence>{' '}
    {/* overlap */}
</Series>
```

**Trimming:**

```tsx
<Sequence from={-0.5 * fps}><MyAnimation /></Sequence>       // skip first 15 frames
<Sequence durationInFrames={1.5 * fps}><MyAnimation /></Sequence>  // trim end
<Sequence from={30}><Sequence from={-15}><MyAnimation /></Sequence></Sequence>  // trim + delay
```

---

### Compositions

```tsx
import { Composition, Folder, Still } from "remotion";

<Composition id="MyComposition" component={MyComp} durationInFrames={100} fps={30} width={1080} height={1080} />

// With default props (use `type` not `interface`)
<Composition id="MyComposition" component={MyComp} durationInFrames={100} fps={30} width={1080} height={1080}
  defaultProps={{ title: "Hello World", color: "#ff0000" } satisfies MyCompositionProps}
/>

// Still (single-frame)
<Still id="Thumbnail" component={Thumbnail} width={1280} height={720} />
```

---

### Assets — staticFile() & public folder

**MUST use `staticFile()`** for assets in `public/`:

```tsx
import { Img, staticFile } from "remotion";
import { Video } from "@remotion/media";
import { Audio } from "@remotion/media";

<Img src={staticFile("logo.png")} />
<Video src={staticFile("clip.mp4")} />
<Audio src={staticFile("music.mp3")} />
// Remote URLs work directly — no staticFile needed
```

---

### Images

**MUST use `<Img>` from `remotion`** — NOT `<img>`, NOT Next.js `<Image>`, NOT CSS `background-image`.

```tsx
import { Img, staticFile } from "remotion";

<Img src={staticFile("photo.png")} style={{ width: 500, height: 300, objectFit: "cover" }} />
<Img src={staticFile(`frames/frame${frame}.png`)} />  // dynamic paths work
```

---

### Videos

Install: `npx remotion add @remotion/media`

```tsx
import { Video } from "@remotion/media";

<Video src={staticFile("video.mp4")} />
<Video src={staticFile("video.mp4")} trimBefore={2 * fps} trimAfter={10 * fps} />
<Video src={staticFile("video.mp4")} volume={(f) => interpolate(f, [0, fps], [0, 1], { extrapolateRight: "clamp" })} />
<Video src={staticFile("video.mp4")} playbackRate={2} loop muted />
```

---

### Audio

Install: `npx remotion add @remotion/media`

```tsx
import { Audio } from "@remotion/media";

<Audio src={staticFile("audio.mp3")} />
<Audio src={staticFile("audio.mp3")} trimBefore={2 * fps} trimAfter={10 * fps} />
<Sequence from={1 * fps}><Audio src={staticFile("audio.mp3")} /></Sequence>  // delay
// volume callback: `f` starts at 0 when audio begins, not composition frame
<Audio src={staticFile("audio.mp3")} volume={(f) => interpolate(f, [0, fps], [0, 1], { extrapolateRight: "clamp" })} />
```

---

### GIFs & Animated Images

```tsx
import { AnimatedImage, staticFile } from "remotion";

// Preferred: supports GIF, APNG, AVIF, WebP
<AnimatedImage src={staticFile("animation.gif")} width={500} height={500} />
<AnimatedImage src={staticFile("animation.gif")} width={500} height={300} fit="cover" playbackRate={2} />

// Fallback: GIF only — npx remotion add @remotion/gif
import { Gif } from "@remotion/gif";
<Gif src={staticFile("animation.gif")} width={500} height={500} />
```

---

### Fonts

**Google Fonts (recommended):** `npx remotion add @remotion/google-fonts`

```tsx
import { loadFont } from '@remotion/google-fonts/Roboto';

const { fontFamily } = loadFont('normal', { weights: ['400', '700'], subsets: ['latin'] });
<h1 style={{ fontFamily, fontSize: 80, fontWeight: 'bold' }}>{text}</h1>;
```

**Local fonts:** `npx remotion add @remotion/fonts`

```tsx
import { loadFont } from '@remotion/fonts';
import { staticFile } from 'remotion';

await Promise.all([
    loadFont({ family: 'Inter', url: staticFile('Inter-Regular.woff2'), weight: '400' }),
    loadFont({ family: 'Inter', url: staticFile('Inter-Bold.woff2'), weight: '700' })
]);
```

---

### Transitions (Full API)

`npx remotion add @remotion/transitions`

```tsx
import { TransitionSeries, linearTiming, springTiming } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";
import { slide } from "@remotion/transitions/slide";
import { wipe } from "@remotion/transitions/wipe";
import { flip } from "@remotion/transitions/flip";

<TransitionSeries>
  <TransitionSeries.Sequence durationInFrames={60}><SceneA /></TransitionSeries.Sequence>
  <TransitionSeries.Transition presentation={fade()} timing={linearTiming({ durationInFrames: 15 })} />
  <TransitionSeries.Sequence durationInFrames={60}><SceneB /></TransitionSeries.Sequence>
</TransitionSeries>

// Slide directions: "from-left" | "from-right" | "from-top" | "from-bottom"
<TransitionSeries.Transition presentation={slide({ direction: "from-left" })} timing={linearTiming({ durationInFrames: 20 })} />

// Spring timing
springTiming({ config: { damping: 200 }, durationInFrames: 25 })

// Overlay (no duration shortening — note: cannot be adjacent to transition or another overlay)
<TransitionSeries.Overlay durationInFrames={20} offset={0}><MyEffect /></TransitionSeries.Overlay>
```

**Duration:** two 60-frame scenes + 15-frame transition = `60 + 60 - 15 = 105` frames total.

---

### Light Leaks (Overlay Effect)

Requires Remotion ≥ 4.0.415. Check: `npx remotion versions`. Upgrade: `npx remotion upgrade`.

`npx remotion add @remotion/light-leaks`

```tsx
import { LightLeak } from "@remotion/light-leaks";

// As TransitionSeries overlay
<TransitionSeries.Overlay durationInFrames={30}><LightLeak /></TransitionSeries.Overlay>

// Standalone decorative overlay
<AbsoluteFill>
  <MyContent />
  <LightLeak durationInFrames={60} seed={3} />
</AbsoluteFill>

// seed: different patterns; hueShift: 0=yellow-orange, 120=green, 240=blue
<LightLeak seed={5} hueShift={240} />
```

---

### 3D with Three.js (React Three Fiber)

`npx remotion add @remotion/three`

**MUST wrap in `<ThreeCanvas>` with `width` and `height` props.**
**FORBIDDEN: `useFrame()` from `@react-three/fiber`** — causes flickering. Use `useCurrentFrame()`.

```tsx
import { ThreeCanvas } from '@remotion/three';
import { useVideoConfig, useCurrentFrame } from 'remotion';

const { width, height } = useVideoConfig();
const frame = useCurrentFrame();

<ThreeCanvas width={width} height={height}>
    <ambientLight intensity={0.4} />
    <directionalLight position={[5, 5, 5]} intensity={0.8} />
    <mesh rotation={[0, frame * 0.02, 0]}>
        <boxGeometry args={[2, 2, 2]} />
        <meshStandardMaterial color="#4a9eff" />
    </mesh>
</ThreeCanvas>;

// <Sequence> inside ThreeCanvas must use layout="none"
```

---

### Text Animations

All text animations driven by `useCurrentFrame()`. CSS transitions FORBIDDEN.

**Typewriter** — use string slicing, NEVER per-character opacity. Spring **word highlight** — scaleX wipe from left.

> Implementing typewriter or word-highlight? Copy from `refs/text-animations.tsx` — do NOT implement from memory. Contains: `getTypedText`, `Cursor`, `TypewriterScene`, `Highlight`.

---

### Text Measurement

`npx remotion add @remotion/layout-utils`

```tsx
import { measureText, fitText, fillTextBox } from '@remotion/layout-utils';

const { width, height } = measureText({ text: 'Hello World', fontFamily: 'Arial', fontSize: 32, fontWeight: 'bold' });
const { fontSize } = fitText({ text: 'Hello World', withinWidth: 600, fontFamily: 'Inter', fontWeight: 'bold' });
```

**MUST ATTENTION** call only after fonts loaded. Use `validateFontIsLoaded: true`. Match font properties exactly between measurement and rendering.

---

### DOM Node Measurement

Remotion applies `scale()` transform — use `useCurrentScale()` to get true dimensions:

```tsx
import { useCurrentScale } from 'remotion';

const scale = useCurrentScale();
const rect = ref.current.getBoundingClientRect();
const trueWidth = rect.width / scale;
```

---

### Captions & Subtitles

`npx remotion add @remotion/captions`

Caption type: `{ text, startMs, endMs, timestampMs, confidence }`

**Transcribe with Whisper.cpp:** `npx remotion add @remotion/install-whisper-cpp`

```ts
import { installWhisperCpp, downloadWhisperModel, transcribe, toCaptions } from '@remotion/install-whisper-cpp';

await installWhisperCpp({ to: './whisper.cpp', version: '1.5.5' });
await downloadWhisperModel({ model: 'medium.en', folder: './whisper.cpp' });
// Convert to 16KHz wav first: npx remotion ffmpeg -i input.mp4 -ar 16000 output.wav
const whisperOutput = await transcribe({
    model: 'medium.en',
    whisperPath: './whisper.cpp',
    whisperCppVersion: '1.5.5',
    inputPath: '/path/to/audio.wav',
    tokenLevelTimestamps: true
});
const { captions } = toCaptions({ whisperCppOutput: whisperOutput });
```

**Import from.srt:**

```tsx
import { parseSrt } from '@remotion/captions';
const { captions } = parseSrt({ input: await fetch(staticFile('subtitles.srt')).then(r => r.text()) });
```

**TikTok-style word highlight display:**

> Implementing TikTok-style captions? Copy from `refs/captions.tsx` — do NOT implement from memory. Contains: `CaptionedVideo`, `CaptionPage`, `delayRender`, `createTikTokStyleCaptions`, per-token active highlighting.

Note: use `whiteSpace: "pre"` — captions are whitespace-sensitive.

---

### Dynamic Compositions — calculateMetadata

```tsx
import { CalculateMetadataFunction } from 'remotion';

const calculateMetadata: CalculateMetadataFunction<Props> = async ({ props, abortSignal }) => {
    const durationInSeconds = await getVideoDuration(props.videoSrc);
    return { durationInFrames: Math.ceil(durationInSeconds * 30) };
};

// Transform props (fetch data before render)
const calculateMetadata: CalculateMetadataFunction<Props> = async ({ props, abortSignal }) => {
    const data = await fetch(props.dataUrl, { signal: abortSignal }).then(r => r.json());
    return { props: { ...props, fetchedData: data } };
};

// Return values (all optional): durationInFrames, width, height, fps, props, defaultOutName, defaultCodec
```

---

### Parameters — Zod Schema

```tsx
import { z } from 'zod';
import { zColor } from '@remotion/zod-types';

export const MyCompositionSchema = z.object({
    title: z.string(),
    color: zColor() // renders color picker in Studio
});

// Root.tsx
<Composition
    id="MyComposition"
    component={MyComponent}
    schema={MyCompositionSchema}
    durationInFrames={100}
    fps={30}
    width={1080}
    height={1080}
    defaultProps={{ title: 'Hello World', color: '#ff0000' }}
/>;
```

Top-level type MUST be `z.object()`.

---

### Mediabunny — Video/Audio Metadata

`npx remotion add mediabunny`

> Need video/audio duration, dimensions, or frame extraction? Copy from `refs/mediabunny-utils.ts` — do NOT implement from memory. Contains: `getVideoDuration`, `getAudioDuration`, `getVideoDimensions`, `canDecode`, `extractFrames`.

Use `staticFile()` for local files. Use `FileSource` instead of `UrlSource` in Node.js/Bun.

---

### FFmpeg in Remotion

```bash
npx remotion ffmpeg -i input.mp4 output.mp3
npx remotion ffprobe input.mp4
```

**Trimming — prefer `<Video>` props (non-destructive, no re-encoding):**

```tsx
<Video src={staticFile('video.mp4')} trimBefore={5 * fps} trimAfter={10 * fps} />

// FFmpeg fallback (MUST re-encode to avoid frozen frames)
// npx remotion ffmpeg -ss 00:00:05 -i public/input.mp4 -to 00:00:10 -c:v libx264 -c:a aac public/output.mp4
```

---

### Silence Detection

```bash
# Step 1: measure loudness
npx remotion ffmpeg -i public/video.mov -map 0:a -af loudnorm=print_format=json -f null /dev/null
# → read input_i (integrated loudness dB) and input_thresh

# Step 2: detect silences (d=0.5 = min silence duration in seconds)
npx remotion ffmpeg -i public/video.mov -map 0:a -af "silencedetect=noise=${THRESH}dB:d=0.5" -f null /dev/null
```

```tsx
<Video src={staticFile('video.mov')} trimBefore={Math.floor(leadingEnd * fps)} trimAfter={Math.ceil(trailingStart * fps)} />
```

---

### Audio Visualization

`npx remotion add @remotion/media-utils`

```tsx
import { useWindowedAudioData, visualizeAudio, visualizeAudioWaveform, createSmoothSvgPath } from '@remotion/media-utils';

const { audioData, dataOffsetInSeconds } = useWindowedAudioData({ src: staticFile('music.mp3'), frame, fps, windowInSeconds: 30 });
if (!audioData) return null;

// Spectrum bars (numberOfSamples must be power of 2)
const frequencies = visualizeAudio({ fps, frame, audioData, numberOfSamples: 256, optimizeFor: 'speed', dataOffsetInSeconds });
// Values 0-1; left=bass, right=highs

// Waveform SVG
const waveform = visualizeAudioWaveform({ fps, frame, audioData, numberOfSamples: 256, windowInSeconds: 0.5, dataOffsetInSeconds });
const path = createSmoothSvgPath({ points: waveform.map((y, i) => ({ x: (i / (waveform.length - 1)) * width, y: 100 + y * 100 })) });

// Bass-reactive scale
const bassIntensity = frequencies.slice(0, 32).reduce((sum, v) => sum + v, 0) / 32;
const scale = 1 + bassIntensity * 0.5;
```

**MUST ATTENTION** pass `frame` from parent to child visualization — NEVER call `useCurrentFrame()` in each child inside `<Sequence>`.

Logarithmic scaling: `const db = 20 * Math.log10(value); const scaled = (db - (-100)) / ((-30) - (-100));`

---

### Lottie Animations

`npx remotion add @remotion/lottie`

```tsx
import { Lottie, LottieAnimationData } from '@remotion/lottie';
import { cancelRender, continueRender, delayRender } from 'remotion';

export const MyAnimation = () => {
    const [handle] = useState(() => delayRender('Loading Lottie animation'));
    const [animationData, setAnimationData] = useState<LottieAnimationData | null>(null);

    useEffect(() => {
        fetch('https://assets4.lottiefiles.com/packages/lf20_zyquagfl.json')
            .then(r => r.json())
            .then(json => {
                setAnimationData(json);
                continueRender(handle);
            })
            .catch(err => {
                cancelRender(err);
            });
    }, [handle]);

    if (!animationData) return null;
    return <Lottie animationData={animationData} style={{ width: 400, height: 400 }} />;
};
```

---

### Charts & Data Visualization

**MUST ATTENTION** drive all animations from `useCurrentFrame()`. Disable all third-party chart library animations.

```tsx
import { spring, evolvePath, getLength, getPointAtLength, getTangentAtLength } from '@remotion/paths';

// Bar chart — spring stagger
const bars = data.map((item, i) => {
    const height = spring({ frame, fps, delay: i * 5, config: { damping: 200 } });
    return <div style={{ height: height * item.value }} />;
});

// Line chart path animation (npx remotion add @remotion/paths)
const pathProgress = interpolate(frame, [0, 2 * fps], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
const { strokeDasharray, strokeDashoffset } = evolvePath(pathProgress, svgPath);
<path d={svgPath} fill="none" stroke="#FF3232" strokeWidth={4} strokeDasharray={strokeDasharray} strokeDashoffset={strokeDashoffset} />;
```

---

### Maps with Mapbox

`npm i mapbox-gl @turf/turf @types/mapbox-gl` — set `REMOTION_MAPBOX_TOKEN` in `.env`.

> Implementing Mapbox map scene? Copy from `refs/maps-mapbox.tsx` — do NOT implement from memory. Key rules: `interactive: false`, `fadeDuration: 0`, explicit `width`/`height`/`position: "absolute"` on container, animate camera via `useCurrentFrame()`, NO cleanup (`_map.remove()`). Render: `npx remotion render --gl=angle --concurrency=1`.

---

### Transparent Video Rendering

```bash
# ProRes (for video editors)
npx remotion render --image-format=png --pixel-format=yuva444p10le --codec=prores --prores-profile=4444 MyComp out.mov

# WebM VP9 (for browsers)
npx remotion render --image-format=png --pixel-format=yuva420p --codec=vp9 MyComp out.webm
```

---

### AI Voiceover (ElevenLabs TTS)

> Implementing ElevenLabs TTS voiceover? Copy from `refs/generate-voiceover.ts` — do NOT implement from memory. Includes `calculateMetadata` integration to size composition to audio duration.

---

### Sound Effects

```tsx
import { Audio } from '@remotion/sfx';
<Audio src={'https://remotion.media/whoosh.wav'} />;
```

Available: `whoosh`, `whip`, `page-turn`, `switch`, `mouse-click`, `shutter-modern`, `shutter-old`, `ding`, `bruh`, `vine-boom`, `windows-xp-error` — all at `https://remotion.media/{name}.wav`

---

### TailwindCSS

Use if installed. NEVER use `transition-*` or `animate-*` Tailwind classes — animate via `useCurrentFrame()`.

---

## Closing Reminders

**Protocols in force (concise digest of the SYNC/shared blocks this skill carries):**


- **MUST ATTENTION** wait for user approval of scene plan (Step 3.3) — NEVER implement scenes before approval
- **MUST ATTENTION** read existing project structure (Step 3.4) before modifications — NEVER overwrite blindly
- **MUST ATTENTION** update `totalChapters` in ALL scene files when adding/removing scenes — one missed file causes visual regression
- **MUST ATTENTION** keep data arrays outside component body — NEVER define `const ITEMS` inside component function
- **MUST ATTENTION** use `npx create-video@latest --yes --blank --no-tailwind` for scaffold — NEVER `npm init` unless fallback needed
- **MUST ATTENTION** use `staggeredEaseOut` for list/card reveals — NEVER all-at-once opacity
- **MUST ATTENTION** verify `PROJECT_EXISTS` before Play mode — report missing project and exit
- **MUST ATTENTION** use TaskCreate to plan ALL work before starting — mark each task done immediately
- **MUST ATTENTION** ALL animations driven by `useCurrentFrame()` — CSS transitions, CSS animations, Tailwind animate/transition classes FORBIDDEN
- **MUST ATTENTION** use Remotion components `<Img>`, `<Video>`, `<Audio>` — NEVER native HTML elements
- **MUST ATTENTION** use `staticFile()` for all public/ folder assets — NEVER raw relative paths
- **MUST ATTENTION** Copy from appropriate `refs/` file — NEVER implement text animations, captions, mediabunny, maps, or voiceover from memory
