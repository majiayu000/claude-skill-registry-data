---
name: zensical-development
description: Best practices for developing zensical/Material for MkDocs static sites. Covers installation, virtual environments, project structure, responsive images, CSS, media embedding, and verification. Use for ANY Material for MkDocs project development beyond basic text editing.
---

# Zensical Development Best Practices

Comprehensive workflow and best practices for developing zensical (Material for MkDocs) static sites with proper setup, responsive design, image handling, and media embedding.

## CRITICAL: Always Use Zensical, Never MkDocs Directly

**NEVER use `mkdocs serve` or `mkdocs build` commands directly.**

Always use the zensical CLI:
- `zensical serve` (NOT `mkdocs serve`)
- `zensical build` (NOT `mkdocs build`)

## Project Setup & Requirements

### Installation & Virtual Environment

**CRITICAL:** Every Zensical project MUST have a Python virtual environment (`.venv`).

```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # macOS/Linux

# Install zensical
pip install zensical
```

### .gitignore Requirements

**MANDATORY entries:**

```gitignore
# Python virtual environment
.venv/
venv/

# Zensical build output
site/

# Cache directories
.cache/

# System files
.DS_Store
```

### Creating a New Project

```bash
# Bootstrap new project
zensical new .

# This creates:
# - .github/ directory
# - docs/ folder with index.md
# - zensical.toml configuration file
```

## Development Workflow

### Step 1: Make Changes

**Text-only changes** (no visual verification needed):
- Fixing typos, updating content

**Visual changes** (REQUIRES visual verification):
- Adding/modifying CSS
- Adding/moving images
- Embedding videos
- Changing layouts

### Step 2: Deploy Locally

```bash
source .venv/bin/activate
zensical serve
# Site runs at http://localhost:8000
```

**Server Restart Required For:**
- CSS file changes
- Configuration changes (`zensical.toml`)
- JavaScript file changes

### Step 3: Verification (MANDATORY for visual changes)

```python
# Navigate to page
mcp__chrome-devtools__navigate_page(url="http://127.0.0.1:8000/page/")

# Take screenshot
mcp__chrome-devtools__take_screenshot()

# Verify image dimensions
mcp__chrome-devtools__evaluate_script(function="""
() => {
  const images = document.querySelectorAll('img');
  return Array.from(images).map(img => ({
    src: img.src.split('/').pop(),
    maxWidth: window.getComputedStyle(img).maxWidth,
    displayWidth: img.offsetWidth
  }));
}
""")
```

## Best Practices

### Responsive Images

```css
img {
    display: block;
    margin: 0 auto;
    max-width: 100%;
    height: auto;
}
```

### YouTube Videos

```html
<div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; margin: 20px 0;">
  <iframe
    src="https://www.youtube.com/embed/VIDEO_ID"
    style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"
    frameborder="0"
    allowfullscreen>
  </iframe>
</div>
```

## Common Issues & Fixes

### Images Cropped/Cut Off
Remove `max-height` from global `img` selector:
```css
img {
    max-width: 100%;
    height: auto;
}
```

### Images Not Loading (404)
Check path relative to markdown file location.

### Horizontal Overflow on Mobile
Use `max-width: 100%` and test at 375px.

## Project Structure

```
project-root/
├── .venv/                   # Virtual environment (in .gitignore)
├── docs/                    # Content directory
│   ├── index.md
│   ├── stylesheets/
│   │   └── extra.css
│   └── img/
├── zensical.toml            # Configuration
├── .gitignore
└── site/                    # Built output (in .gitignore)
```

## Common Commands

```bash
# Setup
python3 -m venv .venv
source .venv/bin/activate
pip install zensical
zensical new .

# Development
zensical serve

# Building
zensical build
zensical build --strict
```

## Summary

1. Every Zensical project MUST have `.venv/`
2. `.gitignore` MUST include: `.venv/`, `site/`, `.cache/`
3. Always activate venv before running zensical commands
4. Visual verification is MANDATORY for CSS/HTML/image changes
5. CSS changes require server restart
6. Images use `max-width: 100%; height: auto;`
