---
name: frontend
description: >-
  Work on the dashboard's frontend — the vanilla JS/CSS page with no framework
  or bundler. Use this whenever a task touches `static/nowplaying.js`,
  `static/style.css`, the Jinja templates (`templates/nowplaying.html`,
  `_icons.html`), the accent-color tinting, the karaoke lyrics sync, the
  now-playing poll, or the empty-state mosaic / recent-plays pile. Covers how
  the page is wired, how it reads i18n and data from the server, the ESLint
  gate, and the Android bridge, so changes match the existing patterns.
---

# Frontend (vanilla JS/CSS, no framework)

The page is plain ES5-ish JavaScript and hand-written CSS — **no framework, no bundler, no build step, no npm dependencies**. Two vendored libraries in `static/lib/` (`fast-average-color`, `vibrant`) are loaded via `<script>` tags. Keep it that way: don't introduce a framework, a bundler, or a package.json.

- `static/nowplaying.js` — all page behaviour (~1300 lines, one file).
- `static/style.css` — all styling.
- `templates/nowplaying.html` — the Jinja page. `templates/_icons.html` — reusable inline-SVG icon macros (`{% import "_icons.html" as icons %}`).
- `DEV=1 python app.py` live-reloads templates and disables static caching, so HTML/CSS/JS edits show on a plain refresh (see `config.py`).

The control that resumes the karaoke follow wears `lyrics_sync_icon`, freed when the auto-search switch went: a circular-arrow glyph there read as a second refresh button next to the real one.

Every icon on the page is an inline SVG macro from `_icons.html`, drawn in the same language: a 24px viewBox, `fill: none`, a 2px `currentColor` stroke with round caps, shared by the private `_frame` macro, and a pixel size passed by the caller. Icons are never emoji or characters from an icon font — a Raspberry Pi kiosk running Raspberry Pi OS has no emoji font installed and renders them as tofu boxes.

## Lint gate

ESLint (flat config `eslint.config.mjs`, dependency-free) runs in CI on `static/*.js` (`.github/workflows/web-ci.yml`):

```bash
npx --yes eslint@9 static/*.js
```

Match the existing style: `var`, small named `function`s, `try/catch` around `localStorage`, defensive null checks (`if (!el.retry) { return; }`).

## How the page gets its data

Nothing is hardcoded in the JS that the server already knows:

- **i18n** — the template serializes the chosen-language dict into a `<script id="i18n-data" type="application/json">` block; the JS reads it once as `I18N` and uses `I18N.some_key` for every dynamic string. Never hardcode a display string in JS — add a key in `i18n.py` (both `fr` and `en`) and read it from `I18N`. See the `i18n` skill.
- **Server host** — `document.body.dataset.lyrionHost` (`LYRION_HOST`).
- **Live state** — the JSON endpoints: `/now-playing.json` (polled), `/stats.json`, `/lyrics.json`, `/mosaic-covers.json`, `/recent-covers.json`.
- **DOM handles** — collected once into the `el = { ... }` object by id; reuse those, don't re-query.

## The polling loop

`poll()` fetches `/now-playing.json` every `POLL_INTERVAL_MS` (2000ms) and calls `render(data)`. Two efficiency contracts to preserve when editing:

- The page sends `?known=<track key>` (the `id|title|artist|album` it already shows); the server omits `lyrics` when it matches, so a steady-state poll skips the DB. Keep the key format in sync with the route.
- `?player=<id>` pins the switcher's pick (persisted in `localStorage`); a malformed id is dropped server-side.

`catchUp()` re-syncs after the tab was backgrounded. Stats poll separately (`pollStats`).

`paintProgress` runs on its own 250ms interval, extrapolating the position between network polls (and driving `syncLyrics` while there are lyrics). Both progress bars are animated with `transform: scaleX()`, never `width`: a `width` transition invalidates layout and paint on every frame of its 0.4s run, so the tick repainted the card continuously; scaleX is compositor-only and costs nothing.

## Accent color from the cover

