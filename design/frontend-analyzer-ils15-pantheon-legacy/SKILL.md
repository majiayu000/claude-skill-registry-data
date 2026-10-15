---
name: frontend-analyzer
description: Analyze React components for design tokens and accessibility. Use for extracting typography, colors, and layout patterns.
globs: ["**/*.tsx", "**/*.jsx", "**/components/**"]
alwaysApply: false
---

# Frontend Analyzer

Analisa e identifica tipografia, cores, layout, fontes e elementos de design system em componentes frontend.

## Overview

The Frontend Analyzer skill provides deep inspection of frontend code, design elements, and visual properties. It extracts typography, color palettes, spacing systems, component hierarchies, and accessibility attributes from React/Next.js applications.

## Core Capabilities

### 1. **Visual Element Analysis**

#### 🔤 Typography Detection
- Font families (system fonts, Google Fonts, custom fonts)
- Font sizes and scaling systems (rem, px, %)
- Font weights (100-900)
- Line heights and letter spacing
- Text decorations and text transforms
- Font loading strategies (WOFF2, variable fonts)

#### 🎨 Color Palette Extraction
- Primary, secondary, accent colors
- Background and text colors
- Semantic colors (success, error, warning, info)
- Opacity/alpha values
- Color space (RGB, HSL, hex, CSS variables)
- Dark mode variants

#### 📐 Layout & Spacing
- Grid systems (CSS Grid, Flexbox)
- Spacing scale (gaps, margins, padding)
- Breakpoints and responsive behavior
- Container queries and fluid sizing
- Z-index hierarchy
- Positioning strategies

#### 🧩 Component Architecture
- Component hierarchy and nesting
- Reusable component patterns
- Props and TypeScript interfaces
- State management patterns
- Custom hooks usage
- Styled components vs CSS modules

### 2. **Analysis Categories**

1. **Visual Inspection** - Screenshots and visual differences
2. **Code Inspection** - Component code structure
3. **Design System** - Design token usage
4. **Accessibility (A11y)** - WCAG AA/AAA compliance
5. **Performance** - Font loading optimization

## Analysis Output Structure

```markdown
## 🎨 VISUAL ELEMENTS DETECTED

### Typography System
- Primary Font: [Font family, source, fallback]
- Heading Scale: H1-H6 sizes and weights
- Body Text: Default size, line-height, letter-spacing
- Monospace: Code/terminal fonts

### Color Palette
- Primary: #XXXXXX (RGB, HSL, CSS var)
- Semantic: Success, error, warning colors
- Dark Mode: Color scheme variants
- Contrast Ratios: WCAG AA/AAA compliance

### Layout System
- Grid: [Columns, gap, max-width]
- Breakpoints: [Mobile, tablet, desktop specs]
- Spacing Scale: [Base unit, multipliers]
```

## Usage Examples

### Example 1: Extract Design Tokens
Input: "Analise tipografia de ofertachina.com"
Output: All fonts used, sizes, weights, loading strategy

### Example 2: Color Palette Analysis
Input: "Extraia paleta de cores do ProductCard"
Output: Exact colors, WCAG compliance, dark mode variants

### Example 3: Component Deep Dive
Input: "Analise estrutura de ProductCard"
Output: JSX structure, props, styling approach, accessibility

### Example 4: Design System Audit
Input: "Audite design system compliance"
Output: % compliance, violations, refactoring recommendations

## Accessibility (WCAG)

- Contrast ratios: Pass/Fail by element
- Font sizes: Minimum sizes met
- Interactive elements: Size compliance
- Semantic HTML: Structure quality

## Performance Metrics

- Font file sizes and optimization
- Image optimization status
- CSS bundle size
- Component render efficiency

## Integrations

### With the integrated browser
- Automated visual analysis
- Color & typography extraction
- Accessibility testing

### With Prompt Improver
- Design tokens inform prompt creation
- UI patterns documented in instructions

## Tools & Technologies Reference

- **CSS Analysis:** PostCSS, cssstats
- **Typography:** Google Fonts API, Font loading APIs
- **Color:** Chroma.js, ntc.js (color naming)
- **Accessibility:** axe-core, WAVE
- **React Inspection:** React DevTools, Storybook
- **Design Systems:** Figma API, Design tokens parser

## References

- [Google Fonts](https://fonts.google.com/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [WCAG Color Contrast Checker](https://webaim.org/resources/contrastchecker/)
- [CSS-Tricks](https://css-tricks.com/)
- [MDN Web Docs](https://developer.mozilla.org/)
- [Figma Design System](https://www.figma.com/design-systems/)

## Changelog

- **v1.0** (2025-12-19): Initial release with typography, color, layout, component, and accessibility analysis

---

## Appendix: Web UI Analysis

Detailed UX and accessibility analysis for web interfaces.

### When to Use

Use this section when:
- Evaluating a web interface for UX issues
- Checking accessibility compliance (WCAG 2.1 AA/AAA)
- Analyzing color contrast ratios
- Reviewing typography and font hierarchy
- Checking responsive design breakpoints
- Measuring Core Web Vitals (LCP, FID, CLS)
- Comparing against Material Design or Apple HIG standards

### Analysis Framework

#### 1. Accessibility (WCAG 2.1)

```
✅ Checklist:
- [ ] Color contrast ratio ≥ 4.5:1 (text), ≥ 3:1 (large text)
- [ ] Touch targets ≥ 44x44px
- [ ] Keyboard navigation works
- [ ] Screen reader labels present
- [ ] Focus states visible
- [ ] Alt text on images
- [ ] ARIA roles correct
```

#### 2. Typography Hierarchy

```
Heading Scale (1.250 ratio):
- h1: 2.441rem (39px)
- h2: 1.953rem (31px)
- h3: 1.563rem (25px)
- h4: 1.25rem (20px)
- body: 1rem (16px)
- small: 0.8rem (13px)
```

#### 3. Color Palette Analysis

```
Primary Colors:
- Main: #hex (contrast ratio)
- Light variant: #hex
- Dark variant: #hex

Semantic Colors:
- Success: #22c55e (green-500)
- Warning: #f59e0b (amber-500)
- Error: #ef4444 (red-500)
- Info: #3b82f6 (blue-500)
```

#### 4. Layout & Spacing

```
8px Grid System:
- xs: 4px (0.25rem)
- sm: 8px (0.5rem)
- md: 16px (1rem)
- lg: 24px (1.5rem)
- xl: 32px (2rem)
- 2xl: 48px (3rem)

Breakpoints:
- mobile: 0-639px
- tablet: 640-1023px
- desktop: 1024-1279px
- wide: 1280px+
```

#### 5. Core Web Vitals

```
Targets:
- LCP (Largest Contentful Paint): < 2.5s
- FID (First Input Delay): < 100ms
- CLS (Cumulative Layout Shift): < 0.1
- FCP (First Contentful Paint): < 1.8s
- TTFB (Time to First Byte): < 0.8s
```

### Output Format

```markdown
## UI Analysis Report

### Summary
- Overall Score: X/100
- Accessibility: ✅/⚠️/❌
- Performance: ✅/⚠️/❌
- Responsive: ✅/⚠️/❌

### Critical Issues
1. [Issue] - [Impact] - [Fix]

### Recommendations
1. [Improvement] - [Code example]

### Resources
- [Link to relevant docs]
```

### Example Usage

```
@frontend Analyze the login page for accessibility issues
@frontend Check color contrast on the dashboard
@frontend Review typography hierarchy on landing page
@frontend Measure Core Web Vitals for homepage
```
