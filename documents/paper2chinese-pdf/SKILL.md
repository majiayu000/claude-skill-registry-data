---
name: paper2chinese-pdf
description: "Translate English academic research PDFs into high-fidelity, full Simplified Chinese PDF and editable Word DOCX editions; exact English title under Chinese title; inline source-faithful figures/tables/equations; preserve true math indices; verify page spacing and original text alignment; output PDF, DOCX, or both as requested."
license: MIT
---

# Paper2Chinese PDF — High-fidelity academic translation

## Trigger & contract
Use for PDF-to-Chinese research-paper translation, especially SHPB/impact-mechanics, cementitious materials, materials science, and other technical papers. It is a **full translation and layout workflow**, not a summarizer, not a bibliography search engine, and not an automatic promise of publication-quality accuracy. The deliverable is **one verified Chinese paper per source, in the requested format**: PDF, editable Word (`.docx`), or both. **Default to PDF only** if the user has not specified. Never silently convert a PDF-only archival task into Word.

**Absolute standards**
1. Preserve the author's meaning, section progression, methods, data, limitations, nomenclature, mathematical notation, units, figure/table numbering, citations, and reference list. Do not fabricate missing data, fix original inconsistencies silently, or extrapolate from other publications.
2. Put the **Chinese title first**, then the **exact English title** immediately beneath it; show author, journal, year, DOI only if verified in the original.
3. **Figures follow discussion**: insert each original figure (and its panels) at the first appropriate local passage. Include Chinese figure captions; avoid placing a stack of figures in a distant appendix.
4. **Tables follow discussion**: transcribe the table faithfully into Chinese where feasible, preserving every cell and unit; complex tables may be cropped as original images with Chinese captions or bilingual header notes if transcription cannot be validated. No table missing or relegated to the end.
5. **Equations follow derivations**: typeset or insert a high-resolution crop of the original mathematical equation *in situ*, with its label; never substitute an explanation for a formula or approximate an equation from OCR.
6. Preserve original English references unless the user requests another treatment. Preserve appendices in their corresponding appendix sections, not intermingled into the main body.
7. **Never** make a 'Chinese text + entire English original attached at end' substitute, or call a condensed reading guide a full translation.
8. Keep filename numbering exactly: `4.paper_title_中文版.pdf` and, if requested, `4.paper_title_中文版.docx` correspond to source `4.paper_title.pdf`. Folder is authoritative: if the user explicitly says a folder contains PDF only, never drop DOCX into it.
9. Translate and validate **one paper at a time**. Do not overwrite a previously approved edition without explicit permission; keep draft/render/check images in temporary working directories, never official library.

## Workflow (complete each gate before next)

### Gate 0: Source and reference samples
- Open the complete source PDF; if user supplied examples of successful Chinese editions, render sample pages from those and match their legibility and structure (e.g., prominent Chinese title, smaller English title, normal academic paragraphs, figure-caption proximity).
- Record journal, DOI (only verified), source page count, section tree, page reading order, and expected figures/tables/numbered equations/appendices/references.
- Check if text is embedded. For scanned or garbled pages, inspect page images first. Do NOT blindly apply bulk OCR on technical equations or tables.
- If the PDF/file is inaccessible, request it again; do not reconstruct unseen material from abstracts.

### Gate 1: Create a content inventory
- Render source pages, inspect multi-column order and panel labels.
- Extract headings, paragraphs, figure/table anchor sentences, captions, graphics, equation screenshots, footnotes and the bibliography, preserving a **source page locator** for each.
- Maintain a reconciliation log with columns: source page/section, material ID, translated location, verification, issues.
- For tables, check row/column counts, merged cells, units, negative signs, SDs, superscripts, significant digits and footnotes.
- For equations, record exactly the printed symbol names/subscripts/superscripts/sign conventions; preserve original equation number.

### Gate 2: Full, controlled translation
- Translate by continuous **semantic paragraphs** in source order, ensuring complete coverage rather than disconnected OCR snippets.
- Place `[UNCERTAIN: page n, reason]` in the working draft for any unreadable fragment; do not publish such markers as a 'finished' translation.
- On ambiguous or contradictory original claims, preserve source data and append a compact, clearly labeled **译者核对注** at the relevant passage; do not silently correct the source.
- Do not fold Results and Discussion into an overview. Preserve the method description, every numerical claim, and quantitative conclusions.
- Domain terminology: see `references/terminology.md`. Translation precision checklist: `references/translation-policy.md`.

