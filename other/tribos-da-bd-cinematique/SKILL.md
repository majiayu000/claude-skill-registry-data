---
name: tribos-da-bd-cinematique
description: Direction artistique Tribos « Illustration BD cinématographique, aventure sportive et mascotte 3D stylisée ». À lire AVANT de générer ou de commander une illustration Tribos (site, app, fiche store, réseaux, campagne), de rédiger un prompt d'image, ou d'intégrer des visuels dans l'interface (hero, états vides, onboarding, démonstrations d'exercices). Contient le prompt maître, les règles par type de visuel et les règles d'intégration UI.
---

# Tribos — DA « BD cinématographique » (v1.0)

Une identité reconnaissable sur le site, l'app, les illustrations de
fonctionnalités et les visuels marketing : **bande dessinée contemporaine
mise en scène comme un film d'animation**, sport vécu en groupe, et un renard
mascotte qui relie tous les supports.

C'est le preset **« Illustrated Comic »**, un des trois presets officiels
(voir [`docs/brand/README.md`](../../../docs/brand/README.md)) :
- **Illustrated Comic** (ce skill) : illustrations BD, fonctionnalités,
  exercices, groupes, états vides ;
- **Cinematic 3D** (`tribos-da-3d-cinematique`) : grands visuels marketing.

- **Minimalist Premium Dark** (`tribos-da-minimal-dark`) : studio noir,
  lumière orange géométrique, renard en mouvement.

Même mascotte, palettes voisines, rendus différents. **Un seul preset par support.**

## Avant toute génération

1. **Joins le renard canonique** : `docs/brand/mascotte/` (partagé par tous
   les presets, décrit dans `docs/brand/README.md`), puis les références de
   style de [`references/`](references/README.md). Un prompt texte seul ne suffit pas à
   garder la mascotte cohérente sur des dizaines d'images : fournis toujours
   l'image de référence au modèle.
2. **Identifie le rôle du visuel** (§3) : hero, mascotte/exercice, groupe ou
   produit. Le rôle décide du niveau de détail, pas le goût du moment.
3. **Fixe** la taille d'affichage, le point focal, le fond et la zone vide
   nécessaire au texte ou à l'interface.
4. Pars du **prompt maître** (§2) et ne change que scène, action et cadrage,
   via le gabarit (§5).

## 1. Identité

- Univers de bande dessinée contemporaine, mise en scène de film d'animation.
- Ton chaleureux, sportif, collectif et accessible. Expressif et immersif,
  **jamais enfantin**.
- Mélange d'illustration peinte, de volumes 3D stylisés et de composition
  éditoriale.
- Le renard est le personnage récurrent. Le sujet principal reste **le sport
  collectif** ; le renard est un repère de marque, pas une présence partout.

### Palette (valeurs de départ)

| Rôle | Couleur | Hex |
|---|---|---|
| Signature | Orange | `#FF791F` |
| Profondeur chaude | Terre cuite | `#D94F16` |
| Lumière, fonds clairs | Crème | `#FFF0DC` |
| Contraste, ombres | Bleu nuit | `#18242B` |
| Accent contrôlé (tenue du renard) | Pétrole | `#237F7A` |

À harmoniser avec les couleurs réelles du produit (`lib/core/app_theme.dart` :
`AppTheme.primary` = `#F3730A`, crème `#FDF4EA`, encre `#2C3A43`). En cas
d'écart, **le produit fait foi** pour l'interface ; la palette ci-dessus
guide les illustrations.

## 2. Prompt maître (à réutiliser tel quel)

```text
# TRIBOS — MASTER ART DIRECTION

## Visual identity
Create a premium cinematic comic-book illustration for Tribos, a social sports
and group-motivation platform.
The art direction combines contemporary European graphic novel aesthetics,
painterly concept art, stylized animated-film character design, and premium
editorial illustration.
The result must feel like a cohesive fictional universe, not a generic fitness
advertisement.

## Color palette
- Dominant vivid warm orange and burnt orange.
- Secondary amber, copper, terracotta and golden sunset tones.
- Cream and warm ivory for highlights and light surfaces.
- Deep charcoal, midnight blue and muted blue-grey for atmospheric contrast.
- Teal or petrol blue as a controlled accent, especially on the fox mascot's
  sportswear.
Orange is the signature color. Use it consistently across backgrounds,
lighting, clothing accents and visual identity.

## Illustration style
- Painterly, detailed environments with visible artistic brushwork.
- Strong, readable silhouettes.
- Stylized anatomy and appealing, expressive characters.
- Cinematic composition with foreground, middle ground and background.
- Atmospheric depth, soft haze, dramatic rim lighting and warm reflected light.
- Graphic-novel storytelling, visual rhythm and carefully controlled contrast.
- Sophisticated material rendering, with soft fur, textured fabrics and natural
  environmental details.
- A polished finish suitable for a premium consumer technology brand.

## Mascot consistency
Use the established Tribos orange fox mascot as a recurring brand character.
Preserve its recognizable orange fur, cream muzzle and chest accents,
expressive eyes, large ears, distinctive fluffy tail and athletic teal clothing.
Maintain consistent proportions, facial features, color distribution and
personality across illustrations.
The fox should feel confident, approachable, determined and slightly playful.
Adapt its pose and expression to the scene without redesigning the character.

## Storytelling
Show sport as a shared adventure rather than an isolated performance.
Use gestures, movement, body language, group interactions and environmental
storytelling to communicate friendship, motivation, progress and collective
effort. Make the action understandable at a glance.

## Lighting and composition
Use directional golden-hour lighting, warm orange highlights, deep cool shadows
and cinematic atmospheric perspective.
Create clear focal points and intentional negative space.
Prioritize readable silhouettes and strong composition at both desktop and
mobile sizes.
Leave uncluttered areas when text or interface elements will overlay the
illustration.

## Quality
High-quality original illustration, professional art direction, sophisticated
color grading, coherent anatomy, believable sports movements, rich but
controlled detail, consistent character design.

## Avoid
Generic stock photography, photorealistic humans, flat corporate vector art,
childish clipart, excessive outlines, oversaturated neon colors, excessive
bloom, plastic-looking characters, inconsistent mascot designs, random
decorative elements, illegible text, logos generated inaccurately, and overly
busy compositions.

The final image must look unmistakably like part of the Tribos visual universe.
```

