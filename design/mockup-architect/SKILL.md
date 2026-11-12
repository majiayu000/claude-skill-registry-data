---
name: mockup-architect
version: 1.0.1
description: Standards for UI mockups as self-contained HTML — dated folders, a gallery index, tokens as CSS variables, and the fixed preview bar that flips palette, corners, accent and mark variants (state in data attributes, localStorage and ?query so screenshots are reproducible). Ships pv-bar.css and pv-bar.js. Use when drawing, comparing or retrofitting mockups, or when a mockup offers options to choose between.
---

# Mockup architect

How to build mockups that can be compared, screenshotted and decided on. Companion to
[landing-page-designer](../landing-page-designer/SKILL.md) (what a landing page must say) and
[ui-ux-architect](../ui-ux-architect/SKILL.md) (what the shipped UI must satisfy).

## 1. Rules

- **Self-contained.** One `.html` opens from `file://`: inline or sibling CSS/JS, no build step, no CDN.
  A mockup never imports the app's code.
- **Dated folder** `mockups/<collection>/<YYYY-MM-DD>/`, an `index.html` gallery linking every page, and a row
  in the collection README (file, what it decides). Superseded rounds move to `archive/`; do not edit them.
- **Tokens, not literals.** Colours, radii and fonts are CSS variables on `:root`; variants are
  `:root[data-<axis>=<value>]` blocks. Same names as the app (`--bg --card --text --muted --line --line-strong
  --accent --btn-bg --btn-fg --shadow`) so the bar and the port both work.
- **One question per page.** A page that offers options says what is being decided and recommends one.
- **Honest data.** Numbers are real or marked sample.
- **Draw, do not ship.** Mockups never touch the app's source.

## 2. The preview bar (use it whenever a page offers options)

`assets/pv-bar.css` + `assets/pv-bar.js`; `assets/example.html` is a working page. Copy both files next to the
mockups (or inline them); do not link across repos.

1. Declare axes in `<script type="application/json" id="pv-config">` in `<head>`, before `pv-bar.js`. Each axis has
   `key`, `label`, `values: [{v, label, sw?}]`; the first value is the default; `when: {key, is}` shows an axis only
   while another has that value (e.g. accent only on palette B).
2. Style variants with `:root[data-<key>=<v>]`. The bar itself reads the page's tokens, so it needs no variants.
3. State is written to `<html data-<key>>`, persisted in `localStorage` as `pv-<key>`, and forced by the query
   string (`?palette=b&accent=ink`). The query wins and is not persisted. A screenshot or parity script renders an
   exact variant by URL; never click in a script.
4. Add class `pv-clear` to the last section so the bar never covers content. Hide the bar in captures with
   `.pv{display:none}`.
5. Accessibility: it is a `role=region` with `aria-pressed` buttons, 36px targets and a forced-colors rule. Check the
   contrast of every variant, not only the default; a variant that fails is a finding, not a footnote.

Axes worth offering: palette, corners (`soft`/`sharp`), accent, logo mark, density, theme (`light`/`dark`).
Keep each axis to what the owner can actually choose; a bar with ten axes decides nothing.

## 3. Retrofit checklist (existing mockups)

1. Only pages that compare options get the bar; single-spec pages do not. Rounds with one file per option (palettes or directions generated as separate files), JS-driven switchers that set properties from a map, and canvas exports are left alone: converting them means reworking the generator, which is a separate job. If a page is generated, change the generator and regenerate, never only the output.
2. Move the page's variant colours into `data-` blocks; remove ad hoc toggles.
3. Add the config, the two assets and `pv-clear`; keep the page working with the bar removed.
4. Open it with each `?query` once; check no console errors.
5. Record the change in the collection README.

## 4. Verification bar

Parser check (no unclosed tags), an axe run per variant and theme, a 390px and a 1440px screenshot per variant,
no console errors, works from `file://`.
