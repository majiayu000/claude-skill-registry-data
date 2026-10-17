---
name: slice-to-diagram
description: Render Uncanvased slice YAML files into a canonical Event Modeling board (Adam Dymitruk style) as an Excalidraw file (.excalidraw) — a left-to-right storyboard with actor swimlanes, UI wireframes showing example data, ⚙️ processors, commands and read models with their fields, one event lane per stream, external-system lanes, and each slice's Given/When/Then specs under it. Use when the user has slice YAML (in slices/ or named files) and wants a diagram, board, or picture back — the reverse/backward pass — or mentions Excalidraw, visualizing an event model, or turning slices into a diagram.
---

# Uncanvased slices → Event Model board (Excalidraw)

This is the **backward pass**: authored slice YAML → one Event Modeling board as an
`.excalidraw` file. A bundled deterministic generator does the layout — **run the
script; never hand-author Excalidraw JSON.**

## Quick start

```bash
python3 .claude/skills/slice-to-diagram/scripts/generate_diagram.py slices/ -o board.excalidraw
```

`paths` may be a **directory** (scanned for `*.yaml`) and/or **individual slice
files**; all selected slices land on ONE combined left-to-right timeline.

| Flag | Effect |
|---|---|
| `--compact` | names only, no field lists (big-picture or workshop view) |
| `--no-specs` | leave out the Given / When / Then area |

## Workflow

1. Decide the selection: the whole `slices/` folder, or the files the user named.
2. Run the generator. It prints the output path, counts (columns, duplicated
   events, story hints), the event streams, and the slice order with ids.
3. **Report** the output path and slice order. The file opens at excalidraw.com
   or in the Excalidraw VS Code extension. Do **not** echo the JSON.
4. **Surface every warning verbatim**:
   - `! off-board reference drawn as ghost`: a name no selected slice produces;
   - `! read model … sits right of its reader`: a sequencing error;
   - `~ story: …`: a reader placed before an event that changes it.
5. If there are story hints, offer to fix the timeline: each hint names the
   slice to move later (raise its `sequence:`), which removes the duplicate.
   If no event stream is set, mention that `context:` splits the events lane.
   Both are modelling decisions, so ask before editing slice files (the
   `img-to-slice` gap review covers them as `out-of-story` and `no-stream`).

## The board

It reads as a storyboard, left to right in time:

| Lane | Holds |
|---|---|
| **One per actor** (`Customer`, `Branch Agent`, `System Agent`, …) | only UI wireframes (with **example data**) and ⚙️ processors |
| **Commands / Read models** | blue commands and green read models, each with its **fields** (`(tag)` marks DCB tags) |
| **Events · `<stream>`** | one orange lane per `context:`; events show their fields |
| **One per external system** (`Stripe`, …) | an automation's `external_call`, a translation's external event |
| **Specifications** | each slice's Given / When / Then scenarios, under its column |

**Rules of the board**
- **It tells one story.** Slices follow `sequence:`; a reader sits after the events it reads.
- **Arrows never point left.** If a view reads an event that happens later, it
  gets its own hatched `(duplicate)` copy of it, and the script prints a story
  hint. Duplicates are a smell to fix by reordering, not decoration.
- **Loops are not story errors.** An event recorded by the view's own consumer
  (the ⚙️ it triggers, or the button on the screen it feeds) is written on the
  view as `cleared by …` / `updated by …` instead of an arrow.
- **Events are the only shared contract.** Commands and read models are drawn
  once, in their own slice.
- **A screen is one frame.** A read model's screen and the button for the next
  command are one wireframe when the slices are neighbours (badge `12·13`).
- **Every element carries its slice `id`** as a corner badge; duplicates carry
  the producer's id. `img-to-slice` uses the badges to match an edited board
  back to its files.
- **Specs are first-class.** Scenarios are drawn under their slice; failures
  appear as red stickies with the message as a white note.

Slices are written by the `img-to-slice` skill; its `REFERENCE.md` defines the YAML.

## Details

See **[REFERENCE.md](REFERENCE.md)** for the per-pattern mapping, where example
data comes from, the duplicate and loop rules, the palette and geometry, and how
to extend the script.
