---
skill_id: ai-media-generation
name: AI Media Generation
description: "AI video and image prompt engineering — video generation, image generation, product video, social media video, cinematic direction, animation, Seedance, Higgsfield, GPT-Image-2. Applies 15 Maxim-authored cinematic styles and the atomic prompt schema."
version: 1.0.0
category: ai-media-generation
office: CMO + CTO
lead_agent: content-strategist
triggers:
  - video generation
  - AI video
  - seedance
  - higgsfield
  - video prompt
  - image generation
  - product video
  - social media video
  - cinematic
  - animation
  - 3D CGI
  - motion design
  - brand story video
collaborates_with:
  - content-strategist
  - brand-guardian
  - video-script-writer
  - ui-designer
---

# AI Media Generation — Domain Dispatcher

Maxim's skill domain for AI video and image prompt engineering. Combines **15 Maxim-authored cinematic styles** (behavioral-moat-framed, see `cinematic-styles/`) with external technical references (20 Higgsfield sub-skills) — total 35 skills, 15 of which are Maxim's original IP with defensible behavioral-framework engineering.

---

## Activation

This domain activates when a task involves:
- AI video or image generation (any model/platform)
- Video prompt writing or optimization
- Cinematic, commercial, or social media video production
- Product videos, brand stories, explainers, ads
- Camera movement and motion design for AI video
- Platform-specific video optimization (TikTok, YouTube, Instagram, LinkedIn)
- Higgsfield, Seedance, Kling, Sora, Veo, Wan, or any supported model
- Image generation with Soul, Nano Banana, Seedream, Flux, GPT Image

---

## MCP Servers — Live Generation (optional)

Maxim's skill files teach Claude HOW to write generation prompts. To actually GENERATE videos/images, connect a Higgsfield MCP server:

