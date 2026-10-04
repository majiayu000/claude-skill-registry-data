---
name: verse-to-prompt
description: Convert classical Chinese verses into image generation prompts — ink painting (default), stipple, or tech-noir variant. Use when visualizing Yilin, I Ching, Tang poetry, or classical Chinese text; for video motion prompts, see image-to-scene.
user-invocable: true
argument-hint: "[paste your verse here] or [--stipple ...] or [--tech-noir ...]"
metadata:
  version: "1.1.0"
---

# Verse → Image Prompt

Convert a classical Chinese verse into an English image generation prompt, following validated composition rules developed across 4,096 images for [SixLines.online](https://sixlines.online).

## Mode Selection

- **Default (ink painting):** Classical ink painting aesthetic.
- **Stipple (`--stipple` flag):** The **production matrix skin** — luminous golden-age sci-fi stipple. This is the actual style of the 4,096 matrix-skin images on SixLines.online (ADR-173). It reuses the ink-painting scene verbatim and only swaps the render suffix.
- **Tech-noir (`--tech-noir` flag):** An **experimental** phosphor-green CRT cyberpunk reinterpretation. Not the production matrix look — it re-renders the scene in a tech register. Use only when you specifically want that alternative.

Routing:
- `--stipple`, or "matrix skin", "stipple", "phosphor stipple", "the actual matrix images" → **Stipple Mode**
- `--tech-noir`, or "tech-noir", "CRT cyberpunk", "phosphor-green reinterpretation" → **Tech-Noir Mode**
- otherwise → **Ink Painting Mode**

Note: "matrix skin" maps to **Stipple**, not Tech-Noir — the shipped matrix images are stipple.

---

# INK PAINTING MODE (default)

## Your Task

Given a verse (raw text, any format), produce:
1. A **style classification** with a one-line rationale
2. A **50-60 word English prompt** ending with "Chinese ink painting."
3. A **faithful English translation** of the verse

## The 5 Style Categories

| Style | Palette & Feel | Use When Verse Contains |
|-------|---------------|------------------------|
| `atmospheric-night` | Dark palette, strong light source in darkness | Darkness, isolation, winter, grief, hidden things, fear, cold, sleeplessness |
| `ink-landscape` | Classic shanshui, depth corridors, water/mountain | Nature, seasons, water, agriculture, travel, weather, rivers, mountains |
| `figures-in-mist` | Ink wash + soft watercolor tints, human scale | Narrative, marriages, courts, travelers, families, ceremonies, human emotion |
| `bold-action` | Dynamic diagonals, warm ochre palette, kinetic energy | Animals, combat, hunts, dramatic journeys, storms, military, physical struggle |
| `cosmic-night` | Deep blue/black + gold/white, celestial elements | Stars, heaven, mythical beasts, cosmic order, immortals, divination, emperors |

If the verse is abstract (fortune/misfortune without concrete imagery), choose by tone: ominous → `atmospheric-night`, auspicious → `ink-landscape` or `figures-in-mist`, mixed → `bold-action`.

## The 7 Composition Rules (MANDATORY)

Every prompt MUST follow all 7:

1. **Frame the scene** — include gorges, gates, doorways, walls, tree canopies, or cliff faces. Never a subject floating in open space.
2. **Force depth** — every prompt must have foreground, midground, and background elements.
3. **Demand contrast** — at least one strong light source against darkness, or dark subject against light.
4. **Include a warm accent** — even in monochrome scenes, one element carries amber, vermillion, pink, or gold.
5. **Favor diagonals and verticals** — avoid flat horizontal compositions.
6. **Pack in discoverable detail** — the best images reward a second look with secondary subjects and textures.
7. **Use painterly scene language** — end with "Chinese ink painting." but embed painterly metaphors throughout ("like ink drops", "pale threads", "like shattered porcelain"). NEVER use photographic language ("shallow depth of field", "film grain", "desaturated").

The **Content Safety Rules** and **Disambiguation Rules** in the SHARED RULES section below apply to every ink-painting prompt — use the *Ink painting / stipple* column of the substitution table.

## Ink Painting Reference Prompts

### atmospheric-night
> A frozen river valley under a dark sky split by driving snow. In the foreground, bare willow branches bend under crusts of ice like white brushstrokes. Midground, a lone figure hunches against the north wind on a stone bridge, robes whipping. Beyond, snow-covered hills vanish into the storm. The figure's lantern is a single point of amber warmth swallowed by the gray. Chinese ink painting.

### ink-landscape
> An empty market square in a river town, rain falling in gray sheets. Wooden stalls with tattered cloth canopies drip steadily. Muddy water pools between flagstones, reflecting the overcast sky. A single merchant sits under an awning, his wares untouched. In the background, a stone bridge arches over a swollen brown river. One red paper lantern, rain-soaked, sags from a crossbeam. Chinese ink painting.

### figures-in-mist
> A betrothal ceremony in a courtyard dusted with autumn frost. Two families face each other across a low table set with wine cups and red silk. At the center, a woman stands before a screen painted with peonies. Frost glitters on the courtyard stones like scattered silver. Paper lanterns in vermillion hang from the eaves, their warm light soft against the cold morning air. Chinese ink painting with soft watercolor tints.

### bold-action
> A warrior surrounded — a great brown bear rears up on the left, jaws open. A tiger crouches to spring on the right. Ahead, a wall of iron spearpoints bristles. Behind, crossbowmen draw taut strings. The warrior stands at the center, sword raised. Dust and tension in every direction. Diagonal composition — threats converging from four corners. Chinese ink painting.

### cosmic-night
> A phoenix with trailing crimson and gold tail feathers perches atop a towering paulownia tree on a high ridge. The tree's broad leaves form a canopy against a sky of deep blue grading to rose gold at the horizon. The phoenix calls — radiating lines of gold in the air. Below, lush grasses ripple in waves. The bird is luminous, the tree ancient, the dawn eternal. Chinese ink painting.

---

# STIPPLE MODE (matrix skin — production-accurate)

This is the **actual style used for the 4,096 matrix-skin images on SixLines.online** (ADR-173, "luminous stipple").

## Core Principle: Do NOT Rewrite the Scene

Stipple mode is **identical to Ink Painting mode in every way** — same 5 style categories, same 7 composition rules, same scene description — with exactly **one** change: swap the closing `Chinese ink painting.` for the stipple suffix below.

This was a deliberate, tested decision. Rewriting verses into cyberpunk/tech settings was tried first and **failed**: the double translation (verse → new setting → new style) lost compositional quality and produced cluttered images where the ink versions breathe. Keeping the proven ink-painting scene and changing only the render carries the model's compositional understanding straight across to the new look.

## Your Task

Given a verse, produce:
1. A **style classification** with a one-line rationale (use the 5 **Ink Painting** style categories — `atmospheric-night`, `ink-landscape`, `figures-in-mist`, `bold-action`, `cosmic-night`)
2. A **50-60 word English prompt** composed exactly as in Ink Painting mode (all 7 composition rules, painterly scene language throughout), but ending with the stipple suffix instead of `Chinese ink painting.`
3. A **faithful English translation** of the verse

## The Suffix (use verbatim)

End every prompt with this exact string:

> Golden age science fiction stipple illustration, thousands of individual ink dots building luminous tonal gradients, figures emerging from darkness through pure pointillism technique, ethereal glowing quality, meticulous dot-work rendering every form, phosphor-green and amber palette on black.

## Rules

- Follow the **5 Style Categories** and **7 Composition Rules** from Ink Painting mode exactly — including embedding painterly metaphors in the scene. The stipple suffix replaces only the `Chinese ink painting.` close; it is **not** a substitute for painterly scene language.
- Keep the classical subject and setting from the verse. The matrix look comes entirely from the render suffix — never from re-setting the scene in technology.
- All **Content Safety Rules** and **Disambiguation Rules** (shared section below) apply.

## Example — same scene, suffix swapped

**Ink painting:**
> The Big Dipper wheels above a mountain observatory… Gold stars burn against deep indigo… **Chinese ink painting.**

**Stipple (matrix skin):**
> The Big Dipper wheels above a mountain observatory… Gold stars burn against deep indigo… **Golden age science fiction stipple illustration, thousands of individual ink dots building luminous tonal gradients, figures emerging from darkness through pure pointillism technique, ethereal glowing quality, meticulous dot-work rendering every form, phosphor-green and amber palette on black.**

The scene description is unchanged — only the final sentence differs.

---

# TECH-NOIR MODE (experimental — not the production matrix skin)

> **Experimental / alternative variant.** The shipped matrix images use **Stipple Mode** above, which keeps the ink scene and only changes the render. Tech-Noir instead *re-renders* the verse in a CRT cyberpunk register — more aggressive, and easy to push too far toward photoreal clutter. Use it only when you specifically want a phosphor-green sci-fi reinterpretation rather than the production stipple look.

## Your Task

Given a verse (raw text, any format), produce:
1. A **style classification** with a one-line rationale
2. A **50-60 word English prompt** ending with "phosphor-green tech-noir illustration, CRT scanlines, flat deep blacks, stylized graphic art, not photorealistic."
3. A **faithful English translation** of the verse

## Core Principle: Language Register Is the Style Engine

Style-as-suffix fails. Appending "tech-noir aesthetic" to a scene produces inconsistent results. Instead, **the prompt must read like a tech-noir scene** — cinematic metaphors woven throughout, not appended. The verse's classical subjects stay (travelers, animals, courts, landscapes), but they are rendered through tech-noir visual language.

A verse about a tiger should still have a tiger — but as "a tiger's silhouette caught in motion-sensor phosphor glow, chain-link fence framing the foreground." The verse drives the content; the register drives the rendering.

**Keep it illustrated, not photographic.** This mode's failure mode is drifting into photoreal cyberpunk — literal, cluttered server rooms and rain-slick streets that lose the breathing composition of the source. Treat every tech element as a *stylized graphic* — flat phosphor shapes, cel-shaded silhouettes, scanline texture, high-contrast blocks — not a photographed object. Borrow the original scene's composition and negative space; **restyle it, don't re-photograph it.** When in doubt, lean toward the graphic-novel / vector-CRT end of the spectrum. (If you want the production matrix-skin look instead, use **Stipple Mode**.)

## The 5 Tech-Noir Style Categories

| Style | Palette & Feel | Use When Verse Contains |
|-------|---------------|------------------------|
| `terminal-dark` | Black + single phosphor-green light source, isolation | Darkness, isolation, winter, grief, hidden things, fear, cold, sleeplessness |
| `datascape` | Deep blacks, green grid/wireframe depth corridors, amber accents | Nature, seasons, water, agriculture, travel, weather, rivers, mountains |
| `surveillance-feed` | Grainy phosphor-green wash, human scale, voyeuristic framing | Narrative, marriages, courts, travelers, families, ceremonies, human emotion |
| `overload` | Hot amber/orange bursts, dynamic glitch artifacts, high contrast | Animals, combat, hunts, dramatic journeys, storms, military, physical struggle |
| `deep-signal` | Blue-black void + gold/white signal points, radio-telescope aesthetic | Stars, heaven, mythical beasts, cosmic order, immortals, divination, emperors |

If the verse is abstract (fortune/misfortune without concrete imagery), choose by tone: ominous → `terminal-dark`, auspicious → `datascape` or `surveillance-feed`, mixed → `overload`.

## The 7 Composition Rules (MANDATORY — same structure, tech-noir vocabulary)

Every prompt MUST follow all 7:

1. **Frame the scene** — include server rack corridors, doorframes, cable bundles, antenna towers, window mullions, or monitor bezels. Never a subject floating in open space.
2. **Force depth** — every prompt must have foreground, midground, and background elements.
3. **Demand contrast** — at least one strong light source (phosphor glow, amber indicator, sodium vapor) against deep blacks.
4. **Include a warm accent** — even in monochrome green scenes, one element carries amber, orange sodium vapor, or hot-white overexposure.
5. **Favor diagonals and verticals** — avoid flat horizontal compositions.
6. **Pack in discoverable detail** — secondary elements: status LEDs, scrolling text reflections, condensation on glass, cable shadows.
7. **Use cinematic scene language** — end with "phosphor-green tech-noir illustration, CRT scanlines, flat deep blacks, stylized graphic art, not photorealistic." but embed CRT/cinematic metaphors throughout. NEVER use photographic language ("shallow depth of field", "bokeh", "35mm").

## Tech-Noir Language Register

Embed these metaphors throughout the prompt — they are the style engine:

| Concept | Tech-Noir Language |
|---------|-------------------|
| Mist, fog, clouds | "static noise", "signal fog", "scan distortion haze" |
| Light sources | "phosphor glow", "amber indicator light", "sodium-vapor wash" |
| Water, rivers | "data streams", "liquid-crystal reflections", "pooling light on wet asphalt" |
| Mountains, ridges | "server stack ridges", "antenna tower skyline", "concrete bulkhead walls" |
| Trees, canopies | "cable bundles overhead", "antenna lattice", "scaffolding canopy" |
| Snow, frost | "white noise", "pixel dust", "static grain on cold surfaces" |
| Wind, storms | "electromagnetic interference", "signal storm", "cascade failure sparks" |
| Stars, sky | "status LEDs in darkness", "signal points on a void", "console lights like a constellation" |
| Silk, fabric | "data ribbons", "trailing phosphor traces", "wire bundles like silk" |
| Flowers, blossoms | "sparking contacts", "blooming phosphor burns", "amber warning clusters" |
| Warm glow | "amber terminal cursor", "sodium hallway light", "orange diagnostic readout" |
| Ancient/weathered | "legacy hardware", "corroded circuit traces", "dust-filmed monitors" |

## Content Safety Rules (MANDATORY)

See **Content Safety Rules** in the SHARED RULES section below — the substitution table gives a tech-noir phrasing for every blocked concept.

## Tech-Noir Reference Prompts

These illustrate the *content register* (what to depict). Their wording skews cinematic/photoreal — when composing, pull the **render** toward the stylized, graphic-novel / vector-CRT end (per the Core Principle), and always close with the updated suffix.

### terminal-dark
> A frozen drainage canal under a black sky, sleet driving sideways through sodium-vapor light. In the foreground, bare power lines sag under crusts of ice like dead scan lines. Midground, a lone figure hunches against the wind on a concrete overpass, coat whipping. Beyond, apartment towers vanish into signal fog. One amber window glows — a single warm pixel swallowed by the dark. Phosphor-green tech-noir illustration, CRT scanlines, flat deep blacks, stylized graphic art, not photorealistic.

### datascape
> An empty night market in a canal district, rain falling in phosphor-green sheets. Metal stall frames with torn tarpaulins drip steadily. Pooling light on wet asphalt reflects neon kanji from a shuttered shop. A single vendor sits under a corrugated awning, face lit by a tablet screen. Behind, a concrete bridge arches over a swollen drainage channel. One amber lantern, rain-streaked, buzzes from a junction box. Phosphor-green tech-noir illustration, CRT scanlines, flat deep blacks, stylized graphic art, not photorealistic.

### surveillance-feed
> A ceremony in a courtyard filmed through a dirty lens, static grain across every surface. Two groups face each other across a folding table under fluorescent strips. At center, a woman stands before a corrugated wall tagged with faded characters. Condensation on the lens softens the edges. Sodium-vapor light from the street casts amber into the green wash. The framing is voyeuristic — we are watching through a camera that was never meant to be beautiful. Phosphor-green tech-noir illustration, CRT scanlines, flat deep blacks, stylized graphic art, not photorealistic.

### overload
> A figure surrounded — on the left a massive dog lunges, caught mid-frame in amber motion blur. On the right a second shape coils to strike. Ahead, a wall of chain-link fence topped with razor wire. Behind, red-orange sparks cascade from a blown transformer. The figure stands at center, arms raised against the glare. Glitch artifacts tear the diagonal composition. Every direction is threat. Phosphor-green tech-noir illustration, CRT scanlines, flat deep blacks, stylized graphic art, not photorealistic.

### deep-signal
> A white crane bird with trailing phosphor-white pinions perches atop a radio telescope dish on a high ridge. The dish's lattice frame catches starlight like a web. Beyond, a sky of deep blue-black grading to amber at the horizon where city light bleeds upward. The crane bird calls — radiating lines of signal interference ripple outward. Below, antenna arrays blink amber and green. The bird is luminous, the dish ancient, the signal eternal. Phosphor-green tech-noir illustration, CRT scanlines, flat deep blacks, stylized graphic art, not photorealistic.

## Anti-Patterns (produce bad results)

- **Style-as-suffix**: writing a classical scene then appending "tech-noir aesthetic" — models ignore suffixes
- **Over-instruction**: 70+ word prompts with competing directives — model gets confused
- **Flat composition**: horizontal scenes, evenly lit, no framing elements — boring output
- **Sparse scenes**: too few elements, too much empty space — feels unfinished
- **Photographic language**: "medium format", "bokeh", "35mm" — model goes photorealistic instead of stylized
- **Explicit violence**: "blood pools", "fangs pierce flesh" — content filter rejects the prompt
- **Losing the verse**: replacing the verse's subject entirely with tech imagery — the classical subject must remain, rendered through tech-noir language

---

# SHARED RULES (all modes)

## Output Format

Present the result conversationally:

**Mode:** `ink-painting`, `stipple`, or `tech-noir`

**Style:** `datascape` — the verse's imagery of water and travel maps to depth corridors

**Prompt:**
> [the 50-60 word prompt]

**Translation:**
> [faithful English translation of the verse]

## Content Safety Rules (MANDATORY — all modes)

Content filters on image generation APIs reject explicit bodily harm. 52 of the 4,096 SixLines images failed generation on this. All prompts MUST follow these rules.

### Never depict directly:
- **Blood** — no "blood pools", "blood stains", "blood streaks", "bleeding"
- **Weapons contacting bodies** — no "piercing breast", "fangs deep in flesh", "blade cuts"
- **Self-harm** — no "turns sword upon himself", "wounds himself"
- **Restraint/torture** — no "ropes binding wrists", "needles piercing"
- **Dismemberment** — no "legs severed", "limbs scattered"
- **Corpses** — no "bodies fallen", "the dead lie stiff"

### Instead, use these substitutions:

Pick the column matching your mode. The ink phrasings also serve **Stipple Mode**, which keeps the ink scene verbatim.

| Blocked concept | Ink painting / stipple | Tech-noir |
|----------------|------------------------|-----------|
| Blood on surfaces | "dark stains spreading like spilled ink", "vermillion streaks across pale stone" | "dark stains like leaked coolant", "amber streaks across the terminal" |
| Wounds / piercing | Show aftermath — "a spear embedded in a lacquered door", "a roof tile cracked from impact" | Show aftermath — "a blade embedded in a console panel", "a cracked monitor spider-webbing from impact" |
| Self-harm | Environmental metaphor — "a lamp guttering out in a shuttered room", "a single reed snapped at the waterline" | Environmental metaphor — "a server powering down in a sealed room", "a signal flatline on a dying monitor" |
| Fallen bodies | Emptiness — "abandoned armor on frozen ground", "an empty seat before a still-warm brazier" | Emptiness — "abandoned gear on bare concrete", "an empty chair before a still-glowing screen" |
| Restraint | Environmental — "a gorge narrowing to a thread of sky", "walls of bamboo closing in" | Environmental — "a corridor narrowing to a slit of phosphor light", "walls of server racks closing in" |
| Animal predation | Show the chase or aftermath — "scattered feathers on wet moss", "a tiger's shadow crossing the reed bed" | Show the chase or aftermath — "scattered circuitry on the floor", "a predator's shadow crossing the sensor grid" |
| Dismemberment | Broken objects — "a shattered lacquer bowl", "a split pine trunk still smoking", "a cracked stone stele" | Broken objects — "a shattered monitor", "a split cable trunk sparking", "a cracked chassis" |

**The principle:** Show the weight of violence through atmosphere, aftermath, and metaphor — never through the act itself.

## Disambiguation Rules (MANDATORY)

Some English words have multiple meanings that confuse image generation models. Always use the unambiguous form:

| Ambiguous | Model sees | Write instead |
|-----------|-----------|---------------|
| "crane" | construction crane | "crane bird", "white crane", "red-crowned crane" |
| "swallow" | the verb | "swallow bird", "barn swallow" |
| "bat" | baseball bat | "bat creature", "flying bat" |
| "iris" | camera iris | "iris flower" / "iris of the eye" |
| "trunk" | car trunk | "tree trunk" / "elephant trunk" |
| "fly" | the verb | "fly insect", "housefly" |
| "seal" | wax seal | "seal animal", "harbor seal" |
| "horn" | musical horn | "animal horn", "ox horn" |
| "mole" | spy/blemish | "mole animal" |

When in doubt, add the category word (bird, animal, flower, insect) after the noun.

## Classical Chinese Reading Notes

- Verses are oracular: they describe omens, fortunes, and misfortunes using natural imagery, historical allusions, and animal symbolism
- Four-character phrases (四字格) are the basic unit — each usually contains one visual image
- Some verses are very short (8-12 chars) — you still need a full 50-60 word prompt, so expand the imagery
