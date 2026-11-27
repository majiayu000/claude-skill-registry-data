---
name: wensity-typography
description: >-
  Set up and fix typography in web UI: choose and load fonts, build a type
  scale of named roles, set line height, letter spacing, measure and line
  breaks, and style numbers, links and code. Use when creating a page,
  section or component, or when changing fonts, text sizes, hierarchy, line
  height, tracking, text wrapping or font loading in React, Next.js,
  Tailwind CSS or CSS, or when headings or body text look off, cramped,
  generic or hard to read. Skip it for edits that leave text styling
  untouched.
---

# Wensity Typography

Type does most of the work in an interface. Get it right and a plain page
looks designed; get it wrong and no amount of color or motion saves it. This
skill gives you a system to set up once and rules to apply everywhere.

The values below are defaults. If the project already has a type system,
keep it and improve how it is used. Replace it only when asked.

## 1. Choose families

- **One family is usually enough.** A good sans with a real weight range
  covers display, headings, body and UI. Add a second family only for a
  role the first cannot do: a display sans with character for a marketing
  page, or a monospace for code and data.
- **Sans only: no serif and no italic.** Headings, body, quotes and
  captions are all set upright in sans. A serif title or an italic line
  reads as a template costume on a web product, so leave both out even on
  blogs, docs and luxury pages; carry tone with weight, size and spacing.
- **Never more than two families plus a monospace.** A third text family
  reads as indecision.
- **Pick for the subject, not by habit.** Do not put the same face on every
  project. Ask what the product's world looks like in print or on hardware,
  then choose a face with that character:

| The product feels like | Reach for | Free examples |
| --- | --- | --- |
| a precise tool (dev tools, data, infra) | a tight grotesk, mono for data | Geist, Switzer, Onest; Geist Mono, JetBrains Mono |
| calm money or health (finance, insurance, clinics) | a steady neo-grotesk or humanist sans | Inter, Public Sans, Source Sans 3 |
| friendly consumer (social, food, travel, education) | a rounder geometric or humanist sans | Plus Jakarta Sans, Figtree, Nunito Sans, DM Sans |
| a confident brand or startup marketing page | a sans with personality at display sizes | General Sans, Manrope, Bricolage Grotesque, Space Grotesk |
| reading and publishing (docs, blogs, magazines) | a calm sans with a true text cut, tight titles in the same family | Inter, Satoshi, Source Sans 3 |
| fashion, editorial or luxury | a refined display sans set large and tight, titles only | Satoshi, General Sans, Clash Grotesk |

- **Check the face can do the job:** the weights you need (usually 400, 500,
  600), tabular figures, good punctuation, the languages you ship, and a
  variable version if you use several weights.

## 2. Define roles, not sizes

Name text by its job. Components use role names; only the role definition
holds pixel values. Seven roles cover almost every interface:

| Role | Used for | Marketing page | App UI |
| --- | --- | --- | --- |
| `display` | hero headline, one per page | 48 to 80px, weight 600, line height 0.95 to 1.05, tracking -0.03em to -0.04em | rarely used |
| `title` | page and section headings | 32 to 44px, weight 600, line height 1.1, tracking -0.02em | 20 to 24px, weight 600, line height 1.25, tracking -0.01em |
| `heading` | card, panel and subsection headings | 20 to 24px, weight 600, line height 1.25, tracking -0.01em | 15 to 16px, weight 600, line height 1.4 |
| `body` | paragraphs | 16 to 18px, weight 400, line height 1.55 to 1.65 | 14 to 15px, weight 400, line height 1.5 |
| `label` | buttons, inputs, nav, table headers | 14 to 15px, weight 500, line height 1.3 | 13 to 14px, weight 500, line height 1.3 |
| `caption` | helper text, metadata, timestamps | 13 to 14px, weight 400, line height 1.45 | 12 to 13px, weight 400, line height 1.4 |
| `code` | inline code, code blocks, IDs | 0.9em of the surrounding text, mono | same |

Rules for the scale:

- **Steps must be obvious.** Neighboring roles differ by at least about 20%
  in size, or by a size step plus a weight step (14px 500 label over 13px 400
  caption is fine; 15px 400 next to 16px 400 doing different jobs is not).
- **A ratio helps, but the table wins.** Marketing pages suit a ratio of 1.25
  to 1.333 between steps; dense app UI suits 1.125 to 1.2. Round to whole
  pixels.
- **Three weights maximum:** regular (400), medium (500) for labels, semibold
  (600) for headings and display. Hierarchy also comes from size, color and
  space, so it does not need five weights. If 600 looks too heavy for a large
  display line, use 500 for display rather than adding a fourth weight.
- **Fluid size only for display and title on marketing pages:**
  `font-size: clamp(2.5rem, 1.5rem + 4vw, 5rem)`. Keep body and UI text fixed
  so dense layouts stay predictable.
