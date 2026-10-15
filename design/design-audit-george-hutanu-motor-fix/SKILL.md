---
name: "design-audit"
description: "Audit an existing UI against Apple's design rules — type scale, spacing, hierarchy, contrast, motion, density — and return findings ranked by impact, each with file:line and an exact replacement value. Read-only until the user names findings to fix; then fixes them three at a time and re-verifies. Measures contrast rather than recalling it."
argument-hint: "What to audit: a path, a component, or a URL. Add 'fix 1-3' to run the fix loop."
compatibility: "Requires the apple-design-skill skill (.claude/skills/apple-design-skill) and Node 18+ for the two helper scripts"
metadata:
  author: "speckit-demo"
  source: "adapted from The Apple Design Audit"
user-invocable: true
disable-model-invocation: false
---

## User Input

```text
$ARGUMENTS
```

Treat the input as the audit target. Empty input: ask what to audit and stop —
do not guess a target or audit the whole repository.

Input containing `fix <range>`: skip to **Phase 2** for those findings from the
audit already in this conversation. No audit in the conversation yet? Say so and
run Phase 1 first.

## Ground rules

1. **Invoke `apple-design-skill` first, every run.** Its `references/` are the
   source of truth for guidance. The files that carry this audit:
   `foundations/typography.md`, `foundations/layout.md`, `foundations/color.md`,
   `foundations/accessibility.md`, `foundations/motion.md`,
   `foundations/dark-mode.md`. Grep `references/topic-index.md` to locate others.
2. **Evidence rule.** Every value you state comes from a file you read this
   session or from a script's output, cited as `path:line`. A value you cannot
   cite does not go in the report — it goes in **Could not verify**.
3. **Compute, never recall.** Contrast ratios come from `contrast.mjs`. Value
   inventories come from `scan.mjs`. Recalled ratios are wrong often enough to
   discredit the whole report.
4. **Their brand, not Apple's.** Apply structural rules — scale, spacing,
   hierarchy, contrast, motion, density. Keep existing hues, fonts, voice,
   and product identity. Output that looks like apple.com is a failed audit.
5. **Phase 1 changes no code.** None. Not the obvious one-liner either.
6. The HIG mirror covers Apple platforms. On web or non-Apple UI the structural
   rules still hold; mark any number that is a web translation rather than
   literal HIG text, and use WCAG for contrast.

## Phase 0 — scope the target

1. Resolve the target to a concrete file set. A path scans as-is; a component
   name resolves to its file plus its stylesheet; a URL needs computed styles
   (`mcp__chrome-devtools__*`: navigate, then `evaluate_script` over
   `getComputedStyle` for the elements in view) — a fetched HTML source is not
   enough, since the real values live in the cascade.
2. **Audit tokens, not call sites.** If the target has a token layer — Tailwind
   theme, CSS custom properties, a `tokens.ts`, a theme provider — read that
   file first and audit it. Fixing a token fixes every call site; fixing call
   sites one by one fights the system. `scan.mjs` deliberately ignores Tailwind's
   default scale (`p-4`, `text-sm`) for this reason.
3. Note which themes exist (light, dark, high-contrast). Contrast is measured in
   **each** theme; a pair that passes on white often fails on the dark ground.
4. Large target? Narrow to the two or three screens that matter most and say
   which ones you took. A thorough audit of the landing page beats a thin sweep
   of forty files.

## Phase 1 — audit

Run both scripts first. They locate and count; they do not judge.

```bash
node .claude/skills/design-audit/scripts/scan.mjs <paths> --samples 6
# then, for every text-on-background pair the scan turned up, in every theme:
node .claude/skills/design-audit/scripts/contrast.mjs "#7a7a7a" "#ffffff"
printf '#7a7a7a|#fff|body on card\n' | \
  node .claude/skills/design-audit/scripts/contrast.mjs --stdin --fail-under 4.5
```

`contrast.mjs` takes hex, `rgb()`/`rgba()`, `hsl()`/`hsla()`, and bare
`0 0% 100%` HSL tokens; a translucent foreground is composited over its
background before measuring. Use the `|` form when a color contains spaces.

Then read the flagged lines and judge these six areas, in this order.

**1. Type scale.** Every size in use, with counts. A scale is 4 to 6 steps with
a consistent ratio (≈1.2 to 1.33 between adjacent steps); more than that is
accumulation, not design. Check the step between a headline and its
sub-headline is at least ~1.4x — closer than that and the eye has no entry
point. Check line height too: roughly 1.1 to 1.25 for display sizes, 1.4 to 1.6
for body. *Not a finding:* sizes that come from a third-party embed you do not
control, or one deliberate outlier with a stated reason.

