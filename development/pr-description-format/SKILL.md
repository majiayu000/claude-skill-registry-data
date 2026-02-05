---
name: pr-description-format
description: Provides PR description format and workflow requirements for GitHub pull requests. Use this skill when creating PRs or using 'gh pr create'.
---

# PR Description Format

## Instructions

### Important Notes

- Do not use roleplay; use normal professional tone.
- If "Why" is unclear, ask user before creating PR.
- PR descriptions should be written in Japanese using plain form (だ/である/体言止め style), not polite form (です/ます style).
- Always check if the repository has a PR template first (common locations: `.github/PULL_REQUEST_TEMPLATE.md`, `.github/pull_request_template.md`, `PULL_REQUEST_TEMPLATE.md`, `docs/PULL_REQUEST_TEMPLATE.md`). If a template exists, use that template instead of the format provided below.

### Workflow Requirements

1. **Always start with Draft PR**: `gh pr create --draft`
2. **Switch to open only when requested**: `gh pr ready`
3. **Update description on new commits**: `gh pr edit --body` to reflect current state

## Examples

### Format: What / Why / How

```markdown
## 概要
[変更内容の簡潔な要約]

## 変更の背景
[なぜこの変更が必要だったか]

## 変更詳細
- [具体的な変更内容と実装の詳細]
```
