---
name: troubleshooting-guides
description: |
  問題解決を効率化するトラブルシューティングガイドの設計スキル。
  診断フロー、問題分類、解決手順書を体系的に設計します。

  Anchors:
  • 『Don't Make Me Think』（Steve Krug）/ 適用: ユーザビリティ設計 / 目的: 問題自己解決力向上
  • SRE原則 / 適用: 障害対応 / 目的: トラブル診断効率化

  Trigger:
  トラブルシューティングガイド作成時、問題診断フロー設計時、エラー説明書作成時に使用
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Troubleshooting Guides スキル

## 概要

問題解決を効率化するトラブルシューティングガイドの設計スキル。複雑な問題を段階的に解決するための診断フロー、問題分類、解決手順書の設計を扱います。ユーザビリティに基づいた情報設計により、サポートドキュメントやデバッグガイドの品質を向上させ、ユーザーの自己解決能力を高めます。

詳細な手順や背景は `references/Level1_basics.md` と `references/Level2_intermediate.md` を参照してください。

## ワークフロー

### Phase 1: 目的と前提の整理

**目的**: タスクの目的と前提条件を明確にし、適用スコープを定める

**アクション**:

1. トラブルシューティング対象のシステム・プロダクトを特定
2. `references/Level1_basics.md` を確認し、問題分類方法を理解
3. `references/problem-classification.md` で既存の分類体系を確認
4. 必要なテンプレート（診断フロー、エラー説明）を選定

### Phase 2: スキル適用

**目的**: スキルの指針に従い、診断フロー・解決手順書を設計・実装

**アクション**:

1. `references/Level2_intermediate.md` を参照し、実務手順を整理
2. `assets/diagnosis-flow-template.md` を使用して診断フローを構築
3. `assets/error-explanation-template.md` でエラー説明を設計
4. 重要な判断点・分岐を明確に記録
5. ユーザー視点のテスト（可読性・実用性確認）を実施

### Phase 3: 検証と記録

**目的**: 成果物の検証・最適化と実行記録の保存

**アクション**:

1. `scripts/validate-diagnostic-flow.mjs` で診断フロー構造を検証
2. `scripts/validate-skill.mjs` でドキュメント構造を確認
3. 成果物がユーザビリティ基準に合致するか確認
4. `scripts/log_usage.mjs` を実行して使用記録・評価結果を保存
5. 反復フィードバックを記録

## Task仕様（ナビゲーション）

トラブルシューティングガイド設計の各タスクと対応するエージェント・リソースの対応表

| Task             | エージェント                       | 思考様式        | 説明                               |
| ---------------- | ---------------------------------- | --------------- | ---------------------------------- |
| 問題分類設計     | `agents/problem-classification.md` | Steve Krug      | 問題を体系的に分類し判断基準を定義 |
| 診断フロー設計   | `agents/diagnosis-flow-design.md`  | Steve Krug      | 段階的な自己診断フローを構築       |
| エラー説明書作成 | `agents/error-explanation.md`      | Betsy Beyer     | 原因・影響・解決策を明確に説明     |
| 解決手順書作成   | `agents/solution-documentation.md` | Jennifer Petoff | 再現可能な解決手順を文書化         |

### ワークフロー順序

```
problem-classification → diagnosis-flow-design → error-explanation → solution-documentation
```

1. **problem-classification**: 問題パターンを抽出し、分類フレームワークを構築
2. **diagnosis-flow-design**: 分類に基づき、ユーザーが段階的に診断できるフローを設計
3. **error-explanation**: 各エラーの原因・影響・解決手順を説明するドキュメントを作成
4. **solution-documentation**: 問題別の詳細な解決手順書とFAQを作成

## ベストプラクティス

### すべきこと

- 問題分類を明確に定義し、ユーザーが直感的に判断できるようにする
- ユーザーの視点に立ち、専門用語を最小限に抑えた説明を心がける
- 診断フローで段階的な判断を提供し、ユーザーの自己解決を支援する
- エラーメッセージには「なぜそのエラーが発生したのか」と「何をすべきか」を含める
- 定期的に実際のユーザーフィードバックを反映し、ドキュメントを改善する
- `references/Level1_basics.md` を参照し、適用範囲と分類方法を明確にする
- `references/Level2_intermediate.md` を参照し、実務手順を整理する
- 作成後に `scripts/validate-diagnostic-flow.mjs` で構造的な整合性を確認する

### 避けるべきこと

- 過度に技術的な用語を使用し、一般ユーザーが理解できないドキュメントを作成する
- 診断フローの分岐が複雑過ぎて、ユーザーが迷う状況を作る
- エラーの原因だけを説明し、解決方法を示さない
- アンチパターンや注意点を確認せずに進める
- 一度作成したドキュメントを放置し、古い情報を提供し続ける
- ユーザーテストやフィードバック収集をスキップする
- `references/Level3_advanced.md` や `Level4_expert.md` の内容を無視して、基本的な手法だけに頼る

## リソース参照

### 学習リソース

- `references/Level1_basics.md` - トラブルシューティングガイド設計の基礎（問題分類、基本的な情報設計）
- `references/Level2_intermediate.md` - 実務的な設計手法（診断フロー設計、ユーザー導線設計）
- `references/Level3_advanced.md` - 応用的な手法（複雑な問題分類、スケーラブルなガイド設計）
- `references/Level4_expert.md` - 専門的な知見（ユーザビリティ測定、最適化戦略）
- `references/legacy-skill.md` - 旧SKILL.mdの全文および背景情報
- `references/problem-classification.md` - 問題分類の実例・フレームワーク

### テンプレート

- `assets/diagnosis-flow-template.md` - 診断フロー設計の標準テンプレート
- `assets/error-explanation-template.md` - エラー説明書の標準テンプレート

### スクリプト・ツール

- `scripts/validate-skill.mjs` - スキル構造・ドキュメント形式の検証
- `scripts/validate-diagnostic-flow.mjs` - 診断フローの整合性検証
- `scripts/log_usage.mjs` - スキル使用記録・自動評価スクリプト

### 参考資料

- 『Don't Make Me Think』（Steve Krug）- ユーザビリティとユーザー中心設計の原則
- 情報設計とアーキテクチャに関するベストプラクティス

## 変更履歴

| Version | Date       | Changes                                                        |
| ------- | ---------- | -------------------------------------------------------------- |
| 1.1.0   | 2025-12-31 | 18-skills.md仕様への対応、Task仕様ナビ、ベストプラクティス拡充 |
| 1.0.0   | 2025-12-24 | 初期リリース、基本的なワークフロー構造とリソース定義           |
