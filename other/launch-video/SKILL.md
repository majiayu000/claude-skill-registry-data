---
name: launch-video
category: video
description: "Produce polished product launch videos using the Liquid Glass aesthetic — dark void backgrounds, 3D perspective floating UI panels, particle effects, spring animations, and cinematic pacing. Built on Remotion with Imagen 4.0 for frames and Veo 3.1 for B-roll. Use when: (1) creating a product demo or launch video, (2) showcasing a UI/app/tool with cinematic polish, (3) building a social-ready video from screenshots and renders, (4) applying the liquid glass floating panel style, (5) composing Remotion videos with 3D transforms and spring animations. Triggers on: 'launch video', 'product video', 'liquid glass video', 'demo video', 'showcase video', 'remotion video', 'floating panel', 'glass aesthetic'."
---

# Launch Video — Liquid Glass Product Showcase

Produce cinematic product launch videos using the Liquid Glass aesthetic: dark void, 3D floating panels, particle effects, spring animations, and confident pacing.

## Compounding Skills

| Skill | Role |
|-------|------|
| `/remotion-best-practices` | Composition structure, `spring()`, `<Sequence>`, render pipeline |
| `/content-creation` | AI asset generation (Imagen 4.0, Veo 3.1) |
| `/arcan-glass` | BroomVA brand tokens (AI Blue, dark-first palette) |
| `/google-veo` | Cinematic B-roll generation prompts |
| `/blog-post` | Distribution pipeline (publish to X, LinkedIn, Instagram) |

## The Liquid Glass Aesthetic

### Core Visual Principles

