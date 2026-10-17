---
name: xiaopu-web-design-skill
description: Generate beautiful, consistent web pages with Claude using a spec-first, code-second design workflow
triggers:
  - design a web page from this PRD
  - create a website with consistent design system
  - generate web design spec before coding
  - build a landing page following design principles
  - design website from screenshot or reference
  - create DESIGN.md specification for my site
  - use web-design skill to build this page
  - follow spec-first design workflow
---

# xiaopu-web-design-skill

> Skill by [ara.so](https://ara.so) — Design Skills collection.

A Claude Code SKILL for designing beautiful, consistent web pages using a **spec-first, code-second** methodology. It generates a comprehensive `DESIGN.md` specification before producing any code, ensuring visual consistency, accessibility, and maintainability.

## What It Does

The web-design SKILL transforms requirements (PRD, reference URLs, screenshots, or keywords) into production-ready web pages through a three-phase process:

1. **Phase A - Understand**: Extract design cues from inputs
2. **Phase B - Produce `DESIGN.md`**: Generate a 9-section design specification
3. **Phase C - Generate Code**: Build HTML/CSS/JS that strictly follows the spec

## Installation

```bash
# Clone into Claude Code skills directory
git clone https://github.com/xiaopu-ai/web-design ~/.claude/skills/web-design
```

Claude Code will auto-discover the skill on next session start.

## Project Structure

```
web-design/
├── SKILL.md              # Core skill instructions
├── references/           # Design systems, style seeds, motion library
│   ├── design-systems/   # Base design system references
│   ├── style-seeds/      # Color and typography presets
│   ├── motion-library/   # Animation patterns
│   ├── interaction-patterns/  # UI interaction guidelines
│   └── quality-checklist.md   # 100-point quality audit
├── scripts/              # Utility scripts
│   ├── crawl.py         # Playwright web crawler
│   ├── extract_tokens.py # Static token extractor
│   └── fetch_images.py  # Unsplash image fetcher
└── docs/                # Example landing page
    ├── index.html
    ├── styles.css
    ├── app.js
    └── DESIGN.md        # Generated spec example
```

## Key Workflow

### Phase A: Understanding Inputs

The skill accepts multiple input types with graceful fallbacks:

```python
# Input types (in priority order):
# 1. PRD (Product Requirements Document)
# 2. Reference URL (existing site to analyze)
# 3. Screenshot (visual reference)
# 4. Keywords (design direction)
# 5. Brand name (extract from context)
```

### Phase B: DESIGN.md Generation

The skill produces a comprehensive 9-section specification:

```markdown
# DESIGN.md Structure

## 1. Color System
- Primary, secondary, accent palettes
- Background and surface colors
- Text and border colors
- Semantic colors (success, error, warning)

## 2. Typography
- Font families and weights
- Size scale and line heights
- Letter spacing and text transforms

## 3. Component Library
- Buttons, cards, inputs, navigation
- Visual states (hover, active, disabled)

## 4. Layout System
- Grid structure and breakpoints
- Spacing scale and container widths

## 5. Motion Design
- Transition timings and easings
- Animation patterns and durations

## 6. Depth & Elevation
- Shadow definitions
- Z-index hierarchy

## 7. Design Principles
- Do's and don'ts
- Visual hierarchy rules

## 8. Responsive Behavior
- Breakpoint strategies
- Mobile-first considerations

## 9. Accessibility
- Color contrast ratios
- Focus states and ARIA patterns
```

### Phase C: Code Generation

After `DESIGN.md` approval, the skill generates code that:

- Strictly follows the specification
- Self-audits against 100-point quality checklist
- Diff-audits against reference URL if provided
- Maintains consistency across pages

## Usage Examples

### Example 1: Generate from PRD

```python
# In Claude Code chat:
"""
Use web-design skill to create a landing page for a SaaS product.

PRD:
- Product: AI-powered email automation
- Target: B2B marketing teams
- Key features: Smart scheduling, A/B testing, analytics
- Brand: Professional, trustworthy, modern
- CTA: Start free trial
"""

# The skill will:
# 1. Extract design direction from PRD
# 2. Generate DESIGN.md with appropriate colors, typography, components
# 3. Wait for approval
# 4. Generate index.html, styles.css, app.js
```

### Example 2: Generate from Reference URL

```python
# In Claude Code chat:
"""
Use web-design skill to create a portfolio site.
Reference: https://example-portfolio.com

Key differences:
- Use warmer color palette
- Add smooth scroll animations
- Include project filtering
"""

# The skill will:
# 1. Crawl reference URL for design tokens
# 2. Extract color, typography, layout patterns
# 3. Generate modified DESIGN.md
# 4. Produce code with requested enhancements
```

### Example 3: Generate from Screenshot

```python
# In Claude Code chat (with screenshot attached):
"""
Use web-design skill to recreate this design as a responsive webpage.
Add accessibility improvements and modern interactions.
"""

# The skill will:
# 1. Analyze screenshot for visual elements
# 2. Infer color palette, typography, spacing
# 3. Generate DESIGN.md with enhancements
# 4. Build accessible, responsive code
```

## Reference Files

### Style Seeds

Located in `references/style-seeds/`, these provide pre-configured design systems:

```yaml
# Example: modern-saas.yaml
colors:
  primary: "#6366F1"
  secondary: "#8B5CF6"
  accent: "#EC4899"
  background: "#FFFFFF"
  surface: "#F9FAFB"
  
typography:
  heading: "Inter"
  body: "Inter"
  
spacing:
  unit: 4px
  scale: [4, 8, 12, 16, 24, 32, 48, 64, 96]
```

### Motion Library

Located in `references/motion-library/`, provides animation patterns:

```javascript
// Example: fade-in-up.js
export const fadeInUp = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0 },
  transition: { duration: 0.6, ease: [0.22, 1, 0.36, 1] }
};

// Example: stagger-children.js
export const staggerContainer = {
  animate: {
    transition: {
      staggerChildren: 0.1,
      delayChildren: 0.2
    }
  }
};
```

### Quality Checklist

The skill self-audits against `references/quality-checklist.md` (100 points):

- **Visual Design** (25 pts): Color contrast, typography hierarchy, spacing consistency
- **Code Quality** (25 pts): Semantic HTML, CSS organization, JavaScript best practices
- **Responsiveness** (20 pts): Mobile-first, breakpoint handling, fluid layouts
- **Accessibility** (20 pts): ARIA labels, keyboard navigation, screen reader support
- **Performance** (10 pts): Asset optimization, lazy loading, critical CSS

## Utility Scripts

### Web Crawler

Extract design tokens from existing websites:

```bash
# Install dependencies
cd scripts
pip install playwright beautifulsoup4

# Run crawler
python crawl.py --url https://example.com --output tokens.json

# Output includes:
# - Color palette (extracted from CSS)
# - Typography (font families, sizes, weights)
# - Spacing values
# - Component patterns
```

### Token Extractor

Parse static files for design tokens:

```bash
# Extract from CSS/HTML files
python extract_tokens.py --input ../docs --output design-tokens.json

# Generates structured JSON:
{
  "colors": {"primary": "#6366F1", ...},
  "typography": {"heading": "Inter", ...},
  "spacing": [4, 8, 16, 24, ...]
}
```

### Image Fetcher

Fetch placeholder images from Unsplash:

```bash
# Set API key
export UNSPLASH_ACCESS_KEY=your_key_here

# Fetch images by query
python fetch_images.py --query "technology" --count 5 --output ../docs/images/

# Options:
# --query: Search term
# --count: Number of images
# --width, --height: Dimensions
# --output: Destination directory
```

## Configuration

### Customizing Design Systems

Create custom style seeds in `references/style-seeds/`:

```yaml
# custom-brand.yaml
name: "My Brand Design System"

colors:
  primary: "#FF6B6B"
  secondary: "#4ECDC4"
  accent: "#FFE66D"
  background: "#F7F7F7"
  text: "#2C3E50"

typography:
  heading: "Playfair Display"
  body: "Source Sans Pro"
  monospace: "Fira Code"

spacing:
  unit: 8px
  scale: [8, 16, 24, 32, 40, 48, 64, 80, 96]

borders:
  radius:
    sm: 4px
    md: 8px
    lg: 16px
    full: 9999px
  width:
    thin: 1px
    medium: 2px
    thick: 4px

shadows:
  sm: "0 1px 2px 0 rgba(0, 0, 0, 0.05)"
  md: "0 4px 6px -1px rgba(0, 0, 0, 0.1)"
  lg: "0 10px 15px -3px rgba(0, 0, 0, 0.1)"
```

### Adding Custom Motion Patterns

Create animations in `references/motion-library/`:

```javascript
// custom-hero-animation.js
export const heroAnimation = {
  container: {
    initial: { opacity: 0 },
    animate: { 
      opacity: 1,
      transition: { staggerChildren: 0.15, delayChildren: 0.3 }
    }
  },
  item: {
    initial: { opacity: 0, y: 40 },
    animate: { 
      opacity: 1, 
      y: 0,
      transition: { duration: 0.8, ease: [0.22, 1, 0.36, 1] }
    }
  }
};

// scroll-reveal.js
export const scrollReveal = {
  initial: { opacity: 0, scale: 0.95 },
  whileInView: { opacity: 1, scale: 1 },
  viewport: { once: true, margin: "-100px" },
  transition: { duration: 0.6 }
};
```

## Common Patterns

### Pattern 1: Multi-Page Website with Consistent Design

```python
# Step 1: Generate DESIGN.md for the entire site
"""
Use web-design skill to create a design system for a 5-page website:
- Home
- About
- Services
- Portfolio
- Contact

Brand: Creative agency, bold and playful
"""

# Step 2: Generate first page
"""
Generate the home page following the approved DESIGN.md
"""

# Step 3: Generate subsequent pages
"""
Generate the about page using the same DESIGN.md spec
"""

# The DESIGN.md ensures consistency across all pages
```

### Pattern 2: Iterative Design Refinement

```python
# Initial generation
"""
Use web-design skill to create a pricing page.
Reference: https://stripe.com/pricing
"""

# Review DESIGN.md, request changes
"""
Update DESIGN.md:
- Change primary color to #7C3AED
- Increase heading font sizes by 20%
- Add glass morphism effect to pricing cards
"""

# Regenerate code with updated spec
"""
Regenerate pricing page code using the updated DESIGN.md
"""
```

### Pattern 3: A/B Testing Variations

```python
# Generate baseline version
"""
Use web-design skill to create a landing page for email signup.
Generate two variations in DESIGN.md:
A: Conservative (blues, serif fonts, minimal animations)
B: Bold (vibrant colors, sans-serif, dynamic effects)
"""

# Skill generates two separate DESIGN.md sections
# Then produces two versions of the page
```

### Pattern 4: Accessibility-First Design

```python
"""
Use web-design skill to create an accessible documentation site.

Requirements:
- WCAG 2.1 AAA compliance
- High contrast mode support
- Keyboard navigation throughout
- Screen reader optimized
- Reduced motion mode

Generate DESIGN.md with accessibility annotations.
"""

# Skill includes detailed accessibility notes in each section
# Code includes ARIA labels, semantic HTML, focus management
```

## Code Examples

### Example: Generated HTML Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Product Name - Tagline</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <!-- Navigation -->
  <nav class="nav" role="navigation" aria-label="Main navigation">
    <div class="nav__container">
      <a href="#" class="nav__logo" aria-label="Home">
        <span class="nav__logo-text">Brand</span>
      </a>
      <ul class="nav__menu">
        <li><a href="#features" class="nav__link">Features</a></li>
        <li><a href="#pricing" class="nav__link">Pricing</a></li>
        <li><a href="#contact" class="nav__link">Contact</a></li>
      </ul>
      <button class="btn btn--primary">Get Started</button>
    </div>
  </nav>

  <!-- Hero Section -->
  <section class="hero" id="hero">
    <div class="hero__container">
      <h1 class="hero__title">Build amazing products faster</h1>
      <p class="hero__subtitle">The all-in-one platform for modern teams</p>
      <div class="hero__cta">
        <button class="btn btn--primary btn--lg">Start Free Trial</button>
        <button class="btn btn--secondary btn--lg">Watch Demo</button>
      </div>
    </div>
  </section>

  <script src="app.js" type="module"></script>
</body>
</html>
```

### Example: Generated CSS (Following DESIGN.md)

```css
/* Design System Variables (from DESIGN.md) */
:root {
  /* Colors */
  --color-primary: #6366F1;
  --color-primary-hover: #4F46E5;
  --color-secondary: #8B5CF6;
  --color-accent: #EC4899;
  --color-background: #FFFFFF;
  --color-surface: #F9FAFB;
  --color-text-primary: #111827;
  --color-text-secondary: #6B7280;
  
  /* Typography */
  --font-heading: 'Inter', sans-serif;
  --font-body: 'Inter', sans-serif;
  --font-size-h1: clamp(2.5rem, 5vw, 4rem);
  --font-size-h2: clamp(2rem, 4vw, 3rem);
  --font-size-body: 1rem;
  --line-height-heading: 1.2;
  --line-height-body: 1.6;
  
  /* Spacing */
  --space-xs: 0.5rem;
  --space-sm: 1rem;
  --space-md: 1.5rem;
  --space-lg: 2rem;
  --space-xl: 3rem;
  --space-2xl: 4rem;
  
  /* Borders */
  --radius-sm: 0.375rem;
  --radius-md: 0.5rem;
  --radius-lg: 1rem;
  
  /* Shadows */
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  
  /* Motion */
  --transition-fast: 150ms cubic-bezier(0.4, 0, 0.2, 1);
  --transition-base: 300ms cubic-bezier(0.4, 0, 0.2, 1);
  --transition-slow: 500ms cubic-bezier(0.4, 0, 0.2, 1);
}

/* Component: Button */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-sm) var(--space-lg);
  font-family: var(--font-body);
  font-size: var(--font-size-body);
  font-weight: 600;
  border-radius: var(--radius-md);
  border: none;
  cursor: pointer;
  transition: all var(--transition-base);
  text-decoration: none;
}

