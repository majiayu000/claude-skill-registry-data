---
name: wechat-theme-extractor
description: Use when extracting visual styles from a WeChat article and generating a markdown-wechat-converter theme.
---

# WeChat Theme Extractor

## Overview

Extract layout and style signals from a WeChat Official Account article, then generate a reusable theme for `markdown-wechat-converter`. The workflow derives typography, colors, spacing, and block styles from the article, writes the generated theme into `markdown-to-wechat.html`, and supports previewing the result.

## When to Use

Use this skill when the user:
- Provides a `mp.weixin.qq.com` article URL
- Wants to extract typography, color, spacing, and block styles from a WeChat article
- Wants a new theme generated for `markdown-wechat-converter`
- Wants the theme written into `markdown-to-wechat.html` and previewed

## Do not use

Do not use this skill when:
- The URL is not a WeChat Official Account article
- The user only wants article text extraction without theme analysis
- The target project does not contain `markdown-wechat-converter` or `markdown-to-wechat.html`

## Instructions

1. Run `scripts/extract.py` to fetch the article HTML and extract the title and `js_content`.
2. Read `.extracted_content.html` and analyze style traits directly from the HTML.
3. Generate a theme object compatible with `markdown-wechat-converter`.
4. Locate `markdown-to-wechat.html` in the current workspace and inject the new theme without breaking existing theme definitions.
5. Re-open the file and verify the theme entry was actually written.
6. If verification succeeds, open `markdown-to-wechat.html` in the browser for preview.

## Workflow

```text
User provides URL
  -> run extractor script
  -> produce .extracted_content.html
  -> analyze styles
  -> generate theme config
  -> write into markdown-to-wechat.html
  -> verify write result
  -> open preview
```

## Run the script

```bash
python3 scripts/extract.py "https://mp.weixin.qq.com/s/xxxxx"
```

## Script responsibilities

The Python script only:
- Fetches article HTML
- Extracts the article title
- Extracts the `js_content` body fragment
- Saves the result to `.extracted_content.html`

The AI handles:
- Style analysis
- Theme generation
- Config injection
- Post-write verification
- Preview opening

## Injection rules for `markdown-to-wechat.html`

When updating `markdown-to-wechat.html`, follow these rules:

1. Find the real theme source first.
   - Search for theme-related objects, arrays, maps, or `const` assignments before editing.
   - Do not assume a fixed variable name unless it exists in the file.

2. Preserve the existing structure.
   - Match the file's current object style, quote style, indentation, and trailing comma convention.
   - Do not reformat unrelated sections.

3. Add, do not overwrite blindly.
   - If the new theme name does not exist, append a new entry in the existing theme collection.
   - If the same theme name already exists, update only that entry instead of duplicating it.

4. Keep the change scoped.
   - Only touch the theme definition block and any minimal registration hook required to make the theme selectable.
   - Do not modify renderer logic, event handlers, or unrelated UI code unless the file structure requires a minimal wiring change.

5. Verify after writing.
   - Re-read the edited section and confirm the theme key, title, and core style properties are present.
   - If the theme block cannot be located safely, stop and report that the target file structure needs manual confirmation.

## Example theme snippet

Generate a theme object that matches the target file's existing structure. Use this as a minimal reference shape:

```js
{
  id: "wechat-clean-blue",
  name: "WeChat Clean Blue",
  styles: {
    body: {
      fontFamily: "\"PingFang SC\", \"Helvetica Neue\", sans-serif",
      fontSize: "16px",
      color: "#2b2b2b",
      lineHeight: "1.75",
      backgroundColor: "#ffffff"
    },
    h1: {
      fontSize: "24px",
      fontWeight: "700",
      textAlign: "center",
      color: "#1f3a5f"
    },
    h2: {
      fontSize: "20px",
      fontWeight: "700",
      color: "#1f3a5f",
      borderBottom: "2px solid #9ec1ff"
    },
    blockquote: {
      color: "#4a5568",
      backgroundColor: "#f7fbff",
      borderLeft: "4px solid #7fb3ff",
      padding: "12px 16px"
    }
  }
}
```

When writing:
- Match the real field names used in `markdown-to-wechat.html`
- Convert this shape if the target file uses arrays, maps, or nested registration
- Include at minimum the theme key, display name, and core typography styles

## Output file

- `scripts/.extracted_content.html`: extracted article body HTML with title and source URL comments at the top

## Validation checklist

- The article HTML was fetched successfully
- `.extracted_content.html` exists and is not empty
- The title and `js_content` were extracted
- The new theme entry exists in `markdown-to-wechat.html`
- The preview page opens successfully
