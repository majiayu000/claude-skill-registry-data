---
name: docker-ops
description: Obsidian LiveSync の Docker Compose 環境を操作・トラブルシューティングします。compose.yaml の構成理解、環境変数（.env）の設定、CouchDB と livesync-proxy のヘルスチェック、バックアップサービスの実行、ログ確認とデバッグを行います。Docker 環境の起動・停止、コンテナの状態確認、トラブルシューティングを依頼されたときに使用してください。
---

# Docker Operations for Obsidian LiveSync

## Overview

このスキルは、Obsidian LiveSync の Docker Compose 環境の操作とトラブルシューティングを支援します。

### サービス構成

```yaml
services:
  couchdb:          # CouchDB 3.x データベース
  livesync-proxy:   # Rust HTTP プロキシ
  backup:           # 手動バックアップ（profilesで制御）
  backup-scheduler: # 定期バックアップスケジューラ
```

## Instructions

### 1. compose.yaml の構成

**CouchDB サービス**:
```yaml
couchdb:
  build: ./couchdb
  volumes:
    - couchdb_data:/opt/couchdb/data
    - ./couchdb/local.ini:/opt/couchdb/etc/local.ini:rw
  environment:
    COUCHDB_USER: ${COUCHDB_USER}
    COUCHDB_PASSWORD: ${COUCHDB_PASSWORD}
  ports:
    - "${HOST_COUCHDB_PORT}:5984"
  healthcheck:
    test: ["CMD", "curl", "-f", "-u", "${COUCHDB_USER}:${COUCHDB_PASSWORD}", "http://localhost:5984/_up"]
```

**livesync-proxy サービス**:
```yaml
livesync-proxy:
  build: ./livesync-proxy
  depends_on:
    - couchdb
  environment:
    COUCHDB_URL: http://couchdb:5984/
    RUST_LOG: info,livesync_proxy=debug
  ports:
    - "${HOST_PROXY_PORT}:3000"
```

**backup サービス**（手動実行）:
```yaml
backup:
  profiles:
    - manual  # docker compose run backup で実行
  volumes:
    - couchdb_data:/data:ro
```

### 2. 環境変数（.env.example 参照）

| 変数 | 説明 | デフォルト |
|------|------|------------|
| `COMPOSE_PROJECT_NAME` | プロジェクト名 | obsidian-sync |
| `HOST_COUCHDB_PORT` | CouchDB ホストポート | 5984 |
| `HOST_PROXY_PORT` | プロキシ ホストポート | 3000 |
| `COUCHDB_USER` | CouchDB ユーザー名 | admin |
| `COUCHDB_PASSWORD` | CouchDB パスワード | (要変更) |
| `COUCHDB_DBNAME` | データベース名 | obsidian |
| `BACKUP_SCHEDULE` | バックアップ CRON | 0 2 * * * |
| `BACKUP_GIT_REPO` | バックアップ先リポジトリ | - |
| `BACKUP_GIT_TOKEN` | Git 認証トークン | - |
| `RUST_LOG` | ログレベル | info |

**初期設定**:
```bash
cp .env.example .env
# .env を編集して COUCHDB_PASSWORD を変更
```

### 3. ヘルスチェックとトラブルシューティング

**サービス状態確認**:
```bash
# コンテナ状態
docker compose ps

# CouchDB ヘルスチェック
curl -u admin:password http://localhost:5984/_up

# プロキシ ヘルスチェック
curl http://localhost:3000/health
```

**ログ確認**:
```bash
# 全サービスのログ
docker compose logs -f

# 特定サービス
docker compose logs -f livesync-proxy
docker compose logs -f couchdb

# 最新50行
docker compose logs --tail=50 livesync-proxy
```

**よくある問題と解決策**:

| 症状 | 原因 | 解決策 |
|------|------|--------|
| CouchDB に接続できない | 認証情報の不一致 | .env の COUCHDB_USER/PASSWORD 確認 |
| プロキシが起動しない | CouchDB 未起動 | `docker compose up couchdb` を先に実行 |
| ポート競合 | ポート使用中 | HOST_PROXY_PORT / HOST_COUCHDB_PORT 変更 |
| データが消えた | ボリューム削除 | `docker compose down` に `-v` を付けない |

### 4. バックアップサービスの使い方

**手動バックアップ**:
```bash
docker compose run backup
```

**スケジューラ起動**（定期バックアップ）:
```bash
docker compose up -d backup-scheduler
```

**バックアップ設定**:
```env
BACKUP_SCHEDULE=0 2 * * *        # 毎日午前2時
BACKUP_RUN_ON_STARTUP=false      # 起動時実行
BACKUP_GIT_REPO=https://github.com/...
BACKUP_GIT_TOKEN=github_pat_xxx
```

## Examples

### 開発環境の起動

```bash
# 初回セットアップ
cp .env.example .env
# .env を編集

# ビルドして起動
docker compose up --build

# バックグラウンド起動
docker compose up -d

# 停止
docker compose down

# データを含めて完全削除（注意）
docker compose down -v
```

### デバッグモードでの起動

```bash
# 詳細ログ有効化
RUST_LOG=debug docker compose up livesync-proxy
```

### CouchDB 直接アクセス

```bash
# データベース一覧
curl -u admin:password http://localhost:5984/_all_dbs

# obsidian データベースの情報
curl -u admin:password http://localhost:5984/obsidian
```

## Reference

### エンドポイント
- `http://localhost:3000/db` - LiveSync 接続 URI（Obsidian プラグイン設定用）
- `http://localhost:3000/health` - ヘルスチェック
- `http://localhost:3000/metrics` - Prometheus メトリクス
- `http://localhost:3000/api/status` - サーバーステータス
- `http://localhost:5984/_up` - CouchDB ヘルスチェック

### ファイル
- `compose.yaml` - Docker Compose 設定
- `.env.example` - 環境変数テンプレート
- `couchdb/local.ini` - CouchDB 設定
