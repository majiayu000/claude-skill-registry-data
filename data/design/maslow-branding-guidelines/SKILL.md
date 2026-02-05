---
name: maslow-branding-guidelines
description: Maslow AI brand tokens - colors, typography, interaction states. Use with any UI framework.
---

# Maslow AI Brand Guidelines

Brand tokens and color usage rules for Maslow AI.

---

## Color System

### Primary Brand Colors

The three colors that form the Maslow logo and represent core service lines.

| Name | Hex | Role |
|------|-----|------|
| **Teal** | #6DC4AD | Primary CTA, Technology services |
| **Pink** | #EE7BB3 | Strategy services, Logo accent |
| **Purple** | #401877 | Brand hero, Premium contexts |

### Secondary Colors

| Name | Hex | Role |
|------|-----|------|
| Blue | #469DBB | Information, Links |
| Orange | #F3A326 | Warnings, Highlights |
| Purple Light | #A070A6 | Design services, Logo middle |

### Extended Palette

#### Teal Variants
| Name | Hex |
|------|-----|
| Teal Primary | #6DC4AD |
| Teal Light | #73C1AE |
| Teal Alt | #60C3AE |
| Teal Tint (Selection) | #EBF7F4 |

#### Pink Variants
| Name | Hex |
|------|-----|
| Pink Primary | #EE7BB3 |
| Pink Muted | #DA85B2 |

#### Purple Variants
| Name | Hex |
|------|-----|
| Purple Primary | #401877 |
| Purple Magenta | #9D4B8E |
| Purple Light | #A070A6 |
| Purple Alt | #A56FA8 |

#### Orange/Warm Variants
| Name | Hex |
|------|-----|
| Orange Primary | #F3A326 |
| Orange Soft | #EBA93D |
| Yellow | #FFF860 |
| Red | #D52C2C |
| Coral | #E19379 |

#### Status Colors
| Name | Hex | Use |
|------|-----|-----|
| Green | #2CD552 | Success, Open status |
| Red | #D52C2C | Error, Closed status |
| Orange | #F3A326 | Warning |
| Blue | #469DBB | Info |

### Neutral Colors

| Name | Hex | Use |
|------|-----|-----|
| Black | #333333 | Primary text (light mode) |
| Gray | #A5A5A5 | Secondary text |
| Silver Background | #E6EAF3 | Light mode page background |
| Light Gray | #EEEEEE | Alternate backgrounds |
| White | #FFFFFF | Cards, surfaces |
| **Dark Blue** | #121D35 | Dark mode background, emphasis bands |

---

## Light & Dark Mode

### Light Mode

| Token | Value | Use |
|-------|-------|-----|
| `--background` | #E6EAF3 | Page background |
| `--surface` | #FFFFFF | Cards, panels |
| `--surface-alt` | #EEEEEE | Alternate sections |
| `--text-primary` | #333333 | Headings, body |
| `--text-secondary` | #A5A5A5 | Captions, muted |
| `--border` | #D0D5E0 | Dividers, outlines |

### Dark Mode

| Token | Value | Use |
|-------|-------|-----|
| `--background` | #121D35 | Page background |
| `--surface` | #1A2847 | Cards, panels |
| `--surface-alt` | #243356 | Alternate sections |
| `--text-primary` | #FFFFFF | Headings, body |
| `--text-secondary` | #B8C4D9 | Captions, muted |
| `--border` | #3A4A6B | Dividers, outlines |

### Dark Band (Emphasis Section)

Use `#121D35` as a full-width background within light mode pages to create visual hierarchy. This is NOT a full dark mode—it's a design element.

```css
.dark-band {
  background-color: #121D35;
  color: #FFFFFF;
}
.dark-band .accent {
  color: #6DC4AD; /* Teal pops on dark */
}
```

---

## Typography

### Font Stack

| Role | Font | Fallback |
|------|------|----------|
| **Primary** | Manrope | system-ui, sans-serif |
| **Secondary** | Graphik | system-ui, sans-serif |

```html
<!-- Google Fonts (Manrope only - Graphik requires license) -->
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@200;300;400;500;600;700;800&display=swap" rel="stylesheet">
```

### Usage

| Element | Font | Weight | Use Case |
|---------|------|--------|----------|
| H1 Hero | Manrope | 800 | Page titles |
| H2 Section | Manrope | 700 | Section headings |
| H3 Card | Manrope | 600 | Card titles |
| Body | Graphik | 400 | Paragraphs |
| Labels | Graphik | 500 | Navigation, UI |
| Micro | Graphik | 500 | Dates, caps labels |

