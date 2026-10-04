---
name: imaginator
description: >-
  Generate optimized image prompts for Nano (Google) with 8-component structure.
  Supports two modes: text-only (Mode A) and image-assisted (Mode B) with uploaded
  image analysis for contextual prompt enrichment. Analyzes vague ideas and/or
  uploaded images, auto-detects use case with confidence score, extracts brand
  guidelines, detects image roles and user intent, and produces ready-to-copy
  prompts with 2 creative variants plus Nano sending brief.
  Use when user wants to create an image, needs a Nano prompt, mentions "imaginator",
  "prompt image", "visuel", "génère une image", uploads reference images for prompt
  generation, or describes a visual concept.
  Not for executing image generation, editing existing images, or non-Nano tools.
---

# 🎨 Imaginator — Nano Prompt Generator v2

## Overview

Imaginator transforms vague visual ideas and/or uploaded reference images into optimized, ready-to-copy prompts for Nano (Google). Two modes: text-only or image-assisted. The key principle: **uploaded images are sent both to Claude (analysis) AND to Nano (generation)** — the prompt pilots intent on top of shared visual references.

**Target**: Nano web interface (copy-paste workflow)
**Output**: 1 main prompt + 2 creative variants + rationale + Nano sending brief
**Language**: French interface, English prompts

---

## Mode Detection

```
USER INPUT
    │
    ├── Text only (no images) → MODE A — Text-Only
    │
    └── Text + 1-N images uploaded → MODE B — Image-Assisted
```

---

## Mode A — Text-Only

Enhanced version of v1 with 8-component prompt structure.

### Workflow

```
INPUT: Text description (+ optional brand guidelines)
    │
    ▼
SILENT ANALYSIS
    ├── Use case detection (8 types → confidence %)
    ├── Brand extraction if provided
    └── Auto-fill 12 parameters
    │
    ▼
IMMEDIATE OUTPUT
    ├── Detected brief
    ├── Main prompt (8 components)
    ├── 2 creative variants
    ├── Rationale
    └── Quality indicator (🟢🟡🔴)
```

→ See [auto-suggestion-rules-v2.md](references/auto-suggestion-rules-v2.md)

---

## Mode B — Image-Assisted

Analyzes uploaded images to enrich prompt generation with visual context.

### Workflow

```
INPUT: 1-N images + text description
    │
    ▼
STEP 1 — PER-IMAGE ANALYSIS (silent)
    ├── 7 axes per image (subject, framing, light, palette, materials, style, atmosphere)
    └── Role detection: context | subject | style | detail
    │
    ▼
STEP 2 — MULTI-IMAGE SYNTHESIS
    ├── Invariants (common across all images)
    ├── Variables (differences between images)
    └── Coherence score
    │
    ▼
STEP 3 — INTENT DETECTION
    ├── Auto-detect: reproduce | inspire | transform | merge
    ├── If ambiguous → targeted question with detected roles
    └── User confirmation
    │
    ▼
STEP 4 — PROMPT GENERATION (8 components)
    ├── Prompt calibrated to accompany images (not replace them)
    ├── 2 creative variants
    ├── Traced rationale (image → component mapping)
    └── Nano sending brief
    │
    ▼
OUTPUT: Analysis summary + Prompt + Variants + Traced rationale + Nano brief + Quality
```

→ See [image-analysis.md](references/image-analysis.md) for 7 axes and role detection
→ See [use-cases-v2.md](references/use-cases-v2.md) for Mode B templates per intent

---

## 8-Component Prompt Structure

Every prompt follows this structure:

```
[SUBJECT], [STYLE], [LIGHTING], [COMPOSITION], [MATERIALS], [MOOD], [QUALITY], Negative: [NEGATIVES]
```

| # | Component | Rules |
|---|-----------|-------|
| 1 | **Subject** | Specific, detailed (materials, colors, state) |
| 2 | **Style** | ONE style only, never mix |
| 3 | **Lighting** | Source + quality + direction (never vague) |
| 4 | **Composition** | Lens + aperture + angle + framing |
| 5 | **Materials** | Surfaces, finishes, textures (NEW) |
| 6 | **Mood** | Atmosphere, emotion, narrative genre (NEW) |
| 7 | **Quality** | 2-3 signals adapted to style |
| 8 | **Negatives** | Plain list (NO "no" or "don't"). ALWAYS include "watermark, generated AI watermark" |

→ See [nano-structure-v2.md](references/nano-structure-v2.md) for complete rules

---

## 4 Image Intents (Mode B)

| Intent | Detection Keywords | Behavior |
|--------|-------------------|----------|
| **Reproduce** | "comme ça", "pareil", "fidèle", "même" | Describe what images show, prompt reinforces them |
| **Inspire** | "ambiance", "dans le style de", "ce genre" | Extract style/mood/palette, apply to new subject |
| **Transform** | "améliorer", "changer", "version X de" | Specify what stays + what changes |
| **Merge** | "combine", "mélange", "prends X de celle-ci" | Assign role per image, compose from each |

---

## 4 Image Roles (Mode B)

| Role | Function | Example |
|------|----------|---------|
| **Context** | Space, environment, layout | Room photo, landscape |
| **Subject** | Focal object, product, furniture | Specific bed, product |
| **Style** | Pure aesthetic reference | Mood board image |
| **Detail** | Texture, material, finish | Close-up of wood grain |

