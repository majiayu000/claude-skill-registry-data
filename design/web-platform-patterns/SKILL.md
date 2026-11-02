---
name: web-platform-patterns
description: "Use before any web (vanilla HTML/CSS/JS, no build step, static hosting) UI / routing / data / offline / image work. The web umbrella skill — view-system architecture, URL-driven state + canonical share URLs, the 404-forwarder, image fallback chains with jittered retry, service-worker versioning discipline, IndexedDB schema migration, the CSS gotchas that cost real iteration (sticky containing-box, scroll-snap rails, container-query heroes), bounded fetches, and the headless verification protocol (Node DOM shim, CDN cache-bust). Triggers on vanilla JS, hash router, showView, service worker, PWA, IndexedDB, share link, playlist link, [hidden], facet chips, native video controls, node --check, GitHub Pages, scroll-snap, position sticky, image fallback, 404.html, URL params, AbortSignal, \"works locally but not deployed\"."
---

# Web Platform Patterns

The umbrella skill for the framework-free web app — the patterns that
shipped three production web apps (two as PWAs) on GitHub Pages with
no build step and no backend. Most generic frontend skills cover
components; this covers the **architecture, data, offline, and
deploy-reality layer** that vanilla web apps live or die on.

## The five web backstops

1. **The URL is the state.** Every surface is a shareable URL;
   filters live in the query. If a view can't be reached by URL, it's
   not done.
2. **One router, one data module.** `route()` reads the location,
   `showView(name)` toggles `<section hidden>`; ALL external calls go
   through `js/api.js`. Never `fetch` from view code.
3. **Errors are user-visible, inline.** Console-only errors don't
   exist for users. Empty states are explicit sentences, never blank
   space.
4. **No `position: fixed` overlays; modals are `<dialog showModal>`.**
   (Safari compositor at the Dynamic Island; native focus trap + ESC.)
5. **Mobile-first, `min-width` queries only, test 375px before
   1280px.**

## View system architecture

- Each view is a `<section>`; `showView(name)` toggles `hidden`.
  **Per-view `IntersectionObserver`s are disconnected on every view
  switch** — leaked observers from a previous view fire on recycled
  sentinels and corrupt paging state.
- **Event delegation for dynamic content**: one listener on the
  container switching on `closest('[data-action]')`, not per-element
  listeners that vanish on re-render.
- Infinite scroll = an `IntersectionObserver` sentinel + page size
  (~60); always show the REAL total count, not the loaded count.
- Debounce text search ~180 ms; mirror the query into the URL.
- **A one-shot render replaces before it appends.** A `rendered` flag
  guarding an append-only render stacks the page on the first
  re-render (AW Home: 28 sections became 81, stale cards still
  showing).
- **Facets are computed against the OTHER facet's selection.** Chips
  built from the whole result set offer combinations with zero rows.
  Assert "no offered chip yields zero rows", in a node test over the
  shipped function.
- **One rule, one function.** Two callers of one rule drift; name it
  (`searchFacets()`, `nativeControlSet()`) and call it from both.
- **View Transitions**: every DOM update of the swap goes INSIDE the
  `startViewTransition` callback (outside it is captured half-applied);
  skip the API under `prefers-reduced-motion` in JS too (a media query
  cannot cancel a snapshot already taken); test that `showView` swaps
  identically with and without the API.

## URL-driven state + the canonical-twin contract

- Hash routes for the SPA (`#/browse?type=x&decade=1930&sort=az`) —
  every filtered view shareable.
- **Canonical share URLs are PATHS** (`/item/{id}`) — the exact URLs
  native apps emit. On a static host, `404.html` forwards paths into
  the hash router. **Never change this shape once apps ship** —
  installed apps depend on it. Legacy routes get forwarder entries,
  not breakage.
- **A merged id's page forwards; it never 404s.** Generate
  `/item/<old>/` as a zero-second meta refresh with a canonical link to
  the survivor, outside the sitemap; give same-title pages distinct
  `<title>`s (see `canonical-entity-identity`).
