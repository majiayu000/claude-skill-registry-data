---
name: visual-page-builder
description: Generate beautiful self-contained HTML pages that explain any concept visually
---

# Visual Page Builder

Generate a polished, self-contained HTML page that explains any concept using visual components. No frameworks, no dependencies, no build step. One file that looks like a real product page.

## Page Types

| Type | Best for | Key components |
|------|----------|---------------|
| **Architecture Overview** | Systems, tech stacks, infrastructure | Flow diagram, connection lines, component cards |
| **Comparison Table** | Tool vs tool, plan vs plan, before vs after | Side-by-side grids, checkmarks, highlight winner |
| **Process Flow** | Tutorials, onboarding, how-to guides | Numbered steps, arrows, status indicators |
| **Timeline** | Roadmaps, project history, changelogs | Vertical timeline, date markers, milestone cards |
| **Dashboard** | Metrics, KPIs, performance summaries | Stat cards, bar charts, progress rings |
| **Concept Explainer** | Abstract ideas, frameworks, mental models | Analogy visuals, layered diagrams, callout boxes |
| **Project Recap** | End-of-project summaries, case studies | Before/after, stats, testimonial cards, gallery |

Ask the user which type fits their content, or auto-detect from their description.

## Workflow

### Step 1: Gather Content

Ask the user for:
- **Title** of the page
- **3-6 sections** they want to cover (or let you suggest based on the topic)
- **Key data points** (numbers, stats, comparisons)
- **Relationships** between concepts (what connects to what)
- **Hierarchy** (what is most important, what is supporting detail)

If the user provides a document, transcript, or notes, extract these elements automatically and confirm.

### Step 2: Plan the Layout

Map each section to a visual component (see Visual Components below). Present the plan:

```
Section 1: "What is X" -> Concept card with icon + 3 key points
Section 2: "How it works" -> 4-step process flow with arrows
Section 3: "Performance" -> Stat cards (3 across) + comparison grid
Section 4: "Get started" -> Callout box with CTA
```

Get user approval before building.

### Step 3: Build the HTML

Generate a single self-contained HTML file.

**Design System:**

| Token | Value |
|-------|-------|
| Background | `#0f0f10` |
| Surface | `#1a1a1d` |
| Surface border | `#2a2a2d` |
| Text primary | `#ffffff` |
| Text secondary | `#a0a0a0` |
| Accent | `#D97757` (or user-chosen) |
| Accent muted | `rgba(217, 119, 87, 0.15)` |
| Font | Inter via Google Fonts, fallback `system-ui, sans-serif` |
| Max width | `1000px` |
| Card radius | `12px` |
| Section spacing | `80px` vertical |

**Visual Components Available:**

| Component | When to use | Structure |
|-----------|-------------|-----------|
| **Stat cards** | Key numbers | Horizontal row, large number + label + optional trend arrow |
| **Section cards** | Feature lists, grouped info | Grid of cards with icon/emoji, title, description |
| **Comparison grid** | Side-by-side analysis | 2-3 columns, rows with checkmarks or values |
| **Flow steps** | Sequential processes | Numbered circles connected by lines, title + description |
| **Status badges** | Tags, categories, states | Colored pill badges (green/yellow/red/blue) |
| **Code blocks** | Technical content, configs | Dark bg, monospace font, syntax-highlighted if applicable |
| **Callout boxes** | Important notes, warnings, tips | Accent left border, icon, highlighted background |
| **Progress bars** | Completion, capacity, scores | Horizontal bar with fill percentage and label |
| **Tables** | Structured data, specs | Striped rows, sticky header, responsive scroll |
| **Timelines** | Chronological events | Vertical line with dots, alternating left/right cards |
| **Quote blocks** | Testimonials, key statements | Large quotation mark, italic text, attribution |
| **Icon grids** | Feature overviews, tool lists | 2-3 column grid with emoji + title + one-line desc |

### Step 4: Save and Preview

Save the file as `[topic-slug]-visual.html` in the current working directory.

Open in the default browser:
```bash
open [topic-slug]-visual.html
```

### Step 5: Iterate

Ask: "How does it look? I can adjust colors, swap components, add sections, or change any text."

Common tweaks:
- Change accent color
- Add or remove sections
- Swap a component type (e.g., table to comparison grid)
- Adjust text content
- Add a logo or header image (base64 inline)

## Rules

- **Every section needs a visual component.** No section should be just a wall of text. If there is no obvious visual, use a callout box or icon grid.
- **Max 50 words before a visual.** Introductory text for a section must be short. Let the visual do the heavy lifting.
- **All CSS and JS inline.** Zero external dependencies. The file must work when double-clicked from the desktop with no server.
- **Zero external fetches required.** Google Fonts is the one allowed exception (with system font fallback). Everything else is inline.
- **Responsive.** Must look good on mobile (stack grids to single column, scale stat cards, scrollable tables).
- **No JavaScript required for content.** JS is only for optional enhancements (smooth scroll, fade-in animations). The page must be fully readable with JS disabled.
- **Consistent spacing.** Use the design system tokens. Do not eyeball padding or margins.
- **Dark theme only.** Do not offer a light mode. The dark palette is part of the brand.
- **Accessible.** Sufficient color contrast (WCAG AA minimum), semantic HTML, alt text on images.
- Keep the total file under 500KB. If inlining images, compress them first.
- The page title should appear in the browser tab (title tag).
