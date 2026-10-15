---
name: layout-measurement-strategy
description: >-
  Measure and trust the intrinsic or auto layout size of a DOM element. Use when offsetHeight,
  getBoundingClientRect, ResizeObserver, scrollHeight, or a mirror, clone, or probe returns zero,
  border-only, short, or context-dependent geometry. Applies to auto-sized content, virtualized lists,
  masonry grids, tooltips, popovers, badges, overlays, and previews that jump after first render;
  especially when measuring display:none or off-screen content, moving a node to document.body, a
  portal, or shadow DOM, or reading before fonts, images, async children, or flex/grid layout settle.
  Also use when someone constrains the element to height:0 before measuring it. Not for pure CSS
  layout with no JavaScript measurement.
---

# Layout Measurement Strategy

## The one theorem everything follows from

> **A layout size is not a property of an element. It is the output of a function whose inputs are (1) the real inline size the element is resolved against, (2) the full CSS context imposed by its ancestors and formatting context, and (3) the readiness of its content. Pin all three to their real-render values or you have measured a _different function_, not the same element more cleanly.**

Auto **block-size** (height, in horizontal writing modes) is a function of **inline-size** (width): text wraps, container queries flip, flex/grid constraints resolve — all against the available inline size. Change the width, the context, or read before content is ready, and the number is **confidently wrong**.

The trap that makes this hard: **the browser never signals that a layout is provisional.** There is no `isLayoutFinal` flag. An early or mis-contexted read returns a plausible-but-wrong number _silently_ — which is worse than an error, because downstream code commits it.

## The two failure modes (90% of real bugs)

1. **No box / collapsed box.** `display: none` generates no layout box (measures `0`). Or the element is in flow but its content hasn't expanded it yet, so it's only `border-top + border-bottom` tall — the **border-only** read (1–2px). This is the collapsed-widget bug below.
2. **Wrong constraint.** Measured at a different width, missing CSS variables/fonts/ancestor classes, or moved to a different parent (`document.body`) where the cascade and formatting context differ.

## The mindset shift: from "measure now" to "observe and settle"

Do not ask "when is the right instant to read the size?" — you will guess wrong, because content arrives late (fonts swap, images load, async children stream). Instead:

- **Producer:** subscribe with a `ResizeObserver` and take the _settled_ value. RO fires after layout, before paint, and **re-fires on every change** — first layout, font swap, image load, stream chunk. It turns "is the geometry final?" from a guess into an event.
- **Consumer:** apply a **reject-border-only guard** (below). Even a correct producer gets its value grabbed early by some eager consumer. The consumer must refuse a collapsed number, not assume what it received is real.

The border-only failure is defeated only by **both halves** — waiting for the real value _and_ refusing to commit the collapsed one.

## Before you measure: can the layout engine do it?

The cheapest measurement is the one you never take. If the browser can size or position the thing for you — a corner badge with `position: absolute; top/right` (needs no height at all), content-driven height with CSS grid/flex, space reserved with `aspect-ratio` or `contain-intrinsic-size` — do that instead of reading geometry into JS. Every measured number is at least one frame stale and becomes its own bug surface (the collapse, the font/image race, the re-render lag). Reach for measurement only when a value genuinely has to cross into JS to drive something the layout engine can't express.

## Decision spine

1. **In the DOM, not `display: none`.** `visibility: hidden` and `position: absolute` keep the layout box (they still lay out); `display: none` has none. Detect it: `el.offsetParent === null` or `offsetHeight === 0`.
2. **Fix the real _inline_ size; read the _block_ size.** Height is a function of width. Think logical axes (`inline-size` / `block-size`), not physical width/height, so RTL and vertical writing modes don't silently measure the wrong axis.
3. **Default to in-place or portal-in-subtree. Off-flow is the exception.** In-place measurement replicates _nothing_ because nothing moved — it keeps the containing block, formatting context, query container, inherited vars, and shadow stylesheets. Reach for off-flow only when the size is genuinely content-driven _and_ you need the number synchronously before paint.
4. **If off-flow: replicate context, don't copy computed styles.** Reproduce the ancestor chain, not a snapshot of resolved lengths (copying `getComputedStyle` freezes `%`, `em`, `ch`, `fit-content`, and kills container queries).
5. **Reject border-only / collapsed measurements.** A content-bearing element measuring to ~chrome height means _layout hasn't happened yet_, not _height is 0_. Never feed it to badges, radii, insets, or animations.
6. **Cooperate for lists/previews: measure once, cache, feed it back.** `content-visibility: auto` + `contain-intrinsic-size: auto <last-size>` lets the browser hold the space and self-correct — instead of re-measuring on every reveal or betting a fixed placeholder height.

