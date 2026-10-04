---
name: deck-design-ppt
description: >
  Create new presentation decks as native editable PPTX files with
  consulting-quality design. Use when the user wants to build a new
  slide deck, presentation, or pitch deck from a brief or topic.
  For editing existing .pptx files, use the pptx skill instead.
---

# Deck Design: Operational Playbook

## What This Skill Does

- **Input:** a deck brief + any structured data the user has (tables, time series, bridges, evaluation criteria, etc.).
- **Output:** a native **editable `.pptx`** file with slide masters, theme colors, and all content as PowerPoint-native objects (text boxes, shapes, charts). Every element is individually editable in PowerPoint.

### The brief

The **brief** is everything the user provides about what they want. Before generating anything, extract these signals:

| Signal | Examples | Defaults if absent |
|---|---|---|
| **Objective** | "pitch to Series A investors", "board strategy update", "SBIR Phase II proposal deck" | General presentation |
| **Audience** | "DoD program managers", "VC partners", "internal team" | General professional |
| **Brand identity** | Logo colors, company name, client palette | Palette defaults |
| **Tone / firm style** | "McKinsey-style", "clean and modern", "urgent/high-stakes" | Infer from audience + objective |
| **Density** | "dense and evidence-heavy", "keep it simple", specific L1/L2/L3 | Infer from audience + objective |
| **Data** | Tables, metrics, timelines, comparisons, evaluations | None. Build from research or request more |

Not every brief contains all signals. Extract what's there, infer what you can, and use defaults for the rest. Do not ask the user to fill out a checklist. If the user provides a custom palette, brand guide, or design spec, follow it. The built-in styles are defaults, not constraints.

### Storyboard intake (from consultant skill)

When the input is a storyboard artifact (from the consultant skill), the brief extraction is already done. Map directly:

| Storyboard field | deck-design-ppt step |
|---|---|
| Firm overlay | Style (Phase 1, step 2) |
| Density level | Density (Phase 1, step 3) |
| Per-slide content description | Data-shape extraction (Phase 1, step 5) + pattern routing (step 6) |
| Structured data | Build script data objects (Phase 2, step 8) |

Skip Phase 1 step 1 (the brief extraction is already done). Steps 5–6 still run here: the storyboard deliberately describes WHAT each slide must prove (the comparison, decomposition, or evaluation), never chart types or data shapes. Deriving the shape from the content description and routing it to a pattern is this skill's job.

### Identity intake (from brand-system skill)

