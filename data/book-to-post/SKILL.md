---
name: book-to-post
description: Search for books using Google Books API (by title or ISBN) and generate a Hugo markdown post with book metadata including cover, description, author, etc. Use when the user provides a book title or ISBN.
allowed-tools: Bash, Read, Write, Glob
---

# Book to Hugo Post (Google Books API)

使用 Google Books API 搜尋書籍，自動抓取書名、作者、封面、簡介等資訊，
並產生一篇 Hugo `content/books/<slug>.md` 文章。

## Runtime

- Python via `uv run`
- Do NOT use system python or pip

## Inputs

- query: 書名或 ISBN（必填）
- --isbn: 將查詢視為 ISBN（可選，預設為書名搜尋）
- --outdir: 輸出目錄（預設 content/books）
- --slug: 手動指定 slug（可選）
- --title: 手動覆蓋文章 title（可選）

## Outputs

- Hugo Markdown 檔案：content/books/<slug>.md
- 包含：書名、作者、ISBN、出版社、出版日期、封面、Google Books 連結、簡介

## Command

ALWAYS execute using:

```bash
# 用書名搜尋
uv run --project .claude/skills/book-to-post .claude/skills/book-to-post/book2post.py "書名"

# 用 ISBN 搜尋
uv run --project .claude/skills/book-to-post .claude/skills/book-to-post/book2post.py "ISBN" --isbn
```

Never use:

- python book2post.py
- pip install
- uv run without --project flag

## Examples

```bash
# 搜尋書名
uv run --project .claude/skills/book-to-post .claude/skills/book-to-post/book2post.py "Effective Java"

# 搜尋 ISBN
uv run --project .claude/skills/book-to-post .claude/skills/book-to-post/book2post.py "9780134685991" --isbn

# 指定輸出目錄
uv run --project .claude/skills/book-to-post .claude/skills/book-to-post/book2post.py "Clean Code" --outdir content/reading
```

## Notes

- Dependencies are resolved via pyproject.toml
- Assume uv is available
- Uses Google Books API (no API key required)
- Returns the first/best match from search results
