---
name: slidev
description: Create and edit markdown-based presentations using Slidev framework. Use when the user asks to create slides, presentations, or decks, or when working with .slides.md files. Supports mise/bun workflow, GitHub Pages publishing, and multi-deck landing pages.
license: MIT
compatibility: Requires mise, bun, and git. Designed for Claude Code, OpenCode, and similar agents.
metadata:
  author: kenny
  version: "1.0"
---

# Slidev Presentations

Create markdown-based slide decks using [Slidev](https://sli.dev) with mise for dev environment and bun as runtime.

## When to Use This Skill

- User asks to create a presentation or slide deck
- User wants to edit existing `.slides.md` files
- User needs to publish slides to GitHub Pages
- User mentions Slidev, slide decks, or presentations

## Project Structure

```
slides-repo/
├── mise.toml              # Dev environment (node, bun)
├── package.json
├── slides/                # All presentations
│   ├── topic-one.slides.md
│   └── topic-two.slides.md
├── scripts/
│   └── build-all.ts       # Builds decks + landing page
└── .github/workflows/
    └── publish.yml        # GitHub Pages deployment
```

## Commands

```bash
# Setup
mise install && bun install

# Development
mise run dev slides/my-deck.slides.md

# Create new deck
mise run new my-topic

# Build all + landing page
mise run build

# Preview
mise run preview
```

## Creating Slides

### Frontmatter

Every deck starts with YAML frontmatter:

```yaml
---
theme: default
title: Presentation Title
info: |
  Description shown in landing page
class: text-center
transition: slide-left
mdc: true
---
```

### Slide Separators

Use `---` between slides:

```markdown
---
# First Slide

Content here

---
# Second Slide

More content
```

### Per-Slide Config

```yaml
---
layout: center
class: text-center
---
```

## Layouts

| Layout | Use Case |
|--------|----------|
| `default` | Standard content |
| `cover` | Title slides |
| `center` | Centered content |
| `two-cols` | Side-by-side |
| `image-right` | Content + image |
| `image` | Full-bleed image |

### Two Columns

```markdown
---
layout: two-cols
---

# Left

Content

::right::

# Right

Content
```

## Interactive Features

### Progressive Reveal

```html
<v-clicks>

- First point
- Second point
- Third point

</v-clicks>
```

### Code Highlighting

````markdown
```ts {1|3|1-3}
const a = 1
const b = 2
const c = a + b
```
````

Lines in `{1|3|1-3}` animate step-by-step.

### Speaker Notes

```markdown
---
# Slide Title

Content

<!--
Speaker notes here.
Press 'p' for presenter mode.
-->
```

## Styling

Slidev uses UnoCSS (Tailwind-compatible):

```html
<div class="text-3xl font-bold text-blue-500">Styled text</div>
<div class="grid grid-cols-2 gap-4">Grid</div>
```

## Publishing to GitHub Pages

The included workflow auto-deploys on push to `main`:

1. Builds all `slides/*.slides.md` files
2. Generates landing page with links to each deck
3. Deploys to GitHub Pages

### First-Time Setup

1. Go to repo Settings → Pages
2. Set Source to "GitHub Actions"

## Examples

### Create a new presentation

```
User: Create a presentation about our Q4 roadmap
Agent: Creates slides/q4-roadmap.slides.md with cover, agenda, and content slides
```

### Add slides to existing deck

```
User: Add a slide about the new API to my slides
Agent: Edits the .slides.md file, adding a new slide section
```

### Publish slides

```
User: Deploy my slides to GitHub Pages
Agent: Runs mise run build, commits to main, triggers workflow
```

## Guidelines

- Keep one concept per slide
- Use `v-clicks` for progressive disclosure
- Add speaker notes for talking points
- Name files descriptively: `2024-q4-roadmap.slides.md`
- Use 2-3 consistent layouts per deck

## Resources

- [Slidev Docs](https://sli.dev/)
- [Themes](https://sli.dev/resources/theme-gallery)
- [UnoCSS](https://unocss.dev/)
