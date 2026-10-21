---
name: website-motion
description: >
  OPTIONAL polish layer: two motion effects that make a long marketing page feel
  authored rather than dumped — a count-up on hero stat numbers, and a 12px
  rise-and-fade reveal on section headings — plus the reduced-motion contract,
  the a11y gate change, and the motion.spec.ts that keep them from silently
  costing a visitor access to content. Not part of the default new-website
  build: add it only when a site has a long scrolling homepage and real numbers
  worth reading. Also carries the one-line hero-height check (a binding
  min-height:100vh hides the next section at every screen height). Trigger
  phrases: "add some motion", "scroll reveal", "fade in on scroll", "animate the
  stats", "count-up numbers", "animated counter", "the page feels flat", "eye
  candy", "make the homepage less static", "prefers-reduced-motion", "does the
  animation break accessibility".
---

# Website motion

Two effects, deliberately. Motion is where a site starts looking machine-made:
applied to every card and paragraph it reads as a template, and it is the single
easiest way to lose content to an accessibility bug nobody notices. This skill
ships the two that earn their place, and — more importantly — the contract that
makes them safe.

**Only add this when the page is actually long.** On a three-section site a
reveal is noise. The count-up needs numbers a visitor should stop and read
(attendee counts, years running, projects shipped), not decoration.

**Prerequisite:** `website-qa` green first. This adds a test file to that suite
and changes how the a11y gate runs.

> ### The class names below are examples, not the scaffold's
>
> `.section-title`, `.section-subtitle`, `.hero-stat-number` and `.hero` appear
> **zero times** in `new-website`'s Astro templates. They come from a real site
> this was extracted from. Nothing here works until you point every selector at
> your own markup — the CSS, the two scripts, and the `CONFIG` block at the top
> of `templates/motion.spec.ts`. The spec skips with a stated reason when a
> selector is left empty, so an unconfigured copy reports "not applicable"
> instead of failing in a way that looks like a product bug.

---

## 0. The one-line check that is not motion

Before adding anything, measure the hero:

```js
const h = document.querySelector('.hero');           // your hero's selector
({ vh: innerHeight,
   heroHeight: h?.getBoundingClientRect().height ?? null,
   nextSectionVisible: h?.nextElementSibling
     ? innerHeight - h.nextElementSibling.getBoundingClientRect().top : null })
```

If `min-height: 100vh` is *binding* — the hero's own content is shorter than the
viewport — the next section starts exactly at the fold and the page reads as a
splash screen. Trim the floor until the next section peeks over the edge.

**Do not copy a number from another site.** The right value is a function of the
hero's content height. If the content already exceeds the viewport, changing
`min-height` does nothing at all on that screen size, and the real lever is
cutting a paragraph out of the hero. Measure, then decide.

---

## 1. The contract

Everything below exists to keep one promise: **no effect may leave content
unreachable.** Three rules, in priority order.

1. **Hidden state is added by JS, never authored in HTML.** A visitor with no JS,
   or one landing mid-page, must see the finished page. The script adds the
   hiding class itself, and only to elements currently below the fold.
2. **`prefers-reduced-motion: reduce` ends with everything visible and nothing
   moving** — including animations that predate this skill. **The Astro scaffold
   ships `html { scroll-behavior: smooth }` with no override**, so this is a
   step you must actually perform, not a property you inherit:

   ```css
   /* AFTER the rules it overrides — see §6, this is the whole trap */
   @media (prefers-reduced-motion: reduce) {
     html { scroll-behavior: auto; }
     /* plus any ambient animation this site runs */
   }
   ```
3. **Print is a third state.** It never scrolls, so `IntersectionObserver` never
   fires and a revealed heading prints blank.

---

## 2. Scroll reveal — section headings only

```css
@media (prefers-reduced-motion: no-preference) {
  /* No transition on the hidden state. `reveal` is added after first paint, so a
     transition here makes an already-drawn heading fade OUT for half a second
     before it can fade in — visible to anyone scrolling straight after load.
     With the transition on the visible state, hiding snaps and only the reveal
     animates. */
  .reveal { opacity: 0; transform: translateY(12px); }
  .reveal.is-visible {
    opacity: 1; transform: none;
    transition: opacity 0.55s ease-out, transform 0.55s ease-out;
  }
  /* Same specificity as the rule above and LATER in the sheet, so the shorthand
     there cannot reset the delay to zero. */
  .reveal-delay.is-visible { transition-delay: 0.09s; }
}
/* Printing never scrolls, so the observer never fires. */
@media print { .reveal { opacity: 1 !important; transform: none !important; } }
```

