---
name: landing-page-designer
version: 1.0.0
description: Design landing-page proposals for a product as self-contained HTML grounded in its code, real captures and brand — one memorable device per page, a choreographed hero film, an accessibility and verification bar (axe x8, parser check, smoke test). Use when asked to draw, propose or improve a product's public/landing page, compare directions, or "make it more attractive / more dynamic". Not for porting a chosen design into the app (later job); upstream concept work is website-concept-architect.
---

# Landing page designer (proposal rounds)

The method for proposing landing pages in rounds, what each decision rests on, and the checks a page must pass before anyone sees it. Upstream of this skill: [website-concept-architect](../website-concept-architect/SKILL.md) (what the site is). Downstream: [ui-ux-architect](../ui-ux-architect/SKILL.md) (porting into the app).

## 0. The job, and what it is not

- **Draw, do not refactor.** Output is proposals under `<proposals-dir>/<date>/<product>/`. Do not touch the app's shipping code; do not commit or push unless the owner says so.
- A page is **finished** only when it passes the verification bar (section 8) and its claims are traced (section 2).
- Work in **rounds**. Each round produces new directions, keeps the old ones as an idea library, and ends with a recommendation and the reason it beats the others.

## 1. The bar (what "impressive" means)

Judge every screenshot against this list.

1. **Five seconds.** A stranger can say what the product does, who it is for, and why it differs, from the first viewport alone.
2. **One device.** The page is remembered for one specific, product-only thing, not a colour. Good devices are literal: the cursor in the logo used as a real cursor; a real number that moves; an agent-to-server exchange shown as the two calls it really is; a push arriving on a phone at the moment the copy says.
3. **Concrete, not abstract.** Every claim points at something in the product or its code.
4. **Real pixels beat illustration.** A cropped screenshot of the running product beats any drawing of it.
5. **Say the trade-off.** Copy states what it does, who it is for, and the one thing it accepts in exchange (self-hosted: your updates and backups; one shared service: one more dependency; delivery only: policy stays in the app).
6. **Forbidden:** stock photography, purple gradients, bento grids of grey cards with an icon each, "Trusted by 10,000 teams", invented testimonials, fake metrics.

## 2. Research first: facts with sources

Before drawing, build a **facts table** per product: claim, value, source file. Read the code, not the marketing.

- **Where to look:** `README.md`, `AGENTS.md`/`CLAUDE.md`, design docs and ADRs, `CHANGELOG.md`, validators and error codes, tool/endpoint registrations, wire/proto mappings, worker/retry constants, the brand mark component, the theme tokens file, the existing landing view.
- **Facts worth finding:** exact tool names and how many are destructive; error codes and messages; constants (retry attempts, backoff base and cap, poll interval, trust limits); request fields (count them in the wire mapping, not the doc); routes; real quick-start commands.
- **Verify counts and names in code.** Docs drift: a documented "six fields" can be eight in code; a README can point at a directory that no longer exists; a hero example can use a unit the server rejects.
- **Flag, never fix silently.** Inconsistencies (stale branding in captures, captures that disagree, doc vs code) go in `NOTES.md` and, if relevant, on the page.
- **Label illustrative data on the page** (sample entries, ids, times, notification text). The reader must tell real from sample without the notes.

## 3. Brand and family

- **Each product keeps its own mark and accent.** Copy the real mark path from its component and the real tokens (backgrounds, text, muted, accent, accent-text, semantic colours) from the tokens file, both themes.
- **Fonts: only the product's own**, copied as woff2 into `fonts/`. Inspect them before choosing a type voice:
  ```bash
  python -c "from fontTools.ttLib import TTFont; t=TTFont('inter-latin.woff2'); print([(a.axisTag,a.minValue,a.maxValue) for a in t['fvar'].axes])"
  ```
  A variable font declared over its full weight range can give hairline numerals for one product and kinetic heavy weight for another, with no new fonts.
- **An org brand kit is family, not template.** Use it for small shared details (a kicker mark, a footer credit in `currentColor`), never as the product's identity.
- **Family layer:** one shared file with spacing, type and motion tokens, header, buttons, kicker, section rail, film control, copy button, footer and the motion kit. Products override colour, type voice and composition. Several pages should read as siblings with distinct personalities.

## 4. Art direction per product

