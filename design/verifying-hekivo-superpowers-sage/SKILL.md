---
name: superpowers-sage:verifying
description: >
  Verify implemented work meets acceptance criteria — run tests, check PHPCS,
  validate Blade output, lando phpunit, lando phpcs, lando yarn test,
  Playwright tests, accessibility check, post-implementation verification,
  done criteria validation, checklist review, verification phase
user-invocable: true
argument-hint: "[section name or plan path]"
---

# Verifying — Visual Comparison with Design Reference

Compare implemented sections against design reference using visual analysis.

## Inputs

$ARGUMENTS

## Procedure

### 0) Playwright gate

Before any verification work, ToolSearch for `mcp__plugin_playwright_playwright__browser_take_screenshot`.

If NOT found:
```
⛔ Cannot verify without Playwright MCP.

Install: claude mcp add playwright -- npx -y @anthropic/playwright-mcp
Restart session after installing. Stop.
```

Do NOT proceed to reference source detection.

### 1) Determine reference source

Priority order:

0. **Live design MCP (Priority 0 — preferred when MCP is configured):**
   - Figma: `get_design_context` + `get_metadata`
   - Paper: `get_computed_styles` + `get_node_info`
   - Pencil: `batch_get(resolveVariables: true)` + `batch_get(readDepth: 4)`
   - Stitch: `get_screen`
   Use when the design MCP is active in the session — live reference is always more accurate than cached assets.
1. **Spec file**: `docs/plans/<active-plan>/assets/section-*-spec.md` — read “Verification Inputs” block to get url, selector, and ref path
2. **Plan assets**: `docs/plans/<active-plan>/assets/section-*.png` — reference image for comparison
3. **Last resort**: ask user to provide screenshot or describe expected appearance

### 1b) Node geometry (multi-column / offset components)

When the reference source is a design MCP **and** the component contains a grid with 2+ columns, offset positioning, or nested containers, fetch node geometry before capturing the implementation screenshot:

- **Figma**: call `get_metadata` — returns `x`, `y`, `width`, `height` for each direct child
- **Paper**: call `get_node_info` — returns width + computed sizes for selected node
- **Pencil**: call `batch_get(readDepth: 4)` — returns layout children with dimensions
- **Stitch**: column count and widths visible in the `get_screen` response

Use these values to confirm column widths (e.g., a 60/40 split) before comparing screenshots. Skipping this step on multi-column layouts is a common source of false MATCH verdicts.

### 2) Capture implementation

1. Read `Verification Inputs` block from the spec file — extract `url`, `selector`, `ref`
2. Read canonical viewport width from `plan.md` frontmatter (`viewport-width` field, default `1440` if absent)
3. Set viewport: `mcp__plugin_playwright_playwright__browser_resize` to `{viewport-width} x 900` before navigating
4. Navigate Playwright to `url`: `mcp__plugin_playwright_playwright__browser_navigate`
5. Take screenshot scoped to `selector`:
   `mcp__plugin_playwright_playwright__browser_take_screenshot`
6. If `selector` fails (element not found), take full-page screenshot and note the difference

### 3) Compare visually

Read both reference and implementation images. Compare on these axes:

| Axis | Check |
|---|---|
| **Layout** | Grid structure, column count, alignment, flex direction |
| **Content** | Headlines match? Body text match? All items present? |
| **Colors** | Background, text, accent colors match? |
| **Typography** | Font size, weight, family approximately correct? |
| **Spacing** | Padding, margins, gaps reasonable? |
| **Icons** | Correct icon set? Right icon names? |
| **Images** | Placeholder or actual? Right aspect ratio? |
| **Responsive** | Does the layout adapt appropriately? |

### 3b) Style spot-check (paper sources only)

This step is **additive** — it runs only when `assets/section-{name}.styles.json` exists (i.e., the source was paper). For all other sources, skip silently and proceed to step 4.

1. Read `docs/plans/<active-plan>/assets/section-{name}.styles.json`
2. For each key property (typography, colors, spacing, border-radius), find the implemented value:
   - **Tailwind class** (`p-6`, `text-lg`, `bg-slate-900`) — resolve to its real value via the project's Tailwind config (`tailwind.config.js` or `@theme` block in `resources/css/app.css`). For example, `p-6` → `padding: 1.5rem` → `24px`.
   - **Arbitrary value** (`p-[23px]`) — capture the literal between brackets.
3. Compare design value vs implemented value. Produce a per-section report block:

```
### Style Spot-Check
✓ padding:    design=24px, impl=p-6 (24px)
✗ font-size:  design=18px, impl=text-base (16px)  — DRIFT
✓ color:      design=#0F172A, impl=bg-slate-900 (#0F172A)
⚠ gap:        design=32px, impl=gap-[31px] — arbitrary value, near-match
```

4. **Non-fatal**: drift here does NOT block verification. The drift items are surfaced as warnings inside the final report (step 4) under a `### Style Drift` subsection. The user decides whether to adjust.

### 4) Report findings

Output a structured report:

```markdown
## Verification: {Section Name}

**Status:** MATCH | DRIFT | MISSING

### Comparison
| Axis | Status | Notes |
|---|---|---|
| Layout | {pass/drift} | {details} |
| Content | {pass/drift} | {details} |
| Colors | {pass/drift} | {details} |
| Typography | {pass/drift} | {details} |
| Spacing | {pass/drift} | {details} |

### Issues Found
- {specific issue with fix suggestion}

### Style Drift
{omit this section if source was not paper, or no drift found.
 Otherwise list the ✗ and ⚠ lines from the spot-check.}

### Recommendation
{proceed / fix before continuing}
```

### 5) Act on findings

- **MATCH**: Mark component as verified, proceed
- **DRIFT**: List specific fixes needed, implement if in `/building` flow
- **MISSING**: Elements from design not implemented — flag for implementation

## Key Principles
- **Read images from disk** — always use Read tool for plan assets
- **Be specific** — "the grid should be 3 columns, got 2" not "layout is wrong"
- **Compare content verbatim** — headlines and body text must match exactly
- **Use base skill**: `verification-before-completion` for completion gate
