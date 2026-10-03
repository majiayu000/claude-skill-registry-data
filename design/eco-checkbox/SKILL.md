---
name: eco-checkbox
description: ECO Design System checkbox component spec — light mode and dark mode states, sizing, and CSS template. Use whenever creating or editing an <input type="checkbox"> in this repo. Read the eco-tokens skill first for the token names referenced below.
---

# eco-checkbox

Component spec for checkboxes, condensed from CLAUDE.md's "Checkbox – Styling" and "Checkbox – Dark Mode" sections and rewritten to reference `eco-tokens`. Figma: `node-id=6408-8453`.

**Read `eco-tokens/SKILL.md` and `eco-tokens/tokens.json` first.** Implement checkboxes with `<input type="checkbox">` + CSS — never `<img>` or an external SVG file.

## Sizing

Total interactive area: 24×24px. Visible box: 16×16px (`appearance: none` + custom border). `margin: 4px` on all sides gives the 24×24 total. Focus ring uses `outline: 2px` with `outline-offset: 2px` — that exactly fills the 4px margin (2px gap + 2px ring = 4px).

## Light mode — states

| State | Background | Border | Checkmark |
|---|---|---|---|
| **Default (unchecked)** | `color.background-primary` (`#fff`) | `1.5px solid` `color.border-selected` (`#000`) | — |
| **Hover (unchecked)** | — | `2px solid` `color.border-selected` (border only gets thicker, no fill) | — |
| **Checked** | `color.surface-100` (`#000`) | `color.border-selected` | White (`stroke="white"`) |
| **Hover (checked)** | `color.text-disabled` (`#939595`) | `color.text-disabled` (`#939595`) | White |
| **Indeterminate** | `color.surface-100` (`#000`) | `color.border-selected` | White horizontal dash |
| **Disabled (unchecked)** | `color.background-primary` | `color.border-disabled` (`#dad9d7`) | — |
| **Disabled (checked)** | `color.surface-disabled` (`#e5e5e5`) | none (matches background) | Grey (`stroke="#939595"`, i.e. `color.text-disabled`) |

`disabled:checked` is light grey background + grey checkmark — **not** the same as the hover-checked dark-grey styling. Don't conflate the two.

**Focus:** ring color is `color.border-focus` (`#455efb`) — this is the same focus token used everywhere else in the system (buttons, inputs, selects). Shown only via `outline-offset: 2px` on `:focus-visible`.

> **Flag:** an earlier, simpler checkbox spec in CLAUDE.md lists the focus ring as `#0052CC`, which doesn't match `border-focus` (`#455efb`) or any other token in the package — every other component in CLAUDE.md and in `tokens.json` uses `#455efb` for focus. Treat `#0052CC` as a stale value from that older section and use `color.border-focus` instead; worth a human fixing the CLAUDE.md source at some point.

## Dark mode — states

Use `.form-checkbox-item--dark` whenever the checkbox sits on a dark surface (`color.surface-100`, `color.surface-80`, etc.) — never the light-mode markup on a dark background.

| State | Fill | Stroke/Border |
|---|---|---|
| **Enabled / Hover / Focus** (unchecked) | transparent (`color.surface-opacity-white-0`) | `color.border-action-2` (`#fff`) |
| **Selected / Selected Focus** | `color.border-action-2` (`#fff`) | `color.border-action-2` |
| **Selected Hover** | `color.surface-40` (`#939595`) | `color.surface-40` |
| **Disabled** | transparent | `color.surface-60` (`#595959`) |
| **Disabled Selected** | `color.surface-60` | `color.surface-60` |
| Checkmark (Selected / Selected Focus) | `color.surface-100` (`#000`, i.e. dark checkmark on the white fill) | — |
| Checkmark (Selected Hover) | `color.border-action-2` (`#fff`) | — |
| Label text | `color.text-primary-inverted` (`#fff`); disabled: `color.text-disabled` | — |

Focus ring in dark mode is the same `color.border-focus` token, same `outline-offset: 2px`, shown only via `:focus-visible`.

## CSS template — light mode

