---
name: json-optimization
description: |
  JSON最適化の専門スキル。
  シリアライゼーション、ペイロードサイズ削減、スキーマ設計を提供します。

  Anchors:
  • 『High Performance Browser Networking』（Ilya Grigorik） / 適用: データ最適化 / 目的: 転送効率向上

  Trigger:
  JSON最適化時、ペイロード削減時、APIレスポンス最適化時に使用
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# JSON最適化（SQLite）

## 概要

SQLiteのJSON1拡張を活用した柔軟なデータ構造設計とパフォーマンス最適化に特化したスキル。半構造化データの効率的な格納、式インデックスによる高速検索、Zodスキーマ統合による検証を提供します。

詳細は `references/Level1_basics.md` と `references/Level2_intermediate.md` を参照してください。

## ワークフロー

### Phase 1: 目的と前提の整理

**目的**: JSON最適化タスクの要件と制約条件を明確にする

**Task**: `agents/analyze-requirements.md`

**アクション**:

1. `references/Level1_basics.md` でJSON1拡張の基礎を確認
2. ペイロードサイズ、クエリパターン、スキーマの動的性を分析
3. 最適化対象（検索速度 vs. ストレージ）を特定

### Phase 2: スキル適用

**目的**: 公式テンプレートと参考資料を使用して実装を進める

**Task**: `agents/design-json-structure.md`

**アクション**:

1. `assets/json-schema-design.md` でJSON構造を設計
2. `references/json-functions-reference.md` でJSON関数を選択
3. 式インデックスとCHECK制約を検討
4. `scripts/analyze-json-usage.mjs` でリレーショナル分離の判定

### Phase 3: 検証と記録

**目的**: 成果物の検証と実行結果の記録

**Task**: `agents/validate-optimization.md`

**アクション**:

1. `scripts/validate-skill.mjs` でスキル適用を検証
2. `scripts/log_usage.mjs` で実行結果を記録
3. `references/Level3_advanced.md` でパフォーマンス最適化の確認

## Task仕様ナビ

| Task                        | 対応リソース                                        | スクリプト             | 説明                             |
| --------------------------- | --------------------------------------------------- | ---------------------- | -------------------------------- |
| JSON構造の基本設計          | Level1_basics.md, assets/json-schema-design.md      | -                      | 半構造化データのスキーマ設計     |
| 検索パフォーマンス最適化    | json-functions-reference.md, Level2_intermediate.md | analyze-json-usage.mjs | json_extract, 式インデックス活用 |
| 動的スキーマ検証            | Level3_advanced.md                                  | -                      | CHECK制約, Zodスキーマ統合       |
| リレーショナル vs. JSON分析 | legacy-skill.md, Level4_expert.md                   | analyze-json-usage.mjs | データベース設計の選択判定       |
| 実装の検証                  | -                                                   | validate-skill.mjs     | スキル構造とアーティファクト確認 |

## ベストプラクティス

### すべきこと

- 動的に変化するスキーマ属性の格納時
- ペイロードサイズを削減する必要がある時
- 複数の検索パターンに対応する時
- スキーマ検証を厳密に管理する時
- `json_extract()` でインデックス対象の列を明確にする
- CHECK制約でJSON構造を検証する
- Level2以上のドキュメントで設計パターンを確認する

### 避けるべきこと

- スキーマレスだからと検証なしで進める
- 式インデックスなしで大規模JSON検索を実装する
- リレーショナル設計とJSON設計を混在させる
- `json_extract()` で常に完全なオブジェクトを取得する
- アンチパターンを確認せずに設計を進める
- パフォーマンス測定なしで最適化を判定する

## リソース参照

### 段階的学習（Progressive Disclosure）

| レベル | リソース                          | 対象タスク           | 読了目安 |
| ------ | --------------------------------- | -------------------- | -------- |
| 基礎   | references/Level1_basics.md       | JSON1拡張の概要      | 5分      |
| 実務   | references/Level2_intermediate.md | 実装パターン         | 15分     |
| 応用   | references/Level3_advanced.md     | パフォーマンス最適化 | 20分     |
| 専門   | references/Level4_expert.md       | 複雑な設計           | 30分     |

### リソース詳細

- `references/json-functions-reference.md`: JSON関数（json_extract, json_type, json_valid）とインデックス活用
- `references/legacy-skill.md`: 旧スキル実装（参考情報）

## コマンドリファレンス

### リソース読み取り

```bash
# 段階的学習
cat references/Level1_basics.md
cat references/Level2_intermediate.md
cat references/Level3_advanced.md
cat references/Level4_expert.md

# 詳細参考
cat references/json-functions-reference.md
cat references/legacy-skill.md
```

### スクリプト実行

```bash
# JSON使用状況の分析とリレーショナル分離推奨
node scripts/analyze-json-usage.mjs --help

# 実行結果の記録
node scripts/log_usage.mjs --result success --phase "Phase 2"

# スキル構造の検証
node scripts/validate-skill.mjs
```

### テンプレート参照

```bash
# JSON構造設計（式インデックス/CHECK制約/Zodスキーマ統合）
cat assets/json-schema-design.md
```

## 変更履歴

| Version | Date       | Changes                                                        |
| ------- | ---------- | -------------------------------------------------------------- |
| 2.0.0   | 2025-12-31 | 18-skills.md仕様への完全準拠。Task仕様ナビ、リソース参照の改善 |
| 1.0.0   | 2025-12-24 | 初版                                                           |