```js
(function () {
  if (!('IntersectionObserver' in window)) return;
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  function partnerOf(heading) {
    var next = heading.nextElementSibling;
    return next && next.matches('.section-subtitle') ? next : null;
  }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (!entry.isIntersecting) return;
      io.unobserve(entry.target);
      entry.target.classList.add('is-visible');
      var partner = partnerOf(entry.target);
      if (partner) partner.classList.add('is-visible');
    });
  }, { threshold: 0.15 });

  document.querySelectorAll('.section-title').forEach(function (heading) {
    // Anything already on screen is left alone — hiding it now would make it
    // flash out and fade back in on load.
    if (heading.getBoundingClientRect().top < window.innerHeight) return;
    heading.classList.add('reveal');
    var partner = partnerOf(heading);
    if (partner) partner.classList.add('reveal', 'reveal-delay');
    io.observe(heading);
  });
})();
```

**Headings only.** The subtitle rides along one beat behind so the pair reads as
one movement — that is what "staggered" should mean here. Applying this to cards,
list items and paragraphs is the AI-generated-site tell.

---

## 3. Hero stat count-up

```js
(function () {
  var nums = document.querySelectorAll('.hero-stat-number');   // your selector
  if (!nums.length || !('IntersectionObserver' in window)) return;
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  function countUp(el) {
    // Writing textContent flattens child markup permanently — a styled
    // <span>+</span> inside the number would not survive the animation.
    if (el.children.length) return;

    var finalText = el.textContent.trim();
    // Digits, an optional group separator ("," in en, "." in de), an optional
    // trailing symbol. Everything else is left exactly as authored: these are
    // published claims, and "4.9" must never animate up to 49.
    var parts = finalText.match(/^(\d{1,3}(?:([.,])\d{3})*|\d+)(\D*)$/);
    if (!parts) return;
    var target = parseInt(parts[1].replace(/\D/g, ''), 10);
    var groupSep = parts[2] || '';
    var suffix = parts[3] || '';

    // Mirror the AUTHORED grouping rather than a runtime locale. The frozen
    // width below is measured from the authored string, so rendering "1,200"
    // where the page says "1.200" — or grouping a number the page left
    // ungrouped — is a different width, which is the exact row-shove the
    // freeze exists to prevent.
    function render(v) {
      var digits = String(v);
      return (groupSep ? digits.replace(/\B(?=(\d{3})+(?!\d))/g, groupSep) : digits) + suffix;
    }

    // Freeze the box first. "0+" is far narrower than "1,200+", and the stat is
    // usually sized by its number rather than its label, so an unfrozen count
    // shoves the whole row sideways every frame.
    // Remember any inline min-width already on the element — blanking it on
    // settle would quietly undo a later styling change someone else made.
    var priorMinWidth = el.style.minWidth;
    el.style.minWidth = el.getBoundingClientRect().width + 'px';
    var done = false;
    function settle() {
      done = true;
      el.textContent = finalText;
      el.style.minWidth = priorMinWidth;
    }
    // A print fired mid-count would capture an intermediate figure — a number
    // the site does not claim. Contract rule 3 covers the reveal; this is the
    // count-up's half of it.
    window.addEventListener('beforeprint', settle);

    var started = performance.now();
    function frame(now) {
      if (done) return;
      var t = Math.min((now - started) / 1400, 1);
      el.textContent = render(Math.round(target * (1 - Math.pow(1 - t, 3))));
      if (t < 1) requestAnimationFrame(frame);
      else settle();
    }
    requestAnimationFrame(frame);
  }

  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (!entry.isIntersecting) return;
      io.unobserve(entry.target);
      countUp(entry.target);
    });
  }, { threshold: 0.6 });
  nums.forEach(function (n) { io.observe(n); });
})();
```

The final values stay in the HTML, so no-JS visitors and crawlers see the real
numbers and the animation only ever replaces them temporarily.

**`min-width` only works on a block box.** If the stat number computes to
`display: inline`, the freeze is a silent no-op and the row still jumps. Check
the computed value, or set `display: inline-block`.

**Run both scripts after the DOM is parsed** — `defer`, a module, or at the end
of `<body>`. In a synchronous `<head>` script the query returns nothing and both
effects are silently dead.

## 4. The a11y gate has to change, or it gets quietly weaker

This is the part that is easy to miss, and it is the reason this skill exists
rather than a snippet in `website-design-system`.

**A reveal leaves headings at `opacity: 0` while axe runs, and axe skips elements
it considers invisible.** Their colour contrast silently stops being checked. The
suite stays green and the gate is weaker than it was the day before.

Force reduced motion in `a11y.spec.ts` so axe always sees the finished page. The
snippet below assumes that file's `for (const path of PAGES)` shape — adjust it to
whatever loop or fixture your suite actually uses. The `emulateMedia` call before
`goto`, and the canary under it, are the load-bearing parts:

```ts
for (const path of PAGES) {
  test(`a11y: ${path}`, async ({ page }) => {
    await page.emulateMedia({ reducedMotion: 'reduce' });
    await page.goto(path, { waitUntil: 'load' });
    // …unchanged
```

