---
name: site-dev
description: |
  Development skill for rohanverma.net Zola static site.
  Use when: editing styles, fixing responsive issues, adding pages, modifying templates.
  Keywords: zola, scss, css, mobile, responsive, template, design, theme, blog, project.
---

# Site Development

> **Philosophy:** Developer's Notebook (light) × Vintage Terminal (dark)
> Minimal, functional, memorable. Monospace everything.

## Quick Reference

| Task | Location |
|------|----------|
| Colors/tokens | `sass/tokens/_variables.scss` |
| Mobile fixes | `sass/utilities/_mobile.scss` |
| Header/nav | `sass/layout/_header.scss` |
| Components | `sass/components/` |
| Templates | `templates/` |
| Config | `config.toml` |

## Design System

### Colors

**Light Mode (Notebook Ink):**
```
Text:   #1e1e1e → #525252 → #737373
Paper:  #f7f5f0 (cream) | #eae7df (shadow)
Accent: #1a4d7a (blue-black ink)
Lines:  #e8a5a5 (red margin) | rgba(180,160,140,0.25) (ruled)
```

**Dark Mode (Amber Terminal):**
```
Text:   #ffb000 → #ff9500 → #cc7a00
Screen: #000000 (pure black)
Accent: #ffcc00 (bright amber)
FX:     text-shadow glow + scanlines + flicker
```

**Indian Palette (accents):**
- `--c-saffron: #FF9933`
- `--c-marigold: #EAA221`
- `--c-peacock: #006D77`
- `--c-accent: #c44536` (terracotta)

### Typography

```scss
Display: "Courier Prime"     // Typewriter headings
Body:    "IBM Plex Mono"     // Refined monospace
Never:   Inter, Roboto, Arial, System fonts
```

Rules: All monospace, line-height 1.8, letter-spacing -0.02em on headings, blinking cursor `▌` after h1.

### Signature Elements

**Notebook (Light):** Red margin at 60px, ruled lines, hole punches, post-it notes, notebook tape on avatar.

**Terminal (Dark):** CRT scanlines, text glow, flicker animation, terminal window with `● ● ●`, amber phosphor (NOT green).

### Icons

**Library:** Lucide Icons (https://lucide.dev)
- `pen-line` - Writing/Blog
- `flask-conical` - Projects
- `train-front` - Travel

## Responsive Breakpoints

| Breakpoint | Target |
|------------|--------|
| max-width: 400px | Small mobile |
| max-width: 640px | Mobile (nav hides) |
| max-width: 768px | Mobile overrides |
| 769px-1024px | Tablet |

**Critical:** Nav hides at 640px. JS toggles `.mobile-menu-open` (not `.active`).

## Gotchas

**Selector Specificity:**
```scss
// WRONG - breaks tags
a, button { display: inline-flex }

// CORRECT
a:not(.tag):not(.tag-item), button { min-height: 44px; }
```

**Tera Conditionals:**
```jinja
{# WRONG - fails if undefined #}
{% if page.extra.status == 'archived' %}

{# CORRECT #}
{% if page.extra.status is defined and page.extra.status == 'archived' %}
```

**CSS Variables:** Always check `_variables.scss` before using. Legacy aliases: `--space-xs/sm/md/lg/xl`.

## Zola Config Patterns

```toml
[extra]
avatar = "/images/avatar.jpg"
handwritten_font = "https://fonts.googleapis.com/css2?family=Shrikhand&display=swap"
commento_src = "https://commento.rohanverma.net/js/commento.js"

[[extra.menu_main]]
name = "Blog"
url = "/blog/"
weight = 2

[extra.fathom_analytics]
site_id = "REDBQ"
server_url = "fathom.rohanverma.net"

[extra.now]
items = ["Item 1", "Item 2"]
```

Access: `{{ config.extra.avatar }}`, `{{ config.extra.menu_main }}`

## Frontmatter

**Blog:**
```toml
+++
title = "Post Title"
date = 2026-01-03
description = "SEO description"
[taxonomies]
tags = ["tag1", "tag2"]
+++
```

**Project:**
```toml
+++
title = "Project"
weight = 1
[extra]
github_url = "https://github.com/..."
demo_url = "https://..."  # optional
status = "archived"       # optional
+++
```

## Writing Style

- First-person, pragmatic voice
- Simple sentences, no em-dashes
- Real examples over theory

## Build

```bash
zola serve   # Development
zola build   # Production
```

## Directory Structure

```
sass/
├── tokens/_variables.scss    # Design tokens
├── base/                     # Reset, typography
├── components/               # Cards, tags, buttons
├── layout/                   # Header, footer
├── utilities/
│   ├── _mobile.scss          # @media overrides
│   └── _helpers.scss         # Utilities
└── pages/                    # Page-specific

templates/
├── base.html                 # Theme toggle, scripts
├── blog.html, blog-page.html
└── projects-*.html
```

## Related Docs

- `DESIGN.md` - Full design system
- `DESIGN_PATTERNS.md` - Visual examples
- `DESIGN_DECISIONS.md` - Philosophy
- `AGENTS.md` - Workflow
