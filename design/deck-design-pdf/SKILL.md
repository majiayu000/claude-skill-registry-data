---
name: deck-design-pdf
description: >
  Create presentation decks as high-fidelity PDF files using web technology
  (HTML, CSS, Tailwind, Font Awesome). Use when the user wants a polished,
  pixel-perfect deck with responsive layouts, rich typography, icons, and
  modern design. For editable PPTX output, use deck-design-ppt instead.
---

# Deck Design PDF: Operational Playbook

## What This Skill Does

- **Input:** a deck brief + any structured data the user provides.
- **Output:** a **PDF file**: pixel-perfect slides rendered from HTML/CSS via Playwright. Not editable in PowerPoint. This is the high-fidelity, print-ready format.

### When to use this vs deck-design-ppt

| Need | Skill |
|---|---|
| Editable slides (PowerPoint/Keynote/Slides) | `deck-design-ppt` |
| Pixel-perfect PDF: web typography, icons, gradients, CSS layouts | `deck-design-pdf` (this) |

### What the web stack unlocks (beyond pptx)

- CSS Grid and Flexbox: responsive layouts instead of coordinate math
- Google Fonts with optical sizing and variable weights
- Font Awesome 6 icons inline with text
- Gradient backgrounds, box shadows, rounded corners, opacity
- ECharts 6 (SVG renderer): 21 chart types, including bar, line, pie, scatter, waterfall, gauge, sankey, treemap, radar, funnel, and heatmap
- Tailwind utility classes: rapid, consistent styling

## Phase 1: Understand and Route

### 1. Read the room

Before asking the user anything, scan the working directory for artifacts that establish context: briefs, consultant storyboards (`*-ghost.md`, `*-outline.md`), data files, brand specs, existing build scripts. Read what's there and form a working hypothesis about what this deck needs: objective, audience, tone, density, and data.

Then ask only for what's genuinely ambiguous and would change the deck's argument or audience calibration. Frame questions as choices, not open fields: *"The data suggests a Bain decision-first structure. Does that fit, or is this more of an internal working session?"* One sharp question beats five vague ones. Maximum 1–3 questions, and zero is fine if the artifacts are clear.

### 2. Classify the deck

This determines how deep the planning phase goes. Two paths:

| Signal | Path | What happens next |
|---|---|---|
| MBB engagement, strategy consulting, due diligence, cost transformation, M&A, pricing, org restructuring | **Consulting** | Load the full consulting reference library (ghost-deck.md, engagement-archetypes.md, skeletons/, firm-dna.md, evidence-recipes.md, density-adaptation.md). Build a rigorous ghost deck with archetype classification, pillar architecture, transitions, and firm overlay. |
| Startup pitch, board update, product narrative, conference talk, investor roadshow, internal update | **General** | Stay in this playbook. Build a ghost deck using the universal quality gates below: governing thought, action titles, helicopter test, exhibit assignment. No archetype classification or skeleton required. |

**Consultant handoff**: if a storyboard from the `consultant` skill already exists (governing thought, pillars, action titles, content descriptions), the argument layer is done. Skip ghost deck construction entirely. Validate the argument (run the helicopter test on the titles), then proceed to the production outline.

### 3. Pick style and density

**Style:**

| If the deck is… | Palette | Surface | Font |
|---|---|---|---|
| Consulting / board / engagement deliverable | `consulting-mckinsey` | Light | Inter |
| Framework evaluation, process-transparent | `consulting-bcg` | Light | DM Sans |
| Diagnostic, decision support, facts-vs-perspectives | `consulting-bain` | Light | Source Sans 3 |
| Startup pitch / product narrative / growth story | `founder` | Light | Plus Jakarta Sans |
| Crisis / urgency / downturn memo / high-stakes | `sequoia` | Dark | Georgia + Inter |
| Warm, rigorous-but-human strategy work (Anthropic-adjacent ivory + clay) | `anthropic-consulting` | Light | Manrope (not vendored, load via `headExtra`) |
| Google-ecosystem client engagement (muted Google Blue) | `meridian-google` | Light | Inter |

The vendored font families are Inter, DM Sans, Plus Jakarta Sans, and Source Sans 3. The agent is not limited to these. Any Google Font can be loaded via a `<link>` tag in `headExtra` when the brief calls for a different typeface.

**Brand identity intake (from brand-system skill)**: if an `identity.js` produced by the `brand-system` skill exists in the working directory, the style decision is already made. Do not route through the table above:

