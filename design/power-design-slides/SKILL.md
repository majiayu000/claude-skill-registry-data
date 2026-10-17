---
name: power-design-slides
description: Generate brand-aligned presentation slides using Claude with 20 codified design principles and 72+ pre-built brand systems
triggers:
  - create a slide deck with power design
  - make slides that look professional
  - generate presentation using brand DNA
  - build a deck with design principles
  - create slides for my brand
  - make a presentation that follows design rules
  - generate branded slides in HTML
  - use power design to create a deck
---

# Power Design Slides

> Skill by [ara.so](https://ara.so) — Design Skills collection

Power Design is a Claude Code skill that generates presentation slides combining **brand DNA** (extracted from URLs or 72+ pre-built brand systems) with **20 codified design principles** from Tufte, Reynolds, Duarte, Williams, Refactoring UI, and WCAG 2.2. Output is beautiful HTML decks that don't look AI-generated.

## What It Does

- Extracts brand identity (colors, typography, voice) from any URL via Firecrawl
- Applies 20 research-backed design rules to every slide
- Generates self-contained HTML presentation files
- Includes 72+ pre-built brand systems (Stripe, Apple, Linear, Spotify, Tesla, etc.)
- Enforces WCAG contrast ratios, modular scales, data-ink ratios, and F-pattern layouts

## Installation

```bash
# Clone into Claude skills directory
git clone https://github.com/ItsssssJack/power-design ~/.claude/skills/power-design

# Or manually:
cd ~/.claude/skills
git clone https://github.com/ItsssssJack/power-design power-design
```

Verify installation:
```bash
ls ~/.claude/skills/power-design/SKILL.md
```

## Project Structure

```
power-design/
├── SKILL.md                          # Skill runbook (this file)
├── principles/
│   ├── design-principles.md          # All 20 rules with citations
│   └── images/                       # Rule illustrations
├── brands/
│   ├── _template.md                  # Template for new brands
│   ├── anthropic-claude.md           # Pre-built brand system
│   ├── stripe.md
│   └── ... (72+ brands)
└── examples/
    └── sample-deck.html              # Reference output
```

## Basic Usage

### 1. Generate a Deck with Pre-Built Brand

```
> use power-design — make me a deck for stripe.com about our new product launch
```

The skill will:
1. Load Stripe's brand DNA from `brands/stripe.md`
2. Ask for content brief (headline + 3-5 key points)
3. Generate `slides.html` applying brand × 20 rules
4. Open in browser

### 2. Extract Brand from URL

```
> use power-design — create slides using the brand from example.com
```

Requires Firecrawl API key:
```bash
export FIRECRAWL_API_KEY=your_key_here
```

The skill extracts:
- Primary/secondary/accent colors
- Typography (font families, weights, sizes)
- Voice/tone
- Component patterns
- Layout principles

### 3. Use Default Design System

```
> use power-design — make a deck about AI safety (no brand)
```

Falls back to a neutral, high-contrast design system.

## The 20 Design Rules

Every slide passes these checks:

| # | Rule | Threshold |
|---:|---|---|
| 1 | One idea per slide | 1 main message |
| 2 | Glanceable in ≤3 seconds | ≤50 words |
| 3 | 3–5 visual chunks | Max 7 |
| 4 | ≥40% whitespace ratio | Measured |
| 5 | 5% edge safe-zone | All sides |
| 6 | Modular scale 1.25–1.618 | Type sizes |
| 7 | Max 4 type sizes per slide | Counted |
| 8 | Body ≥24px, title ≥48px | Enforced |
| 9 | Line-height 1.4–1.6 body | CSS |
| 10 | Line length ≤60 chars | Measured |
| 11 | WCAG contrast ≥4.5:1 | 7:1 aim |
| 12 | 60-30-10 color split | Measured |
| 13 | One accent per slide | Max 1 |
| 14 | Never hue-only encoding | Patterns/icons |
| 15 | 8pt grid spacing | All margins |
| 16 | Single grid alignment | Consistent |
| 17 | Proximity ≤16px related | ≥48px unrelated |
| 18 | Data-ink ratio ≥80% | Charts only |
| 19 | F-pattern layout | Headline top-left |
| 20 | Pick one mode (minimal/rich) | Consistent |

Full documentation with sources: `principles/design-principles.md`

## Code Examples

### Create a Custom Brand System

Create `brands/my-company.md`:

```markdown
# My Company Brand System

**Source URL:** https://mycompany.com  
**Last updated:** 2025-01-15

## Colors

### Primary
- **Brand Blue:** `#0066FF` (rgb(0, 102, 255))
- **Dark Navy:** `#001133` (rgb(0, 17, 51))

### Secondary
- **Warm Gray:** `#F5F5F0` (rgb(245, 245, 240))
- **Cool Gray:** `#E8EBF0` (rgb(232, 235, 240))

### Accent
- **Action Orange:** `#FF6B35` (rgb(255, 107, 53))

### Semantic
- **Success:** `#00CC66`
- **Warning:** `#FFAA00`
- **Error:** `#FF3333`

## Typography

### Font Families
- **Sans:** "Inter", system-ui, sans-serif
- **Mono:** "JetBrains Mono", monospace

### Scale (1.25 ratio)
- **Display:** 64px / 700
- **H1:** 48px / 700
- **H2:** 36px / 600
- **Body:** 24px / 400
- **Caption:** 18px / 400

### Line Heights
- Display/Headings: 1.1
- Body: 1.5

## Voice & Tone

- **Personality:** Technical but approachable
- **Formality:** Professional casual
- **Key phrases:** "Ship fast", "Build trust", "Stay nimble"

## Layout Principles

- 8pt grid system
- 5% minimum edge margins
- Max content width: 1200px
- Card-based components with subtle shadows
```

### Generate Slides Programmatically

If you want to script deck generation:

```python
# deck_generator.py
import subprocess
import os

def generate_deck(brand_name, content_brief, output_path="slides.html"):
    """
    Generate a Power Design deck via Claude CLI
    """
    prompt = f"""
    use power-design
    
    Brand: {brand_name}
    
    Content:
    {content_brief}
    
    Generate slides.html and save to {output_path}
    """
    
    result = subprocess.run(
        ["claude", "code", "--prompt", prompt],
        capture_output=True,
        text=True
    )
    
    if os.path.exists(output_path):
        print(f"✓ Deck generated: {output_path}")
        return True
    else:
        print(f"✗ Generation failed: {result.stderr}")
        return False

# Usage
content = """
Headline: Introducing Data Pipeline v2
Points:
- 10x faster ingestion
- Real-time validation
- Zero-downtime migrations
- Built-in observability
"""

generate_deck("stripe", content, "pipeline-v2-deck.html")
```

### Extract Brand DNA via Firecrawl

```python
# brand_extractor.py
import os
import json
from firecrawl import FirecrawlApp

def extract_brand_dna(url):
    """
    Extract brand identity from website using Firecrawl
    """
    api_key = os.environ.get("FIRECRAWL_API_KEY")
    if not api_key:
        raise ValueError("FIRECRAWL_API_KEY not set")
    
    app = FirecrawlApp(api_key=api_key)
    
    # Scrape with structured extraction
    result = app.scrape_url(url, params={
        "formats": ["markdown", "html"],
        "extract": {
            "colors": "array of hex color codes used prominently",
            "typography": "font families and key sizes",
            "tone": "brand voice description"
        }
    })
    
    return {
        "url": url,
        "colors": result.get("extract", {}).get("colors", []),
        "typography": result.get("extract", {}).get("typography", ""),
        "tone": result.get("extract", {}).get("tone", ""),
        "raw_markdown": result.get("markdown", "")
    }

# Usage
brand_data = extract_brand_dna("https://stripe.com")
print(json.dumps(brand_data, indent=2))
```

### HTML Deck Structure

Generated decks follow this pattern:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Deck Title</title>
    <style>
        /* Reset */
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        /* Base (follows Rule 15: 8pt grid) */
        body {
            font-family: 'Inter', system-ui, sans-serif;
            font-size: 24px; /* Rule 8: body ≥24px */
            line-height: 1.5; /* Rule 9: 1.4-1.6 */
            background: #FFFFFF;
            color: #1A1A1A; /* Rule 11: 7:1 contrast */
        }
        
        /* Slide container */
        .slide {
            width: 100vw;
            height: 100vh;
            padding: 5%; /* Rule 5: 5% safe-zone */
            display: flex;
            flex-direction: column;
            justify-content: center;
            scroll-snap-align: start;
        }
        
        /* Typography (Rule 6: modular scale 1.25) */
        h1 {
            font-size: 64px; /* 24 × 1.25³ */
            font-weight: 700;
            line-height: 1.1; /* Rule 9: display 1.05-1.2 */
            margin-bottom: 48px; /* Rule 17: ≥48px unrelated */
        }
        
        h2 {
            font-size: 48px; /* Rule 8: title ≥48px */
            font-weight: 600;
            margin-bottom: 32px;
        }
        
        /* Max line length (Rule 10: ≤60 chars) */
        p, ul {
            max-width: 40em; /* ~60 chars at 24px */
            margin-bottom: 16px; /* Rule 17: ≤16px related */
        }
        
        /* Accent (Rule 13: one per slide) */
        .accent {
            color: #0066FF;
            font-weight: 600;
        }
        
        /* Navigation */
        .nav {
            position: fixed;
            bottom: 5%;
            right: 5%;
            font-size: 18px;
            opacity: 0.5;
        }
    </style>
</head>
<body>
    <!-- Slide 1: Title (Rule 1: one idea) -->
    <section class="slide">
        <h1>Introducing<br><span class="accent">Data Pipeline v2</span></h1>
        <p style="font-size: 32px; opacity: 0.7;">Ship faster. Scale smarter.</p>
    </section>
    
    <!-- Slide 2: Key point (Rule 3: 3-5 chunks) -->
    <section class="slide">
        <h2>10× Faster Ingestion</h2>
        <ul style="font-size: 28px; line-height: 1.6;">
            <li>Parallel processing across 16 workers</li>
            <li>Smart batching with adaptive backpressure</li>
            <li>Zero data loss guarantees</li>
        </ul>
    </section>
    
    <!-- More slides... -->
    
    <div class="nav">Use ← → to navigate</div>
    
    <script>
        // Arrow key navigation
        let currentSlide = 0;
        const slides = document.querySelectorAll('.slide');
        
        document.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowRight' && currentSlide < slides.length - 1) {
                currentSlide++;
                slides[currentSlide].scrollIntoView({ behavior: 'smooth' });
            } else if (e.key === 'ArrowLeft' && currentSlide > 0) {
                currentSlide--;
                slides[currentSlide].scrollIntoView({ behavior: 'smooth' });
            }
        });
    </script>
</body>
</html>
```

## Common Patterns

### Refining Generated Decks

After initial generation, refine via natural language:

```
> make the title slide more dramatic
> add a chart showing adoption growth
> use more whitespace on slide 3
> change accent color to match our new brand
> add a closing slide with call-to-action
```

The skill maintains context and applies all 20 rules to changes.

### Data Visualization Slides

When generating charts:

```
> add a slide with a bar chart showing revenue by quarter
```

The skill will:
- Apply Rule 18 (data-ink ratio ≥80%): remove gridlines, borders, fills
- Use brand accent color for key data point
- Add direct labels (no legend)
- Ensure WCAG contrast on labels

### Multi-Section Decks

For longer presentations:

```
> create a 15-slide deck with 3 sections: Problem, Solution, Results
```

The skill adds section dividers with distinct visual treatment while maintaining consistency.

### Dark Mode Decks

```
> generate the deck in dark mode
```

Applies Rule 20 (two valid modes) by:
- Inverting background/foreground
- Maintaining 7:1+ contrast
- Adjusting accent colors for dark backgrounds

## Configuration

### Environment Variables

```bash
# Required for URL-based brand extraction
export FIRECRAWL_API_KEY=your_firecrawl_api_key

# Optional: default brand when none specified
export POWER_DESIGN_DEFAULT_BRAND=stripe

# Optional: output directory
export POWER_DESIGN_OUTPUT_DIR=~/presentations
```

### Custom Brand Library Location

```bash
# Use a custom brand directory
export POWER_DESIGN_BRANDS_DIR=~/my-brands
```

Then structure as:
```
~/my-brands/
├── company-a.md
├── company-b.md
└── _template.md
```

## Troubleshooting

### "Brand not found in library"

**Problem:** Requested brand doesn't exist in `brands/` directory

**Solution:**
1. Check spelling: `ls ~/.claude/skills/power-design/brands/ | grep -i "brandname"`
2. Use URL extraction instead: `use brand from https://example.com`
3. Create custom brand using `brands/_template.md`

### Low Contrast Warnings

**Problem:** Generated slides fail WCAG contrast checks

**Solution:**
The skill auto-corrects to 4.5:1 minimum. If you see warnings:
```
> increase contrast between text and background
> use darker text color
```

Or manually edit the generated HTML `<style>` section.

### Firecrawl Extraction Fails

**Problem:** Brand DNA extraction times out or returns empty

**Solution:**
1. Verify API key: `echo $FIRECRAWL_API_KEY`
2. Check URL is publicly accessible
3. Try alternative pages: `/about`, `/brand`, `/press`
4. Fall back to manual brand creation

### Slides Too Text-Heavy

**Problem:** Generated slides violate Rule 2 (glanceable in ≤3 seconds)

**Solution:**
```
> split slide 4 into two slides
> use bullet points instead of paragraphs
> add an icon to represent this concept visually
```

The skill will redistribute content across more slides.

### Typography Not Loading

**Problem:** Custom fonts in brand system don't render

**Solution:**
Ensure brand `.md` file includes web-safe fallbacks:
```markdown
**Sans:** "CustomFont", "Inter", system-ui, sans-serif
```

Or add `@import` in generated HTML:
```html
<style>
  @import url('https://fonts.googleapis.com/css2?family=CustomFont:wght@400;600;700&display=swap');
  /* ... rest of styles ... */
</style>
```

### Chart Data-Ink Issues

**Problem:** Generated charts have too much decoration

**Solution:**
```
> remove the chart gridlines
> use direct labels instead of a legend
> make the bars thinner with more space between
```

Or manually edit SVG/canvas code following Tufte's guidelines in `principles/design-principles.md` Rule 18.

## Advanced Usage

### Batch Generation

```bash
# Generate multiple decks from a list
for brand in stripe linear vercel; do
  claude code --prompt "use power-design; create a product launch deck for ${brand}; content: New AI features - 3x faster, smarter autocomplete, team collaboration; save as ${brand}-launch.html"
done
```

### CI/CD Integration

```yaml
# .github/workflows/generate-decks.yml
name: Generate Presentation Decks

on:
  push:
    paths:
      - 'presentations/*.txt'

jobs:
  generate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Install Power Design
        run: |
          git clone https://github.com/ItsssssJack/power-design ~/.claude/skills/power-design
      
      - name: Generate Decks
        env:
          FIRECRAWL_API_KEY: ${{ secrets.FIRECRAWL_API_KEY }}
        run: |
          for brief in presentations/*.txt; do
            claude code --prompt "use power-design; brand: our-company; content from ${brief}; output: ${brief%.txt}.html"
          done
      
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./presentations
```

### API Integration (Python)

```python
# power_design_api.py
import subprocess
import tempfile
import os

class PowerDesignAPI:
    def __init__(self, brands_dir=None):
        self.brands_dir = brands_dir or os.path.expanduser(
            "~/.claude/skills/power-design/brands"
        )
    
    def list_brands(self):
        """Return list of available pre-built brands"""
        brands = []
        for f in os.listdir(self.brands_dir):
            if f.endswith('.md') and f != '_template.md':
                brands.append(f.replace('.md', ''))
        return sorted(brands)
    
    def generate(self, brand, content, output_path=None):
        """
        Generate deck with Power Design
        
        Args:
            brand: Brand name from library or URL
            content: Dict with 'headline' and 'points' list
            output_path: Where to save HTML (temp file if None)
        
        Returns:
            Path to generated HTML file
        """
        if output_path is None:
            fd, output_path = tempfile.mkstemp(suffix='.html')
            os.close(fd)
        
        headline = content.get('headline', 'Untitled')
        points = content.get('points', [])
        points_text = '\n'.join(f"- {p}" for p in points)
        
        prompt = f"""
        use power-design
        
        Brand: {brand}
        
        Headline: {headline}
        
        Key points:
        {points_text}
        
        Generate slides and save to: {output_path}
        """
        
        result = subprocess.run(
            ["claude", "code", "--prompt", prompt],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if os.path.exists(output_path):
            return output_path
        else:
            raise RuntimeError(f"Generation failed: {result.stderr}")

# Usage
api = PowerDesignAPI()

print("Available brands:", api.list_brands()[:5])

deck_path = api.generate(
    brand="stripe",
    content={
        "headline": "Introducing Stripe Tax",
        "points": [
            "Automate sales tax calculation",
            "150+ jurisdictions supported",
            "Real-time rate updates",
            "One-click integration"
        ]
    }
)

print(f"Deck generated: {deck_path}")
```

## Resources

- **Full principles with citations:** `principles/design-principles.md`
- **Brand library:** `brands/` (72+ pre-built systems)
- **Example deck:** `examples/sample-deck.html`
- **Community:** https://bit.ly/3PATPoL
- **Showcase site:** https://power-design.vercel.app

## Key Takeaways for Agents

1. **Always apply all 20 rules** — they're non-negotiable and research-backed
2. **Brand DNA comes first** — extract or load before generating content
3. **One idea per slide** — split complex topics across multiple slides
4. **Contrast is critical** — aim for WCAG AAA (7:1), minimum AA (4.5:1)
5. **Whitespace is content** — 40%+ ratio makes slides glanceable
6. **Grid everything** — 8pt spacing, single alignment system
7. **Modular type scale** — use 1.25–1.618 ratio, max 4 sizes per slide
8. **Data-ink ratio for charts** — remove all non-essential decoration
9. **F-pattern layout** — headline and key visual top-left
10. **Consistent mode** — pick minimal or rich, stay there

When in doubt, refer to `principles/design-principles.md` for specific thresholds and research citations.
