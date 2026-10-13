---
name: create-wechat-publish-package
description: Format a Chinese article for WeChat Official Account and build a complete, auditable publishing package. Use when converting a DOCX or final manuscript into mobile-friendly inline-styled HTML; ordering article cards; generating title, digest, author and source metadata; producing Markdown and plain-text fallbacks; checking image references and top whitespace; creating a manifest and ZIP; or preparing files for manual import into the WeChat browser editor and draft box.
---

# Create WeChat Publish Package

Turn the final article and ordered images into a publication-ready folder without sending or publishing it. Preserve the author’s analytical logic and only make language changes that are requested or clearly necessary.

## Workflow

1. Identify the latest source document and treat older packages as reference only.
2. Proofread spelling, punctuation, grammar, headings, bold emphasis, numbers, units, dates, and forecast labels.
3. Confirm the narrative sequence and the exact insertion point of every image.
4. Read [package-standard.md](references/package-standard.md) and [wechat-html-style.md](references/wechat-html-style.md).
5. Generate an answer-first title, a concise digest, and two alternative titles. Do not repeat the article title inside the body unless the user requests it.
6. Run [build_publish_package.py](scripts/build_publish_package.py) or adapt it for the document’s structure.
7. Verify that every source image is embedded or copied and referenced exactly once in the HTML and Markdown.
8. Check WeChat compatibility risks before preview: no unitless `line-height`, no horizontally scrolling wide tables, no `min-width`/`overflow-x` layout that can exceed the screen, and no body text with line height smaller than its font size.
9. Open the HTML locally and inspect both desktop and narrow mobile widths. Check the first screen for excess blank space and confirm there is no horizontal overflow.
10. Validate the manifest, ZIP, hashes, image dimensions, and file count.
11. If requested, open the final HTML in the in-app browser. Do not publish or mass-send unless the user explicitly authorizes that separate action.

## Editorial Rules

- Preserve factual meaning and analytical caveats during polishing.
- When the user supplies replacement copy and asks to change text only, preserve existing tags, inline styles, image positions, and block order. Apply only layout changes the user explicitly requests.
- Use institutional, precise Chinese with an engaging narrative line. Avoid sensational wording that overstates the evidence.
- Bring the strongest properly qualified number forward when it helps the lead.
- Bold conclusions, denominators, turning points, and policy mechanisms—not entire paragraphs.
- Keep heading language parallel and answer-oriented.
- Distinguish official forecasts from author assumptions and static scenarios.
- Keep the source vintage visible whenever a balance sheet, policy rule, or monthly series could update.

## HTML Rules

- Use inline styles for all article content because the WeChat editor may remove head-level CSS.
- For a no-whitespace copyable HTML requested by the user, set both preview and article containers to `width:100%;max-width:none;margin:0;padding:0`. Do not add desktop or mobile side padding.
- Set the first body element’s top margin to zero. Do not include a large preview-page top padding that gets copied into WeChat.
- Use explicit pixel line heights rather than unitless ratios because the WeChat editor/plugin checker can misread ratio values as too small. Prefer 16–17 px body text with 30–32 px line height, 21–22 px section headings with about 30–32 px line height, and 13 px source notes with about 23 px line height.
- Do not render comparison tables as wide HTML tables with `min-width`, `overflow-x`, or horizontal scrolling unless the user explicitly requires a true table. For mobile WeChat articles, convert small comparison tables into stacked cards or vertical key-value blocks that stay within `width:100%;max-width:100%;box-sizing:border-box`.
- Use `width:100%;height:auto;display:block` for article cards.
- Keep image paths relative and package the original images separately. Browser copy/paste may not transfer local images; the README must instruct the editor to upload the numbered images manually when needed.
- Do not use scripts, external stylesheets, iframes, data URIs, or unsupported interactive elements.

## Required Outputs

Create this structure unless the user requests otherwise:

```text
<package>/
  01_发布信息.txt
  02_公众号正文_可粘贴.html
  02A_公众号正文_HTML片段.html
  03_公众号正文_带图片.md
  04_公众号正文_纯文本.txt
  05_发布信息.json
  06_数据来源.md
  README_发布说明.md
  manifest.json
  images/
    01_结论短语.png
    02_结论短语.png
  cover/                 # only when requested or supplied
  <latest-source>.docx   # when the source is DOCX
<package>.zip
```

The metadata JSON must include title, author, digest, source URL when available, image order, cover status, source filename, and alternative titles.

## Final QA

- Confirm the body does not duplicate the platform title.
- Confirm no image is present only in the DOCX media folder but absent from the article body.
- Confirm HTML, Markdown, text, metadata, README, and manifest describe the same title and image count.
- Confirm all files use UTF-8 and Chinese characters are not garbled.
- Confirm inline CSS uses pixel `line-height` values, not unitless ratios, percentages, or values smaller than the font size.
- Confirm the rendered mobile preview has `documentElement.scrollWidth <= viewport width` and no visible element protrudes beyond the viewport.
- Confirm the ZIP expands to one package root and contains every manifest entry.
- Report that saving to a draft, publishing, and mass-sending were not performed unless separately requested.