Decide a **personality** before layout; let it drive type, grid, colour weight and pace. Examples that worked:

| Personality | Type voice | Composition and pace |
|---|---|---|
| Calm, editorial (finance) | One huge hero figure in a light weight with tabular numerals; mono for ledger lines | Generous whitespace, asymmetric grid, a night band, one full-bleed real capture |
| Loud, kinetic (fitness) | Black weight, tight negative tracking, oversized numerals | Full-bleed accent band with a ticker, hard rules, loud and quiet sections alternating |
| Technical, exact (identity) | Mono callouts, big mono numerals | Hairline grid ground, numbered figures with captions, annotated diagrams |
| Terse, rhythmic (notifications) | Giant mono status words | A time ruler as recurring motif, negative space, a pinned section |

- **Avoid the default skeleton** (eyebrow, h1, lede, two buttons, trust list, glow) unless you change it with intent. A round where every product shares one skeleton has failed.
- **Pace a long page** like a film: a quiet section, a loud one, one full-bleed moment, a dark band, a change of background. Uniform spacing reads as stitched.
- **Design 390 px on purpose:** own crops of captures for phones, diagrams that reflow (stack, side bus) instead of shrinking, film content above the fold.
- **Contact sheet check:** render all products' first viewports side by side (both themes, 1440 and 390). Look for sameness and family breaks.

## 5. The hero film

One choreographed sequence per product that tells the product in 4 to 8 seconds and **settles on a static final state**.

- **The final state is the plain HTML.** JS off and reduced motion show it at once; the film only animates towards it (a `reset()` for the start state, steps `[ms, fn(instant)]`, `end()` cleanup).
- **Plays once on view**, never loops; pauses when the tab is hidden; has a visible **Pause/Replay** control (WCAG 2.2.2). Typing inside a film is driven by the film timeline so Pause freezes it too.
- **Tell the truth in sequence.** Use real behaviour as the plot: request → rejected with the real error → resend → saved; three copies → one; queued → poll → sent. Do not fake a highlight the data does not support.
- **Shared-element moves** (a total flying into the hero figure, tables flying into one database) make one scene instead of a list of reveals.
- Accessible text: the visible typed layer is `aria-hidden`; the full sentence is in an `.sr` span once.

## 6. Motion rules

- **Gate:** content visible by default; a head script adds `html.anim` only when `prefers-reduced-motion` allows; every hide or animate rule sits under `.anim`.
- **Opacity only in one-shot reveals** (IntersectionObserver, ends at 1). Scroll-linked effects (`animation-timeline: view()/scroll()`, sticky scrubbing) animate **transform, clip-path or stroke only**: a half-transparent text state fails contrast in axe.
- Allowed: CSS scroll-driven animations with static fallback, View Transitions for the theme switch (circular wipe from the toggle), CSS `linear()` springs, variable-weight animation, count-ups that write the final text when motion is off.
- Auto-moving content (tickers, auto-play) needs a pause control and pauses on hover/focus.
- Measure layout shift; reserve space for counters and typed text.

## 7. Captures

- **From the running product only**, never a mockup of it. Seed demo data deterministically so numbers agree across captures (or say on the page that they do not).
- Crop **with intent** (one panel per point), both themes, 2x, plus separate phone crops.
- **Crop out stale branding** and flag it. Say in captions when the UI language differs from the page's.
- Implement as a light/dark `<img>` pair with `height:auto`, a meaningful `alt`, and markers positioned in the capture's coordinate space (measure it; markers drift).
- If the build is blocked (private packages, missing token), say so, label drawn data as illustrative, and list the exact unblock.

## 8. Hard requirements and verification bar

Every page:
- Self-contained HTML, inline CSS and SVG, **no CDN**, only the product's fonts; under **200 KB** excluding captures.
- Light and dark via `data-theme` with a toggle (stored preference, system default).
- Landmarks, one `h1`, heading order without gaps, skip link, focus-visible, 44 px targets, forced-colors fallback.

