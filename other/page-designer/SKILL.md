---
name: page-designer
description: Design and build landing pages for campaigns. Use when creating quiz funnels, lead magnets, course sales pages, webinar registration pages, or any conversion-focused landing page. Requires a brand bible or design system from /website_brand_analysis. Part of the creative team under /creative_director.
---

# Page Designer

Build conversion-focused landing pages using brand guidelines.

## Prerequisites

Before designing a landing page, ensure you have:
1. **Brand bible** — Run `/website_brand_analysis` first if missing
2. **Design system CSS** — Should exist at `output/{brand}-design-system.css`
3. **Clear offer** — What's the CTA? What does the user get?

## Workflow

1. **Confirm inputs** — Brand bible path, page type, offer details
2. **Load design system** — Read the CSS tokens and component patterns
3. **Draft structure** — Outline sections based on page type template
4. **Build HTML** — Single self-contained file with inline CSS
5. **Review with user** — Send file, get feedback, iterate

## Page Types

### Quiz/Assessment Landing Page
```
Nav (sticky)
Hero (gold bg) — headline + value prop + CTA + meta (time, questions, results)
Discover (cream bg) — 3 cards: what they'll learn
Sample (peach bg) — preview question with interactive styling
Social Proof (navy bg) — big number + logos
Final CTA (cream bg) — repeat primary CTA
Footer (navy bg)
```

### Lead Magnet / Free Resource
```
Nav
Hero — headline + subhead + email capture form
Preview — what's inside (screenshots, outline)
Benefits — 3 key outcomes
Testimonials — social proof
Final CTA — repeat form
Footer
```

### Webinar / Event Registration
```
Nav
Hero — event title + date/time + host + register CTA
What You'll Learn — 3-4 bullet outcomes
Speaker Bio — photo + credibility
Agenda — timeline or topics
Final CTA — urgency element + register
Footer
```

### Course Sales Page
```
Nav
Hero — course name + tagline + price + enroll CTA
Pain Points — problems this solves
Transformation — before/after
Curriculum — modules/lessons
Instructor — bio + credibility
Testimonials
Pricing — card with features
FAQ
Final CTA
Footer
```

## Design Tokens (Example)

Load from `output/{brand}-design-system.css` or use these defaults:

```css
/* Colors */
--navy: #0F1E35;        /* Headers, footer, dark sections */
--gold: #FFCA51;        /* Primary CTAs, hero backgrounds */
--orange: #FF6D33;      /* Hover states, interactive feedback */
--cream: #FFFDF9;       /* Main background */
--peach: #FCE6DF;       /* Accent sections */

/* Typography */
--font-heading: 'Circular Std', system-ui, sans-serif;
--font-body: 'Circular Std', system-ui, sans-serif;

/* Spacing */
--section-lg: 80px;
--section-md: 64px;
--section-sm: 48px;
```

## Component Patterns

### Primary Button (Gold)
```css
.btn-primary {
  background: var(--gold);
  color: var(--navy);
  padding: 16px 32px;
  border-radius: 8px;
  font-weight: 700;
  box-shadow: 0 4px 20px rgba(255, 202, 81, 0.4);
}
.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 32px rgba(255, 202, 81, 0.5);
}
```

### Card with Orange Hover Accent
```css
.card {
  background: white;
  border-radius: 12px;
  border: 1px solid rgba(15, 30, 53, 0.08);
  transition: all 0.25s ease;
}
.card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 3px;
  background: var(--orange);
  opacity: 0;
  transition: opacity 0.25s;
}
.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 32px rgba(15, 30, 53, 0.12);
}
.card:hover::before { opacity: 1; }
```

### Link Hover → Orange
```css
a { transition: color 0.15s; }
a:hover { color: var(--orange); }
```

## Output

- **File**: `output/{brand}-landing-{page-type}.html`
- **Format**: Single self-contained HTML (inline CSS, no external deps except fonts)
- **Responsive**: Mobile-first, breakpoints at 768px and 1024px

## Quality Checklist

- [ ] All sections use correct background colors (cream/peach/gold/navy)
- [ ] Primary CTAs are gold with navy text
- [ ] Interactive elements hover to orange
- [ ] Typography matches brand fonts from design system
- [ ] Hero has subtle depth (gradient or shadow)
- [ ] Cards lift on hover with orange top accent
- [ ] Footer links hover to orange
- [ ] Mobile responsive (stacked grids, adjusted padding)