### Type Scale

| Element | Size | Weight | Line Height |
|---------|------|--------|-------------|
| H1 Hero | 48px | 800 | 1.1 |
| H2 Section | 36px | 700 | 1.2 |
| H3 Card | 24px | 600 | 1.3 |
| Body Large | 18px | 400 | 1.6 |
| Body | 16px | 400 | 1.6 |
| Caption | 14px | 500 | 1.5 |
| Micro | 12px | 500 | 1.5 |
| Small Caps | 11px | 500 | 1.5 |

### Headline Pattern

The brand uses a distinctive headline style: **bold keyword** + regular supporting text.

```html
<h1>
  <span class="bold">At Maslow</span><br>
  <span class="light">we turn big data into<br>business success stories</span>
</h1>
```

```css
.bold { font-weight: 800; color: #333333; }
.light { font-weight: 400; color: #A5A5A5; }
```

---

## Logo

### Color Logo Components

The Maslow logo uses three overlapping elements:

| Position | Color | Hex |
|----------|-------|-----|
| Left | Pink | #EE7BB3 |
| Center | Purple Light | #A070A6 |
| Right | Teal | #6DC4AD |

### Logo Variants

| Variant | Use Case |
|---------|----------|
| Color (Full) | Primary usage on light backgrounds |
| Color (Squared) | App icons, favicons |
| Black | Single-color printing, dark backgrounds |
| White | Dark backgrounds, overlays |

### Logo + Wordmark

```
[Logo] MASLOW | AI
```

- **MASLOW**: Manrope, weight 800, letter-spacing 0.02em
- **|**: Vertical bar separator
- **AI**: Manrope, weight 300 (light)

---

## Semantic Color Mapping

### Service Lines

| Service | Primary Color | Hex |
|---------|--------------|-----|
| **Strategy** | Pink | #EE7BB3 |
| **Technology** | Teal | #6DC4AD |
| **Design** | Purple Light | #A070A6 |

### Colored Keyword Headlines

```html
<h2>
  <span style="color: #EE7BB3">Strategic</span> navigation,
  flawless execution
</h2>

<h2>
  <span style="color: #6DC4AD">Technology</span> savvy,
  usability geniuses
</h2>

<h2>
  <span style="color: #A070A6">Design</span> expertise,
  user empathetic
</h2>
```

---

## Accent Lines

Thin horizontal lines (2-3px) in brand colors are a signature design element.

```css
.accent-line {
  height: 3px;
  width: 60px;
  background-color: var(--maslow-teal);
}

.accent-line-full {
  height: 3px;
  width: 100%;
  background-color: var(--maslow-pink);
}
```

---

## Interaction States

### Selection & Hover

Use light teal background with teal left border for selected/hover states on list items.

| State | Background | Border |
|-------|------------|--------|
| Default | transparent | none |
| Hover | #EBF7F4 | none |
| Selected/Active | #EBF7F4 | 3px left #6DC4AD |

```css
.list-item:hover {
  background-color: #EBF7F4;
}
.list-item.selected {
  background-color: #EBF7F4;
  border-left: 3px solid #6DC4AD;
}
```

### Focus States

Use brand colors for focus rings, not browser defaults.

```css
:focus-visible {
  outline: 2px solid #6DC4AD;
  outline-offset: 2px;
}
```

---

## Content-Type Badges

Assign badge colors by content type for consistency across the site.

| Content Type | Badge Color | Hex |
|--------------|-------------|-----|
| Case Study | Purple | #401877 |
| Article | Coral | #E19379 |
| Insight | Teal | #6DC4AD |
| News | Orange | #F3A326 |

```css
.badge-case-study { background: #401877; color: #FFFFFF; }
.badge-article { background: #E19379; color: #FFFFFF; }
.badge-insight { background: #6DC4AD; color: #333333; }
.badge-news { background: #F3A326; color: #333333; }
```

---

## Button Hierarchy

| Button Type | Background | Text | Use Case |
|-------------|------------|------|----------|
| Primary | #333333 | #FFFFFF | Main CTA ("Contact us") |
| Accent | #6DC4AD | #FFFFFF | Secondary CTA |
| Submit | #E19379 | #FFFFFF | Form submissions |
| Ghost | transparent | #333333 | Tertiary actions |

