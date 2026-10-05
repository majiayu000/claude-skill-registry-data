---
name: ad-video
description: Generate platform-optimized video ads from a product brief. Supports brand kits, 6 ad types, 6 platform formats (TikTok, Instagram, YouTube, Facebook, LinkedIn), batch personalization, A/B variants, stock footage, screen recordings, and AI voiceover. ~$1-5/video.
version: 1.0.0
category: build
platforms:
  - CLAUDE_CODE
permissions:
  - filesystem
  - shell
  - network
  - api
tags: [video, advertising, marketing, remotion, batch, brand-kit, social-media]
author: skills-hub
---

# Ad Video

Create platform-optimized video ads from a product brief. Describe your product, get ads for TikTok, Instagram, YouTube, Facebook, and LinkedIn — rendered and ready to upload.

## Setup

### Step 1: Check Prerequisites

```bash
TOOLKIT=~/.openclaw/workspace/claude-code-video-toolkit
cd $TOOLKIT
python3 tools/verify_setup.py
```

The ad-video skill extends the video-toolkit. Ensure video-toolkit is installed and configured first.

### Step 2: Install Additional Dependencies

```bash
cd $TOOLKIT
pip3 install --break-system-packages playwright qrcode[pil] Pillow
playwright install chromium
```

### Step 3: Configure API Keys

Add to `.env`:
```
PEXELS_API_KEY=...    # Free at pexels.com/api (stock footage)
```

Voiceover and music use existing video-toolkit Modal endpoints (Qwen3-TTS, MusicGen).

## Creating an Ad

### Step 1: Create Project

```bash
cd $TOOLKIT
cp -r templates/ad-template projects/MY_AD
cd projects/MY_AD
npm install
```

### Step 2: Define Brand Kit

Create or edit `brand.json`:

```json
{
  "name": "Acme Corp",
  "tagline": "Ship faster, break nothing",
  "website": "https://acme.com",
  "logo": {
    "primary": "brand/logo.svg",
    "light": "brand/logo-light.svg",
    "dark": "brand/logo-dark.svg",
    "icon": "brand/icon.svg",
    "minWidth": 120,
    "safePadding": 16
  },
  "colors": {
    "primary": "#2563EB",
    "secondary": "#7C3AED",
    "accent": "#F59E0B",
    "background": "#0F172A",
    "surface": "#1E293B",
    "text": "#F8FAFC",
    "textMuted": "#94A3B8",
    "ctaBackground": "#2563EB",
    "ctaText": "#FFFFFF",
    "gradient": ["#2563EB", "#7C3AED"]
  },
  "fonts": {
    "heading": { "family": "Inter", "weight": 800, "source": "google" },
    "body": { "family": "Inter", "weight": 400, "source": "google" },
    "accent": { "family": "Space Grotesk", "weight": 700, "source": "google" }
  },
  "social": {
    "twitter": "@acmecorp",
    "linkedin": "acme-corp"
  }
}
```

Validate: `python3 tools/brand_validate.py --brand brand.json`

### Step 3: Write Ad Config

Edit `src/config/ad-config.ts`:

```typescript
export const adConfig: AdBrief = {
  type: 'product-launch',
  product: {
    name: 'Acme Deploy',
    tagline: 'Ship faster, break nothing',
    description: 'One-click deployments with automatic rollbacks and zero-downtime.',
    features: [
      'One-click deploy',
      'Automatic rollbacks',
      'Zero-downtime migrations',
    ],
    painPoints: [
      'Deployments take hours and break production',
      'Rollbacks are manual and terrifying',
    ],
    pricing: { amount: '$29/mo', trial: '14-day free trial' },
  },
  assets: {
    productShots: ['products/dashboard.png', 'products/deploy-screen.png'],
    screenRecording: {
      url: 'https://app.acme.com/dashboard',
      script: [
        { action: 'wait', duration: 1000 },
        { action: 'click', selector: '#deploy-btn' },
        { action: 'wait', duration: 2000 },
      ],
    },
    stockQueries: ['developer coding', 'server room'],
  },
  cta: {
    text: 'Start Free Trial',
    secondary: 'Learn More',
    url: 'https://acme.com/signup',
    qrCode: true,
  },
  targets: ['tiktok', 'instagram-reel', 'youtube-preroll', 'facebook', 'linkedin'],
  voiceover: { enabled: true, speaker: 'Ryan', tone: 'excited' },
  music: { preset: 'upbeat-tech', volume: 0.12 },
};
```