**2. Spacing.** Establish the base unit (4px or 8px) from what dominates, then
list what breaks it and where. *Not a finding:* hairlines and borders (1px),
focus rings (2px), optical centering nudges, values a vendor component ships.
Two section paddings that differ by 4px with no reason **is** a finding.

**3. Hierarchy.** Per screen: name the one thing the eye should land on first.
Then say whether it actually wins, and by what mechanism it loses — usually
competing sizes, a same-weight neighbor, or equal spacing above and below every
element. This is the area scripts cannot see, and usually the highest-impact one.

**4. Contrast.** Every text-on-background pair, in every theme, measured. Body
text needs 4.5:1; large text (≥24px regular or ≥18.66px bold) needs 3:1; UI
component boundaries and focus indicators need 3:1. Include placeholder text,
disabled states, and text over images or gradients — those fail most often.
State the measured ratio, never an estimate.

**5. Motion.** Every transition with its duration and easing. Flag anything over
300ms for a UI state change, and `linear` on anything that is not an opacity
fade, a progress indicator, or a looping spinner. `transition: all` is a defect
regardless of duration — it animates properties you never intended and costs
layout. Check `prefers-reduced-motion` is honored.

**6. Density.** Where the layout crams and where it wastes. Look at tap targets
(44×44pt on iOS, 60×60pt on visionOS — `components/menus-and-actions/buttons.md`;
the per-platform table is `foundations/accessibility.md`), line
length (roughly 45 to 75 characters for body copy), and whether related things
sit closer together than unrelated ones.

### Finding format

```
<n>. <AREA> — <path:line>
    Problem:      <one sentence>
    Current:      <exact value>
    Replace with: <exact value>
    Why:          <references/... path, WCAG criterion, or "web translation">
```

### Ranking

Rank the whole list by how much each fix changes how expensive the product
feels, using these tiers — then number the findings in that order:

- **Tier 1 — changes the feel.** Hierarchy on the first screen the user sees.
  Body-text contrast failures. Collapsing seven type sizes to four. The spacing
  rhythm of the primary layout.
- **Tier 2 — visible on inspection.** Secondary screens, hover and press motion,
  density, inconsistent radii or borders.
- **Tier 3 — nits.** Single-instance off-grid values, dead CSS, anything a
  reader would not notice in a side-by-side.

The tiers are the rule; ordering *within* a tier is a judgement made over a
dozen findings at once, which is where a ranked report quietly becomes an
arbitrary one. Write the findings to a scratch JSON array and order them:
`node .claude/scripts/jev.mjs rank <file>.json --about "how much more expensive the product feels once this is fixed"`.
Keep the tiers — a Tier 3 nit never outranks a Tier 1 finding whatever it
scores. If the lane is unavailable, order by eye and say so.

Cap the report at about twelve findings. Sixty nits is noise, and the ranking is
what makes the report usable. Close with: the top three, one line on why they
are the top three, and a **Could not verify** list (anything you could not read,
compute, or reach) — state that explicitly rather than leaving a silent gap.

## Phase 2 — fix loop

Fix only the findings the user named, about three at a time.

1. Apply the batch.
2. Show a before/after of the exact lines changed. Nothing else — no drive-by
   refactors, no reformatting, no "while I was in there".
3. Prove the scope: `git diff --stat` for the batch. A file in that list you did
   not mean to touch is a mistake to undo, not to explain.
4. Re-verify mechanically — re-run `scan.mjs` on the changed files, and
   `contrast.mjs` on any pair you touched — then state per finding whether it
   now passes.
5. Stop. Wait for the next batch. Do not roll on unasked.

A fix that needs a token change touches the token, then spot-checks the call
sites that consumed it.

## Failure modes

- **Generic advice, no numbers.** The HIG skill did not fire. Invoke
  `apple-design-skill` explicitly and re-run — a finding without a number is
  not a finding.
- **Output looks like Apple, not like the product.** Surface style got copied
  instead of rules applied. Revert, keep the brand palette and fonts, apply
  structure only.
- **Nothing feels different after the fixes.** Tier 3 findings got picked. Go
  back to the top three.
- **The audit rewrote files.** Phase 1 is read-only; that is the whole contract.
  Revert and re-run.
- **Findings multiply on every screen.** They are call sites of one token
  defect. Go up a level and audit the token layer.

## Boundaries

This skill judges design intent — look, rhythm, hierarchy, contrast, motion. It
does not judge framework API usage, and the HIG mirror never contains API names:
verify SwiftUI/UIKit/CSS specifics against current framework documentation.
It is not a substitute for testing with real assistive technology; a passing
contrast ratio is a floor, not an accessibility review.