- **Body text floor:** 16px on marketing and reading pages, 14px in dense app
  UI. Input text is 16px on mobile, or iOS Safari zooms the page when the
  field is focused.

In Tailwind CSS v4, define the roles once (replace the family names with the
ones you chose):

```css
@theme {
  --text-display: clamp(2.75rem, 1.6rem + 4.2vw, 5rem);
  --text-display--line-height: 1;
  --text-display--letter-spacing: -0.035em;
  --text-display--font-weight: 600;

  --text-title: 2.25rem;
  --text-title--line-height: 1.1;
  --text-title--letter-spacing: -0.02em;
  --text-title--font-weight: 600;

  --text-heading: 1.25rem;
  --text-heading--line-height: 1.3;
  --text-heading--letter-spacing: -0.01em;
  --text-heading--font-weight: 600;

  --text-body: 1rem;
  --text-body--line-height: 1.6;

  --text-label: 0.875rem;
  --text-label--line-height: 1.3;
  --text-label--font-weight: 500;

  --text-caption: 0.8125rem;
  --text-caption--line-height: 1.45;
}
```

Then use `text-display`, `text-title`, `text-body` in markup instead of
`text-[44px]` or a chain of `text-4xl leading-tight tracking-tight`. In
Tailwind v3 put the same values under `theme.extend.fontSize` as
`[size, { lineHeight, letterSpacing, fontWeight }]` tuples.

## 3. Line height and letter spacing

- **Line height goes down as size goes up.** Display 0.95 to 1.05, titles 1.1
  to 1.2, body 1.5 to 1.65, labels 1.2 to 1.35. A 64px headline at line
  height 1.5 falls apart into separate lines.
- **Tight tracking for big text, none for body.** Display -0.03em to -0.04em,
  titles -0.02em, headings -0.01em, body and labels 0. Do not go tighter than
  -0.05em; letters start to touch. Tune by eye for the face you chose.
- **No positive tracking on lowercase body and interface text.** Positive
  tracking only helps all-caps text, and all-caps text should be rare (see
  section 6).
- **Wide lines need more leading.** If body text runs near 75 characters, use
  line height 1.6 or more; at 50 characters, 1.5 is enough.
- **Light text on dark backgrounds looks heavier and tighter.** On dark themes
  add about 0.05 to body line height.

## 4. Measure and line breaks

- **Body text: 60 to 75 characters per line.** Set `max-width: 65ch` on
  paragraphs, not on the whole page. Captions and helper text can run
  narrower.
- **Display headlines: about 12 to 20 characters per line.** A headline
  running across a 1440px screen in one line has no shape. Constrain it with
  `max-width` in `ch` or a container width.
- **Balance headings, pretty-wrap paragraphs:**

```css
h1, h2, h3, .text-display, .text-title { text-wrap: balance; }
p, li, figcaption { text-wrap: pretty; }
```

  Both are progressive: older browsers ignore them. `balance` evens out
  headline lines; `pretty` stops a single word sitting alone on the last
  line of a paragraph.
- **Hand breaks only between phrases**, and check them at every width the
  text renders at. A `<br>` that lands mid-line on a phone is worse than the
  default wrap. Prefer `max-width` over `<br>`.
- **Long words and URLs** in user content need `overflow-wrap: anywhere` on
  their container, or they push the layout sideways on mobile.
- **Truncation is a last resort.** Truncate single-line labels in tight UI
  (`truncate` in Tailwind). If the hidden part matters, make the full text
  reachable by keyboard and touch (a tooltip on a focusable element, an
  expandable row, a detail view); a `title` attribute alone is not enough.
  Never truncate body text or anything the user must read to act.
- **Multi-line clamps** (`line-clamp-2`): keep line height at 1.3 or more on
  the clamped text so descenders (g, y, p) are not cut off. Do not add bottom
  padding inside the clamp; it shows the top of the next line.

## 5. Text color and contrast

- **Three text colors are enough:** primary (headings and body), secondary
  (supporting text, captions, placeholders), and disabled. Define them as
  tokens. Avoid making a fourth by lowering opacity on the fly.
- **Contrast floors (WCAG 2.2 AA):** 4.5:1 for body and small text, 3:1 for
  text 24px and up (or 18.66px bold). Secondary text and **placeholder text
  also need 4.5:1**. Only text in disabled controls is exempt.
- **On dark backgrounds use off-white, not pure white,** for long text
  (around 90 to 94% lightness). Pure white on near-black glares.
- **On colored or tinted surfaces,** tint secondary text toward the surface
  hue instead of using a neutral grey, which looks dirty on color.

## 6. What to avoid

- **Eyebrows and kickers:** small uppercase letter-spaced labels above a
  heading ("FEATURES", "WHY US", "HOW IT WORKS"). Do not use them. They are
  the clearest sign of template UI. If a heading needs context, write a
  better heading.
