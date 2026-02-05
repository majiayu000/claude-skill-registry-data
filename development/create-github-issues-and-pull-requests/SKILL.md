---
name: Create GitHub Issues and Pull Requests
description: Create GitHub Issues and Pull Requests in this repository.
allowed-tools: Bash(gh issue:*), Bash(gh pr:*)
---

To create GitHub Issues and Pull Requests in this repository, follow these guidelines.

1. Check the existing Issues and/or Pull Requests to avoid duplicates, gather context, and follow existing styles and formats.
2. Collect necessary information about the Issue or Pull Request you want to create or manage.
3. Use the GitHub CLI commands to create or manage Issues and Pull Requests. Make sure that set `AI Created` label.

Rules:

- Make Issue or Pull Request title using the conventional commit message style in Japanese. For example: `feat(kintone): QRコードを読み取る機能を実装` or `fix(chrome): 自動入力の問題を修正 #123`.
- For Issues and Pull Requests, use a concise title and a detailed description.
- Use the label named `AI Created` for Issues and Pull Requests created by AI assistants. And set another proper labels if necessary.
- Write Issues and Pull Requests descriptions in Japanese, but you can use English for technical terms.
- Write `(Written by Claude Code)` or `(Written by GitHub Copilot)` in the bottom of the Issue or Pull Request description to indicate AI assistance.
