---
name: designing-on-canvas
description: >
  Our board conventions for drawing a product's screens on a Design canvas: real components
  through `x-import`, shared parts through `dc-import`, `is_interactive` on linked boards,
  tweaks for states, one page per flow, `NN-name` board ids and titles. Holds our conventions
  only; the canvas's own rules are read live from the Design type on every run.
when_to_use: >
  A design workflow agent is about to create or edit boards on a canvas (`/create-design`,
  `/design-system`, `/refine-design`). Not for reading the canvas rules themselves, which this
  skill deliberately does not hold.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# designing-on-canvas

## When it applies

You are drawing boards for a product whose components already exist in code or in a built
design system. Apply these conventions on top of the canvas rules passed to you as
`canvasRules`; where they disagree on mechanics, the canvas rules win.

## Conventions

1. **Real components by `x-import`.** Every component the product already has is used through
   `x-import component-from-global-scope="Ns.Name"` (the namespace is in `design.md`). Never
   redraw one.
2. **Shared parts by `dc-import`.** A part used on more than one board (header, nav, card
   shell) lives in one file and comes in through `<dc-import>`.
3. **`is_interactive` on any linked board.** It is a key of the board's entry in
   `project/canvas.json`, not of the board file. Set it on every board that is the source or
   target of a link.
4. **Tweaks for states and variants.** Empty, error, loading and variants are tweaks in
   `data-props`, one object per tweak, e.g. `{"empty":{"type":"boolean","default":false}}`; a
   state sets that tweak's default. Do not draw a second board for a state.
5. **One canvas page per flow.** `pages: [{id,name}]` in `canvas.json`, and each board's
   `page` names its flow.
6. **`NN-name` board ids and a `title`.** File `NN-name.dc.html` (starts with a digit, so it is
   legal), `NN` the order in the flow. The title is the `title` key in `canvas.json`.
7. **No inline copies of components.** If a component is not importable, say so in the brief;
   do not paste its markup into a board.

## Canvas rules arrive live

The canvas rules (format, craft, view state, design-system components, the runtime) are not in
this skill and are never copied into it; they change release to release. The command reads
them every run and passes them to you as `canvasRules`. If you must read them yourself:
`type_url` on the Design type returns only its `SKILL.md`, so read each reference through a
canvas, with `Artifact read url=<canvas url> path=artifact-type/reference/<file>`.

The Design type tells its agents not to verify renders. Here, local renders are done by our
code (`design-render.js`, under the contract's render-pass statement), never by you: draw, do
not launch a browser.

## Never

- Copy canvas rules, or any part of the Design type's text, into a board, brief or skill.
- Draw a component that exists in the library.
- Put `is_interactive` or a title inside the board file.