1. **Palette**: `identity.js` emits engine-compatible palette CSS. Write it into this skill's palette directory, then pass its name to `createDeck`:

   ```javascript
   const fs = require('fs');
   const brand = require('./identity');
   fs.writeFileSync('<this-skill>/palettes/' + brand.palette.name + '.css', brand.toCSS());
   // then: createDeck({ palette: brand.palette.name, ... })
   ```

2. **Fonts**: if `brand.fonts` names a family outside the vendored four, load it via a Google Fonts `<link>` in `headExtra` (network required at build time) or accept the stack's system fallback.
3. **Style direction**: `brand.style` routes composition treatment, not colors:

   | `identity.js` style | Compose like | Treatment |
   |---|---|---|
   | `institutional` | `consulting-mckinsey` | Restrained chrome, sharp corners, rules over boxes |
   | `modern` | `founder` | Cards, rounded corners, confident accent use |
   | `dark` | `sequoia` | Dark surfaces as default, high-contrast accents |
   | `bento` | `founder` | Card-grid compositions dominate, surface-muted tiles |
   | `editorial` | none | Typography-led: oversized headings, fewer panels, whitespace as structure |
   | `data-forward` | `consulting-bcg` | Chart-dense, panel mini-headers, minimal decoration |

The identity's colors and fonts are authoritative. Layout and composition belong to this skill.

**Density:**

| Context | Level | What changes |
|---|---|---|
| Startup pitch, roadshow, board update | **L1 Narrative** | 1 message per slide. Fewer elements, each scaled up to fill the body zone. |
| Corporate strategy, business review | **L2 Structured** | Multi-panel layouts. Evidence density moderate. |
| MBB engagement, due diligence, deep analysis | **L3 Dense** | Multi-evidence composites. Chained arguments. |

**Show deck vs. working deck**: infer from audience and objective, don't ask. "Board presentation" → `tier: 'presentation'` (body ≥15pt, room-safe). "Diligence data room" → `tier: 'document'` (body ≥12pt, dense but legible). The tier shifts ALL text tokens automatically.

For L2+ consulting decks, apply firm-specific conventions from [firm-dna.md](firm-dna.md). For density adaptation rules, see [density-adaptation.md](density-adaptation.md).

## Phase 1.5: Ghost Deck

Before writing any HTML, build the **ghost deck**, the narrative skeleton that precedes all visualization. Charts and code are execution. The ghost deck is the thinking.

The ghost deck process produces two artifacts:
- **`{slug}-ghost.md`**: the argument layer. Governing thought, action titles, exhibit types. A senior reviewer can approve this without knowing CSS.
- **`{slug}-outline.md`**: the execution layer. Ghost deck + density tiers, layout geometry, chart dimensions, column alignment. This is what the build phase reads.

**Process management.** Building a ghost deck requires populating multiple interdependent layers and passing quality gates that may trigger backtracking. Use your task management tools to track which layers are complete, which gates have passed, and what needs revisiting. Externalize this state. Don't try to hold it all in one pass.

### Universal quality gates

These apply to **every deck**: consulting, startup, board update, conference talk. They are not consulting methodology. They are good deck design.

Start from the governing thought, one sentence that states the deck's answer. Build pillars that support it. Write action titles for every slide before you touch any charts. Read the titles in sequence. If they don't tell a complete story, the problem is in the pillars, not the titles. Only assign exhibits once the argument holds. Cut any slide that isn't load-bearing.

**What must exist in every ghost deck:**

| Layer | What it is | Depends on |
|---|---|---|
| **Governing thought** | One sentence: the deck's answer. If you can't write it, the analysis isn't done. | The brief and data |
| **Action titles** | Full-sentence conclusion for every slide. "Revenue grew 12% driven by pricing power", not "Revenue Overview." | Governing thought |
| **Helicopter test** | Read all titles in sequence. Complete, persuasive story in 2 minutes? If not, fix the titles. | Action titles |
| **Exhibit assignment** | What visual proves each slide's claim. Use [chart-taxonomy.md](chart-taxonomy.md): "What does this slide need to prove?" → exhibit type. | Helicopter test passed |
| **Dead slide test** | Can any slide be removed without breaking the argument? If yes, remove it. | All of the above |

