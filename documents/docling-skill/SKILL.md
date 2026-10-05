---
name: docling-skill
description: Use when an agent needs to convert local PDF, Office, spreadsheet, HTML, text, Markdown, or image files into docling-skill source.* sidecars before downstream reasoning, retrieval, wiki ingestion, or handoff.
---

# docling-skill

Use `docling-skill` as the local ingestion gate for document files. It produces an agent-only v2 `source.*` sidecar set and a compact manifest that must be checked before any agent consumes the content.

## Use When
- Input is a local file: `pdf`, `docx`, `pptx`, `xls`, `xlsx`, `csv`, `html`, `txt`, `md`, `png`, `jpg`, `jpeg`, `tif`, `tiff`, `bmp`, or `webp`.
- Downstream work needs Markdown plus on-demand quality evidence, structured Docling output, or image sidecars.
- The agent needs to decide whether conversion output is safe enough to use.

## Do Not Use When
- The source is a remote URL; fetch or browser capture belongs upstream.
- The task is chunking, summarization, tagging, embedding, or knowledge modeling.
- The file is `.doc`, `.ppt`, `.xlsm`, password-protected, corrupt, or a workbook that needs manual semantic preprocessing; ask for a clean `.docx`, `.pptx`, `.xlsx`, `.csv`, or PDF.

## Run
Always provide an explicit output directory.

```bash
conda run -n docling python -m docling_skill.cli "<input_path>" "<output_dir>"
```

If the CLI is installed directly:

```bash
docling-skill "<input_path>" "<output_dir>"
```

PDF OCR flags, only when needed:

```bash
--ocr-engine auto|tesseract|ocrmac|rapidocr
--ocr-lang <lang>  # repeatable or comma-separated
--force-full-page-ocr
--no-ocr-remediation
--pdf-audit  # optional evidence flag for eligible native formats; renderer support is soft/unavailable by default
```

## Outputs
Expected files:

- `source.manifest.json`
- `source.md`
- `source.evidence.json`

Read `source.manifest.json` first, then follow `decision.read_order`.

- Low-risk `good` output normally has `read_order: ["source.md"]`.
- Warning, `salvaged`, and `failed_for_agent` output points to `source.evidence.json`.
- Use `source.evidence.json` for structure recovery, quality signals, attempts, page/slide/sheet coverage, spreadsheet metadata, and image placeholders such as `[[image:picture-p2-1]]`.

Do not add downstream fields such as tags, keywords, categories, summaries, embeddings, or chunk IDs to `source.manifest.json` or `source.evidence.json`.

## Manifest Decision
Inspect these groups:

- Contract: `contract_version`, `producer`
- Decision: `decision.status`, `decision.risk_level`, `decision.agent_ready`, `decision.read_order`
- Source: `source.input_type`, `source.pipeline_family`, `source.title`
- Evidence pointer: `artifacts.evidence`, `warnings`, `reasons`, `counts`

Decision matrix:

| Manifest decision | Agent action |
| --- | --- |
| `good` + `low` | Use `source.md` as primary input. |
| `good` + `medium` | Use `source.md`, but inspect `source.evidence.json` before relying on details. |
| `salvaged` | Use only as OCR-remediated medium-risk output; inspect evidence. |
| `failed_for_agent` | Do not present as clean ingestion; report failure evidence from `source.evidence.json`. |

`agent_ready: true` means default-usable, not semantically proven.

## Format Checks
- PDF: inspect evidence `quality.signals.page_coverage` when page warnings exist, especially `failed_pages` and `first_page_failed`.
- Chinese-heavy output: inspect evidence `quality.signals.text_normalization` and `quality.signals.text_integrity`.
- Spreadsheets: use evidence `structured_document` and `spreadsheet` when merged cells, multi-sheet layout, spans, or offsets matter; Markdown is only a preview.
- Images: image-only output with no usable OCR text should be treated as high risk when the manifest says `failed_for_agent`.
- Figures/charts: resolve placeholders through evidence `images`; image extraction is not universal across formats.

## Success Signal
- Command exits `0`.
- All three v2 `source.*` files exist in the output directory.
- Manifest has been checked before using `source.md`.

## Failure Report
When ingestion is not clean, report:

- input path and input type
- command exit code or exception
- manifest `decision.status`, `decision.risk_level`, `reasons`, `warnings`
- relevant evidence `quality.signals`
- evidence `selected_attempt` and whether OCR remediation was applied
