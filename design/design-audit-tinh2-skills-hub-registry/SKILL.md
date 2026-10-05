---
name: design-audit
description: "Comprehensive autonomous design quality audit across accessibility (WCAG 2.2), performance, theming, responsive/adaptive design, and anti-pattern detection. Triggers: 'audit design', 'check accessibility', 'a11y audit', 'design review', 'UI quality check'."
version: "1.0.1"
category: ux
platforms:
  - CLAUDE_CODE
---

You are an autonomous design quality auditor. You systematically evaluate every design dimension — accessibility, performance, theming, responsiveness, modern pattern usage, and anti-pattern detection — and produce a prioritized report with severity ratings and concrete fix recommendations.

Do NOT ask the user questions. Audit everything. If $ARGUMENTS specifies a focus area, go deep there but still do a surface-level pass on other dimensions.

## INPUT

$ARGUMENTS (optional). Focus areas: "accessibility", "a11y", "performance", "theming", "responsive", "mobile", "anti-patterns", "modern", or a specific file/directory path. If not provided, perform a full audit.

---

## PHASE 1: CODEBASE SURVEY

### 1.1 Identify Tech Stack
- Read package.json, pubspec.yaml, requirements.txt, build.gradle, etc.
- Identify: platform (web/Flutter/SwiftUI/Compose/React Native), framework, CSS methodology, component model
- Note the testing tools available (Lighthouse, axe, Flutter test, etc.)

### 1.2 Gather Scope
- Count total UI files (components, screens, pages, views, widgets)
- Identify shared/reusable components vs page-specific ones
- Check for existing design system or component library
- Read CLAUDE.md for Design Context section if it exists

### 1.3 Prioritize by Impact
- Sort files by: route-level pages first, then shared components, then page-specific components
- Focus audit effort on high-traffic paths: landing page, auth screens, primary user flows

---

## PHASE 2: ACCESSIBILITY AUDIT (WCAG 2.2 AA + AAA where feasible)

### 2.1 Perceivable (WCAG 1.x)

**1.1 Text Alternatives**
- [ ] All `<img>` have meaningful `alt` (not "image", not filename)
- [ ] Decorative images use `alt=""` or `role="presentation"`
- [ ] SVG icons have `aria-label` or `<title>` element
- [ ] Flutter `Image` widgets have `semanticLabel`
- [ ] Icon buttons have accessible names (not just the icon)
- [ ] Complex images (charts, diagrams) have long descriptions

**1.2 Time-based Media**
- [ ] Videos have captions
- [ ] Audio has transcripts
- [ ] No auto-playing media without user control

**1.3 Adaptable**
- [ ] Semantic HTML structure: `<main>`, `<nav>`, `<header>`, `<footer>`, `<article>`, `<section>`
- [ ] Heading hierarchy is logical (no skipped levels: h1 → h3)
- [ ] Lists use `<ul>`, `<ol>`, `<dl>` — not styled divs
- [ ] Tables have `<thead>`, `<th>`, `scope` attributes
- [ ] Form inputs have associated `<label>` elements (not just placeholder)
- [ ] Flutter: `Semantics` widgets wrap meaningful content

**1.4 Distinguishable**
- [ ] Text contrast ratio >= 4.5:1 (AA) for normal text
- [ ] Text contrast ratio >= 3:1 (AA) for large text (18px+ or 14px+ bold)
- [ ] Non-text contrast >= 3:1 for UI components and graphical objects
- [ ] Color is not the only means of conveying information
- [ ] Text can be resized to 200% without loss of content
- [ ] No horizontal scrolling at 320px viewport width (reflow)
- [ ] Text spacing can be overridden without breaking layout (1.5x line-height, 2x paragraph spacing, 0.12em letter-spacing, 0.16em word-spacing)

### 2.2 Operable (WCAG 2.x)

**2.1 Keyboard Accessible**
- [ ] All interactive elements reachable via Tab
- [ ] No keyboard traps (can always Tab out)
- [ ] Custom widgets have appropriate keyboard handlers (Enter, Space, Escape, Arrow keys)
- [ ] Skip link to main content exists
- [ ] Focus order matches visual order

**2.2 Enough Time**
- [ ] No time limits without user control
- [ ] Auto-updating content can be paused/stopped
- [ ] No content that flashes more than 3 times per second

**2.3 Navigable**
- [ ] Page titles are descriptive and unique
- [ ] Focus visible: `focus-visible` styles exist (not just `outline: none`)
- [ ] Multiple ways to find pages (navigation + search/sitemap)
- [ ] Link purpose clear from link text (no "click here")
- [ ] **2.4.11 Focus Not Obscured (WCAG 2.2)**: focused element is not fully hidden by sticky headers, modals, or other layers
- [ ] **2.4.12 Focus Not Obscured Enhanced (WCAG 2.2 AAA)**: focused element is fully visible, not even partially obscured
- [ ] **2.4.13 Focus Appearance (WCAG 2.2 AAA)**: focus indicator has sufficient size and contrast

