---
name: tribos-da-minimal-dark
description: Preset de direction artistique Tribos « Minimalist Premium, Dark Cinematic » — fond presque noir, lumière orange sculpturale, grandes formes géométriques, renard 3D en mouvement, interface minimaliste de marque sport-tech. À lire AVANT de générer un hero ou un visuel dans ce style, de rédiger le prompt correspondant, ou de construire une page sombre et épurée (landing, pages produit) autour de ces visuels.
---

# Tribos — preset « Minimalist Premium, Dark Cinematic »

Une marque premium de sport et de technologie, avec la qualité d'un film
d'animation 3D, sans surcharger l'interface. Noir, lumière orange, formes
géométriques et un renard **en mouvement** — pas de paysage.

**La règle centrale : le premium vient du contrôle, pas de l'accumulation
d'effets.** Une mascotte très bien rendue, une forme orange forte et une
typographie soignée suffisent.

Un des trois presets officiels (voir [`docs/brand/README.md`](../../../docs/brand/README.md)) :

| Preset | Différence |
|---|---|
| **Minimalist Premium Dark** (ce skill) | studio noir, géométrie lumineuse, renard en action, ton sport-tech |
| Cinematic 3D (`tribos-da-3d-cinematique`) | même rendu 3D, mais paysage de montagne au coucher de soleil |
| Illustrated Comic (`tribos-da-bd-cinematique`) | BD peinte, illustrations de fonctionnalités |

Même mascotte, palettes voisines. **Un seul preset par support.**

## Avant toute génération

1. **Joins le renard canonique** : `docs/brand/mascotte/`.
2. Joins la référence de composition : `references/hero/`.
3. Choisis le contexte (landing ou page produit, §4) : il fixe la taille de
   la mascotte, la lumière et la quantité de géométrie.
4. Pars du prompt maître (§2) ou de la variante hero (§3).

## 1. Les trois piliers

| | Règle |
|---|---|
| **01 — Mascotte 3D dynamique** | Le renard est le point focal. Il court, saute ou se prépare à l'effort : pose énergique, silhouette lisible. Fourrure détaillée, vêtements texturés, expression sympathique, rendu de film d'animation haut de gamme. |
| **02 — Noir et lumière orange** | Fond presque noir, ombres profondes, grandes formes géométriques orange lumineuses. La lumière dessine la composition et met le personnage en valeur. Pas de paysage. |
| **03 — Interface minimaliste** | Sans-serif moderne, gros titre blanc, un seul mot ou groupe de mots en orange, navigation discrète, CTA orange. Espacements généreux, peu de bordures, rien de décoratif. |

### Palette

| Rôle | Couleur | Hex |
|---|---|---|
| Fond principal | Noir profond | `#0B0C0E` |
| Surfaces | Anthracite | `#17191D` |
| Accent de marque | Orange Tribos | `#FF721C` |
| Lumière | Ambre | `#FF9A43` |
| Texte | Blanc cassé | `#F7F5F1` |
| Accent mascotte | Pétrole | `#176E6B` |

Le noir pose l'atmosphère, l'orange crée la hiérarchie. Orange **sélectif** :
CTA, mots importants, formes lumineuses, rim light. Pour l'interface de
l'app, `AppTheme.primary` (`#F3730A`) fait foi.

## 2. Prompt maître

