---
name: content-saver
description: Guides users through saving generated content (summaries, notes, key points) to professionally formatted and themed files. Use when users want to save, export, or persist content generated during the session, choose Option 4 after transcription, apply styling/themes to saved content, or explicitly ask to save summaries, notes, or derived content.
---

# Content Saver

This skill provides professional formatting templates AND visual themes for saving generated content to files. Content can include summaries, notes, key points, analysis, or any text derived from transcriptions.

## Available Formats

| Format | File | Best For |
|--------|------|----------|
| **Executive Summary** | `formats/executive-summary.md` | Business stakeholders |
| **Detailed Notes** | `formats/detailed-notes.md` | Research, reference |
| **Key Points** | `formats/key-points.md` | Quick reference |
| **Structured Data** | `formats/structured-data.md` | Integration, JSON |
| **Plain Text** | `formats/plain-text.md` | Universal compatibility |

## Available Themes

### Classic Themes
| Theme | File | Style |
|-------|------|-------|
| **Professional Dark** | `themes/professional-dark.md` | Dark mode, teal accents |
| **Professional Light** | `themes/professional-light.md` | Clean, navy headings |
| **Modern Minimalist** | `themes/modern-minimalist.md` | Off-white, whitespace |
| **Academic** | `themes/academic.md` | Warm sepia, serif fonts |
| **Vibrant Creative** | `themes/vibrant-creative.md` | Bold purple/pink |

### Premium Themes (Enhanced UI/UX)
| Theme | File | Style | Features |
|-------|------|-------|----------|
| **Neural AI** | `themes/neural-ai.md` | Cyberpunk, glowing accents | Animations, gradients, callouts |
| **Glassmorphism** | `themes/glassmorphism.md` | Frosted glass, modern | Blur effects, hover states, cards |
| **Notion Style** | `themes/notion-style.md` | Notion-inspired, clean | Toggles, callouts, properties |
| **GitHub Docs** | `themes/github-docs.md` | GitHub documentation | Alerts, labels, dark mode |
| **Terminal Hacker** | `themes/terminal-hacker.md` | Retro terminal, green text | CRT effects, ASCII art, prompts |

### Shared Resources
| Resource | File | Purpose |
|----------|------|---------|
| **Components Library** | `themes/COMPONENTS.md` | Reusable UI patterns |

## Theme Selection Guide

| Content Type | Recommended Themes |
|--------------|-------------------|
| Technical documentation | GitHub Docs, Terminal Hacker |
| Meeting notes & wikis | Notion Style |
| Research papers | Academic |
| Product reports | Glassmorphism, Professional Light |
| AI/ML content | Neural AI |
| Developer logs | Terminal Hacker |
| Business documents | Professional Light/Dark |
| Creative briefs | Vibrant Creative, Glassmorphism |

## Workflow

### Step 1: Identify Content
Confirm what content the user wants to save (summary, key points, notes, analysis).
If content doesn't exist yet, offer to generate it first.

### Step 2: Present Format Options
```
## Save Content — Choose a Format

1. **Executive Summary** — Professional markdown with metadata
2. **Detailed Notes** — Comprehensive documentation format
3. **Key Points** — Bulleted action items and takeaways
4. **Structured Data** — JSON for programmatic use
5. **Plain Text** — Simple, universal format

Which format would you like? (1-5)
```

### Step 3: Present Theme Options
```
## Apply a Theme

### Classic Themes
1. **Professional Dark** — Sleek dark mode with teal accents
2. **Professional Light** — Clean corporate styling
3. **Modern Minimalist** — Elegant simplicity
4. **Academic** — Scholarly with serif fonts
5. **Vibrant Creative** — Bold and energetic

### Premium Themes (Enhanced UI/UX)
6. **Neural AI** — Futuristic cyberpunk with glowing effects
7. **Glassmorphism** — Modern frosted glass aesthetic
8. **Notion Style** — Clean productivity-focused design
9. **GitHub Docs** — Developer documentation style
10. **Terminal Hacker** — Retro green-on-black terminal

11. **No Theme** — Plain formatting only

Which theme? (1-11)
```

### Step 4: Apply Template & Save
1. **Read the template**: Use Read tool on `formats/{format-name}.md`
2. **Read the theme** (if selected): Use Read tool on `themes/{theme-name}.md`
3. **Read components** (optional): Check `themes/COMPONENTS.md` for reusable patterns
4. Structure content according to the format template
5. Apply theme CSS/styling from theme file
6. Include appropriate components (callouts, badges, cards) from the theme
7. Generate filename: `{source}_{type}_{YYYYMMDD}.{ext}`
8. Save with `write_file` tool
9. Confirm save and offer next steps

