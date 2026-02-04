---
name: .claude/skills/agile-project-management/SKILL.md
description: |
  スクラム・カンバンの実践知識とアジャイルプロジェクト管理の体系的手法。
  ジェフ・サザーランドのスクラムフレームワークを基盤として、
  イテレーティブ開発とチームの自己組織化を実現します。
  
  📖 参照書籍:
  - 『Agile Estimating and Planning』（Mike Cohn）: 見積もり
  
  📚 リソース参照:
  - `resources/Level1_basics.md`: レベル1の基礎ガイド
  - `resources/Level2_intermediate.md`: レベル2の実務ガイド
  - `resources/Level3_advanced.md`: レベル3の応用ガイド
  - `resources/Level4_expert.md`: レベル4の専門ガイド
  - `resources/legacy-skill.md`: 旧SKILL.mdの全文
  - `scripts/log_usage.mjs`: 使用記録・自動評価スクリプト
  - `scripts/validate-skill.mjs`: スキル構造検証スクリプト
  
  Use proactively when handling agile project management tasks.
version: 1.0.0
level: 1
last_updated: 2025-12-24
references:
  - book: "Agile Estimating and Planning"
    author: "Mike Cohn"
    concepts:
      - "見積もり"
      - "計画"
---

# アジャイルプロジェクト管理スキル

## 概要

スクラム・カンバンの実践知識とアジャイルプロジェクト管理の体系的手法。
ジェフ・サザーランドのスクラムフレームワークを基盤として、
イテレーティブ開発とチームの自己組織化を実現します。

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
- プロジェクト開始時のフレームワーク選択
- スプリント計画とイテレーション管理
- チーム編成と役割定義
- アジャイル原則の導入と教育

### 避けるべきこと
- アンチパターンや注意点を確認せずに進めることを避ける

## コマンドリファレンス

### リソース読み取り
```bash
cat .claude/skills/agile-project-management/resources/Level1_basics.md
cat .claude/skills/agile-project-management/resources/Level2_intermediate.md
cat .claude/skills/agile-project-management/resources/Level3_advanced.md
cat .claude/skills/agile-project-management/resources/Level4_expert.md
cat .claude/skills/agile-project-management/resources/legacy-skill.md
```

### スクリプト実行
```bash
node .claude/skills/agile-project-management/scripts/log_usage.mjs --help
node .claude/skills/agile-project-management/scripts/validate-skill.mjs --help
```

## 変更履歴

| Version | Date | Changes |
| --- | --- | --- |
| 1.0.0 | 2025-12-24 | Spec alignment and required artifacts added |
