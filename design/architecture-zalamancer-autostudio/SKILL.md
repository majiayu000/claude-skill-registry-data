---
name: architecture
description: ProAnimate project architecture, tech stack, file organization, layer system, and state management. Auto-applied when discussing project structure.
user-invocable: false
---

# ProAnimate Architecture

Professional web-based animation studio for generating short-form talking character videos with automated lip sync, emotions, AI orchestration, motion graphics, 2D/3D characters, and multi-format export.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 19 + TypeScript + Vite |
| Styling | Tailwind CSS (dark theme: `bg-zinc-900`, `text-zinc-100`) |
| State | Zustand + Immer (immutability) + Zundo (undo/redo) |
| Video Rendering | Remotion (Player + WebCodecs/MediaRecorder) |
| 3D Rendering | Three.js + React Three Fiber |
| 2D Rendering | PixiJS (optional GPU-accelerated canvas) |
| Lottie | lottie-web |
| Backend | Express.js on port 3001 |
| Database | PostgreSQL via Supabase |
| Storage | Supabase Storage (sprites, audio, thumbnails) + IndexedDB (3D blobs, media) |
| Auth | Supabase Auth (email/password, Google OAuth) |
| Payments | Stripe |
| AI - Scripts | Gemini 2.0 Flash |
| AI - Orchestrator | Gemini 2.0 Flash (with Google Search grounding) |
| AI - Characters (2D) | Gemini (Vertex AI image gen) via NanoBanana2 pipeline |
| AI - Characters (3D) | Meshy API (text-to-3D, image-to-3D) |
| AI - Motion (3D) | HunyuanMotion (text-to-3D-motion via HuggingFace) |
| AI - Voice | ElevenLabs (TTS + phoneme alignment + music gen) |
| AI - SVG Objects | Gemini 2.5 Pro |
| AI - Manim | Claude Opus (code gen) |
| Stock Media | Pixabay API |
| Sound Effects | Freesound API |

## File Organization

```
src/
  components/
    canvas/          -- Canvas layer renderers (VideoCanvas.tsx composites all)
    panels/          -- Left panel feature UIs (ScriptsPanel, Character3DPanel, etc.)
    dashboard/       -- Dashboard page, clip grid, batch creation
    layout/          -- EditorLayout, LeftPanel/, RightPanel/, TopMenuBar
    timeline/        -- Timeline.tsx, tracks, playhead, zoom controls
    ui/              -- Shared UI components (GlassPanel, IconButton, etc.)
    overlays/        -- Full-screen overlay components
    pages/           -- Route pages (RigEditorPage, BrandIntelPage, PortfolioPage)
    nodeCanvas/      -- Node-based canvas editor
  services/          -- Business logic, AI clients, processing, export
    effects/         -- Visual effect processors (blur, glitch, neon, etc.)
    motionDesign/    -- Color harmony, typography, timing, visual flow
    qualityAssurance/ -- Quality gates, pre-publish checks, auto-fix
    orchestrator/    -- Orchestrator steps and plan building
    copilot/         -- Copilot service
    manim/           -- Manim video generation pipeline (5-agent system)
  stores/            -- Zustand stores (one per feature domain)
  types/             -- TypeScript type definitions
  hooks/             -- Custom React hooks
  remotion/          -- Remotion export layer components
  engine/            -- Animation engine (easing, spring, particles, path, stagger)
  motionGraphics/    -- Kinetic typography templates (~90), scene layouts (16), registry
  data/              -- Built-in assets (Lottie library, 100+ HTML templates)
  constants/         -- Tab groups, shared constants
  pixi/              -- PixiJS GPU-accelerated renderers + Moveable proxies

server/
  index.ts           -- Express server entry, all route mounting
  routes/            -- API route handlers
  services/          -- Server-side services (AI providers, scrapers, encoding)
  middleware/        -- Auth middleware (supabaseAuth.ts), API key auth, usage logger
  schemas/           -- Server schemas
  jobs/              -- Background jobs (scheduler, metricsPoller)

vendor/
  bonerigging/       -- @bonerigging/core + @bonerigging/editor
```

## Canvas Layer System

### Render Order (bottom to top)

`VideoCanvas.tsx` composites all visual layers inside a `CameraPreviewWrapper`. Each layer is wrapped in `Layer3DWrapper` for the 3D exploded-view debug mode. Layers render in this exact order:

