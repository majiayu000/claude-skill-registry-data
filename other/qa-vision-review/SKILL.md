---
name: qa-vision-review
section: visual
description: "AI vision review of screenshots. Catches visual anomalies DOM probes cannot see — cropped UI, broken icons, misaligned elements, modal positioning errors, color-contrast issues, layout breakage, stuck skeletons, and mobile-render bugs. Uses Sonnet vision."
model: sonnet
applyOn: all
needsSetup: false
viewportSensitive: true
interactive: false
---

# qa-vision-review

## Overview

This is the only skill in Argus that consumes images instead of DOM. Every other detector queries the rendered DOM via `browser_evaluate`. This skill takes the screenshots produced during Step 5.4 (h) and hands them to a Sonnet sub-agent with vision enabled. The sub-agent looks at what the page actually looks like and flags visual bugs that no DOM probe can see.

The skill is invoked from orchestrator Step 6 after all per-cell execution is complete.

---

## What it checks

Things DOM probes structurally cannot detect, but a human-or-vision-model sees instantly:

| Issue type | Severity | What it catches |
|---|---|---|
| `croppedElement` | high | Button text, headings, or content visibly cut off (e.g. "Save Cha…" instead of "Save Changes") |
| `brokenIcon` | high | Icon shows as broken-image placeholder, empty box, or "X" — including missing webfont glyphs |
| `misalignedElement` | medium | Form labels visibly off-axis from inputs, columns drifting, vertical center broken |
| `modalPositionWrong` | high | Modal/dialog appears in wrong location — off-screen, partially hidden, or overlapping wrong region |
| `dropdownClipped` | high | Open dropdown extends past the visible viewport boundary |
| `zIndexStackingError` | high | Element visibly behind another that should be on top (modal behind backdrop, tooltip behind chrome) |
| `colorContrastIssue` | medium | Visibly low-contrast text — barely readable against background even at normal viewing |
| `visualHierarchyBroken` | medium | H1 visually smaller than H2; primary CTA visually less prominent than secondary action |
| `excessiveWhitespace` | low | Huge empty regions taking >40% of the viewport without purpose |
| `imageDistortion` | medium | Stretched, pixelated, or improperly scaled image |
| `loadingSkeletonStuck` | high | Skeleton placeholder or shimmer still visible after the page should have loaded |
| `blankRegion` | medium | Large content region rendered empty — possible failed fetch or hidden content |
| `mobileTextOversized` | medium | Text visibly oversized for the mobile viewport — single word taking multiple lines unnecessarily |
| `overlappingContainers` | high | Two containers visibly overlapping when they should be stacked or adjacent |
| `cutoffButtonLabel` | high | Button text exceeds its container and is being clipped |
| `tooltipPositionWrong` | low | Tooltip pointer not pointing at its trigger, or tooltip rendered off-screen |
| `formFieldCrowded` | medium | Form inputs visually packed too tightly to be usable |
| `inconsistentSpacing` | low | Visible inconsistency in card grid gaps, list separators, or button rows |
| `brokenVisualState` | medium | Hover/focus/active state visible when it shouldn't be, or missing when it should |
| `brandElementBroken` | high | Logo missing, distorted, or rendered as text fallback |
| `emptyHeaderOrFooter` | low | Header or footer rendered empty when content was expected |

Severity is set by the sub-agent based on user impact, not just visual severity.

---

## Self-skip conditions

Self-skip silently (no error, no finding) if any of these are true:

1. `customize.toml -> vision_review = false`
2. CLI flag `--no-vision` was passed
3. The cell's `route` is not in `customize.toml -> vision.critical_routes` (when `critical_routes` is non-empty)
4. The orchestrator has already reviewed `vision.max_cells` cells this run
5. No screenshots exist for this cell in `.tmp/{runId}/screenshots/{cell.id}-*`

Log a single line summary per skipped cell: `[skip vision] {cell.id} {reason}`.

---

## Orchestrator flow

The orchestrator runs this skill ONCE at Step 6, after all per-cell execution has completed. It does NOT run per-cell during Step 5.

