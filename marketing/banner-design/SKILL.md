---
name: maxim:banner-design
description: Maxim Banner Design Intelligence — digital banner creation, ad creative, social media banners, hero sections, display advertising, promotional graphics. Activates pre-attentive attribute theory and pattern interruption science for every banner. Powered by Maxim behavioral science layer.
argument-hint: "[social|display|hero|email|print] [dimensions] [goal]"
confidence: 🟢 HIGH
---

# Maxim Banner Design Intelligence

> Maxim behavioral layer active. Behavioral science applied to every output.
> External reference: `community-packs/ui-ux-pro-max/.claude/skills/banner-design/`

## Agents in This Skill

### 1. attention-architect
Engineers the first 300ms of banner perception.
- Applies Pre-Attentive Attributes (Ware): color, motion, orientation, size — in that priority order
- Applies Banner Blindness Theory (Benway 1998) — deliberately breaks expected banner patterns
- Applies F-Pattern and Z-Pattern eye tracking to anchor CTA in natural gaze path
- Sizes, positions, and contrasts every visual element for maximum fixation probability
- Output: Visual hierarchy spec + attention flow diagram + pattern interruption plan

### 2. conversion-copywriter
Owns all text within the banner.
- Applies AIDA (Attention → Interest → Desire → Action) to banner narrative arc
- Applies Hick's Law — single CTA per banner, no choice paralysis
- Applies Power Words library (urgency, exclusivity, social proof, curiosity)
- Character limits enforced: Headline ≤7 words, subhead ≤12 words, CTA ≤3 words
- Proactively loops: `behavior-science-persuasion` for psychological trigger validation

### 3. brand-compliance-enforcer
Ensures every banner matches brand identity.
- Validates against `community-packs/ui-ux-pro-max/.claude/skills/brand/` brand guidelines
- Validates color palette (no off-brand hex), typography (approved fonts only), logo clear space
- Loops: `brand` skill for consistency cross-check
- Flags violations before output: CRITICAL (blocks) / WARNING (flags) / SUGGESTION (notes)

### 4. format-optimizer
Adapts banner specifications to platform and format requirements.
- Social: 1200×628 (OG), 1080×1080 (square), 1080×1920 (story), 1200×627 (LinkedIn)
- Display: 728×90 (leaderboard), 300×250 (medium rectangle), 160×600 (wide skyscraper), 320×50 (mobile)
- Hero: 1440×600 (desktop), 768×400 (tablet), 375×300 (mobile)
- Email: 600×200 (header), 600×400 (feature)
- Outputs format-specific asset spec with safe zones, bleed, and text boundary guidelines

## Maxim Behavioral Framing

**Core Principle:** Banner blindness is the default state. Every banner must earn attention by violating the expected visual pattern of its context, then immediately deliver value within the next 1.5 seconds of engagement.

**Framework Selection by Task:**

| Task | Framework |
|---|---|
| Attention design | Pre-Attentive Attributes (Ware) + Gestalt Laws |
| CTA copy | AIDA + Hick's Law + Cialdini Scarcity/Social Proof |
| Brand compliance | CBBE (Keller) + Visual Consistency Audit |
| Campaign alignment | AARRR (which stage is this banner serving?) |
| Performance prediction | ELM (Elaboration Likelihood Model) — peripheral vs central route |

## Dispatch

| Argument | Agent | Focus |
|---|---|---|
| `social` | attention-architect + conversion-copywriter + brand-compliance-enforcer | Social platform specs |
| `display` | attention-architect + format-optimizer | Ad network specs |
| `hero` | attention-architect + conversion-copywriter | Web hero sections |
| `email` | conversion-copywriter + brand-compliance-enforcer | Email header banners |
| `audit` | brand-compliance-enforcer | Compliance-only review |

## Proactive Agent Loops

- **Always** loop `brand` skill for identity compliance
- Loop `marketing` skill to confirm campaign stage alignment (awareness / consideration / conversion)
- Loop `behavior-science-persuasion` for CTA psychology validation
- Loop `design` for visual hierarchy and Gestalt review

## Confidence Tagging

🟢 HIGH — brand guidelines exist, platform + goal are specified, Maxim behavioral layer fully applied
🟡 MEDIUM — brand guidelines missing or platform unspecified
🔴 LOW — no brand context, no goal defined (flag and request both before proceeding)

---
_Copyright (c) 2026 iSystematic Inc. Maxim product. BSL 1.1._
