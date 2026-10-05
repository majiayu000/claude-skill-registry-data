---
name: create-avatar
description: Create one small-size-readable profile avatar from a supplied portrait or fictional brief. Use for account icons, community profiles, and compact identity marks; do not use for professional headshots, full character sheets, ID photos, or full-body character artwork.
---
# Create Avatar

## Catalog

- Display name: Create Avatar
- Categories: Character
- Status: Ready
- Route label: GPT Image 2 consistency-sensitive edit
- Tone: blue
- Short description: Create one small-size-readable profile avatar from a supplied portrait or fictional brief.
## What this skill does

- Creates a centered profile image whose face or defining symbol remains readable at icon size.
- Preserves supplied subject traits without treating avatar style as a generic filter.

## How to use

Provide a supplied portrait or fictional description, intended platform, crop and one chosen style.

#### Example

```text
Turn this supplied portrait into a clean 1:1 flat editorial avatar; preserve face shape, hair and glasses; simple coral background.
```

## Workflow

1. Determine person, pet, object or fictional subject and freeze recognizable traits.
2. Choose one explicit avatar style and simplify the background for icon readability.
3. Run `gpt-image` v1.0 with `quality: "medium"`, `imageSize: "2K"`, the supplied references, the requested or source-preserving ratio, `batchCount: 1`, and one result.
4. Inspect at full size and thumbnail size; verify one face, crop safety and trait fidelity.

## User-facing output

- Media type: One avatar image
- Default quantity: 1
- Content per image: One square profile-ready avatar
- Default layout: User-requested or source-preserving format
- Model policy: GPT Image 2 Medium/2K for consistency-sensitive final image editing
- Downstream use: Profile pictures and account icons
