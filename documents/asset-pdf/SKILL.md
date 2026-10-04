---
name: "Asset: PDF"
description: "Rasterise pages of a PDF (tabletop game documents, print pieces) with pdftoppm and frame chosen pages with the project's theme into preview cards"
when_to_use: "When a project ships a PDF and its README, itch page or social card needs page previews; when the user mentions a PDF, rulebook, character sheet, print-and-play or page preview."
model: sonnet
effort: medium
metadata:
  glyph: ᛊ
  family: asset
disable-model-invocation: true
allowed-tools: ["Read", "Write", "Glob", "Grep", "Bash"]
argument-hint: "<file.pdf> [pages e.g. 1, 3-5, cover] [dpi] [no frame] [theme family]"
---

# PDF page previews

Load `asset-conventions` first; pdftoppm flags in `~/.claude/library/references/asset-tools.md`.

```xml
<asset-pdf>
	<arguments>
		A PDF path (if omitted, list PDFs under `docs/`, `dist/`, `export/`, `print/` and ask which). Pages as numbers, ranges or "cover" (page 1) and "spread" (two consecutive pages composed side by side); default: cover plus the first two interior pages. A bare number 72–600 is DPI (default 200; 300 for print-quality). "no frame" skips framing. A theme family selects the frame block.
	</arguments>
	<steps>
		<step num="1">`pdfinfo &lt;file&gt;` for page count and page size; refuse page numbers out of range with the count shown. Slug the document name for `docs/assets/pdf/&lt;doc-slug&gt;/`.</step>
		<step num="2">Rasterise the requested pages only: `pdftoppm -png -r &lt;dpi&gt; -f N -l N &lt;file&gt; docs/assets/pdf/&lt;doc-slug&gt;/page` (one call per page or range; output names keep the original page numbers, zero-padded).</step>
		<step num="3">Unless "no frame": resolve the `frame` theme and run `bun ~/.claude/library/scripts/asset/frame.ts &lt;page&gt;.png docs/assets/pdf/&lt;doc-slug&gt;/framed/&lt;page&gt;.png --project . --no-chrome --max-width 1200` per page (a page is not a browser; chrome is always off). For "spread", compose the two pages side by side with a 24px gap using sharp before framing.</step>
		<step num="4">Quality gate: Read each framed PNG; check the page isn't rendered blank (fonts missing → try `-r` higher or report), text is legible at the output size, bleed marks aren't showing (crop with `-x -y -W -H` if the PDF has them). Report per the conventions; offer `asset-card` with the cover as hero.</step>
	</steps>
	<rules>
		<rule>Never rasterise the whole document by default; page previews are a handful of pages, chosen.</rule>
		<rule>Rasterised pages of a paid product are previews: keep to the cover and non-spoiler interior pages unless told otherwise.</rule>
	</rules>
</asset-pdf>
```
