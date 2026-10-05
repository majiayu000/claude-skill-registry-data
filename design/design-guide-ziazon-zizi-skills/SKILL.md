---
name: design-guide
description: >
  Use when visual/UX design judgment is needed — color palettes, typography,
  spacing/hierarchy, theme selection, and applying design best practices. Invoke
  whenever choosing colors or themes, picking status/badge colors, designing a
  screen's look, making something "look better / more professional / polished",
  white-label/partner theming, or reviewing a UI for visual quality. Aimed at a
  design-averse user who wants design decisions made well on their behalf; records
  design preferences and good-practice references over time. Scope is visual/
  aesthetic judgment ONLY — for component/state/data-access structure use the
  frontend skill; for Tabler component specifics and Vue workarounds use tabler-ui;
  for which content belongs on the screen at all, and in what order, use
  information-architecture. These often apply to one screen; this skill decides how
  it should look.
---

# Design Guide

Goal: make sound visual/UX design decisions and explain them simply, so a design-averse
user gets professional-looking results without having to drive the aesthetics.

## Workflow

1. **Read `LEARNINGS.md` beside this skill, when your copy keeps one, first** — it holds
   the user's recorded preferences and project-specific specs (e.g. a prior screen's
   filtering UX, partner theming; this install's examples: `LOCAL.md` beside this skill,
   when your copy keeps one — *Recorded specs*). A decision that contradicts a recorded
   preference is a rework, not a judgment call.
2. **Anchor to the app's existing design language.** In a Tabler app, lean on Tabler's
   palette/spacing/components (see tabler-ui) instead of inventing a parallel language —
   consistency beats novelty. For UX shape, check your design system's reference
   templates before designing from memory (this install's location: `LOCAL.md` beside
   this skill, when your copy keeps one — *Reference templates*).
3. **Choose colors with the 3-tier method.** When no brand palette is given, use the
   3-tier color system from *Refactoring UI* (Wathan & Schoger) as the default toolkit
   (this install's worked reference: `LOCAL.md` beside this skill, when your copy keeps
   one — *Color reference*): Primary (look-defining accents, the minority of pixels),
   Neutrals (tinted grey ramp, ~90% of the UI), Supporting (semantic + extra accents,
   sparingly). A hue is ~10 shades, not 3;
   tint the grey to the brand temperature; recipe = 1 primary + 1 grey + 2–4 supporting.
   Check text/background contrast (WCAG AA).
4. **Apply the standing decisions below** — they are settled user preferences, not
   options to re-litigate.
5. **When the outcome is hard to predict, render candidates — don't reason in the
   abstract.** For icon geometry, glyph fit, spacing: build each option as an SVG,
   `rsvg-convert` → PNG, `magick montage` them **next to the real existing elements**
   (e.g. sibling icons in the same badge, on the real background), then judge family-fit
   visually and let the user pick. This caught that a wide glyph never fits a square
   badge and that a half-scale car blobs at stroke-2 — obvious in render, invisible in code.
6. **Deliver a concrete recommendation** (specific colors/values), not a menu — with a
   one-line rationale. Offer a preview/sample when comparing options.
7. **Verify in BOTH light and dark mode** before showing the result, with inline
   screenshots — theme-dependent contrast failures are an established bug class here.

## Standing decisions (apply by default; recorded user preferences)