Ad types: `product-launch`, `feature-highlight`, `testimonial`, `comparison`, `seasonal-promo`, `app-demo`.

**Type-specific config fields** (add alongside the base config):

- **testimonial:** `testimonial: { quote: '...', author: 'Jane Doe', title: 'CTO at Startup', avatar: 'brand/jane.png', rating: 5 }`
- **comparison:** `comparison: { competitor: 'OldTool', advantages: [{ dimension: 'Speed', us: '50ms', them: '500ms' }] }`
- **seasonal-promo:** `seasonal: { event: 'Black Friday', discount: '50% off', deadline: 'Nov 30' }`

### Asset Manifest

Each asset gets a manifest entry telling the skill what it contains, its role in the ad, and how prominently to feature it.

```typescript
interface AdAsset {
  path: string;                    // relative path to file
  type: 'product-shot' | 'screenshot' | 'logo' | 'video' | 'testimonial' | 'stock' | 'icon';
  description: string;             // what this asset shows — Claude uses this for scene placement
  tags: string[];                  // searchable: ['hero', 'feature-x', 'pricing', 'social-proof']
  scene?: string;                  // force into scene: 'hook', 'problem', 'solution', 'feature', 'cta'
  weight: 1 | 2 | 3 | 4 | 5;     // 1=background, 3=standard, 5=hero product shot
  platform?: string[];             // limit to platforms: ['tiktok', 'instagram'] or omit for all
  variant?: string;                // A/B variant group: 'A', 'B', etc.
  animation?: 'parallax' | 'zoom' | 'rotate' | 'float' | 'slide-in' | 'none';
  cropSafeZone?: boolean;          // true = has important content at edges, respect safe zones
  duration?: number;               // suggested screen time in seconds
  notes?: string;                  // "main hero shot — use in hook and CTA"
}

interface AdManifest {
  assets: AdAsset[];
  defaults: {
    weight: number;
    durationByWeight: {
      1: number; // 1s — flash/background
      2: number; // 2s — supporting
      3: number; // 3s — standard feature
      4: number; // 4s — featured product shot
      5: number; // 5s — hero shot, max emphasis
    };
  };
}
```

#### How Weights Work for Ads

| Weight | Role | Screen Time | Position | Animation |
|--------|------|-------------|----------|-----------|
| 5 — Hero | Main product shot | 4-6s | Hook opener AND CTA closer | Parallax zoom, glow |
| 4 — Featured | Key feature demo | 3-4s | Solution/feature scenes | Zoom or slide-in |
| 3 — Standard | Supporting visual | 2-3s | Any relevant scene | Standard animation |
| 2 — Supporting | Context/texture | 1-2s | Background or B-roll | Subtle or none |
| 1 — Filler | Stock/generic | 0.5-1s | Only if needed | Quick flash |

#### Smart Placement Rules

- `type: 'product-shot'` + `weight: 5` → Hook (first 3 seconds) AND CTA end card
- `type: 'screenshot'` + tags `['feature-x']` → Feature highlight scene for that feature
- `type: 'testimonial'` → Testimonial scene, with name/title lower third
- `type: 'logo'` → Hook corner + CTA end card + watermark throughout
- `type: 'stock'` → B-roll behind text overlays in problem/solution scenes
- `scene: 'hook'` assets always appear in first 3 seconds
- `platform: ['tiktok']` assets only used in TikTok renders (e.g., vertical product shots)
- `variant: 'A'` assets only used in A variant renders

#### Example

