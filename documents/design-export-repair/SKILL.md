---
name: design-export-repair
description: "Fixes broken decks/PDFs exported from Claude's \"Design\" feature (or similar AI deck generators) — cut-off or clipped text, wrong/substituted fonts, and corrupted .pptx package structure that shows up only once you export to PDF, not while looking at it in the app. Use this skill whenever the user uploads a zip, .pptx, or .pdf exported from Claude Design (or mentions \"Design\" export, an AI-generated deck, or a generated slide deck/PDF) AND reports it looking broken, wrong, cut off, garbled, or different from the original when opened, printed, or converted to PDF — even if they don't use the word \"repair\" or name the specific defect. Also trigger for general \"my exported PDF/deck is broken, help fix it\" requests when the file was clearly produced by an AI design/deck tool rather than hand-authored. Produces both a repaired, still-editable .pptx and a clean PDF, plus a report of exactly what was wrong and what changed."
---

# Design export repair

Fixes AI-generated deck/PDF exports (built for Claude Design's export
path, but the checks are generic OOXML/PDF hygiene, not Claude-specific)
that look fine in the app but come apart once exported — text missing
its last few characters, fonts that don't match the original design, or
a `.pptx` that some converters choke on even though PowerPoint opens it
fine.

Four defect classes were found and fixed against a real broken export;
`references/defect-classes.md` has the full story for each, including how
they were confirmed and what the fix trades off. Skim it before extending
this skill to a case it doesn't already handle — in particular, defect #4
there is a good example of why "the shape geometry looks right" is not
the same claim as "the rendered PDF looks right," and it's worth reading
before assuming a new complaint is a geometry problem.

## End-to-end: from Claude Design to a clean file

This is written for the person running Claude Code, not just for Claude —
skim it once so you know what to actually do. There are two different
ways a Design project reaches Claude Code, and they behave differently.

