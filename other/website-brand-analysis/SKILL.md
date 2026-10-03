---
name: website-brand-analysis
description: Analyze a website and generate a comprehensive brand bible (positioning, offers, voice, visual style, layout patterns) PLUS extractable design tokens for page building. Screenshots sent live during analysis. Use when creating brand guidelines, style guides, or preparing context for LLM-powered content/design.
---

# Website Brand Analysis

Generate a comprehensive brand bible from a website, suitable for dropping into LLM context for copy and design work.

**Outputs:**
1. `{brand}-brand-bible.md` — Positioning, voice, copy guidelines
2. `{brand}-design-system.css` — Extractable CSS variables and component styles for `/page_designer`

## Workflow

### Phase 1: Live Crawl & Screenshot

**IMPORTANT: Send each screenshot to the user via Telegram immediately after capturing it.**

This creates a visual, demo-friendly experience where the user sees progress in real-time.

```
For each page:
1. Navigate to page
2. Take full-page screenshot
3. IMMEDIATELY send to user via message tool with caption (page name)
4. Extract key data (colors, fonts, copy patterns)
5. Move to next page
```

**Pages to analyze (in order):**
1. Homepage
2. Main product/service pages (look for nav links)
3. Pricing page (if exists)
4. About page (if exists)
5. Blog/content page (for tone analysis)
6. Any course/offer detail pages
7. Contact/demo page

**For each page, extract:**
- Screenshot (full page)
- Key copy (headlines, CTAs, value props)
- Visual patterns (colors via computed styles, layout structure)

### Phase 2: Checkpoint with User

**STOP before writing the report and check in:**

```
"Here's what I've analyzed so far:
• Homepage
• [Product page 1]
• [Product page 2]
• [Pricing]
• [etc.]

Are there any other pages I should check before I generate the brand bible?"
```

**Wait for user response.** They may point out:
- Missing product pages
- Specific landing pages
- Case studies or examples
- Other important sections

If user provides additional pages, go back to Phase 1 for those pages.

### Phase 3: Extract Design System

Before generating the brand bible, extract actual CSS values from the site.

**Run this extraction script on the homepage (or most representative page):**

```javascript
// Extract design tokens via browser evaluate
(() => {
  const styles = {
    colors: {},
    typography: {},
    spacing: {},
    borders: {},
    shadows: {},
    components: {}
  };
  
  // Get CSS custom properties from :root
  const rootStyles = getComputedStyle(document.documentElement);
  const cssVars = {};
  for (const prop of document.styleSheets) {
    try {
      for (const rule of prop.cssRules) {
        if (rule.selectorText === ':root') {
          for (const style of rule.style) {
            if (style.startsWith('--')) {
              cssVars[style] = rule.style.getPropertyValue(style).trim();
            }
          }
        }
      }
    } catch(e) {}
  }
  styles.cssVariables = cssVars;
  
  // Sample key elements
  const h1 = document.querySelector('h1');
  const h2 = document.querySelector('h2');
  const p = document.querySelector('p');
  const btn = document.querySelector('button, .btn, [class*="button"]');
  const card = document.querySelector('[class*="card"], .card');
  const nav = document.querySelector('nav, header');
  
  if (h1) {
    const s = getComputedStyle(h1);
    styles.typography.h1 = {
      fontFamily: s.fontFamily,
      fontSize: s.fontSize,
      fontWeight: s.fontWeight,
      lineHeight: s.lineHeight,
      letterSpacing: s.letterSpacing,
      color: s.color
    };
  }
  
  if (h2) {
    const s = getComputedStyle(h2);
    styles.typography.h2 = {
      fontFamily: s.fontFamily,
      fontSize: s.fontSize,
      fontWeight: s.fontWeight,
      lineHeight: s.lineHeight,
      color: s.color
    };
  }
  
  if (p) {
    const s = getComputedStyle(p);
    styles.typography.body = {
      fontFamily: s.fontFamily,
      fontSize: s.fontSize,
      fontWeight: s.fontWeight,
      lineHeight: s.lineHeight,
      color: s.color
    };
  }
  
  if (btn) {
    const s = getComputedStyle(btn);
    styles.components.button = {
      fontFamily: s.fontFamily,
      fontSize: s.fontSize,
      fontWeight: s.fontWeight,
      padding: s.padding,
      borderRadius: s.borderRadius,
      backgroundColor: s.backgroundColor,
      color: s.color,
      border: s.border,
      boxShadow: s.boxShadow
    };
  }
  
  if (card) {
    const s = getComputedStyle(card);
    styles.components.card = {
      padding: s.padding,
      borderRadius: s.borderRadius,
      backgroundColor: s.backgroundColor,
      border: s.border,
      boxShadow: s.boxShadow
    };
  }
  
  if (nav) {
    const s = getComputedStyle(nav);
    styles.components.nav = {
      backgroundColor: s.backgroundColor,
      padding: s.padding,
      borderBottom: s.borderBottom
    };
  }
  
  // Get body background
  styles.colors.background = getComputedStyle(document.body).backgroundColor;
  
  return JSON.stringify(styles, null, 2);
})()
```