```typescript
const manifest: AdManifest = {
  assets: [
    {
      path: 'assets/hero-product.png',
      type: 'product-shot',
      description: 'Product hero shot on clean white background',
      tags: ['hero', 'product'],
      weight: 5,
      scene: 'hook',
      animation: 'parallax',
      notes: 'Use in hook AND CTA. This is the money shot.',
    },
    {
      path: 'assets/dashboard-screenshot.png',
      type: 'screenshot',
      description: 'Dashboard showing the analytics panel with live metrics',
      tags: ['feature-analytics', 'demo'],
      weight: 4,
      scene: 'feature',
      animation: 'zoom',
      cropSafeZone: true,
    },
    {
      path: 'assets/customer-testimonial.mp4',
      type: 'testimonial',
      description: 'Sarah from Acme Corp saying the product saved them 40 hours/month',
      tags: ['social-proof', 'testimonial'],
      weight: 4,
      scene: 'testimonial',
      duration: 5,
    },
    {
      path: 'assets/logo-dark.svg',
      type: 'logo',
      description: 'Company logo dark variant for light backgrounds',
      tags: ['brand'],
      weight: 3,
    },
  ],
  defaults: {
    weight: 3,
    durationByWeight: { 1: 1, 2: 2, 3: 3, 4: 4, 5: 5 },
  },
};
```

### Step 4: Gather Assets

**Stock footage:**
```bash
cd $TOOLKIT
python3 tools/pexels_search.py \
  --query "developer coding" --type video --orientation landscape \
  --output projects/MY_AD/public/stock/
```

**Screen recording (optional):**
```bash
cd $TOOLKIT
python3 tools/screen_record.py \
  --url "https://app.acme.com/dashboard" \
  --script projects/MY_AD/scripts/demo-flow.json \
  --viewport 1280x720 \
  --device "iPhone 14 Pro" \
  --output projects/MY_AD/public/recordings/demo.mp4
```

Supports device emulation (`--device`), custom viewports, and CSS injection (hide cookie banners, blur PII).

**Voiceover:**
```bash
cd $TOOLKIT
python3 tools/qwen3_tts.py \
  --text "Tired of deployments that break production? Meet Acme Deploy." \
  --speaker Ryan --tone excited \
  --output projects/MY_AD/public/audio/vo.mp3 --cloud modal
```

**Speakers:** `Ryan`, `Aiden`, `Vivian`, `Serena`, `Uncle_Fu`, `Dylan`, `Eric`, `Ono_Anna`, `Sohee`
**Tones:** `neutral`, `warm`, `professional`, `excited`, `calm`, `serious`, `storyteller`, `tutorial`

**Background music:**
```bash
cd $TOOLKIT
python3 tools/music_gen.py \
  --preset upbeat-tech --duration 30 \
  --output projects/MY_AD/public/audio/bg.mp3 --cloud modal
```

Presets: `corporate-bg`, `upbeat-tech`, `ambient`, `dramatic`, `tension`, `hopeful`, `cta`, `lofi`.

### Step 5: Generate Composition

Claude reads the ad config and brand kit, then generates the Remotion composition. The composition includes:

1. **HookScene** — Attention-grabbing opener (question, stat, or bold claim)
2. **ProblemScene** — Visualize the pain point
3. **SolutionScene** — Product reveal with key highlights
4. **CTAScene** — Call-to-action with end card

Each scene uses KineticText for headlines, ProductShot for product images, and brand-consistent colors/fonts from brand.json.

**Ad script structure:** Hook (stop scrolling) > Problem (empathy) > Solution (product demo) > CTA (next action).

### Step 6: Render All Platforms

```bash
cd $TOOLKIT/projects/MY_AD

# Preview
npx remotion studio

# Render all platforms
npx remotion render src/index.ts Ad-tiktok out/tiktok.mp4
npx remotion render src/index.ts Ad-instagram-reel out/instagram-reel.mp4
npx remotion render src/index.ts Ad-youtube-preroll out/youtube-preroll.mp4
npx remotion render src/index.ts Ad-facebook out/facebook.mp4
npx remotion render src/index.ts Ad-linkedin out/linkedin.mp4
```

