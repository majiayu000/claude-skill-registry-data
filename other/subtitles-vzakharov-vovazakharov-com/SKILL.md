---
description: Burn the words of a dictation onto its video — the corrected transcript rendered as an HTML page over the footage, approved by the operator, then walked frame by frame into a new video file. Invoke as `/subtitles <dictation file>`. Use when the operator asks for subtitles, титры or "слова на видео" for a recording that `/dictation` has already transcribed and they have agreed.
---

End state of this skill: a new video file with the recording's own words on the
picture, rendered from a page the operator looked at and approved.

**None of the tooling exists yet.** What follows is the shape it is to be built
in, so the session that builds it starts from the decisions rather than
re-taking them. Say so plainly when the operator asks for subtitles before the
tooling is there.

## What it runs on, and why not earlier

Two inputs, both already in the branch:

- **The corrected dictation file** — `writing/<project>/dictations/<slug>.md`,
  the text under its one body heading. Corrected and agreed, which is the whole
  reason this is a separate skill: a track built from the recognizer's raw
  output puts the mis-hearings back on screen, in the speaker's voice, burned
  in. Verbatim mode only — a retake file is the script for a recording that has
  not been made yet, so there is nothing to lay it over.
- **The per-word timings**, which are in the first model's hearing and nowhere
  else. It is on the branch as
  `docs/remove-before-merging/transcripts/<slug>.<model>.json.gz` (an older
  dictation's as `deepgram/<slug>.deepgram.json.gz`) — read it with `gzip -dc`,
  and never re-run the recognizer to get one: the corrections this skill joins
  on were made against the hearing the branch carries, and a fresh transcription
  is a different set of words.

So the first piece of work is a **join**: each corrected word onto the time its
mis-heard counterpart occupied.

**Settle the join before writing anything else, because corrections change the
word count.** «человек, научный не обязательностью» is four words and «наученный
необязательностью» is two, so two timings collapse into one span. Matching off
by index gets this wrong silently and the subtitles drift for the rest of the
video — a failure that looks like nothing until the end.

## Three decisions, all the operator's

None of these is a setting with a sensible default. Ask, in this order:

1. **Which stretches go on the video at all.** A recording is longer than what
   is worth putting on screen.
2. **Whether the silences come out.** Cutting them changes every timing
   downstream of each cut, so it is decided before the join is applied, not
   after.
3. **The burn** — and that one has a gate of its own, below.

## The burn is a page, and the page is what gets approved

The video underneath, the words as ordinary DOM with CSS animations. That page
is the deliverable the operator reviews: a self-contained HTML file — styles,
fonts and script inlined — that they download, open from `file://` on any
machine, and adjust by hand. The video sits beside it in the same folder.

**Where the page gets the video from is one setting, and both values are
useful.** A relative path is what the operator edits against — frame-accurate
scrubbing while they adjust timings, and a page that works with no network. A
`raw.githubusercontent.com` URL makes the page a single file they can send
someone, at the cost of that offline property, and it is served as
`application/octet-stream`, which not every browser will play in a `<video>`
element. Inlining the bytes as a `data:` URI is the third option and the worst
of them: about a third more bytes, and the whole file loads before the first
frame paints.

**Rendering is a step they trigger on a version they have looked at**, never the
automatic tail of the previous stage. Headless Chromium walks the approved page
frame by frame and ffmpeg muxes the frames — the technique Remotion is built on,
and the same one `src/blog/scripts/lib/print-job.ts` and
`src/blog/scripts/render-mermaid.ts` already use here, so half the tooling is in
the tree.

**Animations run off the frame number, never the clock.** A page driven by
`Date.now()` or by CSS timing renders differently on two passes over identical
input, so the thing the operator approved is not the thing that comes out.

What it costs: the render is not real-time — minutes of rendering per minute of
video.

## Do NOT

- Build a track from the hearing directly. The corrected text is the source; the
  hearing is only the clock.
- Re-run the recognizer for timings. The saved hearing is why it was saved.
- Render without the operator having seen the page.
