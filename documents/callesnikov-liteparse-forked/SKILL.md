---
name: callesnikov-liteparse-forked
description: Parse PDFs and other documents locally with LiteParse/lit when the user asks Codex to extract text, preserve layout, produce JSON with bounding boxes, batch-parse documents, inspect specific PDF pages, or generate page screenshots for visual review. Use for PDF, DOCX, PPTX, XLSX, images, OCR, page-range extraction, and local document-ingestion workflows where cloud parsing is not desired.
---

# Callesnikov Liteparse Forked

Use LiteParse as a local, fast document parser from the Codex shell. Prefer read-only inspection first, parse into new output folders, and keep source documents unchanged.

## Installed Runtime

This skill has a local Node install of LiteParse. Use the wrapper first:

```powershell
C:\Users\User333\.codex\skills\callesnikov-liteparse-forked\scripts\lit.ps1 --version
```

Current local package: `@llamaindex/liteparse@2.0.1`.

Current verified CLI version from `lit --version`: `2.0.0` (the package and CLI version strings may differ).

Latest npm version checked on 2026-05-28: `@llamaindex/liteparse@2.0.1`.

Local CLI target:

```powershell
C:\Users\User333\.codex\skills\callesnikov-liteparse-forked\tools\liteparse-node\node_modules\.bin\lit.cmd
```

Reference files saved for quick future lookup. Read them only when the built-in command navigator is not enough:

- `references/upstream-liteparse-readme.md` for upstream project capabilities, formats, caveats, and current wording.
- `references/upstream-node-readme.md` for Node package usage and local CLI behavior.
- `references/upstream-python-readme.md` for Python package usage when a Python workflow is requested.
- `references/upstream-agent-skill.md` for the original LiteParse agent-skill workflow and command taxonomy.

## Source Of Truth

Fetch or update future setup data from these upstream locations:

- Main repo: `https://github.com/run-llama/liteparse`
- Agent skill source: `https://github.com/run-llama/llamaparse-agent-skills`, skill path `skills/liteparse/SKILL.md`
- Node package: `@llamaindex/liteparse`
- Python package: `liteparse`
- Rust crate/CLI: `liteparse`
- Docs: `https://developers.llamaindex.ai/liteparse/`

Before installing or updating, re-check the upstream README/package metadata because LiteParse is moving quickly. Record the version actually installed in the skill folder.

Update locally only:

```powershell
npm install --prefix C:\Users\User333\.codex\skills\callesnikov-liteparse-forked\tools\liteparse-node @llamaindex/liteparse@latest
```

After update, run the wrapper `--version` and all three subcommand help checks before using it on user PDFs.

## Intent Navigator

Use this table to translate loose user phrasing into the right operation.

| User intent / wording | Command family | Default behavior |
|---|---|---|
| "прочитай PDF", "что внутри", "вытащи текст", "распарси" | `parse` | Text output, `--no-ocr` first for speed unless scan/OCR is implied |
| "сохрани структуру", "координаты", "таблицы", "bbox", "layout" | `parse --format json` | JSON output with text items and bounding boxes |
| "страницы 5-10", "только page X", "извлеки этот раздел" | `parse --target-pages` | Parse only requested pages |
| "это скан", "плохо читается", "OCR", "фото PDF" | `parse` with OCR | OCR enabled, set `--ocr-language`, consider `--dpi 300` |
| "быстро", "черновик", "текстовый PDF" | `parse --no-ocr` | Fast text-first extraction |
| "покажи страницу", "нужно увидеть", "скриншоты", "визуально" | `screenshot` | PNG screenshots of selected pages |
| "папка PDF", "много документов", "прогони всё" | `batch-parse` | New output directory, usually `--recursive --extension .pdf` |
| "найди ответ по PDF", "сравни", "суммаризируй" | `parse`, then analyze | Parse first, then search/summarize/cite pages |
| "docx/pptx/xlsx/image" | `parse` if converters exist | Check LibreOffice for Office, ImageMagick for images |
| "зашифрован", "пароль" | `parse --password` | Ask for password, never store it in manifest/logs |

If the request is vague, choose a conservative default: text parse into a new timestamped folder, then inspect whether output is enough. Ask only when page range, password, destination, or format is necessary and cannot be inferred.