**Common deck patterns.** For non-consulting decks, [chart-taxonomy.md](chart-taxonomy.md) § Deck Archetypes provides narrative arcs and exhibit mixes for common formats: investor/roadshow (Problem → Solution → Traction → Market → Model → Team → Ask), board updates (Headlines → KPIs → Progress → Risks → Decisions), due diligence memos, transformation roadmaps, and more. Use these as starting points for the slide sequence, then write action titles and apply the quality gates above. Don't force a pattern that doesn't fit the brief. Adapt or combine as the argument requires.

**Backtracking, not patching.** If the helicopter test fails, the problem is upstream: the pillars don't support the governing thought, or the titles are topic labels instead of conclusions. Go back to where the argument breaks. Don't patch titles to paper over a structural gap.

**When the brief supports multiple valid governing thoughts**: surface the options and let the user choose before proceeding. Otherwise, commit to the strongest hypothesis and work forward.

### Consulting path

For MBB engagements and strategy consulting, the ghost deck goes deeper. Load the full reference library:

| Doc | Purpose |
|---|---|
| [ghost-deck.md](ghost-deck.md) | 5-layer model, quality gates, anti-patterns |
| [engagement-archetypes.md](engagement-archetypes.md) | 8 archetypes, 5 transition types, rising-stakes progression |
| `skeletons/*.md` | Pillar architecture, slide-by-slide index, kill conditions per archetype |
| [firm-dna.md](firm-dna.md) | McKinsey/BCG/Bain epistemology, communication signatures |
| [evidence-recipes.md](evidence-recipes.md) | 10 data-shape recipes, layering rules |
| [density-adaptation.md](density-adaptation.md) | L1/L2/L3 compression/expansion rules |

On top of the universal quality gates, the consulting path adds:

- **Archetype classification**: classify the engagement using [engagement-archetypes.md](engagement-archetypes.md), then load the matching skeleton from `skeletons/`. The skeleton provides a pillar architecture and slide-by-slide index as a starting point. Customize it to the specific brief.
- **Pillar architecture**: 3–5 MECE pillars supporting the governing thought. Work backward: "What must be true for the governing thought to hold?"
- **Transition architecture**: at each pillar boundary, select a transition type (Pivot, Narrowing, Escalation, Synthesis, Decision Gate). Verify rising-stakes progression: Recognition → Clarity → Conviction → Urgency.
- **Firm overlay**: apply [firm-dna.md](firm-dna.md) conventions for the target firm style. This affects header structure, communication signature, and composition patterns, not the argument itself.
- **Evidence recipes**: for each exhibit, check [evidence-recipes.md](evidence-recipes.md) for the standard composition: primary chart + supporting elements + annotation layers, governed by density level.

These layers have dependencies (you can't design transitions until pillars exist, and you can't assign evidence recipes until exhibits are selected), but the agent decides the working order based on what the brief gives it. A brief with strong data might start from what the data proves and work backward to the governing thought. A brief with a clear strategic question might start top-down.

### Consultant handoff

When a storyboard from the `consultant` skill already exists (governing thought, pillars, action titles, content descriptions, structured data), the argument layer is done. This skill inherits it and focuses on production:

1. Run the helicopter test on the provided action titles. If titles read as topic labels rather than conclusions, strengthen them.
2. For each slide, use the content description + [chart-taxonomy.md](chart-taxonomy.md) decision tree to select exhibit types. The consultant describes WHAT each slide proves. This skill decides HOW to visualize it.
3. This skill may tighten action titles, add transition slides, or adjust slide count for density. The consultant's governing thought and pillar architecture are authoritative. Exhibit selection and layout composition belong to this skill.

### Presenting the ghost deck

Once the ghost deck is complete, present it to the user as the **storyline**: just the action titles in sequence. This is the helicopter test output:

> *Here is the argument this deck makes, read top to bottom:*
> *1. [Action title]*
> *2. [Action title]*
> *...*
> *Does this story hold? Anything missing, out of order, or unconvincing?*

Don't print the full outline with density tiers and exhibit types. That's implementation detail. The user's job is to validate the argument, not review the geometry. If they approve, proceed to the production outline. If they redirect, revise and present again.

### Production outline

The production outline (`{slug}-outline.md`) extends the ghost deck by adding geometry to every slide. This is the contract between thinking and building: the build phase copies these numbers, no sizing reasoning required at code time.

For every slide in the ghost deck, add:
- **Density tier**: which CSS class governs typography
- **Layout**: composition type + percentage split (e.g., "asymmetric split, left 60% / right 40%")
- **Column alignment**: `items-start` when columns differ in content height, `items-center` only for visually balanced columns
- **Chart spec**: explicit dimensions derived from the space budget (see § Space audit below)
- **Evidence layers**: 1 for L1, 1–2 for L2, 2–4 for L3