## Themed Output

When theme is applied, wrap content in HTML:
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{Document Title}</title>
  <style>
    /* CSS from theme file */
  </style>
</head>
<body>
  <article>
    <!-- Formatted content with theme components -->
  </article>
</body>
</html>
```
Save as `.html` instead of `.md` when themed.

## Using Theme Components

Premium themes include rich components. Reference `themes/COMPONENTS.md` for:

### Callouts / Alerts
```html
<!-- Notion/Glassmorphism style -->
<div class="callout callout-info">
  <div class="callout-icon">💡</div>
  <div class="callout-content">Important insight here...</div>
</div>

<!-- GitHub style -->
<div class="markdown-alert markdown-alert-note">
  <p class="markdown-alert-title">📘 Note</p>
  <p>Information the user should know...</p>
</div>

<!-- Terminal style -->
<div class="status status-success">[OK] Operation completed.</div>
```

### Badges / Tags
```html
<span class="badge badge-success">Complete</span>
<span class="tag tag-blue">transcript</span>
<span class="label label-purple">featured</span>
```

### Cards (Glassmorphism, Neural AI)
```html
<div class="card">
  <h4>Key Insight</h4>
  <p>Important finding...</p>
</div>
```

### Toggle Sections (Notion, GitHub)
```html
<details class="toggle">
  <summary class="toggle-header">Expand for details</summary>
  <div class="toggle-content">Hidden content...</div>
</details>
```

## Theme Feature Matrix

| Feature | Neural AI | Glassmorphism | Notion | GitHub | Terminal |
|---------|-----------|---------------|--------|--------|----------|
| Dark Mode | Built-in | Gradient BG | Light only | Auto-detect | Built-in |
| Animations | Yes | Hover effects | No | No | Flicker |
| Callouts | Yes | Yes | Yes | 5 types | Status msgs |
| Cards | Yes | Yes (glass) | Properties | No | ASCII box |
| Code Highlighting | Gradient bar | Frost border | Border | GitHub style | Terminal |
| Print Styles | Yes | Yes | Yes | Yes | Yes |
| Responsive | Yes | Yes | Yes | Yes | Yes |

## External Dependencies

Some premium themes load fonts from Google Fonts CDN:

| Theme | CDN Fonts | Fallback Fonts |
|-------|-----------|----------------|
| **Neural AI** | Orbitron, Inter, JetBrains Mono | system sans-serif, monospace |
| **Glassmorphism** | Plus Jakarta Sans, Inter, Fira Code | DM Sans, system-ui, monospace |
| **Notion Style** | Inter | -apple-system, system-ui |
| **Terminal Hacker** | VT323, Fira Code, Share Tech Mono | Source Code Pro, monospace |

**Offline/Restricted Environments**: All themes include fallback fonts that work without internet access. The design will remain functional with system fonts.

## Critical Rules

1. **Always Confirm** — Never save without confirming format, theme, filename
2. **Read Templates On-Demand** — Use Read tool to fetch specific format/theme files
3. **Preserve Content** — Don't modify meaning when formatting
4. **Include Metadata** — Source reference, date, content type
5. **Match Theme to Content** — Suggest appropriate themes based on content type
6. **Use Components** — Leverage theme-specific callouts, badges, and cards
7. **Report Success** — Confirm path and offer follow-up

## Error Handling

| Error | Resolution |
|-------|------------|
| No content to save | Offer to generate first |
| Write failure | Report error, suggest alternative |
| Template not found | Use Read tool on correct path |
| Theme not found | Fall back to Professional Light or no theme |
| Component not in theme | Use generic HTML equivalent |

## Quick Examples

### Neural AI Theme Output
Best for: AI research, technical analysis, ML documentation
```html
<h1>Analysis Report</h1>
<span class="badge badge-primary">AI Generated</span>
<div class="callout callout-info">
  <strong>Neural Analysis:</strong> Key insights detected...
</div>
```

### Notion Style Output
Best for: Meeting notes, project documentation, wikis
```html
<div class="properties">
  <div class="property">
    <span class="property-name">Source</span>
    <span class="property-value">Video Transcript</span>
  </div>
</div>
<details class="toggle">
  <summary>Key Takeaways</summary>
  <div class="toggle-content">...</div>
</details>
```

### Terminal Hacker Output
Best for: Developer logs, CLI documentation, tech tutorials
```html
<div class="status status-success">[OK] Transcript processed.</div>
<div class="prompt">
  <span class="prompt-symbol">$</span>
  <span class="prompt-command">cat summary.txt</span>
</div>
```