The signature visual: the page samples the cover art (served **same-origin** via `/cover/...` precisely so the canvas isn't tainted) to derive two colors — a **tint** (the average color, `FastAverageColor`) and an **accent** (the dominant vibrant swatch, `Vibrant`, normalized in HSV via `rgb2Hsv`/`hsv2Rgb`: fixed brightness `ACCENT_V`, saturation clamped into `[ACCENT_SAT_FLOOR, ACCENT_SAT_MAX]`, and swatches under `ACCENT_SAT_MIN` — greyscale covers — falling back to `ACCENT_DEFAULT`). `SWATCH_ORDER` sets swatch preference. Vibrant reads its input at its layout size (`width`/`height`, not the natural size) and samples one pixel in five, so it is never handed the `<img>` itself — the same cover would yield a different accent on every screen size. It reads a canvas copy at `COVER_SIZE` (`swatchSource`), the size library covers are fetched at (`?size=`): those are read pixel for pixel, oversized remote artwork is scaled down. `setTint`/`setAccent`/`resetColors` push them into CSS custom properties. If you change how covers are served, keep them same-origin or the tint breaks.

The `body.in-app` header is the one place held out of that tinting: `.lyrion-link` fills the two round buttons with translucent white rather than the accent, so they lift whatever is behind them by a constant amount and drift with the page's own tint. Only the Android app ever shows that bar, and there it is framed by native chrome — status bar, navigation bar, the settings screen, all pinned to `colors.xml` — which cannot follow the cover, so an accent-filled button was the only thing in the frame changing hue per track. Anything visible on the web keeps the accent; the accent's other landing spots (progress, the active line, the switch when on, focus outlines, the stats figures) are unaffected.

`.now-playing` and `.stats-panel` carry no `backdrop-filter`, and should not get one back: the only thing painted behind them is the body's gradient, so blurring it is a visual no-op (flat fills differ by at most 1/255 with the blur removed), while the blur puts each on its own composited layer. That costs a Raspberry Pi its GPU compositing path — where a window covering the output is handed straight to the driver and Chromium's partial updates flash on screen — and makes the software fallback (`--disable-gpu-compositing`) too slow to scroll lyrics. The blur that does real work is `.cover-zoom-frost`, which blurs artwork rather than a gradient.

`html` declares `color-scheme: dark`. Without it the UA paints its light widgets — the page and lyrics scrollbars above all — over the dark page, which is what a Raspberry Pi kiosk shows. `scrollbar-color` tints them from `--tint-color` alongside everything else, and inherits, so the one declaration covers every scroller on the page.

## Fitting the viewport

Two regimes, split at 861px wide. Above it the page itself is the viewport (`html`/`body` at `100dvh`, `overflow: hidden`) and every overflowing region scrolls internally. Below it the page scrolls, because the stats panel wraps under the card — but the card is still fitted to the visible viewport in landscape (`.left-panel` at `100dvh` minus the body gutter), so the lyrics box and the mode row under it are never left off screen. Both work the same way: the card is a grid of `auto 1fr` rows, `.np-lyrics-block` stretches into the `1fr` one, and `.np-lyrics` takes what is left with `flex: 1 1 0` — a basis of `auto` would size it from the synced lyrics' full content height and push the row below out of view. `100dvh`, never `100vh`, which is iOS Safari's *large* viewport. Beside the card, the stats panel is a quarter of the viewport clamped to 320–400px: 320px up to 1280px wide, where the card is already tight, and no wider than 400px so the card keeps the room and a stat's label stays near its figure.

Every cover on the page keeps its artwork's ratio rather than a fixed square; `coverRatio` reads it from the image's `naturalWidth/naturalHeight` once loaded, clamped to `[COVER_R_MIN, COVER_R_MAX]` (0.5–2). The card's `fitCardCover` sets it as `--np-cover-r` on `.np-cover`, and the box is as wide as its slot for a landscape picture, as tall as the slot is wide for a portrait one, centred across the slot — so the slot sizes below are its upper bound. On the stacked layouts (≤1080px) `.np-side` is centred vertically in the first row, so a landscape cover shorter than the meta sits level with its middle; above that the cover keeps its column's top edge, which the pile hangs from. `object-fit: cover` only crops past the clamp. The box hugging the picture is also what keeps the recent-plays pile tucked under its lower edge and the enlarged-cover FLIP starting from the picture itself.

On the stacked layouts the cover is the lever on a short screen: it sets the card's first row, so the ladder shrinks it by viewport height (200px under 1081px wide, 160px under 600px tall, 100px under 500px) and the lyrics take what it gives back. Its floor is the meta beside it, ~94px — shrink past that and the row stops moving. Above 1080px wide the cover spans both rows in a column of its own and the meta sets row one, so it stays full size however short the screen.

## Karaoke lyrics sync

`parseLRC` turns timestamped LRC into `[{time, text}]`; `syncLyrics` (driven off the aged playback `time` from the poll) highlights the current line via `paintLine` and auto-scrolls, unless the user scrolled away (`setAutoFollow`, `updateScrollReset`, the resume-scroll button). Plain (un-timed) lyrics render as static text. The glide between lines is `scroll-behavior: smooth` on the box plus a transition on `.lrc-line`, both dropped under `prefers-reduced-motion: reduce`. In synced mode the box also carries `will-change: transform`, which is what makes that glide affordable: held on its own layer it is rasterised once and the scroll moves the layer, instead of re-rasterising every line on each frame of the animation. Without it the glide costs 481ms of raster over eight scrolls under a software compositor, against 2ms with it — the difference between a Raspberry Pi that can run this page and one that cannot. The web search runs for every track and has no on-screen control: an operator who wants the app to stop calling out sets `LYRICS_PROVIDERS` to an empty value. The display still picks synced over plain on its own, but which version ends up on screen is the user's to change — see the version cycler below.

## Lyrics version cycler

`versions` holds the lyrics available for the current track — the library's own text when it has any, and every upload the web search returned (`webVersions` reads the response's `versions` list, falling back to its single `lyrics`/`synced` pair) — in order of preference: `rankVersions` puts synced versions first, then the library's text, then plain web versions, and remembered-hidden ones last, so the version the page lands on is always `1/n`. `versionIdx` is `versionIdx` is the one on screen (`-1` when none is). Both reset on every track. The source line under the lyrics box (`#np-lyrics-source`) is the control: `updateSource()` renders it, `showVersion()` moves between entries, and a tap advances the index. A retry keeps only the library's entry before searching again, so the new answer never stacks a second copy of the previous one.

