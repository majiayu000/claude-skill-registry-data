---
name: img-to-slice
description: Convert a photo or screenshot of an Event Model board (Miro, Excalidraw, whiteboard, paper) into Uncanvased YAML slice files, one per vertical slice, then run a question-by-question gap review to complete the model. Use when the user supplies an event model image, re-parses an updated board, wants existing slices reviewed for gaps, story order, streams or missing specs, or mentions forward-pass or generating slice YAML from a picture.
---

# Event Model image → Uncanvased slices

The YAML is the source of truth. Write only YAML.

An event model is a **storyboard**: read left to right, it tells one story of the system over time. Screens show real data, every field can be traced to the event it came from, events sit in lanes per stream, and every slice is backed by Given / When / Then specs. Transcribe toward that; the gap review completes it.

## Workflow

**Review mode**: invoked with no image (e.g. `review`) → skip steps 1–4 and run the gap review over every file in `slices/`, then summarize as in step 6.

1. If `slices/` is not empty, ask whether the image is the whole board or a fragment ([UPDATE.md](UPDATE.md) §0).
2. Transcribe only what the image shows. Cut the timeline into slices and classify each by `pattern`.
3. Attach Given-When-Then sub-diagrams and white notes to their slices ([REFERENCE.md](REFERENCE.md)).
4. Write one file per slice into `slices/` using the [REFERENCE.md](REFERENCE.md) templates. Reconcile existing slices first ([UPDATE.md](UPDATE.md)).
5. Run the gap review ([GAPS.md](GAPS.md)).
6. Reply with a summary, no YAML:
   - files written or changed (`id` + path + title); slices kept unchanged
   - gap tally (fixed / deferred / ignored) and deferred section A gaps, including earlier runs'
   - events not yet read by any view
   - timeline changes (slices moved in the story) and event streams
   - gap-review additions to **redraw on the board**
   - deferred questions and hotspots as an **agenda for the next modeling session**

## File format

- Raw YAML only: no code fences, no prose.
- Filename: kebab-case slug of the title + `.yaml` (`Add List` → `slices/add-list.yaml`). No numbering. Same title = same slice. Use `-2`, `-3` only when two different slices in this run share a title.
- Every slice has a stable `id` ([REFERENCE.md](REFERENCE.md)): never renumbered, never reused.
- Never overwrite silently: existing files change only via [UPDATE.md](UPDATE.md) or an accepted gap fix.
- Names: sticky text in PascalCase (`Order Placed` → `OrderPlaced`). Same text, same name. Keep spelling; mark a likely typo `# ?`.
- Unreadable type → `string`. Illegible value → keep the label, add `# ?`.
- Slice id badge: a small number in a sticky's corner (as drawn by `slice-to-diagram`) is the slice `id`, not a note and not a `sequence`. `12·13` on a screen means the screen belongs to slices 12 and 13.
- Other badges, stars, `*` or annotations → trailing `# note: <text>`.

## Reading the board

Colors are hints, not proof. Slice id badges are proof: stickies sharing a badge belong to the same slice; a sticky without one is new on the board.

| Block | Looks like |
|---|---|
| Event | yellow/orange sticky, past tense |
| External event | pink sticky, `(External)` label, or in an external-system lane |
| Command | blue sticky, imperative |
| Read model | green sticky |
| Processor | ⚙️ cog / gear / robot |
| UI | wireframe (fields, buttons, tables); a filled-in value (`Compact`, `42310`) → `example:` on that input / output |
| Note | white sticky |
| Hotspot | red sticky: an open question, not a block; `# todo: hotspot: <text>` on the nearest node |
| Spec | `GIVEN` / `WHEN` / `THEN` rows, or a dashed frame of small stickies under a slice ([REFERENCE.md](REFERENCE.md) Scenarios) |
| Field list | `field: type` lines under a sticky's name → its `fields` / `payload`; `(tag)` → also in `tags` |
| Duplicate | hatched / dashed event marked `(duplicate)`: a copy of an event drawn elsewhere, never a new event or slice |
| Loop note | `cleared by X` / `updated by X` under a read model: X is in its `sources` |

Swimlanes: a UI lane label is the `actor`; an event lane label (`EVENTS · Booking` → `Booking`) is the `context`, the event stream; a lane named after a foreign system holds external events or an automation's `external_call` (`system`).

## Patterns

- **state_change**: UI → Command → Event.
- **state_view**: Event(s) → Read Model (→ UI). Every read model box gets its own `state_view` slice, including to-do lists feeding a ⚙️, except a translation's read model, which lives only inside the translation slice.
- **automation**: Read Model → ⚙️ → Command → Event.
- **translation**: External Event → Read Model → ⚙️ → Command → internal Event. Only a translation's read model may consume an external event.

A processor calling a 3rd-party API ("GET Salesforce Account") is an automation with `external_call`, not a translation.

**Actor:** the lane label if drawn. Otherwise `User  # inferred` for `state_change`, and `System Agent  # inferred` (or the ⚙️'s label) for `automation` and `translation`. A `state_view` has an actor only when a UI reads it: that screen's lane label (or `User  # inferred`).

## Flag, don't fix

Transcribe rule violations as drawn, with a slice-level `# warn: <rule>`. Fixes happen only in the gap review.
- Event → command directly: "don't trigger commands from events".
- Event → event: "no event after event".
- One command, several events: allowed, usually a smell.
- ⚙️ chain missing its read model or resulting event.