If an `identity.js` produced by the brand-system skill exists in the working directory, the visual identity decisions are already made. Skip [Style Routing](#style-routing). Register the identity as a theme in the build script instead:

```javascript
const { createDeck } = require('<this-skill>/masters');
const { THEMES } = require('<this-skill>/masters/theme');
const brand = require('./identity');

const hex = c => c.replace('#', '');   // themes use bare hex, identity.js uses #-prefixed
THEMES[brand.palette.name] = {
  name:      brand.firm?.name || brand.palette.name,
  accent:    hex(brand.palette.accent),
  canvas:    hex(brand.palette.surface),
  mist:      hex(brand.palette.surfaceMuted),
  midnight:  hex(brand.palette.surfaceDark),
  text:      hex(brand.palette.text),
  textSec:   hex(brand.palette.textMuted),
  textFine:  hex(brand.palette.textFine),
  border:    hex(brand.palette.accentLight),
  positive:  hex(brand.palette.positive),
  caution:   hex(brand.palette.warning),
  negative:  hex(brand.palette.negative),
  font:        brand.fonts.body.family,
  fontDisplay: brand.fonts.heading.family,
  headerBar: brand.style === 'institutional' || brand.style === 'data-forward',
  darkMode:  brand.style === 'dark',
};

createDeck(brand.palette.name, slides, 'deck.pptx');
```

Two caveats:

- **Fonts**: PPTX embeds no fonts. The theme font renders only if installed on the viewer's machine. For unusual identity fonts, fall back to the stack's system font rather than risking substitution.
- **Style direction**: `brand.style` shapes composition, not just chrome. `institutional` / `data-forward` lean on C-series density, `modern` / `bento` on card-heavy P-series, `dark` on full-bleed `sequoia`-like treatment, `editorial` on typography-led patterns over charts.

### Pattern library (21 communication patterns)

| Tier | Namespace | What it answers | Use when |
|---|---|---|---|
| Tier 1 | **P-series** (`p01` … `p15`) | "What communication move is this slide making?" | All decks |
| Tier 2 | **C-series** (`c01` … `c06`) | "What dense consulting composition does this slide require?" | MBB-style engagement deliverables |

All patterns work across all 5 styles. The palette controls the visual identity, not the pattern.

**Patterns are reference implementations, not constraints.** Use them when they fit the content. When a slide needs a layout that no pattern covers, build custom using `pptxgenjs` directly. The grid constants, theme tokens, and slide master chrome still apply. The pattern library is a starting vocabulary, not a ceiling.

## How To Generate A Deck (Algorithm)

### Phase 1: Understand

1. **Analyze the brief.** Extract signals from [The brief](#the-brief). Research what the brief references: web search for market data, benchmarks, competitors. User-provided data is the primary source.
2. **Pick style:** `consulting-mckinsey` / `consulting-bcg` / `consulting-bain` / `founder` / `sequoia`. See [Style Routing](#style-routing).
3. **Pick density level.** See [Density Profiles](#density-profiles).
4. **Load firm reference** (consulting decks only). See [Firm Style](#firm-style-consulting-decks).
5. **Extract data shapes** (table, timeline, bridge, grid ratings, etc.).
6. **Route each slide** to a pattern using the [Routing Table](#routing-table), or build custom if no pattern fits.

### Phase 1.5: Outline

Before writing any code, produce a **deck outline** in markdown. This prevents sparse slides, content overlap, and mid-build surprises.

The outline must include:
1. **Governing thought**: one sentence that states the deck's answer.
2. **Slide list**: for each slide, an action title, pattern, content summary, and data shape.
3. **Flow test**: read all action titles in sequence. Do they tell a complete story without the slide bodies? If not, fix the narrative before proceeding.
4. **Density check**: for each slide, confirm the content fills the body zone without overflowing. Patterns use dynamic vertical centering. Content that is too sparse will float, and content that exceeds slot budgets will crowd.
5. **Data sufficiency**: for each slide, confirm you have the data its pattern needs (chart series, metric values, table rows). If not, research to fill gaps before building.

Save the outline as `{slug}-outline.md` alongside the build script. It serves as both a planning artifact and documentation for future edits.

### Phase 2: Build

7. **Read the slot budget** for each pattern just-in-time: `masters/patterns/<pattern>.slots.md`.
8. **Write the build script.** Assemble the slide list with structured data for each pattern:

```javascript
const { createDeck } = require('<this-skill>/masters');

createDeck('consulting-mckinsey', [
  { pattern: 'p01-cover', data: { title: '...', subtitle: '...' } },
  { pattern: 'p10-agenda', data: { items: [...] } },
  { pattern: 'p04-scorecard', data: { title: '...', cards: [...] } },
  { pattern: 'p03-evidence', data: { chart: {...}, callouts: [...] } },
  { pattern: 'c05-divider', data: { sectionNum: '02', title: '...' } },
  { pattern: 'p08-closer', data: { title: '...', nextSteps: [...] } },
], 'strategy-update.pptx');
```

`<this-skill>` = this skill's base directory path (provided in context when the skill loads). Node resolves `pptxgenjs` and `sharp` from the skill's own `node_modules/`. No install needed in the user's project.

9. **Run it:** `node build-deck.js` produces the `.pptx` directly. No HTML, no browser, no rendering step.

### Phase 3: QA

10. Generate thumbnail grid for visual review and fix any issues:

Use the **pptx** skill's thumbnail script to generate a preview grid of the deck.

## Output Organization

Save deliverables to the current working directory (or a user-specified output folder). Use kebab-case naming derived from the deck title:

- `{slug}.pptx`: the deliverable
- `build-{slug}.js`: the build script (reproducible)
- `{slug}-outline.md`: the deck outline (content plan)

**Intermediate artifacts** (QA thumbnails, temp rasterizations) go to the system temp directory. Do not leave them in the workspace.

## Architecture

Self-contained: `package.json` + `node_modules/` are inside the skill folder. All `require()` calls resolve locally. No workspace-level install needed. Run `npm install` inside this skill folder if `node_modules/` is missing.

The build kit lives in `masters/`:

| File | Purpose |
|---|---|
| `masters/index.js` | Orchestrator: `createDeck(palette, slides, output)` |
| `masters/grid.js` | Spatial constants (margins, body zone, footer Y). One grid, all patterns use it. |
| `masters/theme.js` | Palette name → theme object (colors, fonts, flags) |
| `masters/layouts.js` | Defines slide masters (COVER, CONTENT, DIVIDER, CLOSER) parameterized by theme |
| `masters/patterns/*.js` | 21 pattern functions. Each fills content into the body zone. |
| `masters/patterns/*.slots.md` | Character budgets per pattern (loaded just-in-time) |
| `masters/examples/*.js` | 8 advanced visual reference scripts (dumbbell, gauge, process flow, composite, scenario, multi-panel, data table, gantt) |

**Slide masters** are parameterized by the theme: one set of master definitions works for all 5 styles. The theme controls:
- Header bar (yes/no + color)
- Footer rule, logo, page number colors
- Canvas background
- Accent color for titles, highlights

**Pattern functions** receive a slide (already has master chrome), the pptx instance, content data, and the theme. They only place content in the body zone and never touch the header, footer, or margins.

**Grid constants** (`grid.js`) define the spatial contract:
- `bodyY` / `bodyEndY`: body zone boundaries
- `marginL` / `contentW`: horizontal margins
- `footerRuleY` / `footerTextY`: footer positions
- `centerY(contentH)`: vertically center content in body zone

## Style Routing

| If the deck is… | Use palette | Notes |
|---|---|---|
| Consulting / board / exec update / engagement deliverable | `consulting-mckinsey`, `consulting-bcg`, or `consulting-bain` | Match firm by content shape |
| Startup pitch / product narrative / growth story | `founder` | Clean, modern blue |
| Crisis / urgency / downturn memo / "burn/runway" rhetoric | `sequoia` | Dark, dramatic, red accent |

Palette files in `palettes/` define colors, fonts, chart rules, and mode variations.

## Firm Style (Consulting Decks)

For every consulting deck, pick the firm style whose philosophy best fits the content:

| Content shape | Best fit | Why |
|---|---|---|
| Conclusion-first, variance analysis, "what happened and why" | McKinsey | Verdict-driven titles + waterfall exhibits |
| Framework evaluation, multi-criteria scoring, "how options compare" | BCG | Evaluation matrices + panel mini-headers |
| Diagnostic, decision support, "here are the facts, here's what we think" | Bain | Facts-vs-Perspectives frame |

Load the corresponding firm reference:

| Firm style | Reference |
|---|---|
| McKinsey | [references/mckinsey.md](references/mckinsey.md) |
| BCG | [references/bcg.md](references/bcg.md) |
| Bain | [references/bain.md](references/bain.md) |

When density level requires [references/craft.md](references/craft.md) (L2+), the firm file layers on top.

## Density Profiles

| Context | Level | Pattern scope | Also read |
|---|---|---|---|
| Startup pitch, roadshow, board update | **L1 Narrative** | P-series only | none |
| Corporate strategy, business review | **L2 Structured** | P + selective C-series | [references/craft.md](references/craft.md) §1–§4 |
| MBB engagement, due diligence, deep analysis | **L3 Dense** | Full library, C-series expected | [references/craft.md](references/craft.md) §1–§7 |

## Routing Table

| User input shape / intent | Pattern | Notes |
|---|---|---|
| Cover page / identity | **p01-cover** | Slide 1 in almost every deck |
| 2×2 positioning / quadrant map | **p02-matrix** | Needs 2 axes + 4–8 items |
| Claim + chart proof (line, bar) | **p03-evidence** | Native PowerPoint chart + sidebar callouts |
| 4–8 KPIs / metrics / health check | **p04-scorecard** | Cards with number + label + trend |
| Timeline / progression | **p05-narrative-arc** | Milestones on a horizontal axis |
| Binary choice (A vs B) | **p06-fork** | Criteria grid with recommendation |
| Process / mechanism / flywheel | **p07-machine** | Numbered steps with connector |
| Closing ask / next step | **p08-closer** | Centered recommendation + bullets |
| Comparison table (rows × columns) | **p09-data-table** | Financial tables, delta coloring |
| Agenda / table of contents | **p10-agenda** | Section list with active highlight |
| Product / platform demo | **p11-product-showcase** | Product area + feature cards |
| Team / founders / engagement team | **p12-team-grid** | 4 cards with name + role + bio |
| Dense evidence: exhibit + sidebar | **c01-multi-evidence** | Chart + metrics row + drivers sidebar |
| Start/end with intermediate deltas | **c02-waterfall** | Stacked bar bridge + interpretation panels |
| Color-coded evaluation grid | **c03-eval-grid** | Criteria × options with RAG fills |
| Facts vs perspectives (two-column) | **c04-facts-perspectives** | 57/43 split: data left, judgment right |
| Section divider (full-bleed) | **c05-divider** | Dark background, section number + title |
| Stacked vertical bar chart | **p13-stacked-bar** | Segmented bars with legend, annotation sidebar |
| Ranked horizontal bars | **p14-horizontal-bar** | Data-driven widths, highlight row, value labels |
| Bubble matrix (size = magnitude) | **p15-bubble-matrix** | Area-proportional circles on rows × columns grid |
| Gantt / workplan timeline | **c06-workplan** | Calendar grid, row spans, milestone markers |

### Advanced visuals (build custom, see `masters/examples/`)

No pre-built pattern. Study the script, adapt the technique.

| Visual type | Script | Technique |
|---|---|---|
| Dumbbell chart (before→after) | `dumbbell-chart.js` | Axis scaling, arrow shapes, SVG gradient bg |
| Gauge / arc indicators | `gauge-arcs.js` | Arc math, stacked distribution bars, bar-anchored text |
| Process flow diagram | `process-flow-diagram.js` | Node graphs, icon rasterization, SVG gradients |
| Multi-zone composite | `multi-zone-composite.js` | Zone layout, data-driven bars, rich text footer columns |
| Scenario comparison cards | `scenario-cards.js` | Nested columns, multi-level bullets |
| Multi-panel segmented bars | `multi-panel-analysis.js` | Stacked bars, dashed brackets, rotated labels |
| Data table with takeaways | `outsourcing-mix-table.js` | Row fills, chip highlights, chevron connectors |
| Gantt workplan | `gantt-workplan.js` | Calendar grid, requirement bubbles, status markers |

## Composition Rules

- **Start** with `p01-cover` (most decks) or `c05-divider` (mid-deck section entry).
- **Do not repeat the same pattern back-to-back.** Alternate patterns by content type.
- **One slide = one argument.** Every action title advances a distinct claim.
- **Use interstitials intentionally:** `p10-agenda` at section openings, `c05-divider` for chapter breaks.
- **Footnotes:** bracket style (`[1]`), restart numbering per slide.
- **Density level governs composition.** Do not use L3 techniques on an L1 deck.
- **Section rhythm.** For decks >8 slides, group into 3-4 sections. Open each section with `p10-agenda` (active item) or `c05-divider`. Close with a synthesis slide before the next section.
- **Firm composition minimums.** McKinsey: ≥1 waterfall (`c02`) per variance analysis. BCG: panel mini-headers on every multi-panel slide. Bain: ≥40% of analytic slides use `c04-facts-perspectives` in diagnostic mode.
- **Chart variety.** Do not use the same chart type (bar, line, table) on consecutive slides. Alternate data shapes to maintain visual engagement.
- **Content fit.** Each pattern's slot budget (`*.slots.md`) defines character limits and item counts. Before routing, verify your content fits: too few items produces a sparse slide, and too many causes crowding. When in doubt, check the slot file's data schema and item ranges.
- **Visual balance.** Content is vertically centered in the body zone (between title and footer). Short content centers naturally, and dense content fills the zone. If a slide looks top-heavy or bottom-heavy in QA, adjust the content volume. Don't force positioning.
- **Spatial constraints.** PPTX uses absolute positioning: no responsive layout. Content must fit between `bodyY` and `bodyEndY`. Anchor elements to zone boundaries and use `valign` + `fit:'shrink'`. Never manually estimate text heights for Y positioning.

## Slot Budgets (Progressive Loading)

Slot budgets are stored per-pattern at `masters/patterns/<pattern>.slots.md`. **Load just-in-time** when building each slide. Do not read all 21 upfront.

## What NOT To Do

- Do not create HTML slide files. Use the `createDeck()` API directly.
- Do not use Playwright or browser rendering for slide content. All slide content must be native PPTX objects (text, shapes, charts) so the output is editable. Exception: rasterizing assets with no PPTX-native equivalent (e.g., SVG gradients, icon fonts). See `masters/examples/` for techniques.
- Do not scatter colors. Define a consistent palette once and reference it throughout.
- Do not position headers or footers in pattern functions. The slide master handles chrome.