.btn--primary {
  background: var(--color-primary);
  color: white;
}

.btn--primary:hover {
  background: var(--color-primary-hover);
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

.btn--primary:active {
  transform: translateY(0);
}

.btn--primary:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

/* Layout: Hero Section */
.hero {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-2xl) var(--space-md);
  background: linear-gradient(135deg, var(--color-surface) 0%, var(--color-background) 100%);
}

.hero__container {
  max-width: 64rem;
  text-align: center;
}

.hero__title {
  font-family: var(--font-heading);
  font-size: var(--font-size-h1);
  font-weight: 700;
  line-height: var(--line-height-heading);
  color: var(--color-text-primary);
  margin-bottom: var(--space-md);
  animation: fadeInUp 0.8s cubic-bezier(0.22, 1, 0.36, 1);
}

.hero__subtitle {
  font-size: 1.25rem;
  color: var(--color-text-secondary);
  margin-bottom: var(--space-xl);
  animation: fadeInUp 0.8s cubic-bezier(0.22, 1, 0.36, 1) 0.2s backwards;
}

.hero__cta {
  display: flex;
  gap: var(--space-md);
  justify-content: center;
  flex-wrap: wrap;
  animation: fadeInUp 0.8s cubic-bezier(0.22, 1, 0.36, 1) 0.4s backwards;
}