Output: one MP4 per platform in `out/`.

### Step 7: A/B Variants (Optional)

Generate variant headlines and CTAs for testing:

```bash
cd $TOOLKIT
python3 tools/generate_variants.py \
  --config projects/MY_AD/src/config/ad-config.ts \
  --elements headline,cta \
  --count 3 \
  --output projects/MY_AD/variants.json
```

Then render each variant:
```bash
cd $TOOLKIT/projects/MY_AD
npx remotion render src/index.ts Ad-tiktok-A out/tiktok-A.mp4
npx remotion render src/index.ts Ad-tiktok-B out/tiktok-B.mp4
npx remotion render src/index.ts Ad-tiktok-C out/tiktok-C.mp4
```

### Step 8: Batch Personalization (Optional)

Create a CSV with variant data:

```csv
id,headline,ctaText,price,audience
dev-us,"Deploy in 60 seconds","Start Free Trial","$29/mo",developers
mktg-us,"Marketing teams ship 3x faster","Try It Free","$29/mo",marketers
dev-eu,"Ship code with confidence","Start Now","€27/mo",developers-eu
```

Render all (local):
```bash
cd $TOOLKIT
python3 tools/batch_render.py \
  --template projects/MY_AD \
  --data projects/MY_AD/variants.csv \
  --platforms tiktok,instagram-reel,facebook \
  --parallelism 4 \
  --output projects/MY_AD/out/batch/
```

Render all (Remotion Lambda for cloud-scale parallelism):
```bash
cd $TOOLKIT
python3 tools/batch_render.py \
  --template projects/MY_AD \
  --data projects/MY_AD/variants.csv \
  --renderer lambda \
  --output s3://my-bucket/ads/
```

Output: `out/batch/{platform}/{id}.mp4` — one video per row per platform.

## Platform Specs

| Platform | Aspect | Resolution | FPS | Duration | Notes |
|---|---|---|---|---|---|
| TikTok | 9:16 | 1080x1920 | 30 | 15-60s | Bottom 20% obscured by UI |
| Instagram Reel | 9:16 | 1080x1920 | 30 | 15-30s | Keep text in center 70% |
| Instagram Feed | 4:5 | 1080x1350 | 30 | 3-60s | 4:5 fills more feed space |
| YouTube Pre-roll | 16:9 | 1920x1080 | 30 | 6-15s | Skippable after 5s |
| Facebook | 1:1 | 1080x1080 | 30 | 5-15s | Square performs best in feed |
| LinkedIn | 16:9 | 1920x1080 | 30 | 15-30s | Data/stats perform well |

## Ad Script Framework

Every ad follows the **Hook > Problem > Solution > CTA** structure:

1. **Hook (2-4s):** Stop the scroll. Use a question, shocking stat, bold claim, or pain point. Must grab attention in the first 1.5 seconds.
2. **Problem (3-7s):** Show empathy. Describe the pain the audience feels. Use animated text, frustrated-user visuals, or before/after.
3. **Solution (4-14s):** Reveal the product. Show it in action (screenshots, screen recording, product shots). Highlight 2-3 key features with animated text + stats.
4. **CTA (2-6s):** Clear next action. Animated button, QR code, pricing, and end card with logo + tagline.

### Duration Allocation by Platform

| Platform | Total | Hook | Problem | Solution | CTA |
|---|---|---|---|---|---|
| TikTok (30s) | 30s | 3s | 7s | 14s | 6s |
| Instagram Reel (15s) | 15s | 2s | 3s | 7s | 3s |
| YouTube Pre-roll (6s) | 6s | 1.5s | -- | 2.5s | 2s |
| YouTube Pre-roll (15s) | 15s | 2s | 3s | 7s | 3s |
| Facebook (15s) | 15s | 2s | 3s | 7s | 3s |
| LinkedIn (30s) | 30s | 3s | 7s | 14s | 6s |