```
N. **Action title (full sentence conclusion)**
   - Density: sd-medium
   - Layout: asymmetric split, left 60% / right 40%
   - Column alignment: items-start
   - Exhibit: clustered bars (market share by segment)
   - Chart spec: 700px × 480px. Body 600px − 120px (top labels + gap) = 480px
   - Data: SWE-bench scores, coding market share
   - Evidence layers: 2
```

Save as `{slug}-outline.md`. The ghost deck is not modified. It remains the clean argument document.

**Outlines that omit exhibit types** produce decks dominated by KPI cards and text bullets, the most common quality failure. The outline must have Layout + Exhibit before the build starts.

### Space audit

Before writing any code, run a space audit on every slide that contains a chart or diagram. The slide canvas is 1280×720px. After header (~76px) and footer (~44px), the body zone is **≈ 600px tall, ≈ 1168px wide** (56px margins each side). In a two-column layout, each column is ≈ 576px.

For each chart slide: subtract any non-chart content (card rows, KPI strips, table rows, gaps) from the 600px body height. The remainder is the chart height. Write this math in the outline. The build agent copies the number directly.

```
body height 600px − top content Apx − bottom content Bpx = chart height
```

**Key rules:**
- If chart height > chart width for that column, the chart is portrait. That's correct. Portrait orientation eliminates blank space structurally.
- If two columns have different content heights, set `align-items:start`. Don't default to center.
- If the computed chart height exceeds the density class default, override it. The space budget wins.

**Estimation reference (1280×720):**

| Content element | Estimated height |
|---|---|
| 3-card row (compact) | ~120px |
| KPI metric strip (3–4 numbers) | ~80px |
| Table (5 rows) | ~180px |
| Gap between elements | 16–24px |

## Phase 2: Build

### How to build slides

Read `{slug}-outline.md`. Each slide entry has an action title, exhibit type, layout, and chart dimensions. The build phase executes these specs. It does not re-derive them. Sizing decisions were made in the outline. The build agent copies the numbers.

You are composing **custom HTML for each slide** based on the user's actual data and the outline's argument. You are NOT filling in a template. The examples under `examples/*.js` are visual pattern references. Study their approach, then write original HTML that serves the specific argument.

**Space budget reference.** At 1280×720, the available zones are:

| Zone | Pixels | Notes |
|---|---|---|
| Slide canvas | 720px tall, 1280px wide | Fixed |
| Header zone | ~76px | Section label + title + accent bar + padding |
| Footer zone | ~44px | Source line, fixed by grid shell |
| **Body height** | **≈ 600px** | What remains. This is your working space |
| Horizontal margin | 56px each side | Tailwind `px-14` |
| **Content width** | **≈ 1168px** | 1280 − 112px margins |
| Each column (2-col) | ≈ 576px | (1168 − gap) ÷ 2 |

**For each slide in the outline:**

1. **Set the tier**: `'presentation'` for any deck projected in a room or read by executives. `'document'` (default) for working sessions and analysis. The tier shifts all text baselines automatically. Do not adjust individual font sizes. Infer from audience and objective. Don't ask.
2. The action title tells you **what to prove**. The exhibit type tells you **how to prove it**. The chart spec tells you the **exact dimensions**.
3. Read the relevant example file to learn the visual pattern: the ECharts config structure, the CSS layout approach, the annotation placement. Do not copy its data or dimensions.
4. Compose the slide HTML with the user's real data. Use the slide shell (header → body → footer). Apply palette CSS custom properties. Never hardcode brand colors.
5. Size slide text through the Tailwind type roles (build-reference.md § Typography scale). Inside ECharts config, compute font sizes and geometry from the chart's actual width and height the way the examples do: declared `[min, max]` ranges with clamped interpolation, not fixed magic numbers.

**What to learn from each example:**

| Look at | To understand |
|---|---|
| ECharts `setOption({...})` structure | Which config keys produce this chart type |
| The "Brand variables" block | Which colors and fonts are meant to be swapped from the palette |
| The "Sizing limits" + computed sizing block | How fonts and geometry interpolate with canvas width/height |
| The "ECharts gotchas" header comment | Library pitfalls this pattern already solved: label colors, wrapping, `containLabel` |
| Semantic color usage | Accent for focus, gray for context, green/red for deltas |
| The `proves` field | What analytical question this pattern answers |

**What NOT to copy from examples:**

