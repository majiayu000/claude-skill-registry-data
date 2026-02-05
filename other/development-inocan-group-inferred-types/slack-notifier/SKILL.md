---
name: slack-notifier
description: |
  Slackチャンネルにフォーマット済みメッセージを送信するSkill。
  「Slackに通知して」「チームに連絡して」「#channelに投稿して」
  などのリクエストで自動発火する。
  MCP連携（フルAPI）とWebhookフォールバック（送信のみ）の両方に対応。
---

# Slack通知 Skill

Slackチャンネルにフォーマット済みメッセージを送信します。
MCP連携とWebhookフォールバックの2つのモードをサポート。

## 連携モード

### モード1: Slack MCP（推奨）
MCP経由でフルSlack APIアクセス。MCP設定が必要。

**利用可能な場合**: `mcp__slack__*` ツールが設定されている
**機能**: メッセージ送信、チャンネル一覧、スレッド返信、リアクション追加

**MCPツール一覧**:
- `mcp__slack__slack_list_channels` - ワークスペースのチャンネル一覧
- `mcp__slack__slack_post_message` - メッセージ投稿
- `mcp__slack__slack_reply_to_thread` - スレッド返信
- `mcp__slack__slack_add_reaction` - リアクション追加

### モード2: Webhook フォールバック
Incoming Webhook経由のシンプルなHTTP POST。MCP不要。

**利用可能な場合**: `SLACK_WEBHOOK_URL` 環境変数が設定されている
**機能**: メッセージ送信のみ（読み取り、リアクションは不可）

## クイックスタート

### 連携モードの確認

送信前に、利用可能な連携方法を確認:
1. MCPを試行: `mcp__slack__slack_list_channels`
2. 利用不可の場合、`SLACK_WEBHOOK_URL` 環境変数を確認
3. 利用可能なモードをユーザーに報告

### シンプルなメッセージ送信

**MCPモード:**
```
mcp__slack__slack_post_message を使用:
  channel: "#channel-name"
  text: "メッセージ内容"
```

**Webhookモード:**
```bash
python3 scripts/send_webhook.py --message "メッセージ内容"
```

## メッセージフォーマット

### 1. シンプルテキスト
プレーンテキスト通知。クイックな更新に。

### 2. フォーマット済み（mrkdwn）
Slackのmarkdown形式。サポート:
- `*太字*` で強調
- `_斜体_` で控えめに
- `` `コード` `` でインラインコード
- ```コードブロック``` で複数行コード
- `<url|テキスト>` でリンク

### 3. 構造化（Blocks）
セクション、ヘッダー、区切り線を使ったリッチレイアウト。
`resources/message-templates.md` にテンプレートあり。

## テンプレート

`resources/message-templates.md` で利用可能:

### アラートテンプレート
- `success`: 緑チェックマーク、成功通知
- `warning`: 黄色警告、注意喚起
- `error`: 赤バツ、失敗通知
- `info`: 青情報マーク、お知らせ

### レポートテンプレート
- `build-report`: ビルドステータスとメトリクス
- `deploy-report`: デプロイサマリー
- `test-report`: テスト結果サマリー

## 使用例

### 例1: シンプル通知
```
ユーザー: 「#dev-teamにビルド完了を通知して」

アクション: MCPまたはWebhookで送信:
"ビルドが完了しました！レビューお願いします。"
```

### 例2: エラーアラート
```
ユーザー: 「#ops-channelにDB接続エラーをアラートして」

アクション: errorテンプレートを使用:
" **アラート: データベース接続失敗**
時刻: 2025-11-27 10:30 UTC
詳細: 30秒後に接続タイムアウト
対応: データベースサーバーの状態を確認してください"
```

## セキュリティ注意事項

**重要: 認証情報の取り扱い**

1. Webhook URLをSKILL.mdやスクリプトに**直接書かない**
2. **環境変数を使用**: `SLACK_WEBHOOK_URL`
3. **MCPトークン**はClaude MCP設定で管理
4. **URLの検証**を送信前に行う（スクリプトで自動実行）

## セットアップ要件

### MCPモード用
1. Bot TokenでSlackアプリを作成
2. Claude設定でMCPサーバーを構成
3. 必要なスコープ: `channels:read`, `chat:write`, `reactions:write`

### Webhookモード用
1. Slack Incoming Webhookを作成
2. 環境変数を設定: `export SLACK_WEBHOOK_URL="https://hooks.slack.com/..."`
3. 追加設定は不要

詳細は `resources/setup-guide.md` を参照。

## スクリプトインターフェース

```bash
# シンプルメッセージ
python scripts/send_webhook.py --message "Hello!"

# テンプレート使用
python scripts/send_webhook.py --message "ビルド失敗" --template error --title "CIアラート"

# カスタムJSON
python scripts/send_webhook.py --json '{"text": "カスタムメッセージ"}'
```

## エラーハンドリング

| エラー | 原因 | 対処 |
|--------|------|------|
| "Slack連携なし" | MCPもWebhookも未設定 | セットアップガイド参照 |
| "チャンネルが見つかりません" | 無効なチャンネル名（MCP） | チャンネル存在を確認 |
| "Webhook失敗" | 無効なURLまたはネットワーク | SLACK_WEBHOOK_URLを確認 |
| "レート制限" | メッセージ送信過多 | 待機してリトライ |

## 制限事項

- **Webhookモード**: 送信のみ、チャンネル一覧やメッセージ読み取り不可
- **WebhookでのDM不可**: Webhookは特定チャンネル専用
- **メッセージ長**: 1メッセージ最大40,000文字
- **レート制限**: Slackは約1メッセージ/秒に制限

## テスト実行

```bash
cd /path/to/slack-notifier
python -m pytest scripts/test_send_webhook.py -v
```

**注意**: テストはモック化されており、実際のSlack送信は行いません。
