---
name: llm-eval-designer
description: |
  LLM生成システムの検証設計スキル。assay-kitフレームワークを活用し、LLM特有の失敗モード（幻覚、例への過学習、部分的処理）を考慮した総合的なテストケース設計を支援する。

  使用タイミング:
  - LLMベースのワークフロー/エージェントの評価設計時
  - ゴールデンデータセット（golden-dataset.yaml）の設計・拡張時
  - 既存テストが特定パターンに過学習していないか検証時
  - LLM出力の品質スコアラー設計時
  - 「なぜこのテストケースが必要か」の根拠を示す時
---

# LLM Evaluation Designer

LLM生成システムの検証を設計するためのガイド。

## Quick Start

```yaml
# 1. 検証対象の機能を特定
target_function: "テキスト置換"

# 2. 不変条件を定義
invariant: "入力テキストAをBに変換、他は不変"

# 3. 失敗モードを列挙（→ references/failure-modes.md）
failure_modes:
  - example_overfitting   # プロンプト例への過学習
  - hallucination         # 幻覚（存在しない内容の生成）
  - partial_processing    # 部分的処理

# 4. 汎化テスト設計（→ references/generalization-patterns.md）
# 5. テストケース生成（→ references/test-case-templates.md）
```

## Core Workflow

### Step 1: 失敗モード分析

LLM特有の失敗パターンを特定。詳細は [failure-modes.md](references/failure-modes.md)。

| 失敗モード | 検出方法 | 対策テスト |
|-----------|---------|-----------|
| 例への過学習 | 例と異なる入力でテスト | 同カテゴリ別例、異カテゴリ例 |
| 幻覚 | 入出力差分の厳密検証 | 入力に存在しない内容チェック |
| 部分的処理 | 全マッチの網羅性検証 | 複数出現、複数ブロック |
| 指示誤解釈 | 境界条件テスト | 類似だが異なる指示 |

### Step 2: 汎化保証設計

プロンプト例への過学習を防ぐテスト設計。詳細は [generalization-patterns.md](references/generalization-patterns.md)。

```
プロンプトに例Xがある場合：
  ├─ Xと同カテゴリの別例Y, Zでテスト
  ├─ Xと異なるカテゴリの例A, Bでテスト
  └─ テスト入力 ∩ プロンプト例 = ∅ を保証
```

### Step 3: テストマトリクス構築

変数の直交組み合わせでテストケースを生成：

```
操作種別 × 入力形態 × 出現パターン × ブロック種別
   ↓
ペアワイズ法で組み合わせ削減
   ↓
優先度付きテストケース生成
```

### Step 4: スコアラー設計

多面的な品質評価。詳細は [scorer-design.md](references/scorer-design.md)。

| スコアラー | 測定対象 | 閾値例 |
|-----------|---------|-------|
| operation-accuracy | 操作種別・数の正確性 | 80% |
| target-block-precision | ターゲット特定の正確性 | 75% |
| content-quality | 生成内容のパターンマッチ | 60% |
| anti-hallucination | 幻覚の不在 | 100% |

## References

- [failure-modes.md](references/failure-modes.md): LLM失敗モード詳細
- [generalization-patterns.md](references/generalization-patterns.md): 汎化テスト設計パターン
- [test-case-templates.md](references/test-case-templates.md): テストケーステンプレート
- [scorer-design.md](references/scorer-design.md): スコアラー設計ガイド

## Anti-Patterns

```yaml
# ✗ Bad: プロンプト例と同じ入力でテスト
prompt_example: "カート → Cart"
test_input: "カート → Cart"  # 過学習を検出できない

# ✓ Good: プロンプト例と異なる入力でテスト
prompt_example: "カート → Cart"
test_inputs:
  - "ユーザー → 利用者"  # 同カテゴリ（カタカナ）別例
  - "効率化 → 最適化"    # 異カテゴリ（漢字）
  - "API → インターフェース"  # 異カテゴリ（英語）
```

```yaml
# ✗ Bad: 単一パターンのみ許容
expectedContentPatterns:
  - "要約"

# ✓ Good: LLMの非決定性を考慮した複数パターン
expectedContentPatterns:
  - "要約|まとめ|サマリー"
```
