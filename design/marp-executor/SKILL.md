---
name: marp-executor
type: executor
description: "Execute Marp slide deck generation from presentation specs."
version: 0.1.0
---

# Marp Executor Skill

## When to Use

**Primary triggers:**
- "make slides", "create a presentation", "build a deck"
- "generate slides from this plan", "turn this into a presentation"
- "marp slides", "markdown slides", "presentation from this content"
- User has content (plan, report, outline) and wants slides produced
- User describes a presentation topic and wants a slide deck

---

## Use When

- You need a slide deck from an outline, plan, report, or direct description
- You want presentation-as-code (Marp markdown → HTML/PDF/PPTX)
- You need slides that render in browser with no build step (HTML output)
- You want to iterate on slides in markdown and re-render
- You need speaker notes embedded in the deck

---

## Do Not Use When

- You need a rich interactive HTML page (not slides) — use `generate-slides` or `frontend-design` instead
- You need a data visualization — use `dataviz-executor`
- You need to **review** an existing presentation — use `copy-critic` or `proposal-critic`
- You need a Google Slides or Keynote file — Marp exports to PPTX which can be opened in those tools
- You need complex animations or video embedding — Marp is intentionally minimal

---

## Resolution Paths

| Situation | Route |
|-----------|-------|
| Have content/outline, need slides | This skill — generates Marp markdown + renders |
| Need interactive HTML page, not slides | Use `generate-slides` or `frontend-design` |
| Need a chart in the slides | Use `dataviz-executor` first, then reference the chart |
| Need to review slide content quality | Use `copy-critic` on the markdown source |

---

## What You Get

- **Marp markdown file** (.md) with frontmatter, slide breaks, speaker notes
- **Rendered output** in one or more formats: HTML (default), PDF, PPTX
- **Theme** applied: built-in (default, gaia, uncover) or custom CSS
- **Deviation log** if output differs from input spec

---

## Output Formats

| Format | Flag | Best For |
|--------|------|----------|
| HTML | (default) | Browser viewing, sharing links, no install needed |
| PDF | `--pdf` | Printing, email attachment, archival |
| PPTX | `--pptx` | Opening in PowerPoint/Keynote/Google Slides |

---

## Companion Skills

- **copy-planner** (upstream, optional): Plans content strategy for the presentation
- **copy-critic** (downstream): Reviews slide content for clarity, tone, audience fit
- **dataviz-executor** (sibling): Generates charts that can be referenced in slides
- **graphic-design-planner** (upstream, optional): Plans visual direction for branded decks
