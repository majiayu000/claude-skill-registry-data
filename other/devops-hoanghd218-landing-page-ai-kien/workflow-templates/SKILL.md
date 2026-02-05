---
name: workflow-templates
description: |
  GitHub Actionsワークフローテンプレートの専門スキル。
  組織標準テンプレート、スターターワークフロー設計を提供します。

  Anchors:
  - Continuous Delivery（Jez Humble）/ 適用: CI/CDパイプライン設計 / 目的: 継続的デリバリー実現
  - GitHub Actions Documentation（GitHub公式）/ 適用: ワークフロー構文 / 目的: 標準準拠
  - GitHub Actions starter-workflows / 適用: テンプレートベース / 目的: ベストプラクティス適用

  Trigger:
  ワークフローテンプレート選定時、CIパイプライン構築時、CDパイプライン構築時、ワークフロー最適化時に使用

allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Workflow Templates

## 概要

GitHub Actions ワークフローテンプレートの選択、カスタマイズ、生成に関する包括的なスキル。4つの専門エージェントによる体系的なワークフロー構築を提供します。

## エージェント構成

| エージェント       | 役割               | 主な機能                                               |
| ------------------ | ------------------ | ------------------------------------------------------ |
| template-selector  | テンプレート選定   | プロジェクト分析、テンプレート推奨、カスタマイズガイド |
| ci-builder         | CIパイプライン構築 | Lint/Test/Build ジョブ設計、キャッシュ戦略             |
| cd-builder         | CDパイプライン構築 | マルチ環境デプロイ、承認フロー、ロールバック           |
| workflow-optimizer | ワークフロー最適化 | キャッシュ最適化、並列実行、条件付き実行               |

## ワークフロー

### Phase 1: 要件分析とテンプレート選定

**目的**: プロジェクト要件を分析し、最適なテンプレートを選定

**アクション**:

1. `template-selector` でプロジェクトタイプを分析
2. `references/project-type-selection.md` に基づくテンプレート選定
3. カスタマイズポイントの特定

### Phase 2: パイプライン構築

**目的**: CI/CDパイプラインの実装

**アクション**:

1. `ci-builder` でCIパイプラインを構築
2. `cd-builder` でCDパイプラインを構築
3. 環境別設定とシークレット管理

### Phase 3: 最適化と検証

**目的**: パフォーマンス最適化と動作確認

**アクション**:

1. `workflow-optimizer` でキャッシュ・並列実行を最適化
2. `scripts/validate-skill.mjs` でスキル構造検証
3. `scripts/log_usage.mjs` で使用記録

## Task仕様ナビ

| タスク             | 担当エージェント   | 参照リソース                  |
| ------------------ | ------------------ | ----------------------------- |
| テンプレート選定   | template-selector  | `project-type-selection.md`   |
| CIパイプライン構築 | ci-builder         | `assets/ci-template.yaml`     |
| CDパイプライン構築 | cd-builder         | `assets/cd-template.yaml`     |
| Node.js環境構築    | ci-builder         | `assets/nodejs-template.yaml` |
| Dockerビルド       | cd-builder         | `assets/docker-template.yaml` |
| キャッシュ最適化   | workflow-optimizer | `template-types.md`           |

## ベストプラクティス

### すべきこと

- `template-selector` でプロジェクト要件を分析してから開始する
- 最小限のテンプレートから始めて段階的に拡張する
- キャッシュ戦略を早期に設計する
- マルチ環境では環境保護ルールを設定する
- 定期的に `workflow-optimizer` でパフォーマンスを確認する

### 避けるべきこと

- 要件分析なしのテンプレート選択
- キャッシュなしでの大規模依存関係インストール
- 本番環境への承認フローなしのデプロイ
- 過度に複雑なワークフロー設計

## リソース参照

### エージェント

| エージェント                   | 説明                       |
| ------------------------------ | -------------------------- |
| `agents/template-selector.md`  | テンプレート選定の詳細仕様 |
| `agents/ci-builder.md`         | CIパイプライン構築         |
| `agents/cd-builder.md`         | CDパイプライン構築         |
| `agents/workflow-optimizer.md` | ワークフロー最適化         |

### リファレンス

| リソース                               | 説明                     |
| -------------------------------------- | ------------------------ |
| `references/project-type-selection.md` | プロジェクトタイプ別選定 |
| `references/template-types.md`         | テンプレートタイプ詳細   |

### テンプレート

| テンプレート                  | 説明           |
| ----------------------------- | -------------- |
| `assets/ci-template.yaml`     | CIパイプライン |
| `assets/cd-template.yaml`     | CDパイプライン |
| `assets/docker-template.yaml` | Dockerビルド   |
| `assets/nodejs-template.yaml` | Node.js環境    |

### スクリプト

| スクリプト                   | 説明           | 使用方法                             |
| ---------------------------- | -------------- | ------------------------------------ |
| `scripts/validate-skill.mjs` | スキル構造検証 | `node scripts/validate-skill.mjs -v` |
| `scripts/log_usage.mjs`      | 使用記録       | `node scripts/log_usage.mjs`         |

## 変更履歴

| バージョン | 日付       | 変更内容                                      |
| ---------- | ---------- | --------------------------------------------- |
| 2.0.0      | 2026-01-01 | 4エージェント体制への再構成、18-skills.md準拠 |
| 1.1.0      | 2025-12-31 | Task仕様ナビテーブル追加、日本語記述統一      |
| 1.0.0      | 2025-12-24 | 初版リリース                                  |
