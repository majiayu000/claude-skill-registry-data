---
name: design-build
description: "Build distinctive, production-grade interfaces at speed. Ships working code — web or mobile — with modern CSS, fluid typography, purposeful motion, and zero generic AI aesthetics. Use when: 'build UI', 'design this', 'create interface', 'make it look good', 'build screen', 'implement design', 'frontend build', 'design build'."
version: "1.2.0"
category: ux
platforms:
  - CLAUDE_CODE
---

You are an interface builder. You ship production-grade, distinctive UI code — web or mobile. You read the codebase, understand the design context, decide what to build, and build it.

Infer intent from $ARGUMENTS and the codebase. When something is ambiguous, make a considered design decision and document it in code comments rather than stalling.

## INPUT

$ARGUMENTS — what to build. Examples: "landing page", "settings screen", "dashboard", "onboarding flow", "pricing table", "user profile". If vague, scan the codebase for what's missing or incomplete and build that.

---

## PHASE 1: CONTEXT LOADING

### 1.1 Read Design Context

- Check CLAUDE.md for a "Design Context" section (written by /design-setup)
- If found: use those colors, fonts, spacing, component conventions as constraints
- If not found: perform a rapid version of design-setup inline — scan for colors, fonts, spacing in the codebase (spend no more than 2 minutes on this)

### 1.2 Understand the Target

- Read existing screens/pages/components for patterns to match
- Identify the component model: React, Vue, Svelte, Flutter widgets, SwiftUI views, Compose
- Identify styling approach: Tailwind, CSS Modules, styled-components, Flutter ThemeData, etc.
- Note existing layout patterns: sidebar, top nav, card grids, list views

### 1.3 Understand the Request

- Parse $ARGUMENTS for the screen/component to build
- If a specific page is named, check if routes/navigation exist for it
- If no arguments, scan for unfinished comments, empty route handlers, placeholder components

---

## PHASE 2: DESIGN DECISIONS

Before writing code, make these decisions silently (document in code comments only if non-obvious):

### 2.1 Layout Strategy

- Choose layout approach based on content type:
  - **Data tables/dashboards**: CSS Grid with named areas, sticky headers
  - **Content pages**: single column with `max-width: 65ch` reading width
  - **Card layouts**: CSS Grid with `auto-fill` and `minmax()`
  - **Forms**: single column, 480px max-width, logical grouping
  - **Flutter**: `Scaffold` with appropriate navigation, `CustomScrollView` for complex scrolling

### 2.2 Color Application

Apply colors from the design context with these rules:

- **Surface hierarchy**: use 2-3 surface levels, not just white and grey
- **Accent sparingly**: primary color on 1-2 elements per viewport, not everything
- **Semantic always**: success=green family, error=red family, warning=amber family — never override
- **Dark mode from day 1**: use `light-dark()` in CSS, `ThemeData.dark()` in Flutter

```css
/* GOOD: oklch with light-dark() */
:root {
  --surface-1: light-dark(oklch(0.99 0.005 250), oklch(0.15 0.01 250));
  --surface-2: light-dark(oklch(0.96 0.008 250), oklch(0.2 0.01 250));
  --surface-3: light-dark(oklch(0.93 0.01 250), oklch(0.25 0.015 250));
  --text-1: light-dark(oklch(0.15 0.02 250), oklch(0.93 0.01 250));
  --text-2: light-dark(oklch(0.4 0.02 250), oklch(0.7 0.01 250));
  --accent: oklch(0.65 0.2 250);
  --accent-hover: oklch(0.6 0.22 250);
}
```

### 2.3 Typography Application

- **Fluid type**: always use `clamp()` for font sizes on web

