---
name: figma-matcher
description: Enforces pixel-perfect implementation of Figma designs by exhaustively extracting every visual property from Figma, spinning up Chrome DevTools to measure the current implementation, building a full comparison checklist, and fixing all discrepancies in a single pass. MUST be triggered whenever implementing UI from Figma, fixing styling to match Figma, or any time the user says "match Figma", "check against Figma", "compare to design", "the design doesn't match", "colors are wrong", "spacing is off", or references a Figma URL in a styling context. Also trigger when you just finished writing CSS/styling code that was informed by a Figma design. This skill is NON-OPTIONAL when Figma designs are involved in styling work.
---

# Figma Matcher

A rigid, checklist-driven process for verifying that implementation matches Figma designs exactly. No visual impressions. No "close enough." Every property gets extracted, compared numerically, and verified.

## Why This Exists

Without this process, you will:
- Pick component variants by name without checking their actual hex values
- Assume "gray" means the same gray
- Skip checking spacing, border-radius, font-weight, opacity
- Iterate 3-5 times with the user correcting you each time

This skill eliminates all of that by forcing exhaustive upfront extraction.

## HARD GATE

You are FORBIDDEN from calling `Edit` or `Write` on any `.scss`, `.css`, `.sass`, `.less`, or `.styled.*` file until you have:
1. Completed Steps 1-4 below
2. Output the full comparison table to the user
3. Received acknowledgment or no objection from the user

If you catch yourself about to edit a styling file without having shown the comparison table, STOP. Go back to Step 1.

## The Process

You MUST complete every step in order. Do not skip steps. Do not combine steps. Do not start writing CSS until Step 5.

### Step 0: Find the Frames and Inventory EVERYTHING In Them

Before extracting anything, locate the exact node ids and enumerate what the design actually contains.

**Finding node ids when you only have a file key or section name:**
- `get_metadata` with no nodeId lists top-level pages; with a page id it should enumerate the tree — but page-level enumeration sometimes returns an empty `width="0"` canvas. Node-level calls still work, so the gap is discovery only.
- When enumeration fails, drive the browser: open the Figma file in the user's Chrome (debug profile), use Figma's **Find** (the search icon in the left sidebar), search the frame/section name, click "See results on other pages" if needed, then click each result and read the `node-id` from the URL. Collect all of them before extracting.

**Coverage rule — account for every child, then decide:**
Run `get_metadata` on the section/frame and list EVERY child frame and instance: desktop frame, mobile frames (closed AND open/overlay states), popout menus, dropdowns, sheets, and every instance inside container rows. For each one, explicitly classify it as (a) in scope, (b) already implemented elsewhere (verify — go look), or (c) out of scope per the user. Never dismiss an instance as "page chrome" without checking the page actually renders it in this context — a tabs-row instance can contain a control (e.g. a store-status dropdown) that the current page is missing entirely. A missed instance is a missed feature, not a styling nit.

Interaction states are frames too: a mockup with a cursor on a row is showing you the hover state; a second mobile frame with an overlay is showing you the opened sheet. Both become checklist rows.

### Step 1: Extract ALL Properties from Figma — Fetch, Don't Transcribe

Machine-readable extraction first; hand-reading generated output is the biggest error source. In order:

1. **`get_variable_defs`** on the main node — returns the design-token map as JSON (`{"Gray/Gray30": "#E7E7E7", "Spacing/spacing-small": "8", "Regular/Medium": "Font(...16, weight: 500, lineHeight: 24...)"}`). This is ground truth for every tokenized color, spacing, radius, font, and shadow. Save it; Step 2 joins against it.
2. **`get_metadata`** on the frame — exact geometry for free: row heights, column widths, x/y offsets, element sizes. Gaps and paddings fall out of the coordinate math (`y=83, height=56, next y=155` → 16px gap).
3. **`get_design_context`** on SMALL nodes only — one atomic piece at a time (a header cell, a row cell, a button, a menu). Large frames silently degrade to sparse metadata with a note telling you to recurse into sublayers; budget for one call per atomic component.
4. **`get_screenshot`** on every frame (desktop, mobile, open states) — download the PNGs; they are the Step 6 visual baseline.
5. **Optional, most exact: Figma REST API** — `GET https://api.figma.com/v1/files/:key/nodes?ids=:nodeId` with an `X-Figma-Token` PAT returns the raw node JSON: fills/strokes as r/g/b/a **floats 0-1 (multiply by 255)**, `cornerRadius`, auto-layout paddings, `itemSpacing`, text `style`, `effects`. Use when a PAT is available; note the sandbox may need `api.figma.com` allowed. The Variables REST endpoint (`/variables/local`) is Enterprise-only — `get_variable_defs` is the plan-independent substitute.

