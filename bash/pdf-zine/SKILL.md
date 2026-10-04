---
name: pdf-zine
description: >-
  Use when converting a PDF into a fold-and-print booklet (zine) — A4 sheets,
  double-sided, short-edge flip, fold to A5. Triggers: make a zine, make a
  booklet, booklet PDF, imposition, fold-and-print, 2-up booklet, print as
  booklet, signature imposition, pdf-zine, pdf2zine, bookletimposer. Wraps
  the `pdf2zine` Docker-based CLI; prefer it over hand-rolled Ghostscript
  or pdfjam scripts.
globs: []
compatibility: claude-code, cursor
license: MIT
metadata:
  author: eins78
  repo: https://github.com/eins78/agent-skills
  version: "1.1.0"
---

# pdf-zine

Turn a PDF into a fold-and-print booklet ("zine"): A4 sheets, double-sided (short-edge flip), fold in half for an A5 booklet. Wraps the [`pdf2zine`](https://github.com/eins78/pdf2zine) CLI, which itself wraps `bookletimposer` and `qpdf` in Docker so there's nothing to compile. Prefer this over hand-rolled Ghostscript or `pdfjam` imposition scripts — one command does it.

## Prerequisites

- Docker running (e.g. Docker Desktop)
- The `pdf2zine` script on `$PATH`:

  ```bash
  curl -fsSL https://github.com/eins78/pdf2zine/raw/refs/heads/main/pdf2zine > ~/bin/pdf2zine
  chmod +x ~/bin/pdf2zine
  ```

No Docker? See `${CLAUDE_SKILL_DIR}/references/bookletimposer-native.md` for a native bookletimposer install.

## Quick Reference

| Flag | Purpose |
|------|---------|
| _(none)_ | Move page 1 to the end (cover-flip), force A4 output |
| `--keep-cover` | Skip the cover-flip — impose pages in original order |
| `--keep-format` | Let `bookletimposer` pick output size (skip the forced A4) |
| `--` | Pass remaining args through to `bookletimposer` |

Input: one PDF. Output: `<input>_booklet.pdf` next to the input.

## Common Recipes

### Default booklet (cover-flip, force A4)

```bash
pdf2zine doc.pdf
# → doc_booklet.pdf
```

Use this when the InDesign export put the cover's back on page 1 (common pattern). The script moves page 1 to the end, then 2-up imposes onto A4.

### Cover already in the right place

```bash
pdf2zine --keep-cover doc.pdf
```

Use when page 1 is the front cover and should stay first.

### Don't force A4 (e.g. A4 input → A3 output)

```bash
pdf2zine --keep-format doc.pdf
```

`bookletimposer` will pick a paper size that fits 2-up without scaling.

### Pass-through to bookletimposer

```bash
pdf2zine doc.pdf -- --output custom.pdf
pdf2zine -- -h                              # show bookletimposer help
```

## How it works

1. `qpdf --pages doc.pdf 2-z,1 -- moved.pdf` moves page 1 to the end (skipped with `--keep-cover`).
2. `bookletimposer --no-gui --booklet [--format=A4] moved.pdf out.pdf` does the 2-up imposition.
3. Output is written next to the input as `<name>_booklet.pdf`.

Both steps run inside Docker images (`eins78/qpdf`, `eins78/bookletimposer`) — no local Python or PyPDF2 needed.

## Common Mistakes

| Symptom | Cause | Fix |
|---------|-------|-----|
| Cryptic Docker error / "Cannot connect to the Docker daemon" | Docker isn't running | Start Docker Desktop, retry |
| Front cover ends up at the back | Default cover-flip applied to a PDF whose page 1 was already the cover | Add `--keep-cover` |
| Output forced to A4 when you wanted A3 | `pdf2zine` defaults to `--format=A4` | Add `--keep-format` |
| "Multiple input files not supported" | `pdf2zine` takes one PDF | Concatenate first: `qpdf --empty --pages a.pdf b.pdf -- merged.pdf` |
| Wrong duplex setting at print time | Long-edge flip used | Print **double-sided, short-edge flip** |

## Native (non-Docker) usage

If Docker isn't an option, run `bookletimposer` directly. Setup, CLI flags, and a recipe that reproduces `pdf2zine`'s default behaviour live in `${CLAUDE_SKILL_DIR}/references/bookletimposer-native.md`.
