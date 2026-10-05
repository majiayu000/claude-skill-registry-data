---
name: make-wallet-photo
description: Prepare one wallet-size print portrait from a supplied photo using a real print dimension, crop, and bleed specification. Use for small personal print photos with an explicit physical size; do not use for passports, official IDs, professional headshots, avatars, or unspecified digital resizing.
---
# Make Wallet Photo

## Catalog

- Display name: Make Wallet Photo
- Categories: Portrait
- Status: Ready
- Route label: GPT Image 2 consistency-sensitive edit
- Tone: blue
- Short description: Prepare one wallet-size print portrait from a supplied photo using a real print dimension, crop and bleed specification.
- Similar skills: id-photo-format, professional-headshot
## What this skill does

- Formats a portrait for a named wallet print size instead of guessing one universal dimension.
- Preserves the original face and checks crop, background and print layout without turning it into an ID photo.

## How to use

Provide a supplied portrait, printer or country size, finish, crop, sheet quantity and resolution.

#### Example

```text
Prepare one 2.5×3.5 inch wallet portrait at 300 dpi; chest-up crop, neutral background, preserve face and clothing.
```

## Workflow

1. Confirm exact printer or regional dimension, DPI, bleed and single-print or sheet output.
2. Choose crop and background adjustments while protecting face, hair, shoulders and aspect.
3. Run `gpt-image` v1.0 with `quality: "medium"`, `imageSize: "2K"`, the supplied references, the requested or source-preserving ratio, `batchCount: 1`, and one result.
4. Verify pixel dimensions, DPI metadata, crop, face fidelity, margins and print preview.

## User-facing output

- Media type: One wallet-size portrait file
- Default quantity: 1
- Content per image: One print-dimensioned portrait
- Default layout: User-requested or print-defined format
- Model policy: GPT Image 2 Medium/2K for consistency-sensitive final image editing
- Downstream use: Personal wallet prints