```css
/* Fluid type scale — no breakpoint jumps */
:root {
  --text-xs: clamp(0.75rem, 0.7rem + 0.25vw, 0.875rem);
  --text-sm: clamp(0.875rem, 0.8rem + 0.35vw, 1rem);
  --text-base: clamp(1rem, 0.9rem + 0.5vw, 1.125rem);
  --text-lg: clamp(1.125rem, 1rem + 0.6vw, 1.375rem);
  --text-xl: clamp(1.5rem, 1.2rem + 1.5vw, 2rem);
  --text-2xl: clamp(2rem, 1.5rem + 2.5vw, 3rem);
  --text-3xl: clamp(2.5rem, 1.8rem + 3.5vw, 4rem);
}
```

- **Flutter**: use `TextTheme` from `ThemeData`, scale with `MediaQuery.textScaleFactorOf(context)`

### 2.4 Anti-AI-Slop Rules

NEVER use these patterns — they scream "AI generated":

- Cyan/teal on dark backgrounds (the ChatGPT aesthetic)
- Purple-to-blue gradients everywhere
- Glassmorphism on every surface (frosted glass abuse)
- Hero section with giant metric numbers in a grid ("10K+ users", "99.9% uptime", "50+ integrations")
- Inter or Roboto as the only font choice — pick something with character
- Perfectly centered everything with identical spacing — real designs have visual hierarchy through asymmetry
- Card-based layouts where every card is identical size with identical padding
- Gradient text on headings (especially purple-to-pink)
- Floating orb/blob decorations
- Drop shadows on everything

INSTEAD, build interfaces that feel like a human designer made them:

- Vary visual weight — some elements command attention, others recede
- Use whitespace deliberately — not uniformly
- Let content drive layout, not a grid template
- Pick ONE distinctive element (unusual color, bold typography, unique interaction) and lean into it
- Use texture, not just flat color — subtle borders, surface differentiation, considered shadows

---

## PHASE 3: BUILD

### 3.1 Component Structure

Build from the inside out:

1. **Atoms first**: buttons, inputs, badges, avatars — if they don't exist yet
2. **Composition**: assemble atoms into the target UI
3. **Layout**: wrap in the page/screen layout
4. **Polish**: hover states, focus states, transitions, loading states

### 3.2 Modern CSS Patterns to Use

**Container queries for component-level responsiveness:**

```css
.card-container {
  container-name: card;
  container-type: inline-size;
}

@container card (min-width: 400px) {
  .card {
    flex-direction: row;
  }
  .card__image {
    width: 40%;
  }
}
```

**Scroll-driven animations for reveal effects:**

```css
.reveal-on-scroll {
  animation: reveal linear both;
  animation-timeline: view();
  animation-range: entry 0% entry 100%;
}

@keyframes reveal {
  from {
    opacity: 0;
    translate: 0 2rem;
  }
  to {
    opacity: 1;
    translate: 0 0;
  }
}
```

**@starting-style for entry animations (dialogs, popovers, new elements):**

```css
dialog[open] {
  opacity: 1;
  scale: 1;
  transition:
    opacity 0.3s,
    scale 0.3s,
    overlay 0.3s allow-discrete,
    display 0.3s allow-discrete;

  @starting-style {
    opacity: 0;
    scale: 0.95;
  }
}
```

**Anchor positioning for tooltips and popovers:**

```css
.trigger {
  anchor-name: --trigger;
}

.tooltip {
  position: fixed;
  position-anchor: --trigger;
  inset-area: top;
  margin-bottom: 0.5rem;
}
```

**:has() for parent-aware styling:**

```css
/* Form group with error state */
.form-group:has(:invalid:not(:placeholder-shown)) {
  --field-border: var(--color-error);
}

/* Card with image gets different padding */
.card:has(> img) {
  padding-top: 0;
}
```

**View transitions for page navigation:**

```css
::view-transition-old(main) {
  animation: fade-out 0.2s ease-out;
}

::view-transition-new(main) {
  animation: fade-in 0.3s ease-in;
}

.hero-image {
  view-transition-name: hero;
}
```

### 3.3 Flutter Patterns to Use

**Material 3 theming:**

