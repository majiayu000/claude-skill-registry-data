---
name: charles-color-analysis
description: "Critique the colour of any visual and the palette behind it: graphics meant to wow (posters, hero images, ads, thumbnails, social posts), landing pages and onboarding, and product app screens. Routes by what the visual is for, measures the real colours (60/30/10 area split, lightness structure, hue gaps, chroma, temperature, text contrast, colour-blind views), and writes a ranked critique with exact OKLCH and hex fixes, alternative palette directions and before/after previews. Use when someone asks to critique, analyse, review, check or fix colours or a palette; asks why colours clash, feel off, muddy, washed out, garish, cheap, cold or out of place; asks whether a palette or accent works, or whether someone's colour critique is right; or wants colour feedback on a design, screenshot, website, app or brand."
---

# Colour analysis

A colour critique says what a viewer will feel, proves it with measurements, and gives the exact change that fixes it. An opinion without numbers ("the orange is a bit much") can't be acted on, and a number without a reason ("C 0.21") can't be trusted, so every finding carries both.

Read [references/principles.md](references/principles.md) before the first critique in a session. It holds the reason, the numbers and the fix for every check below.

## 1. Route: what is the visual for?

```
What does this visual have to do?
├── Stop the scroll or sell one idea at a glance: poster, hero art, ad, thumbnail, cover, social post,
│     packaging → GRAPHIC
├── Express a brand, then lead to one action: landing page, marketing site, onboarding, splash, paywall, email → LANDING
│     The image is only the hero or first screen → run it once as GRAPHIC and check its CTA by LANDING's rules.
│     A full page → run it as LANDING, then measure the hero again as GRAPHIC with --crop.
│     Inside a full-bleed hero, GRAPHIC rules win; below it, LANDING rules.
├── Be used again and again to read, find and act: app screens, dashboards, settings, tools, feeds, forms → APP
└── Only colours: a palette, tokens, a brand sheet → PALETTE. Judge it for each route it will live in.
      With no areas given, assume 60/30/10 shares by role and say so, but never judge proportion from your own
      assumption: lay the palette onto a stand-in screen (HTML, rendered with `shot`) and measure that.
```

Route first, because the same colour is right in one place and wrong in another. A 25% neon accent makes a poster; on a settings screen it is noise. A rule taken from the wrong route produces a confident, wrong critique.

