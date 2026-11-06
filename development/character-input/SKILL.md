---
name: character-input
description: "Keyboard actions and pointer look for a character controller in the browser: rebindable action map, edge-triggered presses, drag or pointer-lock look deltas, right-button turn, wheel steps. Use when wiring WASD/jump/crouch/sprint and mouse look into any Three.js scene. Ships character-input.js."
---

# Character input

Target: browser DOM events; no framework. `scripts/character-input.js` exports
`createCharacterInput(canvas, opts)` and `defaultActions()`.

## Actions, not keys

Code asks for actions (`moveForward`, `jump`, `crouch`, `sprint`, `interact`...), never
key codes. The action map is a plain mutable object of `action → [KeyboardEvent.code]`;
rebind by assigning `input.actions.jump = ['KeyJ']`. Defaults:

| Action | Codes |
| --- | --- |
| moveForward / moveBack / moveLeft / moveRight | W A S D and the arrows |
| jump | Space |
| sprint | ShiftLeft, ShiftRight |
| crouch | KeyC |
| interact / use | KeyE |
| secondary / carry | KeyF |
| tertiary / stow | KeyG |

`getMove()` returns `{ x, z }` in −1/0/1 (x right, z back, so forward is −z, matching
camera space). It is a shared object; read it before the next call.

## Held versus pressed

- `isAction(name)` is true while any bound key is down.
- `wasPressed(name)` is true for exactly one frame after the key went down, ignoring
  auto-repeat. Jump, interact and view toggles use this.

Presses are cleared at the end of the frame, not when read, so several systems can see
the same press. Call `input.endFrame()` after all updates in your loop (or pass an
`onLateUpdate` hook in `opts` if the host loop has one).

## Look

Two modes, switchable at runtime with `setLookMode('drag' | 'capture')`:

- **drag**: left button held and dragged on the canvas moves the look. Works
  everywhere, including iframes and embedded previews.
- **capture**: pointer lock on click; raw `movementX/Y`. Can be refused by the browser;
  the request is made with `.catch` and nothing waits on it. Esc releases.

`consumeMouseDelta()` returns `{ dx, dy }` in pixels accumulated since the last call
and zeroes it. Consume exactly once per frame in the camera update.

The right button gives a separate `consumeTurnDelta()` for rotating a held object or
similar, so it never fights the look.

`consumeWheel()` returns the signed count of wheel notches since the last call (zoom
steps).

## Hygiene

- Keys typed in inputs, textareas, selects and contenteditable elements are ignored.
- Space and the arrows call `preventDefault` so the page does not scroll.
- `blur` resets everything held, so a key does not stay down after alt-tab.
- The context menu is suppressed on the canvas (right button is a control).
- `dispose()` removes every listener.