```css
.btn-primary { background: #333333; color: #FFFFFF; }
.btn-accent { background: #6DC4AD; color: #FFFFFF; }
.btn-submit { background: #E19379; color: #FFFFFF; }
.btn-ghost { background: transparent; color: #333333; border: 2px solid #D0D5E0; }
```

---

## Action Links

Use Orange for action text links.

```css
.action-link {
  color: #F3A326;
  text-transform: uppercase;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.05em;
}
```

Examples: "READ ARTICLE →", "VIEW CASE STUDY →", "LEARN MORE →"

---

## Text Emphasis

### On Dark Backgrounds

Use Yellow/Orange for highlighting keywords on dark backgrounds or hero images.

```css
.hero-text .highlight {
  color: #F3A326;
}
```

Example: "At Maslow, we build **web applications** that delight users."

### On Light Backgrounds

Use brand colors (Teal, Pink, Purple) for emphasis per semantic meaning.

---

## Callouts & Quotes

Use Teal quotation mark with light teal background.

| Element | Color | Hex |
|---------|-------|-----|
| Quote icon | Teal | #6DC4AD |
| Background | Light Teal | #EBF7F4 |
| Text | Dark | #333333 |

```css
.callout {
  background: #EBF7F4;
  padding: 24px;
  border-radius: 8px;
}
.callout-icon {
  color: #6DC4AD;
  font-size: 48px;
}
```

---

## Gradients

```css
/* Logo gradient */
linear-gradient(135deg, #EE7BB3, #A070A6, #6DC4AD)

/* Hero gradient (dark) */
linear-gradient(135deg, #401877 0%, #121D35 100%)

/* Teal to Purple */
linear-gradient(135deg, #6DC4AD, #401877)

/* Warm gradient */
linear-gradient(135deg, #F3A326, #EE7BB3)
```

---

## Spacing Scale

Base unit: 4px

| Token | Value |
|-------|-------|
| `--space-1` | 4px |
| `--space-2` | 8px |
| `--space-3` | 12px |
| `--space-4` | 16px |
| `--space-5` | 20px |
| `--space-6` | 24px |
| `--space-8` | 32px |
| `--space-10` | 40px |
| `--space-12` | 48px |
| `--space-16` | 64px |
| `--space-20` | 80px |
| `--space-24` | 96px |

---

## Border Radius

| Token | Value |
|-------|-------|
| `--radius-sm` | 4px |
| `--radius-md` | 8px |
| `--radius-lg` | 12px |
| `--radius-xl` | 16px |
| `--radius-2xl` | 24px |
| `--radius-full` | 9999px |

---

## Brand Guidelines

### ✅ DO

- Use Teal #6DC4AD for primary CTAs
- Use Pink #EE7BB3 for Strategy-related content
- Use Purple #401877 for premium/hero moments
- Use Dark Blue #121D35 for dark bands within light pages
- Use Manrope for headings, Graphik for body
- Include accent lines as visual separators
- Map service colors consistently (Strategy=Pink, Tech=Teal, Design=Purple)

### ❌ DON'T