`MAX_VERSIONS` (5) is the whole cycle's budget and mirrors the server constant of that name, since only the page knows whether a library text takes one of the places. `rankVersions` trims the tail to fit but never sheds the library's text, so the least useful web version is the one dropped.

A version whose text matches one already in the cycle, to the whitespace, never joins it (`textKey`, `offeredAs`): a provider repeating what the tags already hold, or two uploads of one transcription, would spend a place on a second copy of the same reading. Timestamps count in that comparison, which is what keeps an upload's two forms apart. The provider it came from is named beside the kept version's own source instead (`noteEcho`, `sourceLabel`: `Library + LRCLIB`), so a text the web confirmed never reads like one it could not find; a retry clears those names along with the previous answer.

The chip floats over the lyrics box's lower-**left** corner — the right edge is where a classic scrollbar puts its gutter, which Chromium on Linux reserves and Android does not, so the left side spares the page from measuring it. The box owes the chip `--source-clearance` of bottom padding — including in `lrc-mode`, which otherwise zeroes it. Without that, `scrollTop` clamps with the last line flush to the bottom edge and the chip covers the line being sung at the end of a song; the clearance is a shade wider than the chip's height plus its inset, so a full line of lyrics never rests under it.

One upload often carries both forms, and `webVersions` emits both: an LRC whose timings fit the recording badly is unreadable as karaoke, and its plain text is then the one that reads, so it stays one tap away rather than being weighed against the synced words first. Synced entries are emitted before plain ones, matching the server's order, so the cap keeps trimming the least useful end.

Two rules decide what lands on screen by itself (`landOnVersions`). Synced lyrics take it, since the library's own text is always plain; a plain web version only joins the cycle, as a second opinion on a library text that may be the wrong one, and the text on screen keeps it wherever ranking moved it. The control is a `<button>` that `disabled`s itself into a passive label only while a search runs. Where the box sizes to its text (the scrolling phone layout), a tap holds its height as an inline `min-height` (`holdLyricsHeight`), so a shorter version or the hidden stop never pulls the chip out from under the finger; the hold is released on a track change and on a width change — not a height change, which the mobile URL bar fires on scroll — and skipped in the fitted layouts, whose box takes its height from the viewport (`flex-basis: 0`).

