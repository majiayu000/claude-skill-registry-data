---
name: id-photo-format
description: Prepare one supplied portrait for one explicitly named ID-photo or passport-photo specification using current issuing-authority research, neutral capture correction, measured crown-to-chin cropping, exact dimensions, background, format, and DPI. Use for passport, visa, license, school, application, or print preparation; never assume universal ear, crop, lighting, or AI-edit rules and never fabricate identity.
---

# ID Photo Format

## Catalog

- Display name: ID Photo Format
- Categories: Portrait
- Status: Ready
- Route label: Official-rule research plus WeShop and measured crop
- Tone: rose
- Short description: Research the authority, correct the capture, then crop around the measured head.

- Similar skills: make-wallet-photo, professional-headshot
## What this skill does

- Produces one exact ID-photo file for one named authority and document type.
- Researches current official crop, ear/face visibility, lighting, background, expression, and alteration rules before editing.
- Scales and crops around the crown-to-chin measurement instead of shrinking the complete input photo.
- Preserves identity and rejects beauty editing, facial reconstruction, or unsupported compliance claims.

## How to use

Name the country, issuing authority, document, and submission/print channel; or provide the complete official specification.

#### Prepare a researched ID photo

```text
Prepare this portrait for the named passport application. Find the current official rules first, then return the exact crop and a compliance record.
```

## Workflow

1. Read `references/authority-research.md` and browse the current issuing authority's official source. Record every required field and whether AI or digital alteration is allowed. If prohibited, stop before generation and provide capture/crop guidance only.
2. Inspect the source. Reject blur, insufficient resolution, severe pose, covered eyes/facial edges, clipped head, or lighting that cannot be corrected without reconstructing identity.
3. Build a neutral capture contract: full-front head, level gaze, required expression, both facial edges visible, ears visible only when the official rule requires them, natural skin tone, uniform exposure, and no face or background shadow.
4. Use GPT Image 2 Medium/2K only for a non-submission preview or where the authority permits the required correction. Never beautify, reshape, invent facial details, or imply official acceptance.
5. Measure the crown-to-chin box and run `scripts/format_id_photo.py` with official head-height and top-margin ratios. The script owns final scaling, crop, dimensions, background fill, and DPI.
6. Re-open the file and verify pixels, DPI, head ratio, top margin, centering, facial-edge/ear rule, shoulders, background color, exposure, shadow, expression, and identity against the recorded source.

## User-facing output

- Media type: One exact-size ID-photo file plus official-source and compliance record
- Default quantity: 1
- Content per image: Crown, full face, neck, and authority-required shoulder area; no full-body shrink
- Default layout: Authority-defined measured head crop; no collage or print sheet unless requested separately
- Model policy: GPT Image 2 Medium/2K only when alteration is permitted; deterministic measured crop always owns final geometry
- Downstream use: Application preparation subject to issuing-authority review
