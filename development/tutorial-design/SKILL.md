---
name: tutorial-design
description: |
  効果的な学習体験を提供するチュートリアル・学習コンテンツの設計スキル。段階的学習パス、成功体験ファースト、レベル別ガイドを組み合わせた体系的アプローチで、学習者の理解度に応じた最適な学習導線を構築します。

  Anchors:
  • The Pragmatic Programmer（Andrew Hunt, David Thomas） / 適用: 実践的改善とコンテンツ品質維持 / 目的: 学習体験の効率化
  • Docs for Developers（Jared Bhatti） / 適用: チュートリアル設計と段階的ガイド / 目的: 学習パス最適化

  Trigger:
  チュートリアル設計、学習コンテンツ作成、段階的ガイド構築、教材構造化、学習者向けドキュメント開発時に使用
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Tutorial Design スキル

## 概要

効果的な学習体験を提供するチュートリアル・学習コンテンツを設計するスキル。段階的学習パス、成功体験ファースト、レベル別ガイドを組み合わせた体系的アプローチで、学習者の理解度に応じた最適な学習導線を構築します。

## ワークフロー

### Phase 1: 学習目標と対象者の明確化

**目的**: チュートリアルが対象とする学習目標と学習者プロフィールを定義する

**アクション**:

1. 学習対象者のレベル（初心者/中級者/上級者）を判定
2. 期待される学習成果と到達目標を言語化
3. 前提知識要件を整理

**参照**: [references/Level1_basics.md](references/Level1_basics.md)

### Phase 2: 学習パス構築と段階設計

**目的**: レベル別ガイドを組み合わせた段階的学習パスを構築する

**アクション**:

1. 学習内容を論理的セクションに分割
2. 成功体験ファーストの原則に従い、簡単な例から複雑な例へ段階化
3. 各セクションの学習到達目標を定義
4. テンプレートに従い、段階的ガイドを作成

**参照**: [references/learning-path-design.md](references/learning-path-design.md), [assets/tutorial-template.md](assets/tutorial-template.md)

### Phase 3: コンテンツ検証と記録

**目的**: 成果物の検証と実行記録の保存

**アクション**:

1. `scripts/validate-skill.mjs` でコンテンツ構造を確認
2. 成果物が学習目標に合致するか検証
3. `scripts/log_usage.mjs` を実行して記録を残す

## Task仕様（ナビゲーション）

チュートリアル設計の各タスクと対応するエージェント・リソースの対応表

| Task           | エージェント                            | 思考様式       | 説明                               |
| -------------- | --------------------------------------- | -------------- | ---------------------------------- |
| 学習目標分析   | `agents/learning-objective-analysis.md` | Benjamin Bloom | 学習目標と到達レベルを定義         |
| 学習パス設計   | `agents/learning-path-design.md`        | Jared Bhatti   | 段階的で効果的な学習パスを設計     |
| コンテンツ作成 | `agents/tutorial-content-creation.md`   | Andrew Hunt    | 各セクションの具体的コンテンツ作成 |
| 学習評価設計   | `agents/learning-assessment-design.md`  | Grant Wiggins  | 評価基準とチェックリストを設計     |

### ワークフロー順序

```
learning-objective-analysis → learning-path-design → tutorial-content-creation → learning-assessment-design
```

1. **learning-objective-analysis**: Bloom's Taxonomyで学習目標を分析・分類
2. **learning-path-design**: 成功体験ファーストで段階的学習パスを構築
3. **tutorial-content-creation**: 各セクションのコンテンツと実習を作成
4. **learning-assessment-design**: 逆向き設計で評価基準とルーブリックを設計

## ベストプラクティス

### すべきこと

- **段階的開示**: 学習者の理解度に応じて、情報を段階的に提示する
- **成功体験ファースト**: 初期段階で達成可能なタスクから開始し、学習者に自信をつけさせる
- **目標の言語化**: 各セクション・レッスンで、具体的な学習目標を明記する
- **フィードバック機構**: チェックリスト、練習問題、評価基準を含める
- **前提知識の明確化**: 必要な前提知識を冒頭で示し、不可欠な参照資料へのリンクを提供する

### 避けるべきこと

- **段階なしの一気説明**: 複雑な概念を前提知識なしに説明することを避ける
- **カテゴリ的な分類**: トピックを体系化したリストで終わらせず、必ず実行可能なステップに落とし込む
- **仮定の多さ**: 読み手の知識や環境を仮定しすぎず、具体的な前提を明記する
- **評価基準なし**: 学習成果の測定方法を定義しないまま進めることを避ける

## リソース参照

### 参照資料（references/）

各段階別の詳細ガイドと知識体系が外部化されています。必要に応じて参照してください：

- **[Level1_basics.md](references/Level1_basics.md)**: チュートリアル設計の基礎、成功体験ファースト、レベル1学習パス
- **[Level2_intermediate.md](references/Level2_intermediate.md)**: 段階的ガイド構築、学習パス設計の実務手順、レベル2学習パス
- **[Level3_advanced.md](references/Level3_advanced.md)**: 複雑なコンテンツ構造化、評価設計、メタ認知の活用
- **[Level4_expert.md](references/Level4_expert.md)**: 企業規模の学習プログラム設計、包括的学習体系、フィードバックループ構築
- **[learning-path-design.md](references/learning-path-design.md)**: 学習パス設計の方法論、段階化手法、学習者分類

### スクリプト（scripts/）

- **[estimate-completion-time.mjs](scripts/estimate-completion-time.mjs)**: チュートリアル完了予想時間の推定
- **[log_usage.mjs](scripts/log_usage.mjs)**: スキル使用履歴の記録（フィードバックループ用）
- **[validate-skill.mjs](scripts/validate-skill.mjs)**: スキル構造と成果物の検証

### アセット（assets/）

- **[tutorial-template.md](assets/tutorial-template.md)**: チュートリアル・学習ガイドの標準テンプレート

## 変更履歴

| Version | Date       | Changes                                                                                           |
| ------- | ---------- | ------------------------------------------------------------------------------------------------- |
| 2.0.0   | 2025-12-31 | 18-skills.md仕様に準拠。frontmatterにAnchorsとTrigger追加、Task仕様ナビを導入、リソース参照を整理 |
| 1.0.0   | 2025-12-24 | Spec alignment and required artifacts added                                                       |
