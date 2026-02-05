---
name: rdc-brand-style-guide
description: Realtor.com brand guidelines for creating branded reports, presentations, dashboards, and visualizations. Includes official colors, typography, logo usage rules, and styling guidance. Use when creating reports, HTML dashboards, presentations, charts, or any deliverable that should follow RDC brand standards. Triggers include requests for "branded" outputs, company presentations, executive reports, slide decks, or visualizations needing consistent Realtor.com styling.
---

# RDC Brand Style Guide

Reference for creating on-brand reports, presentations, and visualizations.

## Brand Assets

### Included Logo Files
This skill includes commonly used logo assets in the `assets/` folder:
- `logo-primary.svg` - Full color logo (house icon + wordmark)
- `icon-home.svg` - Standalone home icon for small sizes/favicons

**Raw URLs for embedding:**
```
https://raw.githubusercontent.com/MoveRDC/claude-skills-marketing/main/skills/rdc-brand-style-guide/assets/logo-primary.svg
https://raw.githubusercontent.com/MoveRDC/claude-skills-marketing/main/skills/rdc-brand-style-guide/assets/icon-home.svg
```

### Additional Brand Assets
For additional logos, icons, photography, and brand resources:
**Brand Asset Portal**: https://dam.gettyimages.com/realtor/brand-assets

## Primary Color Palette

| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| **Realtor Red 600** | #D92228 | 217, 34, 40 | Primary brand color, accents, CTAs, highlights |
| **Realtor Red 700** | #B81D22 | 184, 29, 34 | Darker red for hover states, depth |
| **Warm Gray 100** | #F2F0EF | 242, 240, 239 | Light backgrounds |
| **Warm Gray 200** | #E9E7E4 | 233, 231, 228 | Card backgrounds, subtle dividers |
| **Warm Gray 400** | #BEB8B0 | 190, 184, 176 | Borders, disabled states |
| **Warm Gray 1200** | #1A1816 | 26, 24, 22 | Primary text, near-black |

**Key rule**: Use red sparingly as an accent. Never use red as large fields of color. Rely on warm grays for most of the design with red highlights for clarity and branding.

## Secondary Palette (Internal Communications Only)

| Name | Hex | Usage |
|------|-----|-------|
| Orange | #CC4E00 | Warnings, alerts |
| Teal | #008583 | Positive indicators, success |
| Teal Dark | #0D3D3B | Dark teal accent |
| Blue | #0D74CE | Links, informational |
| Blue Dark | #113264 | Chart series, headers |
| Brown | #582D1D | Earthy accent |
| Purple Bright | #C2298A | Highlights |
| Purple | #953EA3 | Chart series |
| Purple Dark | #651249 | Dark accent |
| Purple Dark 2 | #53195D | Deepest purple |

## Typography

### Primary Fonts
| Font | Weight | Usage |
|------|--------|-------|
| **Galano Grotesque** | Bold | Headlines, impact text |
| **Galano Grotesque** | Medium | Body copy, supporting text |

### Fallback Fonts by Context
| Context | Font | Weights |
|---------|------|---------|
| Google Slides/Docs/Sheets | **Poppins** | Extra Bold (headlines), Normal (body) |
| Email | **Helvetica** | Bold (headlines), Regular (body) |
| Web (no custom fonts) | Arial, Helvetica | Bold, Regular |

### Typesetting Rules
- **Headlines**: 120% leading, optical spacing, 0 kerning
- **Body**: 50% of headline size, 140% leading, optical spacing
- **Spacing**: 100% of headline size between headline and body

## Text Style Guidelines

### Capitalization
- Use **sentence case** for headlines, subheads, and CTAs
- Capitalize only proper nouns

### Punctuation
- No punctuation at end of headlines unless: question, exclamation, or internal punctuation needed
- If one headline in a series needs punctuation, add to all for consistency
- Use **Oxford comma** in lists (the comma before "and")
- Address consumers with commas, never colons

## Logo Usage

