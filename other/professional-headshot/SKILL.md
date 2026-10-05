---
name: professional-headshot
description: Turn one supplied portrait into one researched, identity-faithful professional headshot with channel-appropriate background, seated or standing posture, shoulder line, lighting, wardrobe, expression, crop, and safe area. Use for LinkedIn, company directories, speaker bios, resumes, press profiles, executive portraits, or team pages; research current channel and profession conventions before generation.
---

# Professional Headshot

## Catalog

- Display name: Professional Headshot
- Categories: Portrait
- Status: Ready
- Route label: GPT Image 2 consistency-sensitive edit
- Tone: rose
- Short description: Research the channel, then create a properly posed and lit professional portrait.
- Similar skills: id-photo-format, make-wallet-photo
## What this skill does

- Produces one professional portrait for one channel, role, market, and brand tone.
- Researches background, seated/standing pose, shoulders, expression, lighting, crop, safe area, and file rules before generation.
- Preserves recognizable identity, age, skin texture, hair, eye color, and distinguishing features.

## How to use

Provide one clear portrait plus the profession, channel, market, brand tone, and seated/standing preference.

#### Create a seated LinkedIn portrait

```text
Create a seated LinkedIn headshot for a product designer. Research the current channel and portrait conventions before choosing the background, posture, light, and crop.
```

## Workflow

1. Read `references/channel-research.md`; browse the current official channel requirement and current profession/market conventions. Record hard constraints separately from creative choices.
2. Bind pose, spine, torso angle, shoulder line, hands, gaze, expression, wardrobe, background type and luminance, key/fill/separation light, crop, headroom, face occupancy, and safe area.
3. Run `gpt-image` v1.0 with `quality: "medium"`, `imageSize: "2K"`, the supplied references, the requested or source-preserving ratio, `batchCount: 1`, and one result.
4. Preserve exact face, age, skin texture, hairline, eye color, and distinguishing marks. Forbid beauty-filter plasticity, age/face reshaping, fake credentials, extra people, logos, text, badges, cluttered backgrounds, harsh facial shadow, or ID-photo styling.
5. Inspect identity, spine and shoulder posture, hand placement, expression, eye focus, catchlights, natural skin, hair/background separation, wardrobe, crop, and circular-safe area. Retry only the failed property.

## User-facing output

- Media type: One researched professional portrait plus a compact requirement record
- Default quantity: 1
- Content per image: One person in one channel-appropriate seated, standing, or crop-only setup
- Default layout: Research-derived crop and safe area; no collage
- Model policy: GPT Image 2 Medium/2K for consistency-sensitive final image editing
- Downstream use: LinkedIn, team pages, company directories, bios, resumes, and press kits
