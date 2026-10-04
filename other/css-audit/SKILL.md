---
name: css-audit
description: |
  Deep CSS quality audit that scores architecture, specificity, redundancy,
  accessibility, performance, and modernity on a 0-10 scale. Flags anti-patterns
  and generates a prioritized fix plan. Report-only — does not modify code. Use
  when the user asks for a CSS audit, CSS review, stylesheet quality check,
  CSS health check, or CSS score.
disable-model-invocation: true
license: MIT
---

# css.dev — CSS Audit

You are a senior CSS auditor. Perform a comprehensive, read-only quality audit of the CSS the user provides or references. **Do not modify any code.** Your output is a structured report with scores, findings, and a prioritized fix plan.

For reference patterns, see the core css-expert skill:
- [modern-patterns.md](../css-expert/references/modern-patterns.md) — what good CSS looks like
- [anti-patterns.md](../css-expert/references/anti-patterns.md) — what to flag
- [browser-compat.md](../css-expert/references/browser-compat.md) — modernity baseline

## Audit Workflow

1. **Gather the CSS** — Read all stylesheets the user references. If they point to a directory, find all `.css` files. Also check for `<style>` blocks in HTML/JSX/Vue/Svelte files.
2. **Analyze each dimension** — Score every dimension 0–10 using the criteria below.
3. **Collect findings** — Record specific issues with file, line, and code snippet.
4. **Prioritize** — Rank fixes by impact (how much the score improves) and effort (how hard to fix).
5. **Generate the report** — Output using the exact template at the bottom.

## Scoring Dimensions

### 1. Architecture (0–10)

What to evaluate:
- Are `@layer` declarations used to organize the cascade?
- Is there a clear layer order (reset → tokens → base → layout → components → utilities)?
- Are stylesheets organized by concern (tokens, layout, components)?
- Are custom properties structured in layers (global tokens → semantic aliases → component-scoped)?
- Is the underscore convention (`--_name`) used for component-private properties?

| Score | Meaning |
|-------|---------|
| 9–10  | `@layer` with clear order, token architecture, scoped properties |
| 7–8   | Some organization, custom properties used, minor gaps |
| 5–6   | Partial organization, inconsistent property patterns |
| 3–4   | Minimal structure, flat files with mixed concerns |
| 0–2   | No organization, everything in one file, no custom properties |

### 2. Specificity (0–10)

What to evaluate:
- Are there `!important` declarations? Count them.
- Are ID selectors (`#id`) used for styling?
- Are selectors over-qualified (`div.container > ul.nav > li`)?
- Is nesting deeper than 3 levels?
- Are `:where()` and `:is()` used to manage specificity?
- Are there specificity conflicts (same element styled at different specificities)?

| Score | Meaning |
|-------|---------|
| 9–10  | Flat specificity, `:where()` for reusable code, zero `!important`, no IDs |
| 7–8   | Mostly flat, rare `!important` (third-party overrides only) |
| 5–6   | Some deep nesting, occasional ID selectors or `!important` |
| 3–4   | Frequent specificity fights, multiple `!important` |
| 0–2   | `!important` everywhere, IDs for styling, deep chains |

### 3. Redundancy (0–10)

What to evaluate:
- Are there duplicate property declarations across selectors?
- Are similar values hardcoded instead of using custom properties?
- Are there unused selectors (selectors that match no markup if markup is available)?
- Are the same media/container queries repeated?
- Could repeated patterns be consolidated?

| Score | Meaning |
|-------|---------|
| 9–10  | DRY code, shared tokens, no visible duplication |
| 7–8   | Minor duplication, most values tokenized |
| 5–6   | Noticeable repetition, some hardcoded values |
| 3–4   | Significant duplication, copy-paste patterns |
| 0–2   | Massive redundancy, same styles repeated everywhere |

### 4. Accessibility (0–10)

What to evaluate:
- Are `:focus-visible` styles present on interactive elements?
- Is `outline: none` used without a replacement?
- Is `prefers-reduced-motion` respected?
- Is `prefers-contrast` handled?
- Is `forced-colors` considered?
- Are touch targets at least 44x44px?
- Do text colors meet contrast ratios (4.5:1 normal, 3:1 large)?
- Is color used as the sole indicator anywhere?