**Save extracted values** to reference when generating the design system CSS.

### Phase 4: Generate Brand Bible

Only after user confirms all pages are covered, generate the report.

**Report structure:**

```markdown
# [Brand] Brand Bible

## Table of Contents
1. Positioning & ICP
2. Offers & Products
3. Voice & Tone
4. Copy Guidelines
5. Visual Style
6. Layout Patterns

## Positioning & ICP
- Who they are (one-line summary)
- Core value proposition
- Target audience (primary + secondary)
- Pain points they address
- Positioning statement
- Competitive differentiation

## Offers & Products
- Product/service table with prices
- Product structure/tiers
- Guarantee/risk reversal (if any)

## Voice & Tone
- Overall voice description
- Tone attributes (with examples)
- Do's and Don'ts
- Headline patterns
- Common phrases/language
- Section labels they use

## Copy Guidelines
- Headline patterns (with examples)
- Subheadline patterns
- Body copy style
- CTA patterns
- Social proof copy patterns
- Feature/benefit copy patterns

## Visual Style
- Color palette (hex, RGB, usage)
- Typography (fonts, weights, sizes)
- Imagery style (photos, graphics, icons)
- Spacing & layout values
- Border radius, shadows
- Component patterns (buttons, cards, etc.)

## Layout Patterns
- Page structure patterns
- Grid system
- Section backgrounds
- Responsive behavior

## Summary
One-page brand overview for quick reference
```

### Phase 4: Deliver

1. Save markdown to `~/aries-app/artifacts/output/{brand-slug}-brand-bible.md` (or the path configured via `ARTIFACT_PIPELINE_CWD`)
2. Send file to user via Telegram
3. Offer to expand any section or add screenshots to a zip

## Technical Notes

### Extracting Colors & Fonts

```javascript
// Run via browser evaluate
(() => {
  const allElements = document.querySelectorAll('*');
  const colors = new Set();
  const fonts = new Set();
  allElements.forEach(el => {
    const s = getComputedStyle(el);
    if (s.color) colors.add(s.color);
    if (s.backgroundColor) colors.add(s.backgroundColor);
    if (s.fontFamily) fonts.add(s.fontFamily);
  });
  return JSON.stringify({
    colors: [...colors].slice(0, 30),
    fonts: [...fonts].slice(0, 10)
  });
})()
```

### Sending Screenshots Live

```
message action=send channel=telegram target={user_id} filePath={screenshot_path} caption="{Page Name}"
```

Always send immediately after capturing — don't batch them.

### Finding Pages to Analyze

1. Check navigation menu for main sections
2. Look for footer links (often has full sitemap)
3. Check for `/pricing`, `/about`, `/contact`, `/blog` standard paths
4. Follow CTAs to see product/offer detail pages

## Example Session

```
User: Analyze https://example.com

[Navigate to homepage]
[Screenshot → send to Telegram: "Homepage"]

[Navigate to /pricing]
[Screenshot → send to Telegram: "Pricing page"]

[Navigate to /product]
[Screenshot → send to Telegram: "Product page"]

[Navigate to /about]
[Screenshot → send to Telegram: "About page"]

Agent: "Here's what I've analyzed:
• Homepage
• Pricing page
• Product page
• About page

Any other pages I should check before generating the brand bible?"

User: "Also check /features and /case-studies"

[Navigate to /features]
[Screenshot → send to Telegram: "Features page"]

[Navigate to /case-studies]
[Screenshot → send to Telegram: "Case Studies page"]

Agent: "Got those too. Ready to generate the report?"

User: "Yes"

[Generate brand bible markdown]
[Send file to user]
```

## Output