/* Animation */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(2rem);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Responsive */
@media (max-width: 768px) {
  .hero {
    padding: var(--space-xl) var(--space-md);
  }
  
  .hero__cta {
    flex-direction: column;
  }
  
  .btn {
    width: 100%;
  }
}

/* Reduced Motion */
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

### Example: Generated JavaScript

```javascript
// app.js - Generated by web-design skill

// Smooth scroll for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      target.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
      });
    }
  });
});

// Intersection Observer for scroll animations
const observerOptions = {
  root: null,
  rootMargin: '0px',
  threshold: 0.1
};

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('is-visible');
      observer.unobserve(entry.target);
    }
  });
}, observerOptions);

// Observe elements with animation class
document.querySelectorAll('.animate-on-scroll').forEach(el => {
  observer.observe(el);
});

// Navbar scroll effect
let lastScroll = 0;
const nav = document.querySelector('.nav');

window.addEventListener('scroll', () => {
  const currentScroll = window.pageYOffset;
  
  if (currentScroll <= 0) {
    nav.classList.remove('nav--scrolled');
    return;
  }
  
  if (currentScroll > lastScroll && currentScroll > 100) {
    // Scrolling down
    nav.classList.add('nav--hidden');
  } else {
    // Scrolling up
    nav.classList.remove('nav--hidden');
  }
  
  if (currentScroll > 50) {
    nav.classList.add('nav--scrolled');
  } else {
    nav.classList.remove('nav--scrolled');
  }
  
  lastScroll = currentScroll;
});

// Keyboard navigation for custom components
document.querySelectorAll('.btn').forEach(btn => {
  btn.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      btn.click();
    }
  });
});

// Focus trap for modal (if present)
function trapFocus(element) {
  const focusableElements = element.querySelectorAll(
    'a[href], button:not([disabled]), textarea:not([disabled]), input:not([disabled]), select:not([disabled])'
  );
  const firstElement = focusableElements[0];
  const lastElement = focusableElements[focusableElements.length - 1];

  element.addEventListener('keydown', (e) => {
    if (e.key !== 'Tab') return;

    if (e.shiftKey) {
      if (document.activeElement === firstElement) {
        lastElement.focus();
        e.preventDefault();
      }
    } else {
      if (document.activeElement === lastElement) {
        firstElement.focus();
        e.preventDefault();
      }
    }
  });
}

// Initialize focus trap for modals
document.querySelectorAll('[role="dialog"]').forEach(modal => {
  trapFocus(modal);
});
```

