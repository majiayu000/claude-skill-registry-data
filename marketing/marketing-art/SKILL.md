---
name: marketing-art
description: Plan and generate film key art, posters, thumbnails, title cards, social stills, banners, and platform-safe promotional images from approved visual identity and verified text.
disable-model-invocation: true
author: Alan Guice (Badgids)
license: Apache-2.0
---

# Marketing Art

## Workflow

1. Read visual bible, approved character/location references, campaign, trailer plan, and verified title/release facts.
2. Write `06_release/artwork/art_briefs.jsonl` for each required key-art, poster, thumbnail, banner, title card, or social still.
3. Give each brief exact aspect/dimensions, visual hierarchy, focal subject, text-safe areas, required text, forbidden text, reference IDs, and delivery role.
4. Use existing image-generation adapters and ComfyUI when rendering is requested.
5. Use exact-text workflows or post-layout methods when title spelling must be exact.
6. Route generated candidates through media QC and `asset-approval`.
7. Never fabricate festival laurels, critic quotes, ratings, logos, or release facts.

## Done

Every requested promotional still asset has a traceable brief and, when rendered, an approved media candidate.

## Reusable design system

When multiple promotional assets belong to one release, establish or read `06_release/artwork/design_system.json` through `design-system` before producing variants. Preserve title treatment, safe zones, typography roles, palette behavior, logo rules, reference priorities, and accessibility constraints across still and motion assets without imitating a living artist.

