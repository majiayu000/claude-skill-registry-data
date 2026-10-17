---
name: diagram-design-editorial
description: Create editorial-quality diagrams in HTML + SVG matching your brand — architecture, flowcharts, sequences, timelines, quadrants, and 9 more types.
triggers:
  - "create a diagram"
  - "make an architecture diagram"
  - "build a flowchart"
  - "generate a sequence diagram"
  - "design a timeline"
  - "create a quadrant chart"
  - "make an org chart"
  - "build a state machine diagram"
---

# Diagram Design — Editorial Diagrams

> Skill by [ara.so](https://ara.so) — Design Skills collection.

Editorial-quality diagrams that match your brand. Fourteen diagram types (architecture, flowchart, sequence, state machine, ER, timeline, swimlane, quadrant, nested, tree, org chart, venn, layers, pyramid) shipped as self-contained HTML + SVG files. No build step, no shadows, no generic rounded boxes.

The skill reads your website and extracts colors + fonts, then applies them across every diagram. Your site's paper color becomes the diagram background. Your CTA color becomes the focal accent. Your body font becomes the node label family.

## Installation

```bash
# Clone and symlink into Claude Code's skills directory
git clone git@github.com:cathrynlavery/diagram-design.git ~/code/diagram-design
ln -s ~/code/diagram-design/skills/diagram-design ~/.claude/skills/diagram-design
```

Restart Claude Code. The skill registers as `diagram-design`.

**Alternative (plugin install):**
```
/plugin marketplace add cathrynlavery/diagram-design
/plugin install diagram-design@diagram-design
```

**For Codex:**
```bash
npx skills add https://github.com/cathrynlavery/diagram-design --skill diagram-design
```

## Brand Onboarding (60 seconds)

Out of the box, diagrams use a clean default palette (jet-black + atomic-tangerine). To apply your brand:

```
You:     "onboard diagram-design to https://yoursite.com"
Claude:  → fetches homepage
         → extracts dominant palette + font stack
         → maps to semantic roles (paper, ink, muted, accent)
         → shows proposed diff
         → writes to references/style-guide.md
You:     "apply it"
```

**What gets extracted:**

| From your site | Becomes |
|---|---|
| `<body>` background | `paper` token |
| Primary text color | `ink` token |
| Secondary text | `muted` token |
| Cards/containers | `paper-2` token |
| Brand color (CTA/link) | `accent` token |
| `<h1>` font | `title` font |
| `<body>` font | `node-name` font |
| `<code>` font | `sublabel` font |

Contrast checks run automatically (WCAG AA). If a color fails at diagram sizes (9–12px), the skill proposes an adjusted value.

**Manual override:** Edit `skills/diagram-design/references/style-guide.md` directly.

## Creating Diagrams

### Quick Start

Just ask Claude to make a diagram — it will pick the right type:

```
"Make an architecture diagram of my app: frontend, backend, database, Redis cache."
"I need a quadrant showing Q2 projects by impact vs effort."
"Give me a sequence diagram of the OAuth handshake."
"Create a timeline of our product milestones."
```

Claude will:
1. Choose the appropriate diagram type
2. Build the HTML + SVG
3. Save it as a self-contained file
4. Apply your brand tokens from `style-guide.md`

### The 14 Diagram Types

| Type | Use for |
|---|---|
| **Architecture** | Components + connections |
| **Flowchart** | Decision logic |
| **Sequence** | Messages over time |
| **State machine** | States + transitions |
| **ER / data model** | Entities + fields |
| **Timeline** | Events on an axis |
| **Swimlane** | Cross-functional flow |
| **Quadrant** | Two-axis positioning |
| **Nested** | Hierarchy by containment |
| **Tree** | Parent → children |
| **Org chart** | Ownership + routing |
| **Venn** | Set overlap |
| **Layers** | Stacked abstractions |
| **Pyramid / funnel** | Ranked hierarchy or drop-off |

**Bonus:** Consultant 2×2 (scenario matrix with named cells)

### Template Scaffolds

Start from a template:

```bash
# Minimal light variant
cp assets/template.html my-diagram.html

# Full editorial with summary cards
cp assets/template-full.html my-diagram.html
```

Each template is self-contained HTML with inline SVG and CSS.

## Working Code Examples

### Example 1: Architecture Diagram

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>App Architecture</title>
  <style>
    :root {
      --paper: #FEFEFE;
      --ink: #1A1A1A;
      --accent: #EB6C36;
      --muted: #64748B;
      --hairline: #D1D5DB;
    }
    body {
      margin: 0;
      padding: 48px;
      background: var(--paper);
      font-family: 'Geist', -apple-system, sans-serif;
    }
    svg {
      display: block;
      max-width: 100%;
      height: auto;
    }
  </style>
</head>
<body>
  <svg viewBox="0 0 800 600" xmlns="http://www.w3.org/2000/svg">
    <!-- Frontend node (focal, coral tint) -->
    <rect x="100" y="100" width="160" height="80" 
          fill="#FFF5F0" stroke="var(--accent)" stroke-width="2" rx="8"/>
    <text x="180" y="145" text-anchor="middle" 
          font-size="14" font-weight="500" fill="var(--ink)">
      Frontend
    </text>
    
    <!-- Backend node -->
    <rect x="100" y="260" width="160" height="80"
          fill="var(--paper)" stroke="var(--hairline)" stroke-width="1" rx="8"/>
    <text x="180" y="305" text-anchor="middle"
          font-size="14" font-weight="500" fill="var(--ink)">
      Backend API
    </text>
    
    <!-- Database node -->
    <rect x="400" y="260" width="160" height="80"
          fill="var(--paper)" stroke="var(--hairline)" stroke-width="1" rx="8"/>
    <text x="480" y="305" text-anchor="middle"
          font-size="14" font-weight="500" fill="var(--ink)">
      PostgreSQL
    </text>
    
    <!-- Connection lines -->
    <path d="M 180 180 L 180 260" stroke="var(--muted)" 
          stroke-width="1" fill="none" stroke-dasharray="4 4"/>
    <path d="M 260 300 L 400 300" stroke="var(--muted)"
          stroke-width="1" fill="none" stroke-dasharray="4 4"/>
    
    <!-- Labels on connections -->
    <text x="190" y="220" font-size="10" fill="var(--muted)"
          font-family="'Geist Mono', monospace">
      HTTPS
    </text>
    <text x="310" y="290" font-size="10" fill="var(--muted)"
          font-family="'Geist Mono', monospace">
      SQL
    </text>
  </svg>
</body>
</html>
```

### Example 2: Flowchart

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Decision Flow</title>
  <style>
    :root {
      --paper: #FEFEFE;
      --ink: #1A1A1A;
      --accent: #EB6C36;
      --muted: #64748B;
      --hairline: #D1D5DB;
    }
    body {
      margin: 0;
      padding: 48px;
      background: var(--paper);
      font-family: 'Geist', -apple-system, sans-serif;
    }
  </style>
</head>
<body>
  <svg viewBox="0 0 600 800" xmlns="http://www.w3.org/2000/svg">
    <!-- Start node (pill shape) -->
    <rect x="220" y="40" width="160" height="48"
          fill="var(--ink)" rx="24"/>
    <text x="300" y="68" text-anchor="middle"
          font-size="12" font-weight="500" fill="var(--paper)">
      Start
    </text>
    
    <!-- Decision node (diamond) -->
    <path d="M 300 160 L 380 220 L 300 280 L 220 220 Z"
          fill="var(--paper)" stroke="var(--hairline)" stroke-width="1"/>
    <text x="300" y="225" text-anchor="middle"
          font-size="12" fill="var(--ink)">
      Valid user?
    </text>
    
    <!-- Process nodes -->
    <rect x="420" y="196" width="140" height="48"
          fill="var(--paper)" stroke="var(--hairline)" stroke-width="1" rx="8"/>
    <text x="490" y="224" text-anchor="middle"
          font-size="12" fill="var(--ink)">
      Grant access
    </text>
    
    <rect x="40" y="196" width="140" height="48"
          fill="#FFF5F0" stroke="var(--accent)" stroke-width="2" rx="8"/>
    <text x="110" y="224" text-anchor="middle"
          font-size="12" fill="var(--ink)">
      Show error
    </text>
    
    <!-- Arrows -->
    <path d="M 300 88 L 300 160" stroke="var(--muted)" 
          stroke-width="1" marker-end="url(#arrowhead)"/>
    <path d="M 380 220 L 420 220" stroke="var(--muted)"
          stroke-width="1" marker-end="url(#arrowhead)"/>
    <path d="M 220 220 L 180 220" stroke="var(--accent)"
          stroke-width="1" marker-end="url(#arrowhead-accent)"/>
    
    <!-- Arrow markers -->
    <defs>
      <marker id="arrowhead" markerWidth="6" markerHeight="6"
              refX="5" refY="3" orient="auto">
        <polygon points="0 0, 6 3, 0 6" fill="var(--muted)"/>
      </marker>
      <marker id="arrowhead-accent" markerWidth="6" markerHeight="6"
              refX="5" refY="3" orient="auto">
        <polygon points="0 0, 6 3, 0 6" fill="var(--accent)"/>
      </marker>
    </defs>
    
    <!-- Labels -->
    <text x="390" y="210" font-size="10" fill="var(--muted)">Yes</text>
    <text x="190" y="210" font-size="10" fill="var(--accent)">No</text>
  </svg>
</body>
</html>
```

### Example 3: Timeline

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Product Timeline</title>
  <style>
    :root {
      --paper: #FEFEFE;
      --ink: #1A1A1A;
      --accent: #EB6C36;
      --muted: #64748B;
      --hairline: #D1D5DB;
    }
    body {
      margin: 0;
      padding: 48px;
      background: var(--paper);
      font-family: 'Geist', -apple-system, sans-serif;
    }
  </style>
</head>
<body>
  <svg viewBox="0 0 900 300" xmlns="http://www.w3.org/2000/svg">
    <!-- Timeline axis -->
    <line x1="100" y1="150" x2="800" y2="150"
          stroke="var(--hairline)" stroke-width="1"/>
    
    <!-- Event 1 (focal) -->
    <circle cx="200" cy="150" r="8" fill="var(--accent)"/>
    <text x="200" y="120" text-anchor="middle"
          font-size="12" font-weight="500" fill="var(--ink)">
      Beta Launch
    </text>
    <text x="200" y="180" text-anchor="middle"
          font-size="10" fill="var(--muted)"
          font-family="'Geist Mono', monospace">
      Jan 2024
    </text>
    
    <!-- Event 2 -->
    <circle cx="400" cy="150" r="6" fill="var(--muted)"/>
    <text x="400" y="120" text-anchor="middle"
          font-size="12" fill="var(--ink)">
      Feature X
    </text>
    <text x="400" y="180" text-anchor="middle"
          font-size="10" fill="var(--muted)"
          font-family="'Geist Mono', monospace">
      Mar 2024
    </text>
    
    <!-- Event 3 -->
    <circle cx="600" cy="150" r="6" fill="var(--muted)"/>
    <text x="600" y="120" text-anchor="middle"
          font-size="12" fill="var(--ink)">
      Public GA
    </text>
    <text x="600" y="180" text-anchor="middle"
          font-size="10" fill="var(--muted)"
          font-family="'Geist Mono', monospace">
      May 2024
    </text>
  </svg>
</body>
</html>
```

## Design System Rules

Every diagram follows these constraints (enforced in all 14 type references):

### Grid & Spacing
- All coordinates, widths, gaps divisible by **4** (non-negotiable)
- Base unit: 4px
- Typical node padding: 16px
- Gap between nodes: 40px minimum
- Margin from edge: 48px

### Colors
- **One accent color** — used for 1–2 focal elements only
- Coral-tinted focal nodes: `#FFF5F0` fill + `accent` stroke
- Non-focal nodes: `paper` fill + `hairline` stroke
- Connection lines: `muted` (solid or dashed)

### Typography
- **Instrument Serif** — titles + italic editorial callouts
- **Geist Sans** — node names, labels
- **Geist Mono** — technical sublabels (ports, URLs, field types)
- Font sizes: 10px (sublabel), 12px (label), 14px (node name), 18px (title)

### Shapes
- Max border-radius: **10px** (8px typical for nodes)
- Border width: 1px (hairline), 2px (focal)
- No shadows, no gradients, no blur effects

### Density
- Target density: **4/10** — every node earns its place
- Show 5–9 primary nodes
- Sublabels only when they add clarity (ports, field types, conditions)

## Configuration

All style tokens live in `skills/diagram-design/references/style-guide.md`:

```markdown
| Role       | Token        | Light default | Dark default  |
|------------|--------------|---------------|---------------|
| Background | `paper`      | `#FEFEFE`     | `#0F0F0F`     |
| Primary    | `ink`        | `#1A1A1A`     | `#E5E5E5`     |
| Accent     | `accent`     | `#EB6C36`     | `#F97316`     |
| Muted      | `muted`      | `#64748B`     | `#94A3B8`     |
| Hairline   | `hairline`   | `#D1D5DB`     | `#334155`     |
| Card       | `paper-2`    | `#F8F9FA`     | `#1A1A1A`     |
```

**Font stack:**

```markdown
| Role       | Family                                      |
|------------|---------------------------------------------|
| Title      | 'Instrument Serif', Georgia, serif          |
| Node name  | 'Geist', -apple-system, sans-serif          |
| Sublabel   | 'Geist Mono', 'SF Mono', Consolas, monospace|
```

Edit this file to override tokens globally, or run `onboard diagram-design to <url>` to extract from a website.

## Common Patterns

### Adding Editorial Annotations

Italic callouts that sit in the margins:

```
"Add an annotation to this diagram explaining why Redis sits between the backend and database."
```

Claude will insert:

```html
<!-- Annotation callout -->
<text x="520" y="340" font-size="11" font-style="italic"
      font-family="'Instrument Serif', Georgia, serif" fill="var(--muted)">
  Redis caches hot queries,
</text>
<text x="520" y="356" font-size="11" font-style="italic"
      font-family="'Instrument Serif', Georgia, serif" fill="var(--muted)">
  reducing DB load by 70%.
</text>
<!-- Dashed leader to relevant node -->
<path d="M 500 300 Q 510 320, 515 335" stroke="var(--muted)"
      stroke-width="1" stroke-dasharray="2 3" fill="none"/>
```

### Hand-Drawn Variant (Sketchy Filter)

```
"Make this diagram look hand-drawn."
```

Applies SVG filters for rough edges:

```html
<defs>
  <filter id="sketchy">
    <feTurbulence type="fractalNoise" baseFrequency="0.05" numOctaves="2" result="noise"/>
    <feDisplacementMap in="SourceGraphic" in2="noise" scale="2"/>
  </filter>
</defs>

<!-- Apply to shapes -->
<rect x="100" y="100" width="160" height="80" filter="url(#sketchy)" ... />
```

### Dark Mode Variant

All templates include CSS custom properties. To generate a dark variant:

```
"Create a dark mode version of this diagram."
```

Claude will swap tokens:

```css
:root {
  --paper: #0F0F0F;
  --ink: #E5E5E5;
  --accent: #F97316;
  --muted: #94A3B8;
  --hairline: #334155;
}
```

### Consultant 2×2 Quadrant

Named scenario matrix (4 cells, each with a label):

```
"Make a 2x2 showing product strategy: differentiation vs cost, and broad vs niche market."
```

Generates quadrant with named cells:

```html
<!-- Top-left cell -->
<rect x="100" y="100" width="300" height="200"
      fill="#FFF5F0" stroke="var(--accent)" stroke-width="2" rx="8"/>
<text x="250" y="190" text-anchor="middle"
      font-size="14" font-weight="500" fill="var(--ink)">
  Premium Niche
</text>
<text x="250" y="210" text-anchor="middle"
      font-size="10" fill="var(--muted)">
  High margin, focused
</text>
```

## Browsing the Gallery

Open the live gallery to see all 14 types with light/dark/editorial tabs:

```bash
open ~/.claude/skills/diagram-design/assets/index.html
```

Or from the repo root:

```bash
open skills/diagram-design/assets/index.html
```

Each example includes three variants:
- **Minimal Light** — `template.html` scaffold
- **Minimal Dark** — dark mode tokens
- **Full Editorial** — `template-full.html` with annotation callouts

## Troubleshooting

### "Diagram looks generic / AI-generated"

**Cause:** Coordinates or gaps not divisible by 4, or too many accent colors.

**Fix:** Check the SVG for non-4-divisible x/y/width/height. Ensure only 1–2 nodes have the accent stroke.

### "Fonts not loading"

**Cause:** Font families require web fonts (Geist, Instrument Serif).

**Fix:** Add to `<head>`:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet">
```

For Geist, use the Vercel CDN or local files:

```html
<link href="https://cdn.jsdelivr.net/npm/@vercel/style-guide@latest/fonts/geist.css" rel="stylesheet">
```

### "Onboarding failed — no colors extracted"

**Cause:** Target site uses inline styles or CSS-in-JS that isn't in the DOM on initial load.

**Fix:** Manually set tokens in `references/style-guide.md`:

```markdown
| Role   | Token    | Value     |
|--------|----------|-----------|
| paper  | `paper`  | `#FFFFFF` |
| ink    | `ink`    | `#000000` |
| accent | `accent` | `#FF6B35` |
```

### "Contrast check failed"

**Cause:** Extracted ink color fails WCAG AA at small sizes (9–12px).

**Fix:** The skill auto-adjusts and shows a proposed value. Accept it, or override in `style-guide.md`.

### "Diagram type not recognized"

**Cause:** Request didn't match one of the 14 types.

**Fix:** Be explicit:

```
"Make a sequence diagram of the login flow."
"Create an architecture diagram showing microservices."
"Build a quadrant chart for prioritization."
```

See the selection guide in `SKILL.md` for triggers.

## Environment Variables

If deploying diagrams to a server that applies tokens via env vars:

```bash
export DIAGRAM_PAPER="#FEFEFE"
export DIAGRAM_INK="#1A1A1A"
export DIAGRAM_ACCENT="#EB6C36"
```

Then reference in HTML:

```html
<style>
  :root {
    --paper: ${DIAGRAM_PAPER};
    --ink: ${DIAGRAM_INK};
    --accent: ${DIAGRAM_ACCENT};
  }
</style>
```

(Most users will edit `style-guide.md` directly instead.)

## Advanced Usage

### Exporting as PNG

Diagrams are self-contained HTML. To export as PNG:

```bash
# Using headless Chrome
npx playwright screenshot my-diagram.html my-diagram.png --full-page

# Or manually: open in browser, screenshot at 2x zoom for retina
```

### Embedding in Markdown

Use an `<iframe>` or convert to data URI:

```markdown
![Architecture](data:image/svg+xml;base64,...)
```

Or link directly:

```markdown
![Architecture](./diagrams/architecture.html)
```

### Custom Diagram Type

To add a 15th type:

1. Create `references/type-custom.md` with the same structure as existing types
2. Add selection trigger to `SKILL.md`:
   ```markdown
   - **Custom diagram** — <use case>
     - Trigger: "create a custom diagram"
   ```
3. Drop an example in `assets/example-custom.html`

Claude will auto-load the reference when triggered.

---

**License:** MIT  
**Repo:** [github.com/cathrynlavery/diagram-design](https://github.com/cathrynlavery/diagram-design)  
**Gallery:** `skills/diagram-design/assets/index.html`
