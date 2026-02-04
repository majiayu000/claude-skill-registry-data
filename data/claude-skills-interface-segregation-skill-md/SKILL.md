---
name: .claude/skills/interface-segregation/SKILL.md
description: |
  SOLID原則のインターフェース分離原則（ISP）を専門とするスキル。
  Robert C. Martinの『アジャイルソフトウェア開発の奥義』に基づき、
  クライアントが使用しないメソッドへの依存を強制しない、
  
  📖 参照書籍:
  - 『The Pragmatic Programmer』（Andrew Hunt, David Thomas）: 実践的改善
  
  📚 リソース参照:
  - `resources/Level1_basics.md`: レベル1の基礎ガイド
  - `resources/Level2_intermediate.md`: レベル2の実務ガイド
  - `resources/Level3_advanced.md`: レベル3の応用ガイド
  - `resources/Level4_expert.md`: レベル4の専門ガイド
  - `resources/fat-interface-detection.md`: 空実装/例外スロー/条件付き実装による肥大化検出手法
  - `resources/interface-composition.md`: allOf/extends/mixinによる小インターフェース組み合わせパターン
  - `resources/isp-principles.md`: クライアント固有インターフェース分離とSOLID準拠設計
  - `resources/legacy-skill.md`: 旧SKILL.mdの全文
  - `resources/role-interface-design.md`: 役割ベース（IValidatable/IRetryable等）インターフェース設計手法
  - `scripts/analyze-interface.mjs`: インターフェース凝集性とISP違反の自動検出
  - `scripts/log_usage.mjs`: 使用記録・自動評価スクリプト
  - `scripts/validate-skill.mjs`: スキル構造検証スクリプト
  - `templates/segregated-interface-template.md`: コア+拡張インターフェース分離設計テンプレート
  - `resources/requirements-index.md`: 要求仕様の索引（docs/00-requirements と同期）
  
  Use proactively when handling interface segregation tasks.
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

# Interface Segregation Principle (ISP)

## 概要

SOLID原則のインターフェース分離原則（ISP）を専門とするスキル。
Robert C. Martinの『アジャイルソフトウェア開発の奥義』に基づき、
クライアントが使用しないメソッドへの依存を強制しない、

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
- IWorkflowExecutorのようなコアインターフェースを設計する時
- 既存インターフェースの肥大化を検出した時
- 複数のクライアントが異なる機能を必要とする時
- インターフェースの分割を検討する時

### 避けるべきこと
- アンチパターンや注意点を確認せずに進めることを避ける

## コマンドリファレンス

### リソース読み取り
```bash
cat .claude/skills/interface-segregation/resources/Level1_basics.md
cat .claude/skills/interface-segregation/resources/Level2_intermediate.md
cat .claude/skills/interface-segregation/resources/Level3_advanced.md
cat .claude/skills/interface-segregation/resources/Level4_expert.md
cat .claude/skills/interface-segregation/resources/fat-interface-detection.md
cat .claude/skills/interface-segregation/resources/interface-composition.md
cat .claude/skills/interface-segregation/resources/isp-principles.md
cat .claude/skills/interface-segregation/resources/legacy-skill.md
cat .claude/skills/interface-segregation/resources/role-interface-design.md
```

### スクリプト実行
```bash
node .claude/skills/interface-segregation/scripts/analyze-interface.mjs --help
node .claude/skills/interface-segregation/scripts/log_usage.mjs --help
node .claude/skills/interface-segregation/scripts/validate-skill.mjs --help
```

### テンプレート参照
```bash
cat .claude/skills/interface-segregation/templates/segregated-interface-template.md
```

## 変更履歴

| Version | Date | Changes |
| --- | --- | --- |
| 1.0.0 | 2025-12-24 | Spec alignment and required artifacts added |