```
Step 6 vision review (pseudo-code):

  1. Read customize.toml -> [vision] section:
       enabled        = vision_review (top-level, default true)
       criticalRoutes = vision.critical_routes (default [])
       maxCells       = vision.max_cells (default 6)
       model          = models.vision_model (default "sonnet")

  2. If enabled = false OR --no-vision passed:
       Log: "⏭️  Vision review disabled — skipping"
       Return.

  3. Build the cell list to review:
       For each cell in audit-plan.json:
         a. If criticalRoutes is non-empty AND cell.route not in criticalRoutes → skip
         b. Find screenshots: glob .tmp/{runId}/screenshots/{cell.id}-*.png
         c. Prefer the *-annotated.png; fall back to the clean *.png
         d. If no screenshots → skip
       Sort the resulting list by phase (smoke → regression → full) and priority.
       Truncate to maxCells.

  4. For each cell in the truncated list:
       a. Read the chosen screenshot path
       b. Read up to 2 representative screenshots per cell (one viewport, max 2)
       c. Dispatch a Sonnet sub-agent (see Sub-agent prompt below)
       d. Parse the JSON array from the response
       e. For each finding, append to .tmp/{runId}/issues/{cell.id}.jsonl
          using the schema in qa-argus Step 5.4 (j)
       f. Increment visionFindingsCount in run-summary.json

  5. If sub-agent dispatch errors (model error, timeout, etc.):
       Log warning: "Vision review error on {cell.id}: {message}"
       Continue with the next cell. NEVER block the audit on a single vision failure.

  6. After the loop, write to run-summary.json:
       {
         "visionEnabled":        true,
         "visionCellsReviewed":  N,
         "visionFindingsTotal":  M,
         "visionFindingsByType": { croppedElement: 2, brokenIcon: 1, ... }
       }
```

---

## Sub-agent prompt

The orchestrator builds and dispatches this prompt via the Agent tool with vision capability:

```
Agent({
  subagent_type: "general-purpose",
  model:         "sonnet",
  description:   "Argus vision review of {cell.id}",
  prompt: `
You are reviewing a screenshot of a web page rendered during an automated QA audit.

Cell context:
  Route:    {cell.route}
  Viewport: {cell.viewport.name} ({cell.viewport.width}x{cell.viewport.height})
  Browser:  {cell.browser}
  App URL:  {baseUrl}

The screenshot is attached. Look at it carefully and identify ONLY VISUAL anomalies — bugs that are obvious from looking at the rendered page but that an automated DOM query would miss.

What to look for:
  croppedElement         — button/heading/content visibly cut off
  brokenIcon             — a broken-image placeholder (failed <img>), a literal "tofu" □ box, or an "X"/empty square where an icon CLEARLY failed to load. This does NOT include caret / chevron / triangle glyphs (^ v < > ‹ › ▲ ▼ ⌃ ⌄ ∧ ∨) used as sort, expand/collapse, dropdown, or pagination indicators — those are valid, intentional UI controls, never a broken icon.
  misalignedElement      — form labels off-axis from inputs, columns drifting, vertical center broken
  modalPositionWrong     — modal off-screen, partially hidden, overlapping wrong region
  dropdownClipped        — open dropdown extending past viewport edge
  zIndexStackingError    — element visibly behind another that should be on top
  colorContrastIssue     — barely-readable text against its background
  visualHierarchyBroken  — H1 smaller than H2; primary CTA less prominent than secondary
  excessiveWhitespace    — huge empty region taking > 40% of viewport without purpose
  imageDistortion        — stretched, pixelated, badly scaled image
  loadingSkeletonStuck   — skeleton or shimmer still visible when page should be loaded
  blankRegion            — large content area rendered empty
  mobileTextOversized    — text visibly too large for mobile viewport
  overlappingContainers  — two containers visibly overlapping when they should be stacked
  cutoffButtonLabel      — button text exceeds container and is clipped
  tooltipPositionWrong   — tooltip pointer not pointing at its trigger
  formFieldCrowded       — inputs packed too tight to be usable
  inconsistentSpacing    — visible inconsistency in card/list/button gaps
  brokenVisualState      — hover/focus visible when it shouldn't be, or missing when it should
  brandElementBroken     — logo missing, distorted, or text-fallback only
  emptyHeaderOrFooter    — header or footer rendered empty when content expected

