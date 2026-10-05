---
name: ui-fix-observe-first
description: >-
  Use when fixing, auditing, improving, or building any web UI — before reading
  or editing component code. Fires on contrast/a11y/overflow/responsive/hover-
  focus/layout complaints, polish, audit, or any visual change. Never diagnose a
  UI defect from code alone: render at real viewports, measure (axe / contrast /
  a11y tree / console / keyboard / reflow), then cite the measurement.
---

# UI fix — observe first

## Rules

1. **Never diagnose a UI change from code alone — render, measure, cite.**
   Runtime defects (contrast, overflow, wrap, responsive, hover/focus, layout
   shift, stacking) do not exist in the JSX. No measurement = not a finding.
2. **Fix correctness directly; settle taste with evidence.** Prefer competitive
   pattern research (Vercel / Linear / Stripe and similar) over asking the user
   to invent aesthetic direction mid-fix.

## Flow A — fix / improve an existing UI

1. **RENDER** the live page at the layout’s target widths (typically **375 + 1440**).
   Public pages → browser / DevTools MCP. Authed apps → a session that can see
   the real UI (logged-in browser automation when needed).
2. **OBSERVE** with layered tools (automation alone misses a large share of issues;
   Lighthouse is a floor, not conformance):
   - **axe-core** for contrast, labels, ARIA, duplicate IDs.
   - **Computed-style WCAG contrast** when axe cannot run (AA normal ≥4.5,
     large/UI ≥3.0).
   - **A11y tree**, console errors, full-page screenshot.
   - **Keyboard pass**: Tab from the top — visible focus, order, no traps,
     focus not obscured (WCAG 2.2).
   - **Reflow** at ~320px / 200% zoom; **24px** tap targets where relevant.
3. **Judge the whole page, not only your widget.** Green per-control metrics do
   not mean the surface is done. Ask what the nearest sibling control offers
   that yours does not. Check fail-soft / session-scoped state / label wrap
   across navigation, not only at rest.
4. **PIN** the defect with a cited measurement (ratio, px, element, axe rule).
5. Split findings:
   - **Correctness** (contrast, a11y, CLS, overflow, tokens, focus) → fix on
     design tokens (`var(--*)`), one class at a time; avoid raw one-off hex.
   - **Aesthetic direction** → research comparable products, pick a clear
     direction, ship quick wins.
6. **GATE** with the project’s full typecheck / lint / test suite (not a scoped
   run that hides breakage). Prefer static a11y (e.g. eslint-plugin-jsx-a11y).
7. **SHIP** via normal PR + CI.
8. **RE-RENDER** to verify the fix and no regressions (dark/light/mobile as
   applicable). Track axe violations, contrast ratios, keyboard pass.
9. Optionally score with `frontend-audit`’s rubric; do not inflate scores.

## Flow B — new UI

Declare design tokens first → generate (Claude Design / Figma / Stitch as
appropriate) → assets → build on tokens → then Flow A observe steps.

## Cross-references

- `frontend-audit` — rubric after fixes
- `ai-wayfinders` / `ai-trust-builders` / `ai-governors` — AI product UX patterns
- `real-user-qa` — upstream QA scenarios when present
