---
name: designor
description: >-
  Generate optimized prompts for Claude Design (Anthropic Labs) through expert
  elicitation. Produces XML-structured briefs ready to paste into Claude Design,
  with preparation checklist and token economy tips. Supports 6 deliverable types
  (UI prototypes, wireframes for Claude Code handoff, pitch decks, one-pagers,
  social assets, design explorations) across 3 modes (quick/standard/deep).
  Includes Phase 0 audit (deliverable type, visual inspiration, design system),
  modular reference library (style/density/brand/audience/anti-patterns anchors),
  and `revise` sub-command for directed critique iteration. Use when user says
  "designor", "prompt claude design", "brief design", "nouveau prototype claude",
  "wireframe handoff", "générer un deck claude", "direction visuelle",
  "variantes design". Not for executing the prompt itself, generating actual
  artifacts, animations/3D (delegate to Claude Code), or product ideation
  (use brainstormer first).
---

# Designor — Expert Prompt Elicitor for Claude Design

## Overview

Designor transforms vague design intentions into structured, token-optimized prompts ready to paste into Claude Design (Anthropic Labs, launched April 2026, powered by Opus 4.7). The skill stops at brief production—it does NOT execute the prompt. Output always contains 3 sections: the prompt itself, a preparation checklist, and token economy tips.

**Core philosophy**: Claude Design quality depends massively on the brief. Without visual inspiration, structured XML, and token-aware patterns, the output is generic regardless of effort. Designor encodes this discipline.

## Quick Decision Tree

```
┌─────────────────────────────────────────────────────────────┐
│              User triggers designor                         │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ Detect type (6) + mode (3) via keywords                     │
│ Ambiguity? → ONE disambiguation question (see Tool Notes)   │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ PHASE 0 — Pre-Elicitation Audit (BLOCKING)                  │
│ Q1: Deliverable type confirmed?                             │
│ Q2: Visual inspiration available (3+ refs)?  ← BLOCKING     │
│ Q3: Design system status (codebase/Figma/charte/none)?      │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│  QUICK        │   │  STANDARD     │   │  DEEP         │
│  3-5 Q        │   │  8-12 Q       │   │  15-20 Q + variants│
│  4-block brief│   │  XML prompt   │   │  XML + 2-3 alts│
└───────┬───────┘   └───────┬───────┘   └───────┬───────┘
        │                   │                   │
        ▼                   ▼                   ▼
┌─────────────────────────────────────────────────────────────┐
│ OUTPUT (always 3 sections)                                  │
│ 1. The prompt (Quick brief OR XML)                          │
│ 2. Preparation checklist (assets, config, DS)               │
│ 3. Token economy tips (Tweaks aggressive, Edit>Comment...)  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
                    Optional Notion export
                    Suggest `designor revise` for iteration
```

## Phase 0 — Pre-Elicitation Audit (BLOCKING)

3 filter questions before any detailed elicitation. **Q2 is a blocking gate.**

| Question | Goal | Blocking? |
|----------|------|-----------|
| Q1: Deliverable type? | Select template (ui/wireframe-handoff/deck/one-pager/social/explore) | Soft (default if ambiguous) |
| Q2: 3+ visual refs available? | Avoid generic AI output | **HARD BLOCK** — pause + suggest sources |
| Q3: Design system status? | Skip/include token questions, recommend DS toggle in Claude Design | Soft (impacts later questions) |

**Why Q2 blocks**: video research confirms 90% of poor Claude Design outputs come from missing visual inspiration. Without 3+ Pinterest/Dribbble/screenshots refs, the generated prompt cannot prevent generic results. If user has no refs, designor pauses and suggests collection (Pinterest themes, Dribbble keywords) before resuming.

→ See [phase-0-audit.md](references/phase-0-audit.md) for detection heuristics, keyword patterns, and edge cases.

## The 3 Modes

| Mode | Questions | Output | Use Case | Target Time |
|------|-----------|--------|----------|-------------|
| `quick` | 3-5 essential | 4-block brief | User knows what they want | 30 sec |
| `standard` (default) | 8-12 across 6 layers | XML prompt + checklist | Standard usage | 2-3 min |
| `deep` | 15-20 + "list styles" + "anticipate Tweaks" | XML + 2-3 alternative directions + iteration plan | Strategic project | 5-10 min |

**6 layers covered in standard/deep**: product intent, persona, visual direction (anchors + refs), information hierarchy, design tokens, technical constraints (responsive, accessibility, output format).

## The 6 Deliverable Templates

Each template has its own elicitation flow and prompt structure.

