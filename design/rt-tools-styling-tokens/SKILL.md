---
name: rt-tools-styling-tokens
kind: pattern
rule: rt-tools-styling
description: A pattern of the rule rt-tools-styling. Take it when a styling token is started or removed, when theme handles are edited, when the dark theme and the contrast are sorted out and when the styling layer is built. Not for narrow-screen thresholds and cascade layers.
---

# Tokens, themes and the styling layer — the ready-made order

A pattern of the rule `rt-tools-styling`. What must be true at that is the law
`docs/constitution/frontend-application.md`.

## When to use

- A styling token is started, renamed or removed.
- A theme handle is edited or a divergence of the dark theme is sorted out.
- The kit's styling layer is built.

## A token is declared, named a handle, or dead

The check is `pnpm run check:tokens-graph`. It reads the declarations and the references over all
of the second kit's styles and sorts a name into three states; the list of handles is
`tools/tokens-handles.json`, the accepted list is `tools/tokens-graph-allowlist.json`.

- **A name has no third state.** Not declared and not named a handle is a dead reference: the rule
  works, the value does not apply, and this can be seen only by eye.
- **A reference to a kit token goes without a fallback value.** A fallback hides the miss and
  survives a theme change: there is nothing to override. It stands only on a consumer's handle.
- **A handle is listed twice and matched by a machine.** The check's data and the section
  "Consumer handles" in `Theming.mdx` — no second list is started without an audit.
- **A shared name on the page root from a component's styles is a refusal.** The name of one's own
  block (`--rt-<block>-*`) passes: that is the third layer, it belongs to the component and must be
  there.
- **A name used by both kits is refused.** The styles file included later wins, and an application
  with two kits gets what neither of them counted on.
- **A preset value that must hold a fixed number takes a preset step of its own, not a shared scale
  name.** The first kit declares `--rt-radius-*` and `--rt-shadow-*` on the page root with its own
  numbers, and the coexistence file restores the second kit's values only on the preset node. A
  preset value built from those names draws the first kit's numbers outside that node — on an
  overlay pane always. Such a value takes a `--rt-mat-radius-*` or `--rt-mat-shadow-*` step.
- **The first kit's scale names are read by expanding the loop, not by a literal search.** The first
  kit declares radii, shadows and the other scales by `@each $token, $value in $<map>` with
  `--rt-<scale>-#{$token}` inside. The check expands one interpolation at the end of a name over the
  map's top-level keys; a name with two interpolations (`--rt-color-#{$hue}-#{$step}`) it does not
  read. A collision the check does not name is therefore not proof of its absence. A name the first
  kit declares that way is looked up by the map in `_tokens.scss`, not by a search over the styles.

## The dark theme answers, and a machine counts the contrast

The check is `pnpm run check:tokens-theme`. It reads three files of the second kit's styling layer,
parses the value graph once and answers with two sections: the completeness of the dark theme and
the contrast of the pairs. The list of pairs is `tools/tokens-contrast-pairs.json`, the accepted
list is `tools/tokens-theme-allowlist.json`.

- **Silence has exactly two lawful reasons: an override and a named commonality.** A colour
  assignment of the light theme is either overridden by the dark one or marked
  `/* rt-theme-shared: reason */` on its own line. The mark stands where the colour is edited and
  dies together with the line.
- **The answer and the mark are inherited along the chain of references.** An assignment referring
  to another assignment changes together with it and inherits its reason: there is no point
  duplicating the line in the dark theme. Twenty silences are closed by ten marks for exactly that.
- **What is judged is a colour declaration of the assignments layer, not a name with the prefix
  `--rt-color-`.** The components' composition tokens (`--rt-input-color-*`, `--rt-nav-*`,
  `--rt-field-*-color`) paint the screen on a par with them, and a forgotten one among them is just
  as invisible.
- **A dark answer lives in the styling layer or declares the component's own property.** A dark
  block in a component's styles painting a property directly is a divergence; overriding a scale
  step by the dark theme is one too — the scale is unchangeable.
- **An accepted list entry carries a reason, and an empty reason fails the run.** A list of four
  dozen places without reasons reads a month later as a list of what somebody once decided not to
  fix.
- **The contrast threshold is one for all the pairs — 4.5:1 — and the list of pairs is kept by
  hand.** The completeness of the list a machine does not judge: a forgotten pair is as silent as
  one that is not there. It is judged by the owner at the review.
- **Contrast numbers are not written into documents.** The measurement table on the "Colors" page
  computes the same thing in the browser over the drawn nodes; the check matches only the
  composition of the pairs against it. A ratio written as text goes stale at the first edit of a
  value and stays silent about it.

## The styling layer is built, not edited

The source is `projects/ui-kit-v2/src/styles/tokens.source.mjs`, the generator is
`tools/build-tokens-v2.mjs`, the audit is `pnpm run check:tokens-build`. What is built is three
styles files of the styling layer and the name types
`projects/ui-kit-v2/src/lib/tokens/rt-design-tokens.ts`.

- **A step, an assignment and the dark theme's answer are edited in the source.** An in-place edit
  is lost on the next build, and the audit names it; every built file carries a header about this.
- **The dark answer lives in the source next to its light assignment, and the dark layout names
  only the names.** A forgotten half of a pair is visible where the colour is edited rather than by
  matching two files: a name without an answer and an answer without a name in the layout each fail
  the build in their own way.
- **A reference to a name the source does not declare and that is not named a consumer handle fails
  the build, and what is built is not rewritten at that.** Otherwise a name with a typo simply does
  not apply: the rule works, the value does not arrive, and this can be seen only in the showcase
  and only if one looks.
- **What is built matches what the formatter gives.** The generator puts a long composite value
  under its name exactly as prettier does: diverging, they give an eternal edit — the formatter
  rewrites the file, the audit turns red on the next run.
- **Rules that declare no properties do not get into the built file.** The backdrop of the sign-in
  screens and the logo inversion stand in their own file `_theme-dark-rules.scss`: the built one
  holds declarations only.
- **The third layer — the component's properties — is not built by the source.** They live in their
  own component's styles next to their own rules; the source knows the scale, the assignments and
  the dark answers.