### 1. Brand Bible (Markdown)
`~/aries-app/artifacts/output/{brand-slug}-brand-bible.md`
- Positioning, offers, voice, copy guidelines
- For content/copy work

### 2. Design System (CSS)
`~/aries-app/artifacts/output/{brand-slug}-design-system.css`
- Actual extracted CSS variables
- Component styles
- For `/page_designer` to use

**Design System CSS structure:**

```css
/* {Brand} Design System
 * Extracted from {url} on {date}
 * Use with /page_designer skill
 */

/* ========== COLORS ========== */
:root {
  /* Primary */
  --color-primary: {extracted};
  --color-primary-hover: {extracted};
  
  /* Secondary/Accent */
  --color-accent: {extracted};
  --color-accent-hover: {extracted};
  
  /* Neutrals */
  --color-background: {extracted};
  --color-surface: {extracted};
  --color-text: {extracted};
  --color-text-muted: {extracted};
  --color-border: {extracted};
}

/* ========== TYPOGRAPHY ========== */
:root {
  /* Font Families */
  --font-heading: {extracted};
  --font-body: {extracted};
  
  /* Font Sizes */
  --text-xs: {extracted};
  --text-sm: {extracted};
  --text-base: {extracted};
  --text-lg: {extracted};
  --text-xl: {extracted};
  --text-2xl: {extracted};
  --text-3xl: {extracted};
  --text-4xl: {extracted};
  
  /* Font Weights */
  --font-normal: {extracted};
  --font-medium: {extracted};
  --font-semibold: {extracted};
  --font-bold: {extracted};
  
  /* Line Heights */
  --leading-tight: {extracted};
  --leading-normal: {extracted};
  --leading-relaxed: {extracted};
}

/* ========== SPACING ========== */
:root {
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 20px;
  --space-6: 24px;
  --space-8: 32px;
  --space-10: 40px;
  --space-12: 48px;
  --space-16: 64px;
  --space-20: 80px;
}

/* ========== BORDERS & SHADOWS ========== */
:root {
  --radius-sm: {extracted};
  --radius-md: {extracted};
  --radius-lg: {extracted};
  --radius-full: 9999px;
  
  --shadow-sm: {extracted};
  --shadow-md: {extracted};
  --shadow-lg: {extracted};
}

/* ========== COMPONENT STYLES ========== */

/* Buttons */
.btn-primary {
  font-family: var(--font-body);
  font-size: {extracted};
  font-weight: {extracted};
  padding: {extracted};
  border-radius: {extracted};
  background-color: var(--color-primary);
  color: {extracted};
  border: {extracted};
  box-shadow: {extracted};
  transition: all 0.2s;
}

.btn-primary:hover {
  background-color: var(--color-primary-hover);
}

/* Cards */
.card {
  padding: {extracted};
  border-radius: {extracted};
  background-color: var(--color-surface);
  border: {extracted};
  box-shadow: {extracted};
}

/* Navigation */
.nav {
  background-color: {extracted};
  padding: {extracted};
  border-bottom: {extracted};
}

/* Typography Classes */
h1, .h1 {
  font-family: var(--font-heading);
  font-size: var(--text-4xl);
  font-weight: var(--font-bold);
  line-height: var(--leading-tight);
  color: var(--color-text);
}

h2, .h2 {
  font-family: var(--font-heading);
  font-size: var(--text-3xl);
  font-weight: var(--font-bold);
  line-height: var(--leading-tight);
}

h3, .h3 {
  font-family: var(--font-heading);
  font-size: var(--text-2xl);
  font-weight: var(--font-semibold);
}

p, .body {
  font-family: var(--font-body);
  font-size: var(--text-base);
  line-height: var(--leading-relaxed);
  color: var(--color-text-muted);
}

/* Container */
.container {
  max-width: {extracted or 1200px};
  margin: 0 auto;
  padding: 0 var(--space-6);
}

/* Section spacing */
.section {
  padding: var(--space-16) 0;
}
```

### 3. Screenshots
Sent live during analysis via Telegram

## Integration with /page_designer

When `/page_designer` is invoked, it should:
1. Check if `{brand}-design-system.css` exists
2. If yes, import those variables and match the styles
3. If no, prompt user to run `/website_brand_analysis` first

```
/page_designer requires:
- {brand}-design-system.css (from /website_brand_analysis)
- Page brief (sections, copy, CTAs)
- frontend-design skill (for quality execution)
```
