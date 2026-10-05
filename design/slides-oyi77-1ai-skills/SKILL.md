---
name: slides
description: Use when create strategic HTML presentations with Chart.js, design tokens, responsive layouts, copywriting formulas, and contextual slide strategies.
domain: content
author: claudekit
license: MIT
subdomain: slides
tags:
- slides
- presentations
- pitch-deck
- chartjs
- copywriting
- html
- strategy
version: 1.0.0
category: content
---


# Slides

Strategic HTML presentation design with data visualization.

## When to Use

- Marketing presentations and pitch decks
- Data-driven slides with Chart.js
- Strategic slide design with layout patterns
- Copywriting-optimized presentation content

## Workflow

1. **Plan** — Define presentation goal, audience, and slide count
2. **Structure** — Select strategy from slide-strategies.csv
3. **Design** — Generate layouts, typography, colors from decision CSVs
4. **Build** — Create HTML slides with Chart.js and design tokens
5. **Validate** — Check token compliance and pattern breaking
6. **Present** — Export and deliver presentation

## Subcommands

| Subcommand | Description | Reference |
|------------|-------------|-----------|
| `create` | Create strategic presentation slides | `references/create.md` |

## References (Knowledge Base)

| Topic | File |
|-------|------|
| Layout Patterns | `references/layout-patterns.md` |
| HTML Template | `references/html-template.md` |
| Copywriting Formulas | `references/copywriting-formulas.md` |
| Slide Strategies | `references/slide-strategies.md` |

## Routing

1. Parse subcommand from `$ARGUMENTS` (first word)
2. Load corresponding `references/{subcommand}.md`
3. Execute with remaining arguments

## Overview

Slides produces strategic HTML presentations directly — no PowerPoint or PDF toolchain. Each deck is a single self-contained HTML file that combines design tokens, Chart.js data visualizations, and copywriting formulas from the reference knowledge base. The workflow is plan → structure → design → build → validate → present.

## When NOT to Use

- A single page or landing section — build the page, not a deck
- Video, motion graphics, or animated explainers — route to HyperFrames or Remotion
- Document-style reports (Word/PDF) — route to document-creator
- When the audience needs an editable PowerPoint file — export the HTML deck and convert, or build in PowerPoint directly
- Pixel-perfect print/PDF output — HTML decks are screen-first

## Verification

1. Run the generated deck in a browser: open the HTML file and step through every slide with the arrow keys
2. Check token compliance — every color, spacing, and type value references the design-token CSS, no raw hex in slide markup
3. Verify each Chart.js canvas renders real data (not empty/zero axes) and is responsive at 1024px and mobile widths
4. Confirm the copywriting formula used (hook → proof → offer → CTA) is present in each section
5. Check pattern breaking — the deck alternates emotional beats at the 1/3 and 2/3 positions instead of one flat rhythm
6. Confirm the deck fits the time budget: ~1 slide per 60–90 seconds of presentation

## Quick Start

Build a minimal token-compliant deck:

Install Chart.js locally with `npm install chart.js` (or use the CDN in the template):
```bash
npm install chart.js
```

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>Pitch Deck</title>
  <link rel="stylesheet" href="assets/design-tokens.css" />
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
  <section class="slide">
    <h1>Hook — the problem in one line</h1>
    <p>Proof — why it matters now</p>
    <a class="cta">Offer → Call to action</a>
  </section>
</body>
</html>
```

Serve the deck locally to preview with `python3 -m http.server 8000`, or use a Node static server via `npx http-server .`.

## Anti-Rationalization Table

| Rationalization | Reality |
|-----------------|---------|
| "A generic template is fine, content matters more" | Generic decks read generic; slide strategy, layout patterns, and copy formulas are what persuade |
| "I'll just use CSS animations for transitions" | Page-load animations break when a deck is opened mid-stream; keep transitions keyboard-navigable and non-blocking |
| "Chart.js is overkill, a static table works" | Decision audiences respond to visual deltas; a line/bar chart communicates trend in one glance |
| "I'll design slides after writing the copy" | Structure first (strategy → layout → copy) prevents redesign churn; copy fills a decided frame |
| "Black-and-white text is always safe" | A brand-compliant token palette with deliberate contrast beats default styling and reads as designed |