| Order | z-index | Layer | Component | What it renders |
|-------|---------|-------|-----------|----------------|
| 0 | -1 | BG Lottie | `LottieLayers type="background"` | Background Lottie animations |
| 0.4 | 0 | WB Background | `WhiteboardBackground` | Whiteboard surface |
| 0.5 | 0 | Whiteboard | `WhiteboardLayer` + `WhiteboardTextItemLayer` + `WhiteboardDrawingOverlay` | Whiteboard strokes, text, drawing |
| 1 | 0 | Grid | inline `<div>` | Checkerboard/grid background |
| 2 | 1 | HTML Templates | `HTMLTemplateLayer` | iframe-based HTML motion templates |
| 2.5 | 1.5 | Motion Graphics | `MotionGraphicLayer` | React kinetic typography |
| 3.5 | 4 | Crowd | `CrowdLayer` | Background crowd characters |
| 4 | 3 | Video | `VideoLayer` | AI-generated videos |
| 5 | 5 | Media | `MediaLayer` (or `MediaMoveableProxies` in PixiJS mode) | Images, stock photos |
| 6 | 6 | Shapes | `ShapeLayer` (or `ShapeMoveableProxies` in PixiJS mode) | Vector shapes |
| 6.3 | 6.3 | Art Curves | `ArtCurveLayer` | Pen tool / art curves |
| 6.5 | 6.5 | SVG Objects | `SVGObjectLayer` | Animated SVG compositions |
| 7 | 7 | Characters | `CharacterComposite` / `MultiCharacterLayer` (or `CharacterMoveableProxies`) | 2D sprite characters |
| 7.25 | 7.25 | Pixel Art | `PixelArtCharacterLayer` | Pixel art characters |
| 7.3 | 7.3 | Avatars | `AvatarCharacterLayer` | Photo-to-avatar characters |
| 7.5 | 7.5 | 3D Characters | `ThreeCanvas` | Three.js 3D character models |
| 8 | 8 | Text | `TextOverlayLayer` (or `TextMoveableProxies`) | Text overlays, titles |
| 8.5 | 9 | Annotations | `AnnotationLayer` | Draw annotations |
| 8.75 | 9.5 | Particles | `ParticleLayer` | Particle effects |
| 8.9 | 9.75 | Audio Reactive | `AudioReactiveLayer` | Audio-reactive visualizers |
| 8.95 | 9.8 | Mixed Media | `MixedMediaLayer` | Style overlays |
| 9 | 10 | Overlay Lottie | `LottieLayers type="overlay"` | Overlay Lottie animations |
| -- | -- | Audio | `AudioLayer` | Hidden audio playback |
| 11 | 20 | Captions | `CaptionOverlay` | Auto-synced subtitles |
| 12 | 21 | Retention Hooks | `RetentionHookLayer` | Retention hook overlays |

**Post-camera overlays** (rendered outside CameraPreviewWrapper):
- `BoneOverlay` -- rig editing bone overlay (pointer events above all)
- `PathEditorOverlayWrapper` -- path editor for art curves
- `MaskEditorOverlayWrapper` -- mask editor overlay

**PixiJS mode**: When `usePixiRenderer` is enabled, Media, Shapes, Text, and Characters use GPU-accelerated `PixiCanvas` with `MoveableProxy` overlays for selection handles.

### Canvas Dimensions

| Aspect Ratio | Resolution |
|-------------|-----------|
| 16:9 | 1920 x 1080 |
| 9:16 | 1080 x 1920 |
| 1:1 | 1080 x 1080 |
| 4:3 | 1440 x 1080 |
| 21:9 | 2560 x 1080 |

## Remotion Export Layer System

`VideoComposition.tsx` mirrors the canvas layer stack for export. Key differences from canvas layers:

1. **Data as props** -- all data passed via `VideoCompositionProps`, never reads Zustand stores directly
2. **Frame from Remotion** -- uses `useCurrentFrame()` / custom `useFrame()` from engine, not `usePlaybackStore`
3. **CameraTransformWrapper** -- wraps all layers with export camera transforms
4. **Style filters** -- `RemotionStyleFilter` and `RemotionStyleEffectFilters` wrap visual layers

### Export Layer Render Order (bottom to top)

