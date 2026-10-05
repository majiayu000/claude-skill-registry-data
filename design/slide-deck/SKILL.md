---
name: slide-deck
description: >
  Generate beautiful HTML slide presentations from markdown or plain text.
  Dark theme, smooth animations, speaker notes. Output is a single HTML file
  that opens in any browser. Use when the user asks to create slides, a presentation,
  a deck, or a pitch. Triggers on: "make slides", "create a presentation",
  "slide deck", "pitch deck", "make a PPT", "presentation for".
tags:
  - slides
  - presentation
  - pitch
  - deck
  - powerpoint
  - keynote
  - reveal
---

# Slide Deck

You generate clean, professional HTML slide presentations from text or markdown input.

## Core Behavior

When the user provides content (text, markdown, outline, or topic), generate a single self-contained HTML file that works as a slide presentation in any browser.

## Output Format

A single HTML file using reveal.js CDN. The file must be:
- Self-contained (no local dependencies)
- Dark theme by default (professional, high contrast)
- Responsive (works on any screen size)
- Keyboard navigable (arrow keys, spacebar)

## HTML Template

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[TITLE]</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5/dist/reveal.min.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5/dist/theme/black.min.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5/plugin/highlight/monokai.min.css">
    <style>
        .reveal { font-family: 'Inter', -apple-system, sans-serif; }
        .reveal h1 { font-size: 2.5em; font-weight: 700; }
        .reveal h2 { font-size: 1.8em; font-weight: 600; color: #58a6ff; }
        .reveal h3 { font-size: 1.3em; color: #8b949e; }
        .reveal li { margin-bottom: 0.5em; font-size: 0.9em; }
        .reveal code { background: #161b22; padding: 2px 8px; border-radius: 4px; font-size: 0.85em; }
        .reveal pre code { padding: 16px; font-size: 0.75em; }
        .reveal .subtitle { color: #8b949e; font-size: 0.7em; margin-top: 0.5em; }
        .reveal .highlight { color: #f0883e; font-weight: 600; }
        .reveal .stat { font-size: 3em; font-weight: 700; color: #58a6ff; }
        .reveal blockquote { border-left: 4px solid #58a6ff; padding-left: 1em; font-style: italic; color: #8b949e; }
    </style>
</head>
<body>
    <div class="reveal">
        <div class="slides">
            [SLIDES HERE]
        </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/reveal.js@5/dist/reveal.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/reveal.js@5/plugin/highlight/highlight.min.js"></script>
    <script>
        Reveal.initialize({
            hash: true,
            transition: 'fade',
            transitionSpeed: 'fast',
            plugins: [RevealHighlight]
        });
    </script>
</body>
</html>
```

## Slide Structure Rules

### Title slide
```html
<section>
    <h1>[Title]</h1>
    <p class="subtitle">[Subtitle or author]</p>
</section>
```

### Content slide (bullets)
```html
<section>
    <h2>[Heading]</h2>
    <ul>
        <li>[Point 1]</li>
        <li>[Point 2]</li>
        <li>[Point 3]</li>
    </ul>
</section>
```

### Stat slide (for impact numbers)
```html
<section>
    <p class="stat">43.3%</p>
    <h2>GPU sits idle during tool execution</h2>
    <p class="subtitle">Matches Kim et al.'s 30-55% finding (HPCA 2026)</p>
</section>
```

### Code slide
```html
<section>
    <h2>[Heading]</h2>
    <pre><code class="language-python">[code here]</code></pre>
</section>
```

### Quote slide
```html
<section>
    <blockquote>"[Quote text]"</blockquote>
    <p class="subtitle">— [Attribution]</p>
</section>
```

## Design Rules
- Maximum 5 bullet points per slide — if more, split into 2 slides
- Maximum 15 words per bullet point
- One big idea per slide
- Use stat slides for impressive numbers (big font, high impact)
- Use code slides only when showing actual code
- Title slide + 8-15 content slides + closing slide is ideal
- Add speaker notes with `<aside class="notes">` when the user provides extra context

## Commands

### From text
User: "Make slides about [topic]"
- Generate 10-12 slides covering the topic
- Save as `[topic]-slides.html`

### From markdown
User: "Turn this into slides: [markdown]"
- Convert headings to slide titles
- Convert bullets to slide content
- Each `##` heading = new slide

### From outline
User: "Slides from this outline: 1. Intro 2. Problem 3. Solution 4. Results"
- Each outline item = 1-2 slides
- Add content based on context

## Rules
- Always output a SINGLE HTML file — no external dependencies except CDN
- Dark theme by default. Light theme only if user requests it.
- Never put more than 5 items on one slide
- Never use clip art, stock photos, or emojis in slides
- File saves to current directory unless user specifies a path
- Name the file descriptively: `agenttrace-presentation.html`, not `slides.html`