### Option A: higgsfield-mcp (Python — pip install)
```bash
pip install higgsfield-mcp
claude mcp add higgsfield -s user -e HIGGSFIELD_API_KEY=your-key -e HIGGSFIELD_SECRET=your-secret -- higgsfield-mcp
```
Tools: `generate_image_soul`, `generate_video_dop`, `generate_speech_video`, `get_soul_styles`, `get_motions`, `create_character`, `get_job_status`
Source: [geopopos/geo_higgsfield_ai_mcp](https://github.com/geopopos/geo_higgsfield_ai_mcp)

### Option B: higgsfield-mcp (Bun/TypeScript)
```bash
git clone https://github.com/jfikrat/higgsfield-mcp.git
cd higgsfield-mcp && bun install
claude mcp add higgsfield -s user -- bun run src/index.ts
```
Tools: `higgsfield_generate_image`, `higgsfield_generate_video`, `higgsfield_wait_for_job`, `higgsfield_list_models`, `higgsfield_check_cost`
Source: [jfikrat/higgsfield-mcp](https://github.com/jfikrat/higgsfield-mcp)

### Without MCP (prompt-only mode)
If no MCP server is connected, Maxim writes the optimized prompt and the user pastes it into the Higgsfield/Seedance web UI manually. All 15 styles, MCSLA formula, camera vocabulary, and platform specs still work — just no automated generation.

### API Key
Get credentials at: https://platform.higgsfield.ai

---

## Skill Libraries

### Maxim-authored Cinematic Styles (15 skills) — Maxim's original IP
Path: `.claude/skills/ai-media-generation/cinematic-styles/`
Coverage: 15 model-agnostic behavioral-framework-engineered cinematic styles. Each ships with a primary behavioral framework (Hook Model, AIDA, Peak-End Rule, Endowment Effect, Hero's Journey, Mirror Neurons, etc.) translated into specific cinematic structure for specific business outcomes (sales, lead gen, commitment, trust, purchase).

Entry point: `cinematic-styles/README.md` (moat framing + dispatch logic)

**Predecessor:** these styles replaced the retired `community-packs/higgsfield-ai-prompts/` subtree (no-license content) in v1.0.0 with Maxim-authored equivalents that carry defensible IP. See `cinematic-styles/README.md` §6 for attribution notes.

### External: higgsfield-ai-prompt-skill (20 sub-skills) — MIT vendored
Path: `community-packs/higgsfield-ai-prompts/`
Coverage: Model selection, camera, motion, audio, pipeline, prompt formula, image generation, troubleshooting, moodboards, recipes, style, and more.
License: MIT (O-Side Media). Technical reference vocabulary — no behavioral-moat framing; Maxim wraps its use via dispatch logic.

Entry point: `community-packs/higgsfield-ai-prompts/SKILL.md`

### External: awesome-gpt-image-2 (GPT-Image-2 structured prompt library) — MIT vendored
Path: `community-packs/awesome-gpt-image-2/`
Coverage: 21 industrial fill-in-the-blank prompt templates + a structured **atomic schema** (subject/task · composition/layout · style/materials · lighting · info-hierarchy) + 500+ reverse-engineered GPT-Image-2 cases across UI · charts/infographics · posters · brand · product · character · scene · document images.
License: MIT (freestylefly). Templates + galleries stay upstream (referenced, not mirrored — see the pack's `MAXIM_INTEGRATION.md`). Prompt-engineering reference — no behavioral-moat framing on its own.
Entry point: `community-packs/awesome-gpt-image-2/MAXIM_INTEGRATION.md`

### Maxim Overlay — Image Generation (GPT-Image-2) 🟢 (the moat on top)
When an image-generation task activates (triggers: image generation · GPT Image · poster · infographic · UI mockup · product image · brand image), do NOT emit a raw template. Compose through the overlay:

1. **Atomic schema (controllability — from the pack):** fill subject/task · composition/layout · style/materials · lighting · info-hierarchy · output-spec (ratio · resolution · text legibility). Structured beats prose for batch + reuse.
2. **Behavioral framing (ADR-007 — cite the framework):** apply the visual-behavior framework that fits the goal — **pre-attentive attributes** (colour/size/orientation for what must be seen first), **visual hierarchy** + **Gestalt** (grouping, single focal point), **Color Psychology** (palette → intended emotion/action), **Fitts' Law** + **Nielsen heuristics** for UI mockups, **AIDA / Peak-End** for ad creative. State which framework drove the composition.
3. **Brand-foundation voice (three-layer):** load `.brand-foundation/personal/` (+ operator + startup overlays); the palette, type, tone, and any embedded copy must pass the brand + `ai-tells` checks — on-brand, not generic-AI-look.
4. **Compliance / ethics:** CSO auto-loop on regulated / person-likeness / third-party-logo content; no deepfake-class person swap without consent.
5. **Confidence tag (ADR-010):** 🟢 only when schema + framework + brand all applied; 🔴 Maxim-UNENHANCED if a raw upstream template is used verbatim.

**Generation (Layer 3 — future, gated):** to produce pixels, a `mxm-image` MCP would call the image API (OpenAI images or an aggregator) — Maxim is model-agnostic (`Maxim_MODEL_PROVIDER=openai`), API key in Doppler. Not built today; this skill writes the governed prompt and the operator generates via their tool (or a connected higgsfield/image MCP).

---

## Sub-Skill Routing

### Maxim Cinematic Styles (15) — primary prompt generation

| Task Signal | Business Outcome | Style Path |
|---|---|---|
| Cinematic / film / movie scene / brand film | Commitment + emotional brand alignment | `cinematic-styles/cinematic/` |
| 3D CGI / 3D animation / premium product render | Purchase confidence + premium positioning | `cinematic-styles/cgi-3d/` |
| Cartoon / 2D animation / explainer | Learning retention + brand affinity | `cinematic-styles/cartoon/` |
| Comic to video / motion comic / episodic | Narrative engagement + series commitment | `cinematic-styles/comic-to-video/` |
| Fight / action / combat / game trailer | Arousal → sales lift | `cinematic-styles/fight-scenes/` |
| Motion design / kinetic type / explainer ad | Comprehension → conversion | `cinematic-styles/motion-design-ad/` |
| E-commerce / product ad / direct response | **DIRECT PURCHASE** (primary sales) | `cinematic-styles/ecommerce-ad/` |
| Anime / Japanese animation / youth market | Tribe identity + loyalty | `cinematic-styles/anime-action/` |
| Product 360 / turntable | Pre-ownership → purchase intent | `cinematic-styles/product-360/` |
| Music video / performance / artist | Cultural brand equity + identity alignment | `cinematic-styles/music-video/` |
| Social hook / TikTok / Reels / Shorts | **LEAD GEN** (top-of-funnel acquisition) | `cinematic-styles/social-hook/` |
| Brand story / mission / founder film | Long-form commitment + mission alignment | `cinematic-styles/brand-story/` |
| Fashion / lookbook / editorial | Aspirational desire → premium purchase | `cinematic-styles/fashion-lookbook/` |
| Food & beverage / ASMR / restaurant | **CRAVING → ORDER** (primary sales) | `cinematic-styles/food-beverage/` |
| Real estate / property / architectural | Showing request + offer (high-value lead gen) | `cinematic-styles/real-estate/` |

### Technical Sub-Skills (20)

| Sub-Skill | Domain | Path |
|---|---|---|
| higgsfield-camera | Camera movements & angles | `community-packs/higgsfield-ai-prompts/mnt/user-data/outputs/higgsfield/skills/higgsfield-camera/` |
| higgsfield-motion | Motion presets & dynamics | `community-packs/higgsfield-ai-prompts/mnt/user-data/outputs/higgsfield/skills/higgsfield-motion/` |
| higgsfield-audio | Audio design & sound cues | `community-packs/higgsfield-ai-prompts/mnt/user-data/outputs/higgsfield/skills/higgsfield-audio/` |
| higgsfield-pipeline | Generation pipeline & workflow | `community-packs/higgsfield-ai-prompts/mnt/user-data/outputs/higgsfield/skills/higgsfield-pipeline/` |
| higgsfield-prompt | Prompt formula & structure | `community-packs/higgsfield-ai-prompts/mnt/user-data/outputs/higgsfield/skills/higgsfield-prompt/` |
| higgsfield-image-shots | Image generation & shot design | `community-packs/higgsfield-ai-prompts/mnt/user-data/outputs/higgsfield/skills/higgsfield-image-shots/` |
| higgsfield-models | Model selection & comparison | `community-packs/higgsfield-ai-prompts/mnt/user-data/outputs/higgsfield/skills/higgsfield-models/` |
| higgsfield-cinema | Cinema techniques & language | `community-packs/higgsfield-ai-prompts/mnt/user-data/outputs/higgsfield/skills/higgsfield-cinema/` |
| higgsfield-style | Visual style & color grading | `community-packs/higgsfield-ai-prompts/mnt/user-data/outputs/higgsfield/skills/higgsfield-style/` |
| higgsfield-soul | Soul ID / Soul Cast / Soul HEX | `community-packs/higgsfield-ai-prompts/mnt/user-data/outputs/higgsfield/skills/higgsfield-soul/` |
| higgsfield-seedance | Seedance-specific features | `community-packs/higgsfield-ai-prompts/mnt/user-data/outputs/higgsfield/skills/higgsfield-seedance/` |
| higgsfield-moodboard | Moodboard creation | `community-packs/higgsfield-ai-prompts/mnt/user-data/outputs/higgsfield/skills/higgsfield-moodboard/` |
| higgsfield-recipes | Genre recipe templates | `community-packs/higgsfield-ai-prompts/mnt/user-data/outputs/higgsfield/skills/higgsfield-recipes/` |
| higgsfield-vibe-motion | Vibe-driven motion presets | `community-packs/higgsfield-ai-prompts/mnt/user-data/outputs/higgsfield/skills/higgsfield-vibe-motion/` |
| higgsfield-mixed-media | Mixed media compositing | `community-packs/higgsfield-ai-prompts/mnt/user-data/outputs/higgsfield/skills/higgsfield-mixed-media/` |
| higgsfield-apps | App integrations | `community-packs/higgsfield-ai-prompts/mnt/user-data/outputs/higgsfield/skills/higgsfield-apps/` |
| higgsfield-assist | Assistant / help utilities | `community-packs/higgsfield-ai-prompts/mnt/user-data/outputs/higgsfield/skills/higgsfield-assist/` |
| higgsfield-recall | Memory & recall system | `community-packs/higgsfield-ai-prompts/mnt/user-data/outputs/higgsfield/skills/higgsfield-recall/` |
| higgsfield-troubleshoot | Troubleshooting & debugging | `community-packs/higgsfield-ai-prompts/mnt/user-data/outputs/higgsfield/skills/higgsfield-troubleshoot/` |
| shared | Shared utilities & templates | `community-packs/higgsfield-ai-prompts/mnt/user-data/outputs/higgsfield/skills/shared/` |

### Retired in v1.0.0: Automation Skills (4)

The previously-vendored Playwright browser-automation skills (higgsfield-image-auto, seedance-auto-generate, ugc-hot-girl, ugc-video-auto) were retired in v1.0.0. Platform-specific website automation belongs to each platform's own tooling ecosystem, not to Maxim's IP portfolio. Users needing direct higgsfield.ai browser automation should install upstream tooling separately.

Maxim's role remains: **generate the behaviorally-engineered prompt** (model-agnostic). Delivery automation is a separate concern with different lifecycle considerations.

---

## Behavioral Layer

### Maxim Confidence Tagging
- **🟢 HIGH** — Style-matched skill activated, MCSLA formula applied, platform specs validated
- **🟡 MEDIUM** — General video/image prompt generated without style-specific skill
- **🔴 LOW** — Raw prompt pass-through, no formula or platform optimization applied

### Compliance Flags for Ad Content
- **Ad disclosures:** Flag when generated content requires FTC/ASA ad disclosure
- **Brand safety:** Validate content against brand guidelines before generation
- **Platform terms:** Flag content that may violate TikTok/Instagram/YouTube community guidelines
- **IP/likeness:** Flag when prompts reference real people, brands, or copyrighted works

### Proactive Agent Loops
- Loop `brand-guardian` when brand assets or brand voice are involved
- Loop `content-strategist` for content calendar alignment
- Loop `compliance` skill when generating ad/commercial content
- Loop `security-analyst` when generating content involving PII or likeness

---

## Core Prompt Formula: MCSLA

All video prompts should follow the **MCSLA** structure:

```
[Model] + [Camera] + [Subject] + [Look] + [Action]
```

- **Model:** Which AI model to use (Kling 3.0, Sora 2, Veo 3.1, Wan 2.7, Seedance 2.0, etc.)
- **Camera:** Named camera movement preset (Dolly In, FPV Drone, 360 Orbit, etc.)
- **Subject:** Who/what is in frame, with specific observable details
- **Look:** Visual style, color grade, lighting, aspect ratio
- **Action:** What changes, what moves, what happens (verbs, not adjectives)

For images, use the image prompt formula:
```
[Shot size] + [Angle] + [Movement keyword] of [subject]. [Pose]. [Environment]. [Lighting]. [Style].
```

Full formula reference: `references/prompt-formula.md`

---

## Platform Optimization

| Platform | Aspect | Hook Window | Duration | Notes |
|---|---|---|---|---|
| TikTok | 9:16 | 0.8s | 15-60s | Pattern interrupt in frame 1, trending audio, completion rate is king |
| YouTube Shorts | 9:16 | 2s | up to 60s | Slightly more tolerance, still mobile-first |
| Instagram Reels | 9:16 | 1.5s | 15-90s | Aesthetic-first, visual polish matters more |
| LinkedIn | 16:9 OK | 2s | 30-120s | Professional tone, insight-driven hook, subtitles required |
| YouTube Standard | 16:9 | 2s | any | Cinematic OK, longer storytelling, SEO title/description matter |

Full specs: `references/platform-specs.md`

---

## 2-Second Hook Framework

Every video prompt MUST address the first 2 seconds explicitly. Proven hook patterns:

1. **Extreme Close-Up Snap to Wide Reveal** — disorientation then context
2. **Black Screen to Dramatic Light Burst** — silence then explosion
3. **Reverse Motion** — unnatural movement catches the brain
4. **Unexpected Scale** — macro of familiar object reads as landscape
5. **Silent Beat Then Explosive Sound** — audio contrast
6. **Extreme Color Shift** — palette punch in 0.6s
7. **Fast Movement Entering Frame** — motion catches peripheral vision
8. **Extreme Depth-of-Field Rack Focus** — professional cinema technique
9. **Stark Geometric Contrast** — visual tension
10. **Protagonist's Eyes Open** — primal human attention grab
11. **Disorienting Camera Rotation** — sensory engagement
12. **Scale Impossibility** — tiny in vast or huge in small

Advanced: Stack 2-3 hooks in the opening 2 seconds for maximum impact.

---

## Quick Reference Files

| File | Purpose |
|---|---|
| `references/style-guide.md` | All 15 styles — when to use each |
| `references/camera-vocabulary.md` | Camera movement vocabulary |
| `references/platform-specs.md` | Platform optimization specs |
| `references/prompt-formula.md` | MCSLA formula and prompt templates |

---

## External Reference Files

| File | Purpose |
|---|---|
| `community-packs/higgsfield-ai-prompts/vocab.md` | Full cinematic vocabulary (camera, shot size, style, lighting, audio) |
| `community-packs/higgsfield-ai-prompts/model-guide.md` | Video + image model comparison tables |
| `community-packs/higgsfield-ai-prompts/image-models.md` | Image model specs, UI controls, pricing |
| `community-packs/higgsfield-ai-prompts/prompt-examples.md` | Production prompt examples by genre |
| `community-packs/higgsfield-ai-prompts/photodump-presets.md` | 29 Photodump style presets |

---
_Copyright (c) 2026 iSystematic Inc. Maxim product. BSL 1.1._
