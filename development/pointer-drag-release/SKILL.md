---
name: pointer-drag-release
description: |
  Guarantee a pointer drag ends even when the release event never arrives. Use when a dragged element sticks to the cursor after the mouse button is let go, when a drag keeps following an unpressed pointer after the cursor re-enters the page, when the user releases outside the window or over another application, or when building any drag interaction on a canvas, slider, divider, resizer, knob, or map. `setPointerCapture` alone does not fix this.
---

# Pointer Drag Release

## Rule

A drag must not depend on a release event arriving. Pointer capture routes events; it does not
promise them. **End** the drag on three independent signals, not one:

1. `pointerup` — the normal exit.
2. `event.buttons === 0` inside `pointermove` — the recovery path when the release never arrived.
3. `lostpointercapture` — the backstop when capture ends without any release event at all.

Miss signal 2 and the element stays glued to the cursor after the user lets go outside the window.

A fourth event, `pointercancel`, is not an exit — see [Cancel is not up](#cancel-is-not-up).

## Why capture is not enough

Mouse pointers have no implicit capture (touch pointers do — the spec captures them to the target on
`pointerdown`). So to keep receiving moves once the cursor leaves the element you need either
`setPointerCapture` or window-level listeners.

Both solve the same problem, and **both fail identically** on the bug above:

|                                                                    | `setPointerCapture` + handlers on the element | `pointerup` on `window` |
| ------------------------------------------------------------------ | --------------------------------------------- | ----------------------- |
| Receives move/up outside the element                               | yes                                           | yes                     |
| Event target stays the element (framework synthetic handlers work) | yes                                           | no                      |
| Suppresses hover/`pointerover` on other elements mid-drag          | yes                                           | no                      |
| Offers `lostpointercapture`                                        | yes                                           | no                      |
| **Release the browser never saw**                                  | **no**                                        | **no**                  |

Prefer capture — it is the spec-blessed route and gives you signal 3 — but understand that neither
listener placement can hear an event that was never dispatched.

## When the release goes missing

A plain mouse-up outside the window is normally still delivered — the browser holds an OS-level grab
for the duration of a drag. The release goes missing when something takes that grab away first:

- An OS surface interrupts mid-drag: Mission Control / Exposé, Cmd/Alt+Tab, a system modal, the
  screenshot crosshair, screen lock, a global-hotkey overlay.
- A native drag-and-drop session starts and replaces the pointer stream — which is exactly what
  `preventDefault()` on `pointerdown` exists to prevent.
- A window manager, remote-desktop session, or VM hands the pointer grab to another surface.
- The tab is throttled or backgrounded across the release.

Once the grab is gone the browser does not know the button came up either, so no amount of listening
helps. The only evidence is the first `pointermove` after the pointer returns, which reports
`buttons === 0`.

## Cancel is not up

`pointercancel` means the interaction was **invalidated**, not finished: the browser took the pointer
over to scroll or zoom, a palm was rejected, the pointer was physically removed. The user never
expressed an intent to land the drag where it stopped.

So the two families deserve different handlers:

| Event                                              | Meaning                  | Action                               |
| -------------------------------------------------- | ------------------------ | ------------------------------------ |
| `pointerup`, `buttons === 0`, `lostpointercapture` | the drag ended           | commit the current value             |
| `pointercancel`                                    | the drag was invalidated | revert to the value at `pointerdown` |

Wiring `onPointerCancel` straight to the up handler is the common shortcut. It is acceptable only
when the drag has no committed value to revert to — otherwise a browser-initiated scroll silently
becomes a user edit.

## Pattern

```tsx
const activeRef = useRef<number | null>(null);
const pointerIdRef = useRef<number | null>(null);
const startValueRef = useRef<number | null>(null);

const handlePointerDown = (event: PointerEvent<HTMLCanvasElement>) => {
  // Capture routes one pointer to this element; it does not stop a second
  // finger from firing `pointerdown` here too. Without this guard the second
  // pointer hijacks the drag and later releases capture for the wrong id.
  if (pointerIdRef.current !== null) return;

  const hit = pick(event);
  if (hit === null) return;

  activeRef.current = hit;
  pointerIdRef.current = event.pointerId;
  startValueRef.current = readValue(hit);
  event.currentTarget.setPointerCapture(event.pointerId);
  // Without this the native text-selection or drag-and-drop gesture starts
  // alongside yours, and a real DnD session will hijack the pointer sequence.
  event.preventDefault();
};

const endDrag = (event: PointerEvent<HTMLCanvasElement>) => {
  activeRef.current = null;
  pointerIdRef.current = null;
  startValueRef.current = null;
  if (event.currentTarget.hasPointerCapture(event.pointerId)) {
    event.currentTarget.releasePointerCapture(event.pointerId);
  }
};

const handlePointerUp = (event: PointerEvent<HTMLCanvasElement>) => {
  if (event.pointerId !== pointerIdRef.current) return;
  commit(activeRef.current);
  endDrag(event);
};

const handlePointerCancel = (event: PointerEvent<HTMLCanvasElement>) => {
  if (event.pointerId !== pointerIdRef.current) return;
  revertTo(activeRef.current, startValueRef.current);
  endDrag(event);
};

const handlePointerMove = (event: PointerEvent<HTMLCanvasElement>) => {
  if (event.pointerId !== pointerIdRef.current) return;
  if (activeRef.current === null) return;
  // A release this document never saw leaves the button "down" as far as the
  // drag state knows. The first move after the cursor comes back carries the
  // truth in `buttons`: no button down means the drag is already over.
  if (event.buttons === 0) {
    handlePointerUp(event);
    return;
  }
  moveTo(activeRef.current, event);
};

// Capture can also end with no release event of any kind — the element being
// detached is the usual way. This fires for every exit, including the ones
// `pointerup` and `pointercancel` miss.
const handleLostPointerCapture = (event: PointerEvent<HTMLCanvasElement>) => {
  if (event.pointerId !== pointerIdRef.current) return;
  commit(activeRef.current);
  endDrag(event);
};
```

```tsx
return (
  <canvas
    onPointerDown={handlePointerDown}
    onPointerMove={handlePointerMove}
    onPointerUp={handlePointerUp}
    onPointerCancel={handlePointerCancel}
    onLostPointerCapture={handleLostPointerCapture}
  />
);
```

## Reproducing and proving it

Do not try to release the physical mouse outside the window — drive the exact event sequence instead,
because the defect _is_ a missing event:

```js
const mk = (type, x, y, buttons) =>
  new PointerEvent(type, {
    bubbles: true,
    cancelable: true,
    composed: true,
    pointerId: 1,
    pointerType: "mouse",
    isPrimary: true,
    clientX: x,
    clientY: y,
    buttons,
    button: buttons ? 0 : -1,
  });

el.dispatchEvent(mk("pointerdown", 100, 100, 1));
el.dispatchEvent(mk("pointermove", 300, 300, 1)); // real drag, button held
// no pointerup — the OS gave the release to someone else
el.dispatchEvent(mk("pointermove", 400, 400, 0)); // cursor comes back, button up
```

Broken: the element follows the last move and any drag-active styling stays on. Fixed: it stops at
the last `buttons === 1` position and the drag state clears. The same script proves the normal path
still works, since the `buttons === 1` move must still move the element.

## Notes

- `buttons` is a bitmask of held buttons, not the button that changed. During any legitimate drag it
  is non-zero, so the check has no false positives. `button` is the wrong property here.
- Pen hover reports `buttons === 0`, but a pen drag only starts on contact (`buttons === 1`), so the
  guard is safe for pen and touch too.
- Signals 2 and 3 are cheap and independent. Add both; neither subsumes the other.
- `window` `blur` looks like a fourth signal but is wrong in both directions, so do not rely on it.
  It under-fires: merely releasing the button over another application usually does not activate that
  application — activation happens on _press_ — so no blur arrives for the exact case signal 2 exists
  for. It over-fires: Cmd/Alt+Tab or a system dialog mid-drag blurs the window while the button is
  genuinely still held. `buttons` reads the pointer's real state rather than the window's focus, which
  is why it has neither failure.
- Escape to revert is worth adding to resizers and sliders. It is a separate concern from release
  (undoability, keyboard access), but it lands on the same `revertTo` path as `pointercancel`.
- Audit siblings once you find one instance. Divider, resizer, and slider drags in the same codebase
  are usually copies of the same incomplete pattern, at different levels of completeness — grade each
  against the three signals rather than assuming the newest one is right.