## Install Layout

When the user explicitly requests installation, keep all skill-owned files under this skill directory:

- `tools/` for local package/project files.
- `downloads/` for fetched upstream metadata, release manifests, checksums, and optional source archives.
- `outputs/` for parser output created during user tasks unless the user names another destination.
- `tessdata/` for manually downloaded Tesseract language data.
- `tmp/` for temporary conversion/screenshot work.

Prefer a local install over a global install. Do not use `npm i -g`, `pip install` into global Python, or `cargo install` globally unless the user explicitly asks for global setup.

Recommended future setup options, in order:

1. Node local CLI:
   `npm install --prefix <skill>/tools/liteparse-node @llamaindex/liteparse`
   Then run with `<skill>/tools/liteparse-node/node_modules/.bin/lit`.
2. Python virtual environment:
   create `<skill>/tools/liteparse-py/.venv`, install `liteparse` inside it, then run `.venv`'s `lit`.
3. Rust binary:
   use only if the user wants Rust/cargo or prebuilt release behavior is not enough.

For maximum practical usefulness, future setup should capture:

- The LiteParse CLI package itself, preferably Node local install or Python venv.
- The upstream `README.md` and `packages/node/README.md` or `packages/python/README.md`.
- The upstream LiteParse agent `SKILL.md` for comparison.
- Optional `tessdata/*.traineddata` files for requested OCR languages.
- Optional notes for LibreOffice and ImageMagick presence, but do not install those system tools without explicit user approval.

## Capability Check

When invoked, first find an available `lit` executable without installing anything:

```powershell
C:\Users\User333\.codex\skills\callesnikov-liteparse-forked\scripts\lit.ps1 --version
Get-Command lit -ErrorAction SilentlyContinue
Get-Command liteparse -ErrorAction SilentlyContinue
Test-Path "$PSScriptRoot\tools\liteparse-node\node_modules\.bin\lit.cmd"
```

If no `lit` exists, explain that setup is needed and offer the local skill-folder install plan. Do not auto-install.

Check version:

```powershell
C:\Users\User333\.codex\skills\callesnikov-liteparse-forked\scripts\lit.ps1 --version
```

## Core Commands

Use quotes around paths. Prefer absolute paths on Windows.

Parse to text:

```powershell
C:\Users\User333\.codex\skills\callesnikov-liteparse-forked\scripts\lit.ps1 parse "C:\path\document.pdf" -o "C:\path\output.txt"
```

Parse to structured JSON with bounding boxes:

```powershell
C:\Users\User333\.codex\skills\callesnikov-liteparse-forked\scripts\lit.ps1 parse "C:\path\document.pdf" --format json -o "C:\path\output.json"
```

Parse selected pages:

```powershell
C:\Users\User333\.codex\skills\callesnikov-liteparse-forked\scripts\lit.ps1 parse "C:\path\document.pdf" --target-pages "1-5,10,15-20" --format json -o "C:\path\pages.json"
```

Fast text-only parse for digitally generated PDFs:

```powershell
C:\Users\User333\.codex\skills\callesnikov-liteparse-forked\scripts\lit.ps1 parse "C:\path\document.pdf" --no-ocr -o "C:\path\document.txt"
```

Generate screenshots for visual inspection:

```powershell
C:\Users\User333\.codex\skills\callesnikov-liteparse-forked\scripts\lit.ps1 screenshot "C:\path\document.pdf" --target-pages "1,3,5" -o "C:\path\screenshots"
```

Batch parse:

```powershell
C:\Users\User333\.codex\skills\callesnikov-liteparse-forked\scripts\lit.ps1 batch-parse "C:\path\input" "C:\path\outputs" --extension .pdf --recursive --format json
```

Important option names from current docs:

- `--format json|text`
- `-o` / `--output`
- `--target-pages`
- `--max-pages`
- `--no-ocr`
- `--ocr-language`
- `--ocr-server-url`
- `--tessdata-path`
- `--dpi`
- `--preserve-small-text`
- `--password`
- `--config`
- `--num-workers`
- `-q` / `--quiet`

For screenshots, current repo docs use `--target-pages` and `-o`/`--output-dir`; verify with `lit screenshot --help` if a command fails because older skill examples used `--pages`.