- **All-caps labels in general,** including small section headings in
  sidebars, settings panels, cards, footers and demo controls. Sentence case
  reads faster; give a small heading weight (500 or 600) and the secondary
  text color instead. Reserve caps for genuine abbreviations (API, URL).
- **Gradient text and one colored word in a headline.** Emphasis comes from
  size, weight and placement, not paint.
- **Italic, anywhere.** Use weight for emphasis, and set quotes upright with
  a rule or a larger size beside them.
- **Serif faces.** Display serifs and text serifs both read as a costume on
  a web product. Pick a sans with character instead.
- **Monospace as decoration.** Mono is for code, data, IDs, keyboard keys
  and numbers in columns. Mono labels on a marketing page are a costume.
- **Centered paragraphs** longer than two lines. Center short headlines and
  single-line CTAs only.
- **Justified text** on the web. Without hyphenation it makes rivers of white
  space.
- **Underlines for anything but links.**

## 7. Numbers, code and data

- **Tabular figures in anything that aligns or updates:** tables, prices,
  timers, counters, stats.
  `font-variant-numeric: tabular-nums;` (Tailwind `tabular-nums`). Without
  it, a counting number jitters sideways as digit widths change.
- **Slashed zero** for IDs and codes where 0 and O can be confused:
  `font-variant-numeric: tabular-nums slashed-zero;`.
- **Align numbers at the end** of table cells (`text-align: end`) so decimal
  places line up. Text columns align at the start.
- **Code:** monospace at about 0.9em of the surrounding text so its x-height
  matches. Inline code gets a subtle background and 0.2em horizontal padding,
  no border. Code blocks get line height about 1.6 and horizontal scroll,
  never wrapping that breaks indentation.
- **Keyboard keys** (`<kbd>`) in the mono face at caption size.

## 8. Links

Underline links inside running text; color alone fails for color-blind
readers. Scope it to prose so navigation lists and buttons are not
underlined (`.prose` is whatever wraps your article or long-form content):

```css
:where(p, td, dd, figcaption, blockquote) a,
:where(.prose, article) li a {
  text-decoration-line: underline;
  text-decoration-thickness: 1px;
  text-underline-offset: 0.2em;
}
```

Navigation, buttons and card links do not need underlines; their position
already says they are interactive.

## 9. Load fonts without layout shift

- **Next.js:** use `next/font` (`next/font/google` or `next/font/local`). It
  self-hosts, preloads and generates a fallback with matching metrics, so
  the page does not jump when the font arrives. Expose it as a CSS variable
  and map the theme font to it with `@theme inline` (so the variable is read
  where it is used, not resolved once at `:root`):

```tsx
// app/layout.tsx
import { Onest } from "next/font/google";
const sans = Onest({ subsets: ["latin"], variable: "--font-brand", display: "swap" });
// <html lang="en" className={sans.variable}>
```

```css
@theme inline {
  --font-sans: var(--font-brand), ui-sans-serif, system-ui, sans-serif;
}
```

- **Optical size:** a face with an `opsz` axis (Inter, Roboto Flex, Fraunces)
  only gets it if you load it: `Inter({ subsets: ["latin"], axes: ["opsz"] })`.
  Keep `font-optical-sizing: auto` so small text gets the sturdier cut and
  large text the finer one.
- **Elsewhere:** self-host WOFF2, `font-display: swap`, preload only the one
  or two files used above the fold, and set `size-adjust`,
  `ascent-override` and `descent-override` on a local fallback face so the
  swap does not shift layout.
- **Load only what you use.** Prefer one variable font file over six static
  weights. Subset to the scripts you ship.

## 10. Rendering details

- `-webkit-font-smoothing: antialiased` on dark themes makes light text look
  less bloated on macOS. Leave light themes at the default.
- Set `::selection` to the brand tint and keep it readable. The browser's
  default blue is a sign the page was not finished.
- Use real punctuation in copy: curly quotes (“ ” ‘ ’), the ellipsis
  character (…), and the multiplication sign (×) in dimensions.
- Respect user settings: size text in `rem`, never block zoom, and check that
  text still fits at 200% text size and with larger letter and line spacing.

## 11. Check before you finish

- [ ] Every text style comes from a named role; no stray pixel sizes.
- [ ] Neighboring roles are clearly different in size, or size plus weight.
- [ ] At most two families plus mono, at most three weights, all loaded.
- [ ] Body text 16px (14px dense UI), inputs 16px on mobile.
- [ ] Paragraphs capped at about 65ch; display lines about 12 to 20 characters.
- [ ] Headings balanced, paragraphs pretty-wrapped.
- [ ] No eyebrows, no gradient text, no colored single word, no serif, no italic.
- [ ] Tabular figures on every changing or aligned number.
- [ ] Text and placeholder contrast passes 4.5:1 (3:1 for large text) in
      every theme.
- [ ] Fonts load with no visible layout shift.
- [ ] Checked at 390px and 1440px with the real copy, longest strings
      included, and at 200% text size.
