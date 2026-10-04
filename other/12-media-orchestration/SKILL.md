---
name: "media-orchestration"
description: "Section-by-section media planning and generation. Image generation (GPT Image 1.5 primary, built-in fallback), logo/icon generation (Ideogram v3 → favicon set), video generation (Sora), social preview images (OG 1200x630 + AI search optimization), stock photo curation (Pexels, Pixabay), critique/remix loops (max 3 rounds), asset compression pipeline, and media performance budgets."
metadata:
  version: "2.1.0"
  updated: "2026-05-03"
  context: "fork"
  effort: "high"
  model: "sonnet"
license: "Rutgers"
compatibility:
  claude-code: ">=2.0.0"
  agentskills: ">=1.0.0"
submodules:
  - 30-ideogram-methods.md
  - build-breaking-rules.md
  - compression-pipeline.md
  - image-optimization.md
  - image-profiling.md
  - lightbox-classifier.md
  - media-prompts.md
  - notebooklm-pipeline.md
  - og-image-generation.md
  - social-brand-hex.md
  - technical-diagramming.md
priority: 3
pack: "media"
stage: stable
triggers:
  - "image gen"
  - "dalle"
  - "media"
  - "og image"
paths:
  - "org:website_build"
---

# 12 — Media Orchestration

Plan and generate all site media section-by-section: images (GPT Image 1.5), logos (Ideogram v3), video (Sora), OG cards, and compression pipeline.

> **Model migration note (pass-77, 2026-06-09)**: `DALL-E` → **GPT Image 1.5** + `GPT-4o` → **GPT Image 2 vision**. Per `platform.openai.com/docs/deprecations`.

## Submodules

- **media-prompts** — prompt templates, Ideogram v3 API
- **compression-pipeline** — Python code, format tables, CF Image Transforms, CLS, broken image detection
- **og-image-generation** — Satori edge-rendered OG, KV / R2 cache, meta-tag helper
- **image-optimization** — Sharp processing, responsive srcset, WebP/AVIF, blur placeholders, R2 pipeline
- **image-profiling** — GPT Image 2 vision batch profiling
- **lightbox-classifier** — per-image eligibility: `kind!=logo` + ≥1024×768 + score≥7
- **social-brand-hex** — canonical brand-color map per social platform
- **notebooklm-pipeline** — per-site podcast via ElevenLabs Studio + infographic via Vega-Lite/Recraft/GPT-Image-2 + HeyGen video + CF Stream + RSS + JSON-LD + cost ceiling $3.50/site

## Strategy by Section

Hero → GPT Image 1.5 / Sora · Features → GPT Image 1.5 / SVG · How It Works → GPT Image 1.5 · Testimonials → stock · About → stock/real · Blog → GPT Image 1.5 · Social → Satori OG 1200×630 · Icons → Ideogram v3

Pre-gen checklist: communication goal? Brand style? Dimensions? Format? Budget? Stock or generated?

## Visual Inspection (MANDATORY)

Read every image before deploy. Check: blur, artifacts, watermarks, wrong colors, AI hallucinations, gibberish text. Fail = regenerate w/ improved prompt. Quality bar: 2× retina, no artifacts, brand palette, consistent style, no uncanny valley.

## Brian's Style

- Space/cosmic — `#00E5FF` + `#7C3AED`, deep black (`#060610`); connections/dots — quantum, neural, constellation
- "Ultra realistic" scenes; transparent logos; simpler always; motifs — squirrels, turtles

## Image Generation

- **GPT Image 1.5** preferred (best quality); **GPT Image 1** for speed; **GPT Image 1-mini** for bulk/drafts
- Fallback: `scripts/image_gen.py`; product screenshots: Playwright on live URL
- Be specific: include colors, specify avoidances

## GPT Image 1.5 First Slot-Fill (CANONICAL — UNIVERSAL)

PRIMARY originator for every slot real-entity sources (Places / uploads / scrape) didn't fill. GPT Image 1.5 invoked BEFORE generic stock; stock APIs run parallel speed-pass fallback (instant return if GPT Image 1.5 hangs >15s). See skill 15 `media-acquisition` + Fail-CLOSED auto-regenerate (5 attempts, $0.40 worst-case ceiling per slot).

## Per-Slot Prompt Mandatory Fields (BUILD-BREAKING — `validate-image-prompts.mjs` + `validate-dalle-slot-fill.mjs`)

Every GPT Image 1.5 call MUST encode 6 fields from `_media_slots.json`:

1. Page topic + intent verbatim from `topic_intent`
2. Brand palette tokens from `_brand.json.colors` (inline hex)
3. Composition + aspect ratio matching `aspect`
4. Subject specificity (NEVER "people" — always "octogenarian volunteer plating soup, soft window light, documentary style")
5. Photographic technical specs (camera, lens, lighting, DoF — "shot on Hasselblad, 85mm prime, golden hour, shallow DoF")
6. Negative prompt block ("no text, no watermarks, no logos, no extra fingers, no AI artifacts, no stock-photo cliches")

Generic prompts FAIL validator. Same template applies to FLUX, Recraft, Stability.

## Fail-CLOSED Auto-Regenerate (BUILD-BREAKING — `validate-no-empty-slots.mjs`)

Every slot MUST end build w/ `filled_url != null AND filled_score >= relevance_floor` (default 8/10 via GPT Image 2 vision). Failure modes (Pexels empty, NSFW-flagged, broken scrape, vision below floor) → immediate re-gen w/ REFINED prompt — NEVER silent skip, NEVER substitute brand-gradient unless 5 attempts exhausted. `media_pipeline_orchestrator` sub-agent owns this loop. See `media-acquisition.md` § Fail-CLOSED chain.

## Logo / Icon / Video / OG

- **Logo** — Ideogram v3 (best text rendering); **Icons** — Recraft V3; output: PNG transparent + SVG; bg removal → favicon set (16/32/180/192/512 + maskable); brand mark MUST be vector-clean
- **Video** — Sora (primary cinematic); Veo (narrative stitching, 7-8 × 8-sec clips → 60-sec arc); HeyGen (explainer/spokesperson); captions VTT + transcript; `prefers-reduced-motion` → static poster fallback
- **OG (1200×630)** — Satori edge-rendered, per-route unique, BRANDED CARD never raw photo, ≤100KB, cached KV 7d / R2 forever

## Stock Photography + Asset Compression + Performance

**Stock**: Pexels first (free, API); Pixabay second. Never Unsplash (generic), iStock/Getty (paid). Critique-and-remix loop max 3 rounds; AI vision <7/10 = reject + regenerate.

**Compression**: AVIF primary (94% browser support, 20-30% smaller than WebP); WebP fallback (Safari 14+); JPEG legacy. Sharp: 320/640/1280/1920w srcset; blur placeholder; dominant color → CSS bg fill. R2 upload per-extension content-type.

**Budgets**: total images/page ≤500KB; largest single ≤200KB; Hero LCP `fetchpriority="high"` + preload; `loading="lazy"` + `decoding="async"` on all others.

## See submodules for: media-prompts, compression-pipeline, og-image-generation, image-optimization, image-profiling, lightbox-classifier, social-brand-hex, notebooklm-pipeline, build-breaking-rules.