For each visual element, extract into a structured checklist:

**Colors** (resolve ALL to hex + rgba):
- Background color (including gradients, overlays, composite backgrounds)
- Border color + opacity
- Text color
- Icon color/fill
- Button background (default, hover, active, disabled states)
- Shadow colors

**Typography:**
- Font family
- Font weight (numeric, not name)
- Font size (px)
- Line height (px or unitless)
- Letter spacing
- Text transform

**Spacing:**
- Padding (top, right, bottom, left)
- Margin (top, right, bottom, left)
- Gap between elements

**Layout:**
- Width (fixed, %, auto, fill)
- Height (fixed, auto, fit-content)
- Display (flex, grid, block)
- Flex direction, align-items, justify-content
- Border radius (each corner if different)

**Borders:**
- Border width
- Border style
- Border color + opacity

**Effects:**
- Box shadow (offset-x, offset-y, blur, spread, color)
- Opacity
- Backdrop filter

**Button/Interactive elements:**
- Full width vs auto width
- Text wrapping behavior (nowrap, normal)
- Min-width constraints

Write these into a numbered checklist. Each item is a row you will verify later.

### Step 2: Resolve SCSS/CSS Variables to Actual Values

For every color, spacing, or size token in your codebase that might be relevant:

1. `grep` the variables file (e.g., `_settings.colors.scss`) to find the actual hex value
2. Follow any aliases (e.g., `$color-ui50: $color-gray50` -> find `$color-gray50: #BDBDBD`)
3. Record the full chain: `$variable-name` -> `$alias` -> `#hexvalue` -> `rgba(r, g, b, a)`
4. Compare against Figma values from Step 1

If a variable doesn't match exactly, note it. You will need a custom override, not a "closest match."

Example:
```
Figma border: rgba(103, 103, 103, 0.5) = #676767 at 50% opacity
$color-ui50 = $color-gray50 = #BDBDBD  --> NOT a match (189 != 103)
$color-ui70 = $color-gray70 = #676767  --> EXACT MATCH
```

### Step 3: Measure Current Implementation via Chrome DevTools

1. Ensure the dev server is running. If not, start it.
2. Use Chrome DevTools MCP to navigate to the page showing the component.
3. Take a screenshot of the current implementation (for visual comparison with Figma screenshot from Step 1).
4. For EVERY element in your checklist from Step 1, run `evaluate_script` to get computed styles:

```javascript
const el = document.querySelector('.your-selector');
const styles = window.getComputedStyle(el);
JSON.stringify({
  backgroundColor: styles.backgroundColor,
  borderColor: styles.borderColor,
  borderWidth: styles.borderWidth,
  borderRadius: styles.borderRadius,
  padding: styles.padding,
  paddingTop: styles.paddingTop,
  paddingRight: styles.paddingRight,
  paddingBottom: styles.paddingBottom,
  paddingLeft: styles.paddingLeft,
  margin: styles.margin,
  color: styles.color,
  fontSize: styles.fontSize,
  fontWeight: styles.fontWeight,
  fontFamily: styles.fontFamily,
  lineHeight: styles.lineHeight,
  letterSpacing: styles.letterSpacing,
  gap: styles.gap,
  width: styles.width,
  height: styles.height,
  minWidth: styles.minWidth,
  maxWidth: styles.maxWidth,
  display: styles.display,
  flexDirection: styles.flexDirection,
  alignItems: styles.alignItems,
  justifyContent: styles.justifyContent,
  boxShadow: styles.boxShadow,
  opacity: styles.opacity,
  whiteSpace: styles.whiteSpace,
  textOverflow: styles.textOverflow,
  overflow: styles.overflow,
});
```

