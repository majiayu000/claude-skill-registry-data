---
name: website-hero-carousel
description: >
  Add a photo place whose photos take turns by themselves, with one dot per photo, to a
  new-website site: a component, one script of the site's own (so a strict
  Content-Security-Policy holds), its texts in English and German, and tests/hero-carousel.spec.ts.
  Settings: pause "button" (default, a visible Pause / Resume button) or "dots" (no button, a dot
  stops it); swap "instant" (default) or "fade". Built to keep the page from jumping, the dots
  readable on any photo, and phones usable. Run on request, for a home page or any page. Trigger
  phrases: "photos that rotate", "auto-rotating hero", "carousel", "slider", "key visual that
  changes", "dots under the photo", "slideshow", "Bildwechsel", "Karussell". Not for one photo (no
  carousel needed), a gallery the visitor pages through, or video.
---

# Website hero carousel: photos that take turns, and the tests that keep them honest

A photo place at the top of a page where two or more photos take turns every few seconds, with a
dot for each. It looks easy and is not: a caption on one photo makes the page jump at every
change; white dots disappear on a pale photo; a phone needs larger targets than a mouse; and
moving content has an accessibility rule of its own. This skill ships the component and, more
importantly, the tests that catch all of these.

## Why it is built this way (say this to the owner, in your own words)

- **The page never jumps.** All photos share one place, cropped to one shape, so the page is as
  tall for the first photo as for the last. There are no captions or credits on the photos: they are
  what moved the page on the site this came from. Credits belong on the site's image-credit page.
- **The dots can be read on any photo.** They sit on a small dark pill, so they show on a pale sky as
  on a dark wall. A test measures this on the pixels of a pale and a dark photo.
- **It works without JavaScript.** The photos then stand one under the other and no button is shown.
- **It is polite.** It stops when the mouse is over it, when the tab is hidden, when keyboard focus
  enters it, and from the start for visitors who ask their device for less motion.
- **Nothing is stored or sent.** No cookie, no storage, no request to another site.

And the honest weak spots, so the owner hears them from you first:

- **Rotating photos are not always the better design.** A single strong photo is calmer, loads
  faster and cannot irritate anyone. Say so; the owner decides.
- **Each extra photo costs the visitor download time on a phone.** Three photos at four sizes each
  are fine; ten are not. Keep it to a handful.
- **"dots" pause mode trades a visible control for a cleaner photo** (the "Pause" section below).

## 0. Is this the right tool? (ask before installing)

