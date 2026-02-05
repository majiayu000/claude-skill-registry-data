---
name: .claude/skills/code-style-guides/SKILL.md
description: |
  業界標準コードスタイルガイドの選択と適用の専門知識。
  Airbnb、Google、Standard等のスタイルガイド適用とカスタマイズを行います。
  
  📖 参照書籍:
  - 『Clean Code』（Robert C. Martin）: 命名と意図の明確化
  
  📚 リソース参照:
  - `resources/Level1_basics.md`: レベル1の基礎ガイド
  - `resources/Level2_intermediate.md`: レベル2の実務ガイド
  - `resources/Level3_advanced.md`: レベル3の応用ガイド
  - `resources/Level4_expert.md`: レベル4の専門ガイド
  - `resources/customization-patterns.md`: スタイルガイドのカスタマイズパターン
  - `resources/legacy-skill.md`: 旧SKILL.mdの全文
  - `resources/migration-strategies.md`: スタイルガイド移行戦略
  - `resources/style-guide-comparison.md`: 主要スタイルガイド(Airbnb、Google、Standard)の比較
  - `scripts/detect-style.mjs`: プロジェクトのコードスタイル自動検出スクリプト
  - `scripts/log_usage.mjs`: 使用記録・自動評価スクリプト
  - `scripts/validate-skill.mjs`: スキル構造検証スクリプト
  - `templates/airbnb-base.json`: Airbnbスタイルベース設定
  - `templates/google.json`: Googleスタイル設定
  - `templates/standard.json`: Standardスタイル設定
  
  Use proactively when handling code style guides tasks.
version: 1.0.0
level: 1
last_updated: 2025-12-24
references:
  - book: "Clean Code"
    author: "Robert C. Martin"
    concepts:
      - "命名と意図の明確化"
      - "小さな関数設計"
---

# Code Style Guides Skill

## 概要

業界標準コードスタイルガイドの選択と適用の専門知識。
Airbnb、Google、Standard等のスタイルガイド適用とカスタマイズを行います。

詳細な手順や背景は `resources/Level1_basics.md` と `resources/Level2_intermediate.md` を参照してください。


## ワークフロー

### Phase 1: 目的と前提の整理

**目的**: タスクの目的と前提条件を明確にする

**アクション**:

1. `resources/Level1_basics.md` と `resources/Level2_intermediate.md` を確認
2. 必要な resources/scripts/templates を特定

### Phase 2: スキル適用

**目的**: スキルの指針に従って具体的な作業を進める

**アクション**:

1. 関連リソースやテンプレートを参照しながら作業を実施
2. 重要な判断点をメモとして残す

### Phase 3: 検証と記録

**目的**: 成果物の検証と実行記録の保存

**アクション**:

1. `scripts/validate-skill.mjs` でスキル構造を確認
2. 成果物が目的に合致するか確認
3. `scripts/log_usage.mjs` を実行して記録を残す


## ベストプラクティス

### すべきこと
- プロジェクトのスタイルガイドを選択する時
- 既存コードパターンに基づいてスタイルを決定する時
- チーム規約とスタイルガイドを整合させる時
- カスタムスタイルルールを設計する時
- スタイルガイド移行を計画する時

### 避けるべきこと
- アンチパターンや注意点を確認せずに進めることを避ける

## コマンドリファレンス

### リソース読み取り
```bash
cat .claude/skills/code-style-guides/resources/Level1_basics.md
cat .claude/skills/code-style-guides/resources/Level2_intermediate.md
cat .claude/skills/code-style-guides/resources/Level3_advanced.md
cat .claude/skills/code-style-guides/resources/Level4_expert.md
cat .claude/skills/code-style-guides/resources/customization-patterns.md
cat .claude/skills/code-style-guides/resources/legacy-skill.md
cat .claude/skills/code-style-guides/resources/migration-strategies.md
cat .claude/skills/code-style-guides/resources/style-guide-comparison.md
```

### スクリプト実行
```bash
node .claude/skills/code-style-guides/scripts/detect-style.mjs --help
node .claude/skills/code-style-guides/scripts/log_usage.mjs --help
node .claude/skills/code-style-guides/scripts/validate-skill.mjs --help
```

### テンプレート参照
```bash
cat .claude/skills/code-style-guides/templates/airbnb-base.json
cat .claude/skills/code-style-guides/templates/google.json
cat .claude/skills/code-style-guides/templates/standard.json
```

## 変更履歴

| Version | Date | Changes |
| --- | --- | --- |
| 1.0.0 | 2025-12-24 | Spec alignment and required artifacts added |
