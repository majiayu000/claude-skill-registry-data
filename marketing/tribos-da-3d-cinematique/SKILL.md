---
name: tribos-da-3d-cinematique
description: Preset de direction artistique Tribos « Cinematic 3D » — landing page cinématographique inspirée des films d'animation (Pixar), mascotte renard 3D expressive, paysage de montagne au coucher de soleil, interface sombre sur paysage orange. À lire AVANT de générer un hero de site, un visuel de campagne ou de fiche store dans ce style, de rédiger le prompt correspondant, ou d'intégrer un tel visuel dans une page (composition, texte, CTA).
---

# Tribos — preset « Cinematic 3D »

Landing page cinématographique inspirée des films d'animation 3D : mascotte
expressive, nature spectaculaire, lumière de coucher de soleil. On reproduit
**le personnage, mais aussi la composition, l'éclairage, la profondeur** et
le contraste entre l'interface sombre et le paysage orange.

C'est un des trois presets officiels (voir [`docs/brand/README.md`](../../../docs/brand/README.md)) :
- **Cinematic 3D** (ce skill) : grands visuels marketing ;
- **Illustrated Comic** (`tribos-da-bd-cinematique`) : illustrations BD.

- **Minimalist Premium Dark** (`tribos-da-minimal-dark`) : studio noir,
  lumière orange géométrique, renard en mouvement.

Même mascotte, palettes voisines, rendus différents. **Un seul preset par support.**

## Avant toute génération

1. **Joins le renard canonique** : `docs/brand/mascotte/`. Sans image de
   référence, le visage, les proportions et la tenue dérivent.
2. Joins la référence de composition si elle existe : `references/hero/`.
3. Décide du cadrage (desktop 16:9 ou plus large, recadrage mobile) et de
   l'emplacement du texte **avant** d'écrire le prompt.
4. Pars du prompt maître (§2), ou de la variante hero (§3).

## 1. Identité

| Pilier | Règle |
|---|---|
| **Orange signature** | Orange vif, ambre, cuivre, reflets dorés. La lumière du décor renforce naturellement la couleur de Tribos. |
| **Contraste cinématographique** | Ombres bleu nuit, premier plan sombre, arrière-plan lumineux. Le texte reste blanc et lisible même sur une image riche. |
| **Personnage d'animation premium** | Fourrure détaillée, yeux expressifs, volumes doux, vêtements texturés, proportions stylisées. Ni réalisme animalier, ni jouet en plastique. |
| **Décor d'aventure** | Montagnes, forêt, brume, nuages éclairés par le soleil : dépassement de soi et aventure collective. |

## 2. Prompt maître

```text
# TRIBOS — CINEMATIC 3D ANIMATED ART DIRECTION

## 1. Creative direction
Create a premium cinematic website visual for Tribos, a social sports platform
built around group motivation, shared challenges and collective progress.
The visual identity combines the charm of high-end 3D animated feature films,
Pixar-inspired character appeal, cinematic environment design and premium
digital product art direction.
The atmosphere should feel adventurous, warm, aspirational, emotionally
engaging and sophisticated.
This is a stylized animated universe, not photorealism, not generic
mobile-game art and not childish cartoon design.

## 2. Signature color palette
Primary: vivid Tribos orange (#F87824).
Secondary: burnt orange, copper, amber and golden yellow.
Shadows: deep navy blue, charcoal and blue-grey.
Highlights: warm ivory and pale golden cream.
Character accent: rich teal or petrol blue sportswear.
Orange must remain the dominant brand color, integrated naturally into the
mascot, sunset lighting, environmental reflections and interface accents.

## 3. Character rendering
Use a high-quality stylized 3D animated-film aesthetic.
Characters feature:
- Expressive, readable eyes and facial expressions.
- Appealing stylized proportions.
- Soft, individually defined fur strands.
- Detailed ears, muzzle, cheeks and tail.
- Natural-looking fabric, stitching and folds.
- Physically coherent shadows and light reflections.
- Carefully sculpted silhouettes and clean material separation.
The result should have the production quality of a premium animated feature
film while maintaining a distinct original Tribos identity.
Avoid photorealistic animals, uncanny human realism, plastic figurine
materials and exaggerated baby-like proportions.

## 4. Canonical Tribos fox mascot
Preserve the established Tribos fox mascot across all generations.
Identity requirements:
- Orange fur with cream-colored cheeks, muzzle, chest and tail tip.
- Large pointed ears with warm pink inner fur.
- Expressive dark brown eyes.
- Distinctive fluffy tail.
- Teal athletic tank top and dark sports shorts.
- White athletic headband when appropriate.
- Confident, friendly and determined personality.
- Optional athletic backpack for outdoor adventure scenes.
Maintain consistent facial structure, fur colors, eye placement, body
proportions, clothing and recognizable silhouette.
Change the pose and expression to fit the scene, but never redesign the mascot.

## 5. Cinematic environment
Create a visually rich natural environment inspired by premium animated
adventure films.
Preferred environments:
- Mountain ranges at sunset.
- Pine forests and wooded trails.
- Outdoor training locations.
- Dramatic ridgelines and expansive landscapes.
- Atmospheric clouds and distant peaks.
Build depth using multiple environmental layers:
1. Dark, softly blurred foreground vegetation.
2. Detailed middle-ground terrain and forest.
3. Distant mountains with atmospheric haze.
4. Glowing sunset clouds and a luminous sky.
The environment should feel expansive, immersive and emotionally uplifting.

## 6. Cinematic lighting
Use a warm golden-hour lighting setup.
- Strong directional sunlight from behind or from the side.
- Warm orange rim light outlining the mascot's ears, fur and tail.
- Soft golden reflections on the character's face and clothing.
- Cool, deep blue shadows for complementary contrast.
- Volumetric sun rays and atmospheric haze where appropriate.
- Natural ambient occlusion and grounded contact shadows.
- Controlled highlights without excessive bloom.
The mascot must remain visually separated from the background.

## 7. Composition for website heroes
Design for a wide desktop website hero, preferably 16:9 or wider.
Use an intentional asymmetric composition:
- Left 40–45%: dark, uncluttered negative space reserved for headline,
  paragraph and CTA.
- Center-right: the fox mascot as the dominant focal point.
- Right side: optional subtle feature labels or supporting visual details.
- Background: expansive mountains and sunset, with enough local contrast to
  preserve text readability.
The fox should occupy approximately 35–45% of the hero's visual attention
without obscuring the headline or conversion form.
Keep the character large enough to convey personality and premium
craftsmanship.
The composition must remain adaptable to responsive mobile crops.

## 8. Website interface integration
The illustration and interface must feel art-directed together.
- White or warm ivory typography.
- Bold, modern sans-serif headlines.
- Orange emphasis on key words and primary CTA buttons.
- Dark translucent areas only where necessary for readability.
- Restrained rounded corners and subtle borders.
- Minimal navigation and clear hierarchy.
- No unnecessary cards, decorations or floating UI elements.
The image should support the website rather than overwhelm the product
information.
Never generate illegible text, fake interface labels or distorted logos inside
the artwork. Render text and UI as separate frontend elements.

## 9. Emotional direction
Communicate:
- Confidence without aggression.
- Ambition without toxic competition.
- Adventure and personal progress.
- Friendship and collective motivation.
- The feeling that sport is better when shared.
The mascot should feel like a memorable companion, not a generic fitness
influencer.

## 10. Quality control
Premium 3D animated-film rendering, coherent anatomy, detailed but controlled
fur, convincing material response, cinematic color grading, carefully staged
lighting, deep environmental perspective, strong silhouette readability and
consistent character design.
Every new asset must belong to the same visual universe.

## 11. Negative constraints
No flat vector illustration.
No 2D comic-book outlines.
No photorealistic wildlife.
No generic stock photography.
No plastic toy appearance.
No excessive lens flare or bloom.
No oversaturated neon colors.
No random floating particles.
No overly busy backgrounds behind text.
No inconsistent fox anatomy or costume.
No generated typography or inaccurate logos.
No excessive glassmorphism competing with the artwork.
```

