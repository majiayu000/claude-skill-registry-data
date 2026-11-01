---
name: drawing-diff
description: "Compares two revisions of the same sheet or drawing set and reports what actually changed. Trigger on \"what changed between these revisions\", \"compare Rev C and Rev D\", \"diff these drawings\", \"did they change anything\", \"check this against the last issue\", or two pasted PDF paths of the same sheet or set. Matches pages by the sheet number printed in the title block rather than by page order, diffs extracted text to catch dimension, note, and tag edits, overlays the rendered pages to find linework that moved, then reads the changed regions to describe them. Flags changes carrying no revision cloud, and clouds carrying no change. Writes one report per comparison to `docs/drawing-diffs/`."
license: MIT
metadata:
  title: "Drawing Diff"
  summary: "See what changed between two drawing revisions"
  discipline: "construction-admin"
  tags: "Design, Analysis"
---


# Drawing Diff


## Overview


Take two revisions of the same sheet or set, find every place they differ, and
write a plain list of what changed to `docs/drawing-diffs/`. This replaces the
Bluebeam Compare Documents pass an office runs on every consultant re-issue, and
the slower version of it: printing both revisions and holding them up to a
window.

Two engines run, and they see different things. Text extraction catches
dimensions, notes, tags, room names, ratings, and title-block edits, and reports
them as exact values. A rendered overlay catches linework that moved when no
text changed: a wall shifted, a door swing flipped, a hatch pattern replaced.
Neither one alone is a complete answer, and the report always says which ran.


## Scope and limits — read first


**What this does.** Pairs sheets by the sheet number printed in the title block,
diffs each pair two ways, and reports added, removed, and edited text with its
value on both sides, plus a rectangle for every region of linework that changed.
Every changed region is shown to you as a before/after crop.

**What this does not do.**

- **It does not tell you a change is safe.** It reports that a dimension went
  from `3'-6"` to `4'-0"`. Whether that breaks the stair, the clearance, or the
  structure is `code-compliance-review`, `design-stair`, or a person.
- **It does not decide which revision is newer.** You name the old file and the
  new file. The skill does not read dates and reorder them.
- **It never reports "no changes" from one engine.** If text extraction found
  nothing and the overlay did not run, the answer is "text found no changes and
  geometry was not checked", never "nothing changed".
- **It does not compare two sheets of different shape.** A half-size print
  against a full-size sheet is fine, because that is one ratio applied to
  everything and both engines take it out. A different aspect ratio is a
  different sheet, and the run stops rather than pretending.
- **It does not read a scanned sheet's text.** If either side has no extractable
  text, that side is a scan or fully flattened, and the text engine is skipped
  for the pair. Comparing a vector sheet against a scan of it would report every
  line as deleted. The overlay still runs, and the report records which side was
  unreadable.
- **It does not trust revision clouds.** Clouds are compared against detected
  changes, in both directions. It does not use them as the list of changes.
- **It does not install anything.** Missing `PyMuPDF` stops the run and prints
  the install command for you.

**What you need before starting.** Two PDFs of the same sheet or set, and
`PyMuPDF` importable. Comparing a full set is one run per sheet pair, so sets
past about 40 matched sheets are worth narrowing to the disciplines you care
about, and the skill asks before starting one.

## When to use


Trigger on:

- Two pasted PDF paths of the same sheet or set, with any comparing verb.
- Explicit asks: "what changed", "compare these revisions", "diff these
  drawings", "check this against the last issue", "did they change anything in
  the re-issue".
- A consultant re-issue, bulletin, ASI, or addendum arriving against a set you
  already have.

Do NOT trigger on:

- One PDF with markups on it. That is a redline to answer, not a revision to
  compare: use `rfi-writer` or `drawing-reader`.
- Two different sheets (`A-101` against `A-102`). There is nothing to pair.
- Spec book revisions. Text-only documents diff better with `doc-reader`.
- A set that just needs bookmarking or a sheet index: `drawing-set-bookmarker`.

