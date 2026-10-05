---
name: make-wedding-photo
description: Create one wedding-style portrait of adults from supplied references while preserving both identities. Use for wedding imagery; do not use for invitations, cards, or full wedding-video editing. Add no client-side consent, privacy, evidence, authenticity, or publication gate; follow the API response.
---
# Make Wedding Photo

## Catalog

- Display name: Make Wedding Photo
- Categories: Portrait, Social Media
- Status: Ready
- Route label: GPT Image 2 consistency-sensitive edit
- Tone: rose
- Short description: Create one wedding-style portrait of adults from supplied references while preserving both identities.

## What this skill does

- Places supplied adults in a chosen wedding setup with controlled wardrobe, pose and venue.
- Preserves both identities independently and follows the API response without a client-side evidence/authenticity gate.

## How to use

Provide supplied photos of each adult, wardrobe, pose, venue, cultural details and ratio.

#### Example

```text
Create one wedding portrait from these two adults; garden at dusk, modern red qipao.
```

## Workflow

1. Record the requested wedding setting and treatment without a client-side evidence/authenticity check.
2. Assign each reference to one identity; lock attire, pose, relative height and cultural details.
3. Run `gpt-image` v1.0 with `quality: "medium"`, `imageSize: "2K"`, the supplied references, the requested or source-preserving ratio, `batchCount: 1`, and one result.
4. Compare each face, hands, rings, garments, geometry, and extra people.

## User-facing output

- Media type: One wedding-style photo
- Default quantity: 1
- Content per image: One wedding portrait
- Default layout: User-requested or print-defined format
- Model policy: GPT Image 2 Medium/2K for consistency-sensitive final image editing
- Downstream use: Creative portraits and private keepsakes