1. **Dark void background** — Pure black (#000000) or near-black (#0A0A0A). No gradients on the base. Content floats in darkness.
2. **3D perspective panels** — Screenshots and UI renders tilted at 8-15° with `perspective(1200px)`. Never flat. Always floating.
3. **Glass material** — Panels have frosted edges, subtle reflection, rounded corners with glow, semi-transparent borders.
4. **Particle field** — Small floating particles (2-4px, low opacity, slow drift) fill the void. Creates depth and life.
5. **Spring motion** — All entrances/exits use Remotion `spring()`. Never CSS transitions. Never linear. Organic, confident.
6. **Confident pacing** — 3-5 seconds per scene minimum. No rapid cuts. Let each visual breathe.
7. **Minimal typography** — Sans-serif (Inter, SF Pro, or system), white on black, centered. Maximum 8 words per title card.

### Color Palette

| Token | Value | Usage |
|-------|-------|-------|
| `void` | `#000000` | Background |
| `panel-bg` | `rgba(20, 20, 25, 0.85)` | Glass panel fill |
| `panel-border` | `rgba(255, 255, 255, 0.08)` | Glass edge |
| `panel-glow` | `rgba(59, 130, 246, 0.15)` | Edge glow (AI Blue) |
| `text-primary` | `#FFFFFF` | Title text |
| `text-secondary` | `rgba(255, 255, 255, 0.6)` | Subtitle, URL |
| `accent` | `#3B82F6` | AI Blue highlights |
| `success` | `#22C55E` | Checkmarks, positive states |
| `particle` | `rgba(255, 255, 255, 0.15)` | Background particles |

### 3D Panel CSS (Remotion)

```tsx
const panelStyle: React.CSSProperties = {
  perspective: '1200px',
  transform: `rotateY(-8deg) rotateX(5deg)`,
  borderRadius: 16,
  border: '1px solid rgba(255, 255, 255, 0.08)',
  boxShadow: `
    0 25px 50px rgba(0, 0, 0, 0.6),
    0 0 30px rgba(59, 130, 246, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.05)
  `,
  background: 'rgba(20, 20, 25, 0.85)',
  backdropFilter: 'blur(20px)',
  overflow: 'hidden',
};
```

### Spring Configuration

```tsx
import { spring, useCurrentFrame, useVideoConfig } from 'remotion';

// Standard entrance
const entrance = spring({
  frame,
  fps,
  config: { damping: 15, stiffness: 80, mass: 0.8 },
});

// Subtle drift (for floating panels)
const drift = spring({
  frame: frame - delay,
  fps,
  config: { damping: 200, stiffness: 10, mass: 2 },
  durationInFrames: 120,
});
```

## Scene Types

### 1. Title Card
**Duration**: 3-4 seconds
**Content**: Product name or tagline, centered, white on black
**Animation**: Fade in with subtle scale spring (0.95 → 1.0)
**Example**: "Build your ideas with Gemini"

### 2. Prompt / Input Scene
**Duration**: 4-6 seconds
**Content**: Chat input or terminal prompt, angled 3D panel
**Animation**: Panel springs in from below, text typewriter effect
**Technique**: `<Img>` of screenshot with 3D CSS transform, typewriter via frame-based string slice

### 3. Split Panel Scene
**Duration**: 4-5 seconds
**Content**: Two UI panels side by side (e.g., prompt + code output)
**Animation**: Panels spring in from opposite sides, particles between them
**Technique**: Two `<Img>` components with opposing `rotateY` transforms

### 4. Product Demo Scene
**Duration**: 5-8 seconds
**Content**: Full product UI as floating glass panel
**Animation**: Slow drift rotation (subtle `rotateY` oscillation), cinematic zoom
**Technique**: `<Img>` or `<OffthreadVideo>` with animated `scale` and `rotateY`

### 5. Detail Zoom Scene
**Duration**: 3-4 seconds
**Content**: Zoom into a specific UI element or feature
**Animation**: Spring scale from full view to cropped detail
**Technique**: Animated `scale` + `translate` on the panel image

### 6. CTA / Brand Card
**Duration**: 3-4 seconds
**Content**: Logo + URL or install command
**Animation**: Fade in, hold, fade out
**Technique**: Centered text, brand icon, subtle glow

### 7. AI Cinematic Frame (Imagen 4.0)
**Duration**: 3-5 seconds
**Content**: AI-generated hero render or concept art inside a GlassPanel
**Animation**: Spring entrance, slow drift rotation, subtle zoom
**Technique**: Generate via Imagen 4.0, place in `public/`, use `<Img src={staticFile('render.png')} />` inside GlassPanel with 3D transform
**When to use**: Abstract concepts, architectural diagrams, mood visuals — anything that benefits from AI-generated imagery over screenshots

```tsx
<GlassPanel rotateY={-10} rotateX={6} delay={5}>
  <Img src={staticFile('imagen-hero-render.png')} style={{ width: '100%' }} />
</GlassPanel>
```

### 8. AI Video B-Roll (Veo 3.1)
**Duration**: 4-8 seconds
**Content**: Cinematic AI-generated video clip as transition or atmosphere
**Animation**: Plays behind or inside a GlassPanel, with optional overlay text
**Technique**: Generate via Veo 3.1, preprocess with `ffmpeg -movflags +faststart`, use `<OffthreadVideo>` in Remotion

```tsx
// Full-bleed cinematic B-roll (between scenes)
<OffthreadVideo
  src={staticFile('veo-broll-corridor.mp4')}
  style={{ width: '100%', height: '100%', objectFit: 'cover' }}
/>

// B-roll inside a glass panel
<GlassPanel rotateY={-5} rotateX={3}>
  <OffthreadVideo
    src={staticFile('veo-product-demo.mp4')}
    style={{ width: '100%', borderRadius: 12 }}
  />
</GlassPanel>
```

**Veo 3.1 prompt pattern for B-roll**:
```
[Camera movement], [Subject/environment], [Action/motion], [Lighting + mood].
Dark background, [accent color] glow. Cinematic, professional. [Aspect ratio].
```

**When to use**: Transitions between scene groups, atmospheric intros/outros, cinematic product demos where motion adds value over a static screenshot.

**Preprocessing** (required for `<OffthreadVideo>` + `parseMedia()`):
```bash
ffmpeg -i veo-clip.mp4 -c:v libx264 -crf 18 -movflags +faststart -r 30 processed.mp4
```

### Hybrid Composition Pattern

The most polished videos combine all three asset types:

```
Title Card (text)
  → Imagen frame in GlassPanel (concept art)
    → Veo B-roll transition (cinematic 4s)
      → Screenshot in GlassPanel (product demo)
        → Remotion-animated data (pipeline nodes, file trees)
          → Veo B-roll outro (atmosphere)
            → CTA card (text)
```

**Rule**: Remotion controls timing, transitions, and text. AI assets provide visual richness. Never let AI control pacing — that's Remotion's job.

## Production Pipeline

```
1. STORYBOARD → Define scenes with types (1-8), durations, and content
2. ASSETS → Generate/capture all visual assets
   a. Screenshots — product UI via agent-browser or manual capture
   b. Imagen 4.0 — hero renders, concept art, abstract visuals
      → ai.models.generateImages({ model: 'imagen-4.0-fast-generate-001', prompt: '...' })
      → Save to public/ directory
   c. Veo 3.1 — cinematic B-roll clips (4-8s each)
      → ai.models.generateVideos({ model: 'veo-3.1-fast-generate-preview', prompt: '...' })
      → Preprocess: ffmpeg -i clip.mp4 -c:v libx264 -movflags +faststart -r 30 processed.mp4
      → Save to public/ directory
3. COMPOSE → Build Remotion composition
   - <Sequence> with premountFor for preloading
   - <Img> + staticFile() for images (never <img>)
   - <OffthreadVideo> + staticFile() for Veo clips (never <video>)
   - GlassPanel + spring() for 3D transforms and entrances
   - ParticleField as background layer
   - Subtitle component for text overlays
4. RENDER → npx remotion render src/Root.tsx CompositionId out/video.mp4
5. POST-PROCESS → Add audio if separate
   - ffmpeg -i video.mp4 -i audio.mp3 -c:v copy -c:a aac final.mp4
6. REVIEW → /creative-review scores output against style brief (target: ≥75)
7. DISTRIBUTE → Push to platforms via /blog-post publish pipeline
```

## Remotion Project Structure

```
launch-video/
├── src/
│   ├── Root.tsx                 # registerRoot
│   ├── Composition.tsx          # Main composition with <Sequence> scenes
│   ├── scenes/
│   │   ├── TitleCard.tsx        # Scene type 1
│   │   ├── PromptScene.tsx      # Scene type 2
│   │   ├── SplitPanel.tsx       # Scene type 3
│   │   ├── ProductDemo.tsx      # Scene type 4
│   │   ├── DetailZoom.tsx       # Scene type 5
│   │   └── CTACard.tsx          # Scene type 6
│   ├── components/
│   │   ├── GlassPanel.tsx       # 3D perspective panel with glass material
│   │   ├── ParticleField.tsx    # Background particle system
│   │   ├── TypewriterText.tsx   # Frame-based typewriter animation
│   │   └── SpringFade.tsx       # Reusable spring fade wrapper
│   └── styles/
│       └── tokens.ts            # Liquid Glass color/spacing tokens
├── public/                      # staticFile() assets (screenshots, renders)
├── package.json
└── remotion.config.ts
```

## Particle Field Component (Reference)

```tsx
const ParticleField: React.FC<{ count?: number }> = ({ count = 40 }) => {
  const frame = useCurrentFrame();
  const particles = useMemo(() =>
    Array.from({ length: count }, (_, i) => ({
      x: (i * 37 + 13) % 100,
      y: (i * 53 + 7) % 100,
      size: 2 + (i % 3),
      speed: 0.1 + (i % 5) * 0.05,
      opacity: 0.05 + (i % 4) * 0.04,
    })), [count]);

  return (
    <AbsoluteFill>
      {particles.map((p, i) => (
        <div key={i} style={{
          position: 'absolute',
          left: `${p.x}%`,
          top: `${(p.y + frame * p.speed) % 110}%`,
          width: p.size,
          height: p.size,
          borderRadius: '50%',
          background: `rgba(255, 255, 255, ${p.opacity})`,
        }} />
      ))}
    </AbsoluteFill>
  );
};
```

## GlassPanel Component (Reference)

```tsx
const GlassPanel: React.FC<{
  children: React.ReactNode;
  rotateY?: number;
  rotateX?: number;
  scale?: number;
}> = ({ children, rotateY = -8, rotateX = 5, scale = 1 }) => (
  <div style={{
    transform: `perspective(1200px) rotateY(${rotateY}deg) rotateX(${rotateX}deg) scale(${scale})`,
    borderRadius: 16,
    border: '1px solid rgba(255, 255, 255, 0.08)',
    boxShadow: '0 25px 50px rgba(0,0,0,0.6), 0 0 30px rgba(59,130,246,0.1), inset 0 1px 0 rgba(255,255,255,0.05)',
    background: 'rgba(20, 20, 25, 0.85)',
    overflow: 'hidden',
    transition: 'none',
  }}>
    {children}
  </div>
);
```

## Quality Checklist

- [ ] Background is pure black or near-black (no gradients)
- [ ] All panels use 3D perspective transform (never flat screenshots)
- [ ] Spring animations on all entrances (no CSS transitions)
- [ ] Particle field present in background
- [ ] Each scene holds 3-5 seconds minimum (no rapid cuts)
- [ ] Typography: sans-serif, white, centered, ≤8 words per title card
- [ ] Glass material: border glow, shadow, rounded corners, semi-transparent
- [ ] Audio present (ambient electronic or narration)
- [ ] Total duration 20-45 seconds
- [ ] `-movflags +faststart` on final render