- Percent-encode slugs in routes — non-ASCII slugs are real.
- "Open in app" on Detail: `appname://` scheme on Apple UAs, an
  `intent://` URL **with the current page as fallback** on Android.

## State in the link (no backend)

User-made lists (playlists, collections) can travel inside the share
URL. Full rules + measurements: `DEEP_LINKS.md` "State in the link".

- Deflate + base64url (`CompressionStream('deflate-raw')`, no
  library). AW measured 50 items at a median 1,368 chars (p95
  1,542); ~2,000 is the practical ceiling (chat apps, email, QR). Cap
  at ~50, say so on screen, never truncate silently. Version-prefix the
  payload; keep an uncompressed variant for platforms without deflate.
- Shape: `/list/#<blob>`. Route in the PATH (Android intent filters
  cannot see a fragment); payload in the FRAGMENT (never reaches a
  server).
- `/list/index.html` is a REAL generated page with generic preview copy.
  GitHub Pages serves `404.html` with HTTP 404 and crawlers skip
  previews on a 404. Keep the 404 forwarder only as a safety net; the
  deploy refuses to ship without the static page.
- Old link shapes decode forever.
- Declare the AASA path only after the Apple app that handles it is
  LIVE (not approved); Android's intent filter ships in the APK, so it
  is safe in the same release.
- TVs share the same link as a QR code; prove it by decoding a photo of
  the screen back to the exact string.

## Data fetch hygiene

- **Bound every external fetch with `AbortSignal.timeout`.** A
  third-party metadata endpoint that "usually works" can hang 30s+
  on specific items; an unbounded await freezes the view. Measured,
  not hypothetical.
- **Build-time data beats runtime APIs.** If a value can be baked
  into your published data (a URL, a synopsis), the live API is a
  bounded FALLBACK only — never a runtime dependency.
- Never `fetch()` hosts that don't send CORS (verify with GET, not
  HEAD); `<img>`/`<video>` elements are CORS-exempt — use them. Full
  matrix in `shared-data-plane-contract`. When fetching arbitrary
  third-party pages IS the feature (reader mode, link previews), use
  the bounded multi-proxy chain in `web-content-extraction`.
- **Auth/token refresh on `visibilitychange`, not timers** — a
  background tab's timers are throttled; refresh when the user
  returns, before the first action.
- Composing consumer surfaces from a live third-party search/scrape
  API bypasses every policy filter your pipeline bakes in — surfaces
  compose from YOUR published data only.

## Images: the fallback chain that survives throttling

Image hosts throttle burst loads with **transient 503s** — a
one-shot `onerror` fallback leaves broken tiles until a manual
refresh:

1. Try sources in order (primary → secondary host).
2. **Retry the whole chain up to 2× with jittered backoff.**
3. When nothing loads, render a **local typographic placeholder
   card** (title + accent bar) — never the host's generic gray
   placeholder, and never a broken-image icon.
4. Know which IDs are NOT fetchable images (synthetic/derived ids)
   and skip straight to the placeholder — don't burn requests on
   guaranteed misses.

Cards: `object-fit: cover` at a fixed aspect; poster + two text
lines, nothing else.

## Service worker discipline

- **Shell cache-first, with a version string bumped on EVERY shell
  change** (`const CACHE = 'shell-v7'`) — a forgotten bump is the
  classic "deployed but users see the old app."
- **`fetch(url, {cache:'no-store'})` does NOT bypass a service
  worker.** A fetch that "proves the server is wrong" may be the worker
  answering. Clear the SW (DevTools > Application) before trusting it.
- Data files (indexes, config JSON): **network-first with last-good
  fallback**.
- **Never cache video/streams.** Pass media requests through
  untouched.