```text
# TRIBOS — MINIMALIST PREMIUM DARK ART DIRECTION

## Creative vision
Create a premium dark visual identity for Tribos, a modern social sports and
group-motivation platform.
The art direction combines minimalist luxury branding, contemporary sports
advertising, cinematic 3D animated-film character design and sophisticated
geometric lighting.
The aesthetic is bold, clean, energetic and controlled.
The result should feel like a premium technology and sports brand: visually
striking without unnecessary decoration, playful without being childish, and
cinematic without becoming visually noisy.

## Color system
- Primary background: near-black (#0B0C0E).
- Secondary surfaces: dark charcoal (#17191D).
- Brand accent: vivid warm orange (#FF721C).
- Lighting accent: amber orange (#FF9A43).
- Main text: soft white (#F7F5F1).
- Secondary accent: restrained petrol teal (#176E6B), mainly on the mascot's
  sportswear.
Black establishes the atmosphere. Orange creates hierarchy, energy and brand
recognition.
Use orange selectively for calls to action, important words, luminous
geometric shapes and rim lighting.

## Mascot design
Use the established Tribos orange fox as the canonical character.
Preserve its recognizable face, expressive dark eyes, cream muzzle and cheeks,
large pointed ears, orange fur, fluffy tail and athletic teal clothing.
Use dark sports shorts, a white athletic headband and an optional black sports
backpack when appropriate.
Render the character as a premium stylized 3D animated-film character:
- Carefully groomed fur with fine strand detail.
- Soft but defined facial features.
- Expressive eyes and a confident smile.
- Natural fabric folds and realistic material response.
- Strong silhouette and polished anatomy.
- Warm orange highlights against cooler shadows.
The character should remain friendly, athletic, confident and approachable.
Never redesign the canonical mascot or change its defining colors and
proportions.

## Pose and movement
Prefer dynamic, athletic poses:
- Running forward.
- Accelerating into a sprint.
- Jumping over an obstacle.
- Landing after a jump.
- Preparing for a challenge.
- Moving confidently toward the viewer.
The pose should convey momentum, determination and optimism.
Keep the movement readable and anatomically coherent. Avoid exaggerated
superhero anatomy, aggressive expressions and excessive motion effects.

## Background and geometry
Use a near-black studio-like environment with a limited number of large
geometric light forms.
Preferred visual elements:
- Diagonal orange light beams.
- Broad translucent orange ribbons.
- Angular luminous planes.
- Subtle gradients between black, burnt orange and amber.
- Controlled atmospheric haze around the light source.
Geometric elements should frame the mascot and reinforce movement.
Use two or three strong shapes at most. Avoid complicated environments, random
floating particles, excessive grids, decorative circles and busy textures.
The background should remain predominantly dark.

## Cinematic lighting
Use a strong orange key light or backlight to separate the mascot from the
background.
- Warm rim lighting around the ears, tail, shoulders and limbs.
- Soft neutral illumination on the face.
- Deep charcoal shadows.
- Restrained amber reflections on fur and clothing.
- Physically coherent contact shadows.
- Controlled highlights with no excessive bloom.
The orange light should feel intentional and sculptural, not like a neon
gaming setup.

## Composition
Design for a wide desktop website hero, ideally 16:9 or wider.
- Left 38–43%: dark negative space for the headline, supporting copy and CTA.
- Center or center-right: large dynamic mascot, overlapping the geometric
  light shapes.
- Far right: optional short supporting message or subtle feature labels.
- Top: minimal navigation with compact logo and one clear CTA.
Keep the main headline readable against an almost-black background.
Use asymmetry, scale and negative space instead of decorative UI cards.
The mascot should occupy approximately one-third of the hero composition while
remaining the dominant visual element.
Keep sufficient space around the face and limbs. Avoid cropping essential
parts of the character accidentally.

## Typography and interface
Use a contemporary sans-serif typeface with a clean geometric structure.
- Large white headline with tight but readable line spacing.
- One important phrase highlighted in vivid orange.
- Small uppercase eyebrow text with restrained letter spacing.
- Short supporting paragraph in soft white or light grey.
- Orange primary CTA with dark text or high-contrast white text.
- Minimal secondary action, optionally with a simple play icon.
- Compact navigation with generous horizontal spacing.
Prefer a flat, clean interface over excessive glassmorphism, borders, shadows
or nested cards.
All interface elements must be implemented separately from the generated
artwork.

## Brand personality
The design should communicate:
- Collective ambition.
- Confidence.
- Energy and forward movement.
- Friendship and mutual motivation.
- Progress without toxic competition.
- Premium simplicity.
The result should feel like a distinctive sports-tech brand, not an esports
team, gaming interface or generic fitness template.

## Quality requirements
High-end stylized 3D rendering, premium animated-film character quality,
sophisticated materials, consistent mascot design, controlled cinematic color
grading, strong visual hierarchy, clean negative space and excellent
silhouette readability.

## Avoid
Photorealistic wildlife, childish cartoon styling, flat vector art, excessive
neon, cyberpunk aesthetics, RGB gaming lights, complex landscapes, excessive
lens flare, strong bloom, too many geometric shapes, floating UI panels,
unnecessary glassmorphism, random decorative elements, inconsistent mascot
anatomy, generated typography, inaccurate logos and overcrowded compositions.
```

