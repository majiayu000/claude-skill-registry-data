---
name: diagrams-and-charts
description: >
  Create blog-quality diagrams and data charts (architecture flows, data structure cards, grouped
  bar charts) as plain HTML, then export them to PNG with a playwriter-based CLI. Ships two
  styles: claude-style (Anthropic engineering blog look, light) and nextjs-style (Next.js docs
  look, dark). Use when the user wants a diagram, chart, figure,
  infographic or data visualization image for a blog post, docs or social, especially "Anthropic
  style", "Claude style", "Next.js style" or a dark diagram.
---

# diagrams-and-charts

Figures are **plain HTML files**: boxes laid out with a css grid, arrows and charts drawn from
data by small TypeScript helpers. `render.ts` exports them through the user's Chrome.

The image is **only the diagram or chart** on its light background, with padding and square
corners. No title, no page frame, no outer card: the blog post or doc supplies those. Put the
title in the surrounding text, not in the image.

```
fig.html ──▶ render.ts: Bun.serve + playwriter tab ──▶ wait network, fonts, helpers ──▶ png
   │ links /skill/<style>/style.css, imports /skill/diagram.ts, /skill/charts.ts
```

## Styles

A style is only fonts and colors: `<style>/style.css` sets tokens and imports the shared
`base.css`. Layout rules live in `claude-style/DESIGN.md` and apply to every style.

| folder          | look                                                        |
| --------------- | ----------------------------------------------------------- |
| `claude-style/` | Anthropic engineering blog: light, warm gray, clay accent   |
| `nextjs-style/` | Next.js docs: dark, gray cards, blue, pink, purple, green, amber |

Switch style by changing one line in the html:

```html
<link rel="stylesheet" href="/skill/nextjs-style/style.css" />
```

Start from the closest example in `examples/` (they link claude-style):

| example                  | use for                                           |
| ------------------------ | ------------------------------------------------- |
| `architecture-flow.html` | services, clients, data flow arrows               |
| `changeset-shape.html`   | struct / record card, storage tiers, derived data |
| `grouped-bar-chart.html` | benchmark comparisons, before vs after            |

## Workflow

1. Read `claude-style/DESIGN.md` (and the chosen style's DESIGN.md). Copy the closest example into a **new file** with a unique
   name, next to where the user wants the image or in `./tmp/<figure-name>/`. Never edit files in
   this skill folder: other agents may render from it at the same time.
2. Replace the content with the user's data. Keep `<div class="canvas" id="diagram">` as root;
   it is exactly what gets exported. Use `.section` + `.section-label` to split one figure into
   regions (e.g. metadata vs storage).
3. Render, then read the png back and fix what looks wrong:

   ```bash
   bun ~/.config/opencode/skills/diagrams-and-charts/render.ts render ./fig.html -o ./fig.png
   ```

Run `render.ts render --help` for options (`--id`, `--scale`, `--width`, `--dark`). Output type
comes from the extension: `.png` / `.jpg` (default scale 2: 2120px wide) or `.svg`.

**SVG for websites and READMEs.** `-o fig.svg --dark nextjs-style` writes one self-contained
svg (css and latin fonts embedded, ~80 to 160 KB) whose colors follow the viewer's light or dark
mode: the page's style in light mode, the colors of `--dark <style>` in dark mode (fonts stay).
Embed it as a plain markdown image `![alt](/assets/fig.svg)`: no `<picture>`, works on GitHub
and in Holocron. Write a full alt text that describes the flow, agents read it instead of
the image.

## Writing figures

- **No coordinates.** Place boxes in a `.flow` grid by cell (`grid-area: row / col`). Give
  boxes that arrows touch an `id`.
- **Arrows** from ids, after the markup:

  ```html
  <script type="module">
    import { connect } from '/skill/diagram.ts'
    connect('dev', 'cache', { color: 'accent', label: 'Trees and file contents' })
    connect('cache', 'server', { from: 'right', to: 'bottom', color: 'accent' })
    connect('server', 'storage', { color: 'purple' })
  </script>
  ```

  Sides are picked from the layout. Force them with `from` / `to` when the route crosses a box.
- **Use the whole palette.** Every style has `blue` plus four category hues: `pink`, `purple`,
  `green`, `amber`. Give each category of boxes one hue (`class="box green"`, also on `.group`
  and `.dashed`) and color the wires of that category the same (`color: 'green'`; the label
  follows). Typical mapping: clients/users green, your system blue, cloud/third party purple,
  devices or targets pink, storage amber. Keep `accent` for the one highlighted path. Bar chart
  series take `colors: ['bar', 'green', ...]`.
- **Charts** from data: `barChart('#diagram', spec)` from `charts.ts`, on an empty canvas. Format value labels yourself;
  values in one chart share one unit.
- `/skill/` maps to this folder, other paths to the html folder. `.ts` files are transpiled on the
  fly, so page scripts can be TypeScript too (`<script type="module" src="./data.ts">`).

## Gotchas

- Concurrent renders are safe: each run uses its own port, tab and playwriter session.
  Only the html and output paths must be unique per figure.
- Needs Chrome with the playwriter extension connected. If connecting fails, ask the user to
  click the extension icon. The CLI opens its own tab in a `diagrams` tab group and closes it.
- Page errors (bad id in `connect`, js exceptions) fail the render with the message. Read it.
- The canvas is 1060px. Keep to about 5 columns and short sub lines; the CLI prints
  `warning: clipped` with the element names when something sticks out. Fix every warning.
- A wire label is centered on its longest segment, so the gap between two boxes must be wider
  than the label. Shorten the label or put it in `sub` (second line) when a gap is narrow.
- Two arrows leaving the same side of one box overlap. Spread them with `fromAt: 0.3` and
  `fromAt: 0.7`, or start one from the enclosing group.
- The svg is the rendered html inside a `<foreignObject>`. Browsers render it (also in `<img>`);
  design tools (Figma, Inkscape) and some image converters do not. Use png there.
- Code that draws asynchronously must register its promise with `track()` from `diagram.ts`,
  otherwise the screenshot can happen before it finishes.
- Use `.box.dashed` (svg outline), not css `border-style: dashed`. Import `diagram.ts` on pages
  with dashed boxes even when there are no arrows.
- Deps come from `~/.config/opencode/node_modules` (goke, playwriter, zod, string-dedent). If
  imports fail, run `bun add goke playwriter zod string-dedent` in `~/.config/opencode`.

## Adding a style

Create `<name>-style/` with `style.css` (fonts `@import`, then `@import url('../base.css')`, then
the `:root` tokens; copy the token list from an existing style), a short `DESIGN.md` with the
palette table, and `references/`. Never hardcode colors in `base.css`, the ts helpers or html:
use tokens, so every figure works in every style.
