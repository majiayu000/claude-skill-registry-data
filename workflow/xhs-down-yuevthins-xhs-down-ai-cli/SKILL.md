---
name: "xhs-down"
description: "Use when the user wants to download Xiaohongshu note content, including text, original images, and best-quality video, or to batch-download all notes from an author profile using browser automation. Trigger on requests like 下载小红书, 保存笔记, 去水印, 抓取 XHS 图片, 抓取 RED 视频, 批量下载小红书博主, 下载这个作者全部笔记, or build an XHS downloader/scraper. Covers note markdown export, original-image reconstruction, video download, and author-profile collection. For real download requests, run the bundled scripts and return note/profile/output evidence instead of a pure checklist. Do not use for Douyin downloads, TikTok downloads, or pure writing tasks."
---

# XHS Down

Downloader workflow for Xiaohongshu notes and author profiles.

## Trigger hints

- Trigger on: 下载小红书、保存笔记、去水印、抓图、抓视频、批量下载小红书博主、XHS downloader、RED 下载
- Also trigger when the user wants note text plus original images/video, not just screenshots
- Do not trigger on: 抖音下载、纯写作改写、无下载语境的小红书内容创作

## Trigger map

- Strong triggers:
  - "下载这篇小红书笔记"
  - "把这个博主的笔记全抓下来"
  - "去水印保存原图"
  - "抓取 RED 视频和正文"
  - "做一个小红书下载器"
- Soft triggers:
  - User wants note text + media together, not just screenshots
  - User wants an author archive rather than a single saved image
- Hard exclusions:
  - 抖音/Douyin/TikTok 下载
  - 纯写作、纯改写、纯选题

## Overlap routing

- If the user clearly means Douyin, route to `douyin-down`.
- If the user wants to write Xiaohongshu content rather than download existing notes, route to the content-creation workflow instead.

## When to use

- Download one or more Xiaohongshu notes to markdown plus media.
- Remove watermark-bearing image URLs by reconstructing original CDN paths.
- Batch-download all notes from an author profile.
- Build or reuse a Xiaohongshu scraping/download pipeline.

## When not to use

- Douyin download: use `douyin-down`.
- A pure writing or repackaging task with no download requirement.

## Prerequisites

- `requests`
- `agent-browser` for author-profile collection
- A logged-in browser session when cookies or profile scraping are required

## Workflow

0. For profile cover-only downloads, run `scripts/xhs_profile_covers.py` and validate `manifest.json` with `scripts/validate_manifest.py`.
1. For single-note downloads, run `scripts/xhs_download.py` directly with one or more note URLs.
2. Add cookies only when authentication is required or when video access needs a logged-in session.
3. For author-profile collection, use `scripts/xhs_author.py` with `agent-browser --auto-connect`.
4. Prefer share links that include `xsec_token` for profile discovery.
5. Keep output naming explicit when the user is preparing a downstream asset library.

## Output Root

Default output directory:

```text
`./xhs-download` by default, or `XHS_OUTPUT_DIR` / `XHS_DOWNLOAD_DIR` when set
```

The bundled scripts use that directory by default. Temporary overrides are allowed with `-o`, `XHS_DOWNLOAD_DIR`, or `XHS_OUTPUT_DIR`.

## Downie Handoff

Downie 4 is available on this Mac and can be used as a fast downloader once a supported page URL or direct media URL is known:

```bash
scripts/downie_handoff.py "https://example.com/video-page"
```

Use Downie for handoff/fallback downloading, especially for video pages Downie already supports or direct media URLs. Keep `xhs_download.py` as the source for XHS metadata, markdown, original image reconstruction, and cases needing cookies or XHS-specific parsing. Do not claim Downie can recover App-only hidden URLs; it still needs a real URL to process.

## Bundled files

- `scripts/xhs_download.py`
- `scripts/xhs_author.py`
- `scripts/downie_handoff.py`
- `scripts/xhs_profile_covers.py`
- `scripts/validate_manifest.py`
- `references/xhs-patterns.md`

## Operating rules

- Treat the author workflow as browser-automation-first; API signing paths are intentionally not the default.
- Preserve markdown output plus original media whenever possible.
- Keep rate limiting and cookie requirements in mind for large batch runs.

## Execution contract

- If the user gives real Xiaohongshu note URLs or author profile targets and asks for download, you must execute the bundled script path or stop at a clearly stated blocker such as missing cookies/session state. Do not answer with only a checklist.
- If the user asks for workflow explanation only, you may stay advisory, but the first line must say `执行模式：未执行（仅流程建议）`.
- For author-archive collection, prefer the browser-automation path before speculating about API-only shortcuts.

## Evidence contract

- Every final answer must start with one of:
  - `执行模式：实际下载`
  - `执行模式：未执行（仅流程建议）`
- For `执行模式：实际下载`, the answer must also include:
  - `目标对象：单篇笔记/作者主页`
  - `执行命令：...`
  - output directory or exported artifact summary
  - whether cookies or browser session were used
- Do not claim the archive is complete unless you have exported-note or media-count evidence.

## Failure contract

- On bad note URL, missing `xsec_token`, browser session failure, or partial media export, return:
  - failure reason
  - command attempted
  - whether note download or author discovery succeeded
- Never blur single-note success into full-author success.

## Acceptance prompts

- Trigger: `请使用 $xhs-down 下载这篇小红书笔记。`
- Real execution: `请使用 $xhs-down 实际准备一次作者主页批量下载，先给执行命令，再给输出证据。`
- Deep path: `请使用 $xhs-down 先做 author discovery，再做单篇或批量导出，并输出每一步结果。`

## Notes

- `.ruff_cache` from the source skill is intentionally not migrated.
- This Codex version keeps the original download logic but uses a simplified routing contract.
