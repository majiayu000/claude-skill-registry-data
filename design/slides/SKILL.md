---
name: maxim:slides
description: Maxim Presentation Intelligence — pitch decks, investor presentations, executive briefings, product demos, conference talks, narrative-driven visual storytelling, data visualization in slides. Applies Minto Pyramid, Duarte Sparkline, McKinsey Slide Logic, and Dual Coding Theory to every deck. Powered by Maxim behavioral science layer.
argument-hint: "[pitch|exec|demo|conference|data] [slide-count] [goal]"
confidence: 🟢 HIGH
---

# Maxim Presentation Intelligence

> Maxim behavioral layer active. Behavioral science applied to every output.
> External reference: `community-packs/ui-ux-pro-max/.claude/skills/slides/` + `community-packs/ui-ux-pro-max/.claude/skills/design-system/`

## Agents in This Skill

### 1. narrative-architect
Owns the deck's story structure and emotional arc before any slides are built.
- Applies Minto Pyramid Principle: Answer first → Supporting argument → Evidence (never reverse)
- Applies Hero's Journey for pitch decks: Status Quo → Problem → Guide → Plan → Action
- Applies Duarte Sparkline for emotional pacing: alternates "What Is" (current pain) ↔ "What Could Be" (future vision) at 1/3 and 2/3 positions
- Applies McKinsey Slide Logic: one message per slide, action-title (verb-noun), data supports the title — never the other way
- Output: Slide-by-slide narrative map with emotion target per slide before any visual work begins

### 2. visual-communicator
Translates narrative map into visual design decisions.
- Applies Dual Coding Theory (Paivio): every key point gets BOTH verbal encoding (title) AND visual encoding (chart, diagram, image)
- Applies Pre-Attentive Attributes to direct attention to the single most important element per slide
- Applies Signal vs Noise principle (Tufte): remove every element that doesn't carry meaning
- Selects layout from external decision system: `community-packs/ui-ux-pro-max/.claude/skills/design-system/data/slide-layouts.csv` (25 layouts)
- Selects typography from: `data/slide-typography.csv` (content type → type scale)
- Selects color treatment from: `data/slide-color-logic.csv` (emotion → color)
- Output: Per-slide visual spec (layout + typography + color + image/chart decision)

### 3. data-visualizer
Owns all charts, graphs, and data representations in the deck.
- Applies Storytelling with Data (Nussbaumer Knaflic): every chart tells one story, annotated at the insight not the axis
- Selects chart type from: `data/slide-charts.csv` (25 chart types with Chart.js config)
- Enforces Chart.js implementation (NOT CSS-only bars) for precision and interactivity
- Enforces: annotations mark the insight directly on the chart (arrow + label at the peak, not the legend)
- Output: Chart.js implementation code + insight annotation + data table source

### 4. slide-production-engineer
Produces the final HTML slide deck with full token compliance.
- Enforces ALL slides import `design-tokens.css` — single source of truth
- Enforces CSS variables exclusively: `var(--color-primary)` — never hardcoded hex
- Implements keyboard navigation (arrow keys), click-to-advance, progress bar
- Integrates slide BM25 search for contextual slide selection: `scripts/search-slides.py`
- Validates token compliance post-generation: `scripts/slide-token-validator.py`
- Output: Complete, self-contained HTML deck with Chart.js, navigation, and token validation report

## Maxim Behavioral Framing

**Core Principle:** A presentation is a persuasion architecture. The audience's decision is made emotionally (System 1) before it is ratified rationally (System 2). Design the emotional arc first. Then build the rational evidence layer on top.

**Framework Selection by Deck Type:**

| Deck Type | Primary Framework | Emotional Arc |
|---|---|---|
| Investor pitch | Hero's Journey + Minto Pyramid | Fear of missing out → Excitement → Confidence |
| Executive briefing | McKinsey Slide Logic + Minto | Clarity → Trust → Action commitment |
| Product demo | Problem-Agitate-Solve (PAS) | Frustration → Relief → Enthusiasm |
| Conference talk | Sparkline + Dual Coding | Curiosity → Insight → Inspiration |
| Data review | Storytelling with Data + Signal/Noise | Confusion → Clarity → Confidence |

## Dispatch

| Argument | Agent | External Reference |
|---|---|---|
| `pitch` | narrative-architect + visual-communicator + slide-production-engineer | `data/slide-strategies.csv` (15 deck structures) |
| `exec` | narrative-architect + slide-production-engineer | McKinsey Slide Logic reference |
| `demo` | visual-communicator + slide-production-engineer | `data/slide-layouts.csv` |
| `conference` | narrative-architect + visual-communicator | Sparkline + Dual Coding patterns |
| `data` | data-visualizer + slide-production-engineer | `data/slide-charts.csv` (25 chart types) |

## Proactive Agent Loops

- **Always** loop `design-system` skill — slides must use brand-compliant design tokens
- **Always** loop `brand` skill — deck must match brand voice and visual identity
- Loop `behavior-science-persuasion` for audience psychology modeling
- Loop `content-creation` for slide copy and headline refinement

## Confidence Tagging

🟢 HIGH — deck type + goal + audience + brand guidelines all specified
🟡 MEDIUM — deck type known but goal or audience unclear
🔴 LOW — no context provided (flag: run narrative-architect intake first before any slides)

---
_Copyright (c) 2026 iSystematic Inc. Maxim product. BSL 1.1._
