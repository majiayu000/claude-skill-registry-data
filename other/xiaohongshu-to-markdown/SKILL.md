---
name: xiaohongshu-to-markdown
description: "Xiaohongshu Article to Markdown — Extracts text from Xiaohongshu image-based posts via OCR. Use when the user needs to convert a Xiaohongshu/Little Red Book post into readable Markdown text. The tool downloads all carousel images from a post and uses macOS Vision OCR to extract the text content. Requires a Chromium browser logged into xiaohongshu.com with CDP enabled. macOS only (uses Vision Framework for OCR)."
---

# Xiaohongshu Article to Markdown

Extracts authentication from a Chromium browser via CDP, fetches post data via httpx, downloads carousel images, and OCRs them into a clean Markdown file using macOS Vision Framework.

## Quick Start

```bash
python3 <skill-path>/scripts/xhs_to_markdown.py <xiaohongshu_url> [--output-dir DIR] [--cdp-port PORT]
```

**Arguments:**
- `url` (required): Xiaohongshu post URL (e.g., `https://www.xiaohongshu.com/explore/...`)
- `--output-dir`: Output directory, defaults to current working directory
- `--cdp-port`: CDP debugging port, default 9222

**Output file:** `{title}_{noteId}.md`

## Prerequisites

1. **macOS** (uses Vision Framework for OCR — no Python OCR dependencies needed)
2. **Chromium-based browser** (Chrome / Edge / Brave / Arc) installed and **logged in to xiaohongshu.com**
3. **Python dependencies**: `pip install playwright httpx && playwright install chromium`
4. **Swift** (pre-installed on macOS)

**Launch browser with CDP:**

```bash
# Arc
/Applications/Arc.app/Contents/MacOS/Arc --remote-debugging-port=9222
# Chrome
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222
# Edge
/Applications/Microsoft\ Edge.app/Contents/MacOS/Microsoft\ Edge --remote-debugging-port=9222
# Brave
/Applications/Brave\ Browser.app/Contents/MacOS/Brave\ Browser --remote-debugging-port=9222
```

## Architecture

```
URL → CDP(extract cookies) → httpx(fetch HTML) → parse __INITIAL_STATE__ JSON
→ extract HD image URLs → httpx download images → Swift Vision OCR → Markdown
```

| Step | Method | Notes |
|------|--------|-------|
| Cookie extraction | CDP `ctx.cookies()` | Invisible, no tabs opened |
| Page fetch | httpx GET | With browser cookies for auth |
| Data parsing | `__INITIAL_STATE__` JSON | Embedded in page HTML |
| Image download | httpx concurrent | Strips quality compression suffixes |
| OCR | macOS Vision Framework (Swift) | `.accurate` level, zh-Hans + zh-Hant + en |
| Output | Markdown file | Title + meta + OCR text + description |

## Output Format

```markdown
# {title}

> Author: {author} | {time} | [Original]({url})

{OCR text from image 1}

{OCR text from image 2}

...

---

{post description, if present}
```

## Lessons Learned

| Date | Lesson | Action |
|------|--------|--------|
| | | |
