---
name: obsidian-writer
description: Write structured notes into the local Obsidian vault at /Users/tangchunwu/Documents/Obsidian Vault. Use when the user asks to save content to Obsidian, archive a note into the vault, create a review/summary/todo note, or organize an existing draft into Obsidian folders with frontmatter.
---

# Obsidian Writer

## Overview

Use this skill when the user wants content written into the local Obsidian vault instead of just shown in chat.

Default vault:

- `/Users/tangchunwu/Documents/Obsidian Vault`

Default behavior:

1. Choose a reasonable folder from the request
2. Create the folder if missing
3. Update an existing note when the target already exists
4. Otherwise create a new Markdown note with frontmatter
5. Keep filenames short and readable
6. When the user asks, link the note into today's Daily Note instead of only storing it in isolation

## Quick Start

Common user intents this skill should handle:

- “写进我的 Obsidian”
- “存成 Obsidian 笔记”
- “归档到我的知识库”
- “放到复盘目录”
- “整理成可在 Obsidian 里继续编辑的文档”
- “链接到今天的 Daily Note”
- “挂到今日日记里”

## Workflow

### 1. Decide target folder

Use the user's explicit folder if given.

Otherwise, pick the closest folder by note type:

- Review / retrospective -> `复盘/`
- Product / strategy -> `产品/`
- Tech fix / debugging -> `技术/`
- Daily notes / loose notes -> `Inbox/`
- Tasks / actions -> `待办/`

If none exists, create it.

Use the bundled folder selector when possible:

- [`scripts/pick_folder.py`](scripts/pick_folder.py)

`pick_folder.py` also recognizes Daily Note / 日记类内容 and routes them to `Daily/`.

### 1.1 Update existing notes when appropriate

Do not always create a new file.

Prefer updating when one of these is true:

1. The user explicitly says “更新这篇笔记” or “覆盖原来的”
2. The target filename already exists
3. The title clearly matches an existing note in the chosen folder

Use:

- [`scripts/upsert_note.py`](scripts/upsert_note.py)

This script:

- creates missing folders
- writes a new file if it does not exist
- updates an existing note by filename match
- also updates an existing note by fuzzy title match
- supports append mode when the user wants to keep the old note and add more content
- normalizes unsafe filenames and auto-adds `.md`
- safely quotes frontmatter values so titles like `技术: 记录` do not break YAML
- accepts `--folder auto` to infer the folder without a separate routing step

Recommended modes:

- `auto`
  - default
  - create if missing
  - update if filename or title matches
- `replace`
  - force overwrite target note
- `append`
  - keep the existing note and append the new content after a separator

### 1.2 Link into today's Daily Note when requested

If the user asks to "链接进今天的 Daily Note", "挂到今日日记", or anything equivalent, use:

- [`scripts/link_daily_note.py`](scripts/link_daily_note.py)

This script:

- finds an existing Daily Note folder from common names (`Daily`, `Daily Notes`, `日记`, `日志`)
- creates `Daily/` if none exists
- creates today's daily note if missing
- inserts a wikilink under a heading such as `## 今天的记录`
- avoids duplicate links when run twice

### 2. Create a clean note

Prefer a note with frontmatter:

```yaml
---
title: 标题
date: YYYY-MM-DD
type: note
status: done
tags:
  - 标签1
  - 标签2
---
```

Recommended `type` values:

- `note`
- `review`
- `summary`
- `plan`
- `todo`

Recommended `status` values:

- `draft`
- `done`
- `archived`

### 3. Keep naming stable

Filename rules:

- Prefer Chinese titles if the user works in Chinese
- Avoid overlong filenames
- Use a date prefix only when it adds value

Good examples:

- `复盘-图片浏览任务与发版平滑性的产品思考.md`
- `复盘-2026-04-09-个人博客与资源库系统.md`
- `技术-博客保存失败排查.md`

### 4. Write through the bundled script

Use:

- [`scripts/upsert_note.py`](scripts/upsert_note.py)
- [`scripts/pick_folder.py`](scripts/pick_folder.py)
- [`scripts/link_daily_note.py`](scripts/link_daily_note.py) when the user requests a Daily Note backlink

This keeps note writing deterministic and avoids repeating filesystem glue.

## Frontmatter Guidance

Use the smallest useful frontmatter set.

Do not invent metadata unless it helps retrieval.

Good default:

```yaml
---
title: ...
date: 2026-04-10
type: review
status: done
tags:
  - 复盘
  - 产品
---
```

## Writing Style

- Write in Simplified Chinese unless the user requests otherwise
- Prefer direct, editable Markdown
- Use short headings and clean lists
- Avoid decorative fluff

## References

See:

- [`references/vault.md`](references/vault.md)

## Output Expectation

When using this skill, actually create the note in the vault and report:

1. Final file path
2. Folder used
3. Write mode used (`auto` / `replace` / `append`)
4. Whether the note was created, updated, or appended
5. Whether frontmatter was added
6. If Daily Note linking was requested, report the Daily Note path and whether the link was inserted or already existed
