---
name: fleetflow
description: FleetFlow（KDLベースのコンテナオーケストレーションツール）を効果的に使用するためのガイド
version: 0.5.0
---

# FleetFlow スキル

FleetFlowをプロジェクトで効果的に活用するための包括的なガイドです。

## 概要

FleetFlowは、KDL（KDL Document Language）をベースにしたコンテナオーケストレーションツールです。

**コンセプト**: 環境構築は、対話になった。伝えれば、動く。

### 主要な特徴

| 特徴 | 説明 |
|------|------|
| 超シンプル | Docker Composeと同等以下の記述量 |
| 可読性 | YAMLより読みやすいKDL構文 |
| ステージ管理 | local/dev/pre/live を統一管理 |
| AIネイティブ | MCP (Model Context Protocol) を標準サポート |
| OrbStack連携 | macOSローカル開発に最適化 |
| Dockerビルド | Dockerfileからのビルドをサポート |
| イメージプッシュ | ビルド後のレジストリプッシュを自動化 |
| クロスビルド | `--platform` でマルチアーキテクチャ対応 |
| サービスマージ | 複数ファイルでの設定オーバーライド |
| 再起動ポリシー | ホスト再起動時のコンテナ自動復旧 |
| 依存サービス待機 | Exponential Backoffで堅牢な起動順序制御 |
| クラウド対応 | さくらのクラウド、Cloudflareなど複数プロバイダー |
| DNS自動管理 | Cloudflare DNSとの自動連携 |
| CI/CDデプロイ | deployコマンドによる自動デプロイ |
| セルフアップデート | 最新バージョンへの自動更新 |

## クイックスタート

### インストール

```bash
# Homebrew (macOS)
brew install chronista-club/tap/fleetflow

# curl
curl -sSf https://raw.githubusercontent.com/chronista-club/fleetflow/main/install.sh | sh

# Cargo
cargo install --git https://github.com/chronista-club/fleetflow
```

### 最小構成

```kdl
// flow.kdl
project "myapp"

stage "local" {
    service "db"
}

service "db" {
    image "postgres:16"  // image は必須
    ports {
        port host=5432 container=5432
    }
    env {
        POSTGRES_PASSWORD "postgres"
    }
}
```

### 基本操作

```bash
fleet setup local    # 初回セットアップ（冪等）
fleet up local       # 起動
fleet ps             # 状態確認
fleet logs           # ログ表示
fleet down local     # 停止・削除
```

## 環境変数

| 変数 | 説明 |
|------|------|
| `FLEET_STAGE` | ステージ名を指定（local, dev, pre, live） |
| `FLEETFLOW_CONFIG_PATH` | 設定ファイルの直接パス指定 |
| `CLOUDFLARE_API_TOKEN` | Cloudflare APIトークン（DNS自動管理用） |
| `CLOUDFLARE_ZONE_ID` | Cloudflare Zone ID（DNS自動管理用） |

### 環境変数ファイル

```
.fleetflow/
├── .env           # グローバル（共通）
├── .env.local     # local 固有
├── .env.dev       # dev 固有
└── .env.live      # live 固有
```

## CLIコマンド一覧

ステージは位置引数で指定します。環境変数 `FLEET_STAGE` でも指定可能です。

| コマンド | 説明 |
|---------|------|
| `setup <stage>` | ステージの環境をセットアップ（冪等） |
| `up <stage>` | ステージを起動 |
| `down <stage>` | ステージを停止・削除 |
| `deploy <stage> --yes` | CI/CD向けデプロイ（デフォルトでpull） |
| `ps [--all]` | コンテナ一覧 |
| `logs [-f] [-n service]` | ログ表示 |
| `start <stage> [-n service]` | 停止中のサービスを起動 |
| `stop <stage> [-n service]` | サービスを停止（コンテナ保持） |
| `restart <stage> [-n service]` | サービスを再起動 |
| `build <stage> [-n service]` | イメージをビルド |
| `build <stage> --push [--tag <tag>]` | ビルド＆レジストリへプッシュ |
| `validate` | 設定を検証 |
| `cloud up <stage>` | クラウド環境を構築 |
| `cloud down <stage>` | クラウド環境を削除 |
| `mcp` | MCPサーバーを起動 |
| `self-update` | FleetFlow自体を最新版に更新 |
| `version` | バージョン表示 |

詳細: [reference/cli-commands.md](reference/cli-commands.md)

## 設定ファイル構造

