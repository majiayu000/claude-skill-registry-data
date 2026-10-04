---
name: marp-slides
description: Create, edit, review, preview, and export polished Marp Markdown slide decks in Canvas Notebook. Use when the user wants Markdown-native presentations, `.marp.md` or `.slides.md` files, version-controlled decks, Marp PDF/image/PPTX/HTML export, speaker notes, dashboard-style slides, data cards, or better looking decks that should remain close to plain text.
license: "MIT"
metadata:
  version: "1.2.0"
  upstream_reference: "https://github.com/robonuggets/marp-slides"
  adapted_for: "Canvas Notebook"
---

# Marp Slides

Create presentation decks as Marp Markdown files that Canvas Notebook can
preview and export. Use this skill when a Markdown-native deck is better than
directly authoring PowerPoint, Google Slides, or a custom HTML presentation.

## Canvas Output Contract

- Create or update a workspace file ending in `.marp.md` or `.slides.md`.
- Put valid YAML frontmatter at the very top of the file.
- Include `marp: true` in frontmatter; Canvas also detects `.marp.md` and
  `.slides.md` file names.
- Use plain `---` slide separators after frontmatter.
- Keep the source readable and easy to diff. Use HTML/CSS only when Markdown is
  not expressive enough.
- Use relative paths for local workspace images such as `./images/chart.png`.
  Canvas inlines supported workspace assets for preview/export when possible.
- Avoid absolute filesystem paths. They are brittle and may not resolve in the
  preview/export sandbox.
- Return the final deck path and mention export options only when relevant.

## Canvas Workflow

1. Decide whether Marp is the right target:
   - Use Marp for text-first decks, technical talks, client narratives,
     dashboards, reports, trainings, pitch drafts, and decks that should be
     easy to revise in Git.
   - Use the `pptx` skill when the user needs editable PowerPoint-native
     shapes, corporate templates, or heavy manual editing in PowerPoint.
   - Use `frontend-slides` when the user needs a standalone animated web
     presentation or custom runtime interaction.
2. Draft a compact outline before writing full slide copy.
3. Choose a concrete visual direction: executive memo, data dashboard,
   editorial report, workshop, classroom teaching, product launch, or investor
   brief.
4. Build the deck as a `.marp.md` / `.slides.md` file with frontmatter and a
   single `<style>` block near the top.
5. Keep every slide within a 16:9 viewport. Split overloaded slides instead of
   shrinking text.
6. Preview in Canvas and revise spacing, contrast, and overflow before final
   delivery.
7. Use Canvas Marp export actions/endpoints for PDF, images, PPTX, or HTML.
   Do not hand-roll a converter.

## Canvas-Safe HTML And CSS

Canvas allows common HTML layout tags, inline styles, tables, images, details,
summary, progress, abbr, and text formatting inside Marp. It does not allow
arbitrary raw SVG elements in user-authored Markdown. Marp itself renders slides
to SVG internally, but custom `<svg>` charts in Markdown may be sanitized.

Prefer Canvas-safe components:

- metric cards built from `<div>`, `<span>`, and CSS
- tables styled as compact scorecards
- CSS bar charts using flex rows and percentage widths
- progress bars with `<progress>`
- gauges or donuts as CSS `conic-gradient` blocks
- browser, terminal, chat, and timeline mockups made from HTML/CSS
- icons as text labels, emoji only if the deck tone allows it, or local images

If a requested chart truly needs SVG precision, create it as a local image asset
first, reference it with a relative path, then preview/export the deck.

## Required Starter Skeleton

Adapt this baseline to the user's brand, audience, and content.

```markdown
---
marp: true
theme: default
paginate: true
size: 16:9
title: "Presentation title"
description: "Short deck summary"
---

<style>
:root {
  --accent: #2563eb;
  --ink: #111827;
  --muted: #64748b;
  --bg: #f8fafc;
  --panel: #ffffff;
  --line: #e5e7eb;
}

section {
  font-family: "Aptos", "Helvetica Neue", Arial, sans-serif;
  color: var(--ink);
  background: var(--bg);
  padding: 56px 64px;
}

section.lead {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

h1 {
  font-size: 54px;
  line-height: 1.02;
}

h2 {
  font-size: 34px;
  line-height: 1.12;
}

p,
li {
  font-size: 23px;
  line-height: 1.35;
}

strong {
  color: var(--accent);
}

.kicker {
  color: var(--accent);
  font-size: 15px;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

.grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 18px;
}

.card {
  background: var(--panel);
  border: 1px solid var(--line);
  border-radius: 12px;
  padding: 20px;
}

.metric {
  font-size: 40px;
  font-weight: 800;
}

.muted {
  color: var(--muted);
}
</style>

<!-- _class: lead -->
<!-- _paginate: false -->

<div class="kicker">Context label</div>

# Presentation title

Short, specific promise for the audience.

---

## The point of this deck

- One clear idea per bullet.
- Keep bullets short.
- Split crowded slides.
```

