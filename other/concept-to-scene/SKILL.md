---
name: concept-to-scene
description: Use when an abstract symbol such as a chakra, sephirah, alchemical stage, rune, or hexagram needs reusable character and action blocks for image generation with a separately chosen visual style. For a complete Blakean image prompt, see blakean-scene.
user-invocable: true
argument-hint: "[tradition name] [concept name and optional brief description]"
metadata:
  version: "1.0.0"
---

# Concept → Embodied Scene

Turn an abstract symbol into a scene with **characters** and **action**. Each block can be used with a separately chosen visual style.

## The Problem This Solves

Describing a lotus diagram, yantra, or hexagram literally tells an image model to draw the symbol. Find a physical action that expresses the supplied reading. A figure can reach, dissolve, hang, kneel, or transform. Choose what the body does based on the meaning the scene needs to convey.

## Your Task

Given a concept, its tradition, and an optional brief description, produce:

1. A **scene interpretation** — one sentence stating the experience or relationship the scene will embody
2. A **characters block** (40-60 words) — who/what is in the scene, described physically
3. An **action block** (40-60 words) — what is happening in the scene, the moment of tension

## The Method: Symbol → Experience → Figure

Start with the user's description, including any source or school they specify. Use it to pick the experience or relationship to embody. If you supply a reading or make an interpretive assumption beyond the description, label the scene interpretation as a **creative reading**. If fidelity to a specific source or school is required and the input leaves the reading unclear, ask for the relevant passage or interpretation.

The symbol type can suggest a physical question:

| Symbol Type | Ask | Example |
|------------|-----|---------|
| Geometric (yantra, mandala, sigil) | What does it feel like to BE inside this geometry? | Anahata yantra → a figure whose chest is open, light pouring from the heart, caught between ascending and descending forces |
| Positional (sephirah on tree, chakra on spine) | What is the body doing at this threshold? | Da'at (the abyss) → a figure at the edge of a void, robes fraying into light above and nothing below |
| Process (alchemical stage, bardo state) | What is the figure becoming? Show the transformation mid-act. | Rubedo → two figures fusing into one form inside a vessel flooding with red fire |
| Elemental (Wu Xing phase, Greek element) | What is the element doing to/through a figure? | Water phase → a figure descending into dark water, the surface closing overhead |
| Relational (yin-yang, conjunction) | Show two figures or forces in the moment of meeting. | Coniunctio → a king and queen reaching toward each other, their outstretched hands beginning to merge |
| Cosmic (hexagram, odù) | What physical change would express this reading? | Gé (Revolution) → a figure mid-molt, old skin splitting away, new form emerging raw |

## The 4 Constraints (MANDATORY)

Every scene MUST satisfy:

1. **At least one figure under tension** — a body reaching, dissolving, kneeling, hanging, transforming, resisting, yielding. Tension is non-negotiable. Static figures standing at rest are forbidden.
2. **Imply the symbol through action.** Use the gesture or physical relationship to evoke the reading. Omit literal diagrams, such as a six-pointed star or hexagram lines. A count taken from the symbol's structure, such as six cloud layers for six hexagram lines, can shape the setting. It must not read as the diagram itself: no stacked bars, labelled petals, or inscribed syllables.
3. **Describe the body specifically.** Give the figure a posture and gesture. Use clothing and the position of the head, hands, and shoulders to reinforce the physical action. A kneeling figure can bow its head, clasp its hands, and tense its shoulders.
4. **Freeze a single moment.** Show the action at the point of maximum tension.

Choose the figures' spatial relationship to fit the reading. Use height when ascent, descent, or hierarchy carries meaning. Two forces that meet as equals can face each other at eye level.

Before writing the final blocks, check whether the same pose and action could illustrate a different concept after swapping the title. If so, make the gesture or relationship more specific to this reading.

## Content Safety (MANDATORY)

Show violence and harm through atmosphere, aftermath, and metaphor, never through the act itself. Keep substitutions free of any one visual style, since the style is chosen separately.

| Blocked concept | Safe alternative |
|----------------|-----------------|
| Blood / wounds | "dark stains spreading across stone", "red streaks on a wall" |
| Weapons contacting bodies | Aftermath — "sword embedded in earth", "arrow lodged in a post" |
| Self-harm / self-sacrifice | Ordeal — "weathered by nine days of wind", "body rigid with strain" |
| Fallen bodies | Emptiness — "abandoned armour on bare ground" |
| Restraint | Environment — "a narrow gorge with no exit" |
| Dismemberment | Broken objects — "shattered vessel", "split tree trunk" |
| Graphic nudity | Cosmic forms — "luminous outline", "translucent figure" |

## Anti-Patterns

- **Describing the symbol literally** — "a twelve-petaled lotus with Sanskrit syllables" → flat diagram, not a scene
- **No figure** — pure landscape or geometry leaves the action without a body
- **Multiple sequential moments** — "first he rises, then he falls, then he is reborn" → pick ONE moment
- **Tradition-as-costume** — don't just dress a generic figure in tradition-specific clothing. The scene itself must arise from the concept's meaning.
- **Over-specifying faces** — diffusion models struggle with specific facial expressions. Use body posture and gesture instead.

## Output Format

Present conversationally:

**Concept:** [tradition] — [concept name]

**Scene interpretation:** [One sentence stating the experience or relationship the scene will embody]

Use **Scene interpretation (creative reading):** when you supply an interpretation beyond the input.

**Characters:**
> [40-60 words describing who/what is physically present]

**Action:**
> [40-60 words describing the moment of tension]

These blocks can also fill two layers in the eight-layer Blakean prompt structure:
```
background → medium → composition → [characters] → [action] → palette → anti → closer
```

## Examples

### Input: Hinduism — Muladhara (Root Chakra)

**Supplied reading:** Grounding gives the rest of the body a stable base.

**Scene interpretation:** A grounded body can bear the weight of everything above it.

**Characters:**
> A heavy, broad figure crouches at the base of a stone column that rises into darkness. Its legs are braced wide and both palms press flat against the floor. Its skin has the grain and colour of the stone beneath it. A single serpent lies coiled three and a half times around the column's base.

**Action:**
> The figure pushes down through its palms and heels, and cracks spread outward through the floor around it. The column above shakes as the force travels up through the stone. The serpent's head lifts slightly, its eyes newly open. The figure's shoulders and thighs stay locked to hold the weight.

### Input: I-Ching — Hexagram 1, Qián (The Creative)

**Scene interpretation (creative reading):** Creative force is a dragon straining upward at the threshold of taking form.

**Characters:**
> A long figure climbs through layered clouds with both arms raised above its head. Its body twists in a spiral from hips to shoulders, and its robes hang down into the clouds below. Scales cover its forearms and run along its spine. Its hands and bare feet end in short curved claws like a dragon's.

**Action:**
> The figure strains into the highest of six cloud layers. Its fingertips just touch the bright edge of the cloud while its trailing robes hang through the darker layers below. The back arches and the ribs flare with the effort of holding the reach. Far beneath, the ground is barely visible.

### Input: Alchemy — Coniunctio

**Supplied reading:** Two distinct elements form a union through mutual effort.

**Scene interpretation:** Two equal forces each yield at the point where they join.

**Characters:**
> Two glassworkers stand face to face at eye level, their feet braced wide on the same stone floor. One rod carries a gather of amber glass and the other a gather of blue. Their leather sleeves crease at the elbows as they hold the glowing tips halfway between them.

**Action:**
> Each worker turns their rod a fraction of a turn as the softened glass meets. Both lean into the seam with elbows held close. The two gathers flatten by the same amount at the point of contact, and a thread of each colour curls into the other at the join.
