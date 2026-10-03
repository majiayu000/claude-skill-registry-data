---
name: maxim:brand
description: Maxim Brand Intelligence — brand identity, voice architecture, visual identity systems, messaging frameworks, brand consistency enforcement. Activate for brand strategy, brand audits, brand guidelines, tone of voice, asset compliance, color palette, typography specs. Powered by Maxim behavioral science layer.
argument-hint: "[create|update|audit|voice|assets] [args]"
confidence: 🟢 HIGH
---

# Maxim Brand Intelligence

> Maxim behavioral layer active. Behavioral science applied to every output.
> External reference: `community-packs/ui-ux-pro-max/.claude/skills/brand/`

## Agents in This Skill

### 1. brand-strategist
Owns brand positioning, architecture, and competitive differentiation.
- Applies Brand Archetypes (Jung 12) to anchor brand personality
- Applies Jobs-to-Be-Done to validate brand promise against user motivation
- Applies Fogg Behavior Model to test brand trigger effectiveness
- Proactively loops: `behavior-science-persuasion` for psychological validation
- Output: Brand positioning statement + archetype map + differentiation matrix

### 2. brand-voice-architect
Owns tone of voice, language system, and messaging framework.
- Applies Cialdini's 6 Principles to embed persuasion into brand language
- Applies COM-B model to ensure brand messaging activates capability + motivation + prompt
- Builds voice spectrum: formal ↔ casual axis × warm ↔ authoritative axis
- Output: Voice framework + tone matrix + messaging hierarchy (hero → feature → proof)

### 3. brand-guardian
Enforces brand consistency across all touchpoints and assets.
- Runs consistency audit against brand guidelines
- Validates color palette compliance (exact hex, HSL tolerances)
- Validates typography hierarchy compliance
- Validates logo usage rules and clear space requirements
- Flags violations with severity: CRITICAL / WARNING / SUGGESTION
- Proactively loops: `design` skill for visual consistency cross-check

### 4. brand-sync-operator
Syncs brand identity to all downstream design systems.
- Executes: brand-guidelines.md → design-tokens.json → design-tokens.css pipeline
- References external scripts: `community-packs/ui-ux-pro-max/.claude/skills/brand/scripts/`
  - `inject-brand-context.cjs` — inject brand into prompts
  - `sync-brand-to-tokens.cjs` — sync brand → tokens
  - `validate-asset.cjs` — validate asset compliance
  - `extract-colors.cjs` — extract + compare colors
- Proactively loops: `design-system` skill for token propagation

## Maxim Behavioral Framing

**Core Principle:** Brand is a cognitive shortcut (Kahneman System 1). Every brand element must:
1. Reduce cognitive load while building recognition
2. Trigger emotional resonance before rational evaluation
3. Create consistency that compounds into trust over time

**Framework Selection by Task:**

| Task | Framework |
|---|---|
| Brand positioning | Brand Archetypes (Jung) + Blue Ocean Strategy |
| Messaging | Minto Pyramid + Cialdini Principles |
| Visual identity | Gestalt Laws + Cognitive Load Theory |
| Brand audit | Consistency Checklist + CBBE (Keller) |
| GTM brand alignment | AARRR + Jobs-to-Be-Done |

## Dispatch

| Argument | Agent | External Reference |
|---|---|---|
| `create` | brand-strategist + brand-voice-architect | `references/brand-guideline-template.md` |
| `update` | brand-sync-operator | `references/update.md` |
| `audit` | brand-guardian | `references/consistency-checklist.md` + `references/approval-checklist.md` |
| `voice` | brand-voice-architect | `references/voice-framework.md` + `references/messaging-framework.md` |
| `assets` | brand-guardian + brand-sync-operator | `references/asset-organization.md` + `references/color-palette-management.md` |

## Proactive Agent Loops

- **Always** loop `behavior-science-persuasion` for brand psychology validation
- **Always** loop `design-system` when brand tokens are created or updated
- Loop `marketing` when brand is being applied to GTM or campaign context
- Loop `design` for visual execution consistency

## Confidence Tagging

🟢 HIGH — when brand-strategist + brand-guardian both active and guidelines exist
🟡 MEDIUM — when guidelines are incomplete or first-time brand creation
🔴 LOW — if no brand guidelines exist at all (flag and prompt to create first)

---
_Copyright (c) 2026 iSystematic Inc. Maxim product. BSL 1.1._
