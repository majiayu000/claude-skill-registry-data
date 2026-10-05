---
name: make-pet-portrait
description: Create one stylized or photographic portrait of a supplied pet while preserving its distinctive markings, species traits, and proportions. Use for identity-faithful pet artwork from a real pet reference; do not use for inventing an animal, creating a human character, making a pet avatar set, or editing only the background.
---
# Make Pet Portrait

## Catalog

- Display name: Make Pet Portrait
- Categories: Character, Portrait
- Status: Ready
- Route label: GPT Image 2 consistency-sensitive edit
- Tone: amber
- Short description: Create one stylized or photographic portrait of a supplied pet while preserving distinctive markings and proportions.
## What this skill does

- Preserves species, facial structure, coat pattern, eye color and signature markings from pet references.
- Applies one declared portrait treatment without inventing accessories or changing breed traits.

## How to use

Provide pet photos, the pet name, desired portrait style, crop and background.

#### Example

```text
Create a dignified oil-painting portrait of this dog on deep green; preserve the white left-ear patch and amber eyes.
```

## Workflow

1. Identify pet-specific invariants across references and resolve conflicting views.
2. Choose one crop, expression, background and style; keep identity anchors explicit.
3. Run `gpt-image` v1.0 with `quality: "medium"`, `imageSize: "2K"`, the supplied references, the requested or source-preserving ratio, `batchCount: 1`, and one result.
4. Compare ears, muzzle, markings, eyes and proportions against the source.

## User-facing output

- Media type: One pet portrait
- Default quantity: 1
- Content per image: One recognizable pet in one portrait treatment
- Default layout: User-requested or source-preserving format
- Model policy: GPT Image 2 Medium/2K for consistency-sensitive final image editing
- Downstream use: Keepsakes and pet profiles