## 3. Variante : le hero de référence

Pour retrouver le hero de référence (`references/hero/`).

```text
Create a cinematic, premium 3D animated-film website hero for Tribos, a social
sports and group-motivation brand.
Wide desktop composition, 16:9 aspect ratio.

SCENE:
An expansive mountain landscape at golden hour. Dramatic layered mountain
peaks, a dense pine forest, softly blurred foreground vegetation and warm
orange clouds illuminated by the setting sun. Deep blue-grey shadows contrast
with glowing amber and copper highlights.

CHARACTER:
The canonical Tribos orange fox mascot stands confidently in the center-right
foreground. The fox has expressive dark brown eyes, detailed soft orange fur,
cream cheeks and muzzle, large pointed ears, a fluffy cream-tipped tail, a
white athletic headband, a teal sleeveless sports top, dark navy sports shorts
and a small black outdoor backpack. Hands resting casually in the shorts
pockets, relaxed confident smile, upright athletic posture.

RENDERING:
Pixar-inspired premium 3D animated feature-film quality, sophisticated stylized
character design, beautifully groomed fur, detailed textile materials,
cinematic global illumination, realistic contact shadows, warm subsurface
scattering, golden rim lighting and atmospheric environmental depth.

COMPOSITION:
Reserve the entire left 40% as a dark, relatively uncluttered area for white
website typography and a call-to-action form. Place the fox prominently in the
center-right, large enough to show its facial expression and athletic outfit.
Keep the far-right area visually calm enough for small secondary feature
labels.

COLOR:
Tribos orange, burnt orange, copper, amber, golden cream, deep navy and
restrained teal.

MOOD:
Adventurous, confident, warm, premium, friendly and aspirational. The visual
communicates that sport is an adventure best shared with friends.

IMPORTANT:
Generate only the visual background and mascot. No typography, no website
navigation, no buttons, no logos, no UI elements and no watermark. These will
be implemented separately in the website frontend.

Maintain a polished, cohesive, high-end animated-film aesthetic. Avoid
photorealism, toy-like materials, childish proportions, excessive bloom and
clutter.
```

## 4. Les trois règles qui comptent le plus

1. **La mascotte reste identique.** Toujours l'image du renard canonique en
   référence ; le prompt décrit l'identité, l'image la garantit.
2. **Le décor fait partie de la signature.** Pas de renard sur fond orange
   uni par défaut : environnements profonds, lumière directionnelle, ombres
   froides — c'est ce contraste qui fait le style.
3. **L'image et le site sont séparés.** On génère décor + personnage en image
   propre ; titres, formulaire, navigation et boutons se font en HTML/CSS
   (site) ou en widgets (app). Interface nette, responsive, accessible.

## Intégration dans le site

- Texte blanc ou ivoire sur la zone sombre de gauche ; mots clés et CTA
  principal en orange (`#F3730A` côté interface).
- Voile sombre translucide **seulement** si la lisibilité l'exige (contraste
  AA minimum sur le titre et le texte du CTA).
- Prévoir un recadrage mobile dédié : le renard au centre, le texte au-dessus
  ou en dessous, jamais sur le visage.
- Exporter en WebP/AVIF, plusieurs largeurs (`srcset`), poids maîtrisé : un
  hero ne doit pas ralentir la page.
- Les règles d'intégration communes aux deux presets sont dans le skill
  `tribos-da-bd-cinematique` (§4) : elles s'appliquent aussi ici.
