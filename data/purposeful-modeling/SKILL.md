---
name: purposeful-modeling
description: 目的を持ったモデリングの専門知識を提供。概念・仕様・実装の3つの視点を区別してUML図を生成する際に使用。ドメインモデル設計、クラス図作成、要件分析、モデリング成果物の目的分類が必要な場合にこのスキルを参照。
---

# 目的を持ったモデリング

John Daniels「Modeling with a Sense of Purpose」に基づく、視点を明確にしたモデリング手法。

## 核心原則

**すべてのモデルは、作成前に目的を宣言すること。**

## 3つの視点

| 視点 | 目的 | ステレオタイプ | 問いかけ |
|------|------|---------------|----------|
| **概念** | 現実世界を理解 | `<<concept>>` | 「それは何か？」 |
| **仕様** | 要件を定義 | `<<type>>` | 「何をすべきか？」 |
| **実装** | コードを説明 | `<<class>>` | 「どう作られているか？」 |

## 視点別ルール

### conceptual（概念モデル）

**適用**:
- ステレオタイプ: `<<concept>>`, `<<domain>>`, `<<entity>>`
- 属性: ドメイン型（Money, Date, Quantity）
- 関係: 多重度のみ、ナビゲーション方向なし

**除外**:
- メソッド/操作
- ID, version, 外部キー
- 可視性修飾子（+, -, #）
- 技術的な型（Long, UUID, List<T>）
- Repository, Service クラス

### specification（仕様モデル）

**適用**:
- ステレオタイプ: `<<type>>`, `<<interface>>`, `<<service>>`
- 操作: シグネチャのみ
- 属性: 型付き

**除外**:
- private メンバー
- デザインパターン構造
- Impl 接尾辞

### implementation（実装モデル）

**適用**:
- ステレオタイプ: `<<class>>`, `<<component>>`, `<<strategy>>`
- 可視性修飾子
- デザインパターン
- すべての技術的詳細

## 詳細リファレンス

詳細なルールと例は以下を参照:

- [references/three-perspectives.md](references/three-perspectives.md) - 視点の詳細定義
- [references/uml-notation-guide.md](references/uml-notation-guide.md) - 視点別UML記法
- [references/examples.md](references/examples.md) - 具体的なモデリング例

## 検証チェックリスト

モデルを完成させる前に確認:

- [ ] 視点が図に明示されている
- [ ] 単一視点を一貫して使用
- [ ] ステレオタイプが視点に適切
- [ ] 禁止要素が含まれていない
