---
name: git-hooks-concepts
description: |
  Git Hooksの基本概念、ライフサイクル、実装パターンを提供し、コミット前のコード品質チェックとプッシュ前のテスト自動化を実現するスキル。

  Anchors:
  • Pro Git (Scott Chacon) / 適用: Git Hooksのライフサイクル理解 / 目的: クライアント/サーバー側フックの適切な選択
  • Continuous Delivery (Jez Humble) / 適用: 自動化パイプライン設計 / 目的: 品質ゲートの段階的実装

  Trigger:
  Use when implementing Git hooks for pre-commit code quality checks, pre-push test execution, or commit message validation.
  pre-commit, pre-push, git hooks, husky, lint-staged, conventional commits
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Task
---

# Git Hooks Concepts

## 概要

Git Hooksの基本概念、ライフサイクル、実装パターンを提供するスキル。クライアント側フック（pre-commit、pre-push）の設計・実装・検証を支援し、コード品質チェックとテスト自動化を実現する。

**適用範囲**: Git管理下のプロジェクト全般（Node.js、Python、Go等）

## ワークフロー

### Phase 1: 要件確認

**目的**: フックの目的と検証項目を明確にする

**アクション**:

1. フックの目的を特定（コード品質、テスト、コミットメッセージ検証など）
2. [references/hook-types-reference.md](references/hook-types-reference.md) でフック種類を確認
3. 対象ファイルタイプと検証ツールを決定

**Task**: `agents/confirm-requirements.md` を参照

### Phase 2: フック実装

**目的**: 選択したフックを実装する

**アクション**:

1. [references/implementation-patterns.md](references/implementation-patterns.md) から適切なパターンを選択
2. [assets/](assets/) のテンプレートをカスタマイズ
3. `.git/hooks/` または `.husky/` にスクリプトを配置

**Task**: `agents/implement-hook.md` を参照

### Phase 3: 検証と記録

**目的**: フックの動作を確認し、記録する

**アクション**:

1. `scripts/validate-git-hooks.mjs` でフック設定を検証
2. 実際にコミット/プッシュしてフックが発火することを確認
3. `scripts/log_usage.mjs` で使用実績を記録

**Task**: `agents/validate-and-log.md` を参照

## Task仕様（ナビゲーション）

| Task                 | 起動タイミング | 入力             | 出力               |
| -------------------- | -------------- | ---------------- | ------------------ |
| confirm-requirements | Phase 1        | フック要件       | 検証項目リスト     |
| implement-hook       | Phase 2        | 検証項目リスト   | フックスクリプト   |
| validate-and-log     | Phase 3        | フックスクリプト | 検証結果、使用記録 |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリの対応ファイルを参照

## ベストプラクティス

### すべきこと

- pre-commitは軽いチェック（1秒以内）、pre-pushで重いテスト実行
- 明確なエラーメッセージで修正方法を提示
- 段階的な検証（軽い→重い順序で実行）
- Task実行前に該当する `agents/*.md` を読み、入出力を確認する
- Phase完了後に `scripts/log_usage.mjs` で記録を残す

### 避けるべきこと

- pre-commitに重いテスト（ユーザーがスキップするようになる）
- フックの重複実装（pre-commitとpre-pushで同じ検証）
- `--no-verify` の日常的な使用（フックの意味がなくなる）
- エラー時の修正方法を提示しない

**詳細**: See [references/implementation-patterns.md](references/implementation-patterns.md) → ベストプラクティス

## リソース参照

### references/（知識外部化）

| リソース     | パス                                                                           | 内容                            |
| ------------ | ------------------------------------------------------------------------------ | ------------------------------- |
| フック種類   | [references/hook-types-reference.md](references/hook-types-reference.md)       | pre-commit/pre-push等の詳細仕様 |
| 実装パターン | [references/implementation-patterns.md](references/implementation-patterns.md) | 10種類の実装パターン集          |

### scripts/（決定論的処理）

| スクリプト               | 用途               | 使用例                                        |
| ------------------------ | ------------------ | --------------------------------------------- |
| `validate-git-hooks.mjs` | フック設定の検証   | `node scripts/validate-git-hooks.mjs`         |
| `log_usage.mjs`          | フィードバック記録 | `node scripts/log_usage.mjs --result success` |
| `validate-skill.mjs`     | 構造検証           | `node scripts/validate-skill.mjs`             |

### assets/（テンプレート）

| テンプレート             | 用途                 |
| ------------------------ | -------------------- |
| `pre-commit-template.sh` | pre-commitフック雛形 |
| `pre-push-template.sh`   | pre-pushフック雛形   |

## フック実行順序

```
git commit
  ↓
1. pre-commit（ステージ済みファイルチェック）
  ↓
2. prepare-commit-msg（メッセージテンプレート）
  ↓
[ユーザーがメッセージ編集]
  ↓
3. commit-msg（メッセージフォーマット検証）
  ↓
[コミット作成]
  ↓
4. post-commit（通知）

git push
  ↓
pre-push（テスト・ビルド確認）
  ↓
[サーバー側フック]
```

**詳細**: See [references/hook-types-reference.md](references/hook-types-reference.md)

## パフォーマンス目標

| フック     | 推奨実行時間 | 検証内容例                 |
| ---------- | ------------ | -------------------------- |
| pre-commit | < 1秒        | Prettier、ESLint           |
| commit-msg | < 0.5秒      | Conventional Commits検証   |
| pre-push   | < 30秒       | テスト、ビルド、型チェック |

## 変更履歴

| Version | Date       | Changes                                 |
| ------- | ---------- | --------------------------------------- |
| 2.1.0   | 2026-01-02 | references/を整理、18-skills.md仕様準拠 |
| 2.0.0   | 2025-12-31 | 18-skills.md仕様に準拠                  |
| 1.0.0   | 2025-12-24 | 初版作成                                |