| Template | Focal | Specific Vocabulary |
|----------|-------|---------------------|
| `ui` | Components, design system, layout, interactions, states | CTA, grid, design tokens, Atomic Design, density |
| `wireframe-handoff` | Flow, info architecture, components front, dev constraints | User flow, low-fi, component IDs, Tailwind mapping, error states |
| `deck` | Narrative arc, tension, proof, density per slide | Problem/Solution/Proof, slide rupture, text/visual ratio |
| `one-pager` | Marketing sections, benefits, objections, brand voice | Hero, social proof, CTA, friction, zoning |
| `social` | Platform format, hook, rhythm, text/visual ratio | Carousel, safe zone, hook, scroll-stopper |
| `explore` | Named directions, variation axes, common constraints | Direction A/B/C, style anchors, orthogonal axes |

→ See [templates-by-deliverable.md](references/templates-by-deliverable.md) for full XML templates and elicitation question lists.

## Main Workflow

1. **Detect type + mode** via keywords. Fallback: ONE disambiguation question if ambiguous (see Tool Notes for environment-specific implementation).
2. **Phase 0 audit** — 3 filter questions (Q2 blocks if no inspiration).
3. **Template-specific elicitation** — variable depth per mode.
4. **Style anchors selection** — 1-2 per dimension, or infer from refs.
5. **Generate output** — 3 sections (prompt + checklist + token tips).
6. **Optional Notion export** — proposed, never imposed.
7. **Suggest `designor revise`** for iteration on result.

## Sub-command: `designor revise`

When the user receives a disappointing Claude Design result, they invoke `designor revise` with:
- The original prompt
- A free-form critique of the result (text + optional screenshots)

Output: a revision prompt following the **directed critique pattern**:
1. Explicitly preserve (what stays)
2. Name 2-4 precise defects
3. Set sharper target (visual or functional)
4. Request complete new version (not patch)

→ See [revise-pattern.md](references/revise-pattern.md) for full pattern, examples, and anti-patterns.

## Style Anchors Library (5 Dimensions)

Modular, combinable, versioned. User picks 1-2 per dimension or designor infers from refs.

| Dimension | Examples |
|-----------|----------|
| Style | Linear-like, Stripe-like, Apple HIG, Material 3, Notion-like, Aquacro, Néo-brutaliste |
| Density | Dense ops dashboard, Generous editorial, Balanced SaaS, Compact mobile-first |
| Brand | Premium B2B, Founder-led startup, Growth-marketing, Corporate, Indie maker |
| Audience | Tech senior, Ops manager, C-level decider, End-user grand public, Investor |
| Anti-patterns | Per deliverable type — generic UI, bullet-heavy slides, etc. |

Tagged `stable` / `emerging` / `experimental`. Mode `deep` offers freshness check via perplexitor.

→ See [style-anchors.md](references/style-anchors.md) for full library + changelog.

## Token Economy (Always Injected)

Designor systematically includes in the output:

- **Aggressive Tweaks instruction** (exact text): `"Augmente le nombre de Tweaks de façon agressive. Je veux pouvoir jouer avec le design un maximum."` — applied AFTER first generation in Claude Design.
- **Edit modes order**: Edit (0 tokens) > Tweaks (0 tokens) > Comment (moderate) > Chat (high).
- **Animations / 3D / video**: delegate to Claude Code, never ask Claude Design (except `wireframe-handoff` which prepares hooks).
- **Design system toggle**: recommend disabled for first project (saves 20-25% quota).

→ See [token-economy.md](references/token-economy.md) for full guidelines and rationale.

## Critical Rules

1. **Phase 0 Q2 BLOCKS** — no visual inspiration → pause, never bypass without `--no-inspiration` flag + warning.
2. **Output always 3 sections** — prompt + checklist + token tips. No exceptions.
3. **Aggressive Tweaks injection mandatory** — exact text included in section 3.
4. **No animations in prompt** — except `wireframe-handoff` template (hooks for Claude Code).
5. **Match user language** — output in user's input language (FR/EN). Templates exist in both.
6. **≤1 disambiguation question** — if disambiguation needed, single question max (implementation per environment, see Tool Notes).
7. **Suggest brainstormer** if product intent unclear — don't proceed with vague intent.
8. **Suggest critiquor** at end — propose review of generated prompt before user pastes it.
9. **Skill stops at brief** — never attempts to execute the prompt or generate the artifact.
10. **Revise is sub-command** — invoked explicitly, not auto-detected from conversation history.

## Flags

