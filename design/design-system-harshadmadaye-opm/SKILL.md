---
name: design-system
description: Creates or extracts a DESIGN.md design system with colour roles, typography, spacing and radius tokens plus a short voice and do/don't guide, validated for contrast. Use when starting a UI project, when asked for a design system, theme, tokens or style guide, or when frontend-design finds no DESIGN.md.
---

# Design system

**Announce at start:** "Using opm-design:design-system to write a validated DESIGN.md."

`P/` below is `${CLAUDE_PLUGIN_ROOT}`. Read `references/design-md-format.md` before writing; the
validator accepts only that format.

## Pick the mode

- **Create** when the project has little or no styling yet.
- **Extract** when it already has a Tailwind config, theme files, CSS custom properties or styled
  components. If both seem true, ask once with AskUserQuestion.

## Create

1. Ask the product type with AskUserQuestion, offering the rows of
   `references/starting-palettes.md` plus "Other".
2. Start from that row: style, palette, font pairing and spacing scale. Change only what the user
   asks to change.
3. Write `DESIGN.md` at the project root: the frontmatter tokens, then the Intent, Voice, Do,
   Don't and Components sections. Intent and Voice come from the user's words; do not invent a
   brand story.

## Extract

Follow `references/extract-from-code.md`:

1. Read sources in priority order: Tailwind config or theme files, then CSS custom properties,
   then component styles.
2. Merge near-duplicate colours: `node P/skills/frontend-design/scripts/contrast.mjs --delta '#3B82F6' '#3A80F5'` (quote hex values).
   Under 3 is the same colour; keep the one used more often.
3. Name each colour by role ("Primary action", "Surface", "Danger"), never by hue, and record the
   source file of each token in the Components section.
4. Write `DESIGN.md` as in Create step 3.

## Validate (both modes)

Run `node P/skills/design-system/scripts/validate-design-md.mjs DESIGN.md`. Fix every
`Violation:` line and rerun until it prints `ok:`. A failing text/surface pair (F-01) is fixed by
changing a token, never by removing the role.

Report the `ok:` line and the token counts. Offer `/opm-design:frontend-design` next if UI work
is waiting.

## Red flags

| Thought | Reality |
|---|---|
| "I'll name it blue-500" | Name colours by role; hue names break on a rebrand. |
| "Close enough, keep both greys" | Merge under ΔE 3; near-twin tokens drift apart. |
| "The validator is too strict" | F-01 is a floor rule. Change the colour. |
| "I'll describe the brand voice myself" | Voice comes from the user or stays a question. |