- **Status color semantics are fixed:** success = green, failed/error = red,
  partial/in-between = amber/yellow, skipped/neutral = grey. Render statuses in tables as
  colored pills/badges in a **soft/muted** tone (the opaque `bg-*-subtle` +
  `text-*-emphasis` pair; Tabler's `-lt` tints fail AA contrast, see
  [tabler-ui's layout-visuals.md](../tabler-ui/layout-visuals.md)), never loud
  full-saturation, never plain text — soft pills stay readable in dense tables.
- **Never use color alone to convey state** — pair it with text or an icon (a red pill also
  reads "Failed"), so state survives color-blindness and greyscale.
- **Semantic colors stay consistent app-wide** (success/warn/danger/info); validation
  feedback is red (`text-danger` / `.invalid-feedback`).
- **Destructive actions always confirm:** every delete/remove opens a warning-styled
  dialog with a danger-colored confirm button first — the danger must be visible before
  the click, never delete-on-click.
- **No silent failures into empty states:** a failed action must surface an error (e.g. a
  toast); a swallowed failure renders a misleading "no data" view indistinguishable from
  genuinely having no data.
- **Date vs. datetime:** show date-only for date-semantic fields (billing-period
  boundaries, from–to ranges); reserve full timestamps for true event times
  (created/updated/started/ended) — precision that carries no meaning is noise.
- **DRY look-and-feel:** the user dislikes re-styled one-off patterns — prefer one
  generic, metadata-driven component (e.g. the data table) so sorting/filtering/styling
  stay uniform everywhere.
- **Hero eyebrow/kicker hierarchy:** a kicker above a hero title must be visually smaller
  than the title and separated by vertical spacing — at the same size it competes with
  the headline and flattens the hierarchy. (Tabler values: `fs-2 fw-semibold mb-3
  text-primary` vs a 3rem `.hero-title` — see tabler-ui. Where these values were
  measured: `LOCAL.md` beside this skill, when your copy keeps one — *Hero kicker values*.)
- **Brand lead-in punctuation:** a primary-colored brand lead-in followed by a
  descriptive phrase reads as one sentence only as **"Brand: lowercase continuation"**
  ("Acme: powering your next project…"); two capitalized fragments read as a collision.
  (This install's original example: `LOCAL.md` beside this skill, when your copy keeps
  one — *Brand lead-in example*.)
- **Custom icons must match the set's design language exactly** (Tabler: 24×24 grid,
  stroke-2, real primitives) — a free-handed one-off reads as foreign next to siblings.
  For a two-concept icon, balance both parts at comparable size; a tiny corner badge
  subordinates one concept (user rejected exactly this). Build/verify details: tabler-ui
  layout-visuals.md.
- **Typography: generous, consistent sizing** — stakeholders repeatedly flag small body
  copy. Align to the app's existing type scale (Tabler marketing scale) rather than
  arbitrary px; body/section descriptions ≥ 1rem.

## Common failure modes

- **Guessing visual outcomes in code** instead of rendering candidates (step 5) — icon
  fit, glyph scale, and spacing judgments made abstractly get rejected on sight.
- **Inventing a new palette/pattern inside an app with an established language** —
  extend Tabler's tokens and existing components; novelty here reads as inconsistency.
- **Full-saturation status colors or plain-text statuses** in tables — violates the
  fixed soft-pill rule above.
- **Checking only light mode** — contrast and hardcoded-color failures surface in dark
  mode (e.g. a third-party sign-in button rendering white-on-white until wrapped in
  `color-scheme: light`; the originating ticket: `LOCAL.md` beside this skill, when your
  copy keeps one — *Dark-mode sign-in button*).
- **Offering the user a menu of options with no recommendation** — the user is
  design-averse; decide, recommend one, explain in a line.

## Before you call this done

- [ ] Read `LEARNINGS.md` (when your copy keeps one); no recorded preference contradicted.
- [ ] Consistent with the app's existing design language (and your design system's
      reference templates where UX shape was involved).
- [ ] Status/semantic colors follow the fixed mapping; contrast meets WCAG AA.
- [ ] Hard-to-predict visuals were rendered and compared, not guessed.
- [ ] Verified in BOTH light and dark mode; inline screenshots shared.
- [ ] Delivered a concrete recommendation with a one-line rationale.

## Capturing learnings (session-handoff protocol)

Accumulate design preferences and good references in `LEARNINGS.md` beside this skill,
when your copy keeps one. On
handoff / "update skills" / after design work: record palettes/themes chosen (hex values +
roles), the user's likes/dislikes (and *why* a liked product's look works — palette,
density, hierarchy, motion), and reusable best-practice notes. Dedupe/merge, tag where
project-specific. Promote settled, general rules into the "Standing decisions" list above
(leave a pointer in LEARNINGS). Read LEARNINGS before design decisions.
