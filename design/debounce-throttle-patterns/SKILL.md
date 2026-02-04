---
name: debounce-throttle-patterns
description: |
  高頻度イベントに対するデバウンス/スロットリングの設計・実装・検証を整理するスキル。
  UIイベントやファイル監視の負荷を最適化し、応答性と安定性を両立する。

  Anchors:
  • Debounce Pattern / 適用: 連続入力の抑制 / 目的: 不要な処理の削減
  • Throttle Pattern / 適用: 定期的な処理制御 / 目的: リソース負荷の平準化
  • Web Performance Patterns / 適用: UIイベント最適化 / 目的: UX改善

  Trigger:
  Use when optimizing high-frequency events, selecting debounce/throttle strategies, tuning delay intervals, or validating performance impacts.
  debounce, throttle, event optimization, scroll resize, input performance
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---
# debounce-throttle-patterns

## 概要

高頻度イベントの最適化に必要な要件整理、パターン選択、実装、検証を支援する。

## ワークフロー

### Phase 1: 要件整理

**目的**: イベントの種類と制約を整理し、最適化対象を明確にする。

**アクション**:

1. `references/Level1_basics.md` で基本概念を確認する。
2. `assets/pattern-selection-checklist.md` で要件を整理する。
3. `references/requirements-index.md` で要件整合を確認する。

**Task**: `agents/analyze-event-requirements.md` を参照

### Phase 2: パターン設計

**目的**: デバウンス/スロットリングの選定とパラメータ設計を行う。

**アクション**:

1. `references/implementation-patterns.md` でパターンを比較する。
2. 待機時間/間隔を設計し、判断根拠を記録する。
3. `assets/debounce-throttle.ts` で実装方針を確認する。

**Task**: `agents/design-pattern-strategy.md` を参照

### Phase 3: 実装

**目的**: 選定したパターンを実装し、影響範囲を記録する。

**アクション**:

1. `assets/debounce-throttle.ts` をベースに実装する。
2. 変更点と影響範囲を整理する。

**Task**: `agents/implement-patterns.md` を参照

### Phase 4: 検証と運用

**目的**: パフォーマンス影響を検証し、改善記録を残す。

**アクション**:

1. `assets/performance-measurement-template.md` で測定結果を整理する。
2. `agents/validate-pattern-performance.md` の観点で評価する。
3. `scripts/log_usage.mjs` で記録を更新する。

**Task**: `agents/validate-pattern-performance.md` を参照

## Task仕様ナビ

| Task | 起動タイミング | 入力 | 出力 |
| --- | --- | --- | --- |
| analyze-event-requirements | Phase 1開始時 | イベント情報 | 要件メモ、制約一覧 |
| design-pattern-strategy | Phase 2開始時 | 要件メモ | パターン設計、パラメータ案 |
| implement-patterns | Phase 3開始時 | 設計メモ | 実装差分、影響範囲 |
| validate-pattern-performance | Phase 4開始時 | 実装差分 | 検証レポート、改善提案 |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

## ベストプラクティス

### すべきこと

| 推奨事項 | 理由 |
| --- | --- |
| イベントの目的を先に整理する | パターン選定が明確になる |
| パラメータ根拠を記録する | 再調整が容易になる |
| 実装後に測定する | 期待効果を確認できる |
| 影響範囲を明示する | 回帰を防止できる |

### 避けるべきこと

| 禁止事項 | 問題点 |
| --- | --- |
| 一律でパターン適用 | UX劣化を招く |
| 根拠なしの間隔設定 | 調整できない |
| 測定を省略する | 効果が不明になる |
| 記録を残さない | 改善が継続できない |

## リソース参照

### scripts/（決定論的処理）

| スクリプト | 機能 |
| --- | --- |
| `scripts/validate-skill.mjs` | スキル構造検証 |
| `scripts/log_usage.mjs` | 使用記録と評価メトリクス更新 |

### references/（詳細知識）

| リソース | パス | 読込条件 |
| --- | --- | --- |
| レベル1 基礎 | [references/Level1_basics.md](references/Level1_basics.md) | 要件整理時 |
| レベル2 実務 | [references/Level2_intermediate.md](references/Level2_intermediate.md) | 設計時 |
| レベル3 応用 | [references/Level3_advanced.md](references/Level3_advanced.md) | 実装時 |
| レベル4 専門 | [references/Level4_expert.md](references/Level4_expert.md) | 検証時 |
| 実装パターン | [references/implementation-patterns.md](references/implementation-patterns.md) | 設計時 |
| 要求仕様索引 | [references/requirements-index.md](references/requirements-index.md) | 仕様確認時 |
| 旧スキル | [references/legacy-skill.md](references/legacy-skill.md) | 互換確認時 |

### assets/（テンプレート・素材）

| アセット | 用途 |
| --- | --- |
| `assets/debounce-throttle.ts` | 実装テンプレート |
| `assets/pattern-selection-checklist.md` | パターン選定チェックリスト |
| `assets/performance-measurement-template.md` | 測定テンプレート |

### 運用ファイル

| ファイル | 目的 |
| --- | --- |
| `EVALS.json` | レベル評価・メトリクス管理 |
| `LOGS.md` | 実行ログの蓄積 |
| `CHANGELOG.md` | 改善履歴の記録 |