The cycle ends on one more stop past the last version (`lyricsHidden`, `showHidden`), where the chip reads `None (0/n)` — no source, ranked as the stop before the first: the box shows `lyrics_hidden` as an empty state, and the next tap starts over from the first version. It is how a text that matches nothing is cleared without a control of its own, so even a single version can be cycled. Stopping there remembers every version in the cycle, per device, in `localStorage` (`lyrion.hiddenLyrics`, the newest `HIDDEN_LYRICS_MAX`), keyed by artist|title plus a hash of the version's `textKey` rather than the track id, which a rescan renumbers. A track whose versions are all remembered opens hidden (`allHidden`), and ranking puts remembered ones last, so a version found later takes the top and shows by itself. Leaving the stop forgets them.

That label carries four things at once — provenance, length, rank (`1/2`) and the synced/plain indicator (`.is-synced`, the accent tint) — so the chevron, not a colour, is what marks it tappable: on this line the accent already means "synced" and cannot also mean "hover". The length is what tells two uploads of one song apart, album names being too long for the chip. While a search runs the chip says so in place of the source, and the spinner lives in the retry segment beside it rather than inside the chip. Its vertical padding is capped by the row: the switch beside it sets the row's height, and anything taller takes that height off the lyrics box above.

## Enlarged cover

Both lyrics controls share `.np-lyrics-tools`, one pill floating over the box's lower-left corner: the row draws the surface and border, retry and the version chip are segments inside it, parted by a divider that only appears when both show. The row carries a `min-height` of the chip's own 25px, and retry alone drops its side padding for a 23px width (`:has(+ .np-lyrics-source[hidden])`), so on the tracks where it is the whole pill it is a circle rather than a capsule. Retry leads: it is the fixed-width one, so it stays under the finger while the chip's label changes length — the other way round it moved up to 134px between states, and furthest exactly when it had just been tapped on an empty panel. The row hides itself when neither does, or an empty outline is left over the lyrics. Retry is icon-only — a word beside the chip made the pair read as two objects — and its square padding is what centres the glyph. Retry shows whenever a track is playing — an unconvincing text on screen is as good a reason to search again as an empty panel, and with the bar gone this row is the only place left to ask from. It greys out while the server's per-track cooldown would refuse the search, and while a search runs it stays in place, disabled, its icon spinning (`.is-busy`, still under `prefers-reduced-motion`), so the pill never loses a segment mid-search. A search that fails behind the library's text (throttled, unreachable, network error) has no empty panel to say so, so retry turns `--text-error` (`.is-failed`) and puts the reason in front of its title and `aria-label` until the next search starts or the track changes; a search that ran and found nothing is not a failure.

## Enlarged cover

The card's artwork is a button (`#np-cover-button`) opening `#cover-zoom`, an overlay holding the artwork with the track's title/artist/album over its lower edge. It covers `.left-panel` — the now-playing card only, leaving the stats panel readable — and is a sibling of the card rather than a child, because opening fades out the card's own children and the overlay must not fade with them.

There is no close button: a click anywhere on the overlay closes it, as does Escape, and `render()` closes it when playback stops. Focus never leaves the trigger, which carries `aria-expanded`.

The overlay has no surface of its own — the panel keeps its card background, and the card's content is what clears out under it (`.left-panel.is-zoomed .now-playing > *`, faded by `animateCardContent`). On the stacked layouts the overlay drops its padding so the picture runs edge to edge, the same width as the stats panel under it; `--cover-zoom-radius` keeps the picture's corners on the card's.

`.cover-zoom-figure` is sized as the largest box of the artwork's ratio that fits the panel — `--cover-r` (set from the card image's `naturalWidth/naturalHeight`, already decoded when the view opens, and settled again when the enlarged image loads — on a track change the card's copy still carries the previous artwork's dimensions) plus a `100cqh` width off the overlay's container query. The picture fills that box, upscaled when the panel is bigger than the artwork, and the rounded edge, shadow and caption hug the picture rather than a letterboxed box. On the stacked layouts the card grows with the lyrics far past its own width, so `.left-panel.is-zoomed` squares it off.

