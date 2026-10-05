---
name: dev-start
description: >
  npm run dev で開発サーバーを起動（ポート3020の自動クリーンアップ込み）。Use when user asks to [開発サーバー起動, npm run dev, /dev-start].
domain: ops
---

開発サーバー（Next.js）をポート3020で起動します。ポート3020が使用中の場合、自動的にクリーンアップしてから起動します。

## 前提

- npm がインストールされていること
- 作業ディレクトリが doboku-note プロジェクトルートであること

## 手順

### Step 1: 開発サーバーを起動

```bash
npm run dev
```

このコマンド実行で以下が自動的に行われます：
1. `predev` スクリプトが実行され、ポート3020をリッスンしているプロセスをkillします
2. 1秒待機し、OSがポートを解放するのを待ちます
3. Next.js 開発サーバーがポート3020で起動します

サーバーが起動すると以下のような出力が表示されます：
```
✅ Port 3020 is free.
 ✓ Ready in X.Xs
 ▲ Next.js 15.5.2
 - Local:        http://localhost:3020
```

### Step 2: ブラウザで確認

http://localhost:3020 にアクセスしてサイトが表示されることを確認

## kill メカニズム

`scripts/kill-port.mjs` がOS別に以下を実行します：

### macOS / Linux
1. `lsof -ti:3020` でポート3020をリッスンしているPIDを検出
2. `kill -9 <pid>` で強制終了
3. OSがポートを解放するまで1秒待機

### Windows
1. `netstat -ano` で全ネットワーク接続を取得
2. ポート3020をリッスンしているPIDを検出
3. `taskkill /PID <pid> /F /T` で強制終了（子プロセスも含める）
4. OSがポートを解放するまで1秒待機

## エラー時の対応

- **Another next dev server is already running** が表示される場合：`kill -9 <PID>` で表示されたPIDを手動終了してから再試行
- **ERR_SOCKET_ERROR** が表示される場合：`lsof -ti:3020 | xargs kill -9` で全プロセスを終了してから再試行
- **EACCES permission denied** が表示される場合：管理者権限が必要な可能性があります

## 開発サーバーの停止

Ctrl+C を押してプロセスを終了します

## ホットリロード

ファイル変更時に自動的に再読み込みが行われます（`next.config.mjs` の FastRefresh が有効）
