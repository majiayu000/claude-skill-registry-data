---
name: regen-character-art
description: >
  Generate or regenerate ReGen Civics character illustrations (the 13
  stewardship roles + any new ones added each season). Wraps the
  nano-banana-pro skill with the canonical solarpunk-elven-jedi style
  guide from docs/planning/CLAUDE_CODE_PROMPT_2026-04-03_CHARACTER_ART.md. Produces
  card portraits and full scenes that match the existing 13 in style,
  palette, and energy. Triggers on: "character art", "role illustration",
  "season character", "regenerate the [role] art", "new role artwork",
  "character portrait", "card portrait", "scene image for [role]",
  "fix the [role] illustration", "generate character", "stewardship role
  art", or any request to create or update an in-game character image.
---

# ReGen Civics Character Art

## What this skill does

Take a stewardship role concept (existing or new) and produce two
images: a card portrait (character-only, soft gradient or transparent,
no text) and a full scene (character in a solarpunk environment with
their name as the only text). Matches the established style of the
13-role pantheon so additions and updates don't drift.

Always invoke the `nano-banana-pro` skill for the actual generation;
this skill is the style-and-content layer on top.

## The non-negotiable style anchor

Every prompt opens with this exact preamble. Without it, the panel
drifts in style.

```
Solarpunk meets elven meets jedi meets regenerative future. A world
that already healed. Rivendell built by permaculture designers with
solar panels woven into living architecture. Studio Ghibli's future
earth. Moss-covered technology. Bioluminescent accents. Flowing
fabrics with circuitry patterns. Living wood merged with soft-glowing
interfaces. Crystal and mycelium and sunlight, not leather and iron and
torchlight.

Color palette: Deep forest greens, warm golds, bioluminescent teals
and cyans, sunrise amber, living wood browns, soft white light. NOT
medieval browns and grays. The world is green and alive and lit from
within.

Style: illustrated character design with hand-painted quality. Warm,
inviting, detailed but not photorealistic. Technology and nature are
indistinguishable. Tools are grown, not forged. Clothing woven from
living fibers. Architecture is part tree, part crystal, part solar
membrane. Every surface has signs of life growing on or through it.
```

This preamble is verbatim from the canonical CHARACTER_ART spec. Don't
paraphrase. Don't shorten. Don't add adjectives.

## The two image formats

### Card portrait

- Character only, no scene
- Soft gradient background (warm green-to-gold) OR transparent
- Standing pose, full body or 3/4 body
- Clean edges (will be composited onto dark card backgrounds with
  HTML-rendered titles below the image)
- NO text on the image. Not the role name. Not the tagline. Nothing.
- Resolution: 2K
- Filename: `[slug]-card.webp`
- Path: `client/public/images/roles/`

### Full scene

- Character on the left or center of a solarpunk landscape
- 16:9 ish landscape aspect ratio
- Character name appears as one simple, clean label on the image (e.g.
  `- THE GARDENER -`)
- NO tagline text. NO "Character Select" header. NO subtitle.
- Resolution: 2K
- Filename: `[slug]-scene.webp`
- Path: `client/public/images/roles/`

## The mandatory life elements

Every scene MUST include both:

1. **Visible fruiting plants.** Berry bushes (raspberry, blueberry,
   blackberry, currant), fruit trees (apple, fig, citrus, persimmon,
   cherry), gourds, pomegranates, grapes, kiwi, passionfruit. Pick at
   least 2-3 species per scene. Real edible food, visibly abundant.

2. **At least one or two animals or creatures.** Songbirds, deer,
   foxes, rabbits, butterflies, dragonflies, bees, frogs, owls,
   hummingbirds, small lizards, geckos, cats, tortoises. Comfortable
   around people. Part of the scene, not background filler.

This rule exists because the existing 13 scenes all have it. Adding a
new scene without abundance + wildlife will read as sterile and break
the set's coherence.

## Character diversity rules

Across the full pantheon, vary:

- Skin tones (deep brown, warm olive, copper, pale freckled, rich dark,
  warm tan, etc.)
- Body types (sturdy, tall and graceful, sharp-featured, soft-bodied,
  young, older with silver hair)
- Ages (mix of younger and older, including elders with silver hair /
  silver locs)
- Genders and presentations (masculine, feminine, androgynous)
- Hair (braids, locs, curly, short, long, woven with vines or flowers)
- Pointed ears on some characters but not all (elven touch)
- Subtle bioluminescent freckles or markings on some

When adding a NEW role, check the existing 13 first (see the canonical
spec for the full roster). Pick attributes that fill gaps in the
diversity matrix, not duplicates.

## Costume direction (binding)