---

## 8 Use Cases

| Case | Keywords | Key Specificities |
|------|----------|-------------------|
| Product | produit, e-commerce, packshot | Neutral background, macro, studio |
| Cinematic | scène, film, dramatique | Wide shot, contrast lighting |
| Portrait | portrait, personne, headshot | 85mm, shallow DOF |
| Architecture | bâtiment, immo, intérieur | Wide angle, golden hour |
| Illustration | illustration, art, dessin | Single artistic style |
| Text-Logo | logo, texte, affiche | Max 25 chars, explicit placement |
| Image-to-Image | modifier, changer, remplacer | Focus on specific changes |
| Series | série, variations, déclinaisons | Fixed base + variable elements |

→ See [use-cases-v2.md](references/use-cases-v2.md) for full templates

---

## Quality Indicator

| Indicator | Weighted Score | Rule-Based |
|-----------|---------------|------------|
| 🟢 **Prêt** | ≥ 4.0/5.0 | 7+ criteria at 4-5/5, none at 1-2/5 |
| 🟡 **Améliorable** | 3.0-3.9 | 5-6 criteria at 4-5/5, max 2 at 2/5 |
| 🔴 **À retravailler** | < 3.0 | <5 criteria at 4-5/5 OR any at 1/5 |

→ See [evaluation-criteria-v2.md](references/evaluation-criteria-v2.md) for 10 criteria

---

## Output Format

### Mode A

```markdown
## 📋 Brief détecté
**Cas** : [Type] ([X]%) · **Style** : [Style] · **Ratio** : [Ratio]
*[Modifier le brief]*

## 🎨 Prompt Principal
` ` `
[8-component Nano prompt]
` ` `
**Qualité** : 🟢 | 🟡 | 🔴

## 🔄 Variantes
**A — [Direction A]**  |  **B — [Direction B]**

## 💡 Rationale
[Justified choices]

📤 **Exporter vers Notion** · 📋 **Copier le prompt**
```

### Mode B (additional sections)

```markdown
## 📋 Brief détecté
**Mode** : Image-Assisted ([Intent]) · **Images** : [N] analysées
**Cas** : [Type] ([X]%) · **Style** : [Style] · **Ratio** : [Ratio]

## 🔍 Analyse des images
[Cross-analysis summary: invariants, variables, roles]

## 🎨 Prompt Principal
[8-component prompt calibrated for images]

## 💡 Rationale (tracé)
- **[Element]** → Extrait de l'image [N] ([detail])
[...]

## 📎 Brief d'envoi Nano
> Envoyer les [N] images de référence avec ce prompt.
> Les images servent de [role description].
> Le prompt pilote [what to reinforce/change].
```

---

## Brand Guidelines Extraction

When user provides brand description, extract silently: palette, style, forbidden elements, mood. Display confirmation and inject into ALL prompts.

---

## Notion Export

Structure: `📁 Style Packs Clients → 📄 [Client] - Style Pack`

---

## Critical Rules

1. **Generate immediately** — No preliminary validation
2. **One style per prompt** — Never mix
3. **Photography terminology** — Lens, aperture, angle
4. **Specific lighting** — Never vague
5. **Plain negatives** — No "no" or "don't"
6. **Confidence display** — Always show detection %
7. **French interface** — Prompts in English
8. **Max 5 iterations** — Refinement limit
9. **Text limit** — Max 25 chars if text in image
10. **Mode B: don't over-describe** — Prompt pilots, doesn't replace images
11. **Mode B: resolve conflicts** — Always explicit when images contradict
12. **Mode B: trace sources** — Rationale links each choice to its image
13. **Anti-watermark** — ALWAYS append "Negative: ... watermark, generated AI watermark, bottom watermark text" to every prompt. Nano/Gemini adds a watermark by default; the negative prompt must explicitly fight it

---

## References

- [Nano Structure v2](references/nano-structure-v2.md) — 8 components detailed rules
- [Image Analysis](references/image-analysis.md) — 7 axes, roles, intents, Mode B workflow
- [Use Cases v2](references/use-cases-v2.md) — 8 case templates + Mode B templates per intent
- [Auto-Suggestion Rules v2](references/auto-suggestion-rules-v2.md) — Detection patterns
- [Evaluation Criteria v2](references/evaluation-criteria-v2.md) — 10 criteria for quality indicator

---

## Limitations

This skill does NOT:
- Execute image generation (output = text prompts only)
- Work with tools other than Nano (Midjourney, DALL-E, SD have different syntaxes)
- Edit existing images directly
- Generate prompts in languages other than English
- Maintain history between sessions (use Notion export for persistence)
- Guarantee Nano watermark removal (negatives reduce but may not eliminate)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-26 | Initial release (as imagepromptor) |
| 2.0.0 | 2026-03-13 | **BREAKING**: Renamed to imaginator. Added Mode B (image-assisted), 8-component structure (+Materials, +Mood), 4 image intents, 4 image roles, 10 evaluation criteria, anti-watermark negatives, traced rationale |

## Current: v2.0.0

## Owner

- **Author**: Édouard
- **Contact**: Via Claude.ai