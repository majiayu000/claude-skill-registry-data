---
name: slide-sage
description: Create or enhance a data-rich, single-file HTML slide deck or pitch deck. Use when the user asks for a new presentation, to convert a PowerPoint (.pptx) or PDF into an HTML deck, or to improve an existing HTML presentation. Not for native PowerPoint editing or high-fidelity PPTX export.
license: MIT
metadata:
  version: "2.2.0"
  author: rhnfzl
---

# Slide Sage

Create data-rich, interactive HTML presentations as a single HTML runtime with charts, diagrams, and code highlighting.

## Core Principles

1. **Data-First** - Charts, diagrams, and metrics are first-class citizens, not afterthoughts
2. **Single HTML Runtime** - Keep presentation HTML, CSS, and JavaScript in one file. Use an `assets/` directory only for many or large images. Load pinned libraries from a CDN by default. When offline delivery is requested, run `scripts/inline-vendor.py` after generation and keep the bundled notices with the output.
3. **Viewport Fitting (NON-NEGOTIABLE)** - Every slide fits exactly within 100vh. No scrolling. Content overflows? Split into multiple slides
4. **Adaptive Intelligence** - When given raw data, act as narrative director. When given a clear outline, act as layout executor
5. **Colorblind Safe** - All data visualization uses accessible color palettes by default
6. **Utility-First CSS (NON-NEGOTIABLE)** - Define CSS classes in `<style>` before referencing them in HTML. Never use inline `style="..."` for properties that repeat across 2+ elements. Read `references/css-class-inventory.md` for all available classes

## Anti-slop design doctrine

Every visual choice must clarify a claim, comparison, hierarchy, or state. Do not use generic dashboard gradients, floating glass cards, repeated glowing borders, or an accent color as decoration. Do not default to Inter or the Catppuccin values `#1e1e2e`, `#cdd6f4`, and `#89b4fa`. Commit to one named preset, use its tokens for the interface, use the Tier 1 palette for data, and give each slide one intentional focal point. Limit a slide to one orchestrated reveal sequence. A literal hex belongs only in the selected preset, Tier 1 palette, or an intentional visual asset.

Charts represent supplied facts. Never silently invent numbers, percentages, sources, or time periods.

## Phase 0: Detect Mode

Determine what the user wants:

- **Mode A: New Presentation** - Create from scratch. Go to Phase 1
- **Mode B: PPT/PDF Conversion** - User provides a .pptx or .pdf file. Extract content with `scripts/extract-pptx.py` or `scripts/extract-pdf.py`, then treat extracted JSON as input for Mode A
- **Mode C: Enhancement** - User references an existing HTML file. Read it first, understand its style and structure, then add/modify slides while preserving consistency

### Mode C Rules

When enhancing existing presentations:
1. Read the existing HTML file completely before making changes
2. Match the existing style preset, fonts, colors, and animation level
3. Check content density before adding - respect slide type limits
4. If modifications cause overflow, split into additional slides automatically
5. Preserve all existing speaker notes and keyboard navigation

## Phase 1: Gap-driven intake

Infer audience and style from a detailed prompt and state the choice in one line. Ask only when the prompt is genuinely thin. Never block in one-shot, subagent, or CI runs: choose sensible defaults and state them in one line. Offer a visual preview only when style is unspecified and a browser is available.

When an interactive response would materially change the deck, ask one focused question. The visual preview is optional and must not delay generation.

### Genuine gaps

| Gap | Focused question |
|---|---|
| No data provided but the topic requires factual chart data | "Do you have the numbers and their source?" |
| Scope is too ambiguous to choose a useful slide count | "Roughly how many slides? (5 for a quick update, 15+ for a deep dive)" |
| The prompt does not say who reads the slide | "Will you present this live, send it to be read on its own, or both?" |
| The prompt does not say how much prose belongs beside the visuals | "Diagram-led, balanced, or text-rich?" |

**Never ask about**: animation level (detect from audience), library choices (auto-select), file format (auto-detect), presenter mode (included automatically whenever the deck has speaker notes, see Reader and density), or brand information when a named preset is sufficient.

