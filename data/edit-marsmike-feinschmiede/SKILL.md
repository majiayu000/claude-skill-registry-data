---
name: edit
description: Editing a pre-recorded video into a brand-themed cut — authors edit_plan.json with overlay beats, captions, and audio score; probe/transcribe/lint/preview/final pipeline. Use when the user provides footage and asks to edit, enhance, or caption it.
---

# edit — pre-recorded footage pipeline

Takes a finished recording (voice and cut are untouched) and adds a planned
layer of visuals. Authors `edit_plan.json` data only — the shared engine in
`edit-engine/` renders it.

## Quick Start

```
/edit footage.mp4
```

See [`references/quick-start.md`](references/quick-start.md) for examples and
short-form vs longform recipes.

## Pipeline

`probe → transcribe → author plan → lint → preview → (approve) → final`

Full step-by-step with the beat catalog and knowledge-doc index:
[`references/pipeline.md`](references/pipeline.md).

## Overlays, captions & images

Hard rules (anchors, `appear_sec`, text placement, derived-file discipline),
caption suppression logic, image sourcing priority:
[`references/overlays.md`](references/overlays.md).

## Audio score

Finals only; bring your own royalty-free assets; auto-generated cue sheet;
level rules: [`references/audio-score.md`](references/audio-score.md).

## References

**Recipe:** [`references/quick-start.md`](references/quick-start.md) · [`references/pipeline.md`](references/pipeline.md).

**Detail:** [`references/overlays.md`](references/overlays.md) · [`references/audio-score.md`](references/audio-score.md).