### Gate 3: Inline layout & accessible reading flow (PDF and DOCX)
- Layout structure shared across **both output formats**: Chinese title; exact English title immediately underneath; verified bibliographic note; abstract; keywords; section headings; full translated paragraphs; nearby figures/equations/tables; appendices; references.
- **No uneven Chinese character spacing**: left-align academic body text; turn off forced justification/distributed alignment, artificial character-width expansion, manually inserted extra spaces, and letter-spacing hacks. Tune natural line breaks against user-approved sample #1.
- **True scientific subscript/superscript**: preserve the source's indexes with semantic math runs or native Word math/run formatting; do NOT print `W_I` as the final mathematical symbol. Validate examples `W_I`, `W_R`, `W_T`, `CO₂`, `kg/m³`, `s⁻¹`. Use original formula crops if complex re-typesetting cannot be verified.
- **Sentence-by-sentence source alignment**: preserve source argument order and paragraph granularity; maintain private `source_page + source_paragraph_id + source_quote → Chinese paragraph` traces for side-by-side comparison; do not falsely claim a fully automated semantic QA check. Natural re-pagination across languages is allowed; do not sacrifice legibility solely to mimic page numbers.
- Follow figure and equation placement rules in `references/layout-spec.md`. Figure image may retain original English labels while Chinese captions explain its meaning; do not pretend all text inside a raster image was translated.
- Match original figure aspect ratio, do not stretch axes or crop legends/panel letters/colorbar/scalebar. Caption must be on same/adjacent page where possible.
- Start a figure or table on a new page only when needed, not as a deliberate appendix trick.
- If an original graph/table is blurry when cropped, re-render at higher resolution; review source page as needed.

### Gate 4: Technical QA (required independently for each requested format)
- Validate item inventory parity: all primary/appendix figures, tables, equations and references accounted for. Check body coverage by source section and appendix.
- Re-render all requested output pages to images: for PDF, rasterize the final PDF; for DOCX, **render actual Word pages** with a Word/LibreOffice-compatible renderer (e.g. `render_docx.py`) and inspect every page. Never infer DOCX layout from the PDF result alone.
- If both are requested, build PDF and DOCX from a **single approved structured translation**; audit both for content/figure count parity and independently review their pagination. Word text should be editable; source plots may be embedded images, complex source formulas may be high-quality images as transparently documented. For complex PDFs, inspect **every** output page or a contact sheet plus all questionable pages.
- Reject outputs containing white/black squares, missing Chinese glyphs, overlapping layers, clipped math, blank boxes, stretched graphs, swapped bilingual order, or whole-source figures only at the end.
- Check terminology consistency and compare all dense numeric tables against the source. Distinguish target density vs measured density, incident pressure vs specimen stress, energy absorption vs absorption efficiency, etc.
- Generate a QA report (can remain internal). Do not claim exact word-for-word validation without doing it.
- Follow `references/quality-checklist.md` item-by-item before final approval.
- If any check fails, repair and repeat the PDF and/or DOCX render inspection before publishing.

### Gate 5: Release
- Output `N.<Chinese-paper-title>_中文版.pdf`, `.docx`, or both as requested. Keep the **specific translation destination and its file-type rules**; source English PDF remains separately. Do not inject Word into a user's PDF-only Library folder.
- Report actual pages for every delivered format, confirmed figure/table/equation inventory, unresolved contradictions and what actually passed QA. Never claim a single click guarantees correct translations.
- For many papers, deliver the first one and confirm user-visible readability before proceeding sequentially.

## Companion tools (optional)
The public repository includes `paper2zh inspect`, `paper2zh build --format pdf|docx|both`, `paper2zh audit` and `paper2zh align` to support PDF inspection, rendering from a reviewed JSON manuscript, and structural QA. **These tools do not automatically translate or reliably infer all diagram/equation crop rectangles. Word output is a true DOCX with editable paragraphs, not just rasterized PDF pages.** The AI agent or researcher remains responsible for sourcing accurate Chinese prose and correctly anchored crop coordinates. See the repository README and `references/tooling.md` for the manifest contract.

## When to stop and ask
- Manuscript text not accessible or missing source pages; mixed documents whose reading order cannot be verified; complex graphic whose essential labels are unreadable; uncertain formula structure; quality checks fail.
- If user provides a template they prefer, prefer it over generic default styling without compromising accuracy.


## Output preference examples
- User: “我只想看PDF，存到SHPB中文译文PDF文件夹。” → **PDF only** in specified folder. No Word output or extra copies.
- User: “可编辑Word文件” → **DOCX**, render + review Word pages before delivery.
- User: “PDF和Word都要” → **Both** from one verified manuscript, independently QA both and deliver both.