Strict rules:
  - Only flag issues that are CLEARLY visible. Do NOT speculate.
  - DO NOT flag minor design choices, brand-specific styling, or stylistic preferences.
  - DO NOT flag things that are arguably intentional (e.g. dark backgrounds, white space as design).
  - DO NOT re-detect DOM-level bugs (touch target size, missing alt, missing h1) — those are handled by other detectors.
  - Sort indicators from component libraries are STANDARD, intentional UI — never a bug. This includes MUI `TableSortLabel` (a small up/down arrow ▲/▼ SVG), Ant Design, Bootstrap, PrimeNG, AG Grid sort carets/chevrons (^ v ‹ › ⌃ ⌄ ∧ ∨), etc. NEVER flag any of these as broken, missing, wrong, low-quality, or "should be an arrow" — the glyph shape (caret vs arrow) is a stylistic preference, which rule 2 already forbids flagging.
  - CRITICAL for sort columns: MUI and most table libraries show the sort indicator ONLY on the currently-active (and sometimes hovered) column — inactive columns intentionally have NO visible arrow. A static screenshot captures no hover state, so most columns will correctly show no indicator. Do NOT flag a column as "missing sort indicator/arrow" — the absence is by design, not a bug. Sort affordance is a DOM/interaction concern handled by qa-test-data-controls, not vision.
  - Limit to 10 findings total. Pick the most impactful.
  - Output ONLY a valid JSON array. No prose, no markdown, no preamble.

Output schema (one object per finding):
  {
    "issueType":       <one of the categories listed above>,
    "severity":        "critical" | "high" | "medium" | "low",
    "description":     "<plain-English description of the visual issue, max 160 chars>",
    "regionHint":      "<approximate location: top-left | top-center | top-right | middle-left | middle | middle-right | bottom-left | bottom-center | bottom-right>",
    "selectorGuess":   "<best-guess CSS selector if obvious from text content, otherwise null>"
  }

If nothing is visually wrong, return [].
`,
  attachments: [<path to chosen screenshot>]
})
```

The orchestrator passes the screenshot file as an attachment using the Agent tool's image-input capability.

---

## Finding-to-issue mapping

For each finding returned by the sub-agent, build the standard Argus issue record:

```
{
  runId:                  <currentRunId>,
  cellId:                 <cell.id>,
  skill:                  "qa-vision-review",
  issueType:              <finding.issueType>,
  severity:               <finding.severity>,
  route:                  <cell.route>,
  viewport:               <cell.viewport.name>,
  viewportClass:          <cell.viewportClass>,
  browser:                <cell.browser>,
  selector:               <finding.selectorGuess || null>,
  description:            <finding.description>,
  bbox:                   null,                        // vision findings do not have an exact bbox
  regionHint:             <finding.regionHint>,        // extra field
  screenshotPath:         <path to the reviewed screenshot>,
  annotatedScreenshotPath: <same path if it was already annotated, else null>
}
```

Note: vision findings do NOT receive a new annotation pass — the screenshot the sub-agent reviewed IS the evidence attached to the bug. The `regionHint` field gives the QA reviewer a quick "where to look."

Append each finding to `.tmp/{runId}/issues/{cell.id}.jsonl` immediately (streaming write, same as Step 5.4 j).

---

## Cost control

The `[vision]` block in `customize.toml` controls cost:

```toml
[vision]
critical_routes = ["/", "/login", "/checkout", "/dashboard"]
max_cells = 6
```

| Config | Behavior |
|---|---|
| `critical_routes = []` (empty) | Review every cell up to `max_cells` |
| `critical_routes = ["/", "/login"]` | Review only cells whose route exactly matches; ignore others regardless of `max_cells` |
| `max_cells = 6` (default) | Hard ceiling — after 6 cells reviewed, stop emitting vision findings for the rest of the run |
| `vision_review = false` (top level) | Skill silently no-ops |

Per-cell cost estimate (Sonnet vision):

| Input | Tokens | Cost @ Sonnet 4.6 |
|---|---|---|
| Screenshot (1440×900 PNG, ~1500 tokens after encoding) | 1500 | $0.0045 |
| Prompt + cell context | 700 | $0.0021 |
| Output (JSON findings, ~10 items × 80 tokens) | 800 | $0.012 |
| **Total per cell** | **~3000** | **~$0.019** |

