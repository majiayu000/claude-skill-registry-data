---
name: figure-review-redteam
description: "Use as the last gate before a figure, KPI panel or report section is sent: an adversarial review that asks how the figure could mislead a hurried or hostile reader, re-plots the same data under alternative honest framings to see if the conclusion flips, inspects the rendered image rather than the spec, and returns a severity-ranked fix list with a ship / ship-with-caveats / revise verdict. Use when reviewing another agent's or person's chart too."
license: CC-BY-4.0
---

# Figure review: red team

Review as the reader most motivated to find a flaw: a sceptical executive, a
competitor, a reviewer, a journalist. The goal is not to approve the figure;
it is to find what is wrong before they do.

## Procedure

1. **Restate the claim** the figure makes, in one sentence with a number. If
   you cannot, that is finding #1 (S3).
2. **Look at the rendered output**, at final size, before reading the spec or
   code. Note what a five-second reader would conclude. Compare that with the
   intended claim.
3. **Run `when-numbers-lie-audit`** (comparison, population, encoding).
4. **Re-plot under alternative honest framings** (quickly, not for
   publication) and see whether the conclusion survives:
   - window shifted one period earlier/later; same period last year
   - per-unit instead of totals (per order, per staff-hour), or the reverse
   - zero baseline vs fitted range (for lines)
   - segmented by the obvious split (channel, region, seed)
   - counts instead of percentages
   If any honest framing reverses or erases the claim, the claim is not
   robust: S1 or S3 depending on how it is worded.
5. **Inspect the mechanics** on the image: clipped labels or data, overlapping
   text, legend covering data, missing series, unreadable ticks, forecast
   indistinguishable from observed, gaps invisible, colours colliding,
   units missing.
6. **Check text against figure**: title, caption, alt text and narrative
   numbers match the data and each other (`headline-and-deck`).
7. **Check the claim's standing**: is it a figure the data can support at all
   (`figure-is-a-claim`)? Is uncertainty labelled
   (`uncertainty-display`)?
8. **Write the fix list and verdict.**

## Severity

| Level | Meaning | Example |
|---|---|---|
| **S1** | States something untrue | €0 tile for a failed sync; "conversion fell" when every segment rose and the title implies close rates fell |
| **S2** | Shows a value or precision the evidence does not contain | interval with no level; forecast drawn as data; "record" without full history |
| **S3** | True numbers, framed to mislead | truncated bars; partial week compared with full; cherry-picked window |
| **S4** | Presentation only; no decision would change | tick density; legend order; caption wording |

Verdict: **ship** (S4 only), **ship with caveats** (S3 items fixed by a stated
caveat the reader will see), **revise** (any S1/S2, or S3 that a caveat
cannot fix).

## Output

```markdown
## Red-team review: <figure id / title>
Claim as read in 5 s: …
Intended claim: …
Verdict: ship | ship with caveats | revise

| # | Sev | Finding | Evidence | Fix |
|---|---|---|---|---|
| 1 | S3 | Bars start at 40% | y-limits [40, 46] | set limits [0, null] or use a dot plot |
| 2 | S2 | Band unlabelled | caption silent | name kind, level, n, method |

Alternative framings tried: window ±1 week (claim holds); by channel (claim reverses, see #3).
```

## ieeVisualizer hooks for the review

- Read `RenderResult.warnings` (or the manifest's per-variant warnings):
  `null_values_omitted`, `colour_cycle_wrapped`, `category_labels_thinned`,
  `forecast_style_overridden`, `limits_ignored`, `datetime_displayed_in_utc`
  each point at a likely finding.
- `validate(spec)` issues are JSON pointers; fixes go back as
  `apply_patch` operations, which keeps the review diff small and auditable.
- `build_figure(spec)` gives the drawn artists, so you can compare what was
  drawn with the dataset values programmatically.
- Not automated: the five-second read, alternative framings and text–figure
  consistency. They are the point of this skill.

## Checklist

- [ ] Claim restated in one sentence with a number.
- [ ] Rendered image inspected at final size before the spec.
- [ ] `when-numbers-lie-audit` run.
- [ ] At least two alternative honest framings tried; outcome recorded.
- [ ] Mechanical issues checked on the image.
- [ ] Title, caption, alt text and narrative numbers match the data.
- [ ] Fix list with severities and a verdict delivered.

Adapted in part from Anthropic's `validate-data` skill (Apache-2.0), whose
three-level confidence assessment is reshaped here into the verdict; changed:
rewritten as an adversarial procedure with alternative framings. Sources and
licences: `SOURCES.md`.