### Reader and density

These two answers decide more about whether a deck lands than the preset does, and **neither is inferable from the audience**. A leadership deck can be diagram-led or text-rich. The same deck can be presented or forwarded. Treat both as genuine gaps unless the prompt states them, because a prompt almost never does.

**Reader** decides WHERE the context lives:

| Answer | Slide face | Speaker notes |
|---|---|---|
| `present` | Stays clean. The room reads the slide, the presenter reads the notes. | Carry the recall material. Presenter mode ships. |
| `send` | Must carry the context. Nobody is there to explain it. | Fold onto the slide instead. A note nobody opens is a note nobody reads. |
| `both` (default) | Readable standalone. | Carry the extra depth. Presenter mode ships. |

**Density** decides HOW MUCH prose sits beside the visual:

| Answer | Shape of a content slide |
|---|---|
| `diagram-led` | Diagram or example is the slide. At most 3 short lines, and only for what the diagram cannot say. |
| `balanced` (default) | One plain-language lead sentence, the diagram, then 4 to 6 points. |
| `text-rich` | Full sentences. The reason, the tradeoff, and the caveat all sit on the slide face. |

Ask both in one turn when both are missing. State the inferred answers in one line when the prompt gives them.

**The failure this prevents.** Terse and dense are both wrong when guessed, and guessing tends to overcorrect: a deck stripped to diagrams starves the presenter of anything to recall from, and a deck padded to explain everything walls off the room it is shown to. "Too much text" on a previous deck does NOT mean `diagram-led` on the next one; it means the reader and density were never separated. Ask instead of swinging.

**Never let the presenter's half be invisible.** If the recall material only exists in a place the presenter cannot see while presenting, it does not exist. Speaker notes without presenter mode are exactly that failure.

### Large decks

For a presentation with more than 15 slides, share a brief outline only when it resolves a genuine scope gap in an interactive run. Otherwise choose a sensible structure, state it in one line, and continue.

## Phase 2: Content Analysis

Analyze the user's content to determine what's needed.

### Detect Content Types

Scan the user's message for:

| Signal | Content Type | Action |
|--------|-------------|--------|
| Numbers, metrics, KPIs, percentages | **Data/Charts** | Read `references/viz-integration.md` |
| "Architecture", "flow", "system design", "pipeline" | **Diagrams** | Read `references/diagram-patterns.md` (CSS/HTML preferred, SVG templates, inline SVG) |
| Code snippets, "API", "endpoint", function names | **Code slides** | Read `references/code-highlighting.md` |
| Comparative language ("vs", "compared to", "before/after") | **Comparison slides** | Use comparison templates |
| JSON/CSV data pasted or file referenced | **Data parsing** | Parse inline or read file |
| .pptx file path | **PPT conversion** | Run `scripts/extract-pptx.py` |
| .pdf file path | **PDF conversion** | Run `scripts/extract-pdf.py` |
| Images referenced | **Image processing** | Use `scripts/process-images.py` if needed |
| Architecture with specific tech (DB, cloud, auth, security) | **Icons** | Read `references/icon-library.md` |

### Library Selection (Silent)

Based on content types, decide which CDN libraries to include. Do NOT ask the user - just select:

| Need | Library | CDN |
|------|---------|-----|
| Bar, line, pie, scatter, radar charts | Chart.js 4.4 | `cdn.jsdelivr.net/npm/chart.js@4.4.7/dist/chart.umd.min.js` |
| Heatmap, sankey, treemap | ECharts 6.1 | `cdn.jsdelivr.net/npm/echarts@6.1.0/dist/echarts.min.js` |
| Custom statistical charts | D3.js v7 | `cdn.jsdelivr.net/npm/d3@7.9.0/dist/d3.min.js` |
| Network/dependency graph | Cytoscape.js | `cdn.jsdelivr.net/npm/cytoscape@3.34.0/dist/cytoscape.min.js` |
| Calendar/activity heatmap | Frappe Charts | `cdn.jsdelivr.net/npm/frappe-charts@1.6.2/dist/frappe-charts.min.umd.js` |
| Code syntax highlighting | Prism.js | `cdn.jsdelivr.net/npm/prismjs@1.30.0/prism.min.js` |
| Number animations | CountUp.js | `cdn.jsdelivr.net/npm/countup.js@2.8.0/dist/countUp.umd.min.js` |
| Typing effects (title slides) | Typed.js | `cdn.jsdelivr.net/npm/typed.js@2.0.16/dist/typed.umd.js` |
| Hand-drawn diagram accents | Rough.js | `cdn.jsdelivr.net/npm/roughjs@4.6.6/bundled/rough.min.js` |
| Generative backgrounds | q5.js | `cdn.jsdelivr.net/npm/q5@4.7.4/q5.js` |
| Icons for diagrams/content | Lucide (inline) | Inline SVG paths from `templates/icons/lucide-sprite.svg` - no CDN needed |