```css
.form-checkbox-item { display: flex; align-items: center; gap: 8px; cursor: pointer; }
.form-checkbox-item input[type="checkbox"] {
  appearance: none; width: 16px; height: 16px;
  border: 1.5px solid var(--color-border-selected);
  background: var(--color-background-primary);
  cursor: pointer; flex-shrink: 0; margin: 4px;
}
.form-checkbox-item input[type="checkbox"]:hover { border-width: 2px; }
.form-checkbox-item input[type="checkbox"]:focus-visible { outline: 2px solid var(--color-border-focus); outline-offset: 2px; }
.form-checkbox-item input[type="checkbox"]:checked { background-color: var(--color-surface-100); border-color: var(--color-border-selected); /* + SVG checkmark, white stroke */ }
.form-checkbox-item input[type="checkbox"]:indeterminate { background-color: var(--color-surface-100); border-color: var(--color-border-selected); /* + SVG dash, white stroke */ }
.form-checkbox-item input[type="checkbox"]:disabled { border-color: var(--color-border-disabled); cursor: not-allowed; }
.form-checkbox-item input[type="checkbox"]:disabled:checked { background-color: var(--color-surface-disabled); border-color: var(--color-surface-disabled); /* + SVG checkmark, #939595 stroke */ }
.form-checkbox-item:has(input:disabled) { cursor: not-allowed; }
.form-checkbox-item:has(input:disabled) span { color: var(--color-text-disabled); }
```

## CSS template — dark mode

```css
.form-checkbox-item--dark { display: flex; align-items: center; gap: 8px; cursor: pointer; }
.form-checkbox-item--dark input[type="checkbox"] {
  appearance: none; width: 16px; height: 16px;
  border: 1.5px solid var(--color-border-action-2);
  background: transparent;
  cursor: pointer; flex-shrink: 0; margin: 4px;
}
.form-checkbox-item--dark input[type="checkbox"]:hover { border-width: 2px; }
.form-checkbox-item--dark input[type="checkbox"]:checked {
  background-color: var(--color-border-action-2);
  border-color: var(--color-border-action-2);
  /* + SVG checkmark, stroke = var(--color-surface-100) (#000, dark mark on white fill) */
}
.form-checkbox-item--dark input[type="checkbox"]:checked:hover {
  background-color: var(--color-surface-40);
  border-color: var(--color-surface-40);
  /* + SVG checkmark, stroke = var(--color-border-action-2) (#fff) */
}
.form-checkbox-item--dark input[type="checkbox"]:focus-visible { outline: 2px solid var(--color-border-focus); outline-offset: 2px; }
.form-checkbox-item--dark input[type="checkbox"]:disabled { border-color: var(--color-surface-60); cursor: not-allowed; }
.form-checkbox-item--dark input[type="checkbox"]:disabled:checked {
  background-color: var(--color-surface-60);
  border-color: var(--color-surface-60);
  /* + SVG checkmark, stroke = var(--color-text-disabled) (#939595) */
}
.form-checkbox-item--dark span { color: var(--color-text-primary-inverted); font-family: 'Breuer Condensed', sans-serif; }
.form-checkbox-item--dark:has(input:disabled) span { color: var(--color-text-disabled); }
```

The checkmark/dash itself is always an inline SVG `background-image` (data URI) on the `:checked`/`:indeterminate` rule — never a separate `<img>` tag or external file. Copy the exact SVG paths from CLAUDE.md's existing checkbox CSS blocks rather than redrawing them, only swap the `stroke` color per state per the tables above.

## HTML structure

```html
<label class="form-checkbox-item">
  <input type="checkbox" />
  <span>Label</span>
</label>
```

Dark mode: same structure with `form-checkbox-item--dark`. Always pair the checkbox with a `<label>` wrapping both the input and its text — never a bare `<input>`.

## Before shipping

Search the current file for an existing `.form-checkbox-item` block before adding a new one — extend/reuse rather than duplicating a parallel checkbox implementation. Test hover, focus (keyboard only), checked, indeterminate, and disabled states at both a mobile (~375px) and desktop (~1024px+) width before calling it done, per CLAUDE.md's repo-wide quality checklist.
