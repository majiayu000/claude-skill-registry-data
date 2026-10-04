---
name: dialog-transitions
description: >
  The `Transition` around a dialog decides when it is mounted and
  nothing else — the fade belongs to the `TransitionChild` overlay and
  panel inside it. Applies whenever adding or changing a transition in
  `src/components/styled`, or giving a dialog an animation of its own.
---

A dialog is wrapped in one `Transition` and holds two `TransitionChild` elements. The wrapper is the **coordinator**: it says when the dialog exists. The children are what animate.

## Rule

Never give the parent `Transition` enter/leave classes — no `{...FADE}`, no `enter`/`leave` of its own. Put the animation on the overlay and the panel.

```tsx
// Right: the wrapper only mounts and unmounts
<Transition appear show={props.isOpen}>
  <HeadlessDialog isOpen unmount={false} onClose={props.onClose}>
    <TransitionChild {...SHEER} class="fixed inset-0">
      <DialogOverlay class="size-full …" />
    </TransitionChild>
    <Suspense>
      <TransitionChild {...FADE} class={PANEL}>
        <DialogPanel class="contents">…</DialogPanel>
      </TransitionChild>
    </Suspense>
  </HeadlessDialog>
</Transition>

// Wrong: the wrapper animates too
<Transition appear show={props.isOpen} {...FADE}>…</Transition>
```

## Why

- **Opacity multiplies.** A panel at 0.5 inside a wrapper at 0.5 is drawn at 0.25, so an animated wrapper makes every child fade faster than it was told to and on a curve nobody wrote.
- **The wrapper is the clock.** Terracotta unmounts once the wrapper's own transition is over. Give the wrapper a transition and it can finish first, cutting a child's longer one off mid-fade; children that want different timings — an overlay slower than the panel — stop being possible.
- **It is a screen-wide layer.** The wrapper is a bare `div` around fixed-position children. Opacity on it makes one stacking context over the whole page and flattens the dialog into a single painted layer, which loses the panel's shadow over the overlay.

## Where the Suspense goes

The boundary is the panel's `TransitionChild` wrapper, inside the styled `Dialog` and with **no fallback**: a panel waiting on a read leaves the overlay and the frame it was opened in standing, and arrives when it has something to show. The slots (`title`, `description`, `lead`, `aside`, `bar`) are resolved inside it too, so a heading that reads a record does not suspend the screen the dialog was opened from.

A dialog that needs a resource therefore declares it and hands it to a body component, and writes no `Suspense` of its own. One written around the dialog reaches the whole screen instead.

Anything **refetched after a write** is read through `.latest`, not by calling the resource. A refetch suspends every plain read of it, and from inside the panel that detaches the panel mid-write: marking a favorite would blink the sheet for the length of one round trip. `latest` still suspends the first time, which is what makes the panel wait for its first record.

## Around it

- The fades live in [`transition.ts`](../../../src/components/styled/transition.ts), spread into each child. `FADE` fades **and grows**, and is for a **dialog's panel** and nothing else. Everything else takes `SHEER`, the same fade with no scale: the overlay, anything placed against the window (hover cards, tooltips), and anything dropped from the control that opened it — a popover, a listbox, a combobox. Two reasons to keep the scale off those: a list dropped from a button grows from the button rather than from itself, and a scale is a transform, which makes the element the containing block for anything `fixed` inside it — that put a hover card a whole viewport down the page.
- **Never put `inert` on anything a `Transition` or `TransitionChild` wraps.** Terracotta drives focus into a panel once it has entered and closes it again when focus leaves; an inert subtree refuses the focus, and the panel shuts the instant it opens. A dialog on its way out keeps `pointer-events-none` while it fades, and `data-open` is how anything outside tells an open dialog from a leaving one.
- Tailwind's `scale-*` sets the **`scale`** property, not `transform`. A transition naming `transform` animates nothing and the panel appears at full size, so `FADE` names `scale`.
- A `PopoverPanel` given `as={TransitionChild}` **never mounts**. The panel and the transition each decide separately whether to render, and the two do not agree; a `DialogPanel` and a `DialogOverlay` are fine that way, a popover's is not. Wrap the panel in the `Transition` and leave the panel itself plain.
- Write a transition as a **wrapper** rather than as `as={TransitionChild}` on the thing it animates: `<TransitionChild {...FADE}><DialogPanel class="contents"/></TransitionChild>`. The wrapper carries the placement and the fade, and the terracotta part inside it is boxless, so a scale has no second box to fight over. The polymorphic form works from terracotta 1.2.2; before it, a `PopoverPanel` written that way mounted nothing at all.
