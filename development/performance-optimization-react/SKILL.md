---
name: performance-optimization-react
description: |
  Reactアプリケーションのパフォーマンス最適化を体系的に実施するスキル。測定駆動の最適化アプローチで、不要な再レンダリングを削減し、ユーザー体験を向上させる。

  Anchors:
  • High Performance Browser Networking (Ilya Grigorik) / 適用: パフォーマンス測定手法 / 目的: データに基づいた最適化判断
  • React公式ドキュメント (Dan Abramov) / 適用: React.memo・useCallback・useMemo / 目的: 測定駆動の最適化実践
  • Clean Code (Robert C. Martin) / 適用: 早すぎる最適化を避ける原則 / 目的: 必要な最適化のみ実施

  Trigger:
  Use when optimizing React performance, reducing re-renders, applying React.memo, analyzing with React DevTools Profiler, implementing Context splitting, or diagnosing rendering performance issues.
  performance optimization, React performance, re-rendering, React.memo, useCallback, useMemo, profiler

allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# Performance Optimization React

## 概要

Reactアプリケーションのパフォーマンス最適化を体系的に実施するスキル。測定→分析→最適化→検証のサイクルで、データに基づいた最適化判断を行い、不要な再レンダリングを削減する。

## ワークフロー

### Phase 1: パフォーマンス測定・分析

**目的**: React DevTools Profilerで測定し、ボトルネックを特定する

**アクション**:

1. React DevTools Profilerをインストール・設定
2. 最適化前のベースライン測定を実施
3. レンダリング時間・再レンダリング回数を記録
4. ボトルネックコンポーネントを特定
5. 再レンダリングの原因を分析（親の更新/Context変更/Props変更/状態更新）
6. 最適化優先度を決定（レンダリング時間・頻度に基づく）

**Task**: `agents/analyze-performance.md` を参照

### Phase 2: 最適化戦略の実装

**目的**: 適切な最適化手法を選択・実装する

**アクション**:

1. 原因に応じた最適化手法を選択
   - React.memo: 親の再レンダリング対策
   - useCallback: コールバックProps安定化
   - useMemo: 計算コスト削減
   - Context分割: Context更新の影響範囲縮小
2. `assets/optimization-checklist.md` で実装計画を立案
3. 測定に基づいて優先度の高いコンポーネントから実装
4. 依存配列を正確に設定（ESLint exhaustive-depsルール準拠）
5. TypeScript型チェックを維持

**Task**: `agents/optimize-rendering.md` を参照

### Phase 3: 効果測定・検証

**目的**: 最適化の効果を測定し、品質を保証する

**アクション**:

1. 最適化後の測定を実施（最適化前と同じ操作で比較）
2. 改善率を計算（目標: レンダリング時間50%削減、再レンダリング回数70%削減）
3. 副作用や新しい問題がないか確認
4. 測定結果をドキュメント化
5. コードレビュー・品質保証を実施
6. `assets/optimization-checklist.md` で最終確認

**Task**: `agents/validate-improvements.md` を参照

## Task仕様ナビ

| Task                  | 起動タイミング | 入力               | 出力                   |
| --------------------- | -------------- | ------------------ | ---------------------- |
| analyze-performance   | Phase 1開始時  | 対象コンポーネント | ボトルネック分析結果   |
| optimize-rendering    | Phase 2開始時  | 分析結果           | 最適化実装コード       |
| validate-improvements | Phase 3開始時  | 最適化実装コード   | 効果測定結果・品質保証 |

## ベストプラクティス

### すべきこと

- 必ずReact DevTools Profilerで測定してから最適化する
- 最適化前後のデータを記録し、改善率を計算する
- React.memoは測定で問題が確認された場合のみ適用する
- useCallback/useMemoの依存配列はESLint exhaustive-depsルールに準拠させる
- レンダリング時間100ms以上のコンポーネントを優先的に最適化する
- Context分割は10個以上のコンポーネントで使用される場合に検討する
- 最適化後に副作用や新しい問題がないか必ず確認する

### 避けるべきこと

- 測定せずに「遅そうだから」という理由で最適化する（早すぎる最適化）
- すべてのコンポーネントにReact.memoを適用する
- useCallback/useMemoの依存配列を空にして警告を無視する
- @ts-ignoreや@ts-expect-errorで型エラーを隠蔽する
- 最適化後の測定を省略する
- Context分割を過度に行い、かえって複雑化させる
- 本番環境でのテストを省略する

## リソース参照

### references/（詳細知識）

| リソース       | パス                                                                           | 用途                          |
| -------------- | ------------------------------------------------------------------------------ | ----------------------------- |
| 基礎レベル     | See [references/Level1_basics.md](references/Level1_basics.md)                 | パフォーマンス最適化の基礎    |
| 中級レベル     | See [references/Level2_intermediate.md](references/Level2_intermediate.md)     | 中級最適化テクニック          |
| 上級レベル     | See [references/Level3_advanced.md](references/Level3_advanced.md)             | 上級最適化パターン            |
| エキスパート   | See [references/Level4_expert.md](references/Level4_expert.md)                 | エキスパート最適化戦略        |
| Profiler測定   | See [references/profiler-measurement.md](references/profiler-measurement.md)   | React DevTools Profiler使い方 |
| 再レンダリング | See [references/re-rendering-patterns.md](references/re-rendering-patterns.md) | 再レンダリングの4つの原因     |
| React.memo     | See [references/react-memo-guide.md](references/react-memo-guide.md)           | React.memo活用ガイド          |
| Context分割    | See [references/context-splitting.md](references/context-splitting.md)         | Context分割戦略               |

### scripts/（決定論的処理）

| スクリプト           | 用途               | 使用例                                                          |
| -------------------- | ------------------ | --------------------------------------------------------------- |
| `validate-skill.mjs` | スキル構造検証     | `node scripts/validate-skill.mjs`                               |
| `log_usage.mjs`      | 使用記録・自動評価 | `node scripts/log_usage.mjs --result success --phase "Phase 3"` |

### assets/（テンプレート）

| テンプレート                | 用途                         |
| --------------------------- | ---------------------------- |
| `optimization-checklist.md` | 最適化プロセスチェックリスト |

## 変更履歴

詳細な変更履歴は `CHANGELOG.md` を参照してください。
