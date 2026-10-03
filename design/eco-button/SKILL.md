---
name: eco-button
description: ECO Design System button component spec — variants, sizes per breakpoint, states, focus handling, and CSS template. Use whenever creating or editing a <button> in this repo. Read the eco-tokens skill first for the token names referenced below.
---

# eco-button

Component spec for buttons, condensed from CLAUDE.md's "Knapp-styling (ECO Design System)" section and rewritten to reference `eco-tokens` instead of hardcoded hex. Figma: `node-id=2007-68126` in the ECO Design System file.

**Read `eco-tokens/SKILL.md` and `eco-tokens/tokens.json` first** — every color below is a token, not a literal value. If CLAUDE.md's button section and this file ever disagree on a color hex, trust the token in `tokens.json` (see "Known drift" in eco-tokens).

## Variants

| Variant | Background | Text | Border |
|---|---|---|---|
| **Primary** | `color.surface-action-1` (`#000`) | `color.text-primary-inverted` (`#fff`) | — |
| **Primary Inverted** | `color.surface-action-2` (`#fff`) | `color.text-primary` (`#000`) | — |
| **Secondary** | transparent | `color.text-primary` | `1px solid` `color.border-action-1` |
| **Secondary Inverted** | transparent | `color.text-primary-inverted` | `1px solid` `color.border-action-2` |
| **Blank** | transparent | `color.text-primary` | — |
| **Blank Inverted** | transparent | `color.text-primary-inverted` | — |
| **Destructive** | `color.surface-danger-default` (`#d90000`) | `color.text-primary-inverted` | — |
| **Accent** | `color.accent-default` (`#c7d300`) | `color.text-primary` | — |
| **System** | transparent | `color.text-primary` | `1px solid` `color.border-action-3` (`rgba(0,0,0,.10)`) |
| **System Selected** | `color.surface-opacity-black-12` | `color.text-primary` | `1px solid` `color.border-action-3` |
| **Disabled** (any variant) | `color.surface-disabled` | `color.text-disabled` | — |
| **Disabled Blank** | transparent | `color.text-disabled` | — |

`System` is for buttons that act at a system level (filters, sort, tool selection) — distinct from `Secondary` by its subtle semi-transparent border (`border-action-3`) instead of a solid black one. `System Selected` is the active/selected state of `System` — same border, `surface-opacity-black-12` background marks the selected state.

## Sizes

Desktop (`min-width: 769px`, breakpoint `lg-md`):

| Size | Height | Button padding | Text padding | Font |
|---|---|---|---|---|
| **lg** | 56px | 16px | `px-8px py-3px` | label-lg: 18px Bold, 0.18px spacing |
| **md** | 48px | 12px | `px-8px py-3px` | label-lg: 18px Bold, 0.18px spacing |
| **sm** | 40px | 8px | `px-8px py-4px` | label-md: 16px Bold, 0.48px spacing |
| **xs** | 32px | 6px | `px-4px py-3px` | label-sm: 14px Bold, 0.56px spacing |

Mobile (default, breakpoint `sm-xs`):

| Size | Height | Padding | Font |
|---|---|---|---|
| **lg** | 48px | 12px | label-lg: 16px Bold, 0.32px spacing |
| **md** | 40px | 8px | label-lg: 16px Bold, 0.32px spacing |
| **sm** | 32px | 6px | label-md: 14px Bold, 0.48px spacing |
| **xs** | 32px | 6px | label-sm: 14px Bold, 0.56px spacing |

Font sizes/line-heights/letter-spacing for `label-lg/md/sm` are in `eco-tokens/tokens.json` → `typography` (already split mobile/desktop) — use those values rather than retyping them, they're identical to what's above.

## States

