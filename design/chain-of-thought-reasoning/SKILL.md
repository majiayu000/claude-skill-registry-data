---
name: chain-of-thought-reasoning
description: |
  推論パターンを選択し、根拠サマリーを短く提示するためのプロンプト設計スキル。
  自己一貫性の比較、推論パターンの適用、説明の明確化を通じて、再現性の高い結論を導く。

  Anchors:
  • The Pragmatic Programmer / 適用: 手順設計 / 目的: 実践的な整理
  • Reasoning and Logic / 適用: 推論パターン / 目的: 一貫性のある説明
  • Self-Consistency (Wang et al.) / 適用: 複数案比較 / 目的: 精度向上

  Trigger:
  Use when selecting reasoning patterns, designing prompts for structured explanations, or comparing multiple solution paths for higher confidence.
allowed-tools:
  - bash
  - node
---

# Chain-of-Thought Reasoning

## 概要

推論パターンの選択と、短い根拠サマリーの提示を支援する。
詳細は `references/` に外部化し、必要時に参照する。

- プロンプト例: `assets/cot-prompt-templates.md`
- 自己一貫性テンプレ: `assets/self-consistency-template.md`

## ワークフロー

### Phase 1: 要件整理

**目的**: 推論の目的と出力形式を整理する

**アクション**:

1. `references/Level1_basics.md` で基礎概念を確認
2. 出力形式と許容粒度を整理
3. 必要な推論パターン候補を列挙

**Task**: `agents/analyze-reasoning-requirements.md`

### Phase 2: パターン選択

**目的**: 適切な推論パターンを選択する

**アクション**:

1. `references/reasoning-patterns.md` を参照
2. タスクタイプに合う推論パターンを選定
3. 補助パターンの併用可否を整理

**Task**: `agents/select-reasoning-patterns.md`

### Phase 3: プロンプト設計

**目的**: 説明サマリーを出すプロンプトを設計する

**アクション**:

1. `references/prompting-techniques.md` を参照
2. `assets/cot-prompt-templates.md` を調整
3. `assets/self-consistency-template.md` の適用可否を確認

**Task**: `agents/design-reasoning-prompts.md`

### Phase 4: 検証と記録

**目的**: 生成結果を検証し記録する

**アクション**:

1. `references/Level4_expert.md` で検証観点を確認
2. 生成結果の一貫性を検証
3. `scripts/validate-skill.mjs` で構造検証
4. `scripts/log_usage.mjs` で記録

**Task**: `agents/validate-reasoning-output.md`

## Task仕様ナビ

| Task | 役割 | 入力 | 出力 | 参照先 | 実行タイミング |
| --- | --- | --- | --- | --- | --- |
| 要件整理 | 目的/粒度整理 | 依頼内容 | 要件メモ | `references/Level1_basics.md` | Phase 1 |
| パターン選択 | 推論パターン選定 | 要件メモ | パターンメモ | `references/reasoning-patterns.md` | Phase 2 |
| プロンプト設計 | テンプレ調整 | パターンメモ | プロンプト案 | `assets/cot-prompt-templates.md` | Phase 3 |
| 検証 | 一貫性確認 | プロンプト案 | 検証メモ | `references/Level4_expert.md` | Phase 4 |

## ベストプラクティス

### すべきこと

- 出力形式と粒度を明確にする
- 推論パターンをタスクに合わせて選ぶ
- 複数案の比較で一貫性を確認する
- 根拠は短く要約する

### 避けるべきこと

- 出力粒度を曖昧にする
- パターン選択を省略する
- 長文の推論過程をそのまま出力する

## リソース参照

### 参照資料

- `references/Level1_basics.md`: 基礎概念
- `references/Level2_intermediate.md`: パターン適用
- `references/Level3_advanced.md`: 自己一貫性
- `references/Level4_expert.md`: 検証/改善
- `references/cot-fundamentals.md`: 推論整理の基礎
- `references/prompting-techniques.md`: プロンプト設計
- `references/reasoning-patterns.md`: 推論パターン
- `references/legacy-skill.md`: 旧版要約（移行時のみ）

### スクリプト

- `scripts/log_usage.mjs`: 実行ログ記録
- `scripts/validate-skill.mjs`: スキル構造検証

### テンプレート

- `assets/cot-prompt-templates.md`: プロンプト例
- `assets/self-consistency-template.md`: 自己一貫性テンプレ

## 変更履歴

| Version | Date       | Changes                                             |
| ------- | ---------- | --------------------------------------------------- |
| 2.1.0   | 2025-12-31 | 18-skills準拠、Task仕様追加、scripts整備            |
| 2.0.0   | 2025-12-31 | 18-skills.md仕様に完全準拠                           |
| 1.0.0   | 2025-12-24 | 初版作成                                            |