**Path A — plain Export (this is the one that matches "my deck/PDF looks
broken"):** In Claude Design, use Export and pick PDF, PPTX, or HTML. Save
the file, then bring it to whichever Claude Code you're using — attach it
in the chat if your setup allows that, or save it to disk and give Claude
the path. Then tell Claude to use this skill: plain language like "this
deck looks broken when I export it to PDF, can you fix it" is enough on
its own (the skill's description is written to match that phrasing), or
name it directly (`design-export-repair`) if you want to be explicit.

**Path B — the "Send to Claude Code" button.** This is a related but
different feature from plain Export — it's aimed at continuing design/
prototype work in code, not at fixing a deck export, but you may end up
here anyway. It offers two options, and they behave differently:

- *"Send to Claude Code Web"* opens a brand-new claude.ai/code session
  with the design bundle already sitting in that session's working
  directory — there's no file to save or attach, it's just already
  there. In that new session, tell Claude to look at what's in the
  working directory and use this skill on it.
- *"Send to local coding agent"* gives you a prompt to paste into your
  local terminal Claude Code. Be aware: as of this writing, that default
  prompt depends on a "Claude Design connector" that local Claude Code
  doesn't ship, and reliably fails silently (see
  [anthropics/claude-code#69246](https://github.com/anthropics/claude-code/issues/69246)
  if you want the details). The same dialog has a **"Download zip
  instead"** option — that one actually works: it downloads a real zip of
  the design files. Save that zip, point local Claude Code at it (or
  unzip it into your project folder first), and tell Claude to use this
  skill on it.

Whichever path you took, `scripts/fix_export.py` accepts a file, a zip, or
a whole directory — `unpack.py` figures out what it's looking at rather
than requiring one specific shape. One thing worth knowing about Path B
specifically: its bundle format is Design's own `*.dc.html` canvas files,
which is a different animal from the `.pptx` this skill's repair pipeline
was actually built and verified against (see
`references/defect-classes.md`) — a `.dc.html` bundle gets routed through
the best-effort HTML path (`convert_html.py`) instead of the fully-tested
one. If you're trying to fix a broken deck/PDF export specifically, Path A
is the one to reach for.

After either path, Claude runs `scripts/fix_export.py` and hands back a
repaired `.pptx` (Path A) or PDF, plus a report explaining exactly what
was wrong and what changed. Open the repaired `.pptx` if you want to keep
editing in PowerPoint/Keynote/Google Slides, or use the `.pdf` directly if
that's the deliverable you needed.

One honest caveat: buttons and flows in Claude products change over time,
and this description of Path B is based on Claude Code's own public issue
tracker rather than hands-on testing of that specific handoff. If what you
see doesn't match this, don't get stuck on it — just get the actual design
files to Claude Code by whatever route works, and tell Claude to use this
skill; `unpack.py` is written to figure out what it's been handed.

## Quick summary of what gets fixed

| # | Defect | Symptom | Fix |
|---|--------|---------|-----|
| 1 | `[Content_Types].xml` declares parts that don't exist in the zip | Some converters fail, drop slides, or garble output; PowerPoint may silently "repair" and hide it | Load + re-save through `python-pptx` (rebuilds the manifest from what's actually there) |
| 2 | A shape's box extends past the slide edge | Can get clipped by renderers that treat the slide as a strict viewport | Translate the shape back in bounds (or scale down + rescale table grids, if the shape is bigger than the slide itself) |
| 3 | Custom webfonts (Inter, Plus Jakarta Sans, JetBrains Mono seen in practice) used but not embedded | Renderer without those fonts substitutes something else — wrong look, different text measurements | Install matching bundled/fetched font files where the renderer will find them, before conversion |
| 4 | LibreOffice clips the tail of any text run with letter-spacing (`a:rPr spc`) | Tracked-out labels/kickers/badges lose their last 1-4 characters — **this is usually the actual cause of "text is cut off" even when #2 is also present** | Render a letter-spacing-neutralized copy through LibreOffice only; the returned `.pptx` keeps its real letter-spacing for editing |

## How to run it

Everything is one script:

```
python3 scripts/fix_export.py <input> --out-dir <where to write results>
```

`<input>` can be:
- a `.pptx` handed directly (this is what Claude Design's export has
  produced in practice — don't assume it must be wrapped in a zip)
- a `.zip` — it gets extracted and searched for a `.pptx` first, then an
  HTML/CSS/JS bundle (`index.html` + assets), then a bare `.pdf`
- a bare `.pdf` — repair is limited without the source; see below

Read the script's own docstring for the full pipeline description before
running it if anything about the input is unusual — it's kept in sync
with what the code actually does.

After it runs, look at `<out-dir>/repair_report.md`. It documents, in
order: what was wrong with the package structure, every shape that got
repositioned/resized (slide, before/after coordinates), the status of
every font the deck uses (installed / fetched / falling back), whether the
letter-spacing workaround applied, and a validation pass on the final PDF
(page count vs. slide count, any pages that look unexpectedly blank, any
text that still touches a page edge). Read this back to the user — it's
written to be shown, not just logged, because the whole point of this
skill is "nothing changes silently."

Outputs land in `<out-dir>`:
- `*.repaired.pptx` — still fully editable, structurally clean, no
  off-canvas shapes, original letter-spacing intact
- `*.repaired.pdf` — the clean PDF, converted from a letter-spacing-
  neutralized render copy (see defect #4) so tracked-out labels don't clip
- `repair_report.md` / `repair_report.json`

## When the input is a bare PDF with no source file

Structural repair (package structure, shape geometry, font substitution)
needs the editable source — there's no way to move a shape or fix a font
reference in something that's already been flattened to fixed vector
paths and rasterized text. `fix_export.py` still runs the same PDF
validation pass (page count sanity, blank-page check, edge-overflow check)
so you at least get an honest read on whether the PDF itself looks broken,
but say so plainly to the user rather than implying a fix happened: ask if
they can re-export from Design as a `.pptx`/zip instead, since that's
where the actual repair leverage is.

## When the input is an HTML/CSS/JS bundle

This path (`scripts/convert_html.py`) is best-effort, not backed by a real
defect investigation the way the `.pptx` path is — there was no sample of
this shape to test against. It applies the generic fixes that most
commonly break an HTML deck's print-to-PDF (forces background/color
printing, un-hides anything relying on `overflow: hidden` + scrolling,
avoids mid-element page breaks) and picks a page size from whatever the
markup hints at. If you hit a real broken HTML export, treat this as a
starting point and read `references/defect-classes.md`'s closing section
on how to diagnose a new case (render, compare, isolate, don't guess from
markup alone) rather than assuming the existing generic fixes cover it.

## Extending this skill

If a deck comes through with a defect not in the table above, the method
that found defect #4 generalizes: don't debug from the XML/CSS alone,
because "looks structurally fine" and "renders fine" are different claims
and only the second one is what the user is reporting. Render the
untouched original to PDF, render a copy with one specific, isolated
change, and compare the two — that's what confirmed the letter-spacing bug
after the geometry and font fixes alone didn't resolve the visible
clipping. `scripts/validate_pdf.py` already does the page-count/blank-
page/edge-overflow checks; add to it if you find another cheap,
objective signal worth checking automatically on every run.
