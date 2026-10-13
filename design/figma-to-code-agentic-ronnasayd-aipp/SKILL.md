---
name: figma-to-code-agentic
description: |
  Convert Figma designs into production-ready component code using an agentic loop that validates implementation against the design.

  Use this skill whenever: a Figma link or file is provided and the user wants code generated from it; the user says "generate this Figma design as React/Vue/HTML", "convert this Figma to code", "build a component from this design", "make it look exactly like Figma", or "match the design"; the user needs pixel-perfect design-to-development handoff; the user mentions needing to validate UI against a Figma spec.

  The skill reads design specs via Figma MCP, auto-detects the framework, generates code, renders a screenshot via browser automation, compares using SSIM (Structural Similarity Index), and iterates up to 10 times until reaching ≥0.9 visual similarity. Works for React, Vue 3, and vanilla HTML/CSS. Perfect for design system components, landing pages, or any UI that must match a Figma spec.
metadata:
  author: Ronnasayd Machado - github.com/Ronnasayd
  version: "1.0.0"
---

# Figma-to-Code Agentic

Generate pixel-perfect component code from Figma designs, iterating automatically until the implementation matches the spec.

## Quick Reference

| Script                             | Purpose                | When to use           |
| ---------------------------------- | ---------------------- | --------------------- |
| `scripts/compare_ssim.py`          | SSIM visual comparison | After each screenshot |
| `scripts/agentic_loop.py`          | Loop state tracker     | Throughout the loop   |
| `references/browser-automation.md` | Screenshot how-to      | Phase 2 setup         |
| `references/diff-analysis.md`      | Systematic diff guide  | When score < 0.9      |

---

## Phase 1: Setup

### 1a. Get the Figma Design

You need **both** the design specs and a reference screenshot.

**Via Figma MCP** (preferred):

```
1. Use Figma MCP to extract: layout, colors, typography, spacing, shadows, borders
2. Export the design frame as PNG at 1x (1280×720 or component's native size)
3. Save as figma_reference.png — this is the comparison target
```

**If no Figma MCP available:**

- Ask the user to paste the Figma link and export a PNG manually
- Proceed with specs described in the prompt; skip SSIM validation (document this)

### 1b. Detect Framework & Styling

Check in this order:

1. Explicit user request ("React", "Vue", "vanilla HTML")
2. Codebase context: scan `package.json`, existing components, imports
3. **Default**: React + Tailwind CSS

Styling approach: match the project's existing conventions (Tailwind, CSS Modules, styled-components, plain CSS).

### 1c. Generate Initial Component

Create a single file: `.jsx`, `.tsx`, `.vue`, or `.html`

**Must include:**

- All imports and dependencies
- Exact spacing, colors, fonts from Figma specs
- Responsive classes/logic (if design has breakpoints)
- Accessibility attributes (`aria-*`, semantic HTML)
- Comment: `// Figma match: initial generation (unvalidated)`

**Wrap in a render test page** (white background, viewport matching Figma export dimensions) for screenshot purposes.

---

## Phase 2: Validation Loop (up to 10 iterations)

Initialize the loop controller:

```bash
python scripts/agentic_loop.py <component_path> figma_reference.png --framework react
```

For each iteration:

### Step A — Screenshot

Use browser automation to render and capture. See `references/browser-automation.md` for platform-specific instructions (Playwright, Puppeteer, Chrome MCP).

**Key settings:**

- Same viewport dimensions as Figma export
- White background, 1x zoom (no DPI scaling)
- Wait for `networkidle` before capturing
- Disable CSS animations: `* { animation: none !important; transition: none !important; }`

### Step B — Compare

```bash
python scripts/compare_ssim.py figma_reference.png screenshot_iter_N.png --json --output-diff diff_N.jpg
```

Output: `ssim_score`, `verdict` (PASS/REVIEW/FAIL), `diff_regions` (top 5 areas of mismatch)

### Step C — Decide

| Score                                    | Action                                          |
| ---------------------------------------- | ----------------------------------------------- |
| ≥ 0.9                                    | ✅ **DONE** — return final code                 |
| 0.90–0.94                                | REVIEW — fix top diff regions, iterate          |
| < 0.90                                   | FAIL — check for structural issues first        |
| Stalled (< 0.001 gain over 3 iterations) | Stop, return best version, document open issues |
| Iteration 10 reached                     | Stop, return best version                       |

### Step D — Refine (if score < 0.9)

Read `references/diff-analysis.md` for a systematic guide to diagnosing and fixing differences.

**Priority order for fixes:**

1. **Layout/structure** — wrong element type, missing wrapper, wrong display mode
2. **Spacing** — padding/margin off by more than 4px
3. **Color** — hex values not matching Figma exactly
4. **Typography** — font size, weight, line-height
5. **Shadows/borders** — blur radius, spread, opacity

Make surgical edits addressing **multiple issues per iteration**. Don't rewrite the whole component.

---

## Output Format

**Component file:**

```
// [component-name].jsx — Figma match: 0.97 ✓ (3 iterations, viewport: 1280×720)
```

**Metadata block** (provide separately):

```
Framework: React / TypeScript
Styling: Tailwind CSS
Figma Link: https://figma.com/...
SSIM Score: 0.97
Verdict: PASS
Iterations: 3
Viewport: 1280×720
```

---

## Thresholds by Component Type

| Component type                            | Recommended threshold |
| ----------------------------------------- | --------------------- |
| Design system components (buttons, cards) | 0.9+                  |
| Landing page / hero sections              | 0.93+                 |
| Complex data tables / forms               | 0.90+                 |

---

## Common Issues

| Symptom                        | Likely cause                   | Fix                                                  |
| ------------------------------ | ------------------------------ | ---------------------------------------------------- |
| Score stuck ~0.88              | Font rendering / anti-aliasing | Use web fonts; accept if visually correct            |
| Screenshot blank               | Component render error         | Check console errors; verify dependencies            |
| Colors off                     | Hex mismatch or color space    | Copy hex from Figma exactly; check `rgb()` vs `hex`  |
| Layout breaks during iteration | Over-aggressive edits          | Roll back last change; make smaller adjustments      |
| Score regresses                | New bug introduced             | Check diff vs previous iteration; revert last change |
| Max iterations reached         | Ambiguous or complex design    | Document open issues; escalate to designer           |

---

## When to Skip SSIM

- No browser automation MCP available → generate code from specs only; note "SSIM validation skipped"
- No Figma MCP available → generate from user-described specs; skip validation
- Design has significant animations/interactions → validate static structure only; document interaction specs separately

---

## Limitations

- **Static only**: generates visual structure. Animations, complex hover states, and interactions are documented as specs, not implemented.
- **Image assets**: Figma images become `<img alt="placeholder" />` unless explicitly provided.
- **Single viewport**: validates at one breakpoint. For multi-breakpoint designs, iterate per breakpoint or use media queries.
- **Font rendering**: varies across OS. Use web fonts (Google Fonts, etc.) for consistency.
- **SSIM sensitivity**: 0.92–0.9 often looks visually identical due to anti-aliasing. Don't over-optimize.