## Visual Directions

Pick one direction and keep it consistent across the deck.

- Executive memo: quiet light theme, strong hierarchy, few colors, concise
  claims, tables and decision boxes.
- Data dashboard: dark or neutral theme, metric cards, trend rows, CSS bars,
  compact footnotes, clear units.
- Editorial report: large title type, generous whitespace, one strong image per
  section, pull quotes.
- Product launch: hero slides, comparison cards, capability rows, screenshots
  as real content.
- Workshop/training: section dividers, step cards, examples, recap slides.
- Investor brief: thesis title, market proof, risk table, milestones, ask.

Avoid generic one-note decks. Match typography, spacing, color, and image
treatment to the audience and subject matter.

## Component Patterns

### Metric Card

```html
<div class="card">
  <div class="muted">Qualified pipeline</div>
  <div class="metric">$4.2M</div>
  <div style="color:#16a34a;">+18% vs last quarter</div>
</div>
```

### CSS Bar Chart

```html
<div class="card">
  <div style="display:flex; justify-content:space-between;">
    <span>Enterprise</span><strong>72%</strong>
  </div>
  <div style="height:10px; background:#e5e7eb; border-radius:999px; overflow:hidden;">
    <div style="width:72%; height:100%; background:var(--accent);"></div>
  </div>
</div>
```

### CSS Donut / Gauge

```html
<div style="width:140px; height:140px; border-radius:50%;
  background:conic-gradient(var(--accent) 0 76%, #e5e7eb 76% 100%);
  display:grid; place-items:center;">
  <div style="width:88px; height:88px; border-radius:50%; background:var(--panel);
    display:grid; place-items:center; font-weight:800;">76%</div>
</div>
```

### Status Row

```html
<div class="card" style="display:flex; align-items:center; justify-content:space-between;">
  <span><span style="color:#16a34a;">●</span> CRM enrichment</span>
  <strong>Ready</strong>
</div>
```

### Terminal Mockup

```html
<div style="background:#0f172a; color:#dbeafe; border-radius:12px; padding:18px;
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size:18px;">
  <div style="color:#93c5fd;">$ canvas export deck.marp.md --pdf</div>
  <div>Rendered 14 slides in 3.2s</div>
</div>
```

### Details And Tooltips

Use sparingly; they work best in HTML preview and may not be meaningful in PDF.

```html
<details>
  <summary>Assumption details</summary>
  <p>Pipeline excludes renewal-only accounts.</p>
</details>

<abbr title="Customer acquisition cost">CAC</abbr>
```

## Image Rules

- Prefer local workspace images when the deck must export reliably.
- Use `![bg right:42% cover](./images/product.png)` for split slides.
- Use `![bg brightness:0.35](./images/hero.jpg)` for full-bleed image slides.
- Hide headers or page numbers on visual slides with local directives:
  `<!-- _header: "" -->` or `<!-- _paginate: false -->`.
- Do not use decorative stock-like images when the user needs product, data, or
  workflow clarity.
- Remote `https:` images can work in preview, but local copies are safer for
  repeatable export.

## Data And Chart Rules

- Put the takeaway in the slide title.
- Include units, time range, and source notes when data is shown.
- Prefer simple visual encodings over dense tables.
- Do not fake precision. Round numbers unless exact values matter.
- For multi-series data, use one accent color plus neutral supporting colors.
- If a chart is too complex for CSS/HTML, generate or save it as an image and
  embed it with a relative path.

## Speaker Notes

Use normal HTML comments for presenter notes. Do not confuse them with Marp
directives.

```markdown
<!--
Presenter note: pause here and ask which risk matters most to the team.
-->
```

## Export Guidance

Canvas Notebook provides Marp preview and export actions for Marp Markdown
files. Normal Marp PPTX export is visually faithful, but it is not guaranteed to
produce fully editable native PowerPoint objects. Use `pptx` instead when the
user requires PowerPoint-native editability.

HTML export preserves more interactive behavior than PDF/PPTX. PDF/images are
best for sharing fixed-layout decks.

## Quality Checks

- File name or frontmatter triggers Marp preview in Canvas.
- Frontmatter is valid YAML and appears at the top of the file.
- Slide separators are plain `---` lines.
- Slides fit 16:9 without clipped content.
- Text is readable at presentation distance.
- Contrast is high enough on every slide.
- Repeated elements use consistent placement and sizing.
- Local assets resolve with relative paths.
- PDF/PPTX/HTML export limitations are clear to the user.
