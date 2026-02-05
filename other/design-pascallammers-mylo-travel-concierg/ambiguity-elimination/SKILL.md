---
name: ambiguity-elimination
description: |
  曖昧性検出と除去スキル。定性的・不明確な表現を具体的・測定可能な要件に変換します。

  Anchors:
  • Don't Make Me Think（Steve Krug）/ 適用: ユーザビリティ判断とUI明確性 / 目的: ユーザーが「考えずに理解できる」表現基準の提供
  • 5つの曖昧性パターン / 適用: 要件ドキュメント全体 / 目的: 定性的・曖昧な表現を体系的に検出・排除
  • 定量化フレームワーク / 適用: 非機能要件の具体化 / 目的: 「速い」「多い」などの曖昧語を計測可能な指標へ変換

  Trigger:
  要件ドキュメントに「速い」「多い」「適切に」などの定性的表現や、定義・スコープ・条件が不明確な箇所があるとき。受容基準・パフォーマンス目標・条件の曖昧性を解決してから開発を開始する必要があるときに適用。
allowed-tools:
  - bash
  - node
---

# 曖昧性除去（Ambiguity Elimination）

## 概要

定性的で不明確な表現を具体的・測定可能な要件に変換するスキル。「速い」「多い」「適切に」などの曖昧語を特定し、発注元・開発者間で検証可能な基準へと結晶化させます。

## ワークフロー

### Phase 1: 曖昧性検出と分類

**目的**: 要件ドキュメント内の曖昧性を見つけ、5つのパターンに分類する

**アクション**:

1. `references/ambiguity-patterns.md` で5つのパターン（定性語、定義不在、スコープ不明、条件不明、対象不明）を確認
2. `detect-ambiguity.mjs` スクリプトで自動検出、または `assets/clarification-checklist.md` で手動検査
3. 検出した曖昧性を一覧化

**Task**: `agents/analyze-ambiguity-context.md` を参照

### Phase 2: 明確化と定量化

**目的**: 曖昧な表現を定量的・具体的な基準に変換する

**アクション**:

1. `assets/clarification-template.md` で各曖昧性に対する明確化質問を実施
2. 発注元・ステークホルダーから定量値・具体例を獲得
3. 新しい受容基準（AC: Acceptance Criteria）を記述

**Task**: `agents/clarify-requirements.md` を参照

### Phase 3: 検証と記録

**目的**: 変換結果を検証し、改善フィードバックを記録

**アクション**:

1. 新規ACが元の要件意図を失わていないか確認
2. 開発チーム・テストチームが「測定・検証可能」と同意するか確認
3. `log_usage.mjs` で使用実績を記録

**Task**: `agents/validate-clarification.md` を参照

## Task仕様ナビ

| Task名               | 役割                               | 入力                                  | 出力                                     | 参照先                                                          | 実行タイミング |
| -------------------- | ---------------------------------- | ------------------------------------- | ---------------------------------------- | --------------------------------------------------------------- | -------------- |
| **曖昧性検出**       | 要件内のあいまいな表現を発見・分類 | 要件ドキュメント（テキスト/Markdown） | 曖昧性一覧（パターン・箇所・重要度付き） | `references/ambiguity-patterns.md`                              | Phase 1で実施  |
| **明確化ヒアリング** | ステークホルダーへの質問と回答収集 | 曖昧性一覧 + テンプレート             | 定量値・具体例・基準値                   | `assets/clarification-template.md` `clarification-checklist.md` | Phase 2の前半  |
| **受容基準記述**     | 新しいAcceptance Criteriaを作成    | ヒアリング結果 + スキーマ             | 測定可能なAC（Given-When-Then など）     | `references/Level2_intermediate.md`                             | Phase 2の後半  |
| **検証会議**         | 開発・テストチームとの同意確認     | 新規AC + 関連要件                     | 承認記録・修正指摘                       | `references/Level1_basics.md`                                   | Phase 3で実施  |

## ベストプラクティス

### すべきこと

- 要件に「速い」「多い」「適切に」などの曖昧な表現がある時
- 定量化が必要な非機能要件の記述時
- 「など」「等」で範囲が不明確な時
- 条件や主体が曖昧な要件の明確化時

### 避けるべきこと

- アンチパターンや注意点を確認せずに進めることを避ける
- 曖昧性の検出段階をスキップして直接ACを書き直す
- 発注元への確認なしに、勝手に定量値を決める
- 元の要件の意図を無視して過度に具体化する

## リソース参照

### 参照資料

以下のリソースは必要に応じて参照してください。

**基礎から応用まで（段階的学習）**:

- `references/Level1_basics.md`: 曖昧性の基本概念と検出パターン（初心者向け）
- `references/Level2_intermediate.md`: 実務での明確化手順と質問テンプレート（実践向け）
- `references/Level3_advanced.md`: 複雑な非機能要件の定量化（応用向け）
- `references/Level4_expert.md`: ドメイン固有の曖昧性と高度なフレームワーク（専門向け）

**パターンカタログ**:

- `references/ambiguity-patterns.md`: 5つの曖昧性パターン（定性語、定義不在、スコープ不明、条件不明、対象不明）と検出・除去手法（**Phase 1で必読**）
- `references/ambiguity-patterns-guide.md`: パターン別の実践ガイド

**参考記録**:

- `references/legacy-skill.md`: 旧SKILL.md（過去の実装参照用）

### テンプレート

**Phase 2で使用**:

- `assets/clarification-template.md`: 各曖昧性に対する質問テンプレート（ステークホルダーヒアリング用）
- `assets/clarification-checklist.md`: 曖昧性検証チェックリスト（手動検査用）

### スクリプト

**自動化ツール**:

- `scripts/detect-ambiguity.mjs`: 要件ドキュメントから曖昧性を自動検出（Phase 1で活用）
- `scripts/log_usage.mjs`: スキル使用記録と自動評価（Phase 3で実行）
- `scripts/validate-skill.mjs`: スキル構造検証（開発時用）

## 変更履歴

| Version | Date       | Changes                                                                                           |
| ------- | ---------- | ------------------------------------------------------------------------------------------------- |
| 2.0.0   | 2025-12-31 | agents/3ファイル追加、Phase別Task参照を追加                                                       |
| 1.1.0   | 2025-12-31 | 18-skills.md仕様に準拠: YAML frontmatter更新、description にAnchors/Trigger追加、Task仕様ナビ追加 |
| 1.0.0   | 2025-12-24 | 初版: 基本的なワークフロー、ベストプラクティス、リソース参照を定義                                |
