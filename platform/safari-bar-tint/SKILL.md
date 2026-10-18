---
name: safari-bar-tint
description: Make iOS 26+ Safari tint its status bar and floating tab bar to match the page, so a site looks native in Safari instead of sitting between white or grey bars. Covers how Safari picks the tint (root background, fixed and sticky elements near the edges, theme-color being ignored), auditing headers, cookie banners and hidden overlays that hijack the tint, glass headers, viewport-fit=cover, and a real-device rollout gate. Use when building or reviewing any site for mobile Safari, when the bars are white, grey or the wrong colour, when a cookie banner or modal turns the bars dark, or when theme-color "does nothing". For general mobile web feel (tap highlight, 100vh, input zoom) use mobile-native.
---

# Safari Bar Tinting (iOS 26+)

Goal: the status bar at the top and the area around Safari's floating tab bar
take the page's own colours. The mechanism is undocumented by Apple; everything
below is community reverse-engineering (sources at the end) plus our own
failure, so the real-device gate at the bottom is not optional.

## What went wrong the first time (2026-10-15)

We followed <https://joshpuckett.me/seamless-mobile-safari>: empty
`.edge-top` / `.edge-bottom` divs with a `position: fixed` coloured `::after`,
`max(12px, env(safe-area-inset-*))` tall. Shipped to seven sites, reverted the
same day:

* **Safari ignores `::before` / `::after` when sampling.** The div itself had no
  background, so Safari never used the strips. They were just visible bars.
* **The 12px minimum is visible everywhere**, desktop included, and over any
  content that scrolls under it.
* The bottom one sat as a band above the floating tab bar and moved with it.
* Colours were picked from design tokens, not from rendered pixels.
* Verified only in the iOS Simulator, then fanned out to every site at once.

Never add decorative edge strips again. Work with what Safari actually samples.

## How Safari 26 picks the tint

1. **`theme-color` is ignored** by iOS 26 Safari. Keep it for Chrome on Android
   and older Safari, never rely on it for iOS.
2. **Fixed or sticky elements at an edge win.** Safari reads `background-color`
   (and `backdrop-filter`) of a `position: fixed` / `sticky` element that sits
   within about 4px of the top or 3px of the bottom and spans about 80% of the
   width. The element's own box counts; pseudo-elements and absolutely
   positioned children do not.
3. **They count even when invisible.** `opacity: 0` and `pointer-events: none`
   do not exclude an element. A closed cookie banner, drawer or modal backdrop
   left in the layout keeps tinting the bars.
4. **Otherwise the root background.** With no qualifying fixed element, Safari
   falls back to the `html` / `body` background. Transparent or unset falls back
   to white (light) or black (dark), which is the classic "white bar".
5. **Images and gradients are not extended.** At `scrollY = 0` a photo hero gets
   the root background colour behind the status bar, not the photo.

## The recipe

Do these in order and stop as soon as the bars look right on a device.

1. **Viewport.** `<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">`.
   Without `viewport-fit=cover` a solid bar fills the bottom safe-area gap. Add
   `env(safe-area-inset-*)` padding to fixed headers, footers and CTAs so nothing
   hides under the notch or the tab bar.
2. **Explicit, opaque root backgrounds.** `html` gets the colour of the top of
   the page (header or first section). `body` gets the page's base colour. Both
   per theme (light and dark). Never transparent, and never changed at runtime:
   transparent sections show `body` through them.
3. **Audit every fixed and sticky element** (`rg -n 'fixed|sticky'`). For each one
   touching the top or bottom edge, decide if its colour should tint the bar:
   * Solid header you want in the status bar: leave it, it already works.
   * Glass or translucent header: keep the fixed element itself transparent
     and move the background and blur to an `aria-hidden`, absolutely
     positioned child with the nav content above it. Otherwise Safari tints the
     bar with a half-transparent colour.
   * Cookie banners, drawers, modals, backdrops, toasts: `display: none` when
     closed, not `opacity: 0`. To animate: set `display: block`, add the open
     class on the next frame; on close remove the class and set `display: none`
     after the transition ends.
4. **Photo or video heroes.** Set `html`'s background to the dominant colour of
   the photo's top edge as a phone crops it (sample rendered pixels from a
   device screenshot, not the source file and not a token). Accept that this is
   an approximation; do not paint anything over the photo to "fix" it.
5. **`theme-color`** per theme with `media="(prefers-color-scheme: …)"`,
   matching `html`, for other browsers.

What not to do:

* No decorative strips, bars or pseudo-elements at the edges.
* No `body { overflow: hidden }` in a page shell; keep `html` scrollable.
* No runtime colour swapping of `html`/`body` on scroll unless a device test
  shows the static colour is wrong and the swap is invisible on desktop.

## Rollout gate

1. Apply to ONE site first.
2. Check on a real iPhone running iOS 26+: top and bottom at rest, scrolled,
   tab bar expanded and collapsed, overscroll at both ends, light and dark,
   every overlay open and closed. The simulator is a first pass only.
3. Check on desktop that nothing visible changed.
4. The user confirms on their phone. Only then apply to the next sites, one
   commit per site, and ship them one at a time.

## Sources

* Josh Puckett, <https://joshpuckett.me/seamless-mobile-safari> (the original
  strip technique; its `::after` strips did not survive a real device for us)
* <https://1ar.io/updates/safari-26-liquid-glass-web/> (sampling rules,
  thresholds, hidden-overlay and white-bar fixes)
* <https://benfrain.com/ios26-safari-theme-color-tab-tinting-with-fixed-position-elements/>
  (theme-color dropped, fixed popovers and dialogs hijacking the tint)