| Export Layer | Props consumed |
|-------------|---------------|
| `RemotionLottieLayer` (background) | `animations` (category: background) |
| `RemotionVideoLayer` | `videos` |
| `RemotionMediaLayer` | `mediaItems`, `keyframeData` |
| `RemotionHTMLTemplateLayer` | `htmlTemplates` |
| `RemotionShapeLayer` | `shapes`, `keyframeData` |
| `RemotionArtCurveLayer` | `artCurves` |
| `RemotionCrowdLayer` | `crowdGroups` |
| `RemotionSVGObjectLayer` | `svgComposition` |
| `RemotionCharacter` (dialogue or single) | `character`, `visemeTimeline`, `emotionTimeline`, `dialogueCharacters` |
| `RemotionRiggedCharacter` | `rigData` (per dialogue char or standalone) |
| `RemotionPixelArtCharacter` | `pixelArtCharacters` |
| `RemotionAvatarCharacter` | `avatarCharacters` |
| `Remotion3DLayer` | `characters3D`, camera props |
| `RemotionTextOverlay` | `textOverlays`, `keyframeData` |
| `RemotionAnnotationLayer` | `annotations` |
| `RemotionParticleLayer` | `particleEmitters` |
| `RemotionAudioReactiveLayer` | `audioReactiveVisualizers` |
| `RemotionLottieLayer` (overlay) | `animations` (category: overlay) |
| `RemotionRetentionHookLayer` | `retentionHooks` |
| `RemotionTransitionLayer` | `clipTransitions` |
| Audio tracks | `audioUrl`, `backgroundAudio`, dialogue line audio |

## Tab / Panel System

### Tab Registration (`src/constants/tabGroups.ts`)

Tabs are organized in `TAB_GROUPS` array. Each group has:
- `id` (TabGroupId) -- group identifier
- `label` -- display name
- `subTabs` -- array of `SubTabDef` with `{ id, label, icon, description }`

| Group ID | Label | Sub-tabs |
|----------|-------|----------|
| `create` | Characters | character |
| `media` | Library | media |
| `video` | Generate | gen-image, gen-text-to-video, image-to-video, gen-audio-to-video, gen-video-to-video, gen-retake, gen-extend, broll-suggest, gen-manim |
| `audio` | Audio | voice-clone, singing, adaptive-music, audio-enhancement, beat-sync |
| `edit` | Edit | mixed-media, animStyle, transitions, cinema-studio |
| `script` | Script | scripts, dialogue, transcript, captions |
| `design` | Design | text, brand-kit, schema, assets, memes, crowd |
| `publish` | Publish | auto-publish, series, competitor-scraper, trends, virality, repurpose |

**Hidden tabs** (not in TAB_GROUPS, mapped via `TAB_TO_GROUP`): `rig-editor`, `rig-editor-3d`, `3d-objects`

### Panel Rendering (`LeftPanel.tsx`)

- `CARD_GRID_THRESHOLD = 2` -- groups with >2 sub-tabs show a card grid first
- Groups with <=2 sub-tabs go directly to panel content
- `PanelContent({ tab })` maps tab IDs to React components
- **Eagerly loaded**: media, videos, assets, character, scripts, dialogue, text, captions, transitions, schema, rig-editor, rig-editor-3d
- **Lazy loaded** (via `React.lazy()`): all other panels (~40+)
- Lazy fallback: spinner with `Loader2` icon

### Navigation System

- **MainGroupHeader** -- shows current group with prev/next buttons and dropdown
- **DrillDownHeader** -- shows current sub-tab with back, prev/next, dropdown
- **SubTabCardGrid** -- card-based navigation for large groups (>2 tabs)
- Character tab has internal mode switcher: 2D / 3D / 1D / Avatar

### Absorbed/Redirected Tabs

`ABSORBED_TAB_REDIRECT` maps deprecated tab IDs to their new locations (e.g., `'camera' -> 'cinema-studio'`, `'svg-art' -> 'assets'`).

## Store Architecture

### Core Stores (barrel-exported from `src/stores/index.ts`)

