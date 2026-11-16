---
name: diagram-lint
description: Produce, check and render architecture diagrams as code. Use when adding a diagram, editing a Mermaid .mmd source or a draw.io generator script, rendering the .svg and .png outputs, or checking a draw.io layout before trusting it.
license: Apache-2.0
compatibility: Python 3.12+. Rendering needs draw.io desktop and mermaid-cli.
metadata:
  version: "1.0"
---

# Diagram lint

Choose the toolchain by diagram type, and read its guide before editing:

| Diagram | Edit | Guide |
|---------|------|-------|
| Topology, or anything with cloud icons or logos | Python generator using `scripts/drawio_lib.py` | [`references/drawio.md`](references/drawio.md) |
| Sequence, logic flow or component | `.mmd` file | [`references/mermaid.md`](references/mermaid.md) |

Never hand-edit `.drawio`, `.svg` or `.png` files. They are generated, so manual
changes are lost on the next run.

Add new `.drawio` files to the `DRAWIO` list in the `Makefile`. New `.mmd` files
are picked up automatically. See the
[worked examples](https://github.com/xavier-thomas/diagram-lint/tree/master/examples/diagrams).

## Setup

If the project has no `diagrams/` directory:

1. Copy `assets/Makefile`, `assets/make_diagrams.py` and `assets/mermaid-config.json`
   into a new `diagrams/` directory.
2. In `Makefile` and `make_diagrams.py`, set `SKILL` to this directory's location.
3. In `mermaid-config.json`, set `fontFamily` to a font that every machine rendering
   the diagrams has. The file also sets a palette that matches the draw.io styles.
4. Add `.drawio-sources` and `*.preview.svg` to the project's `.gitignore`.

## Commands

Run from the repository root. `<skill>` is this directory and `diagrams/` is
where the project keeps its diagram sources.

```bash
python3 diagrams/make_diagrams.py                              # regenerate the .drawio files
python3 <skill>/scripts/check_layout.py diagrams/*.drawio      # check draw.io geometry
python3 <skill>/scripts/check_mermaid.py diagrams/*.mmd        # check Mermaid self-messages
python3 <skill>/scripts/content_diff.py old.drawio new.drawio  # after a re-layout, prove the content is unchanged
python3 <skill>/scripts/preview.py diagrams/example.drawio     # rough SVG if draw.io is not installed
make -C diagrams                                               # real renders; needs draw.io desktop and mermaid-cli
```

`check_layout.py` fails on any edge it reports as `UNVERIFIED`. `check_mermaid.py`
fails on any self-message that carries text. `make -C diagrams check` runs both.

## Inspect the render

A diagram change is not done until you have inspected the real render. A passing
geometry check is not enough: it cannot see a label on a caption or a blank icon.

1. Run `make -C diagrams`. Do not inspect `preview.py` output.
2. Open the `.png`. Read the whole diagram, then every edge label and icon at full
   size. Inspect wide diagrams in halves.
3. Check each item below. On any failure, fix the source, re-render and restart
   the list.
   - No line runs through a node or icon caption.
   - No lines cross, except at an agreed line jump.
   - No lines touch, except at a shared endpoint, and none is drawn on another.
   - No edge label sits on a caption, another label, an elbow's corner or a boundary line.
   - Every box is larger than its text, with clear space on both sides. No text touches
     a box's edge or spills outside it.
   - No step number sits on its text, and no self-message label crosses its lifeline.
   - No icon is an empty box. Unknown stencil names render blank.
   - Every logo is recognisable at its drawn size on a white background.
   - The theme is light, with nothing adapting to a dark viewer.
   - Colours match across both toolchains, if the project uses a palette.
   - The diagram agrees with the project's recorded design decisions, if any. This
     is a judgement call that no script checks.
4. Spot-check one label in the `.svg`. It must be a `<text>` element, not an
   embedded raster.
5. Add this line to the pull request or commit message:
   `Inspected <file>.png at <date>: <failures fixed, or "none">`. If you could not
   open the render, say so instead.

## CI

Compare only `.drawio` and `.svg` files. PNG bytes drift with fonts and browser
versions, so comparing them fails builds for no design reason.

Run `make -C diagrams check` as well, if the project has CI. It needs only Python.
