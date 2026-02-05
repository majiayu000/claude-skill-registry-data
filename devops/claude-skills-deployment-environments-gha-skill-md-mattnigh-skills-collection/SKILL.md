---
name: .claude/skills/deployment-environments-gha/SKILL.md
description: |
  GitHub Actions の environments を設計し、承認フローと保護ルールを安全に運用するスキル。
  
  📖 参照書籍:
  - 『The Pragmatic Programmer』（Andrew Hunt, David Thomas）: 実践的改善
  
  📚 リソース参照:
  - `resources/Level1_basics.md`: レベル1の基礎ガイド
  - `resources/Level2_intermediate.md`: レベル2の実務ガイド
  - `resources/Level3_advanced.md`: レベル3の応用ガイド
  - `resources/Level4_expert.md`: レベル4の専門ガイド
  - `resources/approval-workflows.md`: 承認者設定、待機タイマー、デプロイゲートの実装パターン
  - `resources/environment-config.md`: 環境設定、保護ルール、シークレット管理の詳細ガイド
  - `resources/legacy-skill.md`: 旧SKILL.mdの全文
  - `scripts/check-environment.mjs`: 環境ステータスと設定を確認する診断スクリプト
  - `scripts/log_usage.mjs`: 使用記録・自動評価スクリプト
  - `scripts/validate-skill.mjs`: スキル構造検証スクリプト
  - `templates/deployment-workflow.yaml`: 複数環境への段階的デプロイの実装サンプル
  - `resources/requirements-index.md`: 要求仕様の索引（docs/00-requirements と同期）
  
  Use proactively when implementing .claude/skills/deployment-environments-gha/SKILL.md patterns or solving related problems.
version: 1.0.0
level: 1
last_updated: 2025-12-24
references:
  - book: "The Pragmatic Programmer"
    author: "Andrew Hunt, David Thomas"
    concepts:
      - "実践的改善"
      - "品質維持"
---

# Deployment Environments Skill (GitHub Actions)

## 概要

GitHub Actions の environments を設計し、承認フローと保護ルールを安全に運用するスキル。

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
- resources/Level1_basics.md を参照し、適用範囲を明確にする
- resources/Level2_intermediate.md を参照し、実務手順を整理する

### 避けるべきこと
- アンチパターンや注意点を確認せずに進めることを避ける

## コマンドリファレンス

### リソース読み取り
```bash
cat .claude/skills/deployment-environments-gha/resources/Level1_basics.md
cat .claude/skills/deployment-environments-gha/resources/Level2_intermediate.md
cat .claude/skills/deployment-environments-gha/resources/Level3_advanced.md
cat .claude/skills/deployment-environments-gha/resources/Level4_expert.md
cat .claude/skills/deployment-environments-gha/resources/approval-workflows.md
cat .claude/skills/deployment-environments-gha/resources/environment-config.md
cat .claude/skills/deployment-environments-gha/resources/legacy-skill.md
```

### スクリプト実行
```bash
node .claude/skills/deployment-environments-gha/scripts/check-environment.mjs --help
node .claude/skills/deployment-environments-gha/scripts/log_usage.mjs --help
node .claude/skills/deployment-environments-gha/scripts/validate-skill.mjs --help
```

### テンプレート参照
```bash
cat .claude/skills/deployment-environments-gha/templates/deployment-workflow.yaml
```

## 変更履歴

| Version | Date | Changes |
| --- | --- | --- |
| 1.0.0 | 2025-12-24 | Spec alignment and required artifacts added |