| Store | Manages |
|-------|---------|
| `useEditorStore` | Panel tabs, modals, aspect ratio, canvas overlay, PixiJS toggle |
| `useTimelineStore` | Tracks, clips, frames, playback, markers, beat snap (Zundo undo/redo) |
| `useCanvasStore` | Canvas dimensions, zoom/pan, 3D view, orbit, character selection |
| `usePlaybackStore` | Current frame, FPS, play state, timecode formatting |
| `useCharacterConfigStore` | Viseme sprites, emotion heads, character parts config |
| `useCharacterPartsStore` | Character part transforms, layer parts, style effects |
| `useVoiceStore` | TTS voice selection, generated audio |
| `useAnimationStore` | Lottie animation items, active animations |
| `useProjectStore` | Project persistence (save/load) |
| `useMultiCharacterStore` | Multi-character dialogue (characters, lines, positions) |
| `useAuthStore` | Supabase auth state |
| `useMediaStore` | Media assets, canvas media items |
| `useTextOverlayStore` | Text overlays, fonts, presets |
| `useVideoLayerStore` | AI-generated video layers |
| `useHTMLTemplateLayerStore` | HTML template iframes |
| `useSettingsStore` | Export settings (resolution, format, quality) |
| `useSVGObjectStore` | SVG object compositions |
| `useKeyframeStore` | Keyframe recording mode, keyframe data |
| `useShapeStore` | Vector shapes |
| `useArtCurveStore` | Pen tool art curves |
| `use3DCharacterStore` | 3D characters on canvas |
| `useRigStore` | 2D bone rigging system |
| `useLayerTreeStore` | Layer tree ordering |
| `useAvatarCharacterStore` | Avatar characters |
| `useCrowdStore` | Crowd background characters |
| `useAnnotationStore` | Drawing annotations |
| `useMemeStore` | Meme templates |

### Non-barrel stores (imported directly to avoid eager loading)

| Store | Manages |
|-------|---------|
| `useOrchestratorStore` | AI orchestrator pipeline (imports 9+ stores) |
| `useCameraStore` | Virtual camera keyframes, shake, focus pull |
| `useMotionGraphicStore` | Kinetic typography instances |
| `useWhiteboardStore` | Whiteboard state, brushes, drawing |
| `usePixelArtCharacterStore` | Pixel art characters |
| `useCopilotStore` | AI copilot sidebar |
| `useBrandStore` / `useBrandDirectorStore` | Brand kit, brand intelligence |
| `useAutoPublishStore` | Auto-publish scheduling |
| `useSeriesStore` | Series/episode management |
| `useCreditsStore` / `useBillingStore` | Credit system, billing |
| `useTranscriptStore` | Transcript editing |
| `useSavedCharactersStore` / `useSaved3DCharactersStore` / `useSavedAvatarCharactersStore` / `useSavedPixelArtCharactersStore` | Persisted character libraries |
| `usePathStore` | Path editing state |
| `useMaskStore` | Mask editing state |

## Server Architecture

### Middleware Chain

```
Request → CORS → [Stripe webhook raw body] → express.json(100mb) → [Rate Limiter] → [requireAuth] → Route Handler
```

1. **CORS** -- allows configured origins (localhost:5173/5174/5175/3000 by default, or `ALLOWED_ORIGINS` env)
2. **Stripe webhook** -- mounted BEFORE `express.json()` to get raw body for signature verification
3. **express.json** -- 100mb limit for base64 images/audio
4. **Rate limiter** (`aiRateLimiter`) -- 20 req/min/IP on AI endpoints, skips OPTIONS
5. **requireAuth** -- Supabase JWT verification, attaches `userId`/`userEmail` to request
6. **requireApiKey** -- API key auth for v1 public API routes
7. **usageLogger** -- logs API key usage for v1 routes

### Route Groups

