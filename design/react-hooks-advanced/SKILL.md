---
name: react-hooks-advanced
description: |
  React Hooksの高度な使用パターンと最適化技術を専門とするスキル。
  useEffect依存配列、メモ化戦略、カスタムフック設計、useReducerパターンを提供し、
  予測可能で効率的な状態管理を実現。

  Anchors:
  • React公式ドキュメント（Meta）/ 適用: Hooks設計 / 目的: 公式パターン準拠
  • 『Learning React』（Banks/Porcello）/ 適用: コンポーネント設計 / 目的: 実践的なHooks活用
  • Dan Abramovのブログ / 適用: useEffect思想 / 目的: 依存配列の完全性原則

  Trigger:
  Use when optimizing React hooks, designing custom hooks, implementing useReducer patterns, fixing useEffect dependency issues, or applying memoization strategies.
  react hooks, useEffect, useCallback, useMemo, useReducer, custom hook, dependency array, memoization

allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# React Hooks Advanced

## 概要

React Hooksの高度な使用パターンと最適化技術を専門とするスキル。ダン・アブラモフの思想に基づき、依存配列の完全性原則、測定駆動のメモ化戦略、カスタムフック設計を通じて、予測可能で効率的な状態管理を実現します。

## ワークフロー

### Phase 1: 現状分析

**目的**: 現在のHooks使用状況を分析し問題点を特定する

**アクション**:

1. 対象コンポーネントのHooks使用状況を確認
2. ESLint（react-hooks/exhaustive-deps）警告を確認
3. パフォーマンス問題の有無をReact DevToolsで測定

**Task**: `agents/analyze-hooks.md` を参照

### Phase 2: 依存配列設計

**目的**: useEffect/useCallback/useMemoの依存配列を適切に設計する

**アクション**:

1. 依存配列の完全性原則を適用
2. 古いクロージャ問題の回避パターンを適用
3. 無限ループ発生パターンを排除

**Task**: `agents/design-dependencies.md` を参照

### Phase 3: メモ化戦略

**目的**: 測定に基づいた適切なメモ化を実装する

**アクション**:

1. React.memo、useCallback、useMemoの適用判断
2. Profilerで再レンダリング頻度を測定
3. 実際のパフォーマンス改善を確認

**Task**: `agents/apply-memoization.md` を参照

### Phase 4: カスタムフック設計

**目的**: 再利用可能なカスタムフックを設計する

**アクション**:

1. 抽出すべきロジックを特定
2. 単一責任でカスタムフックを設計
3. テスト可能な形で実装

**Task**: `agents/design-custom-hooks.md` を参照

## Task仕様ナビ

| Task                | 起動タイミング | 入力               | 出力           |
| ------------------- | -------------- | ------------------ | -------------- |
| analyze-hooks       | Phase 1開始時  | 対象コンポーネント | 分析レポート   |
| design-dependencies | Phase 2開始時  | 分析レポート       | 依存配列設計書 |
| apply-memoization   | Phase 3開始時  | パフォーマンス計測 | メモ化実装     |
| design-custom-hooks | Phase 4開始時  | 共通ロジック       | カスタムフック |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

## ベストプラクティス

### すべきこと

| 推奨事項                           | 理由                       |
| ---------------------------------- | -------------------------- |
| ESLint exhaustive-depsルールに従う | 古いクロージャ問題を防止   |
| メモ化は測定してから適用           | 無駄なオーバーヘッドを回避 |
| 複雑な状態にはuseReducerを使用     | 状態遷移の予測可能性向上   |
| カスタムフックで共通ロジックを抽出 | 再利用性と可読性向上       |
| useCallbackの依存配列を最小化      | 不要な再生成を防止         |

### 避けるべきこと

| 禁止事項                       | 問題点                               |
| ------------------------------ | ------------------------------------ |
| 依存配列から値を意図的に除外   | 古いクロージャ、予測不能な動作       |
| 無差別なメモ化                 | メモ化自体がコストになる             |
| useEffect内での無限ループ      | パフォーマンス劣化、クラッシュ       |
| eslint-disable-next-lineの多用 | 本質的な問題を隠蔽                   |
| useRefで依存配列を回避         | 警告を抑制するだけで問題解決にならず |

## リソース参照

### references/（詳細知識）

| リソース         | パス                                                                               | 読込条件       |
| ---------------- | ---------------------------------------------------------------------------------- | -------------- |
| 依存配列パターン | [references/dependency-array-patterns.md](references/dependency-array-patterns.md) | 依存配列設計時 |
| メモ化戦略       | [references/memoization-strategies.md](references/memoization-strategies.md)       | メモ化検討時   |
| useReducer       | [references/use-reducer-patterns.md](references/use-reducer-patterns.md)           | 複雑状態管理時 |
| Hooks選択ガイド  | [references/hooks-selection-guide.md](references/hooks-selection-guide.md)         | Hooks選択時    |

### scripts/（決定論的処理）

| スクリプト                        | 機能                 |
| --------------------------------- | -------------------- |
| `scripts/analyze-hooks-usage.mjs` | Hooks使用状況の分析  |
| `scripts/log_usage.mjs`           | スキル使用履歴の記録 |

### assets/（テンプレート）

| アセット                         | 用途                   |
| -------------------------------- | ---------------------- |
| `assets/custom-hook-template.md` | カスタムフック開発雛形 |
| `assets/use-reducer-template.md` | useReducerパターン雛形 |

## 変更履歴

| Version | Date       | Changes                                    |
| ------- | ---------- | ------------------------------------------ |
| 3.1.0   | 2026-01-02 | agents/追加（4エージェント体制確立）       |
| 3.0.0   | 2026-01-02 | 18-skills.md仕様完全準拠、ワークフロー改善 |
| 1.0.0   | 2025-12-31 | 初版                                       |
