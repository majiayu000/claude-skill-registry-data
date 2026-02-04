---
name: research-pdf
description: Create distinctive HTML one-pagers with curated aesthetics, then convert to PDF using headless browser.
---

# Research PDF Generator

Create distinctive, memorable HTML one-pagers that avoid generic "AI slop" aesthetics.

## Setup Required

Before using this skill, configure your output directory:

```bash
# Add to your shell profile (~/.zshrc or ~/.bashrc)
export RESEARCH_PDF_DIR="$HOME/research-pdfs"

# Create the directory structure
mkdir -p "$RESEARCH_PDF_DIR/html" "$RESEARCH_PDF_DIR/pdf"
```

**Requirements:**
- macOS, Linux, or Windows with WSL
- Brave Browser or Google Chrome installed

## Instructions

When the user asks to research a topic and create a PDF:

1. **Research the topic** and gather key information
2. **Choose an aesthetic preset** based on content type (see Document Aesthetics below)
3. **Create an HTML file** in `$RESEARCH_PDF_DIR/html/` with:
   - Filename: `{topic-slug}-YYYYMMDD.html` (lowercase, hyphens, date suffix)
   - Example: `python-web-frameworks-20251212.html`
   - Date is the creation date; keep original date if updating later
   - Compact, print-friendly design (max 1-2 pages)
   - Follow the design standards below

4. **Generate the PDF** by running:
   ```bash
   research-pdf-generate
   ```
   Or if the command isn't in PATH:
   ```bash
   $RESEARCH_PDF_DIR/generate-pdfs.sh
   ```

5. **Verify** the PDF was created in `$RESEARCH_PDF_DIR/pdf/`

## File Locations

All paths relative to `$RESEARCH_PDF_DIR` (defaults to `~/research-pdfs`):

| Purpose | Path |
|---------|------|
| HTML source files | `$RESEARCH_PDF_DIR/html/` |
| Generated PDFs | `$RESEARCH_PDF_DIR/pdf/` |
| Conversion script | `$RESEARCH_PDF_DIR/generate-pdfs.sh` |

---

## Design Philosophy

**CRITICAL: Avoid generic AI aesthetics.** Every document should have distinctive character.

### What to AVOID (Generic AI Slop)
- System font stacks (`-apple-system, BlinkMacSystemFont, Roboto`)
- Flat white/gray backgrounds with no texture
- Purple gradients on white (overused AI default)
- Identical layouts across all document types
- No motion or interactivity in browser view

### What to EMBRACE
- **Intentional typography** - Fonts chosen for the content's personality
- **Texture and atmosphere** - Paper grain, subtle patterns, depth
- **Micro-interactions** - Hover states, transitions (for browser viewing)
- **Layout surprise** - Break the grid occasionally for emphasis
- **Cohesive theming** - CSS variables for consistency

---

## Document Aesthetics (Choose Based on Content Type)

### 1. TERMINAL - For Dev Tools, CLI, Technical Cheatsheets
Dark theme with hacker aesthetic. Think terminal green on dark.

```css
:root {
  --font-display: 'JetBrains Mono', 'Fira Code', monospace;
  --font-body: 'JetBrains Mono', 'Fira Code', monospace;
  --color-ink: #e6edf3;
  --color-ink-bright: #00ff88;
  --color-ink-dim: #7d8590;
  --color-paper: #0d1117;
  --color-paper-elevated: #161b22;
  --color-accent: #58a6ff;
  --color-accent-soft: rgba(88, 166, 255, 0.1);
  --color-border: #30363d;
  --color-muted: #484f58;
}
body {
  background: var(--color-paper);
  color: var(--color-ink);
  /* CRT scanline effect */
  background-image: repeating-linear-gradient(
    0deg,
    transparent,
    transparent 2px,
    rgba(0, 255, 136, 0.03) 2px,
    rgba(0, 255, 136, 0.03) 4px
  );
}
```

### 2. EDITORIAL - For Restaurant Guides, Reviews, Lifestyle
Warm, magazine-like. Serif headlines, refined spacing.

```css
:root {
  --font-display: 'Playfair Display', 'Crimson Pro', Georgia, serif;
  --font-body: 'Source Sans 3', 'Libre Franklin', sans-serif;
  --color-ink: #1a1a1a;
  --color-paper: #fefcf9;
  --color-accent: #c41e3a; /* Carmine red */
  --color-accent-soft: #fef0f2;
  --color-muted: #6b7280;
}
body {
  background: var(--color-paper);
  /* Subtle paper texture */
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.04'/%3E%3C/svg%3E");
}
h1 {
  font-family: var(--font-display);
  font-weight: 700;
  letter-spacing: -0.02em;
  border-bottom: 3px double var(--color-accent);
}
```