1. **Is the owner sure about rotation?** One photo needs none of this. Ask once, plainly.
2. **How many photos, and are they the same shape?** Two to five. Any shape works (each is cropped to
   the carousel's shape), but a photo with its subject at the edge loses it in the crop: look at each
   one at the carousel's shape (16 / 9 by default) and at a phone's.
3. **Do the photos link anywhere?** Any slide may link to a page (a project, say); mixing linked and
   unlinked slides is fine (the CI page does).
4. **Which pause mode?** Read "Pause" below to the owner and let them choose. Default: the button.

## 1. What it adds to the site

| File | From this skill's `templates/` | What it is |
|---|---|---|
| `src/components/HeroCarousel.astro` | `HeroCarousel.astro` | the markup, the dots, the styles |
| `src/components/hero-carousel-text.ts` | `hero-carousel-text.ts` | the words it says, in English and German |
| `public/js/hero-carousel.js` | `hero-carousel.js` | the script: puts the slides in one place, rotates, handles the controls |
| `tests/hero-carousel.spec.ts` | `hero-carousel.spec.ts` | the carousel as a visitor meets it (list below) |

Install all four. The templates hold **no image file**: the photos are the site's own, passed in as
props.

**How it works, in one paragraph.** The server sends every slide, one under the other, and the
controls hidden. The script, a file of the site's own under `public/js/` rather than an inline script
(so a strict `script-src 'self'` lets it run), then puts the slides in one grid cell, shows the
controls and marks the slide on show. Which slide is on show is a data attribute; the CSS does the
rest, the one-second fade included. A slide is shown only when its image is complete, so a late or
failed photo never leaves a blank place.

**What the spec checks** (a visitor's view, on the page as built): the markup and every dot's name;
the interval to the millisecond on a frozen clock; the Pause button or the dot stopping it, with the
labels and the live region; keyboard focus (stops it, stays stopped, Resume); the pointer holding it
and a fresh interval after leaving; reduced motion; a hidden tab; a late and a failed second image;
the page without JavaScript; **no height jump** at 1280, 768 and 390 px; that a slide not on show
cannot be reached by keyboard or in the accessibility tree; that a photo's link works and a dot
never opens it; 32 px targets (44 on touch screens); **the dots against the pill over every photo,
read from rendered pixels**; forced colours; axe in both themes; nothing stored or sent; the script is a
file, not inline; the fade runs on a frame part-way and settles, and does not run under reduced motion.

## 2. Install (on a branch, as a pull request: `AGENTS.md` §2)

1. Copy the four files to the places in §1 (`mkdir -p public/js` first).
2. Put the carousel on a page, inside that page's `<Base>`, near the top:
   ```astro
   ---
   import HeroCarousel from '../components/HeroCarousel.astro';
   import first from '../assets/hero-1.jpg';
   import second from '../assets/hero-2.jpg';
   ---
   <HeroCarousel label="Photos of our work" slides={[
     { image: first,  alt: 'What the first photo shows', label: 'Short name', href: '/projects/one' },
     { image: second, alt: 'What the second shows',      label: 'Another name' },
   ]} />
   ```
   - `label`: what the carousel is, for a screen reader. Required.
   - each slide: `image` (an imported photo), `alt` (a sentence that says what is in it, at least 10
     characters: the build stops on less), `label` (the dot's short name), `href` (optional).
   - `pause`: `"button"` (default) or `"dots"`. `swap`: `"instant"` (default) or `"fade"`.
     `intervalMs`: default 6000, never below 2000. `ratio`: default `"16 / 9"`. `lang`: the page's own.
   Photos: JPEG or PNG, **about 2,400 px wide**, kept to what the page needs (the build makes four sizes
   of each, AVIF with a WebP fallback). The first photo loads first (high priority); the others load at low
   priority and keep their place.
3. **Language.** English and German are built in, and the component takes the page's own language
   (`Base.astro` hands it down as `Astro.locals.lang`). Any other: "Add a language" below, first.
4. In `tests/hero-carousel.spec.ts` set `PAGE` (the page with the carousel), `PAUSE` and `SWAP` to what the
   page passes (the component's defaults are `button` and `instant`; the spec needs them written out).
   The spec fails while one is empty. `LANG` only if the page passes `lang`.
   **Photos for the contrast test:** the spec reads the carousel's real photos, so it meets the owner's own.
   If every one of them is dark, the "white dots on the pill" test cannot fail; to see it fail, check a pale
   one in once by hand (the mutation check in §3 does).
5. `npm run check && npm test`.

### Pause (read this to the owner before they choose)

Moving content that starts by itself, lasts more than five seconds and sits beside other content falls
under WCAG 2.2.2, Level A, which asks for "a mechanism for the user to pause, stop, or hide it" (read at
https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html). The same page defines *pause* as
"stopped by user request and not resumed until requested by user", and does not say the mechanism must
be visible. It does not discuss slide indicators.

- **`pause="button"` (the default).** A Pause button beside the dots (Resume while stopped). Visible, named,
  the reading nobody disputes, and the one a visitor finds. Its price: a small word on the photo.
- **`pause="dots"`.** No button. Choosing a dot shows that photo and stops the rotation until the visitor
  reloads; focus entering it from the keyboard stops it too, and reduced motion starts it stopped. That is
  likely a mechanism in the sense of 2.2.2, but **nothing tells a visitor that a dot stops it, and there is
  no way to resume**. The first site to use this mode chose it for the cleaner photo, knowing that.

This skill draws no conformance conclusion: whether "dots" is accepted is for the site's own auditor.
If the owner picks it, write one line in the site's docs saying so, with the date.

### Add a language

On a new site in that language, or when a site gains it later.

1. Read the site's voice first (`CONTENT_GUIDE.md`; in German the register, "du" or "Sie"). The texts are
   a handful of words: where the language allows, address nobody.
2. In `src/components/hero-carousel-text.ts`, copy the `en` entry of `TEXT` under the language's two-letter
   code (`fr`, not `fr-CA`) and translate every value; `npm run check` fails while one is missing.
3. The page and its test, as in §2 steps 3 and 4.

## 3. Try it once (the owner), and the checks behind this skill

After `npm run build && npm run preview`, or on the pull request's preview address, the owner:

1. Waits: the photos change by themselves, the dot on show follows.
2. Moves the mouse over it: it holds. Takes it away: it goes on, after a full interval.
3. On a phone: taps a dot (it shows its photo); no sideways scrolling; the dots are easy to hit.
4. In the button mode: presses Pause, sees it say Resume, presses it again.

The checks this skill was built with, so a change to a template can be judged: the spec carries one
test for each of these, and each fails when the thing it guards is removed. Run once by hand when the
templates change (the CI job installs them in a fresh site and runs the spec, in all three
combinations of the settings it uses):

| Remove this from `HeroCarousel.astro` | This test fails |
|---|---|
| the grid rules (`display: grid`, `grid-area`) | "the slides share one place …" |
| `aspect-ratio` on the photo | the same test (a 4:3 photo is taller) |
| the pill's `background` | "rendered over every photo …" (white on a pale photo is about 1:1) |
| `border-width: 5px` on the dot on show | the forced-colours test |
| the `transition` rules | the fade test ("a frame part-way") |
| `pointer-events: none` on slides not on show | "the photo links to its page …" (a fading slide takes the click) |
| the `inert` and `aria-hidden` the script sets on slides not on show (`hero-carousel.js`) | the Tab-key and accessibility-tree tests (the link of the slide that is going stays reachable and readable while it fades) |
| the script's `recover()` (a failed photo on show is replaced by the first other one that is there, now or when it arrives) | "a first image that fails …" |

## 4. The privacy page, and the way back

The carousel stores nothing and sends nothing: **nothing to add** to the privacy page.

To remove it: delete the four files, the `<HeroCarousel>` block **and the `import HeroCarousel` line (with the
photo imports only it used)** from the page; put one photo back. Nothing else refers to it, apart from
`PAGES`-driven suites that only see the page.

## 5. Not in this skill (so nobody assumes)

Previous / next arrows, swipe gestures, captions on the photos, credits on the photos, video slides,
more than one carousel on a page (its ids are fixed), lazy loading of the later photos. Each can be
added later; none is needed for the first version.
