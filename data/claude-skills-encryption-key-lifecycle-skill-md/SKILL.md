---
name: .claude/skills/encryption-key-lifecycle/SKILL.md
description: |
  暗号化と鍵ライフサイクル管理スキル。暗号化アルゴリズム選定、
  鍵生成、保管、ローテーション、廃棄の全フェーズを網羅します。
  保存時・転送時・使用時の暗号化戦略を提供します。
  
  📖 参照書籍:
  - 『The Pragmatic Programmer』（Andrew Hunt, David Thomas）: 実践的改善
  
  📚 リソース参照:
  - `resources/Level1_basics.md`: レベル1の基礎ガイド
  - `resources/Level2_intermediate.md`: レベル2の実務ガイド
  - `resources/Level3_advanced.md`: レベル3の応用ガイド
  - `resources/Level4_expert.md`: レベル4の専門ガイド
  - `resources/legacy-skill.md`: 旧SKILL.mdの全文
  - `resources/rotation-procedures.md`: rotation-procedures の詳細ガイド
  - `scripts/generate-keys.mjs`: keysを生成するスクリプト
  - `scripts/log_usage.mjs`: 使用記録・自動評価スクリプト
  - `scripts/validate-skill.mjs`: スキル構造検証スクリプト
  
  Use proactively when handling encryption key lifecycle tasks.
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

# Encryption & Key Lifecycle Management

## 概要

暗号化と鍵ライフサイクル管理スキル。暗号化アルゴリズム選定、
鍵生成、保管、ローテーション、廃棄の全フェーズを網羅します。
保存時・転送時・使用時の暗号化戦略を提供します。

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
- 暗号化方式を選択する時
- 鍵生成・保管方法を設計する時
- Secret Rotationプロセスを実装する時
- 鍵の廃棄・無効化手順を定義する時
- データ保護要件を評価する時

### 避けるべきこと
- アンチパターンや注意点を確認せずに進めることを避ける

## コマンドリファレンス

### リソース読み取り
```bash
cat .claude/skills/encryption-key-lifecycle/resources/Level1_basics.md
cat .claude/skills/encryption-key-lifecycle/resources/Level2_intermediate.md
cat .claude/skills/encryption-key-lifecycle/resources/Level3_advanced.md
cat .claude/skills/encryption-key-lifecycle/resources/Level4_expert.md
cat .claude/skills/encryption-key-lifecycle/resources/legacy-skill.md
cat .claude/skills/encryption-key-lifecycle/resources/rotation-procedures.md
```

### スクリプト実行
```bash
node .claude/skills/encryption-key-lifecycle/scripts/generate-keys.mjs --help
node .claude/skills/encryption-key-lifecycle/scripts/log_usage.mjs --help
node .claude/skills/encryption-key-lifecycle/scripts/validate-skill.mjs --help
```

## 変更履歴

| Version | Date | Changes |
| --- | --- | --- |
| 1.0.0 | 2025-12-24 | Spec alignment and required artifacts added |
