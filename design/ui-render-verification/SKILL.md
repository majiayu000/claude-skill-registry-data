---
name: ui-render-verification
description: "Use when a UI change needs pixel/size proof, not tests."
version: 1.0.0
author: OpenAmer
license: Apache-2.0
platforms: [windows, linux, macos]
metadata:
  openamer:
    tags: [ui, css, verification, playwright, react, sizing, evidence]
    related_skills: [build-artifact-provenance, desktop-evidence-ledger, openamer-desktop-build, windows-computer-use]
---

# UI render verification — prove what the component actually paints

## Trigger

- A UI change must be shown to work ("the loader is now OpenAmer's own", "the
  mark is too big") and rebuilding/restarting the host app is expensive or would
  kill the session.
- A layout complaint tests cannot see: an element "extremely big", clipped,
  invisible, or off its line.
- You replaced one component with another and need to know whether sizing,
  animation, and accessibility survived at **every** call site.
- Before claiming a visual fix is live: the artifact must carry the new bytes
  (that half lives in `build-artifact-provenance`).

## Why green tests are not evidence here

`jsdom` has **no layout engine**: `getBoundingClientRect()` returns zeros, no
flex/grid resolution runs, CSS animations never tick. A vitest test can prove
markup and props and still be blind to the bug the user sees.

Measured 2026-11-20: a spinner component was migrated app-wide and rendered
**hundreds of pixels wide**, filling a whole grid cell — every unit test green,
`tsc` and `eslint` clean. Cause: the old component was a **text glyph** (size
came from the surrounding font), the new one is a **box** (`inline-grid` + a
`size-full` SVG). 37 of 108 call sites carried no `size-*` class, so the box had
no intrinsic size — and a grid child with no size stretches to its cell.

## Recipe — the real component, the real shipped CSS, a real browser

```js
// 1. compile the ACTUAL component (alias the app's import root)
await esbuild.build({
  alias: { '@': resolve(root, 'src') },
  bundle: true, entryPoints: [resolve(root, 'src/components/ui/<thing>.tsx')],
  external: ['react', 'react-dom', 'react/jsx-runtime'],
  format: 'esm', jsx: 'automatic', platform: 'node',
  outfile: bundlePath, tsconfig: resolve(root, 'tsconfig.json')
})

// 2. server-render it to real markup
const [{ Thing }, { createElement }, { renderToStaticMarkup }] = await Promise.all([
  import(pathToFileURL(bundlePath).href), import('react'), import('react-dom/server')
])
const markup = renderToStaticMarkup(createElement(Thing, { decorative: true }))
```

3. **Bind the CSS that SHIPS**, not the source stylesheet:

```js
const deployed = 'release/win-unpacked/resources/app.asar.unpacked/dist/assets'
const cssFile  = readdirSync(deployed).find(f => /^index-.*\.css$/.test(f))
```

A Tailwind utility exists only after a build. Verifying against `styles.css`
proves nothing about what the user runs, and a class that never got emitted is a
change that ships as a no-op while the JSX looks perfect.

4. **Measure, then judge with a number** (Playwright + `getBoundingClientRect`):

```js
const report = await page.evaluate(() => [...document.querySelectorAll('[data-slot]')].map(el => {
  const r = el.getBoundingClientRect(), s = getComputedStyle(el)
  return { slot: el.dataset.slot, w: +r.width.toFixed(2), h: +r.height.toFixed(2), fontSize: s.fontSize }
}))
```

Exit non-zero on a violated expectation (`h ≈ 1.15 × fontSize`, `h === 24` for
`size-6`) so the harness is a gate, not a screenshot to eyeball. Runnable
starting point: `scripts/render_harness.mjs` (component → markup → measured table
+ exit code, with a frozen-frame mode).

## Deterministic frames of an animation

Screenshots alone are a coin flip against a moving animation. Freeze it exactly:

```css
.frozen .animated-el {
  animation-delay: var(--freeze, 0ms) !important;   /* negative = seek forward */
  animation-play-state: paused !important;
}
```

Drive it from a query param (`?t=1300` → `--freeze: -1300ms`) and you capture the
*same* frame twice, days apart. Stitch frames into a GIF with
`PIL.Image.save(..., save_all=True, append_images=..., duration=100, loop=0)` to
show the motion without anyone rebuilding.

## The sizing contract this bug class wants

A component that may be dropped into a text line must be **bounded by default**,
not `auto`:

```tsx
className={cn('oa-loader inline-grid size-[1.15em] shrink-0 place-items-center', className)}
```

- `1.15em` scales with the line exactly like the glyph it replaced; an explicit
  `size-6` still wins (tailwind-merge resolves the conflict inside `cn`).
- The default makes omission harmless — no call site can blow up a layout by
  forgetting a size. Without it, one forgotten `size-*` is a full-cell mark.
- Keep `shrink-0` too, or a flex row can still squeeze it to nothing.

## Audit every call site before shipping a component swap

Grep is not enough — parse the tags and flag the ones that lost their size:

```python
TAG = re.compile(r'<BrandLoader\b[^>]*/>', re.S)
CLS = re.compile(r'className="([^"]*)"')
# flag tags whose className has no (size-|h-|w-) token and no inline style
```

The count is the finding: "37 of 108 call sites have no size" explains a bug that
looks random and tells you whether one base-class fix covers all of them.

## Pitfalls

- **Do not verify against the source CSS** (step 3). Same for JSX: when the claim
  is "the shipped UI contains X", grep the built bundle
  (`app.asar.unpacked/dist/assets/index-*.js`).
- **A dev-server screenshot is not the shipped UI.** Different CSS build, often
  different fonts; the user looks at the packaged one.
- **Keep the harness out of the repo.** `tmp/` harnesses appear as untracked
  changed paths and make a clean tree look dirty — move them next to the evidence
  (`reports/<topic>-harness/`) or delete them once the number is recorded.
- **Do not judge a mark at one size.** Render a ladder (12/14/16/20/24/32/48 px);
  a shape that reads at 48 px is often mush at 12 px, and inline button spinners
  live at 12–16 px.
- **Reduced motion hides the animation, not the size.** If the app pins a static
  frame under `prefers-reduced-motion`, verify that branch too — a mark that
  vanishes there looks like a missing control.

## Verification

```bash
node reports/<topic>-harness/size-check.mjs   # PASS + a table of measured boxes
```

Report numbers, not adjectives: "16.09 px inside a 180 px cell (was: full cell),
explicit `size-6` = 24 px, 12 px text → 13.8 px" is a measurement; "looks better
now" is not.