**Default**: If the presentation has only text, include NO extra libraries. CSS animations suffice. Use CDN libraries by default. If the user explicitly needs offline delivery, create the deck first, run `scripts/inline-vendor.py`, and keep `THIRD_PARTY_NOTICES.md` with the offline copy. Do not call a deck offline if the converter reports an unsupported static remote asset.

### Detect Animation Level

| Audience Signal | Level |
|----------------|-------|
| "Technical", "engineers", "developers", "code review" | **Minimal** |
| "Business", "stakeholders", "team update" | **Balanced** |
| "Pitch", "investors", "conference", "keynote", "wow" | **Dramatic** |
| No signal | **Balanced** (default) |

### Detect File Format

- Less than 3 small images → **Single HTML file** (images as data URIs)
- Many images or large images → **HTML file + assets/ folder**

## Phase 3: Style Selection

Read `references/style-guide.md` for the full style system.

### Three-Tier System

**Tier 1: Data-Viz Palettes** - Always applied. Colorblind-safe chart colors regardless of aesthetic choice.

**Tier 2: Named Presets** - Choose by the requested tone first, then use content type only as a tie-breaker. Read the compact index in `references/style-guide.md` and load the matching file from `references/presets/`.

**Tier 3: Custom Theme** - If user provides brand colors, generate a custom theme using the theme builder algorithm.

### Style Application

1. Set `data-theme` and `data-mode` on `<html>` from the chosen preset
2. Add the preset's matching font `<link>` in `<head>` before the presentation `<style>` block. If CSS is the only option, place the preset's `@import` as the first stylesheet statement, before `viewport-base.css` and all other rules.
3. Inline the selected preset CSS with its system-font fallback, then inline `viewport-base.css` so the base classes consume the preset tokens.
4. Use the Tier 1 palette for charts, independently of the preset accent
5. Apply the preset's light or dark default unless the user overrides it

## Phase 4: Generate Presentation

### Step 1: Read Required References

Always read:
- `references/html-template.md` - Base HTML structure, SlidePresentation class
- `references/viewport-system.md` - Responsive CSS rules
- `assets/viewport-base.css` - Core CSS to inline
- `references/css-class-inventory.md` - Available CSS classes and inline style rules

Conditionally read (based on Phase 2 analysis):
- `references/viz-integration.md` - If charts/data
- `references/diagram-patterns.md` - If architecture/flow diagrams
- `references/animation-guide.md` - For animation patterns at detected level
- `references/code-highlighting.md` - If code snippets
- `references/presenter-mode.md` - Whenever the deck has speaker notes, which is every deck whose reader is `present` or `both`. Not optional: notes the presenter cannot open during the talk are notes that do not exist. Skip only for a `send` deck, where the notes are folded onto the slide instead.

### Step 2: Plan Slide Structure

Before generating, plan the slide deck:

1. **Title slide** - Presentation title, subtitle, date/author
2. **Agenda/Overview slide** - If 8+ slides
3. **Content slides** - One concept per slide, respect density limits:
   - Title: 1 heading + 1 subtitle
   - Content: 1 heading + 4-6 bullets OR 2 short paragraphs
   - Chart: 1 heading + 1 chart (max 55vh height) + optional caption
   - Code: 1 heading + 10-12 lines of code
   - Diagram: 1 heading + 1 diagram (max 60vh)
   - Comparison: 1 heading + 2 columns
   - Quote: 1 quote (max 3 lines) + attribution
   - Image: 1 heading + 1 image (max-height: min(50vh, 400px))
