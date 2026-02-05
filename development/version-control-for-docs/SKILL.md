---
name: version-control-for-docs
description: |
  Gitを活用したドキュメントのバージョン管理と変更履歴管理の専門スキル。
  ブランチ戦略、コミット規約、Changelog生成、PRレビューを提供します。

  Anchors:
  - Pro Git（Scott Chacon）/ 適用: ブランチ戦略・履歴管理 / 目的: Gitベストプラクティス
  - Conventional Commits / 適用: コミットメッセージ規約 / 目的: 自動化可能なコミット
  - Keep a Changelog / 適用: Changelog形式 / 目的: 人間が読みやすい変更履歴

  Trigger:
  Use when managing document versions with Git, designing branch strategies, generating changelogs, or preparing PR reviews for documentation.

allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Version Control for Docs

## 概要

Gitを活用したドキュメントのバージョン管理と変更履歴管理の専門スキル。4つの専門エージェントによる包括的なドキュメント管理ワークフローを提供します。

## エージェント構成

| エージェント         | 役割                   | 主な機能                               |
| -------------------- | ---------------------- | -------------------------------------- |
| branch-strategy      | ブランチ戦略設計       | モデル選択、命名規則、マージ戦略       |
| commit-message       | コミットメッセージ規約 | Conventional Commits、prefix設計       |
| changelog-generation | Changelog生成          | 自動生成、フォーマット、バージョニング |
| pr-review            | PRレビュー準備         | テンプレート、チェックリスト           |

## ワークフロー

### Phase 1: 戦略策定

**目的**: ドキュメント管理のブランチ戦略とコミット規約を決定

**アクション**:

1. `branch-strategy` でブランチモデルを選択
2. `commit-message` でコミット規約を策定
3. チーム規模・更新頻度に応じた戦略調整

### Phase 2: 実装と運用

**目的**: 策定した戦略に基づいてドキュメント管理を実施

**アクション**:

1. ブランチ作成・コミット・マージを実施
2. `changelog-generation` でChangelog自動生成
3. `pr-review` でPRテンプレート・チェックリスト適用

### Phase 3: 検証と改善

**目的**: 運用結果を検証し継続的に改善

**アクション**:

1. `scripts/validate-skill.mjs` で構造検証
2. `scripts/generate-changelog.mjs` でChangelog生成
3. `scripts/log_usage.mjs` で使用記録

## Task仕様ナビ

| タスク             | 担当エージェント     | 参照リソース              |
| ------------------ | -------------------- | ------------------------- |
| ブランチモデル選択 | branch-strategy      | `branch-strategy.md`      |
| コミット規約策定   | commit-message       | `commit-conventions.md`   |
| Changelog自動生成  | changelog-generation | `changelog-generation.md` |
| PRテンプレート作成 | pr-review            | `review-workflow.md`      |
| Git差分確認        | -                    | `git-diff-guide.md`       |

## ベストプラクティス

### すべきこと

- **Conventional Commits**形式でコミットメッセージを記述する
- ドキュメント変更は必ず**ブランチを作成**してから実施
- PRには必ず**レビューチェックリスト**を添付
- `scripts/generate-changelog.mjs` でChangelog自動生成

### 避けるべきこと

- main/masterブランチへの直接コミット
- コミットメッセージにprefixを付けない
- Changelogを手動で更新する（自動化推奨）
- レビューなしでマージする

## リソース参照

### エージェント

| エージェント                     | 説明                   |
| -------------------------------- | ---------------------- |
| `agents/branch-strategy.md`      | ブランチ戦略設計       |
| `agents/commit-message.md`       | コミットメッセージ規約 |
| `agents/changelog-generation.md` | Changelog生成          |
| `agents/pr-review.md`            | PRレビュー準備         |

### リファレンス

| リソース                             | 説明                 |
| ------------------------------------ | -------------------- |
| `references/branch-strategy.md`      | ブランチ戦略詳細     |
| `references/commit-conventions.md`   | コミット規約詳細     |
| `references/changelog-generation.md` | Changelog生成ガイド  |
| `references/review-workflow.md`      | レビューワークフロー |
| `references/git-diff-guide.md`       | Git差分確認ガイド    |

### アセット

| アセット                       | 説明                  |
| ------------------------------ | --------------------- |
| `assets/changelog-template.md` | Changelogテンプレート |
| `assets/pr-template.md`        | PRテンプレート        |

### スクリプト

| スクリプト                       | 説明           | 使用方法                                     |
| -------------------------------- | -------------- | -------------------------------------------- |
| `scripts/generate-changelog.mjs` | Changelog生成  | `node scripts/generate-changelog.mjs --help` |
| `scripts/validate-skill.mjs`     | スキル構造検証 | `node scripts/validate-skill.mjs -v`         |
| `scripts/log_usage.mjs`          | 使用記録       | `node scripts/log_usage.mjs`                 |

## 変更履歴

| バージョン | 日付       | 変更内容                             |
| ---------- | ---------- | ------------------------------------ |
| 2.0.0      | 2026-01-01 | 18-skills.md仕様完全準拠、構造最適化 |
| 1.0.0      | 2025-12-24 | 初版リリース                         |
