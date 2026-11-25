---
name: pitch-deck
description: Make an investor pitch deck (startup or VC fund) as one HTML file from a one-line prompt, at top-seed-deck quality. Covers finding the company's design system, headline rules, the slide grid, spacing, logos and visual clarity. Use for pitch decks, seed decks, fund decks, investor slides.
---

# pitch-deck

The bar: a partner flips through it in 60 seconds and gets the whole argument from the headlines and the
pictures alone. Work in this order, in one pass: **gather → facts → headlines → design system → one
picture per slide → build → check.** One Write of `deck.html`, Read it back once, fix with Edit.

## 0. Gather real material first (half of a great deck is real material, not design)

Before writing anything, collect what is real. Generic boxes are what you draw when you know nothing.
- If the prompt names a site, URL, repo or file, read it (WebFetch, Read). If it names a real company you
  can look up, fetch its homepage. Take from it: the exact product name and one-liner, what the product
  literally does on screen (the command, the screen, the output), the integrations or customers it names,
  its real colours, fonts and logo shape (look at the CSS: `--` variables, `font-family`, theme colours).
- The brand lives in the stylesheet, not the page text (WebFetch drops `<link>` tags, so never guess a
  CSS path). With a shell, run exactly:
  `curl -sL <site> | grep -oiE '<link[^>]+stylesheet[^>]*>|<link[^>]+icon[^>]*>|fonts.googleapis[^"]*'`
  then for each stylesheet `curl -sL <css-url> | grep -oE -- '--[a-zA-Z0-9-]+:[^;]{2,60}|font-family:[^;]{2,80}' | head -80`.
  Without a shell, WebFetch the CSS URLs found in the page source. Map the variables onto §3 tokens
  (paper/background, surface, ink/text, muted, brand/accent colour, accent-soft) and write the mapping
  with its source URL in the brand comment. Never guess a palette for a company whose site you could read.
- **Brand = what the homepage renders, not every variable in the CSS.** Stylesheets carry dozens of
  colours (dark mode, unused themes, third-party widgets); the brand is what a visitor sees. Decide it from:
  the page background (`<body>`/`<html>`), the colour of the main call-to-action button in the hero
  ("Try", "Get started", "Sign up", "Start"), the hero headline's colour and font, and `<meta name=theme-color>`.
  If a headless browser is available (`python3 -c 'import playwright'` succeeds), read these from the render:
  `python3 - <<'PY'
from playwright.sync_api import sync_playwright
J="()=>{const c=e=>getComputedStyle(e);return {bg:c(document.body).backgroundColor,theme:(document.querySelector('meta[name=theme-color]')||{}).content,cta:[...document.querySelectorAll('a,button')].filter(e=>{const b=e.getBoundingClientRect();return b.top<900&&b.width>60&&b.height>28&&c(e).backgroundColor!='rgba(0, 0, 0, 0)'}).slice(0,5).map(e=>[e.innerText.trim().slice(0,20),c(e).backgroundColor,c(e).color]),h1:[...document.querySelectorAll('h1,h2')].slice(0,2).map(e=>[c(e).color,c(e).fontFamily.slice(0,40)])}}"
with sync_playwright() as p:
  b=p.chromium.launch();g=b.new_page(viewport={'width':1440,'height':900});g.goto('<site>');g.wait_for_timeout(2500);print(g.evaluate(J));b.close()
PY`
  Without one, find the hero CTA in the HTML (`curl -sL <site> | grep -oiE '<(a|button)[^>]*>[^<]{2,30}' | head -20`)
  and resolve its class or inline colour in the CSS. paper = page background; accent = the CTA colour when it
  is saturated, else the most saturated colour used on the hero (headline highlight, logo); display font = the
  hero headline's font. Write each token with where it came from (`accent #2f6bff = "Get started" button`).
- Real brand beats invented brand: when the company has a site, its deck uses the site's own palette,
  fonts and tone. §3 is only for companies with no site.
- Write the material as an HTML comment `<!-- material: ... -->` at the top of deck.html: product verbs,
  named tools/partners, the on-screen moment to draw, brand tokens with their source.
- The product slide draws THAT on-screen moment as a faithful HTML mock (the real command, the real
  output words), not a generic dashboard.
