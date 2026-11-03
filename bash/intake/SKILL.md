---
name: intake
description: >
  Step 1 of the content pipeline. Use when a raw filmed clip needs to enter
  the system — the user drops a camera file and wants a job started, says
  "start a new project with this clip", or "rough cut this" names a raw
  file that has no projects/<job>/ folder yet. Copies (never moves) the
  raw file into projects/<job>/raw/ and scaffolds the rest of the job
  folder. Job names are kebab-case titles about the CONTENT, never the
  camera filename.
---

# Intake

The only job of this skill is: get one raw file safely into a properly
named project folder. Nothing else touches picture or sound yet.

## 1. Name the job

Job names are kebab-case titles about the content (`why-your-standups-suck`),
never the camera filename (`C0043.MP4`). If the user gave you a filename
and no title, look at the footage or ask for a one-line description and
derive a short kebab-case title from it — don't just slugify the filename.

## 2. Scaffold the folder

```bash
scripts/new-project.sh <job-name>
```

This creates `projects/<job-name>/` with `raw/ audio/ assets/ broll/
outputs/ hf-graphics/ transcript/ .cache/`, drops in `finalize.sh` and
`prune.sh` (generated from `lib/templates/`, already executable), an
empty `transcript/corrections.json`, and `hf-graphics/PROJECT.md` (the
resume doc for the graphics build — read this at the start of every
future session touching this job).

It refuses to run if the folder already exists, and warns (but doesn't
block) if the name still looks like a camera filename.

## 3. Copy the raw file in

**COPY, never move.** The original file the user filmed stays wherever
it already lives; `raw/` is this pipeline's own copy.

```bash
cp "<source file>" "projects/<job-name>/raw/"
```

If there's more than one file for this job (multiple angles, a second
take), only the primary take goes in `raw/` — everything else (extra
angles, cutaway footage) goes in `broll/`. The rough-cut skill expects
exactly one file in `raw/`.

Verify the copy before moving on:

```bash
ffprobe -v error -show_entries format=duration,size -of default=noprint_wrappers=1 "projects/<job-name>/raw/<file>"
```

## 4. Hand off

Intake is done. Move straight to `/rough-cut` — that's the "rough cut
this" entry point and the only slow step (transcription) in the whole
default path.
