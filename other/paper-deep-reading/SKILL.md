---
name: paper-deep-reading
description: Create beginner-friendly deep-reading notes for journal and research paper PDFs. Use when Codex needs to learn a paper, translate it paragraph by paragraph, build an Obsidian knowledge-base note, extract and place figures, write detailed figure notes, explain concepts for beginners, maintain a question log, or export the note to PDF. Also use for Chinese requests such as 学习文献, 精读论文, 逐段翻译, 图注解释, 问题荟萃, and Obsidian 笔记.
---

# Paper Deep Reading

## Purpose

Turn a journal paper into a polished learning artifact: one main Obsidian Markdown note with paragraph-level translation, placed figures, detailed figure notes, beginner explanations, glossary support, a question log, and optional PDF export.

Use the PDF skill or an equivalent render-and-inspect workflow whenever the source is a PDF. For two-column journal articles, rendered pages are the source of truth for reading order and figure placement.

## Default Workflow

1. Inspect the source PDF: title, authors, sections, page count, figures, captions, tables, references to supplements, and any copyright-sensitive constraints.
2. Create a vault-style output folder with `assets/figures/`, `exports/`, and one main Markdown note unless the user asks for multiple notes.
3. Translate and explain paragraph by paragraph. Number natural paragraphs as `P01`, `P02`, etc.; correct OCR or extraction order against page renders.
4. Insert each figure near the paragraph that first uses it. Store images under `assets/figures/` with stable descriptive names.
5. For every main figure, write a figure note that explains what type of figure it is, what each panel does, what claim it supports, why it matters, and why the authors included it.
6. Add beginner support at first use of key concepts, methods, axes, formulas, materials, and mechanisms. Mark claim boundaries: measured, calculated, inferred, or proposed.
7. Maintain a question log for knowledge questions. Merge repeated questions into the closest existing entry instead of duplicating long explanations.
8. Verify Markdown links, figure paths, section coverage, and whether the output is readable in Obsidian.
9. Export to PDF only when requested. Render the note, inspect representative pages visually, and place final PDFs in `exports/`.

## Required References

Read only the reference files needed for the user's request:

- `references/reading-workflow.md`: full paper-to-note workflow and quality gates.
- `references/figure-note-guide.md`: how to crop, place, and explain figures.
- `references/beginner-explanation-guide.md`: how to explain a difficult field to a novice without oversimplifying.
- `references/obsidian-note-style.md`: note structure, callouts, links, and CSS expectations.
- `references/question-log-guide.md`: how to maintain the learning question log and merge repeated concepts.

## Bundled Resources

- `assets/note-template.md`: starting structure for the main paper note.
- `assets/question-log-template.md`: structure for the separate question log.
- `assets/figure-note-template.md`: reusable figure-note block.
- `assets/obsidian-css-snippet.css`: optional Obsidian CSS for readable callouts and figures.
- `scripts/validate_note_structure.py`: lightweight validation for headings, images, callouts, and repeated question IDs.
- `scripts/export_obsidian_note_pdf.js`: Markdown/Obsidian image rendering to PDF through Playwright.
- `scripts/extract_pdf_assets.py`: optional PyMuPDF helper to render pages and extract embedded images.

## Output Standards

- Prefer one substantial Markdown note over many small files.
- Keep images close to the text that explains them.
- Write figure notes specific to the paper, not generic captions.
- Explain graph axes before interpreting trends.
- Avoid unsupported claims. Say when a point is an inference from the paper.
- Do not publicly include copyrighted full-text translations in example repositories unless the source license permits it.
- Before finishing, report the note path, figure count, question-log status, and any export path.
