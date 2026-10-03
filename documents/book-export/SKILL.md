---
name: book-export
description: Assemble the full manuscript from chapters/ into a typeset PDF (and optionally EPUB). Use when the user asks to build the book, export the book, compile a draft, produce a readable copy, or ship the manuscript. Defaults to a DRAFT-watermarked preview build; will refuse to produce a ship build if any chapter is not ship-ready.
model: sonnet
---

# book-export

Final-assembly skill for *Builder-Leader: The AI Exoskeleton That Crosses the Gap*. Takes the chapter files in `chapters/` and produces a typeset PDF in `export/`.

## When to run

- User says "build the book", "export the book", "ship it", "produce a PDF", "finish the book", "compile the draft", or anything pointing at final assembly.
- Automated gates at milestone boundaries (end of Stage 2, end of Stage 3, etc.).

## Modes

Two modes, passed as the first argument to `scripts/build.sh`:

| Mode | Behavior |
|---|---|
| `preview` (default) | Compiles every chapter in `chapters/` regardless of status. Stamps `DRAFT — NOT FOR CIRCULATION` in the running header of every page and large on the title page. Writes status column in the TOC. For sharing pre-ship drafts with named readers. |
| `ship`    | Refuses to compile unless **every** chapter's frontmatter `status` field is `ship-ready`. No watermark. Clean TOC. For final distribution. |

Pass `epub` as the second argument to also produce an EPUB.

```
./build.sh preview        # → export/book-preview.pdf
./build.sh preview epub   # → export/book-preview.pdf + export/book-preview.epub
./build.sh ship           # → export/book.pdf (gated on ship-ready)
```

## Inputs

- `chapters/*.md` — chapter files, sorted by filename (00 → 10)
- `canon/thesis.md` — used to extract title and one-line description
- Each chapter's YAML frontmatter (`chapter`, `title`, `status`, `word_count`)

## Procedure

1. **Prepare.** Ensure `export/` exists. Check pandoc + xelatex are on PATH. If missing, tell the user to install and stop.
2. **Gate (ship mode only).** Read frontmatter of every chapter file. If any `status` is not `ship-ready`, print the list of offenders and exit 1.
3. **Strip frontmatter.** For each chapter file, produce a frontmatter-stripped copy in a tempdir. Keep chapter order by filename prefix.
4. **Assemble.** Concatenate into a single `manuscript.md` with page breaks between chapters (pandoc `\newpage` raw LaTeX).
5. **Build TOC data.** Derive title list from frontmatter titles. Status column appears in preview mode only.
6. **Invoke pandoc.** Uses `templates/book.tex` as header include, `templates/titlepage.tex` as before-body include. xelatex engine. 6"×9" trim. Iowan Old Style body, Avenir Next display.
7. **Report.** Print output path, final page count, and any pandoc warnings.

## Typography decisions (locked)

- **Trim:** 6" × 9" (standard trade hardcover)
- **Body:** Iowan Old Style 11/15pt (ships with macOS, book-optimized)
- **Display:** Avenir Next for chapter numbers, chapter titles, running heads
- **Chapter opener:** drop cap (40pt first letter) + small caps first three words of chapter
- **Pull quotes:** fenced div `::: pullquote ... :::` — rendered larger italic with rule above/below, no quote marks
- **Block quotes:** standard markdown `>` — indented, slightly smaller, roman
- **Attributions / citations:** numbered endnotes per chapter via pandoc footnotes (`[^1]` markdown). Currently zero citations in chapters; wired for future use.
- **Running heads:** verso = book title (small caps), recto = chapter title (italic). Folio outer. Preview mode adds `DRAFT — NOT FOR CIRCULATION` in header center.
- **Front matter:** title page with title + subtitle + author + DRAFT notice + copyright, then TOC
- **Back matter:** about the author placeholder (stub for later)

## Copyright notice (title-page verso, preview and ship)

```
Copyright © 2026 Justin Johnson. All rights reserved.
No part of this manuscript may be reproduced, distributed, or transmitted
without the prior written permission of the author.
Working title; subject to change.
```

## Pull-quote markdown convention

To render a pull quote in any chapter, use a pandoc fenced div:

```markdown
::: pullquote
You can't read your way across the gap. You cross it by building.
:::
```

Attribution, if present, goes on the next line inside the div, prefixed by an em-dash-free separator (the project bans em-dashes):

```markdown
::: pullquote
The harness is the moat.

, Justin Johnson, Run Data Run
:::
```

The skill will render this as a centered pull quote with the attribution styled smaller.

## Dependencies

- `pandoc` 3.x (installed via Homebrew)
- `xelatex` from MacTeX / BasicTeX
- LaTeX packages: `fontspec`, `microtype`, `geometry`, `fancyhdr`, `xcolor`, `hyperref`, `setspace`, `parskip`

If any LaTeX package is missing, the skill prints the exact `sudo tlmgr install` command to fix it and exits.

## What this skill does NOT do

- Does not modify any chapter file.
- Does not run fact-checking or red-team. Those are `book-fact-check` and `book-red-team`.
- Does not publish. Distribution is a separate human step.
- Does not attempt cover art. Cover is a later concern.

## Output location

- `export/book-preview.pdf` — preview builds
- `export/book.pdf` — ship builds
- `export/book-preview.epub` / `export/book.epub` — when epub flag is set
- `export/.build.log` — pandoc stderr from the latest build