| State | Rule |
|---|---|
| **Enabled** | Base style per variant above |
| **Hover — Primary / Destructive / Accent** | `background-image: linear-gradient(90deg, color.surface-opacity-white-20, color.surface-opacity-white-20), linear-gradient(90deg, [base color], [base color])` — white 20% overlay on top of the solid background |
| **Hover — Secondary** | `background: color.surface-opacity-black-05` |
| **Hover — Blank / icon buttons on light background** | `background: color.surface-opacity-black-05` — same rule as Secondary hover |
| **Focus** | Ring shown **only on keyboard navigation** (Tab), never on click. `outline: 2px solid transparent; outline-offset: 2px;` on the button, then `body.keyboard-nav button:focus { outline-color: color.border-focus /* #455efb */ }`. Use the `outline` method, not a `::after` with `inset` — a button with a border (e.g. Secondary's 1px) loses its gap with the inset method (`inset:-3px − 1px border − 2px ring = 0px gap`); `outline` always measures from the outer border edge, so the 2px gap stays consistent regardless of variant. |
| **Disabled** | Per Disabled row in the Variants table above. `cursor: not-allowed`. |

`body.keyboard-nav` is set globally via JS on `Tab` keydown and removed on `mousedown`/`touchstart` — reuse the existing global listener rather than adding a second one; check `template.html`/`mypages-template.html` for it before writing a new one.

## Typography (all buttons)

- Font: `Breuer Condensed Bold`, sans-serif
- `text-transform: uppercase`
- `white-space: nowrap`
- `font-feature-settings: 'ss02' 1, 'ss03' 1` (for label-lg/md)

## CSS template (Primary, adapt per variant/size using the tables above)

```css
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  position: relative;
  border: none;
  cursor: pointer;
  font-family: 'Breuer Condensed', Arial, sans-serif;
  font-weight: 700;
  text-transform: uppercase;
  white-space: nowrap;
  outline: 2px solid transparent;
  outline-offset: 2px;
  transition: outline-color 100ms cubic-bezier(.35,0,.35,1); /* duration-fast-2, ease-standard */
}
body.keyboard-nav .btn:focus { outline-color: var(--color-border-focus); }

/* Sizes -- Desktop (md: 769px+) */
.btn--lg { height: 56px; padding: 16px; font-size: 18px; letter-spacing: 0.18px; }
.btn--md { height: 48px; padding: 12px; font-size: 18px; letter-spacing: 0.18px; }
.btn--sm { height: 40px; padding: 8px;  font-size: 16px; letter-spacing: 0.48px; }
.btn--xs { height: 32px; padding: 6px;  font-size: 14px; letter-spacing: 0.56px; }
/* Mobile overrides (default, wrap desktop sizes above in @media (min-width: 769px) instead) */

/* Variants */
.btn--primary   { background: var(--color-surface-action-1); color: var(--color-text-primary-inverted); }
.btn--secondary { background: transparent; color: var(--color-text-primary); border: 1px solid var(--color-border-action-1); }
.btn--destructive { background: var(--color-surface-danger-default); color: var(--color-text-primary-inverted); }
.btn--accent    { background: var(--color-accent-default); color: var(--color-text-primary); }
.btn--blank     { background: transparent; color: var(--color-text-primary); }
.btn--system    { background: transparent; color: var(--color-text-primary); border: 1px solid var(--color-border-action-3); }
.btn--system.is-selected { background: var(--color-surface-opacity-black-12); }

/* Hover */
.btn--primary:hover, .btn--destructive:hover, .btn--accent:hover {
  background-image: linear-gradient(90deg, var(--color-surface-opacity-white-20), var(--color-surface-opacity-white-20)),
                     linear-gradient(90deg, currentColor, currentColor); /* replace currentColor with the variant's own bg var */
}
.btn--secondary:hover, .btn--blank:hover { background: var(--color-surface-opacity-black-05); }

/* Disabled */
.btn:disabled, .btn--disabled { background: var(--color-surface-disabled); color: var(--color-text-disabled); cursor: not-allowed; border: none; }
.btn--blank:disabled { background: transparent; }
```

Note: the hover gradient's second `linear-gradient(90deg, X, X)` must use the variant's *own* solid background color (e.g. `var(--color-surface-action-1)` for Primary, `var(--color-surface-danger-default)` for Destructive, `var(--color-accent-default)` for Accent) — write it out per variant rather than `currentColor`, which was only a placeholder above.

## Before shipping a new/changed button

Per CLAUDE.md's quality-control checklist (applies repo-wide, not just buttons): verify the breakpoint switch actually happens at 769px (not 640px) by checking computed styles at ~375px, ~700px, and ~1024px+ — don't assume the CSS is right just because it reads correctly. Search the file for an existing `.btn`/button pattern before adding a new CSS class; extend, don't duplicate.
