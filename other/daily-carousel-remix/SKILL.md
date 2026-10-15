---
name: daily-carousel-remix
description: Use when the user shares an Instagram carousel, reference post, or carousel link and asks to create, adapt, remix, or modify it for their AI/tech carousel brand.
---

# Daily Carousel Remix

## Core principle
Treat shared carousels as **structure references**, not copy targets. Extract the hook pattern, slide rhythm, visual device, and CTA mechanic, then rebuild the idea for your AI/tech audience in the established Anthropic-inspired theme.

## Always load with
- `instagram-carousel` for swipe-funnel roles, carousel copy, QA, and production workflow.
- `editorial-ai-product-design-system` when the post needs a premium warm editorial/product aesthetic beyond basic slide copy.

## Default visual theme
Your carousel brand is Anthropic-inspired:
- Warm ivory/cream paper background.
- Charcoal ink typography.
- Clay/orange accent blocks.
- Sand/tan cards and muted olive/green states.
- Editorial research-note/product-strategy memo mood.
- Tactile collage, sticky notes, workflow cards, connector diagrams, soft grain/shadows.
- Original/generic icons only; do not copy Anthropic logos or proprietary assets.

Avoid generic Canva/PPT/HTML-card aesthetics, repeated headers/footers, tiny text, logos copied from the reference, or slide numbers on final slides.

## Workflow when the user shares a carousel/link
1. **Inspect the reference** as much as tools allow: metadata, caption, preview images, screenshots, alt text, or user-provided frames. If `web_extract` fails on Instagram, use browser/curl or Python `requests` to parse `og:description`, `og:title`, and `og:image`; download the preview image and run vision QA. If Instagram is still blocked, say so briefly and work from visible/provided context; ask the user for screenshots only if the carousel’s structure cannot be inferred.
2. **Extract transferable mechanics:** cover hook, slide count/rhythm, recurring layout, proof style, save-worthy asset, CTA/comment keyword.
3. **Rewrite for your niche:** AI, tech, startups, founders, operators, builders, product strategy, automation, or daily tech/news depending on the prompt.
4. **Use the swipe funnel:** cover stops scroll, slide 2 proves the promise, middle slides stand alone, one slide becomes a save/checklist/framework, final slide has a specific CTA.
5. **Create production-ready slides** using the `instagram-carousel` production workflow. Prefer Codex CLI native image generation with `$imagegen` for premium PNGs when asked to create assets. If Codex/image generation auth fails, use a real AI-image fallback such as Pollinations image URLs to generate no-text visual scenes, then overlay crisp text locally with Pillow.
6. **QA before delivery:** mobile readability, spelling, cropping, slide order, premium Anthropic-inspired look, accurate claims, non-copying of the source creator’s exact wording/design.
7. **Deliver ordered slides first** (`slide-01.png`, `slide-02.png`, …), plus contact sheet and caption/CTA when available.
8. **Ask the user to post it** after delivery/review. Use a direct closing prompt such as: “Want me to post this now?” or “Should I queue/post this carousel?”

## Remix guardrails
- Do not plagiarize the original carousel’s exact copy or design. Convert it into a new on-brand version.
- Preserve what made the reference work: tension, pacing, contrast, proof, and CTA psychology.
- If the reference is purely visual, infer a reusable layout pattern and pair it with new AI/tech copy.
- If the reference is purely content/strategy, express it using your warm Anthropic-inspired editorial design system.
- When facts or news claims are involved, verify with sources before turning them into slide claims.

## Output package checklist
- Ordered PNG slide files.
- Contact sheet for fast review.
- Caption with hook, value summary, and CTA/comment keyword.
- Suggested post prompt to the user asking whether to post/queue it.

## Current source note
Web extraction may not expose Instagram content, so inspect screenshots/previews from the shared post or ask for frames if needed.