```kdl
project "name"              // プロジェクト名（必須）

stage "local" {             // ステージ定義
    service "db"
    service "web"
}

service "db" {              // サービス定義
    image "postgres:16"     // 必須
    restart "unless-stopped" // 再起動ポリシー
    depends_on "other"      // 依存サービス
    wait_for { ... }        // 依存サービス待機設定
    ports { ... }
    env { ... }
    volumes { ... }
    build { ... }           // Dockerビルド設定
    healthcheck { ... }     // ヘルスチェック設定
}

// クラウドインフラ（オプション）
providers {
    sakura-cloud { zone "tk1a" }
    cloudflare { account-id env="CF_ACCOUNT_ID" }
}

server "app-server" {       // クラウドサーバー定義
    provider "sakura-cloud"
    plan core=4 memory=4
}
```

詳細: [reference/kdl-syntax.md](reference/kdl-syntax.md)

## 重要な仕様

### imageフィールドは必須

`image`フィールドは**必須**です。省略するとエラーになります：

```kdl
// 正しい定義
service "db" {
    image "postgres:16"
}

// エラー: imageが必須
service "db" {
    version "16"  // これだけではダメ
}
// Error: サービス 'db' に image が指定されていません
```

### サービスマージ機能

複数ファイルで同じサービスを定義すると、設定がマージされます：

```kdl
// flow.kdl（ベース設定）
service "api" {
    image "myapp:latest"
    ports { port host=8080 container=3000 }
    env { NODE_ENV "production" }
}

// flow.local.kdl（ローカルオーバーライド）
service "api" {
    env { DATABASE_URL "localhost:5432" }
}

// 結果:
// - image: "myapp:latest" (保持)
// - ports: [8080:3000] (保持)
// - env: { NODE_ENV: "production", DATABASE_URL: "localhost:5432" } (マージ)
```

**マージルール**:

| フィールドタイプ | ルール |
|----------------|--------|
| `Option<T>` | 後の定義が`Some`なら上書き、`None`なら保持 |
| `Vec<T>` | 後の定義が空でなければ上書き、空なら保持 |
| `HashMap<K, V>` | 両方をマージ（後の定義が優先） |

### Dockerビルド機能

規約ベースの自動検出と明示的指定の両方に対応：

```kdl
// 規約ベース: ./services/api/Dockerfile を自動検出
service "api" {
    image "myapp/api:latest"
    build_args {
        NODE_VERSION "20"
    }
}

// 明示的指定
service "worker" {
    image "myapp/worker:latest"
    dockerfile "./backend/worker/Dockerfile"
    context "./backend"
    target "production"  // マルチステージビルド
}
```

### イメージプッシュ機能

ビルドしたイメージをレジストリにプッシュ：

```bash
# ビルドのみ
fleet build local -n api

# ビルド＆プッシュ
fleet build local -n api --push

# タグを指定してビルド＆プッシュ
fleet build local -n api --push --tag v1.0.0

# クロスビルド（linux/amd64向け）
fleet build live -n api --push --platform linux/amd64
```

**認証方式**:
- Docker標準の `~/.docker/config.json` から認証情報を取得
- credential helper（osxkeychain, desktop など）も自動対応
- 環境変数 `DOCKER_CONFIG` でパスをカスタマイズ可能

**対応レジストリ**:
- Docker Hub (docker.io)
- GitHub Container Registry (ghcr.io)
- Amazon ECR (*.dkr.ecr.*.amazonaws.com)
- Google Container Registry (gcr.io)
- プライベートレジストリ (localhost:5000 など)

**タグ解決の優先順位**:
1. `--tag` CLIオプション
2. KDL設定の `image` フィールドのタグ
3. デフォルト: `latest`

### クラウドインフラ管理

複数のクラウドプロバイダーをKDLで宣言的に管理：

```kdl
providers {
    sakura-cloud { zone "tk1a" }
    cloudflare { account-id env="CF_ACCOUNT_ID" }
}

stage "dev" {
    server "app-server" {
        provider "sakura-cloud"
        plan core=4 memory=4
        disk size=100 os="ubuntu-24.04"
        dns_aliases "app" "api"  // DNSエイリアス
    }
}
```

### 再起動ポリシー

ホスト再起動後にコンテナを自動復旧させる：

```kdl
service "db" {
    image "postgres:16"
    restart "unless-stopped"  // ホスト再起動後も自動起動
}
```

**対応する値**:

| 値 | 説明 |
|----|------|
| `no` | 再起動しない（デフォルト） |
| `always` | 常に再起動 |
| `on-failure` | 異常終了時のみ再起動 |
| `unless-stopped` | 明示的に停止されない限り再起動（推奨） |

