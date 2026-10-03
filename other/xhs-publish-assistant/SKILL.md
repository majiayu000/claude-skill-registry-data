---
name: xhs-publish-assistant
description: Prepare copy-ready Xiaohongshu/Rednote publish materials from a local XHS article package. Use when the user asks for "输出发布格式", "小红书发布格式", "准备发布", "二次编辑发布格式", or needs title/body/tags/output image directory/checks without browser automation or clicking publish.
---

# XHS Publish Assistant

## Purpose

Prepare the final copy-paste bundle for a Xiaohongshu note. This skill is a publishing formatter, not a publishing robot.

Use it after the XHS role has already produced or approved the title, body, tags, and card images. Do not use this skill to choose topics, rewrite the note, generate cards, scrape comments, or register post-publish metrics.

## Hard Boundaries

- Do not open or automate Xiaohongshu pages.
- Do not click publish, save, update, or any final platform button.
- If the user asks for browser automation, login checks, creator-center fill, automatic publishing blockers, content-data export, or final posting, route to `$xhs-automation-publisher` and keep the same explicit final-publish approval gate.
- Do not generate a publish HTML panel.
- Do not list every image path unless the user explicitly asks; output only the `output\` directory.
- Do not modify published article source files. For a re-edit, use or create a `reedit-YYYY-MM-DD\` package and keep the original as history.
- Do not invent missing title/body/tags. If extraction is uncertain, say exactly what is missing and ask the user or read the source file manually.

## Workflow

1. Resolve the target article directory.
   - Normal package: `content/xhs/<date>/<article>/`
   - Re-edit package: `content/xhs/<date>/<article>/reedit-YYYY-MM-DD/`
   - If the user only says "这篇", use the latest active XHS path from the conversation. If ambiguous, ask for the path.
2. Read the relevant source:
   - Prefer `reedit-note.md` inside a re-edit directory.
   - Otherwise read `content-pack.md`.
3. Before producing the final publish format, ensure title/body/caption copy has passed `$humanizer-zh` in the current role workflow. If it has not, load `$humanizer-zh` and polish only the public copy without changing facts, dates, prices, claims, account identity, or image order.
   - If the note includes narrative prose, story fragments, or dialogue, use `$story-deslop` only for those narrative passages after facts are locked.
   - Do not use either skill to invent missing copy. If source copy is incomplete, stop and report what is missing.
4. Run the helper when available:

```powershell
$skillRoot = if ($env:CODEX_HOME) { Join-Path $env:CODEX_HOME "skills\xhs-publish-assistant" } else { Join-Path $HOME ".codex\skills\xhs-publish-assistant" }
node (Join-Path $skillRoot "scripts\build_publish_format.cjs") "<article-or-reedit-directory>"
```

5. Review the helper output against the source file. Fix obvious extraction mistakes manually before responding.
6. Return only the final publish format. Keep it easy to copy.

## Required Output Format

Use this exact section order:

**标题**
```text
<title>
```

**正文**
```text
<body>
```

**标签**
```text
<hashtags, one line, <= 10 tags>
```

**配图目录**
```text
<absolute output directory ending with backslash>
```

**发布前检查**
```text
账号：<account or 待确认>
图片数量：<N>
图片尺寸：<全部 1080x1440 | mixed details | 未检查>
标题长度：<N> / 20
标签数量：<N> / 10
文案去 AI 味：<已运行 humanizer-zh | 已运行 humanizer-zh + story-deslop | 待确认>
标题覆盖：<short judgment>
封面职责：<short judgment>
图片顺序：按 output 目录内 xhs-*.png 文件名顺序上传
状态：<可发布 | 需补齐>
```

For a re-edit, append one extra section:

**二次编辑记录**
```text
这是已发布笔记二次编辑。
编辑前基线：<views/comments/likes/favorites/shares if known>
编辑后请告诉我实际保存时间，我会登记为 reedit_phase。
```

## Checks

- Tags must be 10 or fewer. If more than 10, trim or ask which to keep.
- Publish title must be 20 characters or fewer. Prefer 12-18 characters when possible. Count each Chinese character, Latin letter, number, punctuation mark, and visible space as one character. If the title is over 20, shorten it or mark the package as `需补齐`.
- The image directory should be an absolute path to an `output\` folder, not individual images.
- Prefer `xhs-*.png` ordering for upload.
- Check PNG dimensions when images exist. Expected card size is `1080x1440`.
- Account must be explicit when possible. In this repo, read `content/xhs/accounts.md` if the package does not state the account.
- For published/re-edited notes, mention the phase split so later retros do not mix original and edited performance.

## Relationship To Other XHS Skills

- XHS role decides the content strategy, title direction, body, card copy, and publish recommendation.
- `humanizer-zh` is required before this skill returns a final copy-ready publish bundle.
- `story-deslop` is optional and only for narrative/story/dialogue passages, not normal Xiaohongshu marketing or analysis copy.
- `xhs-visual-director` is the default upstream for new carousel visuals, cover redesigns, and full visual rewrites. It should produce the style judgment, visual master, confirmation image, and final card images before this skill checks the output directory.
- Existing HTML/render workflows or `guizang-social-card-skill` may still be used for legacy packages or small local edits, but the final publish bundle should state whether the visual direction was confirmed.
- `cheat-on-content` handles prediction, publish registration, retro, and rubric calibration after the user publishes.
- `xhs-comment-research` reads and analyzes comments; this skill does not scrape comments.
- `xhs-automation-publisher` handles authorized browser/CDP automation. It defaults to preview/fill and requires explicit user approval before final posting or interaction commands.