## Troubleshooting

### Issue: DESIGN.md is too generic

**Solution**: Provide more specific inputs:

```python
# Instead of:
"Create a landing page"

# Use:
"Create a landing page for a B2B SaaS product targeting enterprise clients.
Brand personality: Professional, innovative, trustworthy.
Reference: https://linear.app
Key difference: Warmer color palette with purple accents."
```

### Issue: Code doesn't match DESIGN.md

**Solution**: Regenerate with explicit instruction:

```python
"Regenerate the code strictly following DESIGN.md.
Run self-audit against quality-checklist.md before outputting.
Ensure all color values, font sizes, and spacing match the spec exactly."
```

### Issue: Missing responsive behavior

**Solution**: Enhance DESIGN.md section 8:

```python
"Update DESIGN.md section 8 (Responsive Behavior) with detailed breakpoints:
- Mobile: 0-640px (single column, stacked nav)
- Tablet: 641-1024px (two columns, hamburger menu)
- Desktop: 1025px+ (multi-column, full nav)

Then regenerate the responsive CSS."
```

### Issue: Accessibility violations

**Solution**: Request accessibility audit:

```python
"Run accessibility audit against WCAG 2.1 AA standards.
Update DESIGN.md section 9 with fixes for:
- Color contrast ratios
- Focus indicators
- ARIA labels
- Keyboard navigation

Then regenerate code with accessibility improvements."
```

