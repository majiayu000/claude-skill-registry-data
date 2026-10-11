---
name: anthill-row-grid-track-overflow
description: "Use when an AntHill .file-list, .change-list or .history-list row shows a stray full-width empty band, a stretched button or a control on its own line, often after enabling Advanced mode, showing files or expanding a row."
---

# AntHill row grids: children outnumbering tracks

## The fault

AntHill's list rows are CSS grids with **fixed track counts** in
`src/AntHill.App/wwwroot/app.css`. Razor rows conditionally render an extra
trailing control, almost always `Advanced`-only. When that control has no
track, CSS grid puts it on an **implicit row** spanning the full width.

Symptom on screen: a wide empty band under every row with one small word
floating in it, a button stretched across the whole panel, or a control
centred on its own line. It looks like a styling nit; it is a track-count bug.

Found three times in one page (source control), same cause each time:

| Row selector | Children in Advanced | Tracks declared | What showed |
|---|---|---|---|
| `.change-list li` | 6 (+ `discard`) | 5 | empty band + floating `discard` |
| `.change-list li.change-file` | 3 (+ `what changed`) | 2 | full-width stretched button |
| `.history-list li` | 5 (+ `what it changed`) | 4 | centred band per entry |

Tracks now (verified 2026-09-24): `.file-list li` 4; `.change-list li` 6 (name, status badge,
shared/held badge, size, file count, discard); `.change-list li.change-file` 3;
`.history-list li` 5.

## Diagnose

1. Count children the Razor row actually renders, **including every
   `@if (Advanced)` branch** and any `else` that emits a spacer such as
   `<span class="uses-blank">`. Non-advanced rows often have one fewer.
2. Count tracks in `grid-template-columns` for that selector. Check for a
   more specific override (`.change-list li.change-file` beats
   `.change-list li`, which beats `.file-list li`), and for `@media` rules: one
   that cuts tracks must hide as many children (`.file-list li` drops to 2
   tracks at ≤620px and hides `.file-when`/`.file-who`).
3. Children > tracks is the bug.

## Fix

Give the trailing control its own `auto` track:

```css
.change-list li { grid-template-columns: minmax(0, 1fr) auto auto 88px 80px auto; }
```

`auto` (not `1fr`): `1fr` is what stretches a button across the panel.

Rows that are genuinely one full-width thing (a confirmation, a diff, an
expanded sub-list) should say so rather than inherit the parent's tracks:

```css
.change-list li.change-discard,
.change-list li.change-patch { grid-template-columns: minmax(0, 1fr); }
```

`.history-list li.revision-changed` (one revision's changes, listed under its row) does the same.

## Verifying: one pitfall that will mislead you

Build a synthetic row with the exact child count Advanced renders; you do not
need the client running. For loading the stylesheet and the `--no-build`
empty-CSS trap, see `anthill-shared-css-verify`.

`getComputedStyle` returns a **live** declaration. Read it *before* detaching
the node, or it reports `none` and you will conclude your fix failed:

```js
await tab.evaluate(`(() => {
  const ul = document.createElement('ul');
  ul.className = 'file-list change-list';
  const li = document.createElement('li');
  for (let i = 0; i < 6; i++) li.appendChild(document.createElement('span'));
  ul.appendChild(li); document.querySelector('.detail-body').appendChild(ul);
  const cs = getComputedStyle(li);
  const tracks = cs.gridTemplateColumns;   // read FIRST
  const rows = [...new Set([...li.children].map(c => Math.round(c.getBoundingClientRect().top)))].length;
  ul.remove();                             // then detach
  return { tracks, rows };
})()`);
```

Proof a row is fixed: all children share one `top` (`rows === 1`). `rows > 1`
means children are wrapping onto implicit grid rows.

## Note

These grids are shared with the Web dashboard, so a track change affects both
surfaces. `AntHill.Web.Tests` renders these components and will catch markup
breakage, but **no test sees a wrapped row**: the markup is valid either way.
Only measurement or a screenshot catches it. `AntHill.Layout.Tests` measures
real layout in a browser but covers no list rows (checked 2026-09-24).
