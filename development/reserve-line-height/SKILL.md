---
name: reserve-line-height
description: |
  Reserve one line of height with `min-height: 1lh` so conditionally rendered text or swapping content (error lines, inline status, button spinner) doesn't cause vertical layout shift. Use when building rows that may be empty, or containers whose content toggles between a text label and a loading indicator of different height.
---

# Reserve Line Height

## Rule

Any slot whose visible content is optional or swaps between variants of different intrinsic height should reserve exactly one line of height up front with `min-height: 1lh` (`min-h-[1lh]` in Tailwind).

## Why `1lh`

`1lh` resolves to the element's own computed `line-height`, so the reservation:

- Scales automatically with the `text-*` utility on the same element.
- Stays a pure layout constraint — no placeholder glyphs in the DOM for assistive tech to announce.
- Survives font and leading changes without magic pixel values.

## Pattern A — Optional text (error, hint, helper)

The row must occupy one line whether `error` is truthy or not:

```tsx
// Always reserves one line of height at the row's own text size.
<p className="min-h-[1lh] text-sm/5 text-red-600">{error}</p>;
```

If the surrounding layout risks collapsing an empty element (some nested flex parents do), keep a non-breaking space as a defensive backstop:

```tsx
<p className="min-h-[1lh] text-sm/5 text-red-600">{error ?? "\u00A0"}</p>;
```

## Pattern B — Label ↔ spinner swap

When a button or inline slot swaps a text label for a loading spinner, the spinner is usually shorter than the label's line-height, so the row collapses on the transition. Pin the container to `1lh` at the text size; the spinner centers within it:

```tsx
<button className="flex min-h-[1lh] items-center justify-center text-sm/5">
  {isLoading ? <Spinner className="size-3" /> : "Resend code"}
</button>;
```

The same treatment applies to anything swapping between states of different heights on the same line: inline status, countdown timers, icon-only indicators replacing a label.

## Don'ts

- Don't hard-code the reserved height in pixels (`min-h-[20px]`) — it drifts the moment text size, font, or leading changes.
- Don't set `height`; the row must still grow when content wraps.
- Don't rely on `&nbsp;` alone without `min-h-[1lh]`; empty strings still collapse the row in many layout contexts.
