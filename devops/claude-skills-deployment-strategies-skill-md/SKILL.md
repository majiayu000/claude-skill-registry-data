---
name: .claude/skills/deployment-strategies/SKILL.md
description: |
  本番環境への安全なデプロイとリスク軽減を専門とするスキル。
  Blue-Green、Canary、Rolling等のデプロイパターンとロールバック戦略を提供します。
  専門分野:
  
  📖 参照書籍:
  - 『The Pragmatic Programmer』（Andrew Hunt, David Thomas）: 実践的改善
  
  📚 リソース参照:
  - `resources/Level1_basics.md`: レベル1の基礎ガイド
  - `resources/Level2_intermediate.md`: レベル2の実務ガイド
  - `resources/Level3_advanced.md`: レベル3の応用ガイド
  - `resources/Level4_expert.md`: レベル4の専門ガイド
  - `resources/deployment-patterns.md`: deployment-patterns のパターン集
  - `resources/health-checks.md`: health-checks の詳細ガイド
  - `resources/legacy-skill.md`: 旧SKILL.mdの全文
  - `resources/railway-deployment.md`: railway-deployment の詳細ガイド
  - `resources/rollback-strategies.md`: rollback-strategies の詳細ガイド
  - `scripts/health-check.mjs`: ヘルスを検証するスクリプト
  - `scripts/log_usage.mjs`: 使用記録・自動評価スクリプト
  - `scripts/validate-skill.mjs`: スキル構造検証スクリプト
  - `templates/deployment-runbook.md`: deployment-runbook のテンプレート
  - `templates/health-endpoint-template.ts`: health-endpoint-template のテンプレート
  - `templates/rollback-checklist.md`: rollback-checklist のチェックリスト
  - `templates/smoke-test-template.ts`: smoke-test-template のテンプレート
  - `resources/requirements-index.md`: 要求仕様の索引（docs/00-requirements と同期）
  
  Use proactively when handling deployment strategies tasks.
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

# Deployment Strategies

## 概要

本番環境への安全なデプロイとリスク軽減を専門とするスキル。
Blue-Green、Canary、Rolling等のデプロイパターンとロールバック戦略を提供します。
専門分野:

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
- デプロイ戦略を選択・設計する時
- ロールバック手順を定義する時
- 本番デプロイのリスクを最小化したい時
- ヘルスチェックとスモークテストを設計する時

### 避けるべきこと
- アンチパターンや注意点を確認せずに進めることを避ける

## コマンドリファレンス

### リソース読み取り
```bash
cat .claude/skills/deployment-strategies/resources/Level1_basics.md
cat .claude/skills/deployment-strategies/resources/Level2_intermediate.md
cat .claude/skills/deployment-strategies/resources/Level3_advanced.md
cat .claude/skills/deployment-strategies/resources/Level4_expert.md
cat .claude/skills/deployment-strategies/resources/deployment-patterns.md
cat .claude/skills/deployment-strategies/resources/health-checks.md
cat .claude/skills/deployment-strategies/resources/legacy-skill.md
cat .claude/skills/deployment-strategies/resources/railway-deployment.md
cat .claude/skills/deployment-strategies/resources/rollback-strategies.md
```

### スクリプト実行
```bash
node .claude/skills/deployment-strategies/scripts/health-check.mjs --help
node .claude/skills/deployment-strategies/scripts/log_usage.mjs --help
node .claude/skills/deployment-strategies/scripts/validate-skill.mjs --help
```

### テンプレート参照
```bash
cat .claude/skills/deployment-strategies/templates/deployment-runbook.md
cat .claude/skills/deployment-strategies/templates/health-endpoint-template.ts
cat .claude/skills/deployment-strategies/templates/rollback-checklist.md
cat .claude/skills/deployment-strategies/templates/smoke-test-template.ts
```

## 変更履歴

| Version | Date | Changes |
| --- | --- | --- |
| 1.0.0 | 2025-12-24 | Spec alignment and required artifacts added |