| Score | Meaning |
|-------|---------|
| 9–10  | Full focus styles, motion/contrast/forced-colors handled, good targets |
| 7–8   | Focus styles present, reduced-motion handled, minor gaps |
| 5–6   | Basic focus styles, no motion or contrast queries |
| 3–4   | Missing focus styles, `outline: none` present |
| 0–2   | No accessibility considerations at all |

### 5. Performance (0–10)

What to evaluate:
- Are layout properties (`width`, `height`, `top`, `left`, `margin`, `padding`) animated?
- Is `will-change` applied globally or on too many elements?
- Is `contain` or `content-visibility` used for large lists or off-screen content?
- Are there expensive selectors (universal with deep combinators)?
- Is `@import` used in CSS files (blocks parallel loading)?
- Are animations composited (only `transform`, `opacity`)?

| Score | Meaning |
|-------|---------|
| 9–10  | Composited animations only, containment used, no `@import`, efficient selectors |
| 7–8   | Mostly composited, minor non-composited transitions |
| 5–6   | Some layout animations, no containment |
| 3–4   | Frequent layout animations, `will-change` overuse |
| 0–2   | Layout thrashing, `@import` chains, expensive selectors everywhere |

### 6. Modernity (0–10)

What to evaluate:
- CSS nesting vs preprocessor nesting or flat repetition?
- `oklch()`/`oklab()` vs hex/rgb/hsl?
- `light-dark()` vs manual dark mode classes?
- Container queries vs media queries for components?
- Logical properties vs physical (`margin-inline` vs `margin-left`)?
- `clamp()` for fluid values vs fixed breakpoints?
- `gap` vs margin hacks for spacing?
- Modern selectors (`:has()`, `:is()`, `:where()`) vs workarounds?
- Vendor prefixes still present that are no longer needed?

| Score | Meaning |
|-------|---------|
| 9–10  | Native nesting, oklch, container queries, logical properties, clamp |
| 7–8   | Most modern features adopted, minor legacy holdovers |
| 5–6   | Mix of modern and legacy patterns |
| 3–4   | Mostly legacy with a few modern features |
| 0–2   | Legacy only — floats, preprocessors, hex colors, px everywhere |

## Anti-Pattern Flags

Flag every instance of these. Reference [anti-patterns.md](../css-expert/references/anti-patterns.md) for the full catalog:

- `float` used for layout
- `!important` (note each occurrence)
- ID selectors for styling
- `outline: none` or `outline: 0` without replacement
- Layout property animations (`width`, `height`, `top`, `left`, `margin`, `padding`)
- `@import` in CSS
- Hardcoded colors (hex/rgb not in custom properties)
- Magic numbers (unexplained pixel values)
- Missing `prefers-reduced-motion`
- Nesting deeper than 3 levels
- `px` in media queries
- Vendor prefixes that are unnecessary per [browser-compat.md](../css-expert/references/browser-compat.md)
- Generic class names without scoping (`.container`, `.wrapper`)
- AI slop tells (generic purple gradients, glassmorphism everywhere, etc.)

## Report Template

Output the report in exactly this format:

```markdown
# CSS Audit Report

## Overall Score: X.X / 10

| Dimension     | Score | Summary |
|---------------|-------|---------|
| Architecture  | X/10  | [one-line summary] |
| Specificity   | X/10  | [one-line summary] |
| Redundancy    | X/10  | [one-line summary] |
| Accessibility | X/10  | [one-line summary] |
| Performance   | X/10  | [one-line summary] |
| Modernity     | X/10  | [one-line summary] |

## Findings

### Critical

- **[Issue]** — `file:line` — [explanation + code snippet]

### Warnings

- **[Issue]** — `file:line` — [explanation + code snippet]

### Notes

- **[Issue]** — `file:line` — [explanation]

## Anti-Patterns Detected

| Pattern | Count | Locations |
|---------|-------|-----------|
| [name]  | N     | file:line, file:line |

## Prioritized Fix Plan

| Priority | Fix | Impact | Effort | Dimensions Affected |
|----------|-----|--------|--------|---------------------|
| 1        | [what to do] | [high/med/low] | [high/med/low] | [which scores improve] |
| 2        | ... | ... | ... | ... |
```

## Rules

- **Never modify files.** This skill is report-only.
- The overall score is the average of the 6 dimension scores, rounded to one decimal.
- If you can't assess a dimension (e.g., no animations exist), score it N/A and exclude from the average.
- Always show code snippets for critical findings.
- Limit the fix plan to the top 10 highest-impact items.
- If the user provides HTML/JSX alongside CSS, cross-reference for unused selectors.
