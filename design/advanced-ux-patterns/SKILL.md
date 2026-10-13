---
name: advanced-ux-patterns
description: Comprehensive UX best practices including accessibility (WCAG 2.2), interaction patterns, user research methods, and usability principles. Use when designing user interfaces, conducting UX audits, or implementing accessible, user-centered designs. Also triggers on WCAG, ARIA, keyboard navigation, screen reader, focus trap, focus management, touch targets, usability testing, heuristic evaluation, card sorting, tree testing, NPS, SUS, form design, navigation patterns, mobile UX, design handoff, cognitive load, information architecture, dark patterns, skeleton screen, error states, reduced motion, dark mode accessibility, component states, error recovery, or any request to audit, improve, spec, or review a user interface — even casually. If UI is involved, use this skill.
metadata:
  version: "1.0.0"
---

# Advanced UX Patterns

Build accessible, user-centered interfaces using proven UX patterns and research-backed principles.

## Quick Start Decision Tree

**Choose your workflow based on task:**

1. **Building new UI?** → Start with accessibility baseline (Step 1)
2. **Auditing existing UI?** → Use UX Audit Checklist (Step 4)
3. **Need interaction patterns?** → See references/interaction-patterns.md
4. **Need user research?** → See references/research-methods.md
5. **Need form design?** → See references/form-patterns.md

## Core Workflow

### Step 1: Accessibility Baseline (WCAG 2.2 Level AA)

**MANDATORY for all interfaces:**

- **Perceivable:**
  - Text alternatives for non-text content (alt text, aria-labels)
  - Captions/transcripts for audio/video
  - Color contrast ≥4.5:1 for normal text, ≥3:1 for large text and UI components
  - No information conveyed by color alone
  - **Dark mode:** Maintain contrast ratios in both themes — don't assume light-mode values carry over

- **Operable:**
  - All functionality available via keyboard
  - Focus indicators visible and not entirely hidden behind sticky headers (**2.4.11 Focus Not Obscured**, new AA in WCAG 2.2; ≥3:1 contrast)
  - No keyboard traps — modals must return focus to trigger on close
  - Skip links for navigation
  - Touch targets: minimum **24×24px** (**2.5.8 Target Size Minimum**, new AA in WCAG 2.2); design target 44×44px for comfort
  - Pointer alternatives for all drag interactions (**2.5.7 Dragging Movements**, new AA in WCAG 2.2)
  - Respect `prefers-reduced-motion`: gate animations in `@media (prefers-reduced-motion: no-preference)` — don't suppress motion globally

- **Understandable:**
  - Language declared in HTML (`lang="en"`)
  - Consistent navigation across pages
  - Clear error messages with specific recovery suggestions (not just "invalid input")
  - Labels for all form inputs — no placeholder-only labels

- **Robust:**
  - Valid HTML/ARIA — don't add ARIA roles that duplicate native semantics
  - Test with real assistive tech (NVDA + Chrome, VoiceOver + Safari), not just axe
  - Degrade gracefully — core content readable without CSS/JS

Validate with: Chrome DevTools → Accessibility panel, or axe DevTools extension, or run `npx axe <url>` in terminal.

See: references/wcag-checklist.md for complete requirements

### Step 2: Interaction Pattern Selection

Choose patterns based on user task:

**Navigation Patterns:**
- Global nav (primary tasks, always visible)
- Breadcrumbs (hierarchy, wayfinding)
- Pagination (large datasets, sequential browsing)
- Infinite scroll (content discovery, mobile-first)

**Input Patterns:**
- Autocomplete (speed, reduce errors)
- Inline validation (immediate feedback)
- Multi-step forms (complex flows, reduce cognitive load)
- Search filters (faceted search, refine results)

**Feedback Patterns:**
- Toast notifications (non-blocking, temporary)
- Modal dialogs (critical decisions, blocking)
- Inline errors (contextual, actionable)
- Loading states (skeleton screens, progress indicators)

**Data Display:**
- Data tables (comparison, sorting, filtering)
- Cards (scannable, visual hierarchy)
- Lists (linear, prioritized content)
- Dashboards (at-a-glance, KPIs)

See: references/interaction-patterns.md for complete pattern library

### Step 3: User Research Integration

**When to conduct research:**
- Before design (discovery, personas, journey maps)
- During design (usability testing, concept validation)
- After launch (analytics, feedback loops)

**Quick research methods:**
- **5-second tests:** First impressions (clarity, hierarchy)
- **Card sorting:** Information architecture
- **Heuristic evaluation:** Nielsen's 10 usability heuristics
- **Analytics review:** Identify pain points (drop-off, errors)

