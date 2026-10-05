---
name: style-guide
description: Reference guide for 42 interior design styles — use when you need style characteristics, keywords, color palettes (hex codes), materials, furniture types, or AI rendering keywords for any design style
---

# Interior Design Style Guide

Comprehensive reference for **42 design styles with regional/era sub-variations**, optimized for AI image generation. Each style includes hex color codes, specific materials (with wood species), signature furniture, and 15+ AI rendering keywords.

## Individual Style Skills

Each style is its own skill — invoke directly with `/style-<name>`:

### Modern & Contemporary
`/style-minimalist` · `/style-scandinavian` · `/style-mid-century-modern` · `/style-japandi` · `/style-contemporary` · `/style-bauhaus`

### Classic & Traditional
`/style-baroque` · `/style-colonial` · `/style-victorian` · `/style-neoclassical` · `/style-art-deco` · `/style-french-provincial` · `/style-regency` · `/style-georgian` · `/style-rococo` · `/style-tudor`

### Asian & Eastern
`/style-japanese` · `/style-chinese` · `/style-vietnamese` · `/style-indochine` · `/style-korean` · `/style-thai` · `/style-balinese` · `/style-moroccan` · `/style-indian` · `/style-persian`

### Regional & Vernacular
`/style-mediterranean-greek` · `/style-mediterranean-italian` · `/style-mediterranean-spanish` · `/style-tropical` · `/style-coastal` · `/style-rustic` · `/style-farmhouse` · `/style-desert-southwestern`

### Specialty & Avant-Garde
`/style-industrial` · `/style-brutalist` · `/style-biophilic` · `/style-maximalist` · `/style-retro-vintage` · `/style-futuristic` · `/style-bohemian` · `/style-wabi-kintsugi`

### Reference
`styles/reference.md` — AI Prompt Formula, Provider Notes (Midjourney/DALL-E/SD/Gemini), Style Compatibility Matrix, Material Glossary, Room Material Tables, Color Hex Reference

## Quick Style Lookup

### Modern & Contemporary
- **Minimalist** — Japanese (zen, ma, tatami) / Scandinavian (hygge, birch, lagom) / Warm (limewash, travertine, bouclé)
- **Scandinavian** — Danish/Swedish/Norwegian/Finnish. Light woods, white, functional warmth
- **Mid-Century Modern** — 1950s-60s organic forms, teak, walnut, Eames, Saarinen
- **Japandi** — Japanese wabi-sabi + Scandi hygge. Shou sugi ban, washi, live-edge oak
- **Contemporary (2024-25)** — Curved forms, bouclé, travertine, limewash, warm earth tones
- **Bauhaus** — Tubular steel, primary colors, geometric purity, Wassily/Barcelona chairs

### Classic & Traditional
- **Baroque** (1600-1750) — Gilded grandeur, trompe-l'œil, velvet, crystal chandeliers
- **Colonial** — American (pine, hearth) / British (rattan, mahogany) / Spanish (terracotta, stucco)
- **Victorian** — Early (Gothic Revival) / High (maximalist) / Late (Aesthetic/Eastlake)
- **Neoclassical** (1750-1850) — Greek/Roman symmetry, fluted columns, Wedgwood blue
- **Art Deco** (1920s-30s) — Geometric glamour, Macassar ebony, chrome, black+gold
- **French Provincial** — Rustic elegance, toile, lavender, carved walnut armoire
- **Regency** (1800-1830) — Sabre legs, brass inlay, rosewood, "Bridgerton" aesthetic
- **Georgian** (1714-1830) — Palladian symmetry, Chippendale, mahogany
- **Rococo** (1715-1775) — Pastel asymmetry, boiserie, shell motifs, gilded bergère
- **Tudor** (1485-1603) — Exposed oak beams, inglenook fireplace, linenfold paneling

### Asian & Eastern
- **Japanese (Wabi-Sabi)** — Tatami, shoji, tokonoma, hinoki cypress
- **Chinese Traditional** — Ming (huanghuali) / Qing (ornate lacquer, red+gold)
- **Vietnamese** — Tropical bamboo+rattan, French-colonial blend
- **Indochine** — French-Asian fusion, dark wood, rattan, silk
- **Korean (Hanok)** — Ondol floors, hanji paper, pine, celadon
- **Thai** — Teak, gilded carving, naga motifs, Thai silk
- **Balinese** — Open-air bale pavilions, paras stone, alang-alang thatch
- **Moroccan/Moorish** — Zellige tile, tadelakt, riad courtyard
- **Indian** — Mughal (marble, jali screens) / Rajasthani (mirror work, vibrant color)
- **Persian** — Persian carpets, muqarnas, turquoise+lapis, iwan courtyards

### Regional & Vernacular
- **Mediterranean** — Greek (white+blue) / Italian (terracotta, Murano) / Spanish (azulejo)
- **Tropical** — SE Asian / Caribbean / Hawaiian. Rattan, bamboo, open-air
- **Coastal/Hamptons** — Shiplap, navy+white, linen, sisal
- **Rustic** — American lodge / European / Mountain. Log, stone, cowhide
- **Farmhouse** — Traditional / Modern. Shiplap, apron sink, barn doors
- **Desert/Southwestern** — Adobe, vigas, saltillo, kiva fireplace, turquoise

### Specialty & Avant-Garde
- **Industrial** — NYC Loft / Warehouse / Soft Industrial. Brick, concrete, matte black
- **Brutalist** — Raw concrete, board-formed, geometric mass, Corten steel
- **Biophilic** — Living walls, natural light, organic forms, wellness
- **Maximalist** — Curated / Eclectic. Jewel tones, velvet, pattern mixing
- **Retro** — 50s (pastel) / 60s (space-age) / 70s (earth, shag) / 80s (neon, Memphis)
- **Futuristic** — Parametric, LED, smart glass, carbon fiber
- **Bohemian** — Traditional / Modern / Chic. Macramé, kilim, rattan
- **Wabi-Kintsugi** — Gold-repaired ceramics, weathered materials, imperfection beauty

## How to Use

1. **User asks about a style** → Invoke `/style-<name>` (e.g., `/style-japanese` for Japanese)
2. **Generating prompts** → Use **AI Keywords** from the style skill + `styles/reference.md` for prompt formula
3. **Color specifics** → Each style skill has 8+ hex codes in color tables
4. **Material specifics** → Each style skill lists 10+ materials with species/types
5. **Fusion request** → Invoke both style skills + check Compatibility Matrix in `styles/reference.md`
6. **Provider optimization** → See Provider-Specific Notes in `styles/reference.md`

## Connected Skills

| Skill | Uses Style Guide For |
|-------|---------------------|
| `/design-consult` | Style recommendation, narrowing options |
| `/generate-prompt` | AI Keywords, materials, hex colors — source of truth |
| `/mood-board` | Textures, furniture, atmospheric descriptions |
| `/edit-design` | Target style vocabulary when shifting styles |
| `/refine` | Diagnosing missing/incorrect keywords |
| `/compare-models` | Consistent prompts via Keyword Matrix |

## Gotchas

- **Sub-styles matter**: "Mediterranean" → specify Greek/Italian/Spanish. "Victorian" → Early/High/Late.
- **Keywords are provider-sensitive**: See Provider-Specific Notes in `reference.md`.
- **Cultural sensitivity**: Asian styles have sacred elements — check Cultural Notes before rendering.
- **Styles blend**: "Modern but warm" = Japandi or Warm Minimalism, not strict Modern.
- **Hex codes are starting points**: Let design brief take priority over canonical colors.
