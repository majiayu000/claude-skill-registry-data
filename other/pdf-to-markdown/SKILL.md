---
$schema: https://gist.githubusercontent.com/remorses/9f3737a6f516c01f4bdb612045c64072/raw/agent-skill.schema.json
name: pdf-to-markdown
description: >
  Convert PDF files to markdown using tested CLI tools. Use when the user asks
  to convert a PDF to markdown, extract text from a PDF, or asks about
  pymupdf4llm, marker, or docling. Covers which tool to pick, exact commands,
  and known output-quality gotchas.
---

# pdf-to-markdown

Three tools tested on a real 73-page book PDF (prose + screenshots + watermarks).
Pick by need, default to marker for quality, pymupdf4llm for speed.

| Tool | Time (73p) | Quality verdict |
|---|---|---|
| marker | ~4 min | Best. Recovers hyperlinks, extracts images as files, dedupes text |
| pymupdf4llm | ~1 min | Fast, readable prose. But duplicates sentences and garbles screenshots inline |
| docling | ~6.5 min | Decent prose and headings, but bloats output with base64 images and zero links |

## marker (best quality)

Needs `llama-server` for text recognition. On macOS install first:

```bash
brew install llama.cpp
```

Convert:

```bash
uvx --from marker-pdf marker_single <input.pdf> --output_dir /tmp/marker-out --output_format markdown
```

- Output lands in `<output_dir>/<pdf basename>/<pdf basename>.md`
- Images are extracted as `.jpeg` files next to the markdown, referenced by relative path. Keep the folder together when moving output
- Recovers inline hyperlinks from the PDF. No duplicated sentences

## pymupdf4llm (fastest)

With image extraction (images saved as PNG files, referenced by relative path):

```bash
uvx --from pymupdf4llm python - <<'EOF'
import pathlib, os, re, pymupdf4llm

os.chdir('/path/to/destination')  # so image refs come out relative
for pdf in sorted(pathlib.Path('.').glob('*.pdf')):
    # slug: path with spaces/parens breaks pymupdf4llm's image saving (see gotcha below)
    slug = re.sub(r'[^a-zA-Z0-9]+', '-', pdf.stem).strip('-').lower()
    md = pymupdf4llm.to_markdown(pdf.name, write_images=True,
                                 image_path=f'{slug}-images', image_format='png',
                                 show_progress=False)
    pdf.with_suffix('.md').write_text(md, encoding='utf-8')
EOF
```

Without images, drop `write_images`/`image_path`/`image_format`.

Useful flags (verified against the source):

| Flag | Default | Use it when |
|---|---|---|
| `pages` | all pages | Convert a page range. Int or list of ints, 0-indexed |
| `embed_images=True` | False | Inline images as base64 instead of saving files. Mutually exclusive with `write_images` |
| `image_dpi` | 150 | Higher (e.g. 300) for sharper screenshot files agents can read |
| `ocr_dpi` | 150 | Higher for better OCR of small text |
| `use_ocr` | `OCRMode.SELECT_KEEP_OLD` | `NEVER` skips OCR entirely (fast); `FORCE_DROP_OLD` OCRs every page |
| `force_text=True` | False | Also extract text that sits inside picture regions |
| `render_html_tables=True` | False | Render tables as HTML instead of markdown pipes, better for complex/scrambled tables |
| `edge_threshold` | None | Layout detection sensitivity, lower values split paragraphs more aggressively |
| `ocr_language` | `"eng"` | Pass other languages for non-English PDFs |
| `ocr_function` | auto | Plug in a custom OCR callable (e.g. your own Tesseract wrapper) |

OCR needs an engine; on this machine Tesseract is available and gets picked automatically.

Known output issues: see the issue taxonomy below. pymupdf4llm hits nearly all of them.

Path bug (crashes with `FzErrorSystem: cannot open file`): pymupdf4llm sanitizes image paths for the markdown reference (spaces → `_`, parens → `-`) and uses that sanitized string as the actual save path, so any space, paren, or bracket in the PDF name or `image_path` breaks saving. Always `os.chdir` into the output folder, pass the PDF name relative, and slugify the `image_path` to alphanumerics and dashes.

