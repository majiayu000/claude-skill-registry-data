---
type: Skill
name: remotion
description: Create programmatic videos using React and Remotion. Translate natural language descriptions into working Remotion components for product demos, release announcements, explainer videos, and animated content.
license: MIT
compatibility: Claude Code, Cursor, Gemini CLI, Codex CLI
---

# Remotion

Generate React-based video components using the Remotion framework. Use this skill when a user needs a video, animation, or motion graphic produced programmatically without a separate video editing tool.

## What This Skill Covers

- Product demo videos
- Release announcement animations
- Explainer videos with animated text and diagrams
- Animated README headers / GIFs
- Data visualisation motion graphics
- Slide-based presentations rendered to MP4

## Prerequisites

```bash
# Create a new Remotion project
npm create video@latest

# Or add Remotion to an existing React project
npm install remotion @remotion/player @remotion/cli
```

Install the agent skill:

```bash
npx skills add remotion/agent-skills
```

## Core Concepts

### Frame-driven animation

Remotion videos are React components. Animation is just state changing over time via `useCurrentFrame()`.

```tsx
import { AbsoluteFill, useCurrentFrame, interpolate } from 'remotion';

export const MyScene = () => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 30], [0, 1], {
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill style={{ backgroundColor: '#0a0a0a', opacity }}>
      <h1 style={{ color: 'white', fontSize: 72 }}>Hello, World</h1>
    </AbsoluteFill>
  );
};
```

### Composition (defines the video)

```tsx
import { Composition } from 'remotion';
import { MyScene } from './MyScene';

export const RemotionRoot = () => (
  <Composition
    id="MyVideo"
    component={MyScene}
    durationInFrames={150}   // 5 seconds at 30fps
    fps={30}
    width={1920}
    height={1080}
  />
);
```

### Timing helpers

```tsx
const { fps } = useVideoConfig();
const frame = useCurrentFrame();

// Enter at 1 second, exit at 3 seconds
const opacity = interpolate(
  frame,
  [fps * 1, fps * 1 + 30, fps * 3, fps * 3 + 30],
  [0, 1, 1, 0],
  { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
);
```

## Standard Workflow

```
User: "Create a 30-second product demo video for our API dashboard"

Steps:
1. Confirm video dimensions (default: 1920×1080), fps (default: 30), duration
2. Plan scenes: intro → feature highlight → call to action
3. Generate Remotion composition + scene components
4. Preview: npx remotion studio
5. Render: npx remotion render
```

## Common Patterns

### Fade-in text

```tsx
const frame = useCurrentFrame();
const opacity = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: 'clamp' });
<div style={{ opacity }}>{text}</div>
```

### Slide in from left

```tsx
const translateX = interpolate(frame, [0, 25], [-200, 0], { extrapolateRight: 'clamp' });
<div style={{ transform: `translateX(${translateX}px)` }}>{content}</div>
```

### Sequence (time-shifted scenes)

```tsx
import { Sequence } from 'remotion';

<Sequence from={0} durationInFrames={60}>  <IntroScene /> </Sequence>
<Sequence from={60} durationInFrames={90}> <FeatureScene /> </Sequence>
<Sequence from={150} durationInFrames={45}><OutroScene /> </Sequence>
```

## Output Formats

```bash
# Preview in browser
npx remotion studio

# Render to MP4
npx remotion render src/index.ts MyVideo out/video.mp4

# Render to GIF
npx remotion render src/index.ts MyVideo out/video.gif --codec=gif

# Render specific frame range
npx remotion render src/index.ts MyVideo out/video.mp4 --frames=0-90
```

## Tips

- Keep each scene in its own component file for maintainability
- Use `spring()` from Remotion for natural-feeling physics-based animations
- Test frame ranges with `--frames` flag before full renders
- Brand colours and fonts belong in a shared `theme.ts` constants file
- Add `--log=verbose` when debugging render failures
