---
name: ppt-master-execution-pitfalls
description: Use when running ppt-master Generate-PPTX routes.
metadata:
  version: "1.0.0"
---

# ppt-master Execution Pitfalls

Pitfalls observed in real Generate-PPTX runs. Each row = symptom + actual fix.

## SVG → PPTX converter hard rules

| # | Symptom | Actual fix |
|---|---|---|
| 1 | `<line>` element rejected: "cannot use filter; supported native targets are rect, circle, path, and text" | Strip `filter="url(#glow)"` from `<line>` and `<polyline>`. Convert arrows to `<path d="M x y L x y L x y Z"/>` with a triangle tail. |
| 2 | `spec_lock typography-size recurrence: undeclared font-size N (M occurrences) exceeds the sparse-display limit` | Every recurring font size must be declared in `spec_lock.md` `## typography` as a lowercase snake_case role with px anchor. M > 2 occurrences triggers the error. Audit all SVG `font-size="N"` values and map them into declared roles (body=24, title=42, subtitle=32, annotation=18, footnote=14). |
| 3 | Pattern fills like `<pattern id="gridp">` render as `ltUpDiag` diagonal lines in the exported PPTX | The converter falls back to a generic pattern. Replace with explicit per-line `<line x1=...>` elements (40px grid × N+1 lines). Costs ~80 SVG elements but guarantees faithful export. |
| 4 | XML well-formedness error: `not well-formed (invalid token)` | Bare `&` in text breaks SVG. Always run text through `html.escape(s, quote=True)` before insertion. Common offenders: ampersand, HTML entity names like `&nbsp;`/`&mdash;`, smart quotes if not raw Unicode. |

## spec_lock.md schema traps

| # | Symptom | Actual fix |
|---|---|---|
| 5 | `design_spec.md schema: missing section 'speaker_notes'` | Section heading MUST exactly match `^X\. Speaker Notes (Requirements\|Plan\|Strategy)$`. |
| 6 | `design_spec.md schema: content outline has no Slide blocks` | Slide blocks MUST use `#### Slide NN -` (4 hashes, 2-digit zero-padded number, no "P" prefix). The "P" prefix or `### Slide PNN` will silently fail to match. |
| 7 | `spec_lock canvas viewBox is required` | `## canvas` section MUST include both `viewBox: 0 0 W H` and `format: PPT 16:9` (or other named format). |
| 8 | `Master export requires spec_lock.md typography rows: title, body` | `## typography` section MUST include `title_family` AND `body_family` as separate roles, plus `font_family` for backwards compatibility. |

## Delegated research pitfall

| # | Symptom | Actual fix |
|---|---|---|
| 9 | Three parallel research subagents all hit 600s timeout with no file written | Subagents waste turns on `web_extract` round-trips. Never delegate "produce markdown report" as one task. Either (a) dispatch ≤3 sites each with a hard line cap, or (b) run web fetches in the main agent via `urllib`/`curl` and assemble the markdown yourself. Do not retry the same subagent shape. |

## Environment / setup

| # | Symptom | Actual fix |
|---|---|---|
| 10 | confirm UI server fails to start with `flask not found` | System Python may be PEP-668. Build a venv with `uv venv /tmp/ppt-env --python 3.13 && uv pip install --python /tmp/ppt-env/bin/python flask python-pptx Pillow uharfbuzz skia-pathops XlsxWriter`. All ppt-master scripts must be invoked via `/tmp/ppt-env/bin/python`, not system python. |
| 11 | `skia-pathops` import fails despite "audited" success message | The wheel installs as `pathops` module, not `skia_pathops`. `import pathops` works. Do not waste cycles fixing the import name — write code against `pathops`. |

## User delegation patterns

| # | Symptom | Actual fix |
|---|---|---|
| 12 | User delegates the entire 3-stage Confirm UI flow and says "继续到底" | Write all 3 stage JSONs + `result.json` with `status: confirmed` and `mode: user-delegated` in one pass. The blocked gates are skipped only when the user explicitly grants delegation — re-confirm wording if ambiguous. |
| 13 | User says "你搜太慢了 / 直接告诉我要搜什么" | Stop autonomous fetching. Emit a structured task list (file name → target page → official source URL → required spec) so the user can drop assets into a known path. Do not loop on slow fetches. |

## Visual review pitfalls

| # | Symptom | Actual fix |
|---|---|---|
| 14 | Low-DPI vision-model review flags "标题被表格遮挡/截断" that ground-truth XML shows is impossible | Always cross-check vision review against actual `<a:off x y>` and `<a:ext cx cy>` in `ppt/slides/slideN.xml`. Low-DPI render + vision OCR produces false positives for Chinese glyphs; the PPTX XML is ground truth. |
| 15 | Page-by-page visual review loops forever at low DPI | Use LibreOffice → PDF → `pdftoppm -r 150` for high-DPI raster, then vision-analyse cropped regions. Default 60 DPI is too lossy for Chinese glyph metrics. |

## Topic research gate

| # | Symptom | Actual fix |
|---|---|---|
| 16 | Topic-only research gate fires repeatedly | Run the bounded research once per `topic-research.md` and capture results in `sources/*.md`. Treat the resulting markdown as content authority; do not re-research every Confirm UI round.