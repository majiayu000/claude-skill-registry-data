---
name: skill-authoring-template
description: 新しいSkillを作るときの必須セクション（入力/出力/禁止/検証/根拠）テンプレ。skill-builder が新規Skillを生成するときに参照する。
---

# Skill Authoring Template

## YAML frontmatter (MUST)
SKILL.md は必ず YAML フロントマターから始める。

最低限:
- name
- description（「何をする」＋「いつ使う」+「キーワード」）

**禁止**: `description: |` のようなマルチライン構文は使用しないこと。

## Required sections (MUST)
- Inputs
- Outputs
- Forbidden
- Verification
- Evidence (which files/dirs informed this)

## Naming (MUST)
- 小文字/数字/ハイフンのみ、64文字以内
- 予約語や紛らわしい語を避ける（例: anthropic / claude を含めない）
- 推奨: **一貫した命名パターン**（公式は gerund: 動名詞形 “verb-ing” を推奨）

例（gerund）:
- `testing-code`
- `writing-documentation`
- `managing-migrations`

## Guidance
- 手順は「誰がやっても同じ」粒度で具体的に
- 検証コマンドは repo に実在するものだけを書く