### Issue: Crawler fails on dynamic sites

**Solution**: Use headless mode with wait conditions:

```bash
# Modify crawl.py to wait for dynamic content
python crawl.py \
  --url https://example.com \
  --wait-for ".main-content" \
  --timeout 10000 \
  --output tokens.json
```

### Issue: Motion animations too aggressive

**Solution**: Request reduced motion:

```python
"Update DESIGN.md section 5 (Motion Design) to include:
- Reduced motion media query support
- Shorter animation durations (max 300ms)
- Subtle effects (opacity and slight movement only)

Regenerate CSS with accessibility-friendly animations."
```

## Best Practices

1. **Always review DESIGN.md before code generation** — it's easier to fix design decisions in the spec than in code.

2. **Keep DESIGN.md in version control** — treat it as source of truth for visual consistency.

3. **Use reference URLs for inspiration, not copying** — the skill extracts patterns, not pixels.

4. **Provide brand context early** — personality keywords help generate appropriate design decisions.

5. **Iterate on DESIGN.md, not code** — update the spec and regenerate rather than manually editing output.

6. **Test accessibility from the start** — request WCAG compliance in initial prompt.

7. **Leverage style seeds for rapid prototyping** — modify existing seeds rather than starting from scratch.

8. **Document custom patterns** — add project-specific components to DESIGN.md for reuse.
