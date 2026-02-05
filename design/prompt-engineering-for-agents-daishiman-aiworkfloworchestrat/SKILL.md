---
name: prompt-engineering-for-agents
description: |
  エージェント向けプロンプトエンジニアリングを専門とするスキル。System Prompt設計、Few-Shot Examples、Role Prompting技術により、高品質なエージェント動作を実現します。

  Anchors:
  • The Pragmatic Programmer (Andrew Hunt, David Thomas) / 適用: 手順設計と実践的改善 / 目的: 体系的なプロンプト設計
  • Role Prompting patterns / 適用: ペルソナ設計と役割定義 / 目的: エージェント動作の最適化
  • Few-Shot Learning / 適用: 効果的な例示選択 / 目的: 文脈構成の改善
  • Prompt Engineering Guide (DAIR.AI) / 適用: プロンプト最適化技術 / 目的: 高品質な応答生成

  Trigger:
  Use when designing system prompts for agents, optimizing agent behavior, implementing role prompting, creating few-shot examples, or improving agent prompt quality.
  Keywords: system prompt, agent prompting, role prompting, few-shot learning, prompt optimization, agent behavior
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Prompt Engineering for Agents

## 概要

このスキルは、エージェント向けのSystem Prompt設計とプロンプト最適化を専門とします。
Role Prompting、Few-Shot Learning、構造化ワークフローなどの技術を活用し、
エージェントの動作品質を体系的に向上させます。

### 対象ユースケース

- **新規エージェント設計**: System Promptをゼロから設計
- **既存エージェント改善**: 動作品質を最適化
- **プロンプト品質評価**: 効果測定と改善提案
- **Few-Shot Examples作成**: 適切な例示を設計

### 主要な知識リソース

- `references/basics.md`: プロンプトエンジニアリングの基本原則
- `references/patterns.md`: System Promptパターン集
- `references/few-shot-techniques.md`: Few-Shot Learning技術
- `references/optimization-strategies.md`: 最適化戦略
- `references/anti-patterns.md`: アンチパターンとトラブルシューティング

## ワークフロー

### Phase 1: 要件分析

**目的**: エージェントの目的と要件を明確にする

**手順**:

1. エージェントの役割と責任範囲を定義
2. 対象タスクと期待される成果物を特定
3. 制約条件と禁止事項を洗い出し
4. `references/basics.md` で基本原則を確認

**成果物**:

- エージェント要件定義（役割、タスク、制約）
- 成功基準リスト

**判断ポイント**:

- 役割定義は1-2文で明確か？
- タスク範囲は具体的か？
- 制約は測定可能か？

### Phase 2: System Prompt設計

**目的**: 構造化されたSystem Promptを作成

**手順**:

1. `assets/prompt-template.md` をベースに骨格を作成
2. `references/patterns.md` から適切なパターンを選択
3. 推奨7セクション構造に従って記述:
   - 役割定義
   - 専門分野
   - ワークフロー
   - スキル管理
   - ベストプラクティス
   - 詳細リファレンス
   - 変更履歴
4. `agents/design-system-prompt.md` を参照して詳細化

**成果物**:

- 完全なSystem Prompt文書
- 役割定義、ワークフロー、制約を含む

**判断ポイント**:

- 7セクション構造に準拠しているか？
- 曖昧な表現（「適宜」「など」）がないか？
- ワークフローは具体的な手順か？

### Phase 3: Few-Shot Examples作成

**目的**: 効果的な例示を設計

**手順**:

1. `references/few-shot-techniques.md` で選択基準を確認
2. 典型的なケースを2-3個選定
3. 境界ケース・エッジケースを1-2個追加
4. 各例に入力・処理・出力を明記
5. 例の数は2-5個に制限（過度な例示を避ける）

**成果物**:

- 2-5個のFew-Shot Examples
- 入力→処理→出力の流れを含む

**判断ポイント**:

- 例は実際の値を使用しているか？
- 典型例と境界例をカバーしているか？
- 例の数は適切（2-5個）か？

### Phase 4: 動作最適化

**目的**: プロンプトを最適化し品質を向上

**手順**:

1. `scripts/analyze-prompt.mjs` で初期分析
2. `references/optimization-strategies.md` で最適化技術を確認
3. 以下の観点で改善:
   - 明確性: 曖昧な表現を排除
   - 簡潔性: 冗長な説明を削減
   - 構造化: セクション構成を整理
   - 具体性: 抽象的な指示を具体化
4. `agents/optimize-agent-behavior.md` を参照して実施

**成果物**:

- 最適化されたSystem Prompt
- 改善ポイントのドキュメント

