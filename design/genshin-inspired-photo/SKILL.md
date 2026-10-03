---
name: genshin-inspired-photo
description: Transform supplied photos or written concepts into luminous Genshin Impact-inspired anime-fantasy imagery while preserving the original subject, identity, pose, composition, architecture, landscape, or food structure. For people, default to dimensional 3D anime game rendering and function-preserving redesign of modern clothing and accessories so the person belongs in the selected nation without becoming a copied character. Includes nation-specific direction for Mondstadt/蒙德, Liyue/璃月, Inazuma/稻妻, Sumeru/须弥, Fontaine/枫丹, Natlan/纳塔, and the northern Nod-Krai/Snezhnaya direction. Use for people, portraits, outfits, pets, landscapes, buildings, streets, interiors, vehicles, objects, and dishes when the user asks for 原神风, 原神3D人物, a named Genshin nation, Teyvat-like fantasy, elemental anime game art, cel-shaded fantasy photography, or a bright open-world anime RPG look.
---

# Genshin-Inspired Photo

Create polished fan-style transformations that evoke a bright elemental anime open world without reproducing official artwork. Build the result from clear shape design, luminous atmosphere, nation-specific spatial and material logic, and restrained cel shading—not from character cosplay, random glowing particles, or a generic anime filter.

## Required Behavior

- Inspect every supplied image before editing it and treat it as the edit target.
- For follow-up edits, preserve every previously approved layer even when the approved subject, clothing, equipment, and background come from different images. Never assume the newest output is authoritative for every layer.
- Use the built-in image generation/editing tool. Preserve the source aspect ratio unless the user requests another format.
- Preserve identity, pose, expression, body proportions, object completeness, food structure, camera viewpoint, and important scene geometry unless explicitly asked to change them.
- When a person is present, use dimensional 3D anime game rendering by default. Do not leave a photographic body under a painted anime face or reduce the person to flat 2D illustration.
- Convert every visible human, not only the hero. Background crowds may use simplified faces and garments, but no person may remain a photographic modern tourist, office worker, school-uniform figure, or contemporary streetwear silhouette inside a converted world.
- In World conversion and Key-art cinematic modes, translate conspicuously modern clothing and accessories into nation-compatible equivalents while preserving their function, attachment point, carried volume, interaction, key color, and broad silhouette. Do not preserve anachronism at the cost of world coherence.
- Keep the transformation clearly original. Do not copy an official character, costume, weapon, city, landmark, promotional composition, logo, interface, elemental icon, or readable game text unless the user explicitly supplies or requests that exact protected element.
- Do not bundle online reference images in any publishable skill package. Use web images only to infer abstract visual principles; private local calibration boards are the sole exception and must remain excluded from publication.
- Produce no watermark, username, UID, game UI, fake logo, caption, or illegible text.

## Workflow

### 1. Classify the Input

Choose one primary subject class:

- **Person or creature:** identity, expression, silhouette, pose, clothing, hair, and accessories are the anchors.
- **Landscape:** landform, horizon, weather, scale, and exploration path are the anchors.
- **Architecture or interior:** massing, facade rhythm, openings, material logic, and cultural context are the anchors.
- **Food or object:** recognizable ingredients, construction, volume, surface texture, and presentation are the anchors.

If several classes appear, select one hero and treat the others as supporting context.

### 2. Choose Transformation Strength

- **Faithful paint-over:** preserve framing and content; change rendering, palette, atmosphere, and small decorative details only.
- **World conversion:** preserve the subject and scene layout; reinterpret materials, vegetation, clothing trim, lighting, and secondary details as a coherent elemental fantasy world.
- **Key-art cinematic:** allow a modest crop, more dynamic depth, wind, particles, and a stronger elemental light path; preserve identity and the core event.

Use Faithful paint-over by default for personal photographs.

### 2A. Set Landscape Anchor Strength

