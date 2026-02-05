---
name: rust-development
description: Obsidian LiveSync プロジェクトの Rust 開発を支援します。DDD 4層アーキテクチャ（domain/application/infrastructure/interfaces）に従った新規モジュール追加、axum ハンドラー・ルーティング実装、DomainError と thiserror を使用したエラーハンドリング、tokio-test・mockall・rstest によるテスト作成を行います。新機能追加、コード修正、アーキテクチャ設計、テスト実装を依頼されたときに使用してください。
---

# Rust Development for Obsidian LiveSync

## Overview

このスキルは、Obsidian LiveSync プロジェクトの Rust 開発における標準的なパターンと規約に従った実装を支援します。

プロジェクトは DDD（Domain-Driven Design）4層アーキテクチャを採用しています：

```
livesync-proxy/src/
├── domain/           # ドメイン層: ビジネスロジックの中核
│   ├── models.rs     # CouchDbDocument, DomainError
│   └── services.rs   # CouchDbRepository トレイト
├── application/      # アプリケーション層: ユースケース
│   └── services.rs   # LiveSyncService
├── infrastructure/   # インフラ層: 外部サービス接続
│   ├── config.rs     # AppConfig
│   └── couchdb.rs    # CouchDbClient（674行）
└── interfaces/       # インターフェース層: HTTP エンドポイント
    └── web/
        ├── server.rs    # ルーター設定（340行）
        ├── handlers.rs  # リクエストハンドラ（163行）
        ├── health.rs    # ヘルスチェック
        └── metrics.rs   # Prometheus メトリクス
```

## Instructions

### 1. DDD 4層の責務と依存方向

**依存方向のルール**: 外側の層は内側の層に依存できるが、逆は不可。

```
interfaces → application → domain ← infrastructure
```

| 層 | 責務 | 依存可能 |
|---|---|---|
| **domain** | ビジネスモデル、トレイト定義 | なし（最も内側） |
| **application** | ユースケースの実装 | domain のみ |
| **infrastructure** | 外部サービス接続 | domain のみ |
| **interfaces** | HTTP エンドポイント | application, domain |

### 2. 新規モジュール追加の手順

1. **ドメインモデルを定義**（`domain/models.rs`）
   ```rust
   #[derive(Debug, Clone, Serialize, Deserialize)]
   pub struct NewModel {
       pub id: String,
       // フィールド
   }
   ```

2. **トレイトを定義**（`domain/services.rs`）
   ```rust
   #[async_trait]
   pub trait NewRepository {
       async fn method(&self, param: &str) -> Result<NewModel, DomainError>;
   }
   ```

3. **アプリケーションサービスを実装**（`application/services.rs`）
   ```rust
   pub struct NewService {
       repo: Arc<dyn NewRepository + Send + Sync>,
   }
   ```

4. **インフラ層で実装**（`infrastructure/`）
   ```rust
   #[async_trait]
   impl NewRepository for ConcreteClient {
       async fn method(&self, param: &str) -> Result<NewModel, DomainError> {
           // 実装
       }
   }
   ```

5. **lib.rs にモジュールを追加**
   ```rust
   pub mod new_module;
   ```

### 3. axum ハンドラー・ルーティング追加

**ハンドラーの基本パターン**（`interfaces/web/handlers.rs`参照）:

```rust
use axum::{
    extract::State,
    http::{Request, StatusCode},
    response::{IntoResponse, Response},
    Json,
};
use std::sync::Arc;
use crate::interfaces::web::server::AppState;

pub async fn new_handler(
    State(state): State<Arc<AppState>>,
    req: Request<Body>,
) -> impl IntoResponse {
    // 処理
    Json(serde_json::json!({"status": "ok"}))
}
```

**ルーティング追加**（`interfaces/web/server.rs`）:

```rust
let app = Router::new()
    .route("/new-endpoint", get(new_handler))
    .route("/new-endpoint/{id}", any(new_handler_with_param))
    // 既存のルート
    .with_state(app_state);
```

### 4. エラーハンドリング

**DomainError の定義**（`domain/models.rs`）:

```rust
#[derive(Debug, thiserror::Error)]
pub enum DomainError {
    #[error("Invalid message format: {0}")]
    InvalidMessage(String),

    #[error("Authentication error: {0}")]
    AuthError(String),

    #[error("CouchDB error: {0}")]
    CouchDbError(String),

    #[error("HTTP proxy error: {0}")]
    HttpProxyError(String),
}
```

**IntoResponse トレイトの実装**（axum 0.8 ベストプラクティス）:

```rust
impl IntoResponse for DomainError {
    fn into_response(self) -> Response {
        let (status, message) = match &self {
            DomainError::InvalidMessage(_) => (StatusCode::BAD_REQUEST, self.to_string()),
            DomainError::AuthError(_) => (StatusCode::UNAUTHORIZED, self.to_string()),
            DomainError::CouchDbError(_) => (StatusCode::BAD_GATEWAY, self.to_string()),
            DomainError::HttpProxyError(_) => (StatusCode::BAD_GATEWAY, self.to_string()),
        };
        (status, Json(json!({"error": message}))).into_response()
    }
}
```

**ハンドラーでの Result 型返却**（推奨パターン）:

```rust
// IntoResponse 実装により ? 演算子が使用可能
pub async fn handler(State(state): State<Arc<AppState>>) -> Result<Json<Value>, DomainError> {
    let result = state.service.do_something().await?;
    Ok(Json(result))
}
```

**ミドルウェアエラーハンドリング**（タイムアウト等）:

```rust
use tower::timeout::TimeoutLayer;
use axum::error_handling::HandleErrorLayer;

let app = Router::new()
    .route("/api/slow", get(slow_handler))
    .layer(
        ServiceBuilder::new()
            .layer(HandleErrorLayer::new(|err: BoxError| async move {
                if err.is::<tower::timeout::error::Elapsed>() {
                    (StatusCode::REQUEST_TIMEOUT, "Request timed out".to_string())
                } else {
                    (StatusCode::INTERNAL_SERVER_ERROR, format!("Error: {}", err))
                }
            }))
            .layer(TimeoutLayer::new(Duration::from_secs(30)))
    );
```

**エラーの伝播**（map_err パターン）:

```rust
// 外部ライブラリのエラーを DomainError に変換
let data = serde_json::from_str(&body)
    .map_err(|e| DomainError::InvalidMessage(format!("JSON parse error: {}", e)))?;

// reqwest エラーの変換
let response = client.get(&url).send().await
    .map_err(|e| DomainError::CouchDbError(e.to_string()))?;
```

### 5. テスト作成

**テストファイルの場所**: `livesync-proxy/tests/`

**使用ライブラリ**:
- `tokio-test`: 非同期テスト
- `mockall`: モック作成
- `rstest`: パラメータ化テスト

**モック作成パターン**（`tests/couchdb_repository_test.rs`参照）:

```rust
use mockall::mock;
use async_trait::async_trait;

mock! {
    pub CouchDbMock {}

    #[async_trait]
    impl CouchDbRepository for CouchDbMock {
        async fn get_document(&self, db_name: &str, doc_id: &str)
            -> Result<CouchDbDocument, DomainError>;
        // 他のメソッド
    }
}

#[tokio::test]
async fn test_example() {
    let mut mock = MockCouchDbMock::new();
    mock.expect_get_document()
        .returning(|_, _| Ok(CouchDbDocument { ... }));

    // テスト
}
```

**インメモリ実装パターン**:
```rust
struct InMemoryRepo {
    data: Mutex<HashMap<String, Model>>,
}

#[async_trait]
impl Repository for InMemoryRepo {
    // 実装
}
```

## Examples

### 新しいエンドポイントの追加

```rust
// 1. handlers.rs に追加
pub async fn new_feature_handler(
    State(state): State<Arc<AppState>>,
) -> impl IntoResponse {
    match state.livesync_service.new_feature().await {
        Ok(result) => Json(result).into_response(),
        Err(e) => {
            (StatusCode::INTERNAL_SERVER_ERROR,
             Json(json!({"error": e.to_string()}))).into_response()
        }
    }
}

// 2. server.rs のルーターに追加
.route("/api/new-feature", get(new_feature_handler))
```

### ドメインエラーの追加

```rust
// domain/models.rs
#[derive(Debug, thiserror::Error)]
pub enum DomainError {
    // 既存のエラー...

    #[error("Validation error: {0}")]
    ValidationError(String),
}
```

## Reference

### 主要ファイル
- `livesync-proxy/src/domain/models.rs` - ドメインモデル
- `livesync-proxy/src/domain/services.rs` - トレイト定義
- `livesync-proxy/src/application/services.rs` - LiveSyncService
- `livesync-proxy/src/interfaces/web/server.rs` - ルーター
- `livesync-proxy/src/interfaces/web/handlers.rs` - ハンドラー

### コマンド
```bash
cd livesync-proxy
cargo build              # 開発ビルド
cargo build --release    # リリースビルド
cargo test --verbose     # 全テスト実行
cargo fmt --all -- --check  # フォーマットチェック
cargo clippy -- -D warnings # リンター
```

### 依存クレート（Cargo.toml）
- axum 0.8.4, tokio 1.45, reqwest 0.12
- thiserror 2.0, anyhow 1.0
- tokio-test 0.4, mockall 0.13, rstest 0.25