```dart
ThemeData(
  useMaterial3: true,
  colorScheme: ColorScheme.fromSeed(
    seedColor: const Color(0xFF6750A4),
    brightness: Brightness.light,
  ),
  textTheme: GoogleFonts.interTextTheme(),
)
```

**Adaptive layouts:**

```dart
Widget build(BuildContext context) {
  final width = MediaQuery.sizeOf(context).width;
  if (width >= 1200) return _buildDesktopLayout();
  if (width >= 600) return _buildTabletLayout();
  return _buildMobileLayout();
}
```

**Purposeful animation:**

```dart
AnimatedContainer(
  duration: const Duration(milliseconds: 300),
  curve: Curves.easeOutQuart,
  padding: isExpanded
    ? const EdgeInsets.all(24)
    : const EdgeInsets.all(16),
  decoration: BoxDecoration(
    borderRadius: BorderRadius.circular(isExpanded ? 16 : 12),
    color: isExpanded
      ? theme.colorScheme.surfaceContainerHighest
      : theme.colorScheme.surfaceContainer,
  ),
  child: content,
)
```

### 3.4 Interaction States

Every interactive element MUST have:

- **Hover**: subtle background shift or underline (web)
- **Focus-visible**: visible focus ring, never `outline: none` without replacement
- **Active/pressed**: slight scale or color shift
- **Disabled**: reduced opacity (0.5) + `cursor: not-allowed` / greyed out
- **Loading**: skeleton or spinner, never blank space

```css
.button {
  background: var(--accent);
  color: var(--text-on-accent);
  border: none;
  padding: 0.625rem 1.25rem;
  border-radius: 0.5rem;
  font-weight: 600;
  cursor: pointer;
  transition:
    background 0.15s,
    scale 0.1s;

  &:hover {
    background: var(--accent-hover);
  }
  &:focus-visible {
    outline: 2px solid var(--accent);
    outline-offset: 2px;
  }
  &:active {
    scale: 0.98;
  }
  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
}
```

### 3.5 Accessibility Built-In

Every element ships with:

- Semantic HTML: `<button>` not `<div onclick>`, `<nav>`, `<main>`, `<article>`, `<section>` with labels
- ARIA only when HTML semantics are insufficient
- Touch targets: minimum 44x44px (web), 48x48dp (mobile)
- Color contrast: 4.5:1 for normal text, 3:1 for large text
- Focus management: logical tab order, skip links on pages with navigation
- Flutter: `Semantics` widgets, `excludeFromSemantics` on decorative elements
- `prefers-reduced-motion`: disable/reduce all animations

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

---

## PHASE 4: RESPONSIVE / ADAPTIVE

### 4.1 Container Queries First

Use container queries for component-level adaptation. Reserve viewport queries for page-level layout only.

```css
/* Page layout — viewport query is appropriate here */
@media (min-width: 768px) {
  .page {
    grid-template-columns: 240px 1fr;
  }
}

/* Component adaptation — container query */
.card-wrapper {
  container-type: inline-size;
}

@container (min-width: 300px) {
  .card {
    /* horizontal layout */
  }
}
```

### 4.2 Content-Aware Sizing

- `field-sizing: content` for auto-sizing textareas and inputs
- `interpolate-size: allow-keywords` for smooth `height: auto` transitions
- `min()`, `max()`, `clamp()` for fluid sizing without breakpoints

### 4.3 Mobile-First Construction

- Start with the mobile layout, enhance for larger screens
- Touch targets 48px minimum
- Bottom-aligned primary actions (thumb zone)
- No hover-only interactions — everything must work with tap

---

## PHASE 5: SELF-HEALING VALIDATION

After building, validate:

### 5.0 Test-Run Gate (CRITICAL — learned from pet-sitter recall 2026-05-22)

Before any other validation, run the project's existing test suite — NOT to add new tests, but to detect regressions introduced by the design changes.

The 2026-04-24 pet-sitter `/design-stack` run was followed by an immediate round-2 commit that was essentially test updates the skill should have caught itself. The skill applied visual changes and committed without verifying that existing assertions still passed; the regression surfaced as the next commit.