- Use generic AI purple (#a855f7, #8b5cf6) — use #401877
- Use pure black (#000000) — use #333333
- Use cyan (#06b6d4) — use #469DBB
- Mix more than 2 fonts
- Use the logo colors outside logo context without purpose
- Put light text on Pink or Teal backgrounds (use dark text)

### Text Contrast

| Background | Text Color |
|------------|-----------|
| #401877 (Purple) | White #FFFFFF |
| #121D35 (Dark Blue) | White #FFFFFF |
| #6DC4AD (Teal) | Dark #333333 |
| #EE7BB3 (Pink) | Dark #333333 |
| #F3A326 (Orange) | Dark #333333 |

---

## CSS Custom Properties

```css
:root {
  /* Primary */
  --maslow-teal: #6DC4AD;
  --maslow-pink: #EE7BB3;
  --maslow-purple: #401877;
  
  /* Secondary */
  --maslow-blue: #469DBB;
  --maslow-orange: #F3A326;
  --maslow-purple-light: #A070A6;
  
  /* Teal Variants */
  --teal-primary: #6DC4AD;
  --teal-light: #73C1AE;
  --teal-alt: #60C3AE;
  
  /* Pink Variants */
  --pink-primary: #EE7BB3;
  --pink-muted: #DA85B2;
  
  /* Purple Variants */
  --purple-primary: #401877;
  --purple-magenta: #9D4B8E;
  --purple-light: #A070A6;
  --purple-alt: #A56FA8;
  
  /* Orange/Warm Variants */
  --orange-primary: #F3A326;
  --orange-soft: #EBA93D;
  --yellow: #FFF860;
  --red: #D52C2C;
  --coral: #E19379;
  
  /* Status */
  --status-success: #2CD552;
  --status-error: #D52C2C;
  --status-warning: #F3A326;
  --status-info: #469DBB;
  
  /* Interaction States */
  --state-hover-bg: #EBF7F4;
  --state-selected-bg: #EBF7F4;
  --state-selected-border: #6DC4AD;
  --state-focus-ring: #6DC4AD;
  
  /* Content Badges */
  --badge-case-study: #401877;
  --badge-article: #E19379;
  --badge-insight: #6DC4AD;
  --badge-news: #F3A326;
  
  /* Neutrals */
  --black: #333333;
  --gray: #A5A5A5;
  --silver-bg: #E6EAF3;
  --light-gray: #EEEEEE;
  --white: #FFFFFF;
  --dark-blue: #121D35;
  
  /* Light Mode */
  --light-background: #E6EAF3;
  --light-surface: #FFFFFF;
  --light-surface-alt: #EEEEEE;
  --light-text-primary: #333333;
  --light-text-secondary: #A5A5A5;
  --light-border: #D0D5E0;
  
  /* Dark Mode */
  --dark-background: #121D35;
  --dark-surface: #1A2847;
  --dark-surface-alt: #243356;
  --dark-text-primary: #FFFFFF;
  --dark-text-secondary: #B8C4D9;
  --dark-border: #3A4A6B;
  
  /* Typography */
  --font-primary: 'Manrope', system-ui, sans-serif;
  --font-secondary: 'Graphik', system-ui, sans-serif;
  
  /* Spacing */
  --space-1: 0.25rem;
  --space-2: 0.5rem;
  --space-3: 0.75rem;
  --space-4: 1rem;
  --space-5: 1.25rem;
  --space-6: 1.5rem;
  --space-8: 2rem;
  --space-10: 2.5rem;
  --space-12: 3rem;
  --space-16: 4rem;
  --space-20: 5rem;
  --space-24: 6rem;
  
  /* Radius */
  --radius-sm: 0.25rem;
  --radius-md: 0.5rem;
  --radius-lg: 0.75rem;
  --radius-xl: 1rem;
  --radius-2xl: 1.5rem;
  --radius-full: 9999px;
}
```

---

## Tailwind Config Extension

```js
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        maslow: {
          teal: '#6DC4AD',
          pink: '#EE7BB3',
          purple: '#401877',
          blue: '#469DBB',
          orange: '#F3A326',
          'purple-light': '#A070A6',
        },
        brand: {
          'teal-light': '#73C1AE',
          'teal-alt': '#60C3AE',
          'pink-muted': '#DA85B2',
          'purple-magenta': '#9D4B8E',
          'purple-alt': '#A56FA8',
          'orange-soft': '#EBA93D',
          yellow: '#FFF860',
          red: '#D52C2C',
          coral: '#E19379',
          green: '#2CD552',
        },
        neutral: {
          black: '#333333',
          gray: '#A5A5A5',
          silver: '#E6EAF3',
          'light-gray': '#EEEEEE',
        },
        dark: {
          blue: '#121D35',
          surface: '#1A2847',
          'surface-alt': '#243356',
          border: '#3A4A6B',
          text: '#B8C4D9',
        },
        state: {
          hover: '#EBF7F4',
          selected: '#EBF7F4',
          'selected-border': '#6DC4AD',
          focus: '#6DC4AD',
        },
        badge: {
          'case-study': '#401877',
          article: '#E19379',
          insight: '#6DC4AD',
          news: '#F3A326',
        },
      },
      fontFamily: {
        display: ['Manrope', 'system-ui', 'sans-serif'],
        body: ['Graphik', 'system-ui', 'sans-serif'],
      },
    },
  },
}
```

---

## Quick Reference Card

| Use Case | Color | Hex |
|----------|-------|-----|
| Primary CTA | Teal | #6DC4AD |
| Hero/Brand | Purple | #401877 |
| Strategy content | Pink | #EE7BB3 |
| Technology content | Teal | #6DC4AD |
| Design content | Purple Light | #A070A6 |
| Dark sections | Dark Blue | #121D35 |
| Light background | Silver | #E6EAF3 |
| Body text (light) | Black | #333333 |
| Body text (dark) | White | #FFFFFF |
| Success | Green | #2CD552 |
| Error | Red | #D52C2C |
| Warning | Orange | #F3A326 |