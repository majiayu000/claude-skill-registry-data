---
name: blakean-scene
description: Convert abstract symbolic concepts into Blakean embodied scene prompts — Blake's 8 compositional patterns, body grammar, and figure types. Use when visualizing oracular or symbolic ideas as figures; for ink-painting scenes from verse, see verse-to-prompt instead.
user-invocable: true
argument-hint: "[tradition name] [concept name and brief description]"
metadata:
  version: "1.0.0"
---

# Blakean Scene — Concept → Embodied Scene

Convert an abstract symbolic concept from any tradition into a **characters** + **action** scene description that slots into the 8-layer prophetic force prompt architecture.

**First:** Read `blakean-reference.md` (in this skill's directory) for the full pattern details, tradition body grammar, palette families, and examples.

## The Core Principle

**The symbol becomes the situation.** Abstract concepts (lotus, sephirah, hexagram, rune) are never depicted as diagrams or geometry. Instead, translate the *feeling* of the concept into a scene with figures under tension — bodies reaching, dissolving, hanging, kneeling, ascending.

**Anti-pattern:** A twelve-petaled lotus with sacred syllables inscribed on each petal. ← This is a diagram, not a scene.

## Selection Decision Tree

Given your concept, ask these questions in order:

1. **Does it involve a figure commanding or revealing?** → Triangle/Apex
2. **Does it involve creating, forming, or bringing into being?** → Arc/Half-Circle
3. **Does it involve dissolution, ecstasy, or being swept up?** → Vortex/Spiral
4. **Does it involve emanation, radiating, or filling space?** → Radial/Expanding
5. **Does it involve confronting the overwhelming or standing guard?** → From Behind/Looming
6. **Does it involve contraction, fall, inward focus, or descent?** → Contracted/Curled
7. **Does it involve duality, opposition, weighing, or two forces?** → Parallel/Mirrored
8. **Does it involve hierarchy, ascent/descent, or axis between realms?** → Vertical Axis

If multiple apply, prefer the one that captures the **emotional core** — the feeling, not the diagram.

## Figure Type Classification

Classify the concept's figure type before writing. This determines anatomy rules — **do not default to human.**

| Type | Anatomy Rules | When to Use |
|------|--------------|-------------|
| **human** | Elongated limbs, tensioned musculature, overdefined deltoids, every tendon visible | Human experience, spiritual struggle, inner states |
| **supernatural** | Blakean anatomy but beyond mortal — wings, flame-bodies, divine radiance, cosmic scale | Divine/demonic beings, cosmic forces, guardian spirits |
| **creature** | Non-human forms with Blakean intensity (taut sinew, visible musculature) as the animal it is | Concept's identity depends on specific non-human forms |
| **hybrid** | Human + non-human elements, each with their own form | Human encounter with the numinous |

**Decision tree:** Non-human identity? → creature. Divine/cosmic beings? → supernatural. Human + non-human interaction? → hybrid. Default → human.

When `figureType` is provided in input, use it directly. When omitted, use this decision tree.

## Output Format

Produce a **complete, ready-to-use image generation prompt** assembled from all 8 layers. **Target length:** 240-280 words total (max 300). Do not describe text, inscriptions, or writing in the scene.

### Input

- **Single concept** (conversational): `[tradition name] [concept name and brief description]`
- **Batch JSON** (pipeline): Array of objects with `id`, `tradition`, `concept`, `description`, optional `pattern` and `figureType`

### The 8 Layers (assemble in this order)

1. **background:** `On a solid black background.` *(fixed — compositing requirement for parchment overlay)*
2. **medium:** `Watercolor and ink over etched line — the quality of a hand-colored copper plate print from the 1790s. Translucent pigment, visible brushwork.` *(fixed)*
3. **composition:** ← From chosen pattern (see reference). 2-3 sentences: angle, framing, spatial structure. Must include framing elements (gorges, gates, arches, columns) and depth layering (foreground, midground, background).
4. **characters:** The figure(s) — follow Figure Type rules and Tradition Body Grammar (see reference).
5. **action:** Key gesture, dramatic moment, body's relationship to space. Must include one discoverable detail.
6. **palette:** Select palette family from reference table, then append: `A single accent of [specific hue] — [what carries it].`
7. **anti:** `No text, no words, no letters, no writing, no borders, no margins, no frames.` *(fixed)*
8. **closer:** `The image emerges from darkness. Fine art quality, highly detailed. Fine art, not photographic.` *(fixed)*

### The 5 Scene Quality Rules (MANDATORY)

1. **Frame the scene** — at least one environmental framing element
2. **Force depth** — name foreground, midground, and background explicitly
3. **Demand contrast** — at least one strong light source against darkness
4. **Include one vivid accent** — one saturated color that pops (not "pale" or "faint")
5. **Pack in discoverable detail** — secondary subject or texture that rewards a second look

### Conversational Output

**Concept:** [tradition] — [concept name]
**Pattern:** [chosen pattern] — [one-line rationale]
**Figure Type:** [human|supernatural|creature|hybrid]
**Body Grammar:** [tradition name] — [posture keywords]
**Palette:** [family name]

**Full prompt:** [All 8 layers concatenated]

**Quality checklist:** Framing ✓ | Depth ✓ | Contrast ✓ | Accent ✓ | Detail ✓

For JSON mode (`--json` or batch), see the schema in the reference file.

## Content Safety Rules

| Blocked concept | Safe alternative |
|----------------|-----------------|
| Blood on surfaces | "dark stains like spilled ink", "vermillion streaks on stone" |
| Wounds / piercing | Aftermath — "a sword embedded in earth", "an arrow lodged in wood" |
| Self-harm | Landscape metaphor — "a candle guttering in a sealed room" |
| Fallen bodies | Emptiness — "abandoned armor on bare ground" |
| Restraint | Environmental — "a narrow gorge with no exit" |

## Anti-Patterns

- **Diagram as scene:** Drawing the symbol literally (Tree of Life diagram, hexagram lines)
- **Static pose:** A figure simply standing or sitting — there must be tension
- **Generic mystical:** Glowing figure in cosmic space — be specific about which body part, which direction
- **Wrong pattern for concept:** Triangle/Apex for dissolution, Contracted/Curled for emanation
- **Nude wrestlers for cosmic opposition:** Supernatural forces need wings, flame, shadow, cosmic scale
- **Forcing human anatomy onto creature concepts:** The creature forms ARE the concept
- **Gorge-as-default framing:** Match framing to tradition (temple columns for Hindu, world-tree for Norse, etc.)
- **Losing the accent:** Must be visible at thumbnail size — "deep violet" not "pale violet"
