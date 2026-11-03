---
name: editing-handoff
description: >
  Default finish for the rough-cut skill. Replays cutlist.json against
  the raw footage as a Premiere/CapCut timeline where every cut is an
  individually trimmable edit point on the original media — never a
  flattened render. Use immediately after building a cut list, whenever
  the job is not headed straight for a full HyperFrames graphics build.
  Time-to-timeline is the metric: this produces output in seconds.
---

# Editing-app handoff

The whole point of this skill: hand the editor a timeline made of real,
trimmable clips pointing at `raw/`, not one baked-together file. If you
want to nudge a cut by two frames, you drag an edit point — you don't
re-run the pipeline.

## 1. Generate the timeline

```bash
uv run .claude/skills/editing-handoff/scripts/build_fcpxml.py <job-name>
```

Requires `projects/<job>/cutlist.json` (from `/rough-cut`). Writes:

- `outputs/<job>.fcpxml` — one FCPXML `<clip>` per kept segment, all
  referencing the same source asset, at frame-exact rational timecodes.
- `outputs/<job>-cutsheet.txt` — a plain-text in/out list as a manual
  fallback.

## 2. Import it

**Premiere Pro / DaVinci Resolve / Final Cut Pro:** File > Import >
select `outputs/<job>.fcpxml`. It lands as a sequence with one clip per
kept segment already assembled on the timeline, each individually
trimmable, all referencing `raw/<file>` — relink media if the app asks
(point it at `projects/<job>/raw/`).

**CapCut Desktop:** try Import > Import Project with the same `.fcpxml`.
CapCut's XML/FCPXML support varies by version and platform — if it
doesn't accept the file, fall back to the cut sheet: drag `raw/<file>`
onto the timeline once, then use `outputs/<job>-cutsheet.txt`'s in/out
timecodes to trim and split it into the same clips by hand. This is
still fast — the timecodes are already measured and frame-snapped, no
guessing.

## 3. What NOT to do here

Don't flatten. Don't run `assemble_rough_cut.sh` for this path. Don't
re-transcribe to "double check" a cut — if a cut looks wrong, check it
against `cutlist.json` and `outputs/.transcript.json`, and if the cut
itself was mismeasured, that's a `/rough-cut` fix (adjust the filler/gap
thresholds or re-run boundary measurement), not something to patch by
hand in the app and forget about.

## When this job later needs a full render

If, after editing-app review, this job turns out to need HyperFrames
graphics/captions/music after all, go back and run
`.claude/skills/rough-cut/scripts/assemble_rough_cut.sh <job-name>` to
produce the flattened, polish-passed base video, then continue at
`/graphics-plan`. The cut list stays the same either way — this skill
and the flattened-render path both read the exact same `cutlist.json`.
