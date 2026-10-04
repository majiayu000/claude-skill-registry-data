---
name: decide
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-15
updated: 2026-03-15
description: 体系化された意思決定：メリット・デメリット行列、加重スコアリング、意思決定ツリー、シナリオ分析、アイゼンハワー行列。
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: utilities
tags: [decision, evaluation, prioritization, framework]
language: ja
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/_services/decide.md', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-15', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

<img src="../banner.png" width="100%" alt="decide banner">

> **日本語** — `decide` の公式日本語版。


# Decide — 体系化された意思決定

> 体系化されたフレームワークと評価手法による合理的判断

---

## 使用タイミング

- 複数の選択肢から選ぶ場合
- メリット・デメリット（Pro/Con）のリストが必要な場合
- 多基準の意思決定
- 重要な決定に対して不確実性がある場合

**トリガーワード：** decide, choose, compare, evaluate, weigh

---

## フレームワーク

### 1. メリット・デメリット行列（シンプル）

2つの選択肢間の迅速な意思決定。

```
PRO A:                    CON A:
- Advantage 1             - Disadvantage 1
- Advantage 2             - Disadvantage 2

PRO B:                    CON B:
- Advantage 1             - Disadvantage 1
- Advantage 2             - Disadvantage 2

Recommendation: [A/B] because [reasoning]
```

---

### 2. 加重スコアリング（複雑）

重み付けを伴う多基準意思決定。

| 評価基準 | 重み | 選択肢 A | スコア A | 選択肢 B | スコア B |
|-----------|--------|----------|---------|----------|---------|
| 基準 1 | 30% | 8 | 2.4 | 6 | 1.8 |
| 基準 2 | 25% | 7 | 1.75 | 9 | 2.25 |
| 合計 | 100% | - | X.XX | - | X.XX |

**プロセス：**
1. 基準の収集
2. 重み付けの割り当て（合計 = 100%）
3. 選択肢の評価（1〜10のスケール）
4. スコアの計算（評価 × 重み）
5. 比較と推奨

---

### 3. 意思決定ツリー（シーケンシャル）

明確な If-Then パスを伴う意思決定：
1. 出発点となる質問を定義
2. 最初の分岐点（最も重要な基準）
3. 次のレベル（2番目に重要な基準）
4. 最終的な選択肢に至る

---

### 4. シナリオ分析（不確実性）

```
Best Case (X% probability):
  Outcome: +Y points -> Expected value: +Z

Realistic Case (X%):
  Outcome: +Y -> Expected value: +Z

Worst Case (X%):
  Outcome: -Y -> Expected value: -Z

Total expected value: [Sum]
```

---

### 5. アイゼンハワー行列（優先順位付け）

```
              URGENT          NOT URGENT
IMPORTANT     1. DO           2. PLAN
NOT IMPORTANT 3. DELEGATE     4. ELIMINATE
```

---

## 品質チェックリスト

最終推奨の前のチェック項目：
- [ ] すべての関連基準が特定されているか？
- [ ] ユーザーの価値観が考慮されているか？
- [ ] 長期的な影響が考慮されているか？
- [ ] リスクが特定され評価されているか？
- [ ] バイアスチェックが実施されているか？
- [ ] 可逆性が評価されているか？

---

## ベストプラクティス

### 基準の定義
- 具体性があり測定可能であること
- 多すぎないこと（3〜7個が理想）
- お互いに独立していること

### 重み付け
- 合計 = 100%
- 最も重要な基準 >= 25%
- 5%未満の重み付けは避ける

### 推奨事項
- 明確で根拠があること
- 代替案に言及すること
- リスクを明記すること
- 可逆性を考慮すること

---

## ワークフローと手順

```
1. User request
2. Understand decision
3. Identify options (2-5)
4. Choose framework
5. Collect criteria
6. Apply framework
7. Bias check (optional)
8. Make recommendation
9. Document reasoning
```

---

## 変更履歴

### 1.0.0 (2026-03-15)
- BACH v3.8.0 から移植

---

*BACH v3.8.0 から移植 | スタンドアロン版*
