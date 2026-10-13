---
name: lookdev
disable-model-invocation: true
description: Judge the current view against a reference image, with measured evidence
argument-hint: [reference image path or inbox name]
---

Run the engine's look-development loop on the current view against `$ARGUMENTS`. Load the recipe
first (`ngine.recipes` with name `authoring/lookdev`, and `authoring/scene-recreation` when the goal
is a whole-scene match), follow its numbered loop — pin the camera, capture, compare, score — and
report the numbers (`lookdev.score`) and what they do NOT establish. Do not declare a match on how
the capture looks; quote the measurement.