Installed CLI help confirmed these command families:

```powershell
C:\Users\User333\.codex\skills\callesnikov-liteparse-forked\scripts\lit.ps1 --help
C:\Users\User333\.codex\skills\callesnikov-liteparse-forked\scripts\lit.ps1 parse --help
C:\Users\User333\.codex\skills\callesnikov-liteparse-forked\scripts\lit.ps1 screenshot --help
C:\Users\User333\.codex\skills\callesnikov-liteparse-forked\scripts\lit.ps1 batch-parse --help
```

## Request Handling

Interpret PDF/document requests conservatively:

- "Вытащи текст", "распарси", "прочитай PDF": produce `.txt` first; use JSON too when layout, coordinates, tables, or citations matter.
- "Сохрани структуру", "таблицы", "где на странице": use `--format json`.
- "Только страницы X-Y": use `--target-pages`.
- "Быстро": use `--no-ocr` unless the PDF is scanned or text output is empty.
- "Скан", "фото", "OCR", "плохо извлеклось": enable OCR, raise DPI if needed, and consider screenshots for manual/vision review.
- "Покажи страницы": use `lit screenshot`, then inspect/render selected PNGs.
- "Папка PDF": use `batch-parse` into a new output directory.
- "Найди/ответь по PDF": parse to text/JSON, then search/summarize locally; cite page numbers when available.

Ask a short clarification only when the output format, page range, destination, or password is required and cannot be inferred.

## Output Rules

Never overwrite user files silently. Write outputs to a new directory by default:

`<input-parent>\liteparse-output\<input-stem>-<timestamp>\`

If working inside the skill folder, use:

`<skill>\outputs\<task-stem>-<timestamp>\`

Use clear filenames:

- `<stem>.txt` for plain text.
- `<stem>.json` for structured output.
- `screenshots/page-0001.png` style for images when LiteParse permits naming, otherwise preserve LiteParse output and report it.
- `manifest.json` for run metadata when doing substantial work: input path, command, LiteParse version, page range, OCR settings, timestamp, output paths.

Keep original PDFs unchanged. Do not repair, linearize, decrypt, compress, rotate, or rename source documents unless the user explicitly asks for that separate operation.

## Encoding And Decoding

Prefer UTF-8 for all text outputs. On Windows, when reading output back into Codex, use `Get-Content -Encoding UTF8` or a parser that preserves UTF-8. If text looks mojibaked, re-read with explicit encoding before concluding extraction failed.

For JSON output:

- Treat text coordinates as page-local bounding boxes.
- Preserve numeric bbox values as emitted.
- Do not invent table structure from coordinates unless asked; describe it as reconstructed/inferred.
- Keep large JSON out of chat; summarize and cite saved paths.

For scanned PDFs:

- OCR can be much slower than text extraction.
- Low confidence or garbled OCR should be reported honestly.
- Use `--ocr-language` matching the document language when known.
- Use `--dpi 300` for difficult scans, while warning that speed and file size will increase.

For encrypted PDFs, ask for the password and pass it with `--password`; do not store the password in manifests or logs.

## Speed Claims

Treat claims like "450 pages in one second" as best-case marketing/benchmark language, usually for text PDFs without OCR on favorable hardware. Expect slower performance for scanned PDFs, OCR, images, Office conversion, complex layouts, high DPI screenshots, and external OCR servers. When performance matters, run a timed smoke parse on a representative file and report pages/sec with the exact command.

## Failure Handling

If `lit` fails:

1. Run `lit --help` and the relevant subcommand `--help`.
2. Check whether the input file exists and is readable.
3. Try `--no-ocr` for digitally generated PDFs.
4. Try a small `--target-pages "1-3"` sample.
5. For Office documents, check LibreOffice availability.
6. For images, check ImageMagick availability.
7. For scanned PDFs, check OCR language/tessdata.
8. Report the failing command and stderr; do not hide parse failures behind a polished summary.

## Boundaries

LiteParse is for extraction, layout-aware parsing, OCR, and screenshots. It is not a full PDF editor. For merging, splitting, rotating, redacting, signing, or modifying PDFs, use another PDF workflow/tool and keep LiteParse for inspection/extraction.