### 3. CORPORATE - For Business Analysis, Board Docs, Professional
Navy + gold accents. Refined, trustworthy, premium feel.

```css
:root {
  --font-display: 'Fraunces', 'Source Serif Pro', Georgia, serif;
  --font-body: 'Inter', 'Source Sans 3', sans-serif;
  --color-ink: #1e293b;
  --color-paper: #ffffff;
  --color-accent: #1e40af; /* Deep blue */
  --color-accent-gold: #b8860b;
  --color-accent-soft: #eff6ff;
  --color-muted: #64748b;
}
body {
  background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
}
h1 {
  color: var(--color-accent);
  border-bottom: 2px solid var(--color-accent-gold);
}
.section h2 {
  background: linear-gradient(135deg, var(--color-accent), #1e3a8a);
  color: white;
}
```

### 4. INDUSTRIAL - For Automotive, Hardware, Specs
Bold, utilitarian, data-forward. Wide headers, strong lines.

```css
:root {
  --font-display: 'Oswald', 'Bebas Neue', Impact, sans-serif;
  --font-body: 'Barlow', 'Roboto Condensed', sans-serif;
  --color-ink: #111827;
  --color-paper: #f3f4f6;
  --color-accent: #dc2626; /* Industrial red */
  --color-accent-alt: #fbbf24; /* Warning yellow */
  --color-stripe: #1f2937;
}
body {
  background: var(--color-paper);
  /* Subtle grid pattern */
  background-image:
    linear-gradient(rgba(0,0,0,0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0,0,0,0.03) 1px, transparent 1px);
  background-size: 20px 20px;
}
h1 {
  font-family: var(--font-display);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  background: var(--color-stripe);
  color: white;
  padding: 12px 20px;
  margin: -20px -20px 20px -20px;
}
```

### 5. FRESH - For Health, Eco, Nature Topics
Organic feel, soft greens, breathing space.

```css
:root {
  --font-display: 'DM Serif Display', Georgia, serif;
  --font-body: 'DM Sans', 'Nunito', sans-serif;
  --color-ink: #1a3d2e;
  --color-paper: #f0fdf4;
  --color-accent: #16a34a;
  --color-accent-soft: #dcfce7;
  --color-earth: #78716c;
}
body {
  background: linear-gradient(135deg, #f0fdf4 0%, #ecfdf5 50%, #f0fdf9 100%);
}
.section {
  border-radius: 16px;
  border: 1px solid #bbf7d0;
}
```

---

## Required CSS Foundation

Every document MUST include this foundation:

```css
*, *::before, *::after {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: var(--font-body);
  font-size: 11px;
  line-height: 1.5;
  padding: 20px;
  max-width: 8.5in;
  margin: 0 auto;
  color: var(--color-ink);
  background: var(--color-paper);
}

/* Micro-interactions for browser viewing */
.section {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.section:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 30px rgba(0,0,0,0.08);
}

tr {
  transition: background 0.15s ease;
}
tr:hover {
  background: var(--color-accent-soft) !important;
}

a {
  color: var(--color-accent);
  text-decoration: none;
  background-image: linear-gradient(var(--color-accent), var(--color-accent));
  background-size: 0% 1px;
  background-position: 0% 100%;
  background-repeat: no-repeat;
  transition: background-size 0.3s ease;
}
a:hover {
  background-size: 100% 1px;
}

/* Print styles */
@media print {
  body { padding: 10px; }
  .section { break-inside: avoid; }
  .section:hover { transform: none; box-shadow: none; }
}
```

---

## Typography Scale

| Element | Size | Weight | Notes |
|---------|------|--------|-------|
| Page Title | 20-24px | 700 | Use `--font-display`, add `letter-spacing: -0.02em` |
| Section Headers | 13-15px | 600-700 | Often on gradient backgrounds |
| Body Text | 10-11px | 400 | Use `--font-body` |
| Table Content | 9-10px | 400 | Tighter line-height (1.3) |
| Footer/Citations | 8-9px | 400 | Use `--color-muted` |
| Badges/Tags | 8-9px | 600 | UPPERCASE, letter-spacing: 0.05em |

---

## Semantic Colors (Use Consistently Across All Aesthetics)

- Success: `#10b981` ✓
- Warning: `#f59e0b` ⚠
- Error: `#ef4444` ✗
- Info: `#3b82f6` ℹ
- Feature: `#8b5cf6` ★

---

## Enhanced Components

