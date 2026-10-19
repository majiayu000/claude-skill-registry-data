---
name: frontend-design-review
description: >
  Review the visual and interaction design of a web UI from screenshots and code:
  hierarchy, spacing and alignment, typography, color and tokens, responsive behavior,
  states (empty, loading, error, hover, focus, disabled), consistency with a design
  system, and polish. Use when asked to critique, polish, or sanity-check a page,
  component, or Figma-to-code result, or to give a design-quality pass before release.
  Produces prioritized, actionable findings with concrete CSS/markup changes. Do not use
  for accessibility conformance (web-accessibility-review), rendering performance
  (react-performance), HTML/CSS syntax questions (web-html-css), or brand strategy.
compatibility: >
  Works with screenshots, a running dev server viewed in a browser at multiple
  viewport widths, or source code (HTML/CSS/Tailwind/CSS-in-JS/React).
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "design-review, ui, ux, css, typography, spacing, responsive, design-tokens"
  topics: "frontend, design, quality"
---

# Frontend Design Review

A design review produces decisions a developer can act on, not taste commentary. Every finding names what is wrong, why it hurts the user, and the specific change. Review at the level the project cares about: match the existing design system before importing new ideas.

Related skills: `web-accessibility-review` (contrast, focus, semantics as conformance), `web-html-css` (implementation), `react-composition-patterns` (component API), `browser-debugging` (inspecting computed styles), `playwright-testing` (screenshot regression).

## When to use / not use

Use for: pre-release polish, PR reviews with UI changes, "this looks off" requests, responsive audits, design-system drift checks, reviewing generated UI.

Do not use for: a11y conformance claims, performance profiling, product or copy strategy, or inventing a brand from nothing without constraints (ask for tokens, references, or audience first).

## Non-negotiable rules

1. **Evidence from the rendered result.** Look at the actual page at several widths (for example 360, 768, 1280 CSS px) and in both light and dark modes if supported, not only at the code.
2. **Respect existing tokens and components.** Prefer the project's spacing scale, type scale, and colors. Flag one-off magic numbers instead of adding more.
3. **Prioritize.** Label findings blocker / should-fix / polish. Do not bury a broken mobile layout under nitpicks.
4. **Be specific and reversible.** Suggest concrete values and show the diff; do not rewrite the whole stylesheet.
5. **Do not fabricate user research** or claim usability test results you did not run.

## Workflow

### 1. Establish context
Audience, primary task on this screen, device mix, existing design system or tokens, brand constraints, supported browsers. If unknown, state assumptions.

### 2. Capture
Render the page (dev server) and capture or view it at narrow, medium, and wide widths. Check zoom to 200%, long content (long names, many items), no content (empty), slow data (loading), failure (error). Use DevTools device emulation; real devices when touch matters.

### 3. Review in layers (top-down)
1. **Purpose and hierarchy**: is the primary action obvious within a couple of seconds? One primary button per view area; size, weight, and contrast should rank importance.
2. **Layout and spacing**: consistent scale (for example 4/8-based), grouping by proximity (related items closer than unrelated), alignment to a grid or consistent edges, enough whitespace, consistent gutters.
3. **Typography**: limited families and sizes from a scale; body text around 16 px or more; comfortable line length (roughly 45-80 characters) and line height (about 1.4-1.6 for body); clear heading hierarchy; avoid centered long paragraphs.
4. **Color**: a small palette from tokens; semantic colors (success, warning, danger) used consistently; sufficient contrast (verify ratios with a tool, see `web-accessibility-review`); dark mode checked rather than inverted by hand.
5. **Components and consistency**: same control looks and behaves the same everywhere; radius, border, shadow, and icon style consistent; no near-duplicates.
6. **States and feedback**: hover, focus-visible, active, disabled, loading, empty, error, success all designed; buttons show progress; forms show inline validation; destructive actions confirm or allow undo.
7. **Responsive behavior**: no horizontal scroll at 320-360 px; touch targets comfortably large; navigation adapts; images scale (`max-width: 100%`, set `width`/`height` or `aspect-ratio` to prevent layout shift); tables have a strategy (scroll container, stacked cards).
8. **Motion**: purposeful, short (roughly 150-300 ms for UI transitions), respects `prefers-reduced-motion`.
9. **Content and microcopy**: labels say what happens; error messages explain how to fix; consistent terminology and capitalization.
10. **Polish**: icon alignment with text baselines, image quality, truncation with ellipsis and title/tooltip where needed, favicon and titles.

### 4. Write findings
Format each as: **[priority] Where** - problem - user impact - fix (with value/snippet).

### 5. Re-check
After changes, re-capture the same viewports and states; confirm no regressions.

## Worked example

Review of a settings page:

- **[blocker] Mobile 360 px**: the data table overflows and the page scrolls horizontally. Impact: key columns unreachable. Fix: wrap in a scroll container.
```css
.table-wrap { overflow-x: auto; }
.table-wrap table { min-inline-size: 40rem; }
```
- **[should-fix] Hierarchy**: "Save", "Cancel", and "Reset" are all filled blue, so the primary action is unclear. Fix: Save keeps the primary style, Cancel becomes secondary (outline), Reset becomes a text button.
- **[should-fix] Spacing**: gaps of 10, 14, and 18 px mixed in one card. Fix: use the 8 px scale tokens (`--space-2`, `--space-3`).
- **[polish] Empty state**: an empty table shows only headers. Fix: add an illustration-free message and a primary "Add key" action.
- Not checked: dark mode and RTL (state this explicitly).

## Anti-patterns

- Reviewing only a desktop screenshot.
- "Make it pop" or "feels off" with no concrete change.
- Introducing new colors, fonts, or radii that bypass the design system.
- Pixel-peeping before fixing hierarchy and layout.
- Overusing shadows, gradients, and animations as a substitute for structure.
- Low-contrast gray text for essential information.
- Designing only the happy path.
- Fixed pixel heights that clip content when text grows.
- Claiming accessibility conformance from a visual pass.

## Verification checklist

- [ ] Checked at least three viewport widths and 200% zoom
- [ ] Checked empty, loading, error, and long-content states
- [ ] Primary action unambiguous per view
- [ ] Spacing, type, and colors come from tokens or are flagged
- [ ] Focus, hover, disabled states exist
- [ ] Findings prioritized with concrete fixes
- [ ] Unchecked areas (dark mode, RTL, browsers) listed

## References

- [Review checklist and CSS recipes](references/checklist.md)
- [Scenarios for evaluating this skill](references/scenarios.md)
- [Sources and provenance](references/sources.md)