4. **Key takeaway / Summary slide** - If 8+ slides
5. **Closing slide** - Thank you, contact, or call to action

The numbers above are the `balanced` default. The density answer from Phase 1 scales the prose, never the viewport rule:

| Density | Content slide | Diagram and chart slides |
|---|---|---|
| `diagram-led` | 1 heading + at most 3 short lines | The visual is the slide. Add a line only for what the visual cannot say. |
| `balanced` | 1 heading + 1 lead sentence + 4-6 bullets | Visual + 2-3 supporting lines |
| `text-rich` | 1 heading + 4-6 full sentences, carrying the reason and the caveat | Visual + the explanation that would otherwise be a speaker note |

Density changes how much goes on a slide. It never changes the 100vh rule. Content that does not fit still splits into another slide at every density.

**Content exceeds limits? Split into multiple slides. Never cram, never scroll.**

### Step 3: Generate HTML

Structure the HTML file:

```
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[Presentation Title]</title>
  <link href="[Google Fonts URL]" rel="stylesheet">
  <style>
    /* viewport-base.css (inlined) */
    /* Chosen style preset CSS variables */
    /* Animation keyframes for detected level */
    /* Code theme CSS (if code slides) */
    /* Prism.js theme (if code slides) */
  </style>
</head>
<body>
  <div class="slides-container">
    <div class="slide" id="slide-1">
      <div class="slide-content">
        <!-- Slide content -->
      </div>
    </div>
    <!-- More slides -->
  </div>
  <script id="speaker-notes" type="application/json">[{"slide":1,"notes":"Speaker note text"}]</script>

  <div class="progress-bar"><div class="progress-fill"></div></div>
  <div class="slide-counter"></div>

  <!-- CDN libraries (only those needed) -->
  <script src="[Chart.js CDN if needed]"></script>
  <script src="[Prism.js CDN if needed]"></script>

  <script>
    // SlidePresentation class (from html-template.md)
    // Chart initializations
    // Diagram template rendering
    // Prism.highlightAll() - MUST call after DOM ready
  </script>
</body>
</html>
```

### Step 4: Chart Generation

When creating charts, follow these rules:

1. Use Chart.js as default (covers 80% of chart needs)
2. Place canvas in a responsive container: `max-height: min(55vh, 420px)`
3. Apply colorblind-safe palette from Tier 1
4. Match chart text colors to the presentation theme
5. Set animation based on detected level (minimal → `animation: false`)
6. Max 2 charts per slide in a side-by-side flexbox layout
7. Include axis labels and a legend where appropriate

### Step 5: Diagram Generation

Use a CSS-first approach for all diagrams.

**Tier 0: CSS/HTML Diagrams (PREFERRED - use for 80% of diagrams)**

Styled divs with flexbox/grid, borders, and accent colors. Full theme integration, perfect sizing, zero dependencies. Use the utility classes from `viewport-base.css`:

- **Sequence flows** → `.sequence-flow`, `.seq-participants`, `.seq-actor`, `.seq-step`, `.seq-arrow`
- **Architecture stacks** → `.arch-stack`, `.arch-row`, `.arch-row-group`
- **Pyramids/hierarchies** → `.pyramid`, `.pyramid-layer`
- **Process flows** → `.process-flow`, `.process-step`, `.process-arrow`
- **Comparisons** → `.card-accent`, `.card-top-accent` with CSS Grid

See `references/diagram-patterns.md` Tier 0 for complete HTML patterns.

**Tier 1: SVG Templates** - If the diagram matches a common pattern, use a pre-designed SVG template from `templates/diagrams/`. Available: microservices, data-pipeline, client-server, layered-arch, cicd-pipeline, hub-and-spoke, cloud-three-tier, kubernetes-cluster, event-driven-pubsub, ml-pipeline, c4-context, network-zones, api-gateway-auth, pyramid-roadmap, funnel, nested-scopes, tree-hierarchy. Write only the data object (~200-400 chars)