- **Logos are the third brand win (with fonts and colours): real marks, never plain names.** Harvest them
  from the site itself first, because the site already ships the exact files:
  `curl -sL <site> | grep -oiE '<img[^>]+>' | grep -viE 'avatar|photo|\.jpe?g' | head -60`
  For each logo note its file URL (make it absolute: `<site origin>/<src>`), its alt text, and the label the
  site puts next to it ("Works with", "Used at", "Backed by", "Customers"). Copy that label exactly; never
  upgrade it (a "used at" row is not "backed by"). Also take the company's own mark: the header logo or the
  favicon SVG from the `<link rel=icon>` you already found, and use that file as `<img>` in the footer and
  cover instead of redrawing it.
- Named tools the site has no file for: `https://cdn.jsdelivr.net/npm/simple-icons@13.21.0/icons/<slug>.svg`
  (lowercase slug, e.g. claude, anthropic, openai, github, slack, notion, stripe).
- **Verify every logo URL before using it:** `curl -s -A Mozilla/5.0 -o /dev/null -w '%{http_code} ' <url>`;
  only 200s go in. A name with no verified file is written as a wordmark in the ink colour. Write the verified
  list in the material comment (`logos: Name=url (label)`).
- Show the logos where they argue: the cover row (P1), and on the product slide wherever the product meets
  those tools (the session window's app icon, the "runs in" line). 3-6 logos, 2.2-3cqw tall, one row,
  never recoloured into the accent.
- **Real imagery beats drawn imagery.** From the same `<img>` list, also keep the site's large product
  screenshots, hero art and illustrations (png/webp/jpg/svg, not avatars or tiny icons; check with
  `curl -sI` that each is 200 and over ~20 KB). Use one where it is the truth of a slide: the product slide
  shows the real screen as a framed picture, the cover or close can carry the hero art. Never more than one
  photo-like image per slide. Skip images that only read on the website: faint, animated or
  mostly-white SVG backgrounds vanish at slide size; then draw the picture instead. Write them in the material comment (`images: url (what it shows)`).
- Facts still come only from the prompt and the fetched pages; never fill gaps from memory.

## 1. Facts

- Use only the numbers, names and claims in the prompt. Never invent a raise, use of funds, runway,
  customers, logos, quotes, team, dates, competitors, market size, growth history or time savings.
- Derived arithmetic is allowed if the inputs are shown (`$120k ARR = $10k MRR × 12`).
- No ask given → the last slide says "Raising our seed round." (fund: no ask line at all).
- No universal words ("every", "all", "only") beyond what the facts cover. A missing number beats a weak one.
- Never print an email, a person's name or anything from the environment unless it is in the prompt.
- **Claims vs. product mocks.** Headlines, ledes, captions, diagram labels and bottom lines use only the
  prompt's numbers: never "36 months average", "6-month rollout", "50-person team", "14.2% loss".
  A **product mock** (a drawn screen of the product: a table, a feed, an inbox) may show realistic sample
  rows ("ACH 10/24 — $4,180.00", "Ethiopia Yirgacheffe · 220 kg") because that is what the product
  displays. Every mock is written exactly as
  `<div class="mock" data-mock> …rows… <div class="cap" style="font-size:1.2cqw">example data</div></div>` (the `data-mock`
  attribute is mandatory; a checker reads it). Nothing outside a `data-mock` element may contain an
  unsourced number, and that includes IDs and codes ("SKU #4471", "ETH-0922", "row 14", "10/24"):
  outside a mock, name things in words.

## 2. Headlines (the deck IS the headlines)

Before any HTML, write the headlines as a list and fix them:
- Each is a **full-sentence claim with a contrast or a number**, disputable, max ~60 characters per line,
  max 2 lines. Patterns: *old way. new way.* / *X does A. Y does B.* / *number + what it means*.
  Pattern examples (fictional, shape only, never reuse the words): "It's not a model problem. It's an
  ingestion problem." · "Clinics book by phone. Ours books itself between visits." ·
  "With Tally, a team closes the month in 2 days. Without it, 11."
- Never a topic label ("Problem", "Our solution", "Traction", "Team").
- **Headline-only test:** read them in a row as one paragraph. It must argue the whole raise.
- Name the one belief an investor holds that kills this deal ("roaster software is a tiny niche") and
  make sure one slide breaks it.
- After the product, every slide argues why this gets **bigger** (a loop, a network, a market), never more features.
- Self-score each headline 0-10 on: big, contrarian, first-principles, simple. Rewrite anything under 8.
- Open with the shift the company rides, never by insulting the reader's current tools.

Default 5-slide arc: **shift/claim → gap (the structural reason it is unsolved) → mechanism (how this
company closes it, next to the old way) → proof (the given numbers) → close.** The close is one
sentence on why it compounds plus the ask, in the §7 close layout, with no diagram. A loop diagram gets
its own slide only in decks of 6+ slides; never put a diagram and the ask on one slide.
Fund: thesis → what founders lack → how the fund works → portfolio facts → close (what a founder gets).
More slides: add loop, product (real UI mock), traction, model, team, between proof and close.

## 3. Design system: find it in the company's world

The brand decides whether the deck looks like a real company in 5 seconds. Decide it before any slide.
If the prompt gives a URL or a real company you know, use their real fonts, colours and logo shape.
Otherwise invent the brand this company would have, from ITS world, not from a deck template.

First write an HTML comment `<!-- brand: ... -->` answering in one line each: what does this company's
truck / packaging / invoice / office wall look like? Which 3 materials or objects belong to its trade?
Then derive these and nothing else. A company with a real site keeps its real fonts and colours exactly
(even Inter, even a plain palette): the lists and bans below apply only when you invent a brand.

- **Display face with character** (headlines, cover, KPI numbers) from Google Fonts, picked by the trade:
  - industrial, hardware, climate, logistics: Archivo (wdth 112-125), Barlow Condensed, Familjen Grotesk, Chivo
  - finance, accounting, legal-ish B2B: Newsreader, Libre Caslon Display, Fraunces (bookkeeping heritage),
    or a grotesk with a distinctive cut (Archivo Narrow, IBM Plex Sans Condensed)
  - infra, security, data, dev tools: Geist, JetBrains Mono for display, Schibsted Grotesk, Space Mono
  A neutral grotesk on a neutral ground is a template, whatever its name: give the brand one thing a
  person would remember (the serif, the ledger-rule texture, the stamp, the condensed caps).
  - food, craft, consumer goods, hospitality: Bricolage Grotesque, Fraunces, Young Serif, Roboto Slab
  - bio, health, science: Newsreader, Source Serif 4, Literata
  - VC fund, editorial, legal: Instrument Serif, Gloock, Libre Caslon Display
  - marketplaces, social, playful consumer: Unbounded, Rubik, Darker Grotesque
  Never use Inter, Manrope, IBM Plex Sans, Instrument Sans, Figtree, Poppins or Space Grotesk as the
  display face. Text face (ledes, labels, mocks) may be a plain sans that pairs with it. Set
  `--display`, `--sans`, and `--hw` (headline weight that suits the face, e.g. 700 for condensed,
  400 for serifs).
- **Ground** from the world: light, dark or saturated. Kraft brown for a roaster, bank navy for finance,
  forest or night for climate, lab white for bio. Cream/off-white only if the trade really lives on paper.
  Define `--paper` (ground), `--surface` (panels, one step lighter/darker), `--fold` (muted panels),
  `--ink`, `--muted` (both with the ground's hue, contrast ≥ 4.5:1 on paper).
- **One accent** (`--accent`, `--accent-soft`) from the trade's materials. It marks only the new/winning
  element and the key phrase. The old way is always ink or muted.
- **One shape language**, used on every slide: corners (0 for industrial/finance, 4px for tools, 999px for
  consumer), one line weight, one CSS-only texture or marker (ledger rules via repeating-linear-gradient,
  a stamp circle, contour lines, a grid dot). Cover object, units and panels all follow it.
- **No borders anywhere.** Depth = fill steps; on light grounds add one soft shadow
  `0 1px 2px rgba(0,0,0,.06), 0 14px 34px -22px rgba(0,0,0,.28)`; on dark grounds no shadow.
- No gradients on type, no glow, no emoji, no icon fonts, no stock-icon cards.
- Swap test: if this deck's fonts and colours could belong to any other startup, choose again.

## 4. The slide system (copy this CSS verbatim, then add the parts you use)

Everything is in `cqw` (1cqw = 19.2px at 1920 wide). This is the grammar of a deck that raised a top
seed round; only the tokens from §3 change per company.

```css
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--sans);-webkit-font-smoothing:antialiased}
.slide{position:relative;width:100%;aspect-ratio:16/9;container-type:inline-size;overflow:hidden;background:var(--paper)}
.in{position:absolute;inset:0;padding:5.4cqw 5.4cqw 7cqw;display:flex;flex-direction:column}
.foot{position:absolute;left:5.4cqw;right:5.4cqw;bottom:2.6cqw;display:flex;justify-content:space-between;align-items:center;font-size:1.2cqw;color:var(--muted)}
.foot .mk{display:flex;align-items:center;gap:.6cqw;color:var(--ink);font-family:var(--display);font-size:1.45cqw;letter-spacing:-.03em}
.label{font-size:1.2cqw;color:var(--muted);margin:0 0 1.4cqw;letter-spacing:.01em}
h1,h2,h3{font-family:var(--display);font-weight:var(--hw);margin:0;text-wrap:balance;color:var(--ink)}
h1{font-size:6.4cqw;line-height:1.03;letter-spacing:-.045em;max-width:12.5ch}
h2{font-size:4.1cqw;line-height:1.07;letter-spacing:-.04em;max-width:26ch}
p{margin:0}
.lede{font-size:1.75cqw;line-height:1.4;color:var(--muted);max-width:42ch;margin-top:1.8cqw;text-wrap:pretty}
.a{color:var(--accent)}
.stage{flex:1;min-height:0;display:flex;align-items:center;margin-top:2.4cqw}
.stage>svg{display:block;width:100%;height:auto;max-height:100%}
.card{background:var(--surface);border-radius:1.2cqw;box-shadow:var(--shadow)}
.num{font-family:var(--display);font-variant-numeric:tabular-nums;letter-spacing:-.055em;line-height:1}
```
`--shadow`: `0 1px 2px rgba(0,0,0,.06),0 14px 34px -22px rgba(0,0,0,.28)` on light grounds, `none` on dark.
Type scale, never smaller: label/foot/captions 1.2cqw (23px), body 1.45cqw, sub 1.75cqw, h2 4.1cqw,
cover h1 6.4cqw, big numbers 5cqw. Every content slide: label + h2 (+ optional one-line lede) top-left,
ONE part in `.stage`, footer = wordmark left, page number right. No borders anywhere.

## 5. Parts (pick one per slide; never the same part twice; fill with this company's real words)

### P1 · cover
```html
<section class="slide s-cover"><div class="in" style="justify-content:center;padding-bottom:5.4cqw">
  <h1>{the shift as a claim, ≤ 8 words}</h1>
  <p class="lede" style="max-width:30ch">{what the company is, one sentence}</p>
  <div style="display:flex;align-items:center;gap:1.6cqw;margin-top:4cqw;flex-wrap:wrap">
    <span style="font-size:1.2cqw;color:var(--muted)">{Works with | Built for | Backed by}</span>
    {3-6 × <span style="display:inline-flex;align-items:center;gap:.6cqw;font-size:1.3cqw"><img src="{verified logo url}" alt="{Name}" style="height:2.2cqw;width:auto">{Name}</span>}
  </div>
  <svg style="position:absolute;right:5.4cqw;top:50%;transform:translateY(-50%);width:36cqw;height:36cqw" viewBox="0 0 400 400">{the cover object: the claim in one drawing, ≥ 8 shapes, one accent detail}</svg>
</div><div class="foot"><span class="mk">{mark svg}{Name}</span><span>{domain or nothing}</span></div></section>
```
The row only lists names the prompt or the fetched site mention (integrations, customers, partners), with the site's own label and verified logo files.
No names → drop the row. Keep the h1 column clear of the object (h1 max 12.5ch).
The logo row is ONE line: at most 5 logos, all inside the text column, never wrapping, never under the
picture or into the footer. More customers → the proof slide gets the logo wall.

### P2 · fan-in: many → few (the shift, the gap, a market converging)
Left: 4-6 pills (who/what), right: 2-3 cards (where it all goes); the winning card in accent.
```html
<div class="stage"><svg viewBox="0 0 1000 440">
  <!-- pill i at y = 40 + i*72 (i = 0..5); card j at y = 110, 220, 330 -->
  <!-- one curve per link: --> <path d="M290 {yi} C 500 {yi}, 520 {yj}, 700 {yj}" fill="none" stroke="var(--fold)" stroke-width="1.7"/>
  <!-- pill: --> <rect x="20" y="{yi-28}" width="270" height="56" rx="28" fill="var(--surface)"/><text x="48" y="{yi+9}" font-size="25" fill="var(--ink)">{name}</text>
  <!-- card: --> <rect x="700" y="{yj-38}" width="270" height="76" rx="16" fill="var(--surface)"/><text x="732" y="{yj+11}" font-size="31" fill="var(--ink)">{name}</text>
  <!-- winning card: fill var(--accent), text #fff; its curves stroke var(--accent) width 2.4 -->
</svg></div>
```
Names ≤ 16 characters (pill text is 25 units). Use `font-family` = var(--sans) on the `<svg>`.

### P3 · three columns, the last one breaks (everyone does X, here it fails)
```html
<div class="stage"><div style="display:grid;grid-template-columns:repeat(3,1fr);gap:2.4cqw;width:100%">
  <!-- column ×3; the third gets background:var(--accent-soft) and accent text -->
  <div style="display:flex;flex-direction:column;gap:1.2cqw">
    <p style="font-size:1.45cqw">{column head}</p>
    <div style="background:var(--fold);border-radius:1.2cqw;padding:1.6cqw;display:flex;flex-direction:column;gap:1cqw;align-items:center">
      <div style="display:flex;gap:.8cqw;flex-wrap:wrap;justify-content:center">{2-4 × <span style="background:var(--surface);border-radius:999px;padding:.6cqw 1.2cqw;font-size:1.25cqw">{chip}</span>}</div>
      <svg width="2cqw" height="4cqw" viewBox="0 0 20 40"><path d="M10 2V36M3 29l7 8 7-8" fill="none" stroke="var(--ink)" stroke-width="2.4" stroke-linecap="round"/></svg>
      <div style="background:var(--ink);color:var(--paper);border-radius:1cqw;padding:1.2cqw 2cqw;font-size:1.45cqw;width:100%;text-align:center">{where it ends}</div>
    </div>
  </div>
</div></div>
<p style="font-size:1.2cqw;color:var(--muted);text-align:right;margin-top:1cqw">{one lowercase caption under the breaking column}</p>
```
All three columns share the same rows, so the eye compares them line by line.

### P4 · the product moment (what the product literally does, on screen)
```html
<div class="stage" style="display:grid;grid-template-columns:7fr 5fr;gap:4.4cqw;align-items:center">
  <div class="card" style="overflow:hidden" data-mock>
    <div style="display:flex;align-items:center;gap:.5cqw;padding:1.1cqw 1.4cqw;background:var(--fold)"><i style="width:.8cqw;height:.8cqw;border-radius:50%;background:var(--paper)"></i><i style="width:.8cqw;height:.8cqw;border-radius:50%;background:var(--paper)"></i><i style="width:.8cqw;height:.8cqw;border-radius:50%;background:var(--paper)"></i><span style="margin-left:1cqw;font-size:1.2cqw;color:var(--muted)">{the real app or screen name}</span></div>
    <div style="padding:1.8cqw 2cqw 2.2cqw;display:flex;flex-direction:column;gap:1.25cqw;font-size:1.25cqw;line-height:1.5">
      <p style="background:var(--paper);border-radius:.8cqw;padding:.9cqw 1.2cqw;font-size:1.4cqw;align-self:flex-start">{what the user types or does}</p>
      {2-4 rows: <div style="display:grid;grid-template-columns:1.4cqw 1fr;gap:.6cqw;color:var(--muted)"><span style="width:.8cqw;height:.8cqw;border-radius:50%;background:{var(--accent) for the product's own step, var(--muted) otherwise};margin-top:.6cqw"></span><div><b style="font-weight:500;color:{var(--accent)|var(--ink)}">{action}</b> {detail}</div></div>}
      {the result, once: <div style="background:var(--accent-soft);border-radius:.7cqw;padding:.8cqw 1cqw;color:var(--ink)">{the output}<small style="display:block;color:var(--muted);font-size:1.2cqw">{why it is right}</small></div>}
      <p style="font-size:1.2cqw;color:var(--muted)">example</p>
    </div>
  </div>
  <div style="display:flex;flex-direction:column;gap:1.3cqw">
    {3 × <p style="display:grid;grid-template-columns:2.6cqw 1fr;gap:1cqw;align-items:baseline;font-size:1.7cqw;line-height:1.35"><span style="font-size:1.2cqw;color:var(--accent)">{1|2|3}</span><span>{step in plain words}</span></p>}
  </div>
</div>
```
The rows are the real product verbs from the gathered material (a command, a call, a click), never
"Step 1: Onboarding".

### P5 · before vs after in units (a result with a count: "4 of 20", "11 of 12")
```html
<div class="stage" style="flex-direction:column;align-items:stretch;justify-content:center;gap:3.6cqw">
  <!-- row ×2: first the old way (marks in var(--ink)), then the new way (marks in var(--accent)) -->
  <div style="display:grid;grid-template-columns:22cqw 1fr 12cqw;gap:3cqw;align-items:center">
    <p style="font-size:1.75cqw;line-height:1.3">{who}<span style="display:block;color:var(--muted);font-size:1.45cqw;margin-top:.4cqw">{condition}</span></p>
    <div style="display:grid;grid-template-columns:repeat({N},1fr);gap:.7cqw">{N × <i style="aspect-ratio:1;border-radius:.5cqw;background:{lit ? colour : var(--fold)}"></i>}</div>
    <p class="num" style="font-size:5cqw;text-align:right">{k}<small style="font-size:1.7cqw;color:var(--muted)">/{N}</small></p>
  </div>
  <!-- optional band with one more given number: -->
  <div style="display:flex;align-items:baseline;gap:2cqw;background:var(--accent-soft);border-radius:1.2cqw;padding:1.6cqw 2.4cqw">
    <span class="num" style="font-size:4.4cqw;color:var(--accent)">{value}</span><p style="font-size:1.75cqw">{what it means}</p></div>
</div>
```
N ≤ 30 per row. One row only when there is no "before" (then the lit subset is the contrast).

### P6 · growth: bars + KPI column (only when the prompt gives at least a start and an end value)
```html
<div class="stage" style="display:grid;grid-template-columns:7.6fr 4.4fr;gap:4cqw;align-items:center">
  <svg viewBox="0 0 900 420"><!-- one bar per GIVEN value only; never invent the points in between.
    Two values → two bars (start, now) with the multiple between them. Bar width 160, rx 12,
    height ∝ value, baseline y=380; earlier bars var(--fold), the last bar var(--accent);
    value above each bar at font-size 34, period label below at 24 in var(--muted). --></svg>
  <div style="display:flex;flex-direction:column;gap:2.4cqw">
    {2-3 × <div><div class="num" style="font-size:5.2cqw">{given or derived-with-inputs value}</div><p style="font-size:1.45cqw;color:var(--muted);margin-top:.6cqw">{what it is}</p></div>}
  </div>
</div>
```

### P7 · once vs every time (a business model, a per-use economy, one-off vs recurring)
```html
<div class="stage" style="display:grid;grid-template-columns:1fr 1.5fr;gap:1.6cqw;align-items:stretch">
  <div class="card" style="padding:2.2cqw 2.4cqw;display:flex;flex-direction:column;gap:1.4cqw">
    <div class="num" style="font-size:3.4cqw">{Sells once}</div>
    <div style="flex:1;display:flex;align-items:center"><div style="width:8cqw;height:8cqw;border-radius:.8cqw;background:var(--ink);color:var(--paper);display:flex;align-items:center;justify-content:center;font-size:1.2cqw">{one unit}</div></div>
    <p style="font-size:1.45cqw;color:var(--muted)">{the old unit, sold once}</p></div>
  <div style="background:var(--accent);color:#fff;border-radius:1.2cqw;padding:2.2cqw 2.4cqw;display:flex;flex-direction:column;gap:1.4cqw">
    <div class="num" style="font-size:3.4cqw">{Sells every use}</div>
    <div style="flex:1;display:grid;grid-template-columns:repeat(18,1fr);gap:.55cqw;align-content:center">{54 × <i style="aspect-ratio:1;border-radius:.35cqw;background:#fff;opacity:.9"></i>, every 3rd opacity .6}</div>
    <p style="font-size:1.45cqw;opacity:.85">{the new unit, sold every time}</p></div>
</div>
```

### P8 · close (the compounding picture, never text alone)
The close is the headline plus ONE picture of why it compounds, filling the right ~55% of the stage.
Pick what fits this company: (a) a loop: 4 rounded labels on an ellipse with accent arrows between
them (inline SVG, arrows in the accent, labels are this company's own nouns: users, data, supply...);
(b) once vs every: a single dark tile next to an accent panel full of small tiles (one sale vs recurring
use); (c) the site's real hero art. Below the headline: the ask as given, else "Raising our seed round.",
then the domain.
```html
<section class="slide"><div class="in"><div style="display:grid;grid-template-columns:42% 1fr;gap:4cqw;align-items:center;height:100%">
  <div><h2 style="font-size:4.6cqw;max-width:14ch">{why it compounds, <span class="a">key phrase</span>}.</h2>
  <p style="font-size:1.75cqw;color:var(--muted);margin-top:2.4cqw">{ask or "Raising our seed round."}</p></div>
  <svg viewBox="0 0 800 520" style="width:100%;height:auto">{the loop or once-vs-every, labels ≥ 26px in viewBox units}</svg>
</div></div><div class="foot"><span class="mk">{mark}{Name}</span><span>{domain}</span></div></section>
```

### P10 · old way vs new way (the gap as one big pair)
Two panels side by side filling the stage: left on `--surface`, the old way drawn with this company's real
artifacts (the stale docs, the manual steps, the tools that disagree) slightly faded or tilted; right on
`--accent-soft`, the product in the middle feeding or fixing the same things, accent on the product.
One caption line under each panel. Words only in captions (no invented counts or versions).

### P9 · loop (a flywheel as a content slide, when the claim is how it compounds)
Same picture as P8(a) but full stage width: an ellipse of 4 labels ~3cqw tall, accent arrows, the headline above.

## 6. Which part where (default 5 slides)
1 cover → P1 · 5 close → P8. For slides 2-4 choose by what THIS company's claim is, not by habit:
the shift or gap → P10 (old vs new pair), P2 (many sources into one) or P3 (three ways, the last
breaks; only when the company itself names three alternatives) or a before/after of
the real product; the product → P4 or the site's real screenshot framed large; proof → P5 (a count),
P6 (growth), a quote with the customer's logo big, or a logo wall when customers are the proof;
business model → P7; compounding → P9. Two companies with different stories should not get the same
three middle slides. More slides: team, market, ask, each drawn, never a bullet list.

**Scale like a top deck.** The picture on every slide fills the stage: at least 85% of the content width,
or at least 60% of the content height when it sits beside text. Inside pictures: labels and pills
≥ 1.4cqw, card titles ≥ 2.4cqw, big numbers ≥ 6cqw. Empty half-slides are a failure. Bigger must still fit: the stage starts below the headline and ends
above the footer band; nothing in the picture may touch the headline, the footer or the slide edge
(an SVG keeps its outermost labels inside its viewBox).

## 7. Check (Read the file back once, then Edit)
0. Slide count is exactly what the prompt asked (default 5). The `<!-- material -->` and
   `<!-- brand -->` comments exist. Every `<img>` src is an absolute `https://` URL (never a relative
   path like `logos/x.svg`: deck.html is opened on its own) that you verified as 200; the site's logos appear on
   the cover and the product slide; the footer uses the company's real mark file when it has one.
1. Every number on a slide is in the prompt, on the fetched site, or derived with shown inputs;
   product mocks carry `data-mock`.
2. Headlines in a row argue the whole raise; each is a claim with a contrast; no topic labels.
3. Each content slide uses a different part from §5 and the part fills the stage.
4. Every slide's picture fills the stage (see §6 scale); the close slide has a picture. Nothing under 1.2cqw, nothing past the slide edge or into the footer band, nothing overlapping. Pictures too: a window, card or SVG must start below the headline's last line and end above the footer; when it does not fit, shrink the picture, never let it slide under the headline or footer.
5. One accent, used only for the new/winning element and the key phrase. No borders.
6. Same label/headline position on every content slide; footer on every slide.