YouTube 6s bumper ads skip the Problem scene entirely -- they are Solution + CTA only.

**Voiceover word budget per scene:** `(durationSeconds - 2) * 2.5` words.

## Ad Type Scene Maps

### Product Launch
Hook (bold-claim) > Problem (list) > Solution (product-reveal) > Feature x2 > CTA

### Feature Highlight
Hook (curiosity-gap) > Feature (full scene) > Demo (screen recording) > CTA

### Testimonial
Hook (stat/social-proof) > Testimonial (full-screen-quote) > Solution (product-reveal) > CTA

### Comparison
Hook (question) > Comparison (table or split-screen) > Solution (highlights) > CTA

### Seasonal Promo
Hook (urgency) > PriceTag (discount reveal) > Feature (quick highlights) > CTA (deadline)

### App Demo
Hook (pain-point) > ScreenRecording (product in action) > Feature x2 > CTA

## Composition Patterns

### Brand-Consistent Text

ALWAYS load fonts from brand kit. NEVER hardcode font families.

```tsx
const { fontFamily: headingFont } = loadFont({
  family: brand.fonts.heading.family,
  weight: brand.fonts.heading.weight,
});
```

### Product Shot with Animation

```tsx
<ProductShot
  src={staticFile('products/dashboard.png')}
  animation="tilt-3d"
  mockup="browser"
  shadow
/>
```

Animations: `parallax`, `zoom-rotate`, `float`, `tilt-3d`, `slide-in`.
Mockups: `phone`, `laptop`, `browser`.

### Animated CTA Button

```tsx
<CTAButton
  text="Start Free Trial"
  backgroundColor={brand.colors.ctaBackground}
  textColor={brand.colors.ctaText}
  animation="pulse"
  position="bottom-center"
  size="lg"
/>
```

Animations: `pulse`, `bounce`, `glow`, `slide-in`.

### QR Code Overlay

```tsx
<QRCode
  url="https://acme.com/signup"
  animation="scan-reveal"
  size={120}
  position="bottom-right"
/>
```

Animations: `fade-in`, `scan-reveal`, `pixel-build`.

### Platform-Aware Layout

```tsx
<PlatformAdapter platform="tiktok">
  <HookScene brand={brand} style="stat" text="87% of deploys fail" animation="slam" />
  <ProblemScene brand={brand} headline="Deployment is broken" painPoints={[...]} />
  <SolutionScene brand={brand} headline="Meet Acme Deploy" productShot="..." />
  <CTAScene brand={brand} ctaText="Start Free Trial" ctaUrl="..." />
</PlatformAdapter>
```

### KineticText Modes

```tsx
<KineticText text="Ship faster" animation="slam" />
```

Modes: `slide-up`, `pop-word`, `typewriter`, `wave`, `split-reveal`, `counter`.

### Transitions

```tsx
import { TransitionSeries, linearTiming } from '@remotion/transitions';
import { fade } from '@remotion/transitions/fade';
```

Import custom transitions from `lib/transitions/presentations/` directly, never from barrel. For additional variety, use GL Transitions (`remotion-gl-transitions`).

### Audio Layering

```tsx
{/* Background music — full duration, low volume */}
<Audio src={staticFile('audio/bg.mp3')} volume={0.12} />

{/* Voiceover — starts 1s in (30 frames at 30fps) */}
<Sequence from={30}>
  <Audio src={staticFile('audio/vo.mp3')} volume={1} />
</Sequence>
```

ALWAYS use `<OffthreadVideo>` for video embeds, NEVER `<video>`.

## Cost Estimates

| Component | Cost | Notes |
|---|---|---|
| Voiceover (Qwen3-TTS) | ~$0.01 | Per scene, ~20s warm GPU |
| Background music (MusicGen) | ~$0.02-0.05 | Duration-dependent |
| Stock footage (Pexels) | Free | 200 req/hr, no attribution needed |
| Screen recording (Playwright) | Free | Local execution |
| AI images (FLUX.2) | ~$0.01/image | If needed for backgrounds |
| Remotion render (local) | Free | ~30s per 30s video |
| Remotion render (Lambda) | ~$0.01-0.10 | Per render, massively parallel |