**Research outputs:**
- User personas (goals, behaviors, pain points)
- Journey maps (touchpoints, emotions, opportunities)
- Wireframes (low-fidelity, quick iteration)
- Prototypes (high-fidelity, validate interactions)

See: references/research-methods.md for detailed guidance

### Step 4: UX Audit Checklist

Use when evaluating existing interfaces:

**Usability (Nielsen Heuristics):**
- [ ] Visibility of system status (loading, progress, errors)
- [ ] Match between system and real world (familiar language, metaphors)
- [ ] User control and freedom (undo, redo, cancel)
- [ ] Consistency and standards (patterns, terminology)
- [ ] Error prevention (constraints, confirmations)
- [ ] Recognition over recall (visible options, defaults)
- [ ] Flexibility and efficiency (shortcuts, power users)
- [ ] Aesthetic and minimalist design (remove clutter)
- [ ] Help users recognize, diagnose, recover from errors
- [ ] Help and documentation (contextual, searchable)

**Accessibility:**
- [ ] Keyboard navigation (tab order, focus management)
- [ ] Screen reader compatibility (ARIA, semantic HTML)
- [ ] Color contrast (text, UI elements)
- [ ] Zoom support (up to 200% without horizontal scroll)
- [ ] Captions/transcripts (multimedia)

**Performance:**
- [ ] First Contentful Paint <1.8s
- [ ] Largest Contentful Paint <2.5s
- [ ] Cumulative Layout Shift <0.1
- [ ] Interaction to Next Paint (INP) <200ms (replaces FID, deprecated March 2024)

**Mobile:**
- [ ] Touch targets ≥24×24px minimum (WCAG 2.2 AA); ≥44×44px comfort target
- [ ] Responsive breakpoints (320px, 768px, 1024px)
- [ ] Portrait/landscape support
- [ ] Native patterns (bottom nav, swipe gestures)

Manual audit tools: Lighthouse (DevTools → Audits), WAVE browser extension, keyboard-only navigation test.

### Step 5: Design Handoff

**Developer-ready deliverables:**

1. **Component specs:**
   - States (default, hover, focus, disabled, error)
   - Spacing (padding, margins in 8px grid)
   - Typography (font, size, weight, line-height)
   - Colors (hex/RGB with semantic tokens)

2. **Interaction specs:**
   - Animations (duration, easing, trigger)
   - Transitions (micro-interactions, state changes)
   - Validation rules (real-time, on blur, on submit)

3. **Responsive behavior:**
   - Breakpoints (mobile-first approach)
   - Layout changes (stack, hide, resize)
   - Image srcsets (responsive images)

4. **Accessibility annotations:**
   - ARIA labels/roles
   - Keyboard shortcuts
   - Focus order
   - Screen reader instructions

5. **Visual regression baseline:**
   - Establish before first deploy: `npx vizzly tdd "npx playwright test"` (local, free tier)
   - Approved screenshots become the baseline — future diffs require explicit approval
   - Rejected diffs fed back to agent/developer as correction context

See: references/design-handoff.md for templates

## Common Patterns Library

### Form Design Best Practices

```
✅ DO:
- Single column layouts (easier scanning)
- Inline validation (immediate feedback)
- Clear labels above inputs (always visible)
- Optional fields marked (assume required)
- Smart defaults (reduce user effort)
- Progress indicators (multi-step forms)

❌ AVOID:
- Placeholder-only labels (accessibility issue)
- CAPTCHA on low-risk flows (use invisible reCAPTCHA v3 or honeypot — visible CAPTCHAs add friction and fail screen readers)
- Disabled submit buttons (show errors instead)
- Ambiguous error messages ("invalid input")
- Reset buttons (accidental data loss)
```

See: references/form-patterns.md

### Navigation Best Practices

```
✅ DO:
- Logo links to home (universal convention)
- Primary nav ≤7 items (NN/g research; Miller's "7±2" applies to working memory chunks, not nav items — but the practical limit holds)
- Active state indicators (current page)
- Breadcrumbs for deep hierarchies (3+ levels)
- Search in header (expected location)

❌ AVOID:
- Hamburger menus on desktop (hide content)
- Auto-playing carousels (accessibility, usability)
- Dropdown menus on hover (mobile, accessibility)
- Pagination for <50 items (use scrolling)
```

See: references/navigation-patterns.md

### Mobile-First Patterns

```
✅ DO:
- Bottom navigation (thumb-friendly)
- Large touch targets (≥44×44px)
- Swipe gestures (back, delete, archive)
- Pull-to-refresh (native feel)
- Sticky CTAs (always visible)

❌ AVOID:
- Horizontal scrolling (poor discoverability)
- Tiny tap targets (<44px)
- Hover-dependent interactions
- Long forms without chunking
```

