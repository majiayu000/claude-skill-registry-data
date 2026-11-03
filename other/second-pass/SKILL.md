---
name: second-pass
description: >
  Step 4 of the content pipeline. Use after the first graphics render,
  when the user reviews it and calls specific adjustments. Iterates
  part by part against the shared HyperFrames timeline built in
  graphics-plan — never a full rebuild for a small note.
---

# Second pass

This step exists because the first graphics pass is never the last
word. The user reviews `outputs/<job>-graphics.mp4` (or individual
parts) and calls adjustments; this skill's job is to land each one as a
small, targeted change and re-render only what changed.

## 1. Take the note as a part-scoped change

Every review note maps to one or more `compositions/part-NN.html`
files. If a note seems to require touching the shared `index.html`
timing (a beat needs to start earlier/later, or run longer/shorter),
that's fine too — it's still one slot's `data-start`/`data-duration`,
not a rebuild.

Don't batch unrelated notes into one edit — land them one at a time so
each is independently reviewable and re-renderable.

## 2. Make the change, re-render just that part

```bash
projects/<job>/hf-graphics/render-part.sh compositions/part-NN.html
```

Use `--quality draft` (the default in `render-part.sh`) for iteration
speed; only the final render script uses `--quality high`.

## 3. Log it

Append a line to `hf-graphics/PROJECT.md`'s **Second-pass notes**
section: what was called, what changed, which part number. Never
delete or overwrite earlier rounds — this is the running log a future
session (or a future you) resumes from instead of re-deriving what's
already been tried.

## 4. When every called adjustment is landed

Re-run the full render:

```bash
projects/<job>/hf-graphics/render-final.sh
```

Then continue to `/captions` (short-form only) or straight to `/music`
/ `/export` if this job has no captions or music.