> **`test.use({ reducedMotion: 'reduce' })` may not be a substitute.** Measured
> once, on Playwright **1.60**, against **a different repo's config** — not this
> toolkit's, whose lockfile currently resolves 1.64.0. There, the `test.use` form
> was accepted without complaint while the page's `matchMedia` still reported
> `no-preference`; `page.emulateMedia` and `browser.newContext` both worked in the
> same run. That contradicts how the option is documented, and the mechanism was
> never established, so treat it as one measurement rather than a rule about
> Playwright. `emulateMedia` is used here because it is the form that was actually
> observed to work.

Whichever form you use, **prove it reached the browser**, because the failure is
silent — and a per-test call is one forgotten line away from a page that quietly
keeps the weakened gate:

```ts
// Canary. Without it, a gate that does nothing looks exactly like a gate.
expect(await page.evaluate(() => matchMedia('(prefers-reduced-motion: reduce)').matches),
  'reduced motion never reached the browser — the a11y gate is not deterministic')
  .toBe(true);
```

---

## 5. `motion.spec.ts` — the test that makes the contract real

Copy this skill's `templates/motion.spec.ts` into the site's `tests/`. It lives
here rather than in the `new-website` Astro overlay on purpose: that overlay is
copied into every scaffold, and this spec asserts an effect a fresh site does
not have — it would fail on day one of every new project.

Each row below exists because of a specific way the contract breaks. The right-hand
column is what the assertion is for, not a claim about how often it has fired:

| assertion | the bug it catches |
|---|---|
| No heading is invisible after a full scroll-through | the whole failure mode this skill guards against |
| Nothing above the fold is hidden at load | a heading that visibly flashes out and fades back in |
| Reveal targets are visible under `media: print` | the print override being deleted or mis-ordered |
| Under reduced motion nothing is hidden, `scroll-behavior` is `auto`, **nothing is animating**, and the `.reveal` rule is force-applied to prove the CSS itself yields | an ambient animation ignoring the preference; smooth scrolling left on; and an override placed *before* the rule it overrides — same specificity, so the original wins and the fix is a silent no-op |
| Stat numbers settle on their published values | someone editing the figures in HTML |

The forced-class step in row 4 is not belt-and-braces. Under reduced motion the
reveal's JS bails, so the hiding class is never added and the stylesheet is never
exercised — without forcing it on, that row would pass with the CSS override
broken.

**A "nothing animates" test must cover the page's other animations too** — an
ambient hero glow, `scroll-behavior: smooth`. Asserting only your own effect
makes the test's name a lie.

**The count-up assertion is a content snapshot, not an animation test.** The
final frame restores the authored string, so it passes with the animation dead.
Say so in the comment rather than implying coverage it does not have; sampling a
1.4s rAF animation from the test side is timing-dependent and not worth a flaky
gate.

---

## 6. Gotchas that cost real debugging time

- **A reduced-motion override must come AFTER the rule it overrides.** Same
  specificity means later wins. Placed up beside the original declaration it
  reads more naturally and does nothing.
- **A marquee-style strip cannot be hovered or clicked by Playwright.** It waits
  for the element to stop moving and a looping element never does. Drive the
  mouse by coordinate (`page.mouse.move`) instead.
- **Sampling a looping animation flakes at the wrap.** A single before/after pair
  measures one window against the loop period — a 1s sample of a 90s loop lands on
  the restart, where position jumps forward, about one run in ninety. Sample
  several intervals and take a majority; only one of them can contain the wrap.
- **Adding a heading changes heading order.** A new section heading between the
  last content heading and the footer's can skip a level. `heading-order` is an
  axe *best-practice* rule, so a WCAG-tagged gate will not catch it — check it
  by hand once, or accept that it is ungated and say so.
- **`document.getAnimations()` takes no arguments.** It is already document-wide,
  pseudo-elements included; the `{ subtree: true }` option belongs to
  `Element.getAnimations()`. Passing it is ignored at runtime and fails a strict
  TypeScript check — a copied test that will not compile.
- **Animation names are Chromium-shaped.** `animationName` / `transitionProperty`
  live on `CSSAnimation` / `CSSTransition`. An engine returning plain `Animation`
  objects still gets caught, but every entry reads `unnamed`, so
  `motionExceptions` cannot filter individual ones.
- **What this spec does NOT cover.** It runs at one viewport, so wrapping and
  section placement on mobile are unchecked — the below-fold set differs there.
  And the toolkit's `template-tests.yml` tests only the Astro starter and two
  other skills, never this template, so CI does not exercise it at all; it was
  verified by running it against a real site instead.
- **A preview pane may report `visibilityState: "hidden"`.** Where it does,
  `IntersectionObserver` never fires, CSS transitions freeze at their start
  value, and deep-scroll screenshots come back blank. None of this reproduces a
  real browser. Verify motion with Playwright, and use `locator.screenshot()` —
  it captures a single element and sidesteps the blank-capture problem.

---

## Boundaries

- Owns motion only. Layout, images and theme tokens stay in
  `website-design-system`; the QA suite stays in `website-qa`.
- Never a default. `new-website` does not run this; a human asks for it.
