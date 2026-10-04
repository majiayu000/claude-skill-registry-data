---
name: effect-props
description: >
  An effect wakes on its sources changing, not on its answer changing.
  A component whose effects do stateful work — loading a sheet, starting
  a playhead, opening a subscription — reads those props through memos,
  so a caller that rebuilds its list does not restart everything in it.
  Applies whenever writing or reviewing a component with a
  `createEffect` fed by props.
---

`createEffect` re-runs when a signal it read updates, whatever the new value is. Reading `props.species` inside an effect subscribes the effect to whatever that prop is derived from, so an unchanged species still wakes it if the accessor behind it changed.

That happens constantly in lists. A box of thirty squares rebuilds every entry when one of them is picked or a page turns, and every square's props are new objects saying exactly what they said before. An effect that reloads a sheet, calls `play()` on a playhead or opens a subscription then does all of it again, thirty times, for nothing. What the player sees is the whole box flinch.

## The rule

Props that an effect reads go through a memo first, and the effect reads the memo.

```tsx
// Wakes whenever the caller rebuilds its entries
createEffect(() => {
  load(props.species, props.shiny === true).then(setSheet);
});

// Wakes when the species or the coat actually changes
const drawing = createMemo(() => props.species);
const sparkling = createMemo(() => props.shiny === true);

createEffect(() => {
  load(drawing(), sparkling()).then(setSheet);
});
```

A memo propagates on `===`, so one over a primitive stops the churn dead. Keep one memo per value rather than one over an object: an object memo is a new object every time and propagates as freely as the prop did.

## When it does not matter

Reading props straight is right in JSX and in memos, which recompute cheaply and settle by value. This is about effects, and among effects only the ones whose re-run costs something or throws away state: a fetch, a playhead, a canvas, a timer, a subscription. An effect that only writes a signal from a value can read props as it likes.
