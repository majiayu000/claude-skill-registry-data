---
name: hover-action-focus-navigation
description: Design hover-revealed actions that behave correctly across pointer clicks, keyboard focus, and focus-visible navigation. Use when cards, rows, tree items, list items, or tiles reveal menus or secondary actions on hover and must avoid sticky actions after mouse clicks without breaking Tab navigation.
---

# Hover Action Focus Navigation

## Principle

Treat pointer presence, DOM focus, and keyboard-visible focus as different states:

- `:hover` reveals contextual actions while the pointer is over the owner.
- `:focus` is browser state, not proof that a focus indicator should remain visible; mouse clicks commonly leave it behind.
- `:focus-visible` represents keyboard-style navigation and should reveal the relevant action and focus treatment.

Do not use broad `:focus-within` to keep a hover action visible. It also matches ordinary mouse-click focus, which makes the action appear stuck after the pointer leaves.

## Ownership

Give each focus state a precise owner:

- When the primary card or row is `:focus-visible`, reveal its secondary action.
- When the secondary action itself is `:focus-visible`, keep that action visible.
- When either control has only ordinary mouse focus, let visibility return to the hover rule.
- Pressing a secondary action must not trigger the primary surface's active state.

Prefer direct-child selectors, `peer`, or narrowly scoped `:has()` rules over container-wide focus propagation. This prevents one nested control from lighting up unrelated parent states.

## Expected State Model

| Input state                       | Secondary action | Primary active feedback |
| --------------------------------- | ---------------- | ----------------------- |
| Pointer over owner                | Visible          | No                      |
| Pointer presses primary control   | Visible          | Yes                     |
| Pointer presses secondary action  | Visible          | No                      |
| Pointer leaves after mouse click  | Hidden           | No                      |
| Keyboard focuses primary control  | Visible          | No                      |
| Keyboard focuses secondary action | Visible          | No                      |

## Verification

Test real input paths separately:

1. Click the primary control, move the pointer away, and confirm the action hides.
2. Click the secondary action, move the pointer away, and confirm it hides despite retained DOM focus.
3. Navigate with Tab and confirm both primary and secondary `:focus-visible` states reveal the action.
4. Confirm the primary focus outline follows the owner's visual geometry, not an unrounded inner button.

The invariant is simple: mouse focus must not create persistent hover UI; keyboard focus-visible must remain discoverable.