## 3. Règles par type de visuel

Le style est le même partout ; c'est le **rôle** qui change le niveau de
spectacle. Le marketing peut être spectaculaire, une illustration de
fonctionnalité doit rester lisible.

| Type | Intention | Règles | Où |
|---|---|---|---|
| **A. Hero** | Cinématique | Grand décor peint (coucher de soleil, montagne, terrain de sport). Mascotte au premier plan, silhouette identifiable. Composition asymétrique avec une zone sombre ou calme pour le titre. Lumière orange chaude, ombres bleu nuit. | Landing page, campagnes, grandes sections éditoriales |
| **B. Mascotte et exercices** | Lisibilité du mouvement | Pose compréhensible en une seconde. Articulations, mains et pieds bien visibles. Fond simple, silhouette détachée. **Angle de vue constant** pour comparer les étapes d'un exercice. | Démonstrations sportives, futures animations IA |
| **C. Groupe et communauté** | Humain et collectif | Plusieurs personnages qui interagissent vraiment (encouragement, course commune, célébration, entraide). Composition qui guide le regard entre eux. Orange dominant, mais vêtements et silhouettes variés. | Pages groupe, progression collective, recrutement |
| **D. Illustrations produit** | Simple et cohérent | Fond crème, sombre uni ou dégradé très léger. Un personnage ou une action. Détails limités (lisible en petit). Ombres douces, accents orange. | Widgets, états vides, onboarding, illustrations secondaires |

## 4. Règles d'intégration UI (pour l'agent de développement)

Le piège : transformer cette DA en site générique fait de dégradés orange et de
cartes arrondies, ou faire de toute l'interface une illustration.

1. Illustration et système d'interface sont **deux couches complémentaires**.
2. Artwork BD cinématographique pour le marketing ; illustrations sobres dans
   l'interface produit.
3. L'orange reste la signature, équilibré par le charbon, l'ivoire chaud et le
   pétrole atténué.
4. **Jamais** un style d'illustration différent par page : un seul univers.
5. Préserver le design canonique du renard sur tous les écrans et assets.
6. Chaque artwork a un but : sport, motivation de groupe, progression,
   intégration ou célébration.
7. Textes, navigation, boutons, graphiques et données restent des **éléments
   d'interface natifs**. Ne jamais les générer dans une image.
8. Pas d'artwork détaillé derrière un petit texte, un formulaire ou un
   contrôle essentiel.
9. Contraste fort et espace négatif suffisant ; pas de bruit visuel ni
   d'excès de dégradés.
10. Contours BD, trames et grain : **avec parcimonie**, pas partout.
11. Ratios d'image cohérents et points focaux prévisibles entre composants
    liés.
12. Assets optimisés pour le responsive ; recadrages ou compositions
    distincts quand mobile et desktop l'exigent.
13. La mascotte soutient l'expérience, elle ne rivalise pas avec le contenu
    important.
14. Avant tout nouvel asset : rôle, taille d'affichage, point focal, fond et
    espace négatif requis.
15. Mieux vaut **peu d'assets très cohérents** qu'une collection d'images IA
    disparates.

## 5. Gabarit pour une nouvelle illustration

```text
Create a new Tribos illustration following the established Tribos Master Art
Direction.

Scene: [Describe the scene]
Purpose: [Website hero / group feature / exercise demonstration / onboarding / campaign]
Main subject: [Fox mascot / group of friends / athlete]
Action: [Describe the exact action]
Environment: [Mountain trail / urban park / gym / minimal background]
Composition: [Wide cinematic / portrait / centered character / negative space on the left]
Lighting: Warm golden-hour light, orange rim lighting, deep blue-grey shadows.
Palette: Burnt orange, amber, cream, charcoal and restrained teal accents.
Rendering: Premium painterly graphic novel illustration, stylized animated-film
character design, sophisticated materials, expressive silhouettes and
atmospheric depth.
Consistency: Match the established Tribos fox design and the existing brand
illustrations.
Constraints: [Transparent background / no text / no logo / clear exercise
posture / mobile crop requirements]

The image must communicate its purpose immediately and feel like an original
illustration from the same cohesive Tribos universe.
```

## Système à deux niveaux

- **Site marketing** : BD cinématographique, décors peints, lumière orange,
  mascotte expressive, scènes de groupe.
- **Application** : même univers, compositions simplifiées, fonds calmes,
  illustrations fonctionnelles.

## État des lieux (à résoudre, pas à reproduire)

Les assets actuels ne suivent pas encore cette DA. Ne les prends **pas** comme
référence de style :

- `assets/mascotte/loup.png` (carte « Séance du jour ») : un **loup gris** en
  débardeur jaune, cartoon à plat — pas le renard orange en tenue pétrole.
- Le splash et l'icône utilisent le renard blanc stylisé (logo), qui reste
  le **logo** : il ne remplace pas la mascotte illustrée.

Avant de remplacer l'un d'eux, vérifie avec l'utilisateur : changer la
mascotte de l'app touche aussi les captures des stores (skill
`tribos-site-sync`, `docs/app-store.md`).