| Flag | Effect |
|------|--------|
| `--quick` | Force quick mode |
| `--deep` | Force deep mode |
| `--template [name]` | Force specific template (ui/wireframe-handoff/deck/one-pager/social/explore) |
| `--no-inspiration` | Skip Q2 phase 0 with explicit warning |
| `--notion` | Auto-export brief as Notion page at end |
| `--freshness-check` | Run perplexitor on style anchors before generation |

## Integrations

- ← `brainstormer` — upstream if product intent is unclear
- → `critiquor` — suggested at end for prompt review
- → `perplexitor` — for freshness check on style anchors (mode deep)
- → `notion-task-enricher` — pattern compatible for Notion export structure

## Quick Example

```
User: "designor un deck investisseur pour mon SaaS PMS"

Designor:
[Detects: template=deck, mode=standard, lang=FR]
[Phase 0]
- Q1: Deck investisseur confirmé.
- Q2: Tu as 3+ refs visuelles (decks Notion, Linear, Pitch.com…) ?
  → User: "Pas encore"
  → Designor pauses, suggests Pinterest "investor deck SaaS minimalist" + Dribbble "pitch deck B2B"
  → User: "OK j'ai 4 captures"
- Q3: Design system existant ?
  → User: "Charte interne, palette + logo"

[Standard elicitation — 8 questions]
- Audience investisseurs (early-stage / late-stage) ?
- Angle narratif (problème opérationnel / opportunité marché) ?
- Tension principale à mettre en scène ?
- Structure souhaitée (10-12-15 slides) ?
- Slides produit avec mockups ?
- Style anchors : Linear-like, Notion-like, Pitch.com-like ?
- Densité : 1 idée/slide ou 2-3 ?
- Export attendu : PPTX direct ou Canva pour ajustements ?

[Output 3 sections]
1. Prompt XML structuré (15 slides, arc P/S/Preuve/Roadmap/Ask)
2. Checklist : 4 refs Pinterest, palette charte, logos clients, KPI à plat
3. Tips : Tweaks agressifs après génération, design system DÉSACTIVÉ pour premier projet, export PPTX testé après validation

→ Suggère: critiquor pour relecture du prompt avant utilisation, Notion export.
```

## Knowledge Base

- [Phase 0 Audit](references/phase-0-audit.md) — Detection heuristics and edge cases
- [Templates by Deliverable](references/templates-by-deliverable.md) — Full XML templates × 6 + quick brief format
- [Style Anchors Library](references/style-anchors.md) — 5 dimensions, versioned, tagged
- [Revise Pattern](references/revise-pattern.md) — Directed critique for iteration
- [Token Economy](references/token-economy.md) — Tweaks, modes order, DS toggle

## Limitations

This skill does NOT:

- Execute the prompt in Claude Design (stops at brief)
- Generate visual references (user collects them)
- Cover product ideation (redirects to brainstormer)
- Cover animations/3D (redirects to Claude Code)
- Guarantee perpetual relevance of style anchors (research preview = fast evolution, freshness check available in deep mode)
- Generate the actual design artifact

## Tool Notes (Environment-Specific Implementation)

The skill mentions "disambiguation questions" abstractly. Concrete implementation depends on environment:

- **Claude.ai web/desktop/mobile**: use the `ask_user_input_v0` tool to display tappable options. Single `single_select` question, 2-4 options, no fallback default.
- **Claude Code (CLI)**: fall back to a plain numbered list in chat output, ask user to reply with the number.
- **Other environments**: numbered list approach, or default to template `ui` + mode `standard` if no interactive input is possible.

The skill must NEVER ask 2+ disambiguation questions in sequence — if more than one ambiguity exists, prioritize the deliverable type question and infer the rest from defaults.

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-04-30 | Initial release — 3 modes × 6 templates, Phase 0 audit, modular anchors library, revise sub-command, Notion export, token economy patterns |
| 1.1.0 | 2026-04-30 | Critiquor pass — agnostification of `ask_user_input_v0` (Tool Notes section), obsolescence disclaimer in token-economy.md, pivot mid-elicitation procedure in phase-0-audit.md |
| 1.2.0 | 2026-04-30 | Style anchors validation pass (5 Perplexity searches) — Aquacro renamed → Liquid Glass (stable, Apple WWDC 2025), Editorial magazine promoted to stable, Retro-futuriste split into 3 distinct anchors (Synthwave UI / Cassette futurism / Y2K revival), Soft pastel maximalist renamed → Tactile maximalism, Néo-brutaliste enriched with 2.0/soft/functional variants |

## Current: v1.2.0

## Owner

- **Author**: Édouard
- **Contact**: Via Claude.ai
