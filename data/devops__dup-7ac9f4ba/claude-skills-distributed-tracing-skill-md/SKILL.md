---
name: .claude/skills/distributed-tracing/SKILL.md
description: |
  分散トレーシングとOpenTelemetry統合の専門スキル。
  マイクロサービスアーキテクチャにおけるリクエストフローの可視化とボトルネック特定を提供します。
  使用タイミング:
  
  📖 参照書籍:
  - 『Observability Engineering』（Charity Majors）: ログ設計
  
  📚 リソース参照:
  - `resources/Level1_basics.md`: レベル1の基礎ガイド
  - `resources/Level2_intermediate.md`: レベル2の実務ガイド
  - `resources/Level3_advanced.md`: レベル3の応用ガイド
  - `resources/Level4_expert.md`: レベル4の専門ガイド
  - `resources/legacy-skill.md`: 旧SKILL.mdの全文
  - `resources/span-design-guide.md`: span-design-guide のガイド
  - `resources/trace-structure-design.md`: trace-structure-design の詳細ガイド
  - `resources/w3c-trace-context.md`: w3c-trace-context の詳細ガイド
  - `scripts/analyze-trace.mjs`: traceを分析するスクリプト
  - `scripts/log_usage.mjs`: 使用記録・自動評価スクリプト
  - `scripts/validate-skill.mjs`: スキル構造検証スクリプト
  - `templates/tracing-config.ts`: tracing-config のテンプレート
  
  Use proactively when handling distributed tracing tasks.
version: 1.0.0
level: 1
last_updated: 2025-12-24
references:
  - book: "Observability Engineering"
    author: "Charity Majors"
    concepts:
      - "ログ設計"
      - "メトリクス"
---

# Distributed Tracing - 分散トレーシング

## 概要

分散トレーシングとOpenTelemetry統合の専門スキル。
マイクロサービスアーキテクチャにおけるリクエストフローの可視化とボトルネック特定を提供します。
使用タイミング:

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
- 分散システムのリクエストフロー を可視化する時
- OpenTelemetryで分散トレーシングを導入する時
- トレースIDとスパンIDを設計する時
- サービス間の呼び出し関係を追跡する時
- レイテンシボトルネックを特定する時
- W3C Trace Contextでトレースを伝播させる時

### 避けるべきこと
- アンチパターンや注意点を確認せずに進めることを避ける

## コマンドリファレンス

### リソース読み取り
```bash
cat .claude/skills/distributed-tracing/resources/Level1_basics.md
cat .claude/skills/distributed-tracing/resources/Level2_intermediate.md
cat .claude/skills/distributed-tracing/resources/Level3_advanced.md
cat .claude/skills/distributed-tracing/resources/Level4_expert.md
cat .claude/skills/distributed-tracing/resources/legacy-skill.md
cat .claude/skills/distributed-tracing/resources/span-design-guide.md
cat .claude/skills/distributed-tracing/resources/trace-structure-design.md
cat .claude/skills/distributed-tracing/resources/w3c-trace-context.md
```

### スクリプト実行
```bash
node .claude/skills/distributed-tracing/scripts/analyze-trace.mjs --help
node .claude/skills/distributed-tracing/scripts/log_usage.mjs --help
node .claude/skills/distributed-tracing/scripts/validate-skill.mjs --help
```

### テンプレート参照
```bash
cat .claude/skills/distributed-tracing/templates/tracing-config.ts
```

## 変更履歴

| Version | Date | Changes |
| --- | --- | --- |
| 1.0.0 | 2025-12-24 | Spec alignment and required artifacts added |
