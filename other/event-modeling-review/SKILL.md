---
name: event-modeling-review
em-version: 1.22.0
description: >-
  Use when starting em's live browser viewer (`em watch --serve`) so a team can watch a model
  update in real time, or facilitating a SCHEDULED stakeholder walkthrough that steps through
  slices one at a time in Review mode, capturing anything the room raises live as `issue "..."`
  red notes. Drives `em`'s watch and review phases.
---

# Event Modeling — watch & review

## Phase: `watch` — live team view

Start the watcher with `--serve` in the background:
`em watch <model-name>.em -o <model-name>.svg --serve` (run_in_background). It re-renders on every
save and pushes an instant reload to the browser over Server-Sent Events. Tell the user to open the
URL it prints and share their screen — updates appear the moment you save, with no polling and no
idle churn between edits.

What that URL opens depends on the model. A model that declares storylines opens on the
**storyline canvas** (`http://localhost:5173/map`): every storyline's own diagram in a draggable
frame, the flow between storylines drawn between frames, reloaded live on every save with the
layout kept. A frame's **open ›** drills into that storyline — the viewer on its own slices and
nothing from outside it — and **‹ Storylines** in the header returns to the canvas. A model
without storylines opens on the timeline (`http://localhost:5173/?svg=<model-name>.svg`). Never
send a room to the full timeline of a storyline model; the storyline is the unit people read.

The viewer navigates like a map — drag to pan, scroll/pinch to zoom, **Fit** to reset — and its
**Review mode** steps through slices one at a time (see the `review` phase below). A save that
fails to render never blanks the shared screen: the last good diagram stays up, an error banner
explains what went wrong, and the viewer recovers on its own at the next successful render.

## Phase: `review` — stakeholder walkthrough

Goal: step a real stakeholder review session through the model slice by slice, one slice
spotlighted at a time, with any open questions the room raises captured live as `issue "..."`
red notes.

**Trigger: a real stakeholder review session is on the calendar — a scheduled use, not
speculation.** Don't propose this phase proactively; it exists for facilitated reviews with
non-engineer stakeholders in the room, not routine model editing.

Start the same live server as `watch`: `em watch <model-name>.em -o <model-name>.svg --serve`
(run_in_background). Open the printed URL and share the screen. With storylines, review one
storyline at a time: open it from the canvas (or start inside it with `--storyline "<name>"`),
then click **Review mode** in the header — Prev/Next walk that storyline's slices only. Between
storylines, **‹ Storylines** returns to the canvas, where the arrows between frames are the
order to take them in. Without storylines, click **Review mode** on the timeline. Use Prev/Next
(or the left/right arrow keys) to step through slices in declaration order — each one
pans/zooms into view with everything else dimmed, so the room's attention tracks one slice at
a time.

**When a State View slice is on screen, ask who reads it (MIL-215):** a person or client in the
room → the `ui` should draw it; another system → `public`; only an automation → nothing, it's
internal by design and needs no endpoint.

**Live capture:** when a stakeholder raises something unresolved, add `issue "..."` to the
relevant element in the `.em` file and save — exactly the same mechanism `event-modeling-conform`
uses for any other issue. The browser updates over the existing SSE push within moments, without
losing the current slice or resetting review mode.

Wrap-up: run `em validate --list-issues` to sweep everything captured during the session and
walk each one with the user, same as any open issue. Update the state file's Participants
section with who attended, and run `em state set-review <date>` to set the `Last stakeholder
review:` marker (mirrors `Last conformance:`).

**Per-slice outcome.** Walk the slice's questions — the doc's `## Open Questions` and every
`issue "..."` note the room added to its elements — and give each one of three endings:

- **Answered in the room** → edit the doc's authored section with the answer and delete the
  `issue` note by hand. Defer is never used to record an answer.
- **Raised in the room, not for this version** → `em slice defer <model> <key> --from-issue "<text>" --until v<n> --decision "<what this version does>"`:
  promotes the captured `issue` into the doc's Open Questions as a deferred item, mirrors it
  into the state file and removes the red note — one command, no hand edit mid-session.
- **Already on the doc, not for this version** → the positional form. A question this version will not answer is deferred with `em slice defer <model> <key> "<question>" --until v<n> --decision "<what this version does>"` — never left `- [ ]`, never deleted, never answered by guessing.

Then, and only then: a slice with nothing left `- [ ]` and no open `issue` →
`em slice review <model>.em <key> --by <name>` (flips its doc to `status: reviewed` and records
`reviewedBy:`/`reviewedOn:`). `em slice review` itself exits 1 on an unchecked Open Question
(`--allow-open` records a deliberately partial walk; `--again` re-records a review after a body edit).
Anything still open stays `draft` — the walkthrough doesn't decide
it, the next session or the open-questions list does.

**The facilitator never ratifies, never offers to ratify, and never suggests ratification in a
review session. Ratification is a separate human gate after review**
(docs/process.md#the-slice-lifecycle-gates). It is typically multi-person, routed through
CODEOWNERS on `slices/**`, and it is not this session's to run — `em slice ratify` will itself
refuse a doc that hasn't been through `em slice review`.

End of phase: state file's `Last stakeholder review:` marker updated, every walked slice whose
questions all closed moved to `status: reviewed`, every issue captured live triaged (resolved on the spot, moved to Open questions / parking lot, or left open on
purpose). Review doesn't chain to another phase — it's a recurring, scheduled activity like
`conform`, not a step in the discover → model → slice sequence.

Preconditions (tool check, model location) are the same as every other phase — see
`../event-modeling-shared/reference/operating-principles.md`.
