---
name: apple-hig-guidelines
description: |
  Apple Human Interface Guidelines（HIG）に基づくUI設計原則を専門とするスキル。

  **Anchors**:
  • Apple Human Interface Guidelines (Official) / 適用: iOS・macOS・watchOS・tvOS UI設計 / 目的: Apple標準UI原則
  • 『Don't Make Me Think』（Steve Krug）/ 適用: ユーザビリティ評価 / 目的: 直感的UI

  **Triggers**: iOS・macOS・watchOS・tvOS アプリのUI設計時、Apple Design System準拠時、クロスプラットフォームApple対応時に使用
version: 1.2.0
level: 1
last_updated: 2025-12-24
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
references:
  - book: "Don't Make Me Think"
    author: "Steve Krug"
    concepts:
      - "ユーザビリティ"
      - "情報設計"
---

# Apple Human Interface Guidelines

## 概要

Apple Human Interface Guidelines（HIG）に基づくUI設計原則を専門とするスキル。

詳細な手順や背景は `references/Level1_basics.md` と `references/Level2_intermediate.md` を参照してください。

## ワークフロー

### Phase 1: 目的と前提の整理

**目的**: タスクの目的と前提条件を明確にする

**アクション**:

1. `references/Level1_basics.md` と `references/Level2_intermediate.md` を確認
2. 必要な references/scripts/templates を特定

**Task**: `agents/analyze-hig-context.md` を参照

### Phase 2: スキル適用

**目的**: スキルの指針に従って具体的な作業を進める

**アクション**:

1. 関連リソースやテンプレートを参照しながら作業を実施
2. 重要な判断点をメモとして残す

**Task**: `agents/design-hig-ui.md` を参照

### Phase 3: 検証と記録

**目的**: 成果物の検証と実行記録の保存

**アクション**:

1. `scripts/validate-skill.mjs` でスキル構造を確認
2. 成果物が目的に合致するか確認
3. `scripts/log_usage.mjs` を実行して記録を残す

**Task**: `agents/validate-hig-ui.md` を参照

## ベストプラクティス

### すべきこと

- iOSネイティブアプリのUI設計時
- Apple Design Systemに準拠したUIを作成する時
- モバイルファーストのUIを設計する時
- クロスプラットフォームApple対応が必要な時

### 避けるべきこと

- アンチパターンや注意点を確認せずに進めることを避ける

## コマンドリファレンス

### リソース読み取り

```bash
cat .claude/skills/apple-hig-guidelines/references/Level1_basics.md
cat .claude/skills/apple-hig-guidelines/references/Level2_intermediate.md
cat .claude/skills/apple-hig-guidelines/references/Level3_advanced.md
cat .claude/skills/apple-hig-guidelines/references/Level4_expert.md
cat .claude/skills/apple-hig-guidelines/references/accessibility-specs.md
cat .claude/skills/apple-hig-guidelines/references/app-icons-specifications.md
cat .claude/skills/apple-hig-guidelines/references/component-states.md
cat .claude/skills/apple-hig-guidelines/references/design-themes.md
cat .claude/skills/apple-hig-guidelines/references/interaction-patterns.md
cat .claude/skills/apple-hig-guidelines/references/launch-screens.md
cat .claude/skills/apple-hig-guidelines/references/layout-grid-system.md
cat .claude/skills/apple-hig-guidelines/references/legacy-skill.md
cat .claude/skills/apple-hig-guidelines/references/notifications.md
cat .claude/skills/apple-hig-guidelines/references/platform-specifics.md
cat .claude/skills/apple-hig-guidelines/references/typography-colors.md
cat .claude/skills/apple-hig-guidelines/references/ui-components.md
cat .claude/skills/apple-hig-guidelines/references/visual-design-specs.md
cat .claude/skills/apple-hig-guidelines/references/widgets-live-activities.md
```

### スクリプト実行

```bash
node .claude/skills/apple-hig-guidelines/scripts/check-hig-compliance.mjs --help
node .claude/skills/apple-hig-guidelines/scripts/log_usage.mjs --help
node .claude/skills/apple-hig-guidelines/scripts/validate-skill.mjs --help
```

### テンプレート参照

```bash
cat .claude/skills/apple-hig-guidelines/assets/hig-design-checklist.md
```

## 変更履歴

| Version | Date       | Changes                                               |
| ------- | ---------- | ----------------------------------------------------- |
| 2.0.0   | 2025-12-31 | agents/3ファイル追加、Phase別Task参照を追加、name修正 |
| 1.2.0   | 2025-12-24 | Spec alignment and required artifacts added           |
