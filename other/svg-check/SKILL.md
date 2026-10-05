---
name: svg-check
description: Apply when editing, generating, or reviewing any SVG diagram. Pixel-perfect Playwright bbox-check is the acceptance test — eyeballing is not sufficient. Run on every SVG before declaring done.
license: MIT
version: 1.0.0
tokens_target: 1800
triggers:
  - svg edit
  - svg review
  - diagram
  - pixel review
  - svg overflow
loads_after: []
supersedes: []
---

# Sub-Skill: SVG Check

**Purpose.** Catch text-overflow and foreign-rect-intersection bugs in SVG diagrams *before* commit. LLM eyeball review at 4× zoom misses these bug classes consistently — measurement is the only reliable test.

The acceptance test is the script output. Not your visual judgment.

---

## When to apply

Apply this skill whenever:

- you are editing an existing SVG (`*.svg` in any docs/diagrams folder),
- you are producing a new SVG from scratch,
- a designer agent reports an SVG as "clean" — verify with the script,
- you are reviewing a PR that touches `*.svg`.

---

## The two bug classes the script catches

1. **OVERFLOW (own-container)**: a `<text>` whose rendered bbox extends past the bounds of its containing `<rect>` (in the same `<g>`). Caught by `getBBox()` measurement, tolerance 2 px.

2. **FOREIGN-RECT INTERSECT**: a `<text>` whose viewport bbox intersects a `<rect>` that is *not* an ancestor of the text — i.e. a tagline ascender that touches a structural box above/below it. Caught by `getBoundingClientRect()` intersection, tolerance 2 px.

Both classes filter false-positives: rects smaller than 40 × 18 (legend swatches) are not treated as containers; texts that start more than 5 px outside a rect's horizontal range are not treated as contained.

---

## How to run

The script lives next to this file: [`overflow-check.js`](./overflow-check.js). It needs Playwright installed once per machine.

### One-time setup

```bash
# From the skill folder
cd skills/svg-check
bash setup.sh
```

Or manually:

```bash
npm install playwright
npx playwright install chromium --with-deps
```

### Run on one SVG

```bash
node skills/svg-check/overflow-check.js path/to/diagram.svg
```

### Run on all SVGs in a folder

```bash
for svg in path/to/*.svg; do
  out=$(node skills/svg-check/overflow-check.js "$svg" 2>&1)
  if echo "$out" | grep -q "FOUND"; then
    echo "FAIL: $svg"; echo "$out" | grep -E "FOUND|  \[|  \""
  fi
done
```

The script exits non-zero when issues are found — suitable for use as a pre-commit gate or CI step.

---

## Acceptance criteria

The script output **must** contain both of these lines, verbatim, for every SVG in scope:

```
OVERFLOW: CLEAN — 0 text overflows past their containing rect
FOREIGN-RECT INTERSECT: CLEAN — 0 text-vs-foreign-rect intersections
```

Anything else means **not done**. Fix the SVG (shorten text, widen rect, move element, change font-size) and re-run until both lines are CLEAN.

In addition, after the script is CLEAN, render a Playwright screenshot in light + dark mode and visually cross-check for bug classes the script does not cover (see § *Limits* below).

---

## How to fix common overflow patterns

| Pattern | Fix |
|---|---|
| Mono-tag text wider than its 200 px box | Move trailing content to a `mono-dim` line below, or drop the suffix entirely. Match the sibling-box pattern. |
| Tagline ascenders touch the rect above | Extend the SVG viewBox height (`500 → 520`) and move the tagline down. Other elements stay put. |
| Two-line label tight in a folder glyph | Move from `y=22/33` to `y=21/34` (13 px line-height instead of 11 px). |
| Annotation text overflowing a chip | Either widen the chip rect or shorten the annotation. Do **not** suppress the script — fix the SVG. |

---

## Examples

See [`EXAMPLES.md`](./EXAMPLES.md) for real before/after fixes with script output.

---

## Limits — what the script does NOT catch

These remain eyeball-only for now. When a missed bug class surfaces, extend the script with a new check class — do not rely on agent self-reporting.

- **Text-vs-line overlaps**: a `<text>` crossing an `<line>` arrow.
- **≥12 px clearance** between text-baseline and the nearest line below it.
- **Sibling text overlaps**: two `<text>` elements at the same coords.
- **Color contrast ratio** in dark mode.
- **Glyph render quality** at small sizes (≤ 10 px).

---

## Why this skill exists (incident history)

- **2026-05-11 #1**: a four-designer parallel review declared `architecture.svg` clean. The GEMINI CLI loader-tag overflowed its 200 px box by 42.6 px. No agent measured.
- **2026-05-11 #2**: a follow-up three-cycle eyeball review missed that the tagline ascenders intruded into the folder-strip border above. The fix was a 20 px viewBox extension; the bug was a 2 px overlap that the agents could not detect by sight.

The script was built after the second miss. It catches both bug classes in under 5 seconds.

The rule that follows from these incidents: **don't trust agent self-reports of "no issues at 4× zoom". Trust the measurement.**

---

## Required output for "done"

When reporting work on any SVG, paste the script output verbatim — both *before* the fix (showing the bug) and *after* the fix (showing CLEAN). Without that paste, the work is not done.