**Single ad, all 5 platforms:** ~$1-3 total
**Batch of 50 variants x 5 platforms (250 videos):** ~$5-25 total (Lambda) or free (local, ~2 hours)

## Remotion Ecosystem Packages

Install the official Remotion skills for best results: `npx skills i remotion-dev/skills/skills/remotion`. This provides 35 production rules covering animations, audio, transitions, text, 3D, and more.

### Core Packages

| Package | What it does |
|---------|-------------|
| `@remotion/transitions` | fade, slide, wipe, flip, clockWipe, iris |
| `@remotion/captions` | TikTok-style word-by-word captions |
| `@remotion/media-utils` | `visualizeAudio()`, `getAudioData()`, `getAudioDurationInSeconds()` |
| `@remotion/layout-utils` | `measureText()`, `fitText()`, `fillTextBox()` |
| `@remotion/light-leaks` | WebGL light leak overlays — use for premium scene transitions |
| `@remotion/motion-blur` | `<Trail>` and `<CameraMotionBlur>` — use for product shot reveals |
| `@remotion/noise` | Procedural noise for film grain |
| `@remotion/google-fonts` | Google Fonts loading |
| `@remotion/shapes` | Geometric shape components |
| `@remotion/paths` | SVG path animation |
| `remotion-animated` | Declarative `<Animated>` with `Move()`, `Scale()`, `Fade()` |

### Community Packages

| Package | What it does |
|---------|-------------|
| **Remotion Bits** (`npx remotion-bits find/fetch`) | ParticleSystem, AnimatedText (char/word/line stagger), StaggeredMotion |
| **GL Transitions** (`remotion-gl-transitions`) | Hundreds of GLSL shader transitions from gl-transitions.com — use for variety in ad cuts |
| **remotion-confetti** | Canvas-based confetti with physics |

### AI Services

| Service | What it does | Cost |
|---------|-------------|------|
| **fal.ai** | Single API for video gen (Veo 3.1, Kling 3, Wan 2.2). One key for AI B-roll generation | $0.05-0.50/sec |
| **whisper.cpp** | LOCAL speech-to-text, zero cost. Use for caption generation | Free |
| **Suno** (via KIE) | AI music with vocals. Better than MusicGen for songs with lyrics | $0.03/song |

### Producer Intelligence

**Audio ducking:** Auto-lower music volume when voiceover speaks. Use Remotion's `interpolate()` on volume based on voiceover audio presence.

**Loudness normalization:** Target LUFS per platform: YouTube -14, TikTok -14, Instagram -14, Facebook -14, LinkedIn -14. Post-process:
```bash
ffmpeg -i input.mp4 -af loudnorm=I=-14:TP=-1.5:LRA=11 output.mp4
```

**Film grain via `@remotion/noise`:** Use `noise2D()` or `noise3D()` for procedural film grain instead of CSS overlay.

**Light leaks via `@remotion/light-leaks`:** WebGL overlays for premium transitions between scenes.

## Key Rules

1. **Brand kit first** — always validate brand.json before composing
2. **Platform specs are law** — never exceed duration limits, always respect safe zones
3. **Hook in 1.5 seconds** — the first scene MUST grab attention immediately
4. **All motion via useCurrentFrame()** — no CSS animations, no Tailwind animate classes
5. **Always staticFile()** for assets — never require() or import
6. **Always `<OffthreadVideo>`** — never raw `<video>` tags
7. **CTA on every variant** — every ad must end with a clear call-to-action
8. **Test at 1x speed** — preview at actual playback speed before rendering

Source: Built on [digitalsamba/claude-code-video-toolkit](https://github.com/digitalsamba/claude-code-video-toolkit) (MIT License)