The caption (`.cover-zoom-meta`) is a plaque hugging its text near the picture's lower edge, not a band across it: absolutely positioned with `width: fit-content` and auto margins. Its tint and its frosting are two layers, stacked under the text by `z-index`: `.cover-zoom-frost` (a span in the template) carries the `backdrop-filter`, and `::before` carries the tint as a rounded box that its own `filter: blur()` feathers, so the plaque has no outline. They stay apart because an engine may drop a `filter` on an element that also has a `backdrop-filter` — the Android WebView does — which cost the plaque its soft edge when one layer carried both. For the same reason the frosting cannot be feathered by a filter, so a radial-gradient mask fades it out inside the tint: unmasked, it shows as a smeared rectangle wherever the artwork under the plaque is lighter or darker than its surroundings.

`paintProgress` paints the playback position into the bar on the artwork's bottom edge along with the card's own, so the two never drift.

Opening is a FLIP: `animateZoom` measures the card cover's box and the enlarged figure's box at run time — the panel's height follows the lyrics, so neither is fixed — and animates the figure from one to the other while the card's content fades out and the caption arrives late; `animateCard` animates the card's height over the same beat so the stats below slide rather than jump. Closing plays it backwards and only then sets `hidden`. Opening fills backwards only (`zoomOpts`): once it ends the enlarged state comes from the stylesheet rather than an animation holding its last frame. Everything is skipped under `prefers-reduced-motion`.

The card shows a 512px thumbnail; the overlay paints that cached thumbnail first and swaps in the original artwork (the same `/cover/` URL without `?size=`) once it has loaded, so it never shows a blank frame.

## Stats panel

Each `.stat-group` folds on a click of its title; collapsed, it hides its `.stat-row`s but keeps its title total and its `.stat-bar`. The completion groups (tracks, albums, both artist counts) carry that bar: one `.stat-bar-seg` per sub row, sized by `flex-grow` from the row's percentage. The CSP refuses inline `style` attributes, so the template ships each percentage as `data-pct` and `paintStatBars` applies it through the CSSOM, on load and after every `/stats.json` poll; a zero segment is `hidden` so it leaves no gap. Each segment's `title` is copied from its legend row (`statBarTitle`), so hovering the bar of a collapsed group still gives the figures. A `stat-level-1`…`stat-level-4` class on both the segment and its row sets `--level-color`, the row's square marker doubling as the bar's legend: the accent for the most played, then 75% and 50% of it mixed into `--nothing`, and `--nothing` itself (near-black) for never played: one scale from black to the accent, shared with the listening calendar.