- Skip admin/secondary tools' paths entirely (they stay live). A
  root-scope SW caches EVERYTHING not excluded: AW's `/pulse` dashboard
  served yesterday's reading beside today's timestamp. Guard with a
  test that regex-reads the `startsWith` bypass clauses out of the
  shipped `sw.js` (`test_sw_bypass.mjs`).
- Offline scope is honest: open + browse cached data; streaming
  playback offline is out of scope.

## IndexedDB

- Version the schema; add stores only in `onupgradeneeded`
  (schema v2 adds `playlists`, v3 adds `channels`, …).
- Progress/resume: persist every ~10 s + on close/end; resume only
  inside the 10s–95% window.
- localStorage is for tiny scalars and seen-flags (with a rolling
  window so it can't grow unbounded); structured user state lives in
  IndexedDB.

## CSS gotchas that cost real iteration

- **An author `display` beats the UA's `[hidden] { display:none }`.**
  `.thing { display:flex }` on a `hidden`-toggled element leaves it on
  screen (AW shipped a 19px empty bordered strip on every desktop
  page). Write `.thing:not([hidden]) { display:flex }`, never
  `!important`.
- **Turning an element into `<a>` inherits the bare `a` rule** (accent
  color, underline). A link not shaped like a link needs
  `color:inherit; text-decoration:none`, affordance on `:hover` /
  `:focus-visible`.

- **A two-column breakpoint set too high makes the main thing grow as
  the window narrows.** Just below it, the player takes the whole
  width, gets taller than it was at a wider window, and pushes the side
  column out of sight (humanshaped.org's exchange at 56rem). Put the
  breakpoint where the side column still fits at its minimum, and cap
  media by the window's height too:
  `width: min(100%, calc((100svh - 8rem) * 16 / 9)); aspect-ratio: 16 / 9`.
- **A grid with no column template sizes its column to min-content**,
  so one unbreakable line (a URL in a `<pre>`) widens the whole column
  past the screen. Write `grid-template-columns: minmax(0, 1fr)`.
- **A phone-only layout keyed on width alone lands on narrow desktop
  windows** (an upright 3:4 camera, taller than a 640px-wide window).
  Add `(pointer: coarse) and (orientation: portrait)`.
- **A cross-origin iframe on a dark page gets an opaque white
  backdrop** (Google's sign-in button) when its document is light. Give
  the iframe `color-scheme: light`.
- **Two-axis sticky (rail `left:0` + ruler `top:0`) requires rows
  set to `width: max-content`** — otherwise the sticky containing
  block is the visible width and the pinned rail detaches mid-strip.
- Scroll-snap rails need `scroll-padding` matched to the container
  inset, or the first/last card snaps half-clipped.
- **Continuously-scaling heroes: every dimension a `clamp()` in
  container-query units (`cqi`)** — scales with the container, no
  breakpoint jumps. Never hard-crop key art into a banner: ambient
  blurred layer behind a sharp, fully-visible poster.
- Carousel auto-advance pauses on hover/touch AND hidden tabs, and
  is disabled (along with ambient drift) under
  `prefers-reduced-motion`. Dots are real `<button>`s synced from
  scroll position.
- System font stack when there's no build step — webfonts mean FOUT
  with no bundler to inline them.
- The Safari body rule (`docs/platforms/web.md`): `100dvh` flex-column body,
  `main { flex:1; overflow-y:auto; min-height:0 }`, no
  `viewport-fit=cover`.

## Native media controls: never draw one twice

The browser's own `<video controls>` bar already has some controls, and
which ones differs per engine (AW measured, 2026-09): Safari (mac/iPad)
has PiP + a speed menu in the bar; Chrome's overflow has speed but PiP
is right-click only; Firefox has neither in the bar. One function
(`nativeControlSet(video, doc)`) decides which of OUR controls to hide;
test it read out of the shipped JS with an engine fixture per row. Do
not assume the matrix; open each browser's menu.

The same holds for a big play button over a paused video: iOS and
iPadOS Safari, Chrome on Android, and Firefox draw their own, while
desktop Chrome and Edge show nothing until the pointer moves onto the
video (humanshaped.org, 2026-10-16: an iPhone showed two stacked play
buttons). Decide it in one tested function from the user agent and
`(pointer: coarse)`, and add the page's own button only where the
browser has none.

## Screen recording on a phone: hand it to the phone's recorder

A page records a screen only through `getDisplayMedia`, and on phones that
is thin: Chrome on Android has never had it, and Safari on iPhone and
iPad gained it in iOS 27 (MDN browser-compat-data, October 2026). The
phone's own recorder (iOS Control Center's Screen Recording, Android's
Screen record tile) works on every phone, records any app rather than
only the browser, and saves to Photos or the phone's videos, which a
plain `<input type="file" accept="video/*">` reaches. So on a phone,
"Screen" shows the steps for that recorder and a button to choose what
it saved; offer in-page sharing as well only where `getDisplayMedia`
exists. Detect it with `typeof md.getDisplayMedia === 'function'`, never
a user-agent ban, and pick the steps by platform remembering that iPadOS
Safari calls itself a Mac (`/Macintosh/` with `maxTouchPoints > 1` is an
iPad). Ask for the microphone in the steps: both recorders leave it off
unless chosen, and a silent screen recording explains nothing.
(humanshaped.org exchanges, 2026-10-15.)

## Porting deterministic logic to JS

When the same seeded logic must agree across platforms (schedules,
rotations, shuffles): port hash/PRNG with **BigInt** (53-bit floats
silently corrupt 64-bit mixers like SplitMix64); anchor "day" logic
to LOCAL time when the experience is local (6 AM local ≠ 6 AM UTC);
verify cross-platform agreement on a fixed seed before shipping.

## Verification protocol (web changes)

- **One-command gate (`tools/test_web.sh`)**: every node test, then
  `node --check` on each shipped script (a syntax error blanks the
  whole app), then a CSS brace-balance count (a truncated `cat >>`
  append silently drops every later rule).
- **Every `API.x` the JS calls must be exported by `js/api.js`.**
  Plain JS has no compiler: AW called a nonexistent `API.summary` for
  115 versions and every web guest got no player. Grep call sites
  against the `return {…}` export block; include a control assert
  that proves the check can fail.
- **Tests read the function out of the SHIPPED file** (regex-extract,
  `new Function`), so the test cannot drift from what runs.
- **Read `PARITY.md` columns by header name.** `row.split("|")` has a
  leading empty element; index math silently overwrote AW's macOS
  column four times.
- **An insane instrument is not evidence.** A zero-width browser window
  reports garbage layout while DOM counts stay valid; never fix CSS to
  satisfy it.

- **Execute the real JS in a Node DOM shim** to verify logic —
  headless Chrome's `--virtual-time-budget` distorts timers and
  `AbortSignal`, and `--timeout` dumps the pre-hydration DOM.
- Pixel-measure layout from screenshots (PIL/sharp) when a layout
  claim matters.
- **Drag the window; don't sample two widths.** Load each page at a few
  widths, then resize one open copy through every width from 1600px to
  320px and back. Fail on sideways scroll, anything past the right
  edge, or a box whose size after the resize differs from a fresh load
  (layout fixed by script at load). Look at the screenshots at the
  in-between widths (640 to 900px) too, where layouts go wrong without
  overflowing. Drive headless Chrome over CDP with
  `Emulation.setDeviceMetricsOverride`, which goes below the 500px
  window floor. Worked example: humanshaped.org's
  `tools/responsive/check.mjs`, which has no dependencies.
- **The Pages CDN caches ~600 s** — verify deploys with cache-busted
  URLs (`?v=...`), or you're testing the previous deploy.
- Local server: `python3 -m http.server 8080`. If it works locally
  but not deployed, suspect (in order): SW cache version, CDN cache,
  Jekyll dropping dot-paths, CORS.