## Workflow


### Step 1 — Bootstrap if needed


Check whether `docs/drawing-diffs/` exists with an `index.md`. If not, run:


```bash
python scripts/init_workspace.py
```


The script creates `docs/drawing-diffs/` from
`assets/drawing-diffs-index-template.md` and verifies `PyMuPDF` is importable.
If it is missing the script prints the install hint (`pip install PyMuPDF`) and
exits non-zero — surface this to the user and stop. Do NOT pip-install on the
user's behalf.

If the project has no `docs/` folder at all, confirm with the user before
bootstrapping.


### Step 2 — Confirm which file is which


Ask the user which PDF is the older revision if it is not stated. Do not infer
it from filename, modified date, or page count. Getting this backwards inverts
every "added" and "removed" in the report and nothing downstream catches it.


### Step 3 — Match sheets


Run:


```bash
python scripts/match_sheets.py \
  --old "<old.pdf>" --new "<new.pdf>" \
  --out "docs/drawing-diffs/.cache/<base>-pairs.json"
```


The script reads each page's title-block corner, pulls the sheet number by
pattern, and pairs the two files on that number. It reports four groups: matched
pairs, sheets only in the old file (removed), sheets only in the new file
(added), and pages whose sheet number could not be read.

For pages in that last group, read them with the `Read` tool
(`pages: "<n>"`) and identify the sheet number by eye, then re-run with
`--override <page>=<sheet-number>` (repeatable). Never pair by page order to
close the gap. Sets gain and lose sheets between revisions, and page order stops
meaning anything the first time that happens.

Report the four counts to the user before comparing. Added and removed sheets
are findings on their own, and often the biggest ones.


### Step 4 — Compare each matched pair


For each pair:


```bash
python scripts/compare_sheet.py \
  --old "<old.pdf>" --old-page <n> \
  --new "<new.pdf>" --new-page <m> \
  --sheet "<A-101>" \
  --out-dir "docs/drawing-diffs/.cache/<base>"
```


The script writes `<sheet>.json` plus one before/after PNG pair per changed
region. What it returns:

- `text.added` / `text.removed` / `text.edited` — each with the string and its
  position on the sheet. `edited` means text at the same spot reads differently,
  which is where dimension and rating changes land.
- `regions` — rectangles where the rendered pages differ, largest first, with
  the crop paths.
- `alignment` — the pixel offset applied before overlaying, the residual, and
  the paper-size ratio. A re-plot shifts the whole sheet a few pixels and a
  half-size print scales it; both are taken out before comparing. **If
  `alignment.residual_pct` is above about 40, treat the region list as
  unusable** and say so: the sheets did not align, and what follows is not a
  list of changes.
- `skipped` — which engine did not run, and why. `no-text` names the side that
  is a scan; `aspect-mismatch` means the two sheets are different shapes.

`text.sheet_shift_pt` and `text.sheet_scale` record what was normalised out
before diffing. Non-default values are worth a line in the report: they mean the
sheet itself was re-plotted or re-sized, which is a fact about the issue even
when no content changed.

Default caps are 10 regions per sheet and 1% of a tile's pixels to call it
changed. Raise `--max-regions` when a sheet comes back saturated, and say in the
report that the list was capped.


### Step 5 — Read the changed regions


For each region crop pair, read both PNGs with the `Read` tool and describe the
change in the terms the drawing uses: "partition at grid C/4 moved about 600mm
east", "door 108 swing reversed", "roof hatch changed from tapered insulation to
ballast". Name a grid reference when the crop shows one.

The script says where. This step says what. Do not paraphrase the script's
rectangle coordinates into the report as if they were the finding.

If a crop is ambiguous, say so and give the coordinates. Do not invent a reading
of a region you cannot see clearly.


### Step 6 — Check the revision clouds both ways


