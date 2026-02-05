---
name: headless-ui-principles
description: |
  ヘッドレスUIアーキテクチャとスタイル非依存コンポーネント設計の専門知識。Radix UI、Headless UI、React Aria等を活用し、アクセシビリティを確保しながら完全なスタイル制御を実現。

  Anchors:
  • Don't Make Me Think (Steve Krug) / 適用: シンプルで直感的なUI設計 / 目的: ユーザビリティ最適化
  • Inclusive Components (Heydon Pickering) / 適用: アクセシビリティ駆動設計 / 目的: WCAG準拠コンポーネント実装
  • Atomic Design (Brad Frost) / 適用: コンポーネント階層設計 / 目的: 再利用可能な設計システム構築

  Trigger:
  Use when implementing headless UI components, building accessible custom components, selecting UI libraries, or designing component architecture with full style control.
  headless ui, radix ui, react aria, accessibility, wcag, aria patterns, compound components, render props, style-agnostic
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Headless UI Principles

## 概要

ヘッドレスUIは、ロジックとUIの表現を完全に分離するアーキテクチャパターン。
Radix UI、Headless UI、React Ariaなどを活用し、アクセシビリティを確保しながら完全なスタイル制御を実現する。

## ワークフロー

### Phase 1: 要件分析と設計方針決定

**目的**: ヘッドレスUI導入の適切性を判断し、アーキテクチャ方針を確定

**アクション**:

1. コンポーネントの機能要件を整理
2. アクセシビリティ要件（WCAGレベル）を確認
3. `references/library-comparison.md` でライブラリを比較選定
4. `references/aria-patterns.md` で必要なWAI-ARIAパターンを特定

**Task**: `agents/analyze-requirements.md` を参照

### Phase 2: コンポーネント実装

**目的**: ヘッドレスUI原則に従ってコンポーネントを実装

**アクション**:

1. `assets/headless-component-template.tsx` を基にコンポーネント設計
2. `assets/headless-hook-template.ts` で状態管理ロジックを抽出
3. WAI-ARIAパターンに基づきロール・属性を設定
4. キーボード操作とフォーカス管理を実装

**Task**: `agents/implement-component.md` を参照

### Phase 3: アクセシビリティ検証

**目的**: WCAG準拠を確認し、品質を保証

**アクション**:

1. `scripts/check-a11y.mjs` で自動検証
2. キーボード操作のみでのナビゲーション確認
3. スクリーンリーダーでの読み上げテスト
4. `scripts/log_usage.mjs` で使用記録

**Task**: `agents/verify-accessibility.md` を参照

## Task仕様ナビ

| Task                 | 起動タイミング | 入力               | 出力                   |
| -------------------- | -------------- | ------------------ | ---------------------- |
| analyze-requirements | Phase 1開始時  | コンポーネント要件 | 設計方針書             |
| implement-component  | Phase 2開始時  | 設計方針書         | 実装済みコンポーネント |
| verify-accessibility | Phase 3開始時  | 実装コード         | 検証レポート           |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリの対応ファイルを参照

## ベストプラクティス

### すべきこと

- ロジックと表現を完全に分離（カスタムフック/コンテキスト活用）
- WAI-ARIAパターンに準拠したロール・属性設定
- キーボード操作をすべての機能で実装
- フォーカスインジケータを常に可視化
- TypeScript型定義で型安全性を確保
- スタイルはAPI経由で完全に制御可能に

### 避けるべきこと

- ライブラリのデフォルトスタイルをそのまま使用
- 比較検討なしのライブラリ選定
- アクセシビリティの後付け実装
- キーボード操作不可の機能
- スクリーンリーダー未対応

## リソース参照

### references/（詳細知識）

| リソース       | パス                                                                           | 内容                    |
| -------------- | ------------------------------------------------------------------------------ | ----------------------- |
| 基礎知識       | See [references/Level1_basics.md](references/Level1_basics.md)                 | 基本概念・設計原則      |
| 中級知識       | See [references/Level2_intermediate.md](references/Level2_intermediate.md)     | 実装パターン            |
| 上級知識       | See [references/Level3_advanced.md](references/Level3_advanced.md)             | 高度な最適化            |
| 専門家向け     | See [references/Level4_expert.md](references/Level4_expert.md)                 | デザインシステム構築    |
| ARIAパターン   | See [references/aria-patterns.md](references/aria-patterns.md)                 | WAI-ARIAパターン集      |
| アーキテクチャ | See [references/headless-architecture.md](references/headless-architecture.md) | ヘッドレス設計原則      |
| ライブラリ比較 | See [references/library-comparison.md](references/library-comparison.md)       | Radix/Headless/Aria比較 |

### scripts/（決定論的処理）

| スクリプト           | 用途                 | 使用例                                          |
| -------------------- | -------------------- | ----------------------------------------------- |
| `check-a11y.mjs`     | アクセシビリティ検証 | `node scripts/check-a11y.mjs src/Component.tsx` |
| `validate-skill.mjs` | スキル構造検証       | `node scripts/validate-skill.mjs`               |
| `log_usage.mjs`      | フィードバック記録   | `node scripts/log_usage.mjs --result success`   |

### assets/（テンプレート）

| テンプレート                      | 用途                           |
| --------------------------------- | ------------------------------ |
| `headless-component-template.tsx` | コンポーネント実装テンプレート |
| `headless-hook-template.ts`       | カスタムフックテンプレート     |

## 変更履歴

| Version | Date       | Changes                                     |
| ------- | ---------- | ------------------------------------------- |
| 2.1.0   | 2026-01-02 | 18-skills.md完全準拠、agents/追加、形式統一 |
| 2.0.0   | 2025-12-31 | Task仕様ナビ、Trigger/Anchors追加           |
| 1.0.0   | 2025-12-24 | 初版                                        |
