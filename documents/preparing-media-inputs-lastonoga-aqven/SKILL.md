---
name: preparing-media-inputs
description: "Prepares images, PDFs, audio, video, long text and tables for AQVEN flows so the model gets what production sends: originals, orientation, crops, segments, chunks, labelled synthetic inputs. Use when a flow, dataset or experiment takes them, and before code cuts or edits them."
---

## MUST

- The model gets what production sends, within the provider's limits: originals at native quality, orientation
  applied, or the crops, segments or chunks production cuts. Experiments measure the production path, not a stand-in.
- Never pre-shrink, re-encode or pre-trim a source. Derived files are rebuilt from the sources by a script in
  the project.
- A case you author points at its media with `file:`, a file in the project; private media stays out of git.
  Even one inspection sample goes where the source will live, never a temporary folder; raw bulk downloads stay
  outside the package until vetted (`building-datasets`).
- Apply stored orientation (a photo's EXIF tag, a PDF page's rotation) before any crop, in scripts and in the
  production step alike.
- A synthetic input has the property it is labelled with, where the prompt looks for it, on a base that does not
  have it at level zero.
- An empty list of crops, segments or chunks is an error or a visible flag, never a silent success.
- Inspect every derived item yourself and write down a decision before a series: a contact sheet for images, PDF
  pages and video frames; a segment table with start, end and a transcript line for audio; the first and last
  lines of every text chunk; sample rows of a table.

## Procedure

| # | Step | Exit criterion |
|---|---|---|
| 1 | Inspect every source by its kind (the table below); `scripts/inspect_inputs.py` prints one row per file. HEIC photos become JPEG first (`sips -s format jpeg <file> --out <file>.jpg`) | a row per file; `$media` taken from the real format |
| 2 | Sources at native quality go into the project, never into `/tmp`: the files of one dataset in `<package>/datasets/<dataset_id>/`, files several datasets share in `<package>/samples/`. Cases point at them with `{$media: "application/pdf", file: "<file>"}` or `file: "@root/samples/<file>"`; old `blob_id` cases become files with `uv run aqven datasets materialize <package> [<dataset_id>…]`. People in images, audio or video, customer documents, personal rows: ask the owner, then a `.gitignore` line on `datasets/<dataset_id>/` or Git LFS | derived files rebuild from the sources with one script; `aqven_check` clean |
| 3 | Orientation before any crop. In production, bytes are read and written only in a `tool` node (`ctx.blobs`); a `code` node sees only `media_type`, `blob_id` and `size_bytes`, while `Text` and table rows are plain values it can split | every image and page render is upright on the contact sheet |
| 4 | Provider limits, from the provider's current docs every time. When an input exceeds them or loses what the task needs, the options depend on where the answer lives: a downscale or trim when only general content matters; native-resolution crops as `Image[]` for small detail; segments within the duration and size limits; for long text a model whose context holds it, sections selected before the call, or chunks by structure in a `map` with a merge (never silent truncation); for tables the needed rows, or a row as the case. Offer the options that fit; when several do, compare them (`use` on the preparation node, or `flow` on a `call` slot) | no piece exceeds a limit silently (`--provider-edge` shows the factor); the chosen option and its reason written down |
| 5 | Cut at boundaries you can check (the table below), not by eye or at fixed offsets. Every piece carries the context the prompt compares against (the definitions a clause refers to, the header row, the speaker names). Try a library with `uv run --with <package>==<version>` before asking the owner to add it | no cut splits a word, sentence, row or event, or leaves out the comparison area |
| 6 | Synthetic input: build the property first, then check it. The base at level zero does not have it; the change is what the prompt's definition says, where it says; a graded series has even steps; edits leave no trace the model could use | the synthetic items are inspected before any run |
| 7 | Inspect every derived and synthetic item as the table below says; accept or reject each | a decision per item is written down |
| 8 | Native input against a text stage (OCR, speech-to-text, frame captions): decide by an experiment (`designing-experiments`). The text stage is a `tool` node (`building-flows`), and its errors are part of what you measure | the choice rests on a series |
| 9 | An empty list of crops, segments or chunks fails the step or is flagged in the output; across a series, count empty lists with `series_outputs` `{series_id, split: "dev", fields: ["<preparation node id>"]}` (top-level nodes only) | a run without them cannot pass as a success |
| 10 | Before a run `uv run aqven prompt preview <flow>.<node>`, after it `run_get_node` of the llm node: number, kind and size of the attachments; for text, the length of the prompt as sent | it matches the production path |

| Kind | Inspect (step 1) | Cut at (step 5) | Look at (step 7) | Synthetic input (step 6) |
|---|---|---|---|---|
| Image | pixel size, real format, EXIF orientation | OCR word boxes, a detector, a form template, confirmed coordinates | contact sheet | the property changed where the prompt looks, no seams |
| PDF or scan | pages, text layer or scanned, page size, rotation | pages, sections, form fields | page renders on the contact sheet | a field value or clause planted on a known page |
| Audio | duration, sample rate, channels, language, speakers | silences, speaker turns | segment table: start, end, first transcript line | noise at a stated signal-to-noise level, splices that cut no word |
| Video | duration, frame rate, resolution, audio track | scene changes, the moment plus a margin | frames at the cut points on the contact sheet | an event at a known timestamp |
| Long text | characters, estimated tokens against the context window, language, structure | headings, pages, speaker turns | first and last line of every chunk | a planted clause with a known answer |
| Table | rows, columns, types, empty cells, encoding, decimal separator | a row, or a group key | sample rows per group | anomalies planted in known rows |

