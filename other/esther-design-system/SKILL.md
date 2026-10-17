---
name: esther-design-system
description: AI-driven personal brand design system that converts content into consistent, brand-aligned HTML pages with predefined colors, fonts, layouts, and components
triggers:
  - create a landing page using esther design system
  - generate a tutorial page with my brand style
  - build an app interface with esther components
  - design a xiaohongshu card using brand guidelines
  - convert this content into a branded HTML page
  - apply esther design system to this layout
  - make a page following brand DNA rules
  - use the personal IP design system
---

# Esther Design System

> Skill by [ara.so](https://ara.so) — Design Skills collection.

Esther Design System is a constraint-based design system for AI agents that transforms content into brand-consistent HTML pages. It enforces strict visual rules (colors, fonts, layouts, components) to ensure every AI-generated page looks cohesive and "not like generic AI output."

## What It Does

- **Converts content → branded HTML pages** for 4 scenarios: tutorials, landing pages, apps, social media cards
- **Constrains AI creativity** via predefined layouts, components, and strict brand rules
- **Enforces quality** through a mandatory 7-step workflow + P0/P1/P2 checklist
- **Prevents "AI look"** by banning common patterns (glassmorphism, gradients, default HTML styles)

## Core Philosophy

```
Strict constraints = consistent quality
Limited options = faster decisions
Explicit rules = predictable output
```

AI can only use pre-approved layouts, colors, fonts, and components. No improvisation allowed.

## Installation

1. **Clone or reference** this repository in your AI agent's context:
   ```bash
   git clone https://github.com/esthersjw/esther-design-system.git
   ```

2. **Load into AI agent**:
   - **Cola Skill**: Place in `~/Cola/skills/esther-design-system/`
   - **Claude Projects**: Upload entire folder
   - **Cursor**: Add to workspace root and reference in `.cursorrules`

3. **Initialize workflow**: Tell your AI agent to read `SKILL.md` before any design task

## File Structure

```
esther-design-system/
├── SKILL.md                    # 7-step workflow (this file)
├── brand-dna.md                # Brand colors, fonts, tone, forbidden patterns
├── assets/
│   ├── template-tutorial.html      # Starting point for tutorials
│   ├── template-landing.html       # Starting point for landing pages
│   ├── template-app.html           # Starting point for app UIs
│   ├── template-cards.html         # Starting point for social cards
│   └── avatar.jpg                  # Brand avatar
└── references/
    ├── layouts.md                  # 15 approved layout patterns with code
    ├── components.md               # 2988-line component library
    ├── checklist.md                # Quality gates (P0/P1/P2)
    ├── scene-tutorial.md           # Tutorial-specific rules
    ├── scene-landing.md            # Landing page rules
    ├── scene-app.md                # App UI rules
    └── scene-cards.md              # Social card rules
```

## 7-Step Workflow

Every design task MUST follow this sequence:

### Step 1: Gather Requirements
Ask the user 5 questions before starting:
```
1. 页面类型？(tutorial/landing/app/cards)
2. 目标受众？
3. 几屏内容？
4. 现有素材？(文字/图片/视频)
5. 特殊约束？(截止日期/技术限制)
```

### Step 2: Load Brand Rules
Read in this order:
1. `brand-dna.md` (global rules)
2. Corresponding scene file (`scene-{type}.md`)
3. `layouts.md` (layout options)
4. `components.md` (component library)

### Step 3: Copy Base Template
```bash
# Start from template, NEVER from scratch
cp assets/template-{type}.html output.html
```

### Step 4: Select 3-5 Layouts
From `layouts.md`, choose layouts ensuring:
- **No two sections use same layout**
- Mix alignment (left/right/center)
- At least one full-width section
- At least one asymmetric section

Example selection:
```
Section 1: Hero (Center Dominant)
Section 2: Feature Grid (Offset Triple Card)
Section 3: Quote (Left Text + Right Visual)
Section 4: Process (Timeline Vertical)
Section 5: CTA (Split Half)
```

### Step 5: Build with Components
From `components.md`, use ONLY pre-built components:
```html
<!-- WRONG: Default HTML -->
<blockquote>Some quote</blockquote>

<!-- RIGHT: Use brand component -->
<div class="quote-block-simple">
  <div class="quote-line"></div>
  <blockquote>Some quote</blockquote>
  <cite>— Author</cite>
</div>
```

### Step 6: Self-Check Against Checklist
Run through `checklist.md`:

**P0 (Must Pass All)**:
- [ ] Brand color ratio: Blue 60% / Yellow 30% / Red 10%
- [ ] Zero forbidden elements (glassmorphism, neon, bounce animations)
- [ ] Zero default HTML styles
- [ ] Warm background (`#FFFCF5` or similar)
- [ ] Serif + sans-serif mix
- [ ] Responsive (mobile-first)
- [ ] All sections use different layouts
- [ ] Fluid sizing with `clamp()`
- [ ] Doesn't look "AI-generated"

**P1 (Should Pass)**:
- [ ] At least one "wow" visual section
- [ ] Extreme font size contrast (h1 vs body ≥ 3:1)
- [ ] Scroll reveal animations
- [ ] Large decorative numbers/English text

### Step 7: Deliver
Output a single `.html` file that:
- Opens directly in browser (no build step)
- Includes all CSS inline or in `<style>` tags
- Uses CDN fonts (Google Fonts, etc.)
- Has no external dependencies except fonts

## Brand DNA Reference

### Colors
```css
/* Primary Palette */
--brand-blue: #2B7FD8;    /* 60% usage */
--brand-yellow: #F4D758;  /* 30% usage */
--brand-red: #E84A5F;     /* 10% usage - accents only */

/* Neutrals */
--warm-bg: #FFFCF5;
--text-dark: #1A1A1A;
--text-gray: #666666;

/* Extension Rules */
/* OK: Tints/shades of brand colors */
--blue-light: rgba(43, 127, 216, 0.1);
--yellow-bg: rgba(244, 215, 88, 0.2);

/* FORBIDDEN: Purple, neon, black backgrounds */
```

### Fonts
```html
<!-- Load in <head> -->
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;700&family=Noto+Sans+SC:wght@400;500;700&family=Fraunces:ital,wght@1,400&family=Caveat&family=Fira+Code&display=swap" rel="stylesheet">
```

```css
/* Usage */
h1, h2, h3 { font-family: 'Noto Serif SC', serif; }
body, p { font-family: 'Noto Sans SC', sans-serif; }
.decorative-english { font-family: 'Fraunces', serif; font-style: italic; }
.handwritten { font-family: 'Caveat', cursive; }
code, pre { font-family: 'Fira Code', monospace; }
```

### Forbidden Patterns
```
❌ Blue-purple gradients
❌ Glassmorphism (backdrop-filter: blur)
❌ Neon colors
❌ animation: bounce
❌ Inter/Roboto fonts
❌ All sections centered
❌ Default <blockquote>, <ul>, <table> styles
❌ Generic AI templates
```

## Key Components

### Magazine-Style Card
```html
<div class="card-magazine">
  <div class="card-eyebrow" style="background: var(--brand-yellow);">
    Category
  </div>
  <h3>Card Title</h3>
  <p>Description text here...</p>
  <a href="#" class="card-link">Learn more →</a>
</div>

<style>
.card-magazine {
  background: white;
  padding: 2rem;
  border-left: 4px solid var(--brand-blue);
  position: relative;
}
.card-eyebrow {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 1rem;
}
</style>
```

### Terminal Code Block
```html
<div class="code-terminal">
  <div class="terminal-header">
    <span class="terminal-dot" style="background: #E84A5F;"></span>
    <span class="terminal-dot" style="background: #F4D758;"></span>
    <span class="terminal-dot" style="background: #2B7FD8;"></span>
    <span class="terminal-title">bash</span>
  </div>
  <pre><code>npm install esther-design-system</code></pre>
</div>

<style>
.code-terminal {
  background: #1A1A1A;
  border-radius: 8px;
  overflow: hidden;
  font-family: 'Fira Code', monospace;
}
.terminal-header {
  background: #2A2A2A;
  padding: 0.75rem 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.terminal-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
}
.terminal-title {
  margin-left: auto;
  color: #999;
  font-size: 0.875rem;
}
.code-terminal pre {
  padding: 1.5rem;
  margin: 0;
  color: #00FF00;
}
</style>
```

### Quote Block with Hand-Written Badge
```html
<div class="quote-handwritten">
  <span class="handwritten-badge">💡 Insight</span>
  <blockquote>
    The best design systems are the ones that constrain creativity
    just enough to ensure consistency.
  </blockquote>
  <cite>— Design Principle #3</cite>
</div>

<style>
.quote-handwritten {
  background: rgba(244, 215, 88, 0.1);
  border-left: 4px solid var(--brand-yellow);
  padding: 2rem;
  position: relative;
}
.handwritten-badge {
  position: absolute;
  top: -0.75rem;
  left: 2rem;
  background: white;
  padding: 0.25rem 0.75rem;
  font-family: 'Caveat', cursive;
  font-size: 1.25rem;
  border: 2px solid var(--brand-yellow);
  transform: rotate(-2deg);
}
blockquote {
  font-size: 1.25rem;
  line-height: 1.6;
  margin: 1rem 0 0.5rem;
  font-style: italic;
}
cite {
  font-size: 0.875rem;
  color: #666;
}
</style>
```

## Common Patterns

### Fluid Typography
```css
/* Always use clamp() for responsive sizing */
h1 {
  font-size: clamp(2rem, 5vw + 1rem, 4rem);
}
p {
  font-size: clamp(1rem, 2vw + 0.5rem, 1.125rem);
}
```

### Layout Grid
```css
.section-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: clamp(2rem, 5vw, 6rem) clamp(1rem, 3vw, 2rem);
}

/* Three-column grid with gap */
.grid-3col {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}
```

### Scroll Reveal Animation
```html
<div class="reveal-on-scroll">Content</div>

<style>
.reveal-on-scroll {
  opacity: 0;
  transform: translateY(30px);
  transition: opacity 0.6s ease, transform 0.6s ease;
}
.reveal-on-scroll.revealed {
  opacity: 1;
  transform: translateY(0);
}
</style>

<script>
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('revealed');
    }
  });
}, { threshold: 0.1 });

document.querySelectorAll('.reveal-on-scroll').forEach(el => {
  observer.observe(el);
});
</script>
```

## Troubleshooting

### "Output looks too generic"
- **Check**: Did you use 3+ different layouts from `layouts.md`?
- **Check**: Did you include at least one decorative English/number element?
- **Check**: Is there extreme font size contrast (hero vs body)?
- **Fix**: Add asymmetry, use `transform: rotate()` on decorative elements

### "Colors feel off"
- **Check**: Measure color usage — Blue should dominate (60%), Yellow accents (30%), Red sparingly (10%)
- **Fix**: Replace overused yellow with blue tints, reserve red for CTAs only

### "Fails P0 checklist"
- **Most common**: Using default `<blockquote>` or `<ul>` styles
- **Fix**: Replace ALL default HTML elements with components from `components.md`
- **Example**:
  ```html
  <!-- WRONG -->
  <ul>
    <li>Item 1</li>
  </ul>
  
  <!-- RIGHT -->
  <div class="custom-list">
    <div class="list-item">
      <span class="bullet" style="background: var(--brand-blue);"></span>
      <span>Item 1</span>
    </div>
  </div>
  ```

### "Not responsive on mobile"
- **Check**: Are you using `clamp()` for all font sizes?
- **Check**: Is grid using `minmax()` with `auto-fit`?
- **Fix**: Add mobile-first media query:
  ```css
  @media (max-width: 768px) {
    .grid-3col {
      grid-template-columns: 1fr;
    }
  }
  ```

### "Animation jank"
- **Check**: Did you include `prefers-reduced-motion`?
  ```css
  @media (prefers-reduced-motion: reduce) {
    * {
      animation-duration: 0.01ms !important;
      transition-duration: 0.01ms !important;
    }
  }
  ```

## Advanced Usage

### Creating Custom Variants

To adapt for a different brand:

1. **Fork the repo**
2. **Edit `brand-dna.md`**:
   ```markdown
   ### 三色
   | 颜色 | 色值 | 比例 |
   |------|------|------|
   | 主色 | #YOUR_COLOR | 60% |
   | 辅色 | #YOUR_COLOR | 30% |
   | 强调 | #YOUR_COLOR | 10% |
   ```
3. **Update CSS variables** in templates:
   ```css
   :root {
     --brand-primary: #YOUR_COLOR;
     --brand-secondary: #YOUR_COLOR;
     --brand-accent: #YOUR_COLOR;
   }
   ```
4. **Replace `assets/avatar.jpg`**
5. **Keep workflow** (`SKILL.md`) and component structure intact

### Adding New Components

Add to `references/components.md`:

```markdown
### Your Component Name

**使用场景**: When to use this

**代码**:
\`\`\`html
<div class="your-component">
  <!-- Component HTML -->
</div>

<style>
.your-component {
  /* Component CSS */
}
</style>
\`\`\`

**注意事项**: Important notes
```

Then reference it in Step 5 of the workflow.

## Example: Full Tutorial Page Generation

**User request**: "Create a tutorial page about CSS Grid"

**AI workflow**:

1. **Ask questions** → User confirms: tutorial type, beginner audience, 5 sections, text-only, no constraints
2. **Load files** → Read `brand-dna.md`, `scene-tutorial.md`, `layouts.md`, `components.md`
3. **Copy template** → Start from `assets/template-tutorial.html`
4. **Select layouts**:
   - Hero: Center Dominant
   - Section 1: Left Text + Right Visual
   - Section 2: Offset Triple Card
   - Section 3: Full Width Code Block
   - Section 4: Timeline Vertical
   - CTA: Split Half
5. **Build content** using components:
   - Magazine cards for grid properties
   - Terminal code block for examples
   - Quote block for key insights
6. **Check**:
   - ✅ Color ratio correct
   - ✅ No forbidden patterns
   - ✅ All sections different layouts
   - ✅ Clamp() used
7. **Deliver** `css-grid-tutorial.html`

## Resources

- **Full component library**: `references/components.md` (2988 lines)
- **All 15 layouts**: `references/layouts.md` (with copy-paste code)
- **Quality checklist**: `references/checklist.md` (P0/P1/P2 gates)
- **Scene-specific rules**: `references/scene-*.md` (4 files)

---

**Key principle**: This system trades AI flexibility for brand consistency. Every constraint is intentional. When in doubt, choose the option with MORE constraints, not fewer.