Do this for EVERY element in the checklist. Not just the ones you think might be wrong. Check children, containers, buttons, icons, text spans, everything.

**Also measure the states, and know the measurement traps:**
- **Open states**: click the dropdown/menu/sheet open inside `evaluate_script` (a short `await` after the click), then measure the popout: width, radius, shadow, item font, item height, item padding. Popouts are checklist rows, not bonuses.
- **Hover cannot be measured synthetically**: `dispatchEvent(mouseover)` does NOT apply `:hover` CSS. Verify hover styles by reading the SCSS, not by measuring a synthetic hover — a transparent reading proves nothing.
- **Mobile pass**: `resize_page` to the design's mobile frame size (usually 390×844), reload, and re-measure the mobile checklist rows. Restore the viewport when done.
- **Position relationships count**: e.g. a menu that "expands in place of" its trigger should top-align with it (`menu.top ≈ toggle.top`), not drop below. Measure `getBoundingClientRect` of both and compare.

### Step 4: Build the Comparison Table and Present It

Create a markdown table with columns:

| # | Element | Property | Figma Value | Current Value | Match? | Fix |
|---|---------|----------|-------------|---------------|--------|-----|
| 1 | Banner container | background-color | rgba(103,103,103,0.08) | rgba(189,189,189,0.08) | MISMATCH | Use $color-ui70 instead of $color-ui50 |
| 2 | Banner container | border-color | rgba(103,103,103,0.5) | rgba(189,189,189,0.8) | MISMATCH | transparentize($color-ui70, 0.5) |
| 3 | CTA button | background-color | rgba(103,103,103,0.15) | rgba(0,85,255,0.15) | MISMATCH | transparentize($color-ui70, 0.85) |

Fill in EVERY row from your checklist. Mark each as MATCH or MISMATCH. When both sides came out of Steps 1 and 3 as JSON, prefer joining them with a small script (Figma floats ×255 for colors; tolerance ≤2/255 per channel, ≤1px for geometry) so no row can be mis-copied or skipped — you write only the Fix column.

For mismatches, specify:
- Which file to change
- Which selector/property
- The exact new value (using the project's variable system where possible)

**Deliberate divergences get their own labeled rows**, not silent "fixes": features added after the frame was drawn (an extra menu item the team ratified), placeholders the user explicitly approved (a native confirm pending a designed dialog), or house-component standards not worth forking (pager copy). Name each one and why it stays.

**Shared components need a decision before the Fix column is final**: if a mismatched style lives on a component other features use, ask the user — scoped override (this feature only) or fix the shared component ("correct everywhere")? Do not silently widen the blast radius, and do not silently fork either.

**OUTPUT THIS TABLE TO THE USER.** Do not proceed until you have done so.

Also show side-by-side screenshots: Figma (from Step 1) and current implementation (from Step 3).

### Step 5: Implement All Fixes in a Single Pass

Only after the table is complete and shown to the user:
- Make ALL changes at once based on the Fix column
- Do not iterate one property at a time
- Do not make partial fixes

**Known implementation traps (each one has burned a real pass):**
- **Icon components may hoist your className onto the `<svg>` itself** (react-inlinesvg does). `.my-icon svg { ... }` then matches nothing — size the class directly and keep only `path`/`circle`/`line` fill/stroke overrides nested. Also check whether the icon is fill-based or stroke-based before writing `fill: currentColor`.
- **Match the house stylesheet's specificity, then add one class.** A scoped `.feature table th` loses to `.house-table table thead tr th`. Mirror the full chain and prefix your block class. For third-party inline styles (e.g. a dropdown's positioning `min-width`), `!important` is the sanctioned tool — copy the existing precedent comment style.
- **Inline flex the trigger buttons**: global button styles plus baseline-aligned inline children inflate line boxes; an explicit `height` + `inline-flex` centering is how you hit an exact design height.
- **`table-layout: fixed` is what makes % column widths and cell ellipsis real.** Give the flexible columns explicit widths only where the design fixes them; leave the rest auto so the browser splits them equally, exactly like equal-width design columns.

### Step 6: Verify Until Zero Discrepancies