- Sample data ("$4.2B", "12.4M units"): use the user's actual numbers.
- Action titles and section labels: write new ones from the ghost deck.
- Hardcoded hex colors for palette roles: use `var(--accent)`, `var(--text)`, etc.
- Fixed dimensions: adapt to the content density and slide count. Examples follow a roughly landscape aspect ratio. Your slide's body space may demand a portrait or square chart. Fill the available body height first, then constrain only if content overflows.

**Fill-first orientation.** When sizing a chart or visual exhibit, start from the body height (≈ 600px), subtract any labels, gaps, or card rows above/below the chart, and set the chart to that remaining height. Do not start from an example's hardcoded height and stretch slightly. A chart that fills the body zone vertically eliminates blank space structurally. No bottom padding hack required. Portrait charts (height > width) are valid and preferred over leaving empty space at the slide bottom.

**Choosing between visual patterns:**

When two exhibit types could work, choose based on the **argument**, not the visual appeal:

- Waterfall answers "what drove the change?": use when the audience needs to see sequential drivers
- Driver tree answers "what multiplies into what?": use when the audience needs to see the structural decomposition
- Horizontal bars answer "who is ahead?": use when ranking is the point
- Distribution answers "how spread out?": use when the variance is the insight, not the average

If the taxonomy's decision tree doesn't clearly route to one pattern, default to the simplest exhibit that proves the title's claim. A single bold number is often more powerful than a chart. Simplicity is not laziness. It is restraint.

Load [build-reference.md](build-reference.md) for the full slide construction reference: build script template, slide shell, layout primitives, content primitives, typography scale, design tokens, spatial constants, icons, ECharts configuration, composition routing, and layout anti-patterns.

### Key build principles

- **Use CSS Grid for the slide shell** (`grid-template-rows: auto minmax(0,1fr) 48px`). This structurally prevents footer overflow. Do not use `flex flex-col` with `flex-1`.
- **Fill-first orientation.** Start from body height (≈ 600px), subtract surrounding elements, set the chart to the remainder. Portrait charts (height > width) are valid and preferred over leaving empty space.
- **Use palette tokens** (`var(--accent)`, `var(--text)`, etc.), not hardcoded hex.
- **Use `headExtra` CSS classes** for the shell on decks >5 slides. Use Tailwind for body content layout.
- **For decks >10 slides**, consider modular authoring: one file per slide, assembled by `build.js`.
- **ECharts: SVG renderer only** (`{ renderer: 'svg' }`). Canvas blanks in Playwright PDF. Always set `animation: false`.

## Firm Style

For L2+ consulting decks only. All three firms use the same charts. What differs is communication structure.

| Firm | Header | Composition signature | Accent |
|---|---|---|---|
| **McKinsey** | Section label + action title. No rule. | Verdict-first: conclusion in title, evidence below. Exhibit numbering. | Navy |
| **BCG** | Section label + action title + green rule below. | Framework-first: analytical structure visible, panel mini-headers. | Green |
| **Bain** | Action title + red rule below. No section label. | Decision-first: facts-vs-perspectives split (left 55% data, right 45% interpretation). | Red |

For full firm conventions, load [firm-dna.md](firm-dna.md). For chart-level visual treatment, see [chart-taxonomy.md](chart-taxonomy.md) § Firm Visual Identity.

## Composition Rules

- **Start** with a cover slide. Use section dividers for chapter breaks in decks >8 slides.
- **One slide = one argument.** Every action title advances a distinct claim.
- **Dead slide test.** If you can remove a slide and the argument still works, remove it. Every slide must be load-bearing.
- **Do not repeat the same layout back-to-back.** Alternate between layout types.
- **Helicopter test.** Read all action titles in sequence. They must tell a complete, persuasive story without any exhibit bodies.
- **Density level governs composition.** Do not use L3 multi-evidence composites on an L1 pitch deck.
- **Chart variety.** Do not use the same chart type on consecutive slides.
- **Icon restraint.** One icon per card or list item. No icon walls. Use accent color, not rainbow.
- **Section rhythm.** For decks >8 slides, group into 3–4 sections. Open each with agenda (active item) or divider. Close with synthesis before the next section.
- **Content fit.** Content must fill the body zone without overflow or sparseness. If a slide looks empty, add evidence layers. If it's crowded, split into two slides.
- **Visual balance.** Content is vertically centered in the body zone by Flexbox. Let `flex-1` handle distribution. Do not force absolute positioning.
- **Color discipline.** Use palette tokens, not hardcoded hex. Semantic colors (emerald/amber/red) only for status indicators, never for decoration.
- **Annotation is value, not decoration.** See chart-taxonomy.md's Annotation Grammar. The callout that says "This 15% gap = $340M unrealized" is why the engagement costs what it costs.

