---
name: skill-maker
description: Anthropic公式ガイド準拠の対話型スキル作成・レビュー支援。Use when user says "create skill", "make skill", "skill review", "スキルを作りたい", "スキルレビュー"。新規作成とdescription品質チェックの2モードで起動。
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Skill Maker

Anthropic公式ガイドに基づき、高品質なスキルを対話的に作成・レビューする。

## Progress Checklist

```
Skill Maker Progress:
- [ ] モード判定（Create / Review）
- [ ] ワークフロー実行
- [ ] バリデーション
- [ ] 出力
```

## Mode Selection

ユーザー入力からモードを判定:

| キーワード | モード |
|-----------|--------|
| create, make, 作りたい, 新規 | Create |
| review, check, レビュー, 品質 | Review |
| 両方検出（create+review） | AskUserQuestion で優先モード確認 |
| 不明 | AskUserQuestion でモード選択 |

## Create Mode: 新規スキル作成

### Step 1/6: Use Case Definition

AskUserQuestion で確認:
- 何を実現するスキルか（目的）
- 誰が使うか（対象ユーザー）
- 2-3個の具体的なユースケース

### Step 2/6: Category Selection

AskUserQuestion でカテゴリ選択:
- Document & Asset Creation（ドキュメント生成）
- Workflow Automation（ワークフロー自動化）
- MCP Enhancement（MCP連携強化）

### Step 3/6: YAML Frontmatter生成

name + description を生成。ユーザーが拒否した場合は再生成（リトライ可）。description基準: [reference.md](reference.md#description-guide)

### Step 4/6: SKILL.md Body作成

ステップ形式のワークフロー + Progressive Disclosure。詳細: [reference.md](reference.md#skill-body-writing-guide)

### Step 5/6: Validation

チェックリスト実行: [reference.md](reference.md#validation-checklist)

### Step 6/6: Output

生成したSKILL.mdを出力。reference.md が必要なら併せて生成。

## Review Mode: 既存スキル品質チェック

### Step 1/4: Target Selection

レビュー対象のSKILL.mdパスをAskUserQuestion で確認。

### Step 2/4: Quality Check

公式基準でチェック:
- description品質（WHAT+WHEN+triggers）: [reference.md](reference.md#description-guide)
- 構造（< 100行、Progressive Disclosure）: [reference.md](reference.md#skill-body-writing-guide)
- セキュリティ（XML禁止、予約名）: [reference.md](reference.md#security-constraints)

### Step 3/4: Issue Report

検出された問題をリスト。severity: critical / important / minor。

### Step 4/4: Fix Suggestions

各問題に対する修正案を提示。ユーザー承認後に適用。

## Reference

詳細: [reference.md](reference.md)
