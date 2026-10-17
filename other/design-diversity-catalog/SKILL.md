---
name: design-diversity-catalog
description: Apply 100 distinct design styles to AI-generated presentations and websites using Claude Code's design-pick skill
triggers:
  - "use a specific design style for my presentation"
  - "apply design-pick to create a unique PPT"
  - "generate a website with a custom design pack"
  - "show me available design packs"
  - "recommend a design style for my landing page"
  - "create editable PowerPoint with professional design"
  - "build a website using velvet-dark-boutique style"
  - "what design packs are available"
---

# Design Diversity Catalog

> Skill by [ara.so](https://ara.so) — Design Skills collection.

This skill enables Claude Code to apply **100 distinct, production-ready design styles** to presentations and websites. Each design pack contains precise specifications for color, typography, layout, charts, diagrams, and anti-patterns, preventing the "AI gray slop" problem where all generated designs look identical.

## What It Does

The `design-pick` skill is a **consumer skill** that:

- Lets you specify a design pack by slug (e.g., `web-velvet-dark-boutique`) to generate styled content
- Recommends 2-3 packs when you describe a desired aesthetic (e.g., "luxury dark tone presentation")
- Bundles 100 design specifications (50 PPT + 50 web) with full color palettes, typography, spacing systems, and layout rules
- Works offline — all pack specifications are bundled in `references/`

**Key principle:** All PPT outputs must be **editable native `.pptx`** files, never full-slide PNG renders. Users must be able to edit text, shapes, and colors in PowerPoint.

## Installation

### Local Project Installation

```bash
# Install skill in current Claude Code project
cp -r skills/design-pick .claude/skills/

# Verify installation
ls .claude/skills/design-pick/SKILL.md
```

### Global Installation

```bash
# Install globally for all Claude Code projects
cp -r skills/design-pick ~/.claude/skills/

# Verify
ls ~/.claude/skills/design-pick/SKILL.md
```

## Using the Skill

### Method 1: Direct Slug Specification

Request a specific design pack by its slug:

```
Use design-pick skill to apply the web-velvet-dark-boutique pack 
and create a product landing page for my SaaS analytics tool
```

```
Apply ppt-corporate-trust-finance pack with design-pick to create 
a Q4 investor presentation from this earnings data
```

### Method 2: Natural Language Recommendation

Describe the desired aesthetic and let the skill recommend packs:

```
I need a professional consulting-style PPT for enterprise clients. 
Use design-pick to recommend and apply an appropriate pack.
```

```
Create a modern, minimalist landing page with clean typography. 
Use design-pick to suggest suitable web packs.
```

### Method 3: Without Claude Code (claude.ai)

1. Browse the catalog at https://design-diversity.vercel.app
2. Open a pack detail page
3. Copy the entire `prompt.md` content
4. Paste into claude.ai chat with your source material
5. Request:

```
Using the design specification above, create an editable native .pptx 
presentation from this outline. Ensure all text, charts, and shapes 
are editable PowerPoint objects, NOT embedded images.
```

## Design Pack Structure

Each pack includes:

```typescript
// Pack metadata structure (meta.yaml)
interface DesignPack {
  slug: string;           // e.g., "web-velvet-dark-boutique"
  title: string;
  category: "ppt" | "web";
  styleAxes: {
    color: string;        // e.g., "dark-rich"
    type: string;         // e.g., "serif-elegant"
    layout: string;       // e.g., "asymmetric-bold"
    space: string;        // e.g., "generous"
    motion: string;       // e.g., "subtle-smooth"
  };
  learnedFrom: string[];  // Open design systems studied
  premium?: boolean;      // Has 5-7 detailed pages
}
```

## Available Pack Categories

### PPT Packs (50 total)

- **Corporate:** Finance, consulting, enterprise trust
- **Creative:** Agency, portfolio, storytelling
- **Technical:** Engineering, data science, research
- **Educational:** Academic, training, workshop
- **Startup:** Pitch decks, product launches

### Web Packs (50 total)

- **E-commerce:** Product pages, boutique stores
- **SaaS:** Landing pages, dashboards, pricing
- **Portfolio:** Creative showcases, case studies
- **Marketing:** Campaign pages, lead generation
- **Content:** Editorial, blogs, documentation

## Accessing Pack Specifications

Within the skill, pack specs are loaded from:

```typescript
// Skill loads from bundled references
const packSpec = await loadReference(
  `design-packs/${category}/${slug}/prompt.md`
);

// Token data for programmatic access
const tokens = await loadReference(
  `design-packs/${category}/${slug}/tokens.json`
);
```

### Example Token Structure

```json
{
  "colors": {
    "primary": "#1a1a2e",
    "accent": "#d4af37",
    "surface": "#16213e",
    "text": {
      "primary": "#eaeaea",
      "secondary": "#a0a0a0"
    }
  },
  "typography": {
    "headings": {
      "family": "Playfair Display",
      "weight": 700,
      "tracking": "-0.02em"
    },
    "body": {
      "family": "Inter",
      "weight": 400,
      "lineHeight": 1.6
    }
  },
  "spacing": {
    "unit": 8,
    "scale": [8, 16, 24, 32, 48, 64, 96]
  }
}
```

## PPT Output Requirements

**Critical:** All PowerPoint outputs must follow these rules:

### ✅ Required

- **Native objects only:** Use `python-pptx` text boxes, shapes, tables, charts
- **Editable text:** All headings, body text, labels must be PowerPoint TextFrame objects
- **Native charts:** Use `pptx.chart` for data visualization when possible
- **Native diagrams:** Build flowcharts/diagrams with AutoShapes and connectors
- **Font embedding:** Embed custom fonts in `.pptx` so recipients see correct typography

### ❌ Prohibited

- **No full-slide PNGs:** Never render HTML/CSS to image and embed as single slide background
- **No text-in-images:** Charts and infographics must have text as separate layers
- **No uneditable renders:** User must be able to click and edit every text element

### Code Example: Creating Editable PPT

```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN

# Load design pack tokens
import json
with open('tokens.json') as f:
    design = json.load(f)

prs = Presentation()
prs.slide_width = Inches(10)
prs.slide_height = Inches(7.5)

# Title slide with native text boxes
slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank layout

# Background shape (editable)
bg = slide.shapes.add_shape(
    1,  # Rectangle
    0, 0,
    prs.slide_width, prs.slide_height
)
bg.fill.solid()
bg.fill.fore_color.rgb = RGBColor.from_string(design['colors']['primary'])

# Title text box (editable)
title_box = slide.shapes.add_textbox(
    Inches(1), Inches(2.5),
    Inches(8), Inches(1.5)
)
title_frame = title_box.text_frame
title_frame.text = "Your Editable Title"
title_frame.paragraphs[0].font.name = design['typography']['headings']['family']
title_frame.paragraphs[0].font.size = Pt(54)
title_frame.paragraphs[0].font.bold = True
title_frame.paragraphs[0].font.color.rgb = RGBColor.from_string(
    design['colors']['text']['primary']
)

# Save as native .pptx
prs.save('output.pptx')
```

## Web Output Patterns

### HTML/CSS Generation

```typescript
// Apply design tokens to React/HTML
interface WebDesignTokens {
  colors: Record<string, string>;
  typography: {
    headings: FontSpec;
    body: FontSpec;
  };
  spacing: {
    unit: number;
    scale: number[];
  };
  breakpoints: Record<string, string>;
}

// Generate CSS from tokens
function generateCSS(tokens: WebDesignTokens): string {
  return `
:root {
  --color-primary: ${tokens.colors.primary};
  --color-accent: ${tokens.colors.accent};
  --font-heading: "${tokens.typography.headings.family}", serif;
  --font-body: "${tokens.typography.body.family}", sans-serif;
  --space-unit: ${tokens.spacing.unit}px;
}

h1, h2, h3 {
  font-family: var(--font-heading);
  font-weight: ${tokens.typography.headings.weight};
  letter-spacing: ${tokens.typography.headings.tracking};
}

body {
  font-family: var(--font-body);
  font-weight: ${tokens.typography.body.weight};
  line-height: ${tokens.typography.body.lineHeight};
  color: ${tokens.colors.text.primary};
  background: ${tokens.colors.surface};
}
`;
}
```

## Browsing the Catalog

### Programmatic Access

```typescript
// Load full catalog index
import catalog from './catalog.json';

interface CatalogEntry {
  slug: string;
  title: string;
  category: 'ppt' | 'web';
  styleAxes: StyleAxes;
  premium: boolean;
  pages?: number;  // Premium packs have 5-7 detailed pages
}

// Filter by category
const webPacks = catalog.filter(p => p.category === 'web');

// Find premium packs
const premiumPacks = catalog.filter(p => p.premium);

// Search by style axis
const darkPacks = catalog.filter(p => 
  p.styleAxes.color.includes('dark')
);
```

### Visual Browsing

Visit https://design-diversity.vercel.app to:

- See preview images for all 100 packs
- Filter by category (PPT/Web) and style axes
- View detailed specifications for premium packs
- Copy `prompt.md` content for claude.ai use

## Common Workflows

### Workflow 1: Quick PPT Generation

```
I have this product launch outline. Use design-pick to recommend 
a modern, bold PPT pack and generate a 10-slide deck as editable 
native PowerPoint. Include title slide, 3 feature slides, customer 
testimonial, pricing comparison table, and CTA slide.
```

### Workflow 2: Brand-Matched Web Page

```
Apply design-pick's web-velvet-dark-boutique pack to create a 
luxury product landing page. Match these brand colors: #1a1a2e, 
#d4af37. Output as single-file HTML with embedded CSS. Include 
hero section, 3-column features, testimonial carousel, and footer.
```

### Workflow 3: Multi-Pack Comparison

```
Show me 3 PPT pack recommendations for a technical architecture 
presentation to engineering leads. Compare their color schemes 
and typography. Generate a sample title slide for each so I can 
choose.
```

## Configuration

No configuration needed — packs are bundled. However, you can extend:

### Adding Custom Packs

```bash
# Create new pack directory
mkdir -p design-packs/web/my-custom-pack

# Required files
touch design-packs/web/my-custom-pack/{prompt.md,tokens.json,meta.yaml,preview.png}

# Update catalog.json
# Add entry following schema v2
```

### Custom Pack Structure

```yaml
# meta.yaml
slug: web-my-custom-pack
title: My Custom Design
category: web
styleAxes:
  color: vibrant-gradient
  type: sans-modern
  layout: grid-structured
  space: compact
  motion: dynamic
learnedFrom:
  - "Material Design"
  - "Apple Human Interface Guidelines"
premium: false
```

## Troubleshooting

### Issue: PPT comes out as images

**Symptom:** Generated `.pptx` has slides as full-page PNG images

**Solution:** Explicitly request in your prompt:
```
Create an EDITABLE NATIVE .pptx where all text, shapes, and charts 
are PowerPoint objects, NOT embedded images. I must be able to click 
and edit any text element.
```

### Issue: Design pack not found

**Symptom:** `Error: Pack 'xyz' not found in references`

**Solution:** 
1. Check slug spelling at https://design-diversity.vercel.app
2. Verify skill installation: `ls .claude/skills/design-pick/references/`
3. Ensure you're using correct category prefix (`ppt-` or `web-`)

### Issue: Fonts don't render correctly

**Symptom:** Output uses fallback fonts instead of pack's specified typography

**Solution:**
- For PPT: Request font embedding in prompt
- For Web: Ensure Google Fonts or font CDN links are included in HTML `<head>`

### Issue: Colors don't match preview

**Symptom:** Generated output has different colors than catalog preview

**Solution:** 
- Check `tokens.json` for authoritative color values
- Request: "Use exact hex codes from the pack's tokens.json"
- Verify your monitor/browser color profile isn't altering previews

## Environment Variables

No API keys required. All pack data is bundled locally.

For catalog site development:

```bash
# site/.env.local (optional)
NEXT_PUBLIC_CATALOG_URL=https://design-diversity.vercel.app
ANALYZE=true  # Enable bundle analysis
```

## Related Resources

- **Catalog Site:** https://design-diversity.vercel.app
- **Contributing Guide:** See `CONTRIBUTING.md` for submitting new packs
- **Pack Sources:** Each pack's `meta.yaml` lists learned design systems
- **License:** MIT for specs/code; see LICENSE file

---

**Remember:** The goal is **design diversity**. Every output should be visually distinct. If two generated presentations look the same, the wrong pack was chosen or the pack spec wasn't fully applied.
