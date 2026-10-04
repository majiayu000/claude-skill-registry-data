---
name: isolate-logos
description: 'Split one AI-generated logo sheet (a uniform grid of logos on a near-white background) into individual PNG assets. Each kept cell is auto-cropped to its content, centered on a square canvas, and written twice: an opaque version on white and a -transparent version where the background is flood-filled to alpha 0 from the borders, preserving white areas inside the artwork. Cells are named in reading order, a dash skips a duplicate cell, and name=basename overrides the output base for the project-wide combined emblem. Use when the user asks to isolate, crop, or extract logos or icons from a generated sheet into assets, or to create transparent versions of them.'
---

Read and follow [the canonical instruction](../../../../../../../../git/llm-shared/instructions/isolate-logos.md)
