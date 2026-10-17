---
name: ky-design-to-html-skill
description: Convert UI screenshots and design mockups to HTML/CSS with asset separation, canvas adaptation, and visual error correction
triggers:
  - convert this UI screenshot to HTML
  - recreate this design as HTML/CSS
  - turn this mockup into a webpage
  - restore this UI screenshot to code
  - generate HTML from this design screenshot
  - build HTML/CSS from this UI image
  - reproduce this page design in HTML
  - translate this screenshot to static HTML
---

# KY Design to HTML Skill

> Skill by [ara.so](https://ara.so) — Design Skills collection.

A Codex/Claude skill for converting UI screenshots and design mockups into HTML/CSS with proper asset separation, canvas ratio handling, screenshot validation, and visual error correction.

## What This Project Does

KY Design to HTML is **not** a "generate UI from description" tool. It focuses on **recreating existing UI screenshots or design files** as accurate HTML/CSS implementations.

The skill solves the common problem where AI tries to do everything at once (understand layout + replicate styles + draw complex assets) and produces broken, distorted, or blurry results.

Instead, it enforces a structured workflow:

1. **Decompose** the page into a structure map
2. **Separate** code-based elements from visual assets
3. **Set canvas ratios** (design dimensions vs. browser viewport)
4. **Write HTML/CSS** with proper structure
5. **Screenshot validation** in browser
6. **Compare and correct** visual errors

## Installation

### For Codex

```bash
mkdir -p ~/.codex/skills
cp -r ky-design-to-html ~/.codex/skills/
```

### For Claude

```bash
mkdir -p ~/.claude/skills
cp -r ky-design-to-html ~/.claude/skills/
```

### Verify Installation

The skill should appear in your agent's skill list. Check that these files exist:

```
ky-design-to-html/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── asset-handling.md
│   └── visual-error-taxonomy.md
└── scripts/
    └── screenshot_page.py
```

## Key Commands

### Basic Usage

When working with an AI agent that has this skill installed:

```text
Use $ky-design-to-html to recreate this UI screenshot as HTML/CSS.
```

Or in Chinese:

```text
使用 ky-design-to-html，把这张 UI 截图还原成一个 HTML/CSS 页面。
```

### Screenshot Validation Script

The skill includes a Python screenshot utility for validation:

```bash
python scripts/screenshot_page.py <html_file> <output_screenshot.png> [--width 1920] [--height 1080]
```

**Example:**

```bash
python scripts/screenshot_page.py landing.html screenshot.png --width 1440 --height 900
```

**Environment Requirements:**

```bash
pip install playwright
playwright install chromium
```

## Core Workflow

The skill enforces this process:

### 1. Page Decomposition

Before writing code, identify:

- **Layout structure** (header, hero, features, footer, etc.)
- **Text elements** (headings, paragraphs, buttons)
- **Visual assets** (icons, images, backgrounds, gradients)
- **Interactive elements** (buttons, links, forms)

### 2. Asset Separation Strategy

Decide what should be:

- **Pure CSS**: Simple shapes, solid colors, basic gradients, shadows
- **SVG inline**: Icons, logos, simple illustrations
- **Image files**: Photos, complex graphics, textures
- **Placeholder data URLs**: Temporary images during prototyping

**Reference:** See `references/asset-handling.md` for decision matrix.

### 3. Canvas & Viewport Setup

Define the design canvas dimensions and browser viewport:

```html
<!-- Design canvas: 1440x900 -->
<!-- Browser viewport: 1920x1080 -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            margin: 0;
            padding: 0;
            width: 1440px;
            margin: 0 auto;
        }
    </style>
</head>
```

### 4. HTML/CSS Implementation

Write semantic, structured HTML with scoped CSS:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Landing Page</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: #ffffff;
            width: 1440px;
            margin: 0 auto;
        }
        
        .hero {
            padding: 80px 60px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        .hero h1 {
            font-size: 56px;
            font-weight: 700;
            line-height: 1.2;
            margin-bottom: 24px;
        }
        
        .hero p {
            font-size: 20px;
            line-height: 1.6;
            opacity: 0.9;
            max-width: 600px;
        }
        
        .cta-button {
            display: inline-block;
            padding: 16px 32px;
            background: white;
            color: #667eea;
            text-decoration: none;
            border-radius: 8px;
            font-weight: 600;
            margin-top: 32px;
            transition: transform 0.2s;
        }
        
        .cta-button:hover {
            transform: translateY(-2px);
        }
        
        .features {
            padding: 80px 60px;
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 40px;
        }
        
        .feature-card {
            padding: 32px;
            background: #f7f9fc;
            border-radius: 12px;
        }
        
        .feature-icon {
            width: 48px;
            height: 48px;
            background: #667eea;
            border-radius: 8px;
            margin-bottom: 16px;
        }
        
        .feature-card h3 {
            font-size: 24px;
            margin-bottom: 12px;
            color: #1a202c;
        }
        
        .feature-card p {
            font-size: 16px;
            line-height: 1.6;
            color: #4a5568;
        }
    </style>
</head>
<body>
    <section class="hero">
        <h1>Build amazing products<br>with confidence</h1>
        <p>The complete platform for building and scaling your SaaS application, from prototype to production.</p>
        <a href="#" class="cta-button">Get Started</a>
    </section>
    
    <section class="features">
        <div class="feature-card">
            <div class="feature-icon"></div>
            <h3>Lightning Fast</h3>
            <p>Optimized performance that scales with your users, from day one to day 1000.</p>
        </div>
        <div class="feature-card">
            <div class="feature-icon"></div>
            <h3>Secure by Default</h3>
            <p>Enterprise-grade security built in, so you can focus on building features.</p>
        </div>
        <div class="feature-card">
            <div class="feature-icon"></div>
            <h3>Developer First</h3>
            <p>Beautiful APIs and documentation that developers actually enjoy using.</p>
        </div>
    </section>
</body>
</html>
```

### 5. Screenshot Validation

Use the included script to capture the rendered page:

```python
# scripts/screenshot_page.py usage
from playwright.sync_api import sync_playwright
import sys

def screenshot_page(html_path, output_path, width=1920, height=1080):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': width, 'height': height})
        page.goto(f'file://{html_path}')
        page.screenshot(path=output_path, full_page=True)
        browser.close()

if __name__ == '__main__':
    screenshot_page(sys.argv[1], sys.argv[2], 
                   int(sys.argv[3]) if len(sys.argv) > 3 else 1920,
                   int(sys.argv[4]) if len(sys.argv) > 4 else 1080)
```

Run it:

```bash
python scripts/screenshot_page.py output.html validation.png --width 1440 --height 900
```

### 6. Visual Error Correction

Compare the screenshot against the original design and identify errors:

**Common visual errors** (see `references/visual-error-taxonomy.md`):

- **Layout shift**: Element positions don't match
- **Size mismatch**: Width/height proportions off
- **Color deviation**: RGB values don't match
- **Font mismatch**: Wrong typeface, weight, or size
- **Spacing errors**: Padding/margin inconsistencies
- **Border/radius**: Wrong corner radius or border width
- **Shadow mismatch**: Box-shadow values incorrect
- **Alignment**: Text or elements not properly aligned

**Correction process:**

```css
/* Before - misaligned spacing */
.hero {
    padding: 60px 40px; /* Too small */
}

/* After - matched to screenshot */
.hero {
    padding: 80px 60px; /* Correct */
}
```

## Configuration

### Asset Handling Rules

From `references/asset-handling.md`:

| Asset Type | Method | When to Use |
|------------|--------|-------------|
| Simple icons | CSS or inline SVG | Geometric shapes, < 3 colors |
| Complex icons | SVG file or data URL | Illustrations, gradients |
| Photos | `<img>` with placeholder | Always |
| Backgrounds | CSS gradient | Simple linear/radial |
| Textures | Background image | Patterns, noise |
| Logos | Inline SVG | Vector, needs to scale |

### Visual Error Priorities

From `references/visual-error-taxonomy.md`:

1. **Critical**: Layout structure, major positioning
2. **High**: Typography (size, weight, spacing)
3. **Medium**: Colors, shadows, borders
4. **Low**: Subtle gradients, minor spacing

## Common Patterns

### Landing Page with Hero Section

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { margin: 0; font-family: -apple-system, BlinkMacSystemFont, sans-serif; }
        .container { max-width: 1200px; margin: 0 auto; padding: 0 24px; }
        .hero { padding: 120px 0; text-align: center; background: #f8f9fa; }
        .hero h1 { font-size: 48px; font-weight: 700; margin-bottom: 24px; }
        .hero p { font-size: 20px; color: #6c757d; max-width: 600px; margin: 0 auto; }
    </style>
</head>
<body>
    <section class="hero">
        <div class="container">
            <h1>Your Product Name</h1>
            <p>A compelling description of what your product does and why it matters.</p>
        </div>
    </section>
</body>
</html>
```

### Dashboard Layout with Sidebar

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <style>
        body { margin: 0; font-family: system-ui, sans-serif; }
        .layout { display: flex; height: 100vh; }
        .sidebar { width: 240px; background: #1a202c; color: white; padding: 24px; }
        .main { flex: 1; background: #f7fafc; padding: 32px; overflow-y: auto; }
        .nav-item { padding: 12px; margin: 8px 0; border-radius: 6px; cursor: pointer; }
        .nav-item:hover { background: #2d3748; }
        .card { background: white; padding: 24px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
    </style>
</head>
<body>
    <div class="layout">
        <aside class="sidebar">
            <div class="nav-item">Dashboard</div>
            <div class="nav-item">Analytics</div>
            <div class="nav-item">Settings</div>
        </aside>
        <main class="main">
            <div class="card">
                <h2>Dashboard Content</h2>
                <p>Main content area</p>
            </div>
        </main>
    </div>
</body>
</html>
```

### Empty State Page

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <style>
        body { margin: 0; font-family: -apple-system, sans-serif; }
        .empty-state { 
            display: flex; 
            flex-direction: column; 
            align-items: center; 
            justify-content: center; 
            height: 100vh; 
            text-align: center; 
            padding: 40px;
        }
        .empty-icon { 
            width: 120px; 
            height: 120px; 
            background: #e2e8f0; 
            border-radius: 50%; 
            margin-bottom: 24px; 
        }
        .empty-state h2 { font-size: 24px; margin-bottom: 12px; color: #1a202c; }
        .empty-state p { font-size: 16px; color: #718096; max-width: 400px; }
        .cta { 
            margin-top: 24px; 
            padding: 12px 24px; 
            background: #3182ce; 
            color: white; 
            border: none; 
            border-radius: 6px; 
            cursor: pointer; 
        }
    </style>
</head>
<body>
    <div class="empty-state">
        <div class="empty-icon"></div>
        <h2>No items yet</h2>
        <p>Get started by creating your first item. It only takes a few seconds.</p>
        <button class="cta">Create Item</button>
    </div>
</body>
</html>
```

## Troubleshooting

### Issue: Screenshot looks squished or stretched

**Cause:** Canvas width doesn't match design dimensions.

**Solution:**

```css
body {
    width: 1440px; /* Match your design canvas */
    margin: 0 auto;
}
```

### Issue: Colors don't match the screenshot

**Cause:** Wrong color values or color space.

**Solution:** Use a color picker tool on the original screenshot:

```css
/* Before - guessed color */
background: #6600ff;

/* After - picked from screenshot */
background: #667eea;
```

### Issue: Fonts look different

**Cause:** System font fallback or wrong font-weight.

**Solution:**

```css
/* Specify exact font stack */
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
font-weight: 600; /* Use exact weight from design */
```

### Issue: Spacing is off

**Cause:** Wrong padding/margin values.

**Solution:** Use browser DevTools to inspect and adjust:

```css
/* Measure exact spacing from screenshot */
.hero {
    padding: 80px 60px; /* Top/bottom: 80px, Left/right: 60px */
}

.hero h1 {
    margin-bottom: 24px; /* Exact spacing below heading */
}
```

### Issue: Screenshot script fails

**Cause:** Playwright not installed.

**Solution:**

```bash
pip install playwright
playwright install chromium
```

### Issue: Layout breaks at different viewport sizes

**Cause:** Design is fixed-width, not responsive.

**Solution:** This skill focuses on **recreating the exact design**, not making it responsive. If you need responsive:

```css
@media (max-width: 1440px) {
    body {
        width: 100%;
        padding: 0 24px;
    }
}
```

## Real-World Example

**Input:** Screenshot of a SaaS landing page (1440x900 design canvas)

**Agent workflow:**

1. **Decompose**: Header with logo + nav, hero section, 3-column features, footer
2. **Asset separation**: Logo as inline SVG, hero background as CSS gradient, feature icons as CSS shapes
3. **Set canvas**: `body { width: 1440px; margin: 0 auto; }`
4. **Write HTML/CSS**: Semantic structure with exact spacing
5. **Screenshot**: `python scripts/screenshot_page.py output.html check.png --width 1920 --height 1080`
6. **Compare**: Hero padding too small, feature cards missing border-radius
7. **Correct**: Update CSS, re-screenshot, validate

**Final deliverable:** Single HTML file that renders pixel-perfect to the original design.

## Best Practices

1. **Always separate assets first** before writing code
2. **Set explicit canvas dimensions** to prevent layout shift
3. **Use CSS variables** for repeated values:

```css
:root {
    --primary: #667eea;
    --spacing-lg: 80px;
    --spacing-md: 40px;
    --spacing-sm: 24px;
    --border-radius: 8px;
}

.hero {
    padding: var(--spacing-lg) var(--spacing-md);
    background: var(--primary);
}
```

4. **Screenshot early and often** to catch errors
5. **Work top-to-bottom** (header → hero → content → footer)
6. **Validate typography** separately (font-size, weight, line-height, letter-spacing)

This skill produces **static, pixel-perfect HTML/CSS recreations** of UI screenshots, not responsive or interactive web apps. For production use, you'll need to add JavaScript, make it responsive, and integrate with your backend.