- Flowing robes, tunics, or capes. Not armor. Not modern streetwear.
- Living-thread embroidery, mycelium patterns, circuitry-woven-into-
  fabric details
- Practical accessories that are TOOLS, not weapons (orbs, holographic
  workstations, balance scales of light, living-wood staffs, crystalline
  tools, glowing markers)
- Bare feet on moss, sandals with vine straps, or comfortable walking
  boots with moss-cushion soles. No leather boots, no heels.
- Subtle bioluminescent accents on jewelry, fabric, or skin

## Scene direction (binding)

- Always golden hour light. Sunset / sunrise. Warm.
- Living architecture: treehouses, mycelium networks, woven solar
  membrane canopies, crystal-and-wood structures
- Bioluminescence: vines, fungi, pathways, freckles. Soft glow, not
  sci-fi neon
- Background depth: foreground plants, midground architecture, distant
  canopy or valley vista
- A subtle nod to the role's craft: gardener has seasonal wheel,
  treasury keeper has balance scale, weaver has bridge of light, etc.

## When generating a NEW role

The 13 canonical roles are in `docs/planning/CLAUDE_CODE_PROMPT_2026-04-03_CHARACTER_ART.md`.
Before generating a new one:

1. **Read the canonical spec.** All 13 entries. Note the slug, tagline,
   character description, scene background, and scene text format.
2. **Pick the role's archetype.** Is this a guide, a maker, a keeper, a
   weaver, a witness, a builder? Each archetype has visual cues.
3. **Pick the role's craft.** What single object or environment makes
   this role legible? (For "The Gardener" it's the seasonal wheel.
   For "The Keeper" it's the balance scale.)
4. **Pick diversity attributes** that fill gaps in the existing 13.
5. **Draft the description** using the same line structure as the
   canonical entries: skin / hair / clothing / craft-object / pose /
   expression.
6. **Draft the scene** including the mandatory fruiting plants and
   animals plus a setting that matches the role's craft.
7. **Generate** via the nano-banana-pro skill at 2K resolution.
8. **Convert** to WebP with `cwebp -q 85 input.png -o output.webp`.

## When REGENERATING an existing role

When Rye says "the Gardener art doesn't feel right" or similar:

1. **Find the existing files.** `client/public/images/roles/[slug]-card.webp`
   and `[slug]-scene.webp`.
2. **Read the canonical entry** in docs/planning/CLAUDE_CODE_PROMPT_2026-04-03_CHARACTER_ART.md.
3. **Ask Rye** what specifically isn't working. Pose? Color palette?
   Setting? Tone? (One AskUserQuestion call, max 2 questions.)
4. **Adjust the prompt** by changing the specific element while keeping
   the style anchor and character description identical.
5. **Generate the new pair.** Save with the same slugs (overwrite).
6. **Compare side-by-side** with the rest of the roster before declaring
   done; the regen mustn't make this character drift away from the set.

## When generating MULTIPLE roles

If asked for multiple at once (e.g. "generate 4 new seasonal roles"),
batch them:

1. Lock the style preamble + diversity matrix planning first
2. Generate all card portraits in one batch run
3. Generate all scenes in a second batch
4. Convert all to WebP at once
5. Place all into `client/public/images/roles/`
6. Add to the role registry in `client/src/data/teamData.ts` (or
   wherever the season's role list lives) once the art lands

## Voice rules for any text on the image

The only text on a scene image is the character name in this format:
`- THE [NAME] -` with em-dash-LIKE characters that are actually hyphens
or en-dashes.

WAIT. The em-dash ban is project-wide. Re-read the canonical spec.
The format `- THE GARDENER -` uses a HYPHEN-MINUS, not an em-dash. This
is fine and matches the established 13.

Don't introduce em-dashes anywhere else (filename, alt text, registry
entry, etc.). Project rule.

## Output checklist

When the skill completes, return:

- [ ] Card portrait at `client/public/images/roles/[slug]-card.webp`
      (2K, WebP)
- [ ] Scene image at `client/public/images/roles/[slug]-scene.webp`
      (2K, WebP)
- [ ] Both pass visual coherence check vs. the existing roster
- [ ] Role registry entry updated in `client/src/data/teamData.ts`
      (or wherever the season's role list lives) with slug, title,
      tagline, image references
- [ ] Optional: a short alt text + caption draft for accessibility

## Cross-references

- `nano-banana-pro` for the actual image generation
- `docs/planning/CLAUDE_CODE_PROMPT_2026-04-03_CHARACTER_ART.md` for the canonical
  style guide and the 13 existing role specs
- `regen-seasonal-roles` skill for evolving the role roster across
  seasons
- `regen-background-design` for full-page background art (different
  context, different style anchor)
- Visual reference: existing files in `client/public/images/roles/`
