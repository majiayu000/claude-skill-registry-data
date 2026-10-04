---
name: design-tokens
description: Use when writing or editing any StyleSheet in kasane — adding a component, restyling a screen, picking a colour, choosing spacing, or when asked to make the UI consistent, fix the palette, or clean up styles.
---

# Design Tokens

`src/theme.ts` is the single source of colour, spacing, and type. Components read from it. **No component introduces a hex literal.**

The tokens were extracted from the 283 hex literals that were previously inlined across `app/` and `src/components/`; the values are unchanged, so replacing a literal with its token is always a pure refactor with no visual diff.

## Quick reference

```ts
import {
  COLOR,
  SPACE,
  TEXT,
  FONT,
  ARC_COLORS,
  MOVIE_COLOR,
  arcColors,
  pressFeedback,
  NARROW_WIDTH,
} from "@/theme";
```

| Need                                          | Token                                         |
| --------------------------------------------- | --------------------------------------------- |
| Screen background, `Stack` `contentStyle`     | `COLOR.background`                            |
| Card, pill, chip                              | `COLOR.surface`                               |
| Block that must separate from a card          | `COLOR.surfaceRaised`                         |
| Notice banner background                      | `COLOR.surfaceNotice`                         |
| Divider, input border                         | `COLOR.border`                                |
| Box behind a loading cover                    | `COLOR.coverPlaceholder`                      |
| Heading, body copy                            | `COLOR.textPrimary`                           |
| Supporting copy                               | `COLOR.textSecondary`                         |
| Label, metadata, uppercase eyebrow            | `COLOR.textMuted`                             |
| `placeholderTextColor`, lowest emphasis       | `COLOR.textFaint`                             |
| Links, active state, brand rule               | `COLOR.accent`                                |
| "Arcs behind", "auto-estimated", "no mapping" | `COLOR.notice`                                |
| Error text                                    | `COLOR.danger`                                |
| Arc segment fill and text                     | `arcColors(segment)`                          |
| Film segment                                  | `MOVIE_COLOR`                                 |
| Any `gap` or `padding`                        | `SPACE.xxs`…`SPACE.pageEndTall`               |
| Clearance above the footer                    | `FOOTER_OFFSET`                               |
| Eyebrow, button, chip, section/page titles    | `...TEXT.<preset>`, plus a `color`            |
| Press and hover feedback on a `Pressable`     | `(state) => [styles.x, pressFeedback(state)]` |
| Phone-width cut-off                           | `NARROW_WIDTH`, or `useIsNarrow()`            |

`SPACE` runs `xxs` 2 · `xs` 4 · `sm` 6 · `md` 8 · `mdl` 10 · `lg` 12 · `lgx` 14 · `xl` 16 · `xxl` 20 · `xxxl` 24 · `page` 32 · `pageEnd` 40 · `pageEndTall` 48. `mdl` and `lgx` are the in-between steps existing controls rely on; prefer the main steps for new UI.

`ARC_COLORS` is shared so the same arc is the same colour in the rail and the pie, and `arcColors` is the one place that picks a segment's slot. Do not reorder it and do not fork a second copy into a component.

## Layout rules

- **No margins.** Space with `gap` and `padding` on the container. This is a hard repo rule, not a preference.
- Lay grids out with `flexDirection: "row"`, `flexWrap: "wrap"`, `gap`, and tile widths from `gridLayout`/`tileWidthFor` in `src/data/gridLayout.ts`. React Native's style types have no `display: "grid"`, so using it takes a cast — and it does nothing on a native tablet. Measure the container with `useLayoutWidth` when the tiles must fill it exactly.
- Reach for a token even when the value looks incidental. `gap: 6` becomes `SPACE.sm`.

## Adding a token

A new colour needs a **role**, not a shade. `COLOR.warningBannerBorder` is a role; `COLOR.yellow2` is not. If no existing role fits, add one to `src/theme.ts` with a comment saying where it applies, then use it. Two roles may legitimately share a value: `COLOR.danger` and `ARC_COLORS[0]` are both `#ff7c5c` and are unrelated, which is exactly why they are separate names.

## Migrating existing styles

When you touch a `StyleSheet.create` block for any reason, convert the literals in that block to tokens. Do not open a separate sweep across all 21 files; convert opportunistically so every diff stays reviewable and visually verifiable.

Find remaining literals:

```bash
grep -rn "#[0-9a-fA-F]\{3,8\}" --include="*.tsx" app src
```

## Common mistakes

| Mistake                                     | Why it hurts                                                                                    |
| ------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| `color: "#f5f5f5"` in a new component       | The next palette change misses it. Use `COLOR.textPrimary`.                                     |
| Naming a token by its colour                | `COLOR.violet` cannot be re-themed. Name the role.                                              |
| Copying `ARC_COLORS` into a component       | The rail and the pie would drift and the same arc would render two colours.                     |
| Adding `margin` "just this once"            | Banned. Use container `gap`/`padding`.                                                          |
| Replacing every literal in one giant commit | Unreviewable, and a single wrong swap is a silent visual regression. Convert per touched block. |