| Path | Auth | Rate Limited | Route File | Purpose |
|------|------|-------------|------------|---------|
| `/api/ai-animation` | JWT | Yes | `aiAnimation.ts` | Claude-powered SVG animation |
| `/api/stripe` | None | No | `stripe.ts` | Billing + webhooks |
| `/api/credits` | None | No | `credits.ts` | Credit balance |
| `/api/marketplace` | None | No | `marketplace.ts` | Template marketplace |
| `/api/social` | None | No | `social.ts` | Social media OAuth + publishing |
| `/api/learning` | None | Partial | `learning.ts` | Content performance learning |
| `/api/meshy` | JWT | Yes | `meshy.ts` | Meshy 3D generation proxy |
| `/api/motion` | JWT | Yes | `hunyuanMotion.ts` | HunyuanMotion proxy |
| `/api/auto-rig` | JWT | Yes | `autoRig.ts` | Auto-rigging |
| `/api/bg-remove` | JWT | No | `bgRemoval.ts` | Background removal |
| `/api/brand-director` | JWT | Yes | `brandDirector.ts` | Brand intelligence AI |
| `/api/competitor-scraper` | JWT | Yes | `competitorScraper.ts` | Competitor video scraping |
| `/api/url-to-video` | JWT | Yes | `urlToVideo.ts` | URL content to video |
| `/api/content-extractor` | JWT | No | `contentExtractor.ts` | Content extraction |
| `/api/virality` | JWT | Yes | `viralityAnalysis.ts` | Virality scoring |
| `/api/recraft` | JWT | Yes | `recraft.ts` | Recraft image gen |
| `/api/generator` | JWT | Yes | `generator.ts` | General AI generator |
| `/api/image-to-video` | JWT | Yes | `imageToVideo.ts` | Image-to-video AI |
| `/api/music-generation` | JWT | Yes | `musicGeneration.ts` | AI music gen |
| `/api/auto-publish` | JWT | No | `autoPublish.ts` | Auto-publish scheduling |
| `/api/style-transfer` | JWT | Yes | `styleTransfer.ts` | Style transfer |
| `/api/whisper` | JWT | Yes | `whisper.ts` | Transcription |
| `/api/svg-animation` | JWT | Yes | `svgAnimation.ts` | SVG animation pipeline |
| `/api/manim` | JWT | Yes | `manim.ts` | Manim video generation |
| `/api/pixellab` | JWT | Yes | `pixelLab.ts` | Pixel art generation |
| `/api/ai` | JWT | Yes | `aiProvider.ts` | AI provider proxy |
| `/api/recordings` | JWT | No | `recordings.ts` | Screen recordings |
| `/api/characters` | JWT | No | `characters.ts` | 2D character CRUD |
| `/api/pixelart-characters` | JWT | No | `pixelArtCharacters.ts` | Pixel art character CRUD |
| `/api/3d-characters` | JWT | No | `characters3d.ts` | 3D character CRUD |
| `/api/avatar-characters` | JWT | No | `avatarCharacters.ts` | Avatar character CRUD |
| `/api/notifications` | None | No | `notifications.ts` | Notifications |
| `/api/portfolio` | None | No | `portfolio.ts` | Portfolio platform |
| `/api/nb2` | JWT | NB2 limiter | `nanoBanana2.ts` | NanoBanana2 character gen (separate rate limiter) |
| `/api/proxy` | JWT | No | `proxy.ts` | CORS proxy for external resources |

### Public API v1 (API-key authenticated)

| Path | Route File | Purpose |
|------|-----------|---------|
| `/api/v1/renders` | `v1/renders.ts` | Programmatic video rendering |
| `/api/v1/voices` | `v1/voices.ts` | Voice generation |
| `/api/v1/characters` | `v1/characters.ts` | Character CRUD |
| `/api/v1/templates` | `v1/templates.ts` | Template access |
| `/api/v1/projects` | `v1/projects.ts` | Project management |
| `/api/v1/translate` | `v1/translate.ts` | Translation (rate limited) |
| `/api/v1/webhooks` | `v1/webhooks.ts` | Webhook management |
| `/api/v1/api-keys` | `v1/apiKeys.ts` | API key management (JWT auth) |
| `/api/v1/openapi.yaml` | static | OpenAPI spec |
| `/api/docs` | inline | Swagger UI |

### Utility Endpoints
- `/api/health` -- Health check (returns configured service statuses)
- `/api/recraft/status` -- Public Recraft availability check
- `/api/proxy/audio` -- Freesound CORS proxy (freesound.org only)

## Path Aliases

- `@/` maps to `./src/` (configured in both `tsconfig.json` and `vite.config.ts`)
- `@bonerigging/core` and `@bonerigging/editor` map to `./src/bonerigging/`

## Key Architectural Patterns

- **Credit gating**: AI operations wrapped in `withCreditGate(operationType, fn)` for billing
- **Service layer**: Pure functions in `src/services/`, stores call services
- **Canvas/Remotion duality**: Every visual feature needs both a canvas layer (preview) and Remotion layer (export)
- **Tab registration**: Features register in `src/constants/tabGroups.ts` and `src/types/editor.ts`
- **Server proxy**: All external API calls go through Express backend to protect API keys
- **Lazy loading**: Non-core panels lazy-loaded via `React.lazy()` in `LeftPanel.tsx`
- **PixiJS dual rendering**: Media, shapes, text, and characters can render via PixiJS GPU canvas with DOM proxy overlays for selection handles
- **3D debug view**: `Layer3DWrapper` provides exploded 3D layer visualization controlled by `useCanvasStore.is3DView`
