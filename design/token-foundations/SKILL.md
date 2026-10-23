---
name: token-foundations
description: "Build or audit semantic design tokens in OKLCH, light and dark. Use when the user says \"set up design tokens\", \"audit the token foundation\" or \"OKLCH colour scales\"."
license: MIT
metadata:
  author: Tony Gorb
  source: https://github.com/tonygorb/skills
  category: design-systems
  cover: "OKLCH"
---

# Token foundations

Build the token layer a product's UI stands on, or audit the one it has. Colour in OKLCH, a
semantic layer over raw scales, light and dark from day one, small scales for type, space and
radius. Structure stays boring so every screen built on it comes out consistent.

This skill works on the tokens themselves. To sweep components for hard-coded colours and swap in
tokens, use `polish-design-system` after this.

## The rule underneath

Three layers, strictly separate.

1. **Primitives.** Raw values with no meaning: `color.brand.500`, `spacing.4`, `radius.md`.
2. **Semantic tokens.** Say what a value is for and point at a primitive: `background`,
   `surface.default`, `text.primary`, `action.primary`. Every colour role declares a light and a
   dark value.
3. **Component tokens.** Only when a reusable component needs one: `button.height.md`,
   `card.radius`. Never per page.

Components use semantic and component tokens only. Never primitives, never raw values.

Keep one source of truth. It can be a tokens JSON file that generates the theme CSS, or the theme
CSS itself. Everything else is derived from it. Never hand-maintain two copies.

## Steps

### 1. Look before you write

Find what the project already has:

- The stack and the theme file (`app/globals.css`, `src/styles/global.css`, `src/index.css`, or
  wherever the global CSS lives).
- Tailwind and its version: v4 uses an `@theme` block in CSS, v3 a `tailwind.config` file.
- Existing tokens: JSON files, `:root` custom properties, a `@theme` block.
- How dark mode switches today: a `.dark` class, a `data-theme` attribute, the system setting.

Then decide the job with the user: **set up** (steps 2 to 7) or **audit** (step 8, read-only).

### 2. Ask for the brand inputs

Ask only what the brief doesn't answer. Three to six questions at most:

- Brand seed colour. Take it as OKLCH (`oklch(60% 0.18 250)`), or convert the hex they give you.
- An accent seed, if there is one.
- Neutrals: tinted toward the brand hue, or pure grey.
- Fonts: sans, and mono if needed.
- Personality and audience, in a few words.
- Anti-references: what it must not look like.

### 3. Generate the colour primitives in OKLCH

OKLCH is perceptually even: the same lightness step looks the same on every hue, so contrast is
predictable. Never put hex or HSL in the source of truth.

Every scale has eleven steps, 50 to 950, with one hue and a fixed lightness ramp. Generate it;
never hand-pick eleven colours.

```bash
node -e '
const [L, C, H] = process.argv[1].split(" ").map(Number); // seed "60 0.18 250"
function linear(l, c) { // OKLCH (l in %) to linear sRGB (Ottosson)
  const a = c * Math.cos(H * Math.PI / 180), b = c * Math.sin(H * Math.PI / 180), Lp = l / 100;
  const x = (Lp + 0.3963377774 * a + 0.2158037573 * b) ** 3;
  const y = (Lp - 0.1055613458 * a - 0.0638541728 * b) ** 3;
  const z = (Lp - 0.0894841775 * a - 1.2914855480 * b) ** 3;
  return [4.0767416621 * x - 3.3077115913 * y + 0.2309699292 * z,
         -1.2684380046 * x + 2.6097574011 * y - 0.3413193965 * z,
         -0.0041960863 * x - 0.7034186147 * y + 1.7076147010 * z];
}
const inGamut = (l, c) => linear(l, c).every(v => v >= -1e-4 && v <= 1 + 1e-4);
const steps = [[50,97,.10],[100,94,.18],[200,88,.35],[300,80,.55],[400,70,.80],
               [500,60,1.0],[600,52,.95],[700,44,.85],[800,35,.65],[900,25,.45],[950,16,.30]];
const out = {}, clamped = [];
for (const [step, l, cMul] of steps) {
  let c = C * cMul;
  while (c > 0 && !inGamut(l, c)) c = Math.max(0, c - 0.005); // lower chroma until it fits sRGB
  if (c < C * cMul) clamped.push(step);
  out[step] = `oklch(${l}% ${c.toFixed(3)} ${H})`;
}
console.log(JSON.stringify(out, null, 2));
console.log("clamped to fit sRGB:", clamped.join(", ") || "none");
' "60 0.18 250"
```

The scales to make:

- **brand** from the brand seed.
- **neutral** with the brand hue and chroma at 0.05 times the seed's (tinted), or chroma 0 (pure
  grey). Add an `850` step between 800 and 900 for raised surfaces in dark mode, and `0` for pure
  white (`oklch(100% 0 0)`), so no semantic token has to hold a raw `white`.
