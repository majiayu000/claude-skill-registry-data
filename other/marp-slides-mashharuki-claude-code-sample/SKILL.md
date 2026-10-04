---
name: marp-slides
description: >
  Create professional, visually excellent presentation slides in Marp Markdown format.
  Use this skill when the user asks to:
  - Create a presentation, slides, deck, slideshow, or プレゼン / スライド
  - Write or generate slides about a specific topic
  - Make a Marp .md file for presenting
  Produces complete, ready-to-render .md files with embedded custom CSS theme, narrative
  structure, and polished visual design. Supports Japanese and English content.
---

# Marp Slides — Excellence Workflow

## Step 1 — Gather Requirements

Clarify before generating (infer from context when obvious):

| Field | Default if unspecified |
|---|---|
| Topic / title | Ask |
| Audience | General business |
| Purpose | Inform / present findings |
| Slide count | 12–15 |
| Language | Match user's language |
| Output path | `./slides.md` |

Ask concisely. For simple requests ("make slides about X"), infer and proceed.

## Step 2 — Plan the Narrative Arc

Before writing, sketch the arc:
```
Title → Agenda → Problem/Context → Body (3–5 slides) → Evidence → Summary → CTA → Ending
```

See `references/design-principles.md` for purpose-specific arc patterns and slide count guidelines.

## Step 3 — Generate the Marp File

### Required Frontmatter

```markdown
---
marp: true
theme: excel
paginate: true
size: 16:9
html: true
style: |
  /* [PASTE FULL CONTENTS OF assets/excel-theme.css HERE] */
---
```

Always embed the full CSS from `assets/excel-theme.css` in the `style:` block.
This makes the file self-contained and immediately renderable without external setup.

### Slide Class Usage

Apply per-slide with `<!-- _class: CLASS -->` immediately before the slide separator:

| Class | Use for |
|---|---|
| `title` | Cover slide — dark gradient, large H1 |
| `section` | Chapter break — blue background |
| `lead` | Key message — centered, large text |
| `dark` | Code showcase, dramatic emphasis |
| `ending` | Final slide — dark gradient, centered |
| *(none)* | Standard content slides |

### Layout Components

Use HTML `<div>` elements with these classes (requires `html: true`):

| Component | Class | Use for |
|---|---|---|
| Two columns | `.columns` | Side-by-side comparison |
| Three columns | `.columns.col-3` | Three options/features |
| Asymmetric cols | `.columns.col-6-4` or `.col-4-6` | Text + image/stat |
| Info card | `.card` `.card.accent/.warn/.success/.danger` | Categorized items |
| Key message box | `.highlight` | Single most important takeaway |
| Large metric | `.number` (or `.number.warm`) | KPI display |
| Tag / badge | `.tag` `.tag.warm/.success/.outline` | Tech stack, labels |
| Step list | `.steps` + `.step` | Numbered process |
| Icon row | `.icons` + `.icon-item` | Feature overview |
| Progress bar | `.progress` + `.progress-bar` | Status/roadmap |

See `references/layout-patterns.md` for copy-paste code examples of each.

### Content Quality Rules

- **1 idea per slide** — if a slide has two topics, split it
- **Max 5–6 bullets** per slide, each ≤12 words
- **`**Bold**` the key phrase** in each bullet (exactly one per bullet)
- **Vary visual types** — never 3+ consecutive all-bullet slides
- **Use `.highlight`** for the single most important message per section
- Write **real content**, not placeholders like "ここに説明を入れる"

See `references/design-principles.md` for full design guidance.

## Step 4 — Output

1. Write the complete `.md` file to the specified path (default: `./slides.md`)
2. Tell the user:
   - How to render: `npx @marp-team/marp-cli slides.md --html` (PDF/HTML)
   - VS Code: Install "Marp for VS Code", enable HTML in settings (`markdown.marp.enableHtml: true`)
3. Offer to adjust: slide count, language, style, or add specific sections

## Technical Notes

- `html: true` is required for layout components (`.columns`, `.card`, etc.)
- Without it, the HTML divs render as literal text — always include it
- For Tailwind CSS (advanced): add CDN script after frontmatter with `preflight: false`
- Mermaid diagrams: enable HTML and use `<div class="mermaid">...</div>`