For landscape, architecture, city and environment-heavy inputs, set one explicit anchor strength:

- **Subtle:** preserve nearly all existing content; use only one quiet source-compatible world cue. Use only when the user asks for restraint, realism or a light touch.
- **Readable — default:** add one legible midground landmark or functional structure, one route that leads toward or through it, and one elemental system that visibly affects the route, structure or terrain.
- **Strong:** use when the user says “太克制,” “看不出来是原神,” “锚点不够,” “更像游戏,” or equivalent. Give the primary landmark roughly 10–25% of the frame width or comparable visual weight, keep it clear of heavy occlusion, and connect foreground, midground and distance through a navigable path and functional elemental flow.

Stronger anchor strength does not permit terrain replacement, copied landmarks, random castles or particle overload. Increase readable world structure, spatial linkage and function—not decoration density.

### 3. Choose a Nation Before an Element

Read [references/nation-atlas.md](references/nation-atlas.md). Select one nation direction before choosing an element:

- If the user names a nation, follow it.
- If the source already has strong cultural or geographic cues, choose the closest compatible nation without replacing those cues.
- If neither is clear, select the direction that best supports the subject and mood; do not blend several nations merely to add detail.
- Treat subregions such as Dragonspine, Chenyu Vale, Enkanomiya, the Sumeru desert, or Fontaine's underwater world as specific variants, not as generic effects.

Apply the selected nation's rules to environment, architecture, clothing, materials, ornament, food presentation, palette, and atmosphere. Use original motifs derived from the source; do not recreate a named city, landmark, costume, emblem, or prop.

### 4. Choose One Elemental Direction

Select one primary direction from the source colors, weather, location, food ingredients, or user prompt:

- **Wind:** turquoise sky, white cloud volume, grass motion, feathers, ribbons, airy light.
- **Stone:** amber-gold light, mineral geometry, layered cliffs, carved motifs, grounded weight.
- **Lightning:** violet-blue atmosphere, sharp energy accents, rain sheen, lacquered surfaces, tense contrast.
- **Nature:** jade and leaf green, luminous plants, pollen, rainforest depth, scholarly ornament.
- **Water:** cyan, pearl white and deep blue, reflective canals, bubbles, glass, flowing curves, clockwork accents.
- **Fire:** vermilion, warm gold, turquoise counterpoints, volcanic light, woven geometry, energetic rhythm.
- **Ice:** pale blue, silver, lavender shadow, crystalline edges, snow haze, formal elegance.

Use one dominant element and at most one quiet secondary accent. Do not cover the frame with unrelated elemental effects.

The element is subordinate to the nation. A Mondstadt Wind scene and an Inazuma Lightning scene must differ in spatial rhythm, materials, architecture, and clothing—not only in color or particles.

### 5. Preserve the Source Before Styling

Write a protected-invariants list in every edit prompt:

- people: identity, facial structure, age, ethnicity, expression, hairstyle, pose, hands, clothing silhouette and key colors;
- landscapes: horizon, mountain profile, shoreline, road or river path, major trees and buildings;
- architecture: footprint, number of floors, roofline, doors, windows, structural supports and perspective;
- food: ingredient count, doneness, portion shape, container, plating orientation and edible appearance.

Do not add fantasy props that block, replace, or truncate the original hero subject.

### 5A. Lock Iteration Lineage

Before every follow-up edit, write a compact **layer provenance map**:

```text
Composition and camera: [authoritative image]
Hero identity, pose and anatomy: [authoritative image]
Approved clothing and equipment: [authoritative image]
Approved environment and architecture: [authoritative image]
Requested change: [one layer only]
```