- **accent** from the accent seed, only if there is one.
- **State scales** at fixed hues, whatever the brand: success 145, warning 75, danger 25, info 240.
  Move info if the brand itself is blue.

The script prints which steps it had to clamp to stay in sRGB. List them in the report.

### 4. Set the other primitive scales

Keep them small and reuse them hard. A sensible default set:

| Family | Steps |
|---|---|
| Spacing | 0, 0.5, 1, 1.5, 2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24, 32 (on a 4px unit: `4` = 16px) |
| Radius | none, xs, sm, md, lg, xl, 2xl, full |
| Font size | xs 12, sm 14, base 16, lg 18, xl 20, 2xl 24, 3xl 30, 4xl 36, 5xl 48, 6xl 60, 7xl 72 |
| Font weight | regular, medium, semibold, bold |
| Line height | tight 1.1, snug 1.25, normal 1.5, relaxed 1.625, loose 1.75 |
| Letter spacing | tighter, tight, normal, wide |
| Shadow | xs, sm, md, lg, xl |
| Motion | durations instant, fast, base, slow, slower; easings linear, standard, emphasized, decelerated, accelerated |
| Breakpoint | sm, md, lg, xl, 2xl |
| Z-index | base, dropdown, sticky, fixed, modal, popover, tooltip, toast |

On top of the font sizes, name the text styles the UI uses: display (large, medium), heading (xl,
lg, md, sm), body (lg, md, sm), caption and label. Each one fixes size, line height, weight and
letter spacing together.

On an existing product, radius and the type scale are brand decisions. Ask before you change them.

### 5. Map the semantic layer

Every role below exists, and every colour role has both modes. A good starting map:

| Role | Light | Dark |
|---|---|---|
| `background` | neutral.50 | neutral.950 |
| `foreground` | neutral.950 | neutral.50 |
| `surface.default` | neutral.0 | neutral.900 |
| `surface.muted` | neutral.100 | neutral.800 |
| `surface.elevated` | neutral.0 | neutral.850 |
| `surface.inverse` | neutral.950 | neutral.50 |
| `border.default` | neutral.200 | neutral.800 |
| `border.strong` | neutral.500 | neutral.600 |
| `border.focus` | brand.500 | brand.400 |
| `text.primary` | neutral.950 | neutral.50 |
| `text.secondary` | neutral.700 | neutral.300 |
| `text.muted` | neutral.600 | neutral.400 |
| `text.inverse` | neutral.50 | neutral.950 |
| `action.primary` | brand.600 | brand.500 |
| `action.primary-hover` | brand.700 | brand.400 |
| `action.primary-foreground` | neutral.0 | neutral.950 |
| `action.secondary` | neutral.100 | neutral.800 |
| `action.secondary-hover` | neutral.200 | neutral.700 |
| `action.secondary-foreground` | neutral.950 | neutral.50 |
| `action.disabled` | neutral.200 | neutral.800 |
| `state.{success,warning,danger,info}` | that scale's 600 | that scale's 600 |
| `state.{role}-foreground` | neutral.0 | neutral.0 |

Add `accent` and `accent-foreground` only if there is an accent seed. `accent` is never the
primary call to action: that is `action.primary`.

`border.default` is for dividers and card edges, which are decorative; `border.strong` is for
input and control outlines, which must reach 3:1.

State colours mean system state only, never decoration, and always come with an icon or text.

### 6. Add component tokens only where needed

Button and input heights, card padding, section padding, container widths, and component radii
that point at the radius scale (`button.radius` = `radius.md`). Nothing named after a page or a
section: no `hero.bg`, no `pricing.card.shadow`.

### 7. Write the theme

Naming: dot notation in JSON (`action.primary`), kebab-case as CSS variables
(`--color-action-primary`).

- **Tailwind v4:** primitives and the light semantic values go in `@theme`, so utilities like
  `bg-background` exist. Dark values override the semantic variables only.
- **Tailwind v3 or no Tailwind:** write `:root { … }` and `.dark { … }` custom properties, and
  extend the Tailwind config through those variables if Tailwind is there.

```css
@theme {
  --color-neutral-50: oklch(97% 0.001 250);
  /* … every primitive … */
  --color-background: var(--color-neutral-50);
  --color-text-primary: var(--color-neutral-950);
}

:root.dark, :root[data-theme="dark"] {
  --color-background: var(--color-neutral-950);
  --color-text-primary: var(--color-neutral-50);
}

@media (prefers-color-scheme: dark) {
  :root:not(.light):not([data-theme="light"]) { /* same dark overrides */ }
}

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { transition-duration: 0.01ms !important; animation-duration: 0.01ms !important; }
}

:root { color-scheme: light dark; }   /* follows the system when no theme is forced */
:root.dark, :root[data-theme="dark"] { color-scheme: dark; }
:root.light, :root[data-theme="light"] { color-scheme: light; }
```

Match the dark switch to the one the project already uses. Wrap the generated block in marker
comments so a later run replaces only that block. If the file has other CSS, merge; never
overwrite it.