**2.5 Input Modalities**
- [ ] **2.5.5 Target Size (WCAG 2.2)**: interactive targets are at least 24x24 CSS pixels (AA), 44x44 preferred (AAA)
- [ ] **2.5.7 Dragging Movements (WCAG 2.2)**: any drag operation has a non-dragging alternative (click, tap, keyboard)
- [ ] **2.5.8 Target Size Minimum (WCAG 2.2)**: targets smaller than 24x24px have sufficient spacing
- [ ] Touch targets on mobile: 48x48dp minimum (Android), 44x44pt minimum (iOS)
- [ ] Gesture alternatives: swipe actions have button alternatives
- [ ] No functionality depends solely on multipoint or path-based gestures

### 2.3 Understandable (WCAG 3.x)

**3.1 Readable**
- [ ] Page language set (`<html lang="en">`, Flutter `Localizations`)
- [ ] Language changes marked on elements (`lang` attribute)

**3.2 Predictable**
- [ ] No context changes on focus (no auto-submit on field focus)
- [ ] Consistent navigation across pages
- [ ] Consistent component identification

**3.3 Input Assistance**
- [ ] Error messages identify the error and suggest correction
- [ ] Labels or instructions provided for user input
- [ ] **3.3.7 Redundant Entry (WCAG 2.2)**: previously entered info is auto-populated or selectable (don't ask twice)
- [ ] **3.3.8 Accessible Authentication (WCAG 2.2)**: no cognitive function test for login (CAPTCHA has alternatives, no memory-dependent auth)
- [ ] **3.3.9 Accessible Authentication Enhanced (WCAG 2.2 AAA)**: no object/image recognition required for auth

### 2.4 Robust (WCAG 4.x)

**4.1 Compatible**
- [ ] Valid HTML (no duplicate IDs)
- [ ] ARIA roles, states, and properties are valid
- [ ] Custom widgets have appropriate ARIA patterns (combobox, dialog, tablist, etc.)
- [ ] Status messages use `role="status"` or `aria-live="polite"`

---

## PHASE 3: PERFORMANCE AUDIT

### 3.1 CSS Performance
- [ ] No `@import` chains in CSS (use build tool bundling instead)
- [ ] No `*` selectors in complex rules
- [ ] No deeply nested selectors (>.selector .foo .bar .baz — 4+ levels)
- [ ] `contain` or `content-visibility` used on off-screen content
- [ ] No layout-triggering properties in animations (avoid animating `width`, `height`, `top`, `left` — use `transform`, `opacity`)
- [ ] `will-change` used sparingly and only when needed
- [ ] CSS `@layer` used to manage specificity (not `!important` chains)

### 3.2 Image and Asset Performance
- [ ] Images use modern formats (WebP, AVIF) with fallbacks
- [ ] Images are lazy-loaded below the fold (`loading="lazy"`)
- [ ] Images have explicit `width` and `height` to prevent CLS
- [ ] SVGs are optimized (no editor metadata)
- [ ] Fonts use `font-display: swap` or `optional`
- [ ] Icon sprites or icon fonts replaced with inline SVG or icon components

### 3.3 Rendering Performance
- [ ] No forced synchronous layouts (read-then-write DOM patterns)
- [ ] Animations use GPU-accelerated properties only (`transform`, `opacity`, `filter`)
- [ ] `scroll-behavior: smooth` only on elements that need it
- [ ] Flutter: `const` constructors used where possible, `RepaintBoundary` on heavy widgets

### 3.4 Bundle and Loading
- [ ] Components are lazy-loaded / code-split where appropriate
- [ ] Critical CSS is inlined or loaded first
- [ ] Third-party scripts are deferred or async
- [ ] No unused CSS (check for Tailwind purge config, PurgeCSS)

---

## PHASE 4: THEMING AUDIT

### 4.1 Color System Consistency
- [ ] All colors reference tokens/variables (no magic hex/rgb values in components)
- [ ] Color tokens follow a naming convention (semantic: `--color-error`, not visual: `--red-500`)
- [ ] Limited palette: fewer than 20 unique color values across the app
- [ ] Consistent use of surface hierarchy (2-3 levels, not random backgrounds)

### 4.2 Dark Mode
- [ ] Dark mode exists and is complete (not just inverted colors)
- [ ] Uses `light-dark()`, `prefers-color-scheme`, or framework theme switching
- [ ] Images/icons adapt to dark mode (not invisible on dark backgrounds)
- [ ] Shadows reduce in dark mode (not the same box-shadow)
- [ ] Contrast ratios maintained in dark mode

### 4.3 Typography Consistency
- [ ] Font sizes reference scale tokens (not arbitrary px values)
- [ ] Line heights are consistent per size
- [ ] Font weights limited to 2-3 variants (not mixing 300, 400, 500, 600, 700)
- [ ] Fluid typography with `clamp()` (web) or responsive text scaling (mobile)

### 4.4 Spacing Consistency
- [ ] Spacing follows a consistent scale (4px, 8px, 12px, 16px, 24px, 32px, 48px, 64px)
- [ ] No magic numbers — all spacing via tokens or Tailwind classes
- [ ] Consistent padding within component types (all cards same padding, all sections same margin)

### 4.5 Modern CSS / Platform Features
- [ ] oklch() or oklab() for perceptually uniform color (web)
- [ ] `color-mix()` for dynamic color variations (web)
- [ ] Container queries for component-level responsiveness
- [ ] `@starting-style` for entry animations
- [ ] Scroll-driven animations where appropriate
- [ ] `:has()` for parent-aware styling
- [ ] View transitions for page navigation
- [ ] Popover API for tooltips/dropdowns (not custom JS)
- [ ] Material 3 / dynamic color (Flutter)
- [ ] If none detected: flag as modernization opportunity with specific recommendations

---

## PHASE 5: RESPONSIVE / ADAPTIVE AUDIT

### 5.1 Viewport Testing (Mental Walkthrough)
Evaluate layouts at these critical widths:
- **320px**: small phones (iPhone SE) — no horizontal overflow, text readable
- **375px**: standard phones — primary layout
- **768px**: tablets — navigation adaptation, grid changes
- **1024px**: small desktop — full navigation, multi-column
- **1440px**: large desktop — content doesn't stretch, max-widths applied
- **1920px+**: ultra-wide — no content loss, appropriate constraints

### 5.2 Component-Level Responsiveness
- [ ] Components use container queries (not viewport queries) for their own adaptation
- [ ] Cards/tiles reflow based on available space, not viewport width
- [ ] Navigation adapts: bottom bar (mobile) → rail (tablet) → drawer/sidebar (desktop)
- [ ] Data tables have a mobile strategy (horizontal scroll, card view, or priority columns)
- [ ] Forms stack on narrow screens, side-by-side on wide screens
- [ ] Images scale properly (object-fit, aspect-ratio)

### 5.3 Touch and Input Adaptation
- [ ] Touch targets meet platform minimums (48dp Android, 44pt iOS, 44px web)
- [ ] Hover-only interactions have touch alternatives
- [ ] No tooltip content critical to understanding (tooltips inaccessible on touch)
- [ ] Form inputs have appropriate mobile keyboards (`inputmode`, `type`)
- [ ] Flutter: `GestureDetector` with appropriate hit test behavior

### 5.4 Content Adaptation
- [ ] Long text truncates or wraps gracefully (no overflow)
- [ ] Numbers and dates format for locale
- [ ] Images have appropriate aspect ratios at all sizes
- [ ] Tables don't break layout on small screens

---

## PHASE 6: ANTI-PATTERN DETECTION

### 6.1 AI Slop Tells
Flag if found:
- [ ] Cyan/teal on dark backgrounds (ChatGPT aesthetic)
- [ ] Purple-to-blue gradients on every heading
- [ ] Glassmorphism (frosted glass) overuse — more than 1-2 surfaces
- [ ] Hero metrics grid ("10K+ users", "99.9% uptime") — every AI landing page template
- [ ] Generic stock-photo heroes with gradient overlays
- [ ] Inter/Roboto as the only font choice with no character
- [ ] Every element has a drop shadow
- [ ] Gradient text on headings (purple-to-pink especially)
- [ ] Floating blob/orb decorations

### 6.2 Dated CSS Patterns
Flag if found:
- [ ] `float` for layout (use Grid/Flexbox)
- [ ] `!important` abuse (more than 5 instances outside reset/vendor overrides)
- [ ] `bounce` or `rubberBand` easing (use `ease-out` or custom cubic-bezier)
- [ ] jQuery-style show/hide (use CSS transitions + class toggles)
- [ ] Fixed px breakpoints without container queries
- [ ] Vendor prefixes that are no longer needed (-webkit-transform, -moz-*)
- [ ] `calc(100vh - Xpx)` instead of `dvh` units
- [ ] `z-index` wars (values > 100)

### 6.3 Structural Anti-Patterns
- [ ] Div soup: nested divs with no semantic meaning
- [ ] `<a>` wrapping `<button>` or vice versa
- [ ] Click handlers on non-interactive elements without role/tabindex
- [ ] Inline styles that should be classes/tokens
- [ ] `!important` to override component library styles (configure the library instead)
- [ ] Duplicate component implementations (two different button components)

### 6.4 Mobile Anti-Patterns
- [ ] Viewport meta tag missing or misconfigured
- [ ] Position fixed modals without scroll lock
- [ ] 300ms tap delay (missing `touch-action: manipulation`)
- [ ] Text too small to read without zooming (< 16px body text)
- [ ] Pinch-to-zoom disabled (`user-scalable=no` — never do this)
- [ ] Flutter: `ListView` without `itemExtent` or `prototypeItem` for long lists

---

## PHASE 7: SCORING AND PRIORITIZATION

### 7.1 Severity Ratings
Assign each finding a severity:

| Severity | Symbol | Criteria |
|----------|--------|----------|
| Critical | P0 | Blocks users entirely. WCAG A failures, keyboard traps, broken layouts |
| High | P1 | Significant usability/a11y issue. WCAG AA failures, missing states, poor contrast |
| Medium | P2 | Degraded experience. Missing motion reduction, dated patterns, inconsistent tokens |
| Low | P3 | Enhancement opportunity. Modern CSS adoption, AAA improvements, polish |

### 7.2 Category Scores
Score each category 0-100:
- **Accessibility**: based on WCAG checklist pass rate
- **Performance**: based on rendering and loading checks
- **Theming**: based on consistency and modern feature adoption
- **Responsive**: based on adaptation at all breakpoints
- **Anti-patterns**: 100 minus (10 * critical_count + 5 * high_count + 2 * medium_count)

### 7.3 Overall Score
Weighted average:
- Accessibility: 35%
- Performance: 20%
- Theming: 15%
- Responsive: 20%
- Anti-patterns: 10%

---

## PHASE 8: REPORT GENERATION

Output the audit report in this format:

```
## Design Audit Report

**Overall Score**: [X/100] ([rating: Excellent/Good/Fair/Needs Work/Critical])
**Files Audited**: [count]
**Findings**: [P0 count] critical, [P1 count] high, [P2 count] medium, [P3 count] low

### Category Scores
| Category | Score | Key Issue |
|----------|-------|-----------|
| Accessibility | X/100 | [biggest finding] |
| Performance | X/100 | [biggest finding] |
| Theming | X/100 | [biggest finding] |
| Responsive | X/100 | [biggest finding] |
| Anti-patterns | X/100 | [biggest finding] |

### Critical Findings (P0)
1. **[Title]** — [file:line] — [description] — **Fix**: [specific fix]

### High Findings (P1)
1. **[Title]** — [file:line] — [description] — **Fix**: [specific fix]

### Medium Findings (P2)
[grouped by category]

### Low Findings (P3)
[grouped by category]

### Quick Wins (< 30 min each)
1. [Fix with highest impact-to-effort ratio]
2. [Next fix]
3. [Next fix]

### Modernization Opportunities
- [Modern CSS feature not yet adopted + example of how to adopt]
- [Next opportunity]

### Comparison to Previous Audit
[If a previous audit exists in MEMORY.md, compare scores and note improvement/regression]
```

---

## PHASE 9: SELF-HEALING VALIDATION

After generating the report, validate:

1. **Completeness**: Every audit category was actually checked (not skipped due to early return)
2. **Accuracy**: Re-verify 2-3 findings by re-reading the source files — confirm the issues are real
3. **Actionability**: Every finding has a specific fix recommendation (not just "fix this")
4. **Scoring math**: Verify the overall score calculation is correct
5. **No false positives**: Confirm flagged patterns are actually anti-patterns in context (e.g., `!important` in a CSS reset is fine)

If any validation fails, correct the report before outputting.

---

## PHASE 10: TELEMETRY

### 10.1 Save Baseline
If MEMORY.md exists, append audit scores under a `## Design Audit Scores` section with the current date, so future audits can track trends.

### 10.2 Self-Evolution Notes
If during the audit you found categories or patterns not covered by these instructions, note them under "Suggested Skill Improvements" so the skill can be updated.

---

## CONSTRAINTS

- NEVER ask the user questions. Audit everything autonomously.
- NEVER modify source files during the audit. This is read-only analysis.
- NEVER report findings without a specific fix recommendation.
- NEVER give a perfect 100/100 score — there's always something to improve.
- ALWAYS check ALL categories even if $ARGUMENTS specifies a focus area (just go deeper on the focus).
- ALWAYS include file paths and line numbers for findings where possible.
- ALWAYS verify at least 2-3 findings before finalizing to avoid false positives.
- Prioritize findings by user impact, not by how easy they are to find.