## docling

```bash
uvx docling convert <input.pdf> --to md --output /tmp/docling-out
```

- By default embeds every image as base64 inline, output can reach tens of MB. Strip with a regex over `!\[Image\]\(data:image[^)]+\)` or use image export options before relying on the file
- Does not recover hyperlinks
- Clean table of contents tables, decent heading detection

## Issue taxonomy: what these CLIs get wrong, and how to fix

All verified on 5 real book PDFs (528 pages). Run the bundled cleanup script for the mechanical fixes:

```bash
# 1. dump the PDF text layer (ground truth for matching)
uvx --from pymupdf python -c "
import pymupdf, pathlib, sys
doc = pymupdf.open(sys.argv[1])
pathlib.Path(sys.argv[2]).write_text('\n'.join(p.get_text() for p in doc))
" input.pdf /tmp/pdf-text.txt

# 2. clean the markdown
bun ~/.config/opencode/skills/pdf-to-markdown/clean.ts --md output.md --pdf-text /tmp/pdf-text.txt \
  --extra-noise 'your watermark or footer regex'
```

| Issue | Which tools | Fix |
|---|---|---|
| Duplicated sentences/paragraphs (overlapping text layers) | pymupdf4llm | Dedupe by normalized sentence, but only remove copies that appear once in the PDF text layer, so the author's real repetition survives. `dedupeSentences` in clean.ts |
| Garbled OCR of screenshots (token soup inline) | pymupdf4llm always, docling partially, marker rarely | Delete the OCR text, keep the image file (agents read images with vision). `removePictureBlocks` in clean.ts |
| OCR garbage prefixes glued to real text (`Brp3 Be Bn2 Adam has replied...`) | pymupdf4llm | Find first 3-word n-gram that matches the PDF text layer, drop everything before it. `garbageFilter` in clean.ts |
| Headings fused into mega-paragraphs | pymupdf4llm, docling | Extract titles from the book's TOC table, split fused paragraphs at each title (recurse: one paragraph can hold several), insert `## title`. `restoreHeadings` in clean.ts |
| Bogus headings (bold body sentences promoted to `#`) | pymupdf4llm, marker | Demote by rules: ends with `,`/`.`/`;`, italic-wrapped, or level 4+ with >8 words followed by lowercase text or another heading. Sample every demotion and eyeball before accepting. `demoteBogusHeadings` in clean.ts |
| Boilerplate noise (watermarks, footers, page numbers as lines) | all | Regex strip, book-specific. Pass watermarks/footers via `--extra-noise` |
| Screenshots with no image ref at all | pymupdf4llm | Render the full PDF page to PNG with pymupdf (`page.get_pixmap(dpi=150)`), insert the ref at the right anchor by hand |
| Split headings (title breaks across pages: `# Chapter 9...` + `# Agency`) | pymupdf4llm | Merge consecutive `#` lines when the first matches a chapter pattern and the second is short |
| Restored heading duplicates an existing heading nearby | cleanup scripts themselves | Drop the duplicate if a same-text heading exists within a few lines above. `dedupeHeadings` in clean.ts |
| Content truncated mid-paragraph (fused and lost in the PDF's own text layer) | any, from source PDF | Unfixable automatically. Report honestly; the content only exists in the PDF itself |
| PDF's own embedded OCR layer is garbage (not the converter's fault) | scanned PDFs | The text layer pollutes both the conversion and any matching. Validate matchers on known-good prose before trusting pass/fail counts |

## Workflow rules

- Run with `uvx` so tools stay isolated, never global pip installs
- First run downloads ML models (marker ~2 GB). Use generous timeouts, 10+ min
- After converting, verify image refs resolve: extract `!\[...\](...)` paths from the markdown and check each file exists. Report count of refs and missing files
- After converting, read a sample of the output (start, middle, end) and report quality honestly: duplicated sentences, garbled OCR, swallowed headings
- Check `file <output>.md` content exists and is not empty before telling the user it worked