## Output Organization

Save deliverables to the current working directory (or user-specified folder). Kebab-case naming:

- `{slug}.pdf`: the deliverable
- `build-{slug}.js`: the build script (reproducible)
- `{slug}-ghost.md`: the argument layer (governing thought, action titles, exhibits)
- `{slug}-outline.md`: the execution layer (ghost deck + geometry)

## Architecture

Self-contained: `package.json` + `node_modules/` are inside the skill folder. All `require()` calls resolve locally.

| File | When to load | Purpose |
|---|---|---|
| `build-reference.md` | Phase 2 (Build) | Slide shell, typography, ECharts, layout primitives, anti-patterns |
| `chart-taxonomy.md` | Exhibit selection | Decision tree, firm visual DNA, deck archetypes, annotation grammar |
| `ghost-deck.md` | Consulting path | 5-layer model, dependencies, quality gates, golden trace |
| `engagement-archetypes.md` | Consulting path | 8 archetypes, transitions, rising-stakes progression |
| `skeletons/*.md` | Consulting path | Pillar architecture, slide index, kill conditions per archetype |
| `firm-dna.md` | Consulting path | McKinsey/BCG/Bain epistemology, communication signatures |
| `evidence-recipes.md` | Consulting path | 10 data-shape recipes, layering rules |
| `density-adaptation.md` | Consulting path | L1/L2/L3 compression/expansion rules |
| `engine/index.js` | Always | `createDeck(options)`: assembles HTML, calls renderer |
| `engine/render.js` | Always | Playwright Chromium → `page.pdf()` |
| `palettes/*.css` | Always | CSS custom properties per style (colors, fonts) |
| `examples/*.js` | Build reference | 46 self-contained visual pattern references, read-only, not imported at runtime |

**How examples relate to deck building:** The agent does NOT import or call example files at runtime. Examples exist as **read-only references**: the agent reads them to learn visual patterns, then writes original HTML in the build script. The build script uses only `engine/index.js` (`createDeck`). Each example is fully self-contained (brand variables, data, sizing limits, and responsive formulas live inline in one file), so reading a single example shows the complete pattern.

The engine handles: HTML document assembly, vendored font loading, Font Awesome injection, ECharts (SVG renderer), Tailwind injection, palette CSS injection, Playwright launch, `page.pdf()` rendering. All assets are local: zero network dependency at build time.

## What NOT To Do

**Rendering constraints:**
- Do not use `<canvas>` for charts. Canvas elements blank in Playwright's PDF pipeline. Use ECharts SVG renderer or CSS-only visuals.
- Do not add animation, transitions, or hover states. The output is static PDF.
- Do not use `@media print` overrides. The engine uses `emulateMedia('screen')`.
- Use CSS Grid (`grid-template-rows: auto minmax(0,1fr) 48px`) for the slide shell, not `flex flex-col` with `flex-1`. See § Wrapped slide shell and § Slide layout anti-patterns.

**Architecture constraints:**
- Do not create separate HTML files per slide. All slides go in one build script, one HTML document, one PDF.
- Do not generate interactive presentations (Reveal.js, Slidev). Output is always static PDF.
- Do not hardcode palette colors. Use CSS custom properties (`var(--accent)`, `var(--text)`, etc.) so palette switching works.

**Design discipline:**
- Do not copy example data into real decks. Example numbers ($4.2B, 12.4M units) are illustrative. Use the user's actual data.
- Do not choose exhibit types by visual appeal. Choose by what the slide's argument needs to prove. A bold number can be more powerful than a chart.
- Do not over-decorate. No icon walls, no rainbow colors, no gradients on data elements. Consulting aesthetics come from restraint, not embellishment.
- Do not use the same exhibit type on consecutive slides. Alternate to maintain visual rhythm.

**Agent behavior:**
- Do not ask the user to pick a chart type. The taxonomy's decision tree and the ghost deck's action titles determine the exhibit. You make the visual decision.
- Do not ask the user for show vs. working deck preference. Infer from audience and objective: "board presentation" is show, "diligence data room" is working.
- Do not present multiple layout options for approval. Commit to the best composition based on the content density and argument structure. The user reviews the output PDF, not a menu of choices.
