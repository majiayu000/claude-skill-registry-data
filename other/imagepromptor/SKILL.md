---
name: imagepromptor
description: >-
  Generate optimized image prompts for Nano (Google) with 6-component structure.
  Analyzes vague ideas, auto-detects use case with confidence score, extracts brand
  guidelines from free text, and produces ready-to-copy prompts with 2 creative variants.
  Use when user wants to create an image, needs a Nano prompt, mentions "imagepromptor",
  "prompt image", "visuel", "génère une image", or describes a visual concept.
  Not for executing image generation, editing existing images, or non-Nano tools.
---

# 🎨 Imagepromptor — Nano Prompt Generator

## Overview

Imagepromptor transforms vague visual ideas into optimized, ready-to-copy prompts for Nano (Google). It uses a "generate first, refine if needed" approach: immediate prompt generation with optional iteration based on quality indicators.

**Target**: Nano web interface (copy-paste workflow)  
**Output**: 1 main prompt + 2 creative variants + rationale  
**Language**: French interface, English prompts

---

## Quick Workflow

```
USER INPUT (vague idea + optional brand guidelines)
                    │
                    ▼
        ┌───────────────────────┐
        │   SILENT ANALYSIS     │
        │   • Use case detection│
        │   • Brand extraction  │
        │   • Auto-fill 10 params│
        └───────────────────────┘
                    │
                    ▼
        ┌───────────────────────┐
        │   IMMEDIATE OUTPUT    │
        │   • Detected brief    │
        │   • Main prompt       │
        │   • 2 variants        │
        │   • Rationale         │
        │   • Quality indicator │
        └───────────────────────┘
                    │
        ┌───────────┴───────────┐
        ▼                       ▼
   🟢 READY                🟡🔴 REFINE
   → Copy & Export         → Answer questions
                           → New version
```

---

## Main Workflow

### Step 1: Receive Input

User provides:
- **Required**: Vague idea or visual concept description
- **Optional**: Brand guidelines (free text or PDF mention)

### Step 2: Silent Analysis

Analyze input without asking validation:

1. **Detect use case** among 8 types → assign confidence %
2. **Extract brand guidelines** if provided (palette, style, mood, forbidden elements)
3. **Auto-fill 10 parameters** based on detection rules

→ See [auto-suggestion-rules.md](references/auto-suggestion-rules.md)

### Step 3: Generate Immediately

Produce complete output in one response:

```markdown
## 📋 Brief détecté
**Cas** : [Type] ([X]%) · **Style** : [Style] · **Ratio** : [Ratio]
*[Modifier le brief]*

---

## 🎨 Prompt Principal

` ` `
[6-component Nano prompt]
` ` `

**Qualité** : 🟢 Prêt | 🟡 Améliorable | 🔴 À retravailler

---

## 🔄 Variantes

**A — [Creative direction A]**
` ` `
[Variant prompt A]
` ` `

**B — [Creative direction B]**
` ` `
[Variant prompt B]
` ` `

---

## 💡 Rationale
- **[Choice 1]** → [Short justification]
- **[Choice 2]** → [Short justification]
- **[Choice 3]** → [Short justification]

---

📤 **Exporter vers Notion** · 📋 **Copier le prompt**
```

### Step 4: Refine if Needed

If quality is 🟡 or 🔴:
1. Display targeted questions (auto-generated based on weak criteria)
2. Also suggest automatic improvements
3. User can answer OR accept suggestions
4. Generate new version
5. Max 5 iterations

---

## Nano Prompt Structure (6 Components)

Every prompt MUST follow this exact structure:

```
[SUBJECT], [STYLE], [LIGHTING], [COMPOSITION], [QUALITY], Negative: [NEGATIVES]
```

| # | Component | Rules | Example |
|---|-----------|-------|---------|
| 1 | **Subject** | Specific, detailed (materials, colors, state) | "A premium skincare bottle in frosted glass with gold cap" |
| 2 | **Style** | ONE style only, never mix | "photorealistic" |
| 3 | **Lighting** | Source + quality + direction | "soft diffused studio light with warm accents from right" |
| 4 | **Composition** | Lens + aperture + angle + ratio | "100mm macro f/2.8, centered, shallow depth of field" |
| 5 | **Quality** | 2-3 signals adapted to style | "4K professional quality, luxury magazine aesthetic" |
| 6 | **Negatives** | Plain list (NO "no" or "don't") | "harsh shadows, fingerprints, dust, reflections, text" |

→ See [nano-structure.md](references/nano-structure.md) for complete rules

---

## Quality Indicator

| Indicator | Meaning | Criteria (background) |
|-----------|---------|----------------------|
| 🟢 **Prêt** | Complete and coherent | 6+ criteria at 4-5/5, none at 1-2/5 |
| 🟡 **Améliorable** | Functional, optimizable | 4-5 criteria at 4-5/5, max 2 at 2/5 |
| 🔴 **À retravailler** | Significant gaps | <4 criteria at 4-5/5 OR critical at 1/5 |

→ See [evaluation-criteria.md](references/evaluation-criteria.md) for 8 criteria details