See: references/mobile-patterns.md

## Anti-Patterns to Avoid

**Dark Patterns (unethical UX):**
- ❌ Trick questions (pre-checked opt-ins)
- ❌ Roach motel (easy to get in, hard to leave)
- ❌ Confirmshaming ("No, I don't want to save money")
- ❌ Forced continuity (auto-renew without warning)
- ❌ Hidden costs (fees revealed at checkout)

**Performance Anti-Patterns:**
- ❌ Blocking JavaScript (delays rendering)
- ❌ Unoptimized images (large file sizes)
- ❌ Excessive third-party scripts (tracking bloat)
- ❌ No lazy loading (load everything upfront)

**Accessibility Anti-Patterns:**
- ❌ Icon-only buttons (no text labels)
- ❌ Low contrast text (hard to read)
- ❌ Auto-playing media (disorienting)
- ❌ Keyboard traps (can't escape)

## Quality Gates

Before finalizing designs:

- [ ] Accessibility audit passed (WCAG 2.2 AA)
- [ ] Mobile-responsive (tested 320px-1920px)
- [ ] Keyboard navigation works (no mouse required)
- [ ] Focus indicators visible (3px, ≥3:1 contrast)
- [ ] Error states defined (with recovery paths)
- [ ] Loading states defined (skeleton screens)
- [ ] Touch targets ≥24×24px (WCAG 2.2 AA minimum); ≥44px comfort target
- [ ] Color contrast ≥4.5:1 (text)
- [ ] Forms have inline validation
- [ ] Performance budget met (LCP <2.5s)

## Stack-Specific Shortcuts (React + Tailwind + shadcn/ui)

These patterns apply directly to Kyle's production stack.

**shadcn/ui a11y defaults:**
- `Dialog` / `AlertDialog` — built-in focus trap, returns focus on close. Don't roll your own.
- `Command` — keyboard-navigable by default; add `aria-label` to `CommandInput`.
- `Select` — uses Radix UI; keyboard + screen reader compatible. Never replace with a `<div>` dropdown.
- `Tooltip` — keyboard-accessible by default; don't add tooltips to non-interactive elements.
- `Table` — add `aria-sort` attributes manually when implementing sortable columns.

**Tailwind utilities:**
- Contrast: `text-gray-900 dark:text-gray-100` — always pair light/dark values; verify with Tailwind's `contrast()` plugin or a browser DevTools check
- Focus ring: `focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2` — use `focus-visible:` not `focus:` to avoid showing rings on mouse click
- Reduced motion: `motion-safe:transition-all motion-reduce:transition-none`
- Screen reader only: `sr-only` for visually hidden labels

**React patterns:**
- Focus management after async operations: `useEffect(() => { ref.current?.focus() }, [isLoaded])`
- Skip link: render as first child of `<body>`, `href="#main-content"`, visible on focus only
- Error boundary + fallback: always define accessible error UI, not just `null`

**Cross-skill callouts:**
- Design tokens, brand colors, Loxihart/FlashFusion profiles → `managing-design-briefs`
- Experience thesis, design system decisions, anti-slop audit → `elite-ui-design`
- Code generation from a confirmed design brief → `frontend-design`
- Prototyping fidelity, usability test plans, A/B experiment design → `prototyping-testing`

## References

- WCAG 2.2 Guidelines: https://www.w3.org/WAI/WCAG22/quickref/
- WCAG 3.0 Working Draft (monitor, not implement yet): https://www.w3.org/TR/wcag-3.0/ — key change: APCA contrast replaces current 4.5:1 ratios; Bronze/Silver/Gold replaces A/AA/AAA
- APCA Contrast Calculator: https://www.myndex.com/APCA/
- Nielsen Norman Group: https://www.nngroup.com/articles/
- Material Design: https://m3.material.io/
- Apple Human Interface Guidelines: https://developer.apple.com/design/human-interface-guidelines
- A11y Project: https://www.a11yproject.com/

## Bundled References

- **references/wcag-checklist.md** - Complete WCAG 2.2 Level AA requirements
- **references/interaction-patterns.md** - Comprehensive pattern library (navigation, input, feedback, data display)
- **references/research-methods.md** - User research playbook (usability testing, 5-second tests, card sorting, tree testing, NPS)
- **references/form-patterns.md** - Form design best practices with ARIA patterns
- **references/navigation-patterns.md** - Navigation pattern library (global, wayfinding, contextual, search)
- **references/mobile-patterns.md** - Mobile-specific UX patterns (touch targets, gestures, safe areas)
- **references/design-handoff.md** - Developer handoff templates (component spec, interaction spec, accessibility annotations)