Then run step 8 on what you wrote.

### 8. Audit: compute contrast, then score

Read-only. Change nothing in this step.

**Contrast.** Resolve every pair to its OKLCH values and compute real WCAG ratios, in both modes.
Never estimate by eye.

```bash
node -e '
function toRgb(L, C, H) { // OKLCH (L in %) to gamma-encoded sRGB 0-1 (Ottosson)
  const Lp = L / 100, a = C * Math.cos(H * Math.PI / 180), b = C * Math.sin(H * Math.PI / 180);
  const l = (Lp + 0.3963377774 * a + 0.2158037573 * b) ** 3;
  const m = (Lp - 0.1055613458 * a - 0.0638541728 * b) ** 3;
  const s = (Lp - 0.0894841775 * a - 1.2914855480 * b) ** 3;
  const lin = [4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
              -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
              -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s];
  const enc = v => v <= 0.0031308 ? 12.92 * v : 1.055 * v ** (1 / 2.4) - 0.055;
  return lin.map(v => Math.max(0, Math.min(1, enc(v))));
}
function lum(rgb) {
  const f = c => c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4;
  const [r, g, b] = rgb.map(f); return 0.2126 * r + 0.7152 * g + 0.0722 * b;
}
const pairs = JSON.parse(process.argv[1]); // [{name, fg:[L,C,H], bg:[L,C,H], min}]
for (const p of pairs) {
  const [x, y] = [lum(toRgb(...p.fg)), lum(toRgb(...p.bg))];
  const ratio = (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05);
  console.log(`${ratio >= p.min ? "pass" : "FAIL"}  ${ratio.toFixed(2)}  (min ${p.min})  ${p.name}`);
}
' '[{"name":"text.primary on background (light)","fg":[16,0.003,250],"bg":[97,0.001,250],"min":4.5}]'
```

Pairs to check, light and dark:

| Pair | Minimum |
|---|---|
| `text.primary` on `background`, `surface.default`, `surface.muted` | 4.5 |
| `text.secondary` on `background` | 4.5 |
| `text.muted` on `background` | 4.5 (3 only if it is never used below 24px, or 18.66px bold) |
| `action.primary-foreground` on `action.primary` | 4.5 |
| `action.secondary-foreground` on `action.secondary` | 4.5 |
| `state.{role}-foreground` on `state.{role}` | 4.5 |
| `border.strong` on `background` | 3 |
| `border.focus` on `background` | 3 |

To fix a failure, move the semantic role one primitive step (for example `text.muted` light from
neutral.600 to neutral.700). Never retune the primitive scale by hand to rescue one pair.

**Score** each area 1 to 10:

- **Tokens:** all colour in OKLCH, eleven steps per scale (neutral adds 0 and 850), constant hue per scale, no page tokens,
  the non-colour families present.
- **Semantic layer:** every required role, both modes for every colour role, semantic values
  point at primitives instead of holding raw values.
- **Contrast:** the table above, both modes.
- **Maintainability:** one source of truth, no copy-paste between the JSON and the CSS, re-runs
  replace a marked block only.
- **Design-tool readiness:** every semantic token has a code name and a design-file name
  (`--color-action-primary` and `Color/Action/Primary`).

For a quick count of components that bypass the tokens, grep for raw palette classes and bracket
values (`bg-blue-500`, `bg-[#…]`). Report the count; hand the sweep to `polish-design-system`.

### 9. Report

```
## Token foundation: <set up | audit>

| Area | Score |
|---|---:|
| Tokens | X/10 |
| Semantic layer | X/10 |
| Contrast | X/10 |
| Maintainability | X/10 |
| Design-tool readiness | X/10 |

Contrast, light: <pair, ratio, pass or fail, one per line>
Contrast, dark: <same>
Gamut clamps: <list, or "none">
Critical issues: <list>
Recommended fixes: <list>
Files written: <list, or "none (audit)">
```

Below 7 overall, recommend fixes before anything is built on top or pushed to a design file. On an
audit, propose the fixes and wait for a yes before you apply any.

## Never

- Hex or HSL in the source of truth.
- A hue that shifts across the steps of one scale.
- A semantic colour with only a light value. Retrofitting dark later is painful.
- A token for one element or one page ("just for this hero gradient"). Use a semantic role or drop it.
- Components that read primitives or raw values directly.
- Different names for the same token in code and in the design file. Fix the name map instead.
- Overwriting hand-written CSS. Merge, or back the file up first and say where.
- Building pages, heroes or marketing sections here. This skill makes the foundation only.
- Contrast numbers you did not compute.

## Red flags: you're about to cut a corner

- "Dark mode can wait for v1." It can't. Map both modes now.
- "These eleven colours look right." Generate the scale; looking right isn't a ramp.
- "The muted text is probably fine." Run the contrast script.
- "I'll just add one more token." Check whether an existing semantic role already says it.