---

## 8 Use Cases

| Case | Detection Keywords | Key Specificities |
|------|-------------------|-------------------|
| **Product** | produit, e-commerce, packshot | Neutral background, macro, studio |
| **Cinematic** | scène, film, dramatique | Wide shot, contrast lighting |
| **Portrait** | portrait, personne, headshot | 85mm, shallow DOF, expressions |
| **Architecture** | bâtiment, immo, intérieur | Wide angle, golden hour |
| **Illustration** | illustration, art, dessin | Single artistic style |
| **Text-Logo** | logo, texte, affiche | Max 25 chars, explicit placement |
| **Image-to-Image** | modifier, changer, remplacer | Focus on specific changes |
| **Series** | série, variations, déclinaisons | Fixed base + variable elements |

→ See [use-cases.md](references/use-cases.md) for templates per case

---

## Brand Guidelines Extraction

When user provides brand description (free text), extract silently:

```
Input: "Ma charte c'est épuré, bleu marine et blanc cassé, 
        style scandinave, jamais de dorures, ambiance calme"

Extraction:
  Palette    : bleu marine, blanc cassé
  Style      : minimaliste scandinave  
  Forbidden  : dorures
  Mood       : calme, professionnelle
```

Display as confirmation:
> 📋 **Charte détectée** : minimaliste scandinave, palette bleu marine/blanc cassé, ambiance calme. *Modifier ?*

Inject extracted elements into ALL generated prompts.

---

## Notion Export

When user requests export, create page structure:

```
📁 Style Packs Clients
  └── 📄 [Client Name] - Style Pack
        ├── 🎨 Detected brand guidelines
        ├── 📋 Validated prompts (with quality indicator)
        └── 🔄 Favorite variants
```

---

## Critical Rules

1. **Generate immediately** — No preliminary validation, output directly
2. **One style per prompt** — Never mix styles (NO "watercolor + photorealistic")
3. **Photography terminology** — Always use lens, aperture, angle terms
4. **Specific lighting** — Never vague ("good lighting" = ❌)
5. **Plain negatives** — List items only, no "no" or "don't"
6. **Confidence display** — Always show detection % for use case
7. **French interface** — Communicate in French, prompts in English
8. **Max 5 iterations** — Stop after 5 refinement cycles
9. **Text limit** — If text in image: max 25 characters, explicit placement

---

## Example

**Input**: 
> "Je veux une image pour mon site e-commerce de cosmétiques bio, ambiance luxe naturel pour Instagram"

**Output**:

## 📋 Brief détecté
**Cas** : Produit (89%) · **Style** : Photoréaliste · **Ratio** : 1:1
*[Modifier le brief]*

---

## 🎨 Prompt Principal

```
A premium organic skincare bottle in frosted glass with bamboo cap,
photorealistic,
soft diffused studio light with warm golden accents from right side,
100mm macro f/2.8, centered on natural stone surface, shallow depth of field,
4K professional quality, luxury organic aesthetic, sharp product detail,
Negative: harsh shadows, fingerprints, dust, artificial feel, plastic, text, watermark
```

**Qualité** : 🟢 Prêt

---

## 🔄 Variantes

**A — Direction nature immersive**
```
A premium organic skincare bottle in frosted glass with bamboo cap,
photorealistic,
soft natural morning light through leaves, dappled shadows,
85mm f/2, product nestled among fresh eucalyptus and river stones,
4K organic luxury aesthetic, natural color palette,
Negative: artificial lighting, studio feel, plastic, harsh contrast, text
```

**B — Direction minimaliste épurée**
```
A premium organic skincare bottle in frosted glass with bamboo cap,
photorealistic,
soft even lighting, minimal shadows, clean aesthetic,
90mm f/4, product centered on pure white surface, generous negative space,
4K minimalist luxury, pristine clarity,
Negative: busy background, shadows, reflections, texture, dust, text
```

---

## 💡 Rationale
- **Photoréaliste** → Crédibilité produit e-commerce
- **Macro 100mm** → Standard packshot, bokeh naturel
- **Bamboo cap** → Renforce le positionnement bio/naturel
- **Négatifs ciblés** → Évite les défauts IA classiques sur les produits

---

📤 **Exporter vers Notion** · 📋 **Copier le prompt**

---

## Limitations

This skill does NOT:
- Execute image generation (output = text prompts only)
- Work with tools other than Nano (Midjourney, DALL-E, SD have different syntaxes)
- Edit existing images directly
- Generate prompts in languages other than English
- Maintain history between sessions (use Notion export for persistence)

---

## References

- [Nano Structure](references/nano-structure.md) — 6 components detailed rules
- [Use Cases](references/use-cases.md) — 8 case templates with examples
- [Auto-Suggestion Rules](references/auto-suggestion-rules.md) — Detection patterns
- [Evaluation Criteria](references/evaluation-criteria.md) — 8 criteria for quality indicator

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-26 | Initial release |

## Current: v1.0.0

## Owner

- **Author**: Édouard
- **Contact**: Via Claude.ai