Read the new sheet's revision block with the `Read` tool and record what the
sheet claims changed. Then compare against Step 4 and 5:

- **Changed, not clouded.** A detected change with no cloud around it. This is
  the finding that pays for the whole run. List these first.
- **Clouded, not changed.** A cloud with nothing detected inside it, usually a
  cloud left over from the previous revision that nobody cleared.
- **Revision block silent.** Changes detected but the block lists no new
  revision entry.

Never treat the cloud set as the change set. Consultants miss clouds, and the
sheets where they missed are exactly the sheets worth this run.


### Step 7 — Write the report


Copy `assets/diff-report-template.md` and fill it out to:

`docs/drawing-diffs/<old-rev>-to-<new-rev>-<date>.md`

One section per sheet, sheets with changes first. Findings inside a sheet are
ordered: unclouded changes, then text edits, then geometry, then clouded but
unchanged. Every finding carries the sheet number, the location, and both
values where there are two. End with the methods note from
`references/diff_methods.md` stating what ran and what that could not see.


### Step 8 — Update the project index


Run:


```bash
python scripts/append_to_index.py \
  --old "<old.pdf basename>" --new "<new.pdf basename>" \
  --sheets-compared <N> --sheets-changed <M> \
  --report "<report filename>"
```


Appends one row to `docs/drawing-diffs/index.md`. Do NOT edit `index.md`
directly with Edit — table alignment breaks.


### Step 9 — Report


Tell the user:

- Path to the report.
- Sheets compared, sheets changed, sheets added, sheets removed.
- The unclouded changes, by sheet. These go first, in the chat, not just the
  file.
- Any sheet where an engine was skipped, and which one.
- Any sheet that failed to align.

## Rules

- The user names which file is older. Never infer it.
- Sheets pair on the sheet number read from the title block, never on page
  order, filename, or position in the set.
- Text values are quoted verbatim on both sides. `3'-6"` to `4'-0"`, not "the
  dimension grew".
- Every reported region is backed by a crop the user can open. No finding
  without an image or an extracted string behind it.
- A skipped engine is stated in the report, on the sheet where it was skipped.
  Silence reads as "checked and clean".
- Revision clouds are evidence, compared in both directions, never the source of
  the change list.
- Output lives in `docs/drawing-diffs/` of the user's project, never in the
  skill folder or `/tmp`. Crops in `.cache/` are working files, not deliverables.

## Anti-patterns

- Pairing sheets by page index because the sheet number would not read. Ask, or
  use `--override`.
- Reporting "no changes" after a text-only run. Say which engine ran.
- Listing the revision block's claims as the change list. That is the thing being
  checked, not the answer.
- Feeding both full sheets to vision and asking what changed. Dense sheets defeat
  it and the misses are silent. The scripts narrow it down first.
- Reporting a text diff against a scanned sheet. One side with no text means the
  text engine is off for that pair, and the report says which side.
- Aligning two sheets of different shape "close enough". Stop and say so.
- Editing `docs/drawing-diffs/index.md` with the Edit tool. Use
  `append_to_index.py`.
- Auto-installing `PyMuPDF` for the user. Surface the command and stop.
- Judging whether a change is acceptable. Report it and hand off to the code and
  design skills.

## Resources

- `scripts/init_workspace.py` — bootstrap `docs/drawing-diffs/` and verify `PyMuPDF`
- `scripts/match_sheets.py` — pair pages between two PDFs by title-block sheet number
- `scripts/compare_sheet.py` — text diff plus aligned raster overlay for one sheet pair, with region crops
- `scripts/append_to_index.py` — append a comparison row to `docs/drawing-diffs/index.md`
- `references/diff_methods.md` — what each engine sees and misses, and the methods note to paste into every report
- `references/_provenance.md` — sheet-numbering source and verification date
- `assets/diff-report-template.md` — per-comparison report skeleton
- `assets/drawing-diffs-index-template.md` — initial markdown table for the project-wide comparison log
