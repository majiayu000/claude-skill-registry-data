---
name: wechat-article-md-local
description: |
  Download and read a single WeChat Official Account article (微信公众号文章) from a public mp.weixin.qq.com link, save it in the workspace as local Markdown with all images downloaded locally, falling back to HTML when Markdown conversion is impossible. ALWAYS use this skill first whenever the user sends a single WeChat article link — even without asking to download it — and especially before summarizing, extracting, analyzing, quoting, rewriting or translating that article. Triggers: mp.weixin.qq.com link, 下载公众号文章, 公众号文章转 Markdown, 保存这篇公众号, wechat article to markdown.

---

# WeChat article → local Markdown

Use this skill for **single article** WeChat Official Account links.

## Default path: use the bundled script first

For normal use, do **not** manually shuttle the full article HTML through the browser tool.
微信公众号正文经常很长，`#js_content.innerHTML` 可能超过工具返回长度，导致提取结果被截断。

优先直接运行这个脚本：

```bash
SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
bash "${SKILL_DIR}/scripts/download_wechat_article.sh" '<MP_URL>' '<OUTPUT_DIR>'
```

这个脚本会自动：
- 用 Playwright 打开文章页
- 提取元数据和完整 `#js_content` HTML
- 调用 `save_wechat_article.py`
- 下载图片到本地
- 生成 Markdown 和 HTML fallback

## What to do

1. Validate the URL is a single article link on `mp.weixin.qq.com`.
2. Run the bundled shell script above.
3. Parse the JSON result printed by the script.
4. Return the saved file paths.

## Expected output from the script

脚本成功时会输出 JSON，包含至少这些字段：
- `title`
- `article_dir`
- `markdown_path`
- `html_path`
- `images_dir`
- `image_count`
- `markdown_ok`

## Fallback path

Only if the bundled script fails, fall back to the manual two-step flow:

1. Use the **browser tool** to open the article page.
2. Extract article metadata and the full `#js_content` HTML from the rendered page.
3. Save the extracted payload to a temporary JSON file.
4. Run `scripts/save_wechat_article.py` manually.

## Manual browser extraction

Use browser evaluate on the opened article page and extract at least:

```js
() => {
  const q = s => document.querySelector(s);
  const text = s => q(s)?.textContent?.trim() || '';
  const html = q('#js_content')?.innerHTML || '';
  return {
    url: location.href,
    title: text('#activity-name') || text('#js_name') || document.title,
    account: text('#js_name'),
    author: text('#js_author_name') || text('#js_author'),
    publish_time: text('#publish_time'),
    description: document.querySelector('meta[name="description"]')?.content || '',
    cover: document.querySelector('meta[property="og:image"]')?.content || '',
    html
  };
}
```

If `html` is empty, stop and report the page could not be extracted.

## Manual converter script

Run:

```bash
SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
source "${SKILL_DIR}/scripts/../.venv-wechat-skill/bin/activate" 2>/dev/null || true
python "${SKILL_DIR}/scripts/save_wechat_article.py" \
  --input /tmp/wechat_article_input.json \
  --output-dir '<OUTPUT_DIR>'
```

## Success response

Report:
- article title
- markdown path
- images directory
- fallback HTML path
- image count if available

## Notes

- This skill is intentionally for **single article links only**.
- Images should always be localized.
- Prefer the bundled shell script over manual browser extraction.
- If Markdown conversion has issues, still keep the cleaned HTML fallback.
- Gotcha: do not rely on a single browser-tool response to carry very large HTML blobs when a local script can write them directly to disk.