`/goal` is a UI command — you cannot invoke it yourself. If the session would benefit from the goal loop, ask the user to run `/goal` with the condition below; otherwise run the same loop manually and do not stop until it's satisfied:

```
/goal For every row in the Figma comparison checklist: re-run evaluate_script via Chrome DevTools on the live page, rebuild the full comparison table, and confirm every row shows MATCH (tolerance: <=2 subpixel rounding in rgba channels). Then take a fresh screenshot and compare side-by-side with the Figma screenshot from Step 1 confirming zero visible differences in color, spacing, sizing, typography, borders, shadows, or layout. Not met until the rebuilt table has 0 MISMATCH rows AND the screenshot comparison shows 0 visual discrepancies.
```

If the user sets it, the goal loop keeps you working across turns until the condition is met and prevents premature completion. If not, the loop below is still mandatory — run it yourself.

#### Each verification pass within the goal:

1. Reload the page in Chrome DevTools
2. Re-run the SAME `evaluate_script` queries from Step 3 for EVERY row in the checklist (not just previous mismatches)
3. Build a fresh comparison table from the new measurements
4. Take a new screenshot
5. Compare screenshot visually against Figma screenshot from Step 1
6. Count: `mismatches_css` = rows where Current != Figma; `mismatches_visual` = visible discrepancies in screenshot
7. IF `mismatches_css == 0` AND `mismatches_visual == 0`:
     - Show the final comparison table with ALL rows marked MATCH
     - Show final screenshot alongside Figma screenshot
     - State: "0 CSS mismatches, 0 visual discrepancies"
     - Goal is satisfied
8. ELSE:
     - Log all remaining discrepancies in an updated table
     - Fix them
     - Run another pass

#### The goal is NOT met until:

- You have re-measured every single CSS property (not just the ones you fixed)
- The fresh comparison table shows MATCH on every row
- A new screenshot has been taken and compared to Figma
- No visual discrepancies remain between the screenshots

"Should match now" does not satisfy the goal. "Looks correct" does not satisfy the goal. Only measured values and screenshots satisfy the goal.

## Rules

1. **Never pick a variant/token by name.** Always resolve to hex and compare numerically.
2. **Never say "close enough."** Either the rgba values match or they don't. A 1-2 unit rounding difference in subpixel rendering is acceptable. A different base color is not. One principled exception: values that render identically by spec count as MATCH — e.g. `border-radius: 100px` vs the design's `50px` on a 40px-tall pill (both clamp to height/2). Note the equivalence in the row.
3. **Never start writing CSS/SCSS before completing Steps 1-4 and showing the table.**
4. **Never skip Chrome DevTools.** Even if you "know" what the computed style is. Measure, don't assume.
5. **Every property gets checked.** Not just the ones that look wrong.
6. **If an existing component variant doesn't match exactly,** add a className override with the correct values. Don't use the "closest" variant and hope nobody notices.
7. **If the dev server isn't running,** start it before Step 3. Do not skip Step 3.
8. **Screenshots are mandatory** at Step 1 (Figma), Step 3 (before), and Step 6 (after).
9. **Button widths and text wrapping** must be explicitly checked. If a button is full-width in Figma, verify it's full-width in implementation. If text shouldn't wrap, verify `white-space: nowrap` — and remember the design usually wants ellipsis truncation, not wrapping, in table cells.
10. **Every frame and instance from Step 0 must be accounted for** — in the table, as a deliberate divergence, or as confirmed-already-implemented. Unaccounted = not done.
11. **Icon glyphs are properties too.** A circled plus is not a bare plus; compare the actual glyph in the screenshot, not just the size.

## When This Skill Applies

- Implementing any UI from a Figma design
- Fixing styling discrepancies reported by the user
- After writing CSS/SCSS that was informed by a Figma design
- Any time a Figma URL is mentioned in a styling context
- When the user says anything resembling "doesn't match the design"
- Proactively, after completing any styling work that references Figma

## Output Format

Always output:
1. The numbered checklist (Step 1)
2. The variable resolution table (Step 2)
3. The full comparison table (Step 4)
4. Screenshots: Figma vs Current vs After-fix
