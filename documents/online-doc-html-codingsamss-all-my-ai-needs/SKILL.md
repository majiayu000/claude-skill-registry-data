---
name: online-doc-html
description: Export Markdown files to paste-friendly standalone HTML for online document editors. Use when the user wants to copy local Markdown content into an online document, reduce manual formatting work, preserve tables/code blocks/headings, convert SVG diagrams to PNG, embed images into HTML, or says "在线文档", "粘贴到在线文档", "Markdown 转 HTML", "图片复制不过去", "导出在线文档 HTML".
---

# Online Doc HTML

## Overview

Use this skill to turn local Markdown into standalone HTML that can be opened in a browser, selected, copied, and pasted into online document editors with less formatting cleanup.

The default output is HTML only. Do not generate DOCX unless the user explicitly asks for it.

## Workflow

1. Identify the Markdown files the user wants to sync or copy.
2. Prefer a repo-local export script if one already exists and is clearly maintained for that repo.
3. Otherwise run the bundled script:

```bash
~/.claude/skills/online-doc-html/scripts/export_online_doc_html.sh --out build/online-doc-html <file1.md> <file2.md>
```

4. Open the generated HTML file in a browser, select the article body, copy it, and paste into the online document editor.
5. If images still fail to paste, treat it as an online editor clipboard/upload limitation. The next step is browser automation to insert or upload images, not more HTML tuning.

## Bundled Script

Use `scripts/export_online_doc_html.sh`.

Behavior:

- Converts each Markdown file to standalone HTML via `pandoc`.
- Converts referenced `.svg` images to `.png` with `rsvg-convert` before HTML export.
- Embeds images and CSS into the generated HTML with `pandoc --embed-resources`.
- Writes output to `build/online-doc-html` by default.
- Generates `targets.tsv` with source Markdown and output HTML paths.
- Removes stale DOCX files from the output directory because DOCX is not the default path.

Dependencies:

- Required: `pandoc`.
- Required for SVG diagrams: `rsvg-convert` from `librsvg`.

On macOS:

```bash
brew install pandoc librsvg
```

## Output Guidance

Tell the user:

- Which HTML files were generated.
- Whether SVG references were fully replaced by PNG images.
- Whether any image references could not be resolved.
- That no online document was modified unless browser automation or API update was explicitly requested and confirmed.

## Guardrails

- Do not overwrite or save online documents without explicit user confirmation.
- Do not reverse-engineer private save APIs as the first approach. Prefer paste-friendly HTML first.
- Keep generated artifacts in ignored build/output directories when working inside a repo.