## Why "height: 0" and "append to body" are the wrong defaults

- **`height: 0` on the element you're measuring** — under `overflow: hidden`, flex/grid, or percentage-height parents, you read back the _constrained_ `0`, not the intrinsic size. Keep the measured element `height: auto`; move a **placeholder** to control flow, not the content.
- **Appending the probe to `document.body`** — silently drops CSS custom properties (the most common thing to revert), ancestor classes that drive descendant selectors (`.dark`, `[data-density]`, `:has()`), the `@container` query context, and any shadow-root `adoptedStyleSheets`. You measured a different element than the one you'll render.

## What corrupts a naive off-flow measurement (the CSS mechanisms)

The cases where measurement is _hardest_ are exactly the cases where the **real layout, not the element, owns the size** — so there is no clean intrinsic number to extract off-flow:

- **Percentage / flex-basis heights** resolve against a _definite_ containing block. Off-flow under an `auto`-height wrapper, they resolve to `auto` → different number. Strongest argument for in-place.
- **Flex/grid children** carry `min-height: auto` (won't shrink below min-content unless you set `min-height: 0`) and, with `align-items: stretch` (default), are stretched to the line's cross size — so you measure the _container_, not the item. Off-flow removes the stretch, giving content size. Neither is "wrong"; name which one you want. **This is the collapsed-widget mechanism.**
- **`aspect-ratio`** makes block-size a function of resolved inline-size — unmeasurable before width is final.
- **`contain: size` / `content-visibility`** make size independent of contents _by contract_ → measures `0` (or `contain-intrinsic-size`). `content-visibility: auto` skips layout while off-screen — putting a probe off-screen defeats itself. Check ancestors for these.
- **Container queries** resolve against the nearest `container-type` ancestor's inline size. Off-flow, that container is gone or wrong-sized → styles flip → wrong height. To measure off-flow you must reproduce `[container @ real inline-size] > [node]` and keep the width in sync — at which point in-place is cheaper and correct.

Full context-replication travel list and the container-query / shadow-DOM details are in `references/context-replication.md`.

## Choosing the measurement API

| Need                                                         | Use                                                 | Notes                                                                                                                                      |
| ------------------------------------------------------------ | --------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| "Notify me when the real size settles" (fonts/images/stream) | **`ResizeObserver`** (`borderBoxSize[0].blockSize`) | Fires after layout, before paint; re-fires on every change; hands you the value **without forcing a reflow**. The default for auto-height. |
| Fractional visual size, **no transforms** in the chain       | `getBoundingClientRect().height`                    | Sub-pixel float; **includes transforms** (a `scale(0.5)` reports half). Forces a sync reflow.                                              |
| Transform-immune integer layout size                         | `offsetHeight` / `offsetWidth`                      | Ignores transforms; **rounds to integer** (don't sum many). Border-box. `0` ⇒ `display:none`.                                              |
| Learn the CSS context to replicate                           | `getComputedStyle()`                                | Use for _non-geometric_ facts (font, custom props). Also forces a reflow for layout props — not free.                                      |

Box consistency: `getBoundingClientRect` / `offset*` are **border-box**; `contentRect` / `clientWidth` are **content-box**. Pick one box and stay in it end-to-end. When feeding a measured height back into layout, `Math.ceil` it — a rounded-down height crops the last text line.

**Margins are in none of these boxes**, and a child's top/bottom margin can _collapse through_ an auto-height wrapper — so the measured box comes back short by the collapsed margin. Give the measured wrapper its own block formatting context (`display: flow-root`) so child margins stay inside the number, or measure an element you know establishes a BFC.

## Timing

| Situation                                                                           | Primitive                                                             | Why                                                                                                                                                                       |
| ----------------------------------------------------------------------------------- | --------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Height depends only on a width you set; content already in DOM; no web fonts/images | **Forced reflow**: write width → read `offsetHeight` in the same task | The read's synchronous flush honors the pending write. Deterministic, no frame wait.                                                                                      |
| Just inserted / unhid synchronously; want the settled box                           | one `ResizeObserver` callback (preferred) or double-`rAF`             | Give the engine a committed layout pass. RO waits for the _actual event_; double-rAF waits a fixed 2 frames that may be too short (async content on frame 3) or wasteful. |
| Text with web fonts                                                                 | `await document.fonts.ready` before trusting                          | Fallback metrics give shorter, provisional line boxes.                                                                                                                    |
| Images / replaced content contribute to height                                      | `await img.decode()` / `load`, or let RO catch the reflow             | 0 intrinsic size until the resource resolves.                                                                                                                             |
| Measuring N nodes                                                                   | **Batch: all writes, then all reads**                                 | One forced layout total vs O(N). Never issue a layout-dirtying write between reads.                                                                                       |
| Feeds a _visible_ size change                                                       | `useLayoutEffect` / RO, not `useEffect`                               | Runs after commit, before paint → no flash of the un-sized state.                                                                                                         |

## The reject-border-only guard

A measurement pipeline needs a **validity predicate, not just a value.** All the early-read failure modes collapse the number _toward_ border-only/zero, so a lower-bound plausibility check catches them:

```ts
// content-box contribution ≈ 0 while the element HAS content ⇒ layout hasn't
// happened yet. Treat as "not measured," not "height is 0."
function isTrustworthy(borderBoxH: number, chromeH: number, prev?: number): boolean {
  if (!Number.isFinite(borderBoxH) || borderBoxH <= 0) return false;
  if (borderBoxH - chromeH <= 1) return false; // border-only
  if (prev != null && borderBoxH < prev * 0.25) return false; // implausible collapse
  return true;
}
```

Commit a value only when it **passes the predicate** _and_ is **stable across two consecutive RO deliveries** (RO fires on every reflow, so stability-across-two is the practical "settled" signal). Then disconnect the observer.

## Case study — a collapsed widget preview

The widget body is a flex/grid child. The host chrome laid out first and resolved the row before the body had content to contribute, so the auto-height body collapsed to `border-top + border-bottom` (~1–2px). The preview read that 1–2px as "the height" and drew the Stage badge against a ~0-height box — the badge detached from its corner.

Both halves of the fix were required:

1. **Producer:** measure the auto-height tile **off-flow with `height: auto` at a fixed real width**, so it sizes to its own content instead of the stretched/constrained row.
2. **Consumer:** the preview **rejects border-only measurements** and waits for a real height before it enters normal flow and positions the badge.

The general principle: _a valid intrinsic measurement must contain a non-zero content contribution when the element has content._ Border-box minus chrome ≤ ε ⇒ "layout hasn't happened," not "size is 0."

## Pre-trust checklist

- [ ] Has a layout box (not `display: none`).
- [ ] Measured at the **real inline size**, including the final scrollbar-gutter state.
- [ ] Same CSS context: custom properties, fonts, ancestor classes, `@container` ancestry, shadow `adoptedStyleSheets`. (Moved to `body`? You almost certainly broke this.)
- [ ] Content is real: fonts loaded, images have dimensions / `aspect-ratio`, async children arrived — or you're taking the RO **settled** value.
- [ ] Right box + deliberate rounding (`Math.ceil` for a container that must not clip).
- [ ] No transform in the chain contaminating a `getBoundingClientRect` read (else use `offsetHeight`).
- [ ] Passed the reject-border-only guard.
- [ ] No RO feedback loop (callback doesn't resize the observed box, or bails when unchanged).

## Copy-pasteable patterns

React/TS hooks + vanilla equivalents — **(A)** in-place placeholder + hidden content (the default), **(B)** off-flow probe, **(C)** the settle loop and batched N-node measurement, plus **animating a container to its content height** and the **React re-render-clobber** gotcha — are in `references/measurement-patterns.md`. Read it when you need working code rather than the strategy.