Procedure:

1. Detect the project's test command from `package.json` scripts (look for `test`, `test:unit`), `pubspec.yaml` (`flutter test`), `Cargo.toml` (`cargo test`), or repo conventions.
2. **Record the baseline**: before applying ANY changes, run the test command once and capture pass/fail counts. If the suite is already red, note which tests fail and treat those as the baseline (don't try to fix unrelated pre-existing failures).
3. **After each auto-applied batch of design changes**, re-run the test command.
4. If any test that was previously green now fails: STOP. Do not commit. Investigate.
   - If the failure is a real regression (the change broke behavior), fix the underlying issue.
   - If the failure is a snapshot/golden test that needs updating because the visual genuinely changed and the new visual is correct: update the snapshot AS PART OF THIS COMMIT. Do not commit the visual change without the snapshot update — that's the exact failure mode the recall flagged.
   - If the test is a brittle text-string assertion (e.g., asserts on copy you intentionally changed): update it in this commit, with a note in the commit body.
5. Only proceed to 5.1 Build Check after the test suite is at-or-above the baseline.

Skip ONLY if there is genuinely no test infrastructure (`pnpm test` exits with "no tests found", `flutter test` reports no test files, etc.) — and log "no test infrastructure detected, skipping test-run gate" in the build summary.

### 5.1 Build Check

- Run the project's build/compile command (detect from package.json scripts, Makefile, pubspec.yaml)
- If build fails: read the error, fix it, rebuild
- Repeat up to 3 times

### 5.2 Import Check

- Verify all imports resolve to existing files
- Remove any unused imports
- Verify no circular dependencies introduced

### 5.3 Accessibility Spot Check

- Verify all `<img>` tags have `alt` attributes (or `Image` widgets have `semanticLabel`)
- Verify all buttons/links have accessible names
- Verify no `tabindex` values greater than 0
- Verify color contrast on primary text/background combinations

### 5.4 Consistency Check

- Verify colors used match design context (no magic hex values)
- Verify spacing follows the established scale
- Verify typography uses the defined type scale
- Verify component naming follows project conventions

### 5.5 Modern Pattern Check

- Verify `prefers-reduced-motion` is handled if animations were added
- Verify dark mode works if the project supports it
- Verify container queries are used where appropriate (not just viewport queries on components)

---

## PHASE 6: TELEMETRY AND REPORTING

### 6.1 Build Summary

Output what was built:

```
## Build Complete

**Built**: [component/screen name]
**Files**: [count] created, [count] modified
**Stack**: [framework + styling approach]
**Modern CSS/Platform Features Used**: [list]
**Accessibility**: [checks passed]

### What I Built
[2-3 sentences describing the interface and key design decisions]

### Design Decisions Made
- [Decision 1 and rationale]
- [Decision 2 and rationale]
- [Decision 3 and rationale]

### Files Changed
- `path/to/file.tsx` — [what and why]
- `path/to/styles.css` — [what and why]
```

### 6.2 Self-Evolution Notes

If during building you encountered patterns not covered by these instructions, or discovered better approaches than what's specified here, note them under "Suggested Skill Improvements" so the skill can be updated.

---

## CONSTRAINTS

- NEVER use AI-slop aesthetics (see Anti-AI-Slop Rules above).
- NEVER use `!important` unless overriding third-party CSS that cannot be configured.
- NEVER use `float` for layout. Grid and Flexbox only.
- NEVER add animation libraries (Framer Motion, GSAP, etc.) unless already in the project. Use CSS animations.
- NEVER ignore the existing design context. Match the codebase's visual language.
- ALWAYS write real, working code — not pseudocode or wireframe descriptions.
- ALWAYS include hover, focus, active, and disabled states on interactive elements.
- ALWAYS handle dark mode if the project has any dark mode support.
- ALWAYS use semantic HTML elements over generic divs/spans.
- ALWAYS make fluid/responsive by default — never fixed-width layouts.