**Tier 2: Inline SVG** - Only for fully custom diagrams needing precise geometry (network topologies, custom shapes). Use `viewBox` + `preserveAspectRatio` + CSS variables for colors. Never use raw coordinate math for arrows - use CSS borders or SVG `<marker>` with clean polygon definitions.

For diagram style:
- **Clean geometric** (default) - Rounded corners, soft colors, professional
- **Hand-drawn** (user opts in) - Apply Rough.js to shapes for sketch-style

### Step 5b: Icon Integration

When slides reference specific technologies or infrastructure components, enhance visual recognition with icons from the curated Lucide icon set.

**When to use icons:**
- Architecture diagrams mentioning specific tech (database, cloud, auth, server)
- Process steps or workflow slides where icons aid scanning
- KPI/metric cards where a category icon adds context
- Bullet lists with technical items (optional, don't overuse)

**How to include:**
1. Read `references/icon-library.md` for the full icon catalog and path data
2. Include the hidden sprite block from `templates/icons/lucide-sprite.svg` at the top of `<body>` (before slides)
3. Reference icons via `<use href="#icon-name">` inside inline SVG diagrams
4. Or use standalone `<svg class="icon">` elements in HTML slide content

**Icon sizing:**
- In SVG diagrams: `width="20" height="20"` for standard boxes, `width="16" height="16"` for small contexts
- In HTML content: use the `.icon` CSS class (1.2em, inherits text color)

**Rules:**
- Icons are always optional - never required. Templates work perfectly without them
- Only include the sprite block when at least one slide uses icons (don't add unused dependencies)
- Icons inherit `currentColor` - they automatically match the presentation theme
- Prefer icons that reinforce the component's function: database→database, auth→shield, API→plug, cloud→cloud

### Step 6: Comparison Slides

When content involves comparisons (before/after, pros/cons, A vs B):
- Use split-view layout from `templates/comparison/split-view.html`
- Or feature matrix from `templates/comparison/feature-matrix.html`
- Color-code columns with accent and secondary accent colors

### Step 7: Visual Polish (Applied by Default)

Apply visual depth only when it makes a claim easier to read. Keep one orchestrated reveal sequence per slide at most.

| Technique | Minimal | Balanced | Dramatic |
|---|---|---|---|
| Card accent borders (`.card-accent`) | Yes | Yes | Yes |
| Badge labels (`.badge`) | Yes | Yes | Yes |
| Tight heading typography (`.tight-heading`) | Yes | Yes | Yes |
| Background grid (`.bg-grid`) | No | Yes | Yes |
| Staggered reveal animations (`.reveal`) | No | Yes | Yes |
| Section labels (`.section-label`) | No | Yes | Yes |
| Glow effects (`.glow`) | No | No | Yes |
| Glow pulse (`.glow-pulse`) | No | No | Yes |

**How to apply:**
1. Add `bg-grid` only when a technical or data-led tone benefits from it
2. Add `reveal` only to one related sequence of elements on a slide
3. Add `card-accent` or `card-top-accent` only where cards clarify grouping
4. Use `badge` classes for labels, step numbers, and status indicators
5. Add `glow` to one key accent element only for a dramatic deck
6. Use `tight-heading` on main headings for tighter letter-spacing
7. Use `inline-code` class for short code references in text (e.g., `FallbackModel(...)`)

See `references/style-guide.md` "Visual Depth Techniques" section for full details.

### Step 8: Code Slide Quality

When generating code slides:
1. Always specify the language class on `<code>` elements: `<code class="language-python">`
2. Call `Prism.highlightAll()` in the initialization script after DOM ready
3. Max 10-12 lines per code block - if more, split across slides
4. For inline code references (like `FallbackModel(...)` in a paragraph), use `<code class="inline-code">` - do NOT create a separate code block
5. Style code containers with proper padding, border-radius, and a code-appropriate background

See `references/code-highlighting.md` for Prism.js initialization requirements.

## Phase 5: Deliver

### Pre-Delivery Validation (MANDATORY)

Before writing the final HTML file, perform these checks. This takes 30 seconds and prevents silent visual regressions.

#### Check 1: Class Integrity

Scan every `class="..."` attribute in the generated HTML. For each class name:

- Is it in `viewport-base.css`? → OK
- Is it in a comparison template you used? → OK
- Is it defined in this presentation's `<style>` block? → OK
- Is it a standard class from a CDN library (e.g., Prism.js)? → OK
- **None of the above? → BUG.** Define the class in `<style>` or use the correct existing class name.

Common traps:

| Wrong (invented) | Fix |
|---|---|
| `section-label` | Available in `viewport-base.css` - use directly |
| `metric-card` | Define `.metric-card` in `<style>`, or use `.kpi-card` from KPI template |
| `slide-header` | Use `<h2>` element (already styled by viewport-base.css) |
| `highlight` | Define `.highlight` in `<style>` with specific styles |
| `content-box` | Use `.slide-content` or `.card` |

#### Check 2: Inline Style Audit

Count `style="` occurrences across all slides. Calculate per-slide average.

- **Target**: max ~3 inline styles per slide average
- **If over threshold**: Identify repeating patterns and extract to CSS classes
- **Common offenders**: `style="color: ..."`, `style="font-size: ..."`, `style="display: flex; gap: ..."`

#### Check 3: Repeating Pattern Detection

Search for any inline style value that appears on 3+ elements. Extract to a class:

- Three `style="font-size: 0.85rem; color: rgba(255,255,255,0.6)"` → `.muted-text` class
- Four `style="display: flex; gap: 1rem; align-items: center"` → `.flex-row .gap-md` or custom class
- Multiple `style="background: rgba(255,255,255,0.05); border-radius: 8px; padding: 1rem"` → `.surface-card` class

#### Check 4: Theme Variable Usage

Verify that custom CSS classes use theme variables, not hard-coded values:

- Colors: `var(--color-accent)` not `#3366cc`
- Spacing: `var(--spacing-md)` not `1.25rem`
- Fonts: `var(--font-mono)` not `'JetBrains Mono'`
- Radius: `var(--radius)` not `12px`

This ensures the presentation respects the chosen theme and can be re-themed by changing `:root` variables.

#### Check 5: Run the static fallback

Run `scripts/validate presentation.html`. It checks class integrity, inline-style density, and theme-variable references without requiring browser automation. When a browser is available, also capture two or three representative slides and inspect console errors and overflow before delivery.

#### Check 6: The presenter can reach their own notes

If the deck has a `speaker-notes` block, presenter mode must be wired, or the notes are unreachable during the talk and the presenter is left recalling from memory. Confirm both: the notes block covers every slide, and pressing `P` opens them. A `send` deck has no notes to reach because its context is on the slide face instead. Never ship notes with no way to open them.

### Output

1. Write the HTML file to the user's specified path (or suggest a reasonable filename like `presentation.html`)
2. Briefly mention:
   - How to open: "Open in any browser"
   - Keyboard shortcuts: "Use arrow keys to navigate, '?' for help"
   - PDF export: "Run `scripts/export-pdf presentation.html`; Browser Print > Save as PDF remains a fallback"
   - Presenter mode: "Press 'P' for presenter view with your speaker notes" whenever the deck ships notes. Say it plainly, because a presenter who does not know the notes are there gets no value from them.
3. Note the tech stack used: "Built with [Chart.js, Prism.js] via CDN"
4. State the reader and density the deck was built at, in one line ("Built diagram-led, for presenting live; press P for your notes"). It tells the user what to push back on if it reads wrong.

### Do NOT

- Do NOT ask for approval before writing the file - just generate it
- Do NOT explain every design decision - the user wants a presentation, not a design document
- Do NOT include unused libraries - only CDN scripts that are actually referenced

## Data Input Handling

### Inline Data

If the user provides numbers in their message, extract and structure them:
- "Revenue went from $2.1M to $2.8M" → bar/line chart data
- Table of values → appropriate chart type
- Percentages → pie/doughnut or bar chart

### JSON/CSV Data

If the user pastes or references structured data:
1. Parse the structure
2. Identify what maps to labels vs values
3. Choose the best chart type for the data shape
4. Generate the chart configuration

### Data Description

If the user describes data without specific numbers:
- In an interactive run, ask for the numbers and their source before plotting a chart.
- In a one-shot, non-interactive, subagent, or CI run, continue with clearly-labeled `SAMPLE DATA` only.
- Put a visible `SAMPLE DATA` badge on the chart slide and this speaker note: `SAMPLE DATA, replace before sharing`.
- Never present sample values as factual evidence or cite an invented source.

## Viewport Fitting - Critical Rules

These apply to EVERY slide in EVERY presentation:

- `.slide` has `height: 100vh; height: 100dvh; overflow: hidden;`
- ALL font sizes use `clamp(min, preferred, max)` - never fixed px/rem
- Images: `max-height: min(50vh, 400px); width: auto; object-fit: contain;`
- Charts: container `max-height: min(55vh, 420px)`
- Diagrams: container `max-height: min(60vh, 450px)`
- Code blocks: `max-height: min(55vh, 400px); overflow: hidden;`
- Include height breakpoints: @media (max-height: 700px), 600px, 500px
- Include `prefers-reduced-motion` support
- Include `@media print` styles that show every slide, hide navigation, and preserve backgrounds
- Never negate CSS functions directly - use `calc(-1 * clamp(...))`

**If content doesn't fit → split into multiple slides. Never scroll.**

## Inline Style Rules - Critical

These rules prevent the #1 cause of post-generation cleanup.

### When Inline Styles Are ACCEPTABLE

- **One-off positioning**: A single element needs `position: absolute; top: 15%; left: 60%`
- **Animation delays**: `style="--stagger-index: 3"` or `style="animation-delay: 0.3s"`
- **Dynamic computed values**: Chart container heights that depend on data count
- **SVG presentation attributes**: `fill`, `stroke`, `transform` inside `<svg>` elements

### When Inline Styles Are FORBIDDEN

- **Font size, color, padding, margin, gap, display** - Always use a class
- **Any property on 2+ elements** - If you write the same style twice, make it a class
- **Background colors on cards/containers** - Use a class with theme variable
- **Typography styling** (font-family, font-weight, text-transform, letter-spacing) - Always a class

### The 3-Strike Rule

Before writing `style="..."` on an element, check:

1. Does this property appear on any other element? → **Make a class**
2. Is this a standard layout property (display, flex, grid, gap, padding, margin)? → **Make a class**
3. Could this be expressed with a theme variable? → **Make a class**

If all three answers are "no", the inline style is acceptable.

### Generation Workflow for Custom Slide Types

When creating a new slide type (metric cards, section headers, tech stack grids, etc.):

1. **Define the CSS class(es) in `<style>` first**
2. Use theme variables (`var(--color-accent)`, `var(--spacing-md)`, etc.)
3. Apply the class in HTML
4. If multiple visual variants needed, use modifier classes (`.card.highlight`, `.step.active`)

## Accessibility

- Colorblind-safe palettes for ALL data visualization (Tier 1 always active)
- Semantic HTML: proper heading hierarchy, alt text for images
- Keyboard navigation: full keyboard support, visible focus indicators
- `prefers-reduced-motion`: disable all animations and transitions
- `@media print`: clean print output, one slide per page
- Sufficient color contrast (WCAG AA minimum)
- `aria-label` on interactive elements (chart canvases, nav buttons)

## Cross-Platform Notes

This skill works across AI coding tools. Some capabilities vary:

- **WebFetch available** (Claude Code, Gemini CLI): Can verify CDN URLs are current
- **WebFetch unavailable** (Codex CLI, Cursor): Use the pinned CDN URLs above - they are stable
- **Subagents available** (Claude Code): Can parallelize chart research and generation
- **Subagents unavailable** (most tools): Sequential generation works fine
- **Bash available** (all): Required for PPT conversion scripts and image processing
- **File reading** (all): Required for Mode C (enhancement) and reference file loading