- Treat the user's latest accepted result for each layer as authoritative, not automatically the latest generated image.
- A request such as “make the background more Mondstadt” changes only the environment. It must not revert an already approved coat, hat, camera, face, pose, architecture, food, or object design.
- If the newest image contains a regression, do not preserve that regression. Use multi-image compositing: one image supplies the edit target and approved background; another supplies the approved subject, garment, equipment, or object appearance.
- Label every input image by role and state both **keep from image A** and **transfer from image B**. Repeat the locked layers in the prompt's final constraints.
- Allow changes outside the requested layer only for minimal contact shadow, reflected light, atmospheric integration, or edge cleanup.

### 6. Perform a Functional Translation Pass

If a person or modern object is present, read [references/character-rendering.md](references/character-rendering.md). Classify each visible item:

- **Keep:** already neutral or world-compatible; retain it with only material and rendering changes.
- **Translate:** visually modern but functionally important; redesign it as a nation-compatible equivalent.
- **Remove branding only:** keep the item but erase logos, model names, UI and commercial text.

Identity, action and function are protected. Surface design is flexible. A camera must remain an optical recording device; sunglasses must remain eye protection; a waterproof jacket must remain weather protection; a backpack must retain its storage volume and straps.

Translate only what visibly clashes. Do not turn every traveler into ceremonial cosplay, armor, or a named playable character.

### 7. Choose the Rendering Mode

- **3D anime world render — default when any person is present:** sculpted forms, clean toon-shader shadow bands, hand-painted albedo textures, physically readable cloth/metal/leather/glass, ambient occlusion at overlaps, controlled specular highlights, rim and bounce light from the environment.
- **3D environment render — default for architecture, food, objects and most landscapes:** modeled depth and practical material response with painterly texture simplification.
- **Illustrated key art — only when the user requests illustration, poster, splash art, or a deliberately painterly result:** stronger brushwork and graphic staging, while retaining volume.

Apply one rendering mode coherently across subject and environment. Do not paste a 3D person onto a flat painted background or vice versa.

### 8. Apply the Visual System

Read [references/visual-language.md](references/visual-language.md) for shape, rendering, color, lighting, materials, depth, and nation routing.

Read [references/genshin-anchor-system.md](references/genshin-anchor-system.md) for the recognition gate. Every finished image must carry at least four mutually reinforcing anchor families: renderer, nation, elemental world function, character/civilian design, and exploration composition. Color or particles alone never count as sufficient anchors.

For landscape-led images, also apply the anchor-scale and thumbnail gates. If the nation or game-world identity disappears when the image is viewed at roughly 20% size, enlarge or clarify the primary midground structure and its functional route instead of adding more particles.

Always include:

- a clean, readable silhouette;
- anime-inspired but dimensional forms;
- controlled cel-shaded shadow regions blended with soft painterly gradients;
- hand-painted surface variation rather than photoreal noise;
- atmospheric depth with a bright, explorable sense of space;
- one motivated elemental light or motif tied to the scene.

### 9. Apply Subject-Specific Rules

Read the matching section in [references/subject-recipes.md](references/subject-recipes.md):

- people and creatures;
- landscapes;
- architecture and interiors;
- food and objects.

Do not use a portrait recipe on food or force clothing ornament onto a landscape.

### 10. Build the Prompt

Use [references/prompt-recipes.md](references/prompt-recipes.md). State, in order:

1. edit or generation use case;
2. source truth, layer provenance and protected invariants;
3. hero subject and action;
4. composition and depth;
5. transformation strength and landscape anchor strength;
6. nation direction and subregion, if any;
7. primary landmark scale, exploration route and elemental world function for landscape-led images;
8. functional translations for clothing, accessories and equipment;
9. rendering mode, with 3D anime world render as the person default;
10. elemental direction;
11. palette, materials, lighting and contact integration;
12. nation-specific exclusions and general exclusions.

Translate user personalization literally. “More realistic,” “less game-like,” “keep the clothes,” “no magic,” or “make the food cuter” must override defaults.

### 11. Generate and Review

After generation, inspect the result and make one targeted correction if needed. Review in this order:

1. no regression against each authoritative lineage image;
2. identity, expression, pose and action fidelity;
3. item function, attachment, carried volume and key-color continuity;
4. complete anatomy, architecture, food and objects;
5. coherent 3D anime rendering across person and world;
6. all background people converted into the same world and renderer;
7. four or more legible Genshin-style anchor families;
8. landscape anchor scale and recognition at roughly 20% thumbnail size;
9. composition and perspective;
10. coherent nation and subregion design;
11. coherent elemental design that supports rather than replaces the nation;
12. rendering quality and AI artifacts;

## Style Guardrails

- Keep faces recognizable; stylize planes, eyes, hair groups, and color—not identity.
- Keep eyes plausible for the chosen stylization strength. Do not enlarge them automatically.
- Keep skin softly modeled with limited cel shadow shapes; avoid porcelain plastic skin.
- Simplify texture frequency while retaining material differences: hair, cloth, stone, metal, wood, glass, water, foliage, and food must not look identical.
- Use ornate detail at focal areas and quieter shapes elsewhere.
- Use elemental particles sparingly and give them a physical path: wind flow, reflected water light, rising heat, drifting pollen, falling snow, or electrical arcs.
- Keep the scene inviting and explorable. Avoid flat poster backgrounds unless requested.
- Preserve natural hands, facial features, building structures, ingredient boundaries, and object counts.
- Make the chosen nation legible through at least three mutually reinforcing systems—such as terrain, architecture, and materials—rather than through one token prop.
- Do not identify a nation only by color. Purple alone is not Inazuma; blue alone is not Fontaine; green alone is not Sumeru.
- Give clothing real construction: layer thickness, hems, seams, closures, tension, folds, and contact shadow. Ornament must follow panels and joints rather than float on the surface.
- Preserve the source person's role. A hiker remains a hiker, a photographer remains a photographer, and a cook remains a cook after redesign.

## Avoid

- direct copies of official characters, outfits, weapons, mascots, icons, maps, UI, logos, or promotional art;
- adding Paimon-like companions, floating menus, rarity stars, health bars, or game screenshots by default;
- generic chibi, flat 2D anime, heavy black comic outlines, or pure cel shading with no volume;
- unchanged modern sportswear, baseball caps, branded cameras, phones or sunglasses that visibly break the selected world when the transformation mode allows redesign;
- full ceremonial costume, fantasy armor or excessive accessories imposed on an ordinary functional outfit;
- oversaturated rainbow palettes, neon cyberpunk, excessive bloom, or particles everywhere;
- photoreal backgrounds with a pasted anime face;
- replacing a real building with an unrelated fantasy castle;
- turning food into plastic toys, losing ingredients, or making it visibly inedible;
- malformed hands, duplicated accessories, broken roofs, fake lettering, watermarks, or UIDs.

## Completion Checklist

- Is the original hero still immediately recognizable?
- Does every previously approved layer still match its authoritative lineage image, with no clothing, equipment, background, identity, pose, or geometry regression?
- Are pose, composition, geometry, and object completeness preserved?
- Do redesigned clothes and accessories preserve their original function, attachment and broad silhouette?
- Does every person read as a dimensional 3D anime game character under the same light as the environment?
- Have modern items been structurally rebuilt rather than merely decorated?
- Are all background people world-compatible even when small?
- Are at least four anchor families legible without relying on text, logos, copied characters, UI, or a single color?
- In a landscape-led image, does one primary midground anchor remain legible at roughly 20% size, with a visible route and elemental function connecting it to the scene?
- Does one coherent elemental direction govern palette and effects?
- Is one nation or subregion clearly legible through spatial, cultural, and material design without copying an official asset?
- Would the nation still be recognizable if all magical particles were removed?
- Does the image combine clean anime shapes with painterly volume and atmospheric depth?
- Are decorative motifs tied to subject, material, or region rather than randomly applied?
- Is the result original and free of official logos, UI, copied characters, watermarks, and fake text?