For the default `max_cells = 6`: **~$0.11 per audit added.** For 12-cell vision on every route: **~$0.23 added.**

---

## Hard rules (enforce strictly)

1. **NEVER call `browser_evaluate` or any MCP tool.** This skill works only from screenshot files on disk. The browser may have been closed by the time Step 6 runs.

2. **NEVER re-detect DOM-level bugs.** If the vision model wants to flag "touch target too small," reject and skip — `qa-detect-touch` already covers it. Vision is for what DOM probes cannot see.

3. **NEVER block the audit on a vision failure.** Sub-agent timeout, model error, parse failure — all log and continue.

4. **NEVER ship a finding without a screenshot path.** The reviewed screenshot path goes on every emitted finding so the bug-filer has evidence to attach.

5. **NEVER exceed `max_cells`.** Track the running count in memory across the loop; stop emitting once the cap is hit, even if more cells qualify.

6. **NEVER mutate the screenshot file.** Read-only. The annotated screenshot was produced in Step 5.4 (h); this skill just consumes it.

---

## Self-skip log messages

For consistent logs the orchestrator should emit one of these per skipped cell:

| Reason | Message |
|---|---|
| `vision_review = false` | `⏭️  Vision review disabled (set vision_review = true to enable)` |
| `--no-vision` flag | `⏭️  Vision review skipped (--no-vision flag passed)` |
| Route not in `critical_routes` | `⏭️  Vision skipped {cell.id} — route {cell.route} not in vision.critical_routes` |
| `max_cells` hit | `⏭️  Vision cap reached (max_cells={N}) — skipping remaining cells` |
| No screenshots for cell | `⏭️  Vision skipped {cell.id} — no screenshots found in .tmp/{runId}/screenshots/` |

---

## Output summary

After Step 6 completes, append the following to `.tmp/{runId}/run-summary.json`:

```json
{
  "visionEnabled":        true,
  "visionCellsReviewed":  6,
  "visionFindingsTotal":  14,
  "visionFindingsByType": {
    "croppedElement": 3,
    "brokenIcon": 1,
    "modalPositionWrong": 2,
    "colorContrastIssue": 4,
    "dropdownClipped": 1,
    "loadingSkeletonStuck": 1,
    "imageDistortion": 2
  },
  "visionCostEstimateUSD": 0.114
}
```

The bug filer (Step 7) reads these findings from the cell JSONLs just like any other skill's findings — no special-casing required.

---

## Failure modes and recovery

| Failure | Behavior |
|---|---|
| Sub-agent times out (> 30 s) | Log warning, continue to next cell. Do not retry — vision is not critical. |
| Sub-agent returns non-JSON | Log warning with the first 200 chars of response, continue to next cell. |
| Sub-agent returns JSON but with unknown `issueType` | Map to closest defined category; if none → emit as `visualAnomalyOther` with severity `low`. |
| Screenshot file missing or unreadable | Log warning, skip cell, continue. |
| `customize.toml -> [vision]` section missing | Use defaults (`critical_routes = []`, `max_cells = 6`). |
| `vision_model` not set in `[models]` | Default to "sonnet". |
| All cells skipped (empty review list) | Log: `⏭️  Vision review: 0 cells qualified — skipping step`. Do not emit a summary. |

---

## Notes

- This skill ships with no external dependencies. The only requirement is that the orchestrator's Agent tool supports image inputs (Sonnet 4.6 does).
- The skill does not modify any screenshots. Annotations (red boxes) are produced by the MCP-driven pipeline (`scripts/annotate-cell-prepare.cjs` → `browser_navigate` + `browser_take_screenshot` → `scripts/annotate-cell-finalize.cjs`) in Step 5.4 (h.3), not here.
- If you want to add a new visual issue type, add it to both the table above and the sub-agent prompt's "What to look for" list. The orchestrator's mapping is pure passthrough — no code changes needed.
- The `regionHint` field is the closest thing this skill can provide to a bounding box. The bug filer (Step 7) can use it to render a textual "see top-right of the screenshot" hint in the ADO ticket body.