### Badges with Depth
```css
.badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 3px 10px;
  border-radius: 100px;
  font-size: 8px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
.badge.yes {
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
  box-shadow: 0 2px 8px rgba(16, 185, 129, 0.25);
}
.badge.no {
  background: linear-gradient(135deg, #ef4444, #dc2626);
  color: white;
  box-shadow: 0 2px 8px rgba(239, 68, 68, 0.25);
}
.badge.warn {
  background: linear-gradient(135deg, #f59e0b, #d97706);
  color: white;
  box-shadow: 0 2px 8px rgba(245, 158, 11, 0.25);
}
```

### Key Insight Box (Grid-Breaking)
```css
.key-insight {
  grid-column: 1 / -1;
  margin: 16px -10px;
  padding: 16px 20px;
  background: linear-gradient(135deg, var(--color-accent-soft), transparent);
  border-left: 4px solid var(--color-accent);
  border-radius: 0 12px 12px 0;
  position: relative;
}
.key-insight::before {
  content: '→';
  position: absolute;
  left: 8px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 18px;
  color: var(--color-accent);
  font-weight: bold;
}
.key-insight p {
  margin-left: 20px;
  font-weight: 500;
}
```

### Winner/Highlight Row
```css
.winner {
  background: linear-gradient(90deg, #dcfce7 0%, #f0fdf4 100%) !important;
  font-weight: 600;
  position: relative;
}
.winner td:first-child::before {
  content: '🏆';
  margin-right: 6px;
}
```

### Keyboard Keys (for cheatsheets)
```css
.key {
  font-family: var(--font-body);
  background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
  border: 1px solid #ced4da;
  border-bottom-width: 2px;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 9px;
  font-weight: 600;
  box-shadow: 0 1px 2px rgba(0,0,0,0.05);
}
```

---

## Emojis
Use strategically: 1-2 emojis in title, 0-1 per section header.

**Recommended:**
📊 Data | 🎯 Goals | 💡 Ideas | ⚡ Fast | 🔒 Security | 🎨 Design | 📝 Notes | 🔗 Links
✅ Done | ⚠️ Warn | ❌ No | 🚀 Launch | 📈 Growth | 🎓 Learn | 🏆 Winner | ⭐ Star

---

## References & Footnotes

Use markdown-style inline citations: `[1]`, `[2]`, `[3]`

```css
.ref {
  color: var(--color-accent);
  font-size: 8px;
  vertical-align: super;
  text-decoration: none;
  font-weight: 600;
}
```

**References Section Format:**
```
[1] Source Name — Title. url.com/path
[2] Author — "Article Title". domain.com/...
```

Keep to 3-5 key references. Place at bottom of document.

---

## Standard Footer Template

**REQUIRED FORMAT:**
```html
<div class="footer">
  <strong>[Document Title]</strong> — [Brief Description]<br>
  Sources: [Source 1] <sup class="ref">[1]</sup> | [Source 2] <sup class="ref">[2]</sup><br>
  Generated: [Date]
  <div class="signature">
    Prepared with research-pdf skill — Claude Code
  </div>
</div>
```

```css
.footer {
  text-align: center;
  font-size: 9px;
  color: var(--color-muted);
  margin-top: 16px;
  padding-top: 12px;
  border-top: 2px solid var(--color-border, #e2e8f0);
}
.footer .signature {
  font-style: italic;
  margin-top: 8px;
  opacity: 0.7;
}
```

---

## Page Layout
- Use CSS Grid for multi-column layouts
- Keep under 8.5in width for Letter size PDF
- Print-friendly: `@media print` rules
- No external dependencies (inline CSS only)
- Include Google Fonts via `@import` for distinctive typography

---

## Quick Reference: Aesthetic Selection

| Content Type | Aesthetic | Key Visual Elements |
|--------------|-----------|---------------------|
| CLI tools, dev cheatsheets | TERMINAL | Dark theme, monospace, green accents, scanlines |
| Restaurant guides, reviews | EDITORIAL | Serif headers, warm paper, red accents |
| Business docs, analysis | CORPORATE | Navy/gold, refined serif, clean gradients |
| Automotive, hardware specs | INDUSTRIAL | Bold sans, uppercase, grid patterns, red/yellow |
| Health, eco, nature | FRESH | Soft greens, organic shapes, breathing space |

---

## Example Usage

User: "Create a research PDF about Python web frameworks"

1. **Select aesthetic**: TERMINAL (it's a dev/technical topic)
2. Create `$RESEARCH_PDF_DIR/html/python-web-frameworks-20251212.html`
3. Run `research-pdf-generate`
4. PDF appears at `$RESEARCH_PDF_DIR/pdf/python-web-frameworks-20251212.pdf`
