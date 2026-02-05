---
name: notification-integration-gha
description: |
  GitHub Actions通知統合スキル。Slack、Discord、MS Teams、Emailへの
  ビルド/デプロイ状態通知を自動化。成功/失敗メッセージのカスタマイズと
  インタラクティブ要素をサポート。

  Anchors:
  • The Pragmatic Programmer (Hunt and Thomas) / 適用: 自動化とフィードバックループ / 目的: 迅速なフィードバックによる問題早期発見
  • Site Reliability Engineering (Google) / 適用: モニタリングとアラート設計 / 目的: 適切な粒度と重要度の通知
  • GitHub Actions best practices / 適用: ワークフロー設計とシークレット管理 / 目的: セキュアで保守性の高い設定

  Trigger:
  Use when setting up notifications, configuring webhooks, adding Slack/Discord/Teams/Email alerts to workflows, troubleshooting notification failures, or implementing status reporting.
  slack notification, discord webhook, teams alert, github actions notify, workflow status, deployment notification
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# GitHub Actions Notification Integration

## 概要

GitHub Actionsワークフローに通知機能を統合する専門知識を提供。
Slack、Discord、MS Teams、Emailへの自動通知設定をセキュアで保守性の高い方法で実装する。

## ワークフロー

### Phase 1: 要件定義と選択

**目的**: 通知要件を明確化し、適切な通知サービスを選択

**アクション**:

1. 通知先プラットフォームを選択（Slack/Discord/Teams/Email）
2. 通知タイミングを決定（成功時/失敗時/両方）
3. メッセージ内容を設計（シンプル/詳細/インタラクティブ）
4. 適切なTaskを選択

### Phase 2: 実装

**目的**: Webhook/トークン設定とワークフロー定義

**アクション**:

1. GitHub Secretsの設定（Webhook URL、Bot Token等）
2. ワークフロー定義（`assets/notification-workflow.yaml`参照）
3. メッセージフォーマット調整
4. 選択したTaskファイルに従って実装

**Task**: 選択した `agents/*.md` を参照

### Phase 3: テストと検証

**目的**: 通知が正しく動作することを確認

**アクション**:

1. `scripts/test-webhook.mjs` でWebhook URLの有効性確認
2. テストワークフロー実行
3. 通知受信確認
4. エラー時は `agents/troubleshoot.md` を参照

### Phase 4: 記録

**目的**: 実行結果を記録

**アクション**:

```bash
node scripts/log_usage.mjs --result success --phase "Phase 2" --notes "Slack通知を実装"
```

## Task仕様（ナビゲーション）

| Task          | 起動タイミング | 入力       | 出力             |
| ------------- | -------------- | ---------- | ---------------- |
| setup-slack   | Slack統合時    | 通知要件   | ワークフロー定義 |
| setup-discord | Discord統合時  | 通知要件   | ワークフロー定義 |
| setup-teams   | MS Teams統合時 | 通知要件   | ワークフロー定義 |
| troubleshoot  | 通知失敗時     | エラー内容 | 修正手順         |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリの対応ファイルを参照

## ベストプラクティス

### すべきこと

- Secretsを安全に管理（環境変数やリポジトリシークレットを使用）
- メッセージに必須情報を含める（リポジトリ、ブランチ、コミット、作者）
- 成功と失敗で異なるメッセージを送信
- Webhook URLをテストしてから本番適用
- `if: always()` で通知ステップを保護

### 避けるべきこと

- Webhook URLやトークンをハードコード
- すべての通知を同じチャネルに送信
- エラー情報なしで失敗通知を送る
- テスト不十分のまま本番適用
- 機密情報を通知メッセージに含める

## リソース参照

### references/（詳細知識）

| リソース      | パス                                                                   | 用途               |
| ------------- | ---------------------------------------------------------------------- | ------------------ |
| 基礎知識      | See [references/basics.md](references/basics.md)                       | 通知統合の基本概念 |
| Slack統合     | See [references/slack-integration.md](references/slack-integration.md) | Slack詳細設定      |
| Discord/Teams | See [references/discord-teams.md](references/discord-teams.md)         | Discord・Teams設定 |

### scripts/（決定論的処理）

| スクリプト         | 用途               | 使用例                                        |
| ------------------ | ------------------ | --------------------------------------------- |
| `test-webhook.mjs` | Webhook動作確認    | `node scripts/test-webhook.mjs --url <URL>`   |
| `log_usage.mjs`    | フィードバック記録 | `node scripts/log_usage.mjs --result success` |

### assets/（テンプレート）

| テンプレート                 | 用途                         |
| ---------------------------- | ---------------------------- |
| `notification-workflow.yaml` | ワークフロー実装テンプレート |

## 変更履歴

| Version | Date       | Changes                    |
| ------- | ---------- | -------------------------- |
| 2.0.0   | 2026-01-02 | 18-skills.md仕様に完全準拠 |
| 1.1.0   | 2025-12-31 | Task navigation追加        |
| 1.0.0   | 2025-12-24 | 初期バージョン             |
