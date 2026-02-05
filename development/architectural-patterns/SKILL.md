---
name: architectural-patterns
description: |
  アーキテクチャパターン（Hexagonal、Onion、Vertical Sliceなど）の選定・比較・適用と、依存関係の準拠評価を支援するスキル。
  境界設計、レイヤー責務、移行計画を整理し、設計判断の根拠と実装の一貫性を保ちます。

  Anchors:
  • Patterns of Enterprise Application Architecture / 適用: パターン比較と選定 / 目的: トレードオフを整理する
  • Domain-Driven Design / 適用: ドメイン中心設計 / 目的: 境界と責務の明確化
  • Clean Architecture / 適用: 依存関係ルール / 目的: レイヤーの一方向性を維持

  Trigger:
  Use when selecting architecture patterns, designing system boundaries, comparing Hexagonal/Onion/Vertical Slice approaches, or evaluating dependency compliance in a codebase.
allowed-tools:
  - bash
  - node
---

# Architectural Patterns

## 概要

アーキテクチャパターンの選定・比較・適用・検証を一連で整理する。
必要な詳細は `references/` に外部化し、必要なときだけ参照する。

- 比較レポートは `assets/pattern-comparison.md` を使用
- 実装準拠の評価は `scripts/evaluate-pattern-compliance.mjs` を使用

## ワークフロー

### Phase 1: コンテキスト整理

**目的**: 対象システムの目的・制約・現状を把握する

**アクション**:

1. `references/Level1_basics.md` で基礎概念を確認
2. `references/requirements-index.md` で適用ルールを確認
3. 現状構造と制約を整理する

**Task**: `agents/analyze-context.md`

### Phase 2: パターン選定と境界設計

**目的**: パターン比較と境界設計を行い、採用方針を固める

**アクション**:

1. `assets/pattern-comparison.md` に比較結果を整理
2. 必要に応じて `references/hexagonal-architecture.md` などを参照
3. 境界設計と依存方向のルールを決める

**Task**:
- `agents/pattern-selection.md`
- `agents/boundary-design.md`

### Phase 3: 準拠評価と記録

**目的**: 実装が設計意図に沿っているか検証し、改善点を記録する

**アクション**:

1. `scripts/evaluate-pattern-compliance.mjs` で依存違反を確認
2. `scripts/validate-skill.mjs` でスキル構造を検証
3. `scripts/log_usage.mjs` でフィードバックを記録

**Task**: `agents/compliance-review.md`

## Task仕様ナビ

| Task | 役割 | 入力 | 出力 | 参照先 | 実行タイミング |
| --- | --- | --- | --- | --- | --- |
| コンテキスト分析 | 目的・制約の整理 | 現状構造、制約 | コンテキスト要約 | `references/requirements-index.md` | Phase 1 |
| パターン選定 | パターン比較と選定 | コンテキスト要約 | パターン比較レポート | `assets/pattern-comparison.md` | Phase 2 前半 |
| 境界設計 | 境界と依存方向の設計 | パターン比較レポート | 境界設計メモ | `references/hexagonal-architecture.md` | Phase 2 後半 |
| 準拠レビュー | 実装準拠と改善点整理 | 対象コード | 準拠評価レポート | `scripts/evaluate-pattern-compliance.mjs` | Phase 3 |

## ベストプラクティス

### すべきこと

- 目的と制約を先に整理してからパターンを選定する
- 境界設計は依存方向と責務の範囲で定義する
- 既存コードの依存違反を定量的に確認する
- パターン選定の理由を記録し、後続判断の根拠にする
- 移行計画とリスクを比較レポートに含める

### 避けるべきこと

- 目的や制約を無視してパターンを先に決める
- 依存方向のルールを曖昧にする
- パターンの用語を混在させて境界が曖昧になる
- 準拠評価なしで移行を進める

## リソース参照

### 参照資料

- `references/Level1_basics.md`: 基本概念と最小チェック
- `references/Level2_intermediate.md`: パターン選定と比較の実務
- `references/Level3_advanced.md`: 移行・検証と段階適用
- `references/Level4_expert.md`: 複合パターンと運用最適化
- `references/hexagonal-architecture.md`: Ports and Adaptersの詳細
- `references/onion-architecture.md`: Onion Architectureの詳細
- `references/vertical-slice.md`: Vertical Sliceの詳細
- `references/requirements-index.md`: 適用ルール索引
- `references/legacy-skill.md`: 旧版の要約（移行時のみ参照）

### スクリプト

- `scripts/evaluate-pattern-compliance.mjs`: 依存関係の準拠評価
- `scripts/validate-skill.mjs`: スキル構造検証
- `scripts/log_usage.mjs`: 実行ログ記録

### テンプレート

- `assets/pattern-comparison.md`: パターン比較レポート

## 変更履歴

| Version | Date       | Changes                                              |
| ------- | ---------- | ---------------------------------------------------- |
| 2.0.0   | 2025-12-31 | 18-skills.md準拠、Task仕様追加、scripts/assets整備 |
| 1.0.0   | 2025-12-24 | 初版作成                                             |
