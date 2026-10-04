---
name: action-forms
description: >
  A dialog that asks the player something and hands an answer back is an
  action form: `openForm(Form, input)` from anywhere, awaited, null when the
  player walks away. An NPC is one folder under `src/overworld/npcs`: `createNpc` in its
  `index.ts` and the script it loads, which talks through a conversation of
  forms. Applies when adding a question dialog, an NPC, or changing what an
  NPC does.
---

A question is a promise. `src/components/forms` holds the forms, the stack they
open on and the one `FormHost` the app draws them in.

## Forms

- A form is `defineForm({ title, prompt, view })`. The view draws only its own
  content and its `DialogActions`; the frame (nameplate, the line under it) is
  whoever opened it. It ends with `submit(answer)` or `cancel()`, and its way
  out says `leave`.
- `openForm(Form, input)` opens it over whatever is up and resolves with the
  answer, or null. Only the top frame shows, so a form opened from inside
  another dialog's flow never fights it for the closing click.
- A form that needs a record declares the resource and reads it in a child
  under its own `Suspense` with a fallback, so a conversation's line stays up
  while it loads.
- Reach for the generic ones before writing a new one: `choose`/`choiceForm`,
  `PickCatchForm`, `PickItemForm`, `PickMoveForm`, `PickBoxForm`,
  `TeachMoveForm`.

## NPCs

- One folder per role under `src/overworld/npcs`. `index.ts` is
  `createNpc(Npc.X, { name, description, quote, spent, sprites, visit, wanders,
  shop, interact: () => import('./interact') })`, and `interact.tsx` beside it
  is the script. Add the folder to the `Record` in `src/overworld/npcs/index.ts`.
- `interact` stays a loader. The server and world generation read the
  definitions, and a static import would hand them every form and picker the
  script asks through.
- `wanders` puts a role in the wandering roll, which is world generation: a
  new wanderer moves who stands on every existing cell, so it is a deliberate
  change with its test updated.
- A script is `(visit) => Promise<void>`. It talks through `visit.say`,
  `visit.ask` and `visit.form`, reads the purse and bag through
  `visit.gold`/`bag`/`carrying`, and reports arrivals with `visit.notify`.
  Roles that share one script (the shops) point `interact` at it.
- A null from a step is the player declining; the script decides whether that
  ends it or steps back. A player who walks away ends the script where it
  stands, so no step needs to check.
- A once-a-window NPC (`visit` in its definition) says its `spent` line instead
  of running the script when the server has already served the player.
- The script is presentation. Everything it changes goes through a server
  function that derives the NPC again from the cell and refuses on its own.