## 3. Variante : le hero de référence

Pour retrouver le hero de référence (`references/hero/`).

```text
Create a premium minimalist dark website hero visual for Tribos, a social
sports and group-motivation brand.

FORMAT:
Wide 16:9 desktop hero composition.

BACKGROUND:
Near-black charcoal studio environment, almost entirely dark. A bold, angular
orange light beam cuts diagonally across the center-right, creating a sense of
speed and forward movement. Subtle burnt-orange gradients and controlled
atmospheric haze. No natural landscape.

CHARACTER:
The canonical Tribos orange fox mascot is sprinting energetically toward the
viewer, positioned in the center-right of the composition. Preserve the
established design: orange fur, cream muzzle and cheeks, large expressive dark
eyes, pointed ears, fluffy tail, white athletic headband, teal sleeveless
sports top, dark navy shorts and black running shoes. Optional black sports
backpack.
The fox has a confident, friendly expression. Its arms and legs form a clear,
believable running pose. Fur reacts naturally to movement. Clothing has
detailed but restrained material definition.

RENDERING:
Premium stylized 3D animated-feature-film quality, Pixar-inspired character
appeal, detailed groomed fur, sophisticated material shading, cinematic global
illumination, warm orange rim lighting, deep shadows and carefully controlled
highlights.

COMPOSITION:
Reserve the left 40% as clean near-black negative space for a large white
headline, orange highlighted words, a short paragraph and an orange CTA
button. Place the fox prominently in the center-right, partially overlapping
the luminous diagonal geometric shape. Preserve sufficient dark space on the
far right for a small secondary message.

DESIGN LANGUAGE:
Minimalist luxury sports branding, premium technology aesthetics, sculptural
orange light, bold contrast, clean geometry, generous negative space and
intentional asymmetry.

COLOR PALETTE:
Near-black, charcoal, vivid Tribos orange, amber, warm white and restrained
petrol teal.

MOOD:
Fast, confident, ambitious, modern, approachable and energetic.

STRICT CONSTRAINTS:
No landscape, no complex scenery, no unnecessary decorative objects, no
excessive neon, no cyberpunk aesthetic, no gaming HUD, no random particles, no
excessive bloom, no text, no typography, no logo, no buttons, no watermark.

Generate only the background and character. The website interface will be
implemented separately.
```

## 4. Tenir la DA sur tout le site

Le preset reste fixe ; seuls ces paramètres varient selon la page.

| Élément | Landing page | Pages produit |
|---|---|---|
| Fond | Noir profond, géométrie orange | Noir ou anthracite uni |
| Mascotte | Grande, en mouvement | Petite, ponctuelle |
| Lumière | Cinématique, contrastée | Douce et discrète |
| Orange | CTA, lumière et mots clés | Actions, progression, états actifs |
| Décoration | **Une** grande forme géométrique | Presque aucune |
| Interface | Éditoriale, très aérée | Fonctionnelle, dense juste ce qu'il faut |

## 5. Intégration

- **Deux ou trois formes lumineuses maximum** par visuel ; une seule sur la
  landing.
- Texte, navigation, boutons et labels en HTML/CSS (site) ou en widgets (app),
  jamais dans l'image.
- Titre blanc sur zone quasi noire : vérifier le contraste (AA minimum), y
  compris sur le recadrage mobile.
- Recadrage mobile dédié : le renard en entier (visage et membres non
  coupés), la forme orange conservée, le texte au-dessus ou en dessous.
- Pas de glassmorphism, de cartes imbriquées ni de particules pour
  « enrichir » : si la page paraît vide, on agrandit la mascotte ou la
  typographie, on n'ajoute pas d'effets.
- Exports WebP/AVIF en plusieurs largeurs ; un fond presque noir se compresse
  bien, ne pas l'alourdir.