### 依存サービス待機（Exponential Backoff）

K8sのReadiness Probeコンセプトを取り入れた、依存サービスの準備完了待機機能：

```kdl
service "api" {
    image "myapp/api:latest"
    depends_on "db" "redis"
    wait_for {
        max_retries 23        // 最大リトライ回数（デフォルト: 23）
        initial_delay 1000    // 初回待機時間ms（デフォルト: 1000）
        max_delay 30000       // 最大待機時間ms（デフォルト: 30000）
        multiplier 2.0        // 待機時間の増加倍率（デフォルト: 2.0）
    }
}
```

**待機時間の計算**（Exponential Backoff）:
```
delay = initial_delay * multiplier^attempt
```
`max_delay`で上限を設定。デフォルト設定では1秒→2秒→4秒→8秒→...→30秒（上限）で待機。

**デフォルト設定での動作**:
- 最大約23回のリトライで約7分間の待機が可能
- `wait_for`のみ指定でデフォルト値が適用される

```kdl
// デフォルト設定を使用
service "api" {
    depends_on "db"
    wait_for  // 全てデフォルト値で待機
}
```

### DNS自動管理（Cloudflare）

`cloud up`/`cloud down`時にDNSレコードを自動管理：

- サーバー作成時: `{service}-{stage}.{domain}` のAレコードを自動追加
- サーバー削除時: DNSレコードを自動削除
- `dns_aliases`でCNAMEエイリアスも自動作成

必要な環境変数:
- `CLOUDFLARE_API_TOKEN`: Cloudflare APIトークン
- `CLOUDFLARE_ZONE_ID`: ドメインのZone ID

### CI/CDデプロイ（deployコマンド）

CI/CDパイプラインからの自動デプロイに最適化されたコマンド：

```bash
# 基本的な使い方（デフォルトでpull）
fleet deploy live --yes

# pullをスキップ
fleet deploy live --no-pull --yes

# GitHub Actionsから
ssh user@vps "cd /app && fleet deploy live --yes"
```

**オプション:**
| オプション | 説明 |
|-----------|------|
| `--no-pull` | イメージのpullをスキップ（デフォルトはpull） |
| `--yes` / `-y` | 確認なしで実行（CI向け） |

**デプロイフロー:**
1. 既存コンテナを強制停止・削除
2. 最新イメージをpull（--no-pullでスキップ可能）
3. コンテナを依存関係順に作成・起動
4. wait_forによる依存サービス待機

### セルフアップデート

```bash
# 手動でアップデート
fleet self-update
```

## コンテナ命名規則

FleetFlowは以下の命名規則でコンテナを作成します：

```
{project}-{stage}-{service}
```

例: `myapp-local-db`

OrbStackでは `{project}-{stage}` でグループ化されます。

## プロジェクト構造

```
fleetflow/
├── crates/
│   ├── fleetflow/              # CLI (bin: fleet)
│   ├── fleetflow-core/         # KDLパーサー
│   ├── fleetflow-config/       # 設定管理
│   ├── fleetflow-container/    # コンテナ操作
│   ├── fleetflow-build/        # Dockerビルド
│   ├── fleetflow-mcp/          # MCPサーバー
│   ├── fleetflow-cloud/        # クラウド抽象化
│   ├── fleetflow-cloud-sakura/ # さくらクラウド
│   └── fleetflow-cloud-cloudflare/ # Cloudflare
├── spec/                       # 仕様書
├── design/                     # 設計書
└── guides/                     # 利用ガイド
```

詳細: [reference/architecture.md](reference/architecture.md)

## スキルの起動タイミング

このスキルは以下の場合に参照してください：

- プロジェクトにFleetFlowを導入する際
- `flow.kdl` 設定ファイルを作成・編集する際
- コンテナ環境の構築・管理を行う際
- ローカル開発環境のセットアップ時
- クラウドインフラを宣言的に管理する際

## リファレンス

- [KDL構文リファレンス](reference/kdl-syntax.md)
- [CLIコマンドリファレンス](reference/cli-commands.md)
- [アーキテクチャ](reference/architecture.md)
- [パターン集](examples/patterns.md)

## 外部リンク

- [GitHub Repository](https://github.com/chronista-club/fleetflow)
- [KDL Document Language](https://kdl.dev/)
- [OrbStack](https://orbstack.dev/)

---

FleetFlow - シンプルに、統一的に、環境を構築する。