**判断ポイント**:

- Token数は適切か？
- 指示は具体的で実行可能か？
- 構造は論理的か？

### Phase 5: 品質評価と検証

**目的**: プロンプトの効果を測定し検証

**手順**:

1. `scripts/validate-prompt-quality.mjs` で品質チェック
2. `agents/evaluate-prompt-quality.md` の評価基準に従う
3. 以下の指標で評価:
   - **明確性**: 指示の明瞭さ（1-5点）
   - **具体性**: 実行可能性（1-5点）
   - **構造化**: セクション構成（1-5点）
   - **完全性**: 必須要素の充足（1-5点）
4. アンチパターンを `references/anti-patterns.md` で確認

**成果物**:

- 品質評価レポート
- 改善推奨リスト

**判断ポイント**:

- 各指標が4点以上か？
- アンチパターンが含まれていないか？
- テストケースで正しく動作するか？

### Phase 6: ドキュメント化と記録

**目的**: 設計プロセスと成果を記録

**手順**:

1. 設計意図と判断根拠を文書化
2. `scripts/log_usage.mjs` で使用記録を保存
3. 変更履歴を更新
4. 評価結果をLOGS.mdに追記

**成果物**:

- プロンプト設計ドキュメント
- 使用ログと評価記録

## 使用タイミング

### このスキルを使うべき時

- ✅ 新しいエージェントのSystem Promptを設計する
- ✅ 既存エージェントの動作を改善する
- ✅ プロンプトの品質を評価する
- ✅ Few-Shot Examplesを追加・改善する
- ✅ エージェント間の一貫性を確保する

### このスキルを使わない時

- ❌ 単純な質問応答（エージェント設計不要）
- ❌ 一度きりのタスク（再利用性がない）
- ❌ プロンプトエンジニアリング不要な作業

## ベストプラクティス

### すべきこと

- ✅ **明確な役割定義**: Role Promptingパターンを使用
- ✅ **構造化**: 7セクション構造に従う
- ✅ **適切な例示**: 2-5個のFew-Shot Examples
- ✅ **制約明示**: すべきこと・避けるべきことを明記
- ✅ **段階的改善**: フィードバックループで継続改善
- ✅ **テンプレート活用**: `assets/prompt-template.md` を使用
- ✅ **品質評価**: 定量的な指標で測定

### 避けるべきこと

- ❌ **曖昧な表現**: 「適宜」「など」「必要に応じて」
- ❌ **過度な例示**: 10個以上のFew-Shot Examples
- ❌ **非構造化**: 一貫性のないセクション構成
- ❌ **制約の欠如**: ガードレールなし
- ❌ **知識の重複**: 外部スキルと重複する詳細
- ❌ **長すぎる文**: 1文が3行以上
- ❌ **検証なし**: 品質チェックをスキップ

## Agent Task仕様書

複雑なプロンプト設計タスクには、専門のAgent Task仕様書を使用:

- `agents/design-system-prompt.md`: System Prompt設計専門タスク
- `agents/optimize-agent-behavior.md`: エージェント動作最適化タスク
- `agents/evaluate-prompt-quality.md`: プロンプト品質評価タスク

## スクリプトとツール

### 分析・検証スクリプト

```bash
# プロンプト構造を分析
node scripts/analyze-prompt.mjs <prompt-file>

# 品質を検証
node scripts/validate-prompt-quality.mjs <prompt-file>

# スキル構造を検証
node scripts/validate-skill.mjs
```

### ログ記録

```bash
# 使用記録を保存
node scripts/log_usage.mjs --task "prompt-design" --outcome "success"
```

### テンプレート

```bash
# プロンプトテンプレートを参照
cat assets/prompt-template.md
```

## 詳細リファレンス

### 基本知識

- `references/basics.md`: プロンプトエンジニアリングの基本原則と用語

### パターンとテクニック

- `references/patterns.md`: System Promptの7つの主要パターン
- `references/few-shot-techniques.md`: Few-Shot Learning技術と選択基準
- `references/optimization-strategies.md`: プロンプト最適化の実践戦略

### トラブルシューティング

- `references/anti-patterns.md`: よくある失敗パターンと対処法

## 変更履歴

| Version | Date       | Changes                                              |
| ------- | ---------- | ---------------------------------------------------- |
| 2.1.0   | 2026-01-02 | 18-skills.md仕様に完全準拠。新referencesとagents追加 |
| 2.0.0   | 2025-12-24 | Spec alignment and required artifacts added          |
| 1.0.0   | 2025-11-24 | 初版作成                                             |