Checks (all must pass before showing anyone):
1. **`verify.js`:** axe-core (wcag2a/2aa/21aa/22aa + best-practice) at **390x844 and 1440x800 × light/dark × motion/reduced = 8 runs, zero violations**. In motion mode scroll the whole page first so reveals fire. Also: no horizontal scroll; images blocked still readable; JS off still readable.
2. **HTML parser check** for swallowed text: a raw `<token>` or `<no-reply@…>` in text becomes a tag and axe will not tell you. Escape as `&lt;`.
3. **Smoke test** per page: click every control at 1440 and 390, fail on `pageerror`, run axe again in interactive end states (dialogs open, after apply).
4. **Screenshots:** settled film and reduced motion, both themes, both widths. Look at them and iterate at least twice as a harsh art director.
5. **Say what is not covered:** screen reader, Safari/Firefox, real devices, user testing of the five-second claim.

## 9. Traps (each cost time once)

- CSS specificity: a theme-switch rule for images must beat component rules (`img.sl`, not `.crop img`).
- Measuring a hidden element gives 0 (lens, zoom): show, then measure.
- Opacity-dimmed inactive steps fail contrast: emphasise with border/background instead.
- `role="list"` needs `listitem` children; section titles must not jump from `h1` to `h3`.
- Glow/mesh backgrounds need full-bleed, a mask, and `body{overflow-x:clip}`.
- An unbreakable `<code>` in a grid cell causes horizontal scroll at 390; a scrollable `pre` fails `scrollable-region-focusable` (give it `tabindex="0"`, `role="region"` and a unique label, or use `pre-wrap`).
- Generic class names collide across shared and product CSS (`.tl`, `.copy`): namespace family classes.
- `cqw` resolves against an ancestor container, never the element itself.
- An `aria-label` that differs from visible text breaks label-in-name; put extra context in an `.sr` span.
- A Python template string missing its `f` prefix leaks `{label}` into the accessible name: grep the output.
- `loading="lazy"` images are missing from full-page screenshots; not a defect.
- Pages assembled by extraction do not update when a source changes until the assembler is re-run.

## 10. Process

1. **Read** the brief/handoff, the product code and docs; build the facts table and flags (section 2).
2. **Inventory brand:** mark path, tokens, fonts (axes), existing captures and their problems.
3. **Round of directions:** 3 small, different directions per product, each built around one device. Keep them as the idea library.
4. **Owner feedback** → combine the best ideas into a long page (section rail, FAQ, real quick start with copy button, a weighted "what you accept" block).
5. **Raise the ceiling:** a shared family layer first, then one art-directed page per product with a hero film. Independent products can be built in parallel (one agent per product, family layer read-only, suggestions reported back and applied once, then all pages rebuilt and re-verified).
6. **Review together:** contact sheets, consistency fixes in the family layer, full re-verification.
7. **Deliver:** per product a `NOTES.md` (concept, real vs sample, flags, verification table); a `HANDOFF.md` for the next session (goal, decisions, flags, weaknesses, next ideas); viewing-only standalone previews with fonts and captures inlined; a short summary with one recommendation per product and why it wins.

## 11. Files and tools

```
<proposals-dir>/<date>/
  HANDOFF.md                  brief for the next session
  <product>/direction-N.html  pages; NOTES.md; fonts/; shots/
  _tools/verify.js            axe x8, overflow, images blocked, JS off
  _tools/family.py            shared shell, tokens, motion kit (film, count, type, onView)
  _tools/build_<product>.py   one generator per product
  _tools/settled.js           screenshot after the film settles
  _tools/standalone.py        viewing-only copy with inlined fonts and captures
  _tools/smoke_<product>.js   interaction smoke tests
```

Generators carry hard-coded paths from the session that made them; fix `sys.path` and output paths before running. `verify.js` expects `axe-core@4.10` installed in a sibling `verify/node_modules`.

## 12. Checklist before you show a page

- [ ] First viewport passes the five-second test; the one device is visible there.
- [ ] Every number and name traced to a file; sample data labelled on the page; flags in `NOTES.md`.
- [ ] Trade-off stated plainly and given visual weight.
- [ ] Hero film settles; final state is the default HTML; Pause/Replay works; reduced motion and JS off read fine.
- [ ] Scroll-linked effects use transform/clip/stroke only; reveals are one-shot.
- [ ] 390 px designed (own crops, reflowed diagrams), not just stacked.
- [ ] verify.js ALL CLEAN (8 runs), parser check clean, smoke test clean, under 200 KB.
- [ ] Looked at the screenshots, both themes, both widths, and changed something because of what you saw.