### Versions
- **Primary Logo**: House icon + wordmark (preferred) → `assets/logo-primary.svg`
- **Mini Logo**: Optimized for small sizes
- **Home Icon Only**: Use when brand is well-established → `assets/icon-home.svg`

### Rules
- Minimum size: **150px width / 1.15 inches**
- Clearspace: Size of one home icon on all sides
- Use over white, gray, or light backgrounds
- On dark/complex backgrounds: Use white pill shape behind logo

### Don'ts
- Don't use wordmark alone
- Don't add drop shadows
- Don't change logo colors
- Don't stack the logo
- Don't place over complex backgrounds without pill

## Chart & Visualization Guidelines

### Standard Time Series / YoY Comparison Charts
| Series | Color | Hex | Usage |
|--------|-------|-----|-------|
| **Primary / Current** | Realtor Red | #D92228 | Current year, main metric (e.g., 2025) |
| **Secondary / Prior** | Black | #1A1816 | Prior year, comparison (e.g., 2024) |
| **Difference / Variance** | Light Gray | #BEB8B0 | % Diff bars, YoY change, variance |
| **Target / Goal** | Teal | #008583 | Target lines, benchmarks, goals |

### Multi-Series Charts (Non-YoY)
When comparing multiple metrics or categories:
1. Realtor Red (#D92228) - Primary/featured series
2. Blue (#0D74CE) - Secondary series
3. Teal (#008583) - Tertiary series
4. Orange (#CC4E00) - Fourth series or warnings
5. Purple (#953EA3) - Additional series
6. Black (#1A1816) - Reference/baseline

### Best Practices
- Use red for the "current" or "focus" data series
- Black/dark gray for historical comparison
- Light gray for difference/variance indicators (bars behind lines)
- Teal for targets, goals, or benchmarks
- Keep gridlines and axis labels in Warm Gray 400 (#BEB8B0)
- Use Warm Gray 1200 (#1A1816) for axis titles and labels

## Status/Semantic Colors

| Status | Color | Hex |
|--------|-------|-----|
| Positive/Success | Teal | #008583 |
| Warning/Caution | Orange | #CC4E00 |
| Error/Negative | Realtor Red 600 | #D92228 |
| Info | Blue | #0D74CE |

## Quick Reference: CSS Variables

```css
:root {
  /* Primary Brand */
  --rdc-red-600: #D92228;
  --rdc-red-700: #B81D22;
  
  /* Warm Grays */
  --rdc-gray-100: #F2F0EF;
  --rdc-gray-200: #E9E7E4;
  --rdc-gray-400: #BEB8B0;
  --rdc-gray-1200: #1A1816;
  
  /* Secondary Palette */
  --rdc-orange: #CC4E00;
  --rdc-teal: #008583;
  --rdc-teal-dark: #0D3D3B;
  --rdc-blue: #0D74CE;
  --rdc-blue-dark: #113264;
  
  /* Chart Colors - YoY Pattern */
  --chart-current: #D92228;      /* Red - current year/primary */
  --chart-prior: #1A1816;        /* Black - prior year/comparison */
  --chart-diff: #BEB8B0;         /* Light gray - variance bars */
  --chart-target: #008583;       /* Teal - targets/goals */
  
  /* Typography */
  --font-primary: 'Galano Grotesque', 'Poppins', Arial, sans-serif;
  --font-headline-weight: 700;
  --font-body-weight: 500;
}
```

## Report Structure Templates

### Executive Report
- Header: Warm Gray 100 background, Realtor Red accent line
- Section headers: Warm Gray 1200 text, Galano Bold
- KPI cards: White background, red for key numbers only
- Charts: Blue palette primary, red for featured callouts

### Data Dashboard
- Background: White or Warm Gray 100
- Cards: White with Warm Gray 200 borders
- Headers: Warm Gray 1200
- Accent: Single red element per section maximum

### Presentation Slides
- Title slides: Bold headline, minimal red accent
- Content slides: High contrast, generous whitespace
- Data slides: Blue chart palette, red highlights sparingly
- Use Poppins in Google Slides
