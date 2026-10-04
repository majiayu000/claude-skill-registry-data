---
name: content-creator
description: "Complete content creation framework — 14 copywriting formulas, 18 psychology effects, 10 NLP techniques, 7 pricing strategies, 6 voice tones, and a 4-step Brief→Brainstorm→Angle→Writing process. Trigger when the user wants to draft ads, social posts, captions, scripts, hooks, landing-page copy, or any conversion-focused content. Niche-agnostic: caller supplies brand/topic, demographic, and target platforms at invocation. Optional language packs (en, vi) and niche presets (cosmetics-beauty, saas, banking-finance, crypto) load on demand."
---

# Content Creator Skill

A composable content-creation framework. The user supplies the inputs; this skill chooses the right formulas, psychology, NLP, pricing levers, voice tone, and platform format — then drafts.

## When to Use

- Writing ads, social posts, captions, hooks, scripts, landing pages, emails, or product copy
- Need a structured framework instead of freestyle copy
- Want a deliberate angle (named formula + psychology effect) rather than vibes
- Targeting a specific niche where compliance / trust accelerators matter

## Inputs

Required (ask via AskUserQuestion if missing):

- **slug** — brand, product, topic, or campaign the content is about
- **demographic** — target audience (age, gender, geography, income, interests, language)
- **platforms** — one or more channels: tiktok, instagram, facebook, linkedin, youtube-shorts, x, threads, farcaster, email, blog

Optional:

- **language** — `en` or `vi` (others work, just no language pack). If omitted, infer from brief; if ambiguous, ask.
- **preset** — niche overlay: `cosmetics-beauty`, `saas`, `banking-finance`, `crypto`. If omitted, framework-only.
- **goal** — sales, leads, signups, demos, awareness, engagement, shares
- **tone** — override the preset/voice-tone default
- **length** — short-form / long-form / specific char or word count
- **must-include** / **must-avoid** — keywords, claims, topics

## The 4-Step Process

1. **Brief** — confirm inputs. If anything required is missing, ask.
2. **Brainstorm** — pick 3–5 formula+psychology pairs that fit goal × platform × niche. Pull from `references/formulas.md`, `references/psychology.md`, `references/nlp.md`. Apply preset's "high-performing angles" if loaded.
3. **Angle Selection** — present 2–3 angles to the user, each labeled with the formula(s) and effect(s) used and a one-line hook preview. User picks one.
4. **Writing** — draft full copy in the chosen language pack's vocabulary, the chosen voice tone, and the platform's format constraints. Apply NLP techniques sparingly. End with a single CTA. If preset has compliance reminders, surface them with the draft.

## On-Demand File Loading

`SKILL.md` is the only file loaded automatically. Read others only when their trigger fires:

| Trigger | Read |
|---|---|
| Any platform named in `platforms` | `references/platforms.md` (the matching section) |
| `language=en` | `languages/en.md` |
| `language=vi` | `languages/vi.md` |
| `language=vi` AND platform is Zalo OA, LinkedIn VN, YouTube VN, or Twitter/X VN | also load `skills/vietnamese-language/references/platforms/[platform].md` |
| `language=vi` AND task needs formal docs, press release, or regulatory language | also load matching file from `skills/vietnamese-language/references/` |
| `language=` other | no pack — write in that language using framework structure, note absence to user |
| `preset=cosmetics-beauty` | `presets/cosmetics-beauty.md` |
| `preset=saas` | `presets/saas.md` |
| `preset=banking-finance` | `presets/banking-finance.md` |
| `preset=crypto` | `presets/crypto.md` |
| `preset=` other | check `presets/{value}.md`; if missing, fall back to framework-only and tell user |
| Brainstorm needs depth | `references/formulas.md`, `psychology.md`, `nlp.md`, `pricing.md`, `voice-tones.md` |

**Layering order** (when both language pack and preset are loaded): framework defaults → language pack overrides phrasing → preset overrides niche angles + trust accelerators + compliance. Preset wins on niche guidance; language pack wins on register/vocabulary.

## Quick Selection Matrix

Pick formulas by job-to-be-done. Combine one formula + one psychology effect minimum.

| Use case | Formula(s) | Psychology effect(s) |
|---|---|---|
| Cold short-form ad (TikTok/Reels) | SSS + Hook-Value-CTA | Pattern Interrupt + Curiosity Gap |
| Retargeting ad | PAS | Loss Aversion + Scarcity |
| Product page / DTC PDP | FAB + 4Cs | Specificity Bias + Social Proof |
| Long-form sales page | AIDA + PPPP | Future Pacing + Risk Reversal |
| High-trust B2B post | ACC + PPPP | Authority + Specificity Bias |
| Transformation story | BAB + Storytelling | Narrative Transport + Identity Labeling |
| Launch / announcement | Hook-Value-CTA | Curiosity Gap + FOMO |
| Comparison / switch story | BAB | Contrast + Loss Aversion |
| Pricing/upgrade nudge | Funnel (BOFU) | Anchoring + Decoy + Reciprocity |
| Repurpose pillar to micro | COC | Cognitive Ease |
| Quick checkout closer | SLAP | Scarcity + FOMO |
| Listing / catalog text | 5W1H + 4Cs | Specificity Bias |

## Registries

**Languages available:** `en`, `vi`. Add new ones by dropping `languages/{code}.md` and listing here.

**Presets available:**

| Preset | Covers |
|---|---|
| `cosmetics-beauty` | Skincare, makeup, fragrance, haircare, body care |
| `saas` | B2B/B2C SaaS, PLG and sales-led, vertical and horizontal tools |
| `banking-finance` | Retail banking, neobanks, lending, insurance, wealth, payments |
| `crypto` | CEX/DEX, L1/L2, DeFi, NFTs, wallets, infra, DAOs |

Add new presets by dropping `presets/{name}.md` (follow the cosmetics-beauty structure) and listing here.

## Output Rules

- One CTA per piece. Never two.
- Specific beats vague: numbers, names, timeframes.
- "You" outweighs "we" at least 3:1.
- Match the language pack's register (formal/casual/bestie). Do not mix.
- Honor platform character/format limits from `references/platforms.md`.
- If preset has compliance reminders, surface them after the draft.
- Default output language = brief language. Honor explicit `language=` override.
- For UI/marketing humanization, the user's `/humanizer` rule still applies post-draft.

## Reference Index

- `references/formulas.md` — 14 copywriting formulas
- `references/psychology.md` — 18 psychology effects
- `references/nlp.md` — 10 NLP techniques
- `references/pricing.md` — 7 pricing strategies
- `references/voice-tones.md` — 6 voice tones
- `references/platforms.md` — per-platform constraints
- `languages/` — language packs (en, vi)
- `presets/` — niche overlays (cosmetics-beauty, saas, banking-finance, crypto)
