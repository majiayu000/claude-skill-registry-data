---
name: dialog-layout
description: >
  Dialog furniture is drawn and aligned by the styled primitives: the
  title sits on a blue nameplate across the sheet's top edge, and the
  DialogActions dock at the foot puts the way out on the left and the
  actions on the right. A dialog has one way out, a button of its own.
  Applies when building or changing any dialog in src/components.
---

The panel's furniture is drawn and aligned by the styled primitives in
`src/components/styled/dialog.tsx`, never per dialog. A dialog is a
white sheet on a soft edge with round, chunky corners and the game's
hard drop, and a handheld's name box on its frame.

- The **nameplate** carries the title, with `lead` as the face in it
  (drawn small, `HeadingPortrait` for a person or a place). It sits
  across the sheet's top edge, outside the part that scrolls.
- Under it the heading row holds the description on the left and
  `aside` on the right. A `quiet` dialog draws neither plate nor row,
  and names itself inside its own content (the catch sheet's bar, the
  safari's field box).
- `DialogActions` is the **dock**: a tinted strip the sheet ends on. The
  way out is written last and drawn first, on the left; the actions
  stand on the right in the order they are written.
- The optional `bar` row under the heading keeps its buttons to the
  **right**, where the rest of the game puts what can be done to a
  thing.

## Rules

- Use `Dialog` and `DialogActions` from `../styled` and the layout
  comes for free. Do not re-align them per dialog, and do not add
  alignment props to `DialogActions`.
- Write the way out (Close, Walk on, Never mind, Cancel, Keep it) last
  in `DialogActions`, so the main action always stands on the right. A
  dialog never has two ways out, and the heading carries no close
  button. Any other row pairing a way out with an action (an inline
  confirm) reads the same way: way out on the left.
- The main action is what the player came to the dialog to do. On an
  ended battle that is leaving it, so Leave battle is the primary on
  the right and Stay and look is the way out.
- Terms a player reads before pressing (price, what they carry,
  stakes) are chips, through `CounterTerms`.
- A control that belongs to the panel rather than its content goes in
  the dock beside the way out (the auction board's Add/Board toggle),
  not in the heading's `aside`.
- The safari is a battle screen rather than a form: a field, a textbox
  that narrates each throw, and a command menu of tiles in place of
  the dock. Its tiles follow the dock's order too: Run, and after an
  encounter Walk on, stand on the left.
