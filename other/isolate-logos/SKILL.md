---
name: isolate-logos
description: 'Split one AI-generated logo sheet (a uniform grid of logos on a near-white background) into individual PNG assets. Each kept cell is auto-cropped to its content, centered on a square canvas, and written twice: an opaque version on white and a -transparent version where the background is flood-filled to alpha 0 from the borders, preserving white areas inside the artwork. Cells are named in reading order, a dash skips a duplicate cell, and name=basename overrides the output base for the project-wide combined emblem. Use when the user asks to isolate, crop, or extract logos or icons from a generated sheet into assets, or to create transparent versions of them.'
user-invocable: true
argument-hint: 'Give the sheet image path, the output folder, the column count, and the cell names in reading order, for example "isolate-logos sheet.png wiki/assets --cols 3 --names download,bridge,forge,-,ship,combined=logo-cplx --prefix logo-cplx".'
---

[Instruction](../../../instructions/isolate-logos.md)

Implementation is mutualized across the shared directories:

- [`../instructions/isolate-logos.md`](../../../instructions/isolate-logos.md)
  — the full collect-inputs, run, verify, and adjust workflow.
- [`../tools/isolate_logos/isolate_logos.py`](../../../tools/isolate_logos/isolate_logos.py)
  — the script: grid split, content crop, square padding, border flood fill.
- [`../tools/isolate_logos/README.md`](../../../tools/isolate_logos/README.md)
  — the tool reference: flags, defaults, and produced files.

Inputs: the sheet image, the output folder, `--cols`, and the ordered cell
names (`-` skips a cell, `name=basename` renames one output). The skill runs
the script via `uv run --with pillow`, then reads each produced
`-transparent.png` back to verify the crop and that white inside the artwork
survived, adjusting `--white-threshold` or `--margin` when needed.