## Scripts

Both scripts sit in this skill's folder and declare their dependencies inline, so `uv run` fetches them in a
throwaway environment and the project gets no new dependency.

```bash
uv run <this skill's folder>/scripts/inspect_inputs.py <folder or files>
uv run <this skill's folder>/scripts/contact_sheet.py <folder or files> --out <sheet.png> --provider-edge 1568
```

`inspect_inputs.py` prints one tab-separated row per file: images through Pillow (real format, EXIF tag, upright
size), PDFs through pypdf (pages, pages with a text layer, page size, rotation), audio and video through `ffprobe`
when it is on `PATH` (the row says so when it is not), text and CSV through the standard library (characters,
estimated tokens, headings; rows, columns, ragged rows, empty cells, decimal commas).

`contact_sheet.py` puts images, PDF page renders or video frames on one captioned sheet with EXIF orientation
applied and stored and upright pixel sizes on each tile, plus a table on stdout. `--tile` sets the tile edge
(480), `--columns` the tiles per row (4), `--provider-edge` the longest edge the provider keeps: a tile above it
shows the factor it would be scaled by. Render PDF pages first with `pdftoppm -r 150 -png <file.pdf> <prefix>`
and video frames with `ffmpeg -ss <seconds> -i <clip> -frames:v 1 <frame.png>`, where installed. Open the sheet
and look at every tile.

## Pitfalls

A pitfall is a general rule; the illustration after it is one instance.

| What goes wrong | Do instead |
|---|---|
| A detail too small after the provider's resize: a 4000 px invoice scan sent as one image came out with unreadable line items | the regions the question needs at native resolution (crops as `Image[]`, or a model whose edge keeps them), checked with `--provider-edge` |
| A long document sent whole: from a 300-page PDF the model answered out of the first part only | the length checked in step 1 against the context window, then one of step 4's long-text options chosen with the owner |
| A cut left out the context the prompt compares against: a clause chunk lost the definitions it refers to | every piece carries its comparison context |
| Pre-shrunk sources made the crop step find nothing, and the run passed with an empty crop list | never pre-shrink; an empty list fails |
| The experiment measured a stand-in: a clean transcript where production sends noisy call audio | the experiment's flow reproduces the production path |
| Segments cut at fixed 30 s marks split a sentence of a meeting across two segments | cut at silences or speaker turns, listed in a table |
| A stereo call with one speaker per channel mixed down to mono, so speaker attribution failed | keep the channels, or separate the speakers first |
| A provider sampled a clip at one frame per second and missed a half-second event | a clip around the moment, or a model or setting that samples densely enough, checked on the frames sent |
| Orientation applied nowhere: phone photos of receipts reached the model sideways | orientation first, checked on the sheet |
| A CSV with decimal commas read as text, so every amount compared as a string | types checked in step 1 |
| A synthetic input without its label's property: a "blurry receipt" was darker overall, the text stayed sharp, and the model that said "sharp" was right | the change is the labelled property, where the prompt looks; check it before the run |
| The base already had the property at level zero: the "clean" contract used as a base already held a termination clause | a clean base, checked in step 7 |
| Edits left a trace the model could use: every planted anomaly in a table was a round number | synthetic items inspected next to real ones |
| Media known only by `blob_id`: the dataset ran on the machine that imported it and nowhere else | the file in the project, `file:` in the case |
| The `$media` of a file reference guessed: a `.mov` clip labelled `video/mp4` (`W_MEDIA_TYPE_MISMATCH`) | `$media` from the real format, checked in step 1 |

## Tools and commands

- Bash: `sips` on macOS or Pillow for images; `ffprobe`, `ffmpeg` and `pdftoppm` where installed; the two
  scripts above.
- `uv run aqven prompt preview <flow>.<node>`: the attachments of a call before any run.
- `aqven` MCP `run_start` (`mode: "live"`), `run_get_node`, `series_outputs` (a node's output across a series).
- `uv run aqven datasets materialize <package> [<dataset_id>…]`: old `blob_id` cases into files.
- `file:` references in cases and case building: `building-datasets`.

## References

- `references/engine/image-preparation.md`: EXIF orientation, crops, synthetic images, the contact sheet,
  checking the trace. Read before step 3 on images and before building any synthetic image.
- `references/engine/preparing-audio-video-documents-and-text.md`: PDFs, audio, video, long text and tables:
  inspection, cut boundaries, chunking, synthetic inputs, native input against a text stage. Read at step 1 for
  any input that is not an image.
- `references/concepts/media-has-real-limits-on-both-sides.md`: provider limits for images, audio, video,
  documents and long text, silent reshaping, why preparation happens in a `tool` node. Read at step 4.
- `references/reference/media.md`: the media value types (`Image`, `Audio`, `Video`, `Document`) and their fields.
  Read before typing a media input.
- `references/engine/dataset-media-files.md`: `file:` references, the two path forms, private files, the three
  media diagnostics. Read at step 2.