| | GRAPHIC | LANDING | APP |
|---|---|---|---|
| Colour's job | one memorable impression; the accent marks the subject | the brand's feeling in the first viewport, then the way to the CTA | reading, finding, state; content brings its own colour |
| 60/30/10 | 60 field, 30 second colour (type, a second field, the subject's body), 10 accent. An accent that is the subject's own colour may take up to 30%, out of the 30 | 60/30/10 in every viewport; the 10 is the CTA plus one highlight | 60 background, 30 surfaces and text (both neutrals), the primary ≤10% |
| Loudest thing | the subject | the hero subject, then the CTA in every viewport | the primary action, the one thing that changed, or the key data |
| Chroma | pop: accent ≥80% of its hue's ceiling. Calm brief: a muted band | surfaces below the hero C ≤0.06; brand-colour blocks allowed | surfaces C ≤0.03; full chroma only on small interactive elements |
| Text floors, APCA \|Lc\| | copy that must be read: 60 small, 45 large; display type may be texture | body 75 (60 at least), CTA labels 60 | body 75 (60 at least), secondary 60, informative icons and borders 30 |
| Freedom | clashes, glow, gradients, neon, when the subject motivates them | colour blocking by section, duotone photos, a colour per onboarding step (same L and C, so the steps read as one set) | none beyond the primary and status colours: consistency beats expression |
| Usual failures | accent small, pale or off the subject; two loud colours; flat digital field; everything mid-grey in value | hero palette that stops at the fold; CTA colour spent on decoration; unrelated section colours; ungraded photos | brand colour on large surfaces; several accent hues; neutrals of two temperatures; pale grey text; meaning carried by colour alone |

Then write one line of intent: "A <route> for <what, for whom>, meant to feel <two or three mood words>; the eye should land on <the subject, offer or CTA>." Take the mood words from the brief, the brand or the category. If there are none, infer them from the content and say they are inferred. When the brief and the design's evident intent disagree (a craft brand drawn as a blockbuster poster), name both, judge against the brief, and give a direction for each. The mood words set the targets ([Mood targets](references/principles.md#mood-targets)) and decide between pop and harmony. In an APP only the table's hue and temperature columns apply: the words choose the primary's hue and the neutrals' tint, and the route's budgets hold.

## 2. Measure

```bash
python3 <skill>/scripts/color.py measure <image> --route graphic|landing|app [--accent COLOUR] [--focus BOX] [--crop BOX] [--scale 2] --out DIR
python3 <skill>/scripts/color.py sample <image> BOX [BOX ...]
python3 <skill>/scripts/color.py palette 'field:#0B1026@60' 'type:#BCD4F2@30' 'accent:#B8F01E@10' --route landing [--grade COLOUR@0.08] --name NAME --out DIR
python3 <skill>/scripts/color.py contrast <text-colour> <surface-colour>
python3 <skill>/scripts/color.py recolor <image> --map FROM:TO [--region BOX] [--grade COLOUR@0.08] [--before ORIGINAL] --out after.png
python3 <skill>/scripts/color.py shot <page.html> --size 1440x900 [--dom --root SELECTOR] --out shot.png
```

- **Arguments.** A colour is hex or `oklch(L C H)`, each colour its own quoted argument. A BOX is `x0,y0,x1,y1`, as fractions of the image (0–1) or as pixels. Always pass `--out` to a scratch folder (the default is the system temp folder).
- **`measure`** prints the palette by area, the **60/30/10 split**, vivid hue peaks, an accent guess, lightness, temperature, the three loudest spots, text contrast per line and flags. It writes `<name>.json` and `<name>.board.png`.
  - When the accent guess is wrong, rerun with `--accent`.
  - Run `--focus BOX` on every CTA and every subject you judge: it ranks that element for loudness and re-reads its label at 3× size, because Vision misses small tracked labels.
- **`palette`** takes roles, which change the checks:
  - `accent`/`primary`/`cta`/`brand` form the accent family.
  - `success`/`warning`/`danger`/`error`/`info` are status colours, kept out of pop/harmony.
  - `content`/`photo`/`product` are content.
  - `peer`/`series`/`tag`/`category` are peers, checked for equal L and C.
  - `text`/`ink`/`label` and `bg`/`field`/`surface`/`card` get contrast printed for every pair.

  Other role names are taken as plain colours. List every colour that appears in quantity, including the subject's shades, or the echo and family checks misfire. It prints the accent's pairs and any flagged pairs; `--all-pairs` prints the rest.
- **`sample`** reads the median colour of a box. Read every designed colour you quote with it. Use it again to compare one patch before and after a fix, because palettes from two `measure` runs don't line up patch by patch.
- **`shot`** renders a local HTML file with headless Chrome: stand-in screens, and HTML mocks of a fix. `--dom` also saves the `dom_colors.js` JSON beside the PNG.
- **Websites and web apps.** Screenshot at 1440×900 and 390×844, and evaluate `scripts/dom_colors.js` in the page with any tool that runs JavaScript in a tab. Set `window.COLOR_ROOT = "<selector>"` first to judge one component and leave out demo chrome; `measure` then crops the screenshot to that component. Save the returned string as JSON and add `--dom file.json`. The DOM gives what pixels can't:
  - exact text/surface pairs at their rendered size, opacity included;
  - gradient-text stops and placeholders;
  - the boundaries of switches, checkboxes, fields and icon-only buttons;
  - coloured shadows (glows);
  - every colour the page paints.

  It can't see emoji, icon fonts or photos; judge those from the screenshot.
- **Open the board and look at it.** The greyscale panel is the value check, the deuteranopia panel is the colour-blind check (protanopia is checked in the flags), and the numbered boxes are the loud spots.
- **The script guesses; you decide.**
  - Its palette and its temperature split mix content (photos, skin, product) with designed colours, and the temperature split ignores neutral fields.
  - Loud spots rank colourful, high-contrast regions, so a dark subject carried by value (roasted beans, a black product) never ranks. Judge such a subject in the greyscale panel, and check that nothing unimportant outranks it.
  - Pixel text contrast is an estimate: off by up to 15 Lc either way, and up to 30 below 1× scale. Vision merges lines across colours (marked `mixed`), misses some small labels and can't see emoji. Confirm every pair you report with `contrast`, on colours read with `sample` or on the designed values.
  - Pass `--scale` (image pixels per CSS px) so text is judged at its real size: 1 for a 1× capture, a design export or a generated image; 2 for retina; 3 for most iPhones; 0.5 for a half-size capture.

## 3. Look before judging

Write these three down before applying any rule:

1. **Where the eye should land**: the subject, the offer or the CTA.
2. **Content or designed.** Content colours (photo, product, skin, food, sky) are facts unless they can be graded or reshot. Designed colours (fields, type, UI, overlays) are the levers. Emoji and icon glyphs are designed in where they go but fixed in colour, and their colour changes by platform. Count content as its own family in the 60/30/10 split.
3. **What each designed colour claims to be**: a material (paper, wood, coffee, stone), a light (sun, neon, glow), print ink, or UI paint. That claim sets how vivid it may be ([Material and light](references/principles.md#6-material-and-light)).

## 4. Walk the checks in order

Note each finding with its numbers. The order is deliberate: a value problem makes hue fixes pointless, and contrast failures outrank taste.

1. **Value.** The greyscale panel must still show the subject, the headline and the CTA. The focal element carries the biggest lightness step in its neighbourhood. In GRAPHIC and LANDING, the designed colours span ≥0.3 in L; text against its surface is judged by contrast, not by this span.
2. **One loudest thing.** Compare the loud spots, and the `--focus` rank of the CTA or subject, with where the eye should land. Two loud spots of different hues (≥45° apart) with similar weight compete, and both lose.
3. **60/30/10.** One family holds 50–70%, the next 20–35%, and the accent 5–15% (the route table gives the exceptions). Two families near equal, or nothing above 45%, means nothing leads. Light accents (L ≥0.85) weigh as much on half the area of dark ones. The accent's own light or haze counts with the accent.
4. **Hue relations.** Measure gaps in OKLCH degrees. Colours ≥90° apart that touch need a second difference: ΔL ≥0.2, or the weaker at ≤60% of the stronger's vividness. Compare vividness rather than raw chroma, so greens and teals aren't let off. Two vivid, far-apart colours at the same lightness vibrate.
5. **Pop or harmony.** The chroma flag says which the palette is: the accent ≥1.8× the next hue family is pop, under 1.5× is harmony, and in between is undecided, which is itself the problem. The flag's band level (quiet, medium, loud) decides calm against playful. A pop accent needs a reason (it is the subject, its light, or the action) and an echo (something nearby in its hue family).
6. **Material and light.** Each colour is no more vivid than what it claims to be. A glow needs a source and a falloff; a coloured shadow is a glow. Surfaces lit by a coloured light take the light's chroma.
7. **Temperature.** The largest designed area sets the temperature, and it matches the promise. Every neutral leans the same way: warm or cool, never both.
8. **Neutrals.** Greys, creams and blacks (C <0.025) lean toward the palette, come from one family, and number three at most. Text on a coloured field is a deep shade of that field's hue or the palette's own ink, never a stray black.
9. **Families, peers and ramps.**
   - Count hue families: GRAPHIC ≤3, LANDING ≤4 plus status colours, APP one primary plus status colours.
   - Peers (tags, chart series, categories, titles of equal rank) share one L and one C.
   - A ramp holds its hue, or moves it one way as it darkens while gaining chroma: warm toward red, cool toward violet, ≤8° a step. It never zigzags.
   - Near-duplicates merge: ΔE <0.035, or <0.02 in an APP, where steps of 0.02–0.07 are normal surface layering.
10. **Text and UI contrast.**
    - Apply the route's floors, plus 15 for text rendered under 12 px.
    - Controls that only their shape identifies (switches, checkboxes, fields, icon-only buttons) need Lc 30 on their boundary.
    - Under APCA, white text passes 60 only on surfaces up to L 0.68, and near-black only from L 0.75. Between those, move the surface. `contrast` prints the move for both the text and the surface.
    - When a move raises the printed vividness by 0.1 or more, lower C with it. A darkened colour gains vividness against its lower ceiling, and a lifted full-chroma colour turns neon.
11. **Colour-blind safety and meaning.** The accent survives deuteranopia (ΔE ≥0.07 against its field). In an APP, nothing is signalled by colour alone.

## 5. Fix

Change one channel per fix, picked by what the finding says:

```
What is wrong?
├── It can't be read or seen, or it is flat in greyscale → move L
│     (the smaller element; move the surface when it sits between L 0.68 and 0.75)
├── It is too loud, out of place or synthetic for what it claims to be → lower C (keep L and H)
├── Two lights, wrong mood, or a temperature clash → turn H 10–25°, or grade the whole design 5–10% toward one colour
└── Nothing leads, or the accent is too big or too small → change areas (crop, scale, what carries the colour), not colours
```

Change two channels only when the finding names two problems.

- Give exact values as OKLCH and hex, and check them with `palette` or `contrast` before writing them down.
- Preview the top two fixes.
  - **Images:** use `recolor`.
    - `--region` confines a change to one box. For several boxes, chain runs and pass `--before` with the original.
    - `--lwin` (0.15–0.35) keeps nearby shades of the same hue out; check the soft edges after.
    - Widen `--range` when anti-aliased edges keep a fringe.
    - `--grade` previews the one-light fix.
    - `recolor` only moves colours that are already there. For a change of shape (filling a button, adding an element), mock it in HTML with `shot`, or composite it.
  - **Web UI:** inject CSS overrides into the live page and re-screenshot. It is truer than recolouring pixels, because a recolor moves every pixel of a hue, labels and anti-aliasing included.
  - **Palettes:** re-render the stand-in screen with each palette.
- When the intent is unclear, or a fix costs something the design may want, give 2–3 directions, each a full measured palette, picked from: keep the pop and make it belong, go harmonious, or move the accent. When the accent is the subject's own colour in a photo, keep it in every direction. Say what each direction costs.
- Never fix by adding a colour, and never fix contrast by raising chroma.
- In GRAPHIC, fix a weak accent by committing harder (bigger, purer, on the subject), never by toning it down. In APP, take colour away before adding any.

## 6. Write the critique

Open with the intent line in italics. Then:

**Verdict:** two sentences: what the colour does well, and the biggest problem. If the person asks whether someone else's critique is right, add a short point-by-point answer right after it: agree, disagree or partly, each point with a number.
**Keep:** 1–3 things that work and why, so the fixes don't break them.
**Fix:** ranked by impact, as many as there are real problems (1–6). Each one: what you see (with numbers) → why viewers feel it (the principle, in plain words) → the exact change → what it costs. Anything that stops people reading or operating comes first: copy that must be read, or a control, under its floor. A failing minor caption may sit below a problem that changes the whole read; say why in one clause.
**Directions:** optional, 2–3 palettes with hex and one line each.
**Numbers:** a compact table of colour, role, area share and OKLCH, plus the contrast pairs you quote.

Write in plain words. The first time, say "lightness (value)" and "chroma (how pure the colour is)". Say "complementary" only with the OKLCH gap in degrees and which wheel you mean, because OKLCH puts yellow opposite blue while the painter's RYB wheel puts orange there. When APCA and WCAG disagree on a pair, give both and say which one you judged by and why.

Weak and strong findings:

- Weak: "The colours clash." Strong: "The red badge and the green button sit 140° apart at almost the same lightness (L 0.62 and 0.64), both near full chroma, so their edges shimmer and neither leads. Darken the green to oklch(0.48 0.15 150) #1F7A43. The pair becomes a light/dark step, the button still reads green, and the badge stays the loudest thing, which is right because it is the alert."
- Weak: "Use a warmer palette." Strong: "The field is a cold grey-blue (oklch 0.92 0.02 250), while every photo is warm wood and skin (H 50–70), so page and pictures look lit by two different lights. Warm the field to oklch(0.93 0.018 75) #F1EADF and grade the photos 6% toward it. It's the same calm, under one light. It costs a little of the 'clean tech' feel."

## 7. Check before sending

- Every finding has numbers, a reason and an exact fix, or is an explicit "keep". The fix list holds only real problems, with nothing added to reach a count.
- Every contrast pair you report was confirmed with `contrast`, not read off the pixel estimate.
- Every rule you applied belongs to the visual's route.
- Every colour you quote was read with `sample` or comes from the design's own values.
- Every area claim comes from a measured image or stand-in, not from a hex list or an assumed share.