The History group opens with the listening calendar (`#listening-calendar`) when `/stats.json` carries a `listening_calendar`, hidden otherwise. It ships as JSON in `#calendar-data` and `renderCalendar` rebuilds it — only when the data changed — on load and after each stats poll: one column per Monday-to-Sunday week up to the server's `today`, starting a year back or at the history's `start` when that is younger — though never fewer than `CALENDAR_MIN_WEEKS` (26) columns, which caps the size of a day — `calendar-level-0` (`--nothing`, as for the bars' never-played level) for a day without plays and four shades cut at the quartiles of the days with plays, so they fit each library's pace: 25, 50 and 75% of the accent mixed into `--nothing`, then the accent itself, so a day with no plays is the first step of the scale rather than a hole in it. Days before the history's `start`, only drawn when the history is shorter than that minimum, stay transparent and unlabelled, so they never read as days without music. Month names come from `Intl` in the page's language, from the history's first column on and one every `CALENDAR_LABEL_WEEKS` columns since a month is too narrow for its name in the side panel; each day's `title` carries its date and count. The legend under it follows each shade with its upper bound (`.calendar-bound`): 0, the three quartile thresholds, then the busiest day's count. The expanded strip then keeps only the most recent weeks that fit the box at `CALENDAR_MIN_DAY_PX` (10px) a day — about 26 to 33 in the side panel — measured from the box's width and redrawn on resize, so a year's history never shrinks the days below that. Collapsing the History group swaps it for `.calendar-weeks`, one row with a cell per week of the same span, shaded at the quartiles of the week totals (`calendarWeeks`), and reveals the 12-month figure in the group title (`.collapsed-only`, titled with its label); expanded, the row and the title figure hide again. Below it, a velocity whose `_partial` flag is set (`data-stat-partial`) reads `≥ N` with `velocity_partial` as its title, rendered by the template and kept by `renderStats`.

## Mosaic and recent-plays pile

The empty-state background mosaic (`loadMosaic`/`layoutMosaic`/`stepMosaic`) and the recent-plays sleeve pile (`loadRecent`/`renderRecent`) are decorative, desktop-driven layouts. They pull cover ids from `/mosaic-covers.json` and `/recent-covers.json`.

Both lay covers out in square slots and fit each artwork's ratio inside its slot: a mosaic tile is centred in its belt slot (`--mosaic-r`), and a sleeve is centred across its slot while `stackRecent` re-hangs the whole pile on every load, each sleeve overlapping the one above by `RECENT_OVERLAP` of that one's real height. The pile's fit loop sizes it for squares, the tallest case, so a pile of wide covers ends shorter rather than overflowing.

The mosaic's belt **steps rather than flows**: one cover every `MOSAIC_STEP_MS`, glided by the tiles' CSS transform transition, and nothing scheduled in between. Continuous motion is what costs — every frame recomposites the whole backdrop, a full core against 2.7% for a still collage — and the cost scales with the step rate, so that constant is the only knob worth turning. A cover only ever glides one slot along its row; anywhere the belt is discontinuous it is placed outright, which stays invisible because those breaks are all off the card.

## Measuring the page

Two traps, both of which quietly yield wrong numbers rather than an error:

- The app's `CSP default-src 'self'` blocks a `<style>` injected at runtime, so a probe that overrides CSS that way measures nothing at all — the override never applies. CSSOM writes (`el.style.foo = …`) and the Web Animations API are unaffected.
- `getBoundingClientRect()` on a mosaic tile returns the bounding box of the 3°-rotated square, ~10px wider than the cover itself. Read the CSS width when the number matters.

## Android bridge

Inside the Android WebView a native object `window.LyrionApp` is injected. The JS detects it (kept in `APP_BRIDGE`), adds `body.in-app`, reveals the header menu button, and wires it to `bridge.openMenu()` / `openSettings()`. Pull-to-refresh is app-only too: a downward drag starting in the card's cover/meta zone (`PULL_ZONE`, so never the scrolling lyrics box) rides the `#np-pull` badge down from the card's top edge and calls `bridge.reload()` past `PULL_TRIGGER`, which reloads through the shell so a server that has gone away lands on the native error view. The gesture only starts with the page and the card both at their top, and the `touchmove` listener is non-passive because suppressing the WebView's overscroll needs `preventDefault()`. On Android, the "open in Lyrion" links become `intent://` URLs targeting the LMS Material app. Guard any app-only behaviour behind the presence of the bridge, as the existing code does.

## Regenerate the screenshots after a visual change

The images (`docs/screenshots/`) are checked in and embedded in the READMEs: the header pair (`dashboard-en.png` in EN, `dashboard-fr.png` in FR, plus `dashboard-app.png`) and the row of thumbnails below it (`demo-*.png` and `dashboard-mobile.png`, shared by both languages). **If your change alters what the dashboard looks like** — layout, styling, colors, the empty state, the lyrics/stats panels, an icon, anything a user would see — regenerate them so the docs don't drift from the app:

```bash
pip install -r requirements.txt playwright
playwright install chromium        # once
python scripts/generate_screenshots.py
```

The script runs the real app with the Lyrion/DB layers mocked (fake track, synced LRC, generated cover art, canned stats) and captures every image with headless Chromium — desktop in **both** languages, the mobile view, the Android app view, and the demo gallery (enlarged cover, karaoke lyrics, recent-plays pile, statistics panel, empty-state mosaic). Each capture is one `Shot` entry in the script's `SHOTS` map, so a new one is a single declarative line. No Lyrion server or database is needed. Commit the updated PNGs alongside the code change, and keep both language shots in sync (they're regenerated together). Skip this only for changes with no visual effect (pure refactors, endpoint-only tweaks).

## Checklist

1. No new framework/bundler/npm dep; stay vanilla and edit the single JS file.
2. Every user-facing string comes from `I18N` (key added to `i18n.py` FR+EN).
3. Read server data from the existing endpoints / `data-*` attributes.
4. Keep covers same-origin so tinting works.
5. Run `npx --yes eslint@9 static/*.js` — it gates CI.
6. Visual change? Regenerate `docs/screenshots/` (see above) and commit the PNGs.
