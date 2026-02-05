---
name: couchdb-client
description: Obsidian LiveSync の CouchDbClient の構造と使用方法を説明します。CouchDbRepository トレイトの実装方法、HTTP プロキシパターン（forward_request）、longpoll リクエストの処理、メトリクス収集、ヘルスチェックの実装を理解・拡張する際に使用します。CouchDB 関連の機能追加、トラブルシューティング、パフォーマンス改善を依頼されたときに使用してください。
---

# CouchDB Client for Obsidian LiveSync

## Overview

このスキルは、Obsidian LiveSync の CouchDbClient の構造と使用方法を説明します。CouchDbClient は CouchDB との通信を担当し、HTTP プロキシとして Obsidian LiveSync プラグインからのリクエストを中継します。

### アーキテクチャ上の位置

```
domain/services.rs     → CouchDbRepository トレイト（抽象）
infrastructure/couchdb.rs → CouchDbClient（実装）
```

## Instructions

### 1. CouchDbClient の構造

```rust
pub struct CouchDbClient {
    client: Client,        // reqwest HTTP クライアント
    base_url: String,      // CouchDB ベース URL
    username: String,      // 認証ユーザー名
    password: String,      // 認証パスワード
}
```

**初期化**:
```rust
let client = CouchDbClient::new(
    "http://couchdb:5984/",
    "admin",
    "password",
);
```

### 2. CouchDbRepository トレイトの実装

**トレイト定義**（`domain/services.rs`）:

```rust
#[async_trait]
pub trait CouchDbRepository {
    // ドキュメント操作
    async fn get_document(&self, db_name: &str, doc_id: &str)
        -> Result<CouchDbDocument, DomainError>;
    async fn save_document(&self, db_name: &str, doc: CouchDbDocument)
        -> Result<CouchDbDocument, DomainError>;
    async fn delete_document(&self, db_name: &str, doc_id: &str, rev: &str)
        -> Result<(), DomainError>;

    // ビュークエリ
    async fn query_view(&self, db_name: &str, design_doc: &str,
        view_name: &str, options: Value) -> Result<Vec<CouchDbDocument>, DomainError>;

    // データベース管理
    async fn ensure_database(&self, db_name: &str) -> Result<(), DomainError>;

    // レプリケーション
    async fn replicate(&self, source: &str, target: &str, options: Value)
        -> Result<Value, DomainError>;

    // HTTP プロキシ
    async fn forward_request(&self, method: &str, path: &str,
        query: Option<String>, headers: HeaderMap, body: Bytes)
        -> Result<Response<Body>, DomainError>;

    // アクセサ
    fn get_base_url(&self) -> String;
    fn get_auth_credentials(&self) -> Option<(String, String)>;
}
```

### 3. HTTP プロキシパターン

**forward_request の処理フロー**:

```
Obsidian Plugin → /db/* → livesync-proxy → forward_request → CouchDB
```

**リクエストタイプ別の処理**:

| エンドポイント | 特徴 | タイムアウト |
|----------------|------|--------------|
| `/_changes?feed=longpoll` | 長時間接続 | 120秒 |
| `/_changes` | 通常の変更取得 | 90秒 |
| `/_bulk_docs` | 大量データ | 60秒 |
| その他 | 通常リクエスト | 60秒 |

**longpoll リクエストの検出と処理**:

```rust
let is_longpoll = path.contains("/_changes")
    && query.as_ref().is_some_and(|q| q.contains("feed=longpoll"));

let client = if is_longpoll {
    Client::builder()
        .timeout(Duration::from_secs(120))
        .tcp_keepalive(Some(Duration::from_secs(30)))
        .tcp_nodelay(true)
        .build()?
} else {
    self.client.clone()
};
```

### 4. エラーハンドリング

**エラータイプ別の処理**:

```rust
match e {
    // longpoll の中断（正常）
    err if is_longpoll && err.to_string().contains("aborted") => {
        // 204 No Content を返す
    }
    // タイムアウト
    err if err.is_timeout() => {
        // 504 Gateway Timeout を返す
    }
    // 接続エラー
    err if err.is_connect() => {
        // 502 Bad Gateway を返す
    }
}
```

### 5. メトリクス収集

**MetricsState の使用**（`interfaces/web/metrics.rs`）:

```rust
// リクエスト記録
state.metrics_state.record_request(&path, method, status_code).await;

// 処理時間記録
state.metrics_state.record_request_duration(&path, method, start);
```

**収集されるメトリクス**:
- `http_requests_total` - 総リクエスト数
- `http_request_duration_seconds` - レスポンス時間（ヒストグラム）
- longpoll/bulk_docs リクエストの個別カウント

### 6. ヘルスチェック

**HealthState の実装**（`interfaces/web/health.rs`）:

```rust
pub struct HealthState {
    pub couchdb_status: RwLock<CouchDbStatus>,
    consecutive_failures: AtomicU32,  // バックオフ用
    // ...
}
```

**バックオフ戦略**:
- 成功時: 通常間隔（30秒）に戻る
- 失敗時: 2^n 秒（最大5分）まで間隔を延長

```rust
let backoff_secs = std::cmp::min(
    2u64.pow(failures),
    self.max_check_interval.as_secs(),
);
```

## Examples

### 新しい CouchDB 操作の追加

```rust
// 1. トレイトにメソッド追加（domain/services.rs）
#[async_trait]
pub trait CouchDbRepository {
    // 既存メソッド...

    async fn compact_database(&self, db_name: &str) -> Result<(), DomainError>;
}

// 2. CouchDbClient に実装追加（infrastructure/couchdb.rs）
async fn compact_database(&self, db_name: &str) -> Result<(), DomainError> {
    let url = format!("{}{}/_compact", self.base_url, db_name);

    let response = self.client
        .post(&url)
        .basic_auth(&self.username, Some(&self.password))
        .header("Content-Type", "application/json")
        .send()
        .await
        .map_err(|e| DomainError::CouchDbError(e.to_string()))?;

    if !response.status().is_success() {
        return Err(DomainError::CouchDbError("Compact failed".into()));
    }
    Ok(())
}
```

### テスト用モックの作成

```rust
use mockall::mock;

mock! {
    pub CouchDbMock {}

    #[async_trait]
    impl CouchDbRepository for CouchDbMock {
        async fn get_document(&self, db_name: &str, doc_id: &str)
            -> Result<CouchDbDocument, DomainError>;
        // 他のメソッド...
    }
}

#[tokio::test]
async fn test_with_mock() {
    let mut mock = MockCouchDbMock::new();
    mock.expect_get_document()
        .returning(|_, _| Ok(CouchDbDocument { ... }));
}
```

### インメモリ実装（テスト用）

```rust
struct InMemoryCouchDb {
    databases: Mutex<HashMap<String, HashMap<String, CouchDbDocument>>>,
}

#[async_trait]
impl CouchDbRepository for InMemoryCouchDb {
    async fn get_document(&self, db_name: &str, doc_id: &str)
        -> Result<CouchDbDocument, DomainError> {
        let dbs = self.databases.lock().unwrap();
        dbs.get(db_name)
            .and_then(|db| db.get(doc_id))
            .cloned()
            .ok_or(DomainError::CouchDbError("Not found".into()))
    }
}
```

## CouchDB Best Practices

### 1. ドキュメント ID 最適化

**影響**: 16バイト ID → 4バイト ID で、1000万ドキュメントが 21GB → 4GB に削減された事例あり。

**推奨**:
- Base64url エンコーディングで効率的な ID 生成
- 順序的/ソート済み ID はランダム ID より挿入が高速
- ID にスラッシュ `/` は避け、コロン `:` を使用（プロキシ互換性）

```rust
// 推奨: 順序的 ID（タイムスタンプベース）
let doc_id = format!("{}:{}", timestamp_ms, uuid_short);

// 階層的 ID（親子関係）
let child_id = format!("{}:child:{}", parent_id, child_uuid);
```

### 2. ドキュメント設計

**多数の小さなドキュメント** > 少数の大きなドキュメント

```rust
// 推奨: 頻繁に変更されるデータを分離
// メインドキュメント
{ "_id": "note:abc", "title": "...", "created_at": "..." }
// メタデータドキュメント（頻繁に更新）
{ "_id": "note:abc:meta", "view_count": 100, "updated_at": "..." }
```

**メタデータフィールド**（推奨）:
```json
{
  "_id": "...",
  "type": "note",
  "created_at": "2025-01-15T10:30:00.000Z",
  "updated_at": "2025-01-15T10:30:00.000Z",
  "created_by": "user_id",
  "version": 1
}
```

日付は ISO 8601 形式（`.toISOString()`）を使用。

### 3. ビュー最適化

**ネイティブ関数で高速化**（JavaScript → ネイティブで 60秒 → 4秒）:

```javascript
// 遅い: JavaScript reduce
{ "reduce": "function(keys, values) { return sum(values); }" }

// 速い: ネイティブ reduce
{ "reduce": "_sum" }
{ "reduce": "_count" }
{ "reduce": "_stats" }
```

### 4. 競合解決

CouchDB は競合を「first-class citizen」として扱う。

```rust
// 競合検出
async fn check_conflicts(&self, db: &str, doc_id: &str) -> Result<Vec<String>, DomainError> {
    let url = format!("{}{}/{}?conflicts=true", self.base_url, db, doc_id);
    let response = self.client.get(&url)
        .basic_auth(&self.username, Some(&self.password))
        .send().await?;
    // _conflicts フィールドをパース
}
```

**解決戦略**:
- 最新のタイムスタンプを勝者とする
- マージ可能なフィールドはマージ
- 解決できない場合はユーザーに通知

### 5. レプリケーション設定

| 設定 | 推奨値 | 説明 |
|------|--------|------|
| `batch_size` | 100-500 | 小さいほどチェックポイント頻度↑、RAM使用量↓ |
| `checkpoint_interval` | 5000ms | 頻繁な更新には低い値 |
| `worker_processes` | 4 | ネットワークスループット向上 |

**継続的レプリケーション**（リアルタイム同期）:
```json
{
  "source": "local_db",
  "target": "remote_db",
  "continuous": true
}
```

### 6. コンパクション

定期的なコンパクションでパフォーマンス維持:

```bash
# データベースコンパクション
curl -X POST http://localhost:5984/dbname/_compact

# ビューコンパクション
curl -X POST http://localhost:5984/dbname/_compact/design_doc
```

## Reference

### 主要ファイル
- `livesync-proxy/src/domain/services.rs` - CouchDbRepository トレイト
- `livesync-proxy/src/infrastructure/couchdb.rs` - CouchDbClient 実装（674行）
- `livesync-proxy/src/interfaces/web/health.rs` - ヘルスチェック
- `livesync-proxy/src/interfaces/web/metrics.rs` - メトリクス

### CouchDB API
- `/_up` - ヘルスチェック
- `/{db}` - データベース操作
- `/{db}/{docid}` - ドキュメント操作
- `/{db}/_changes` - 変更フィード
- `/{db}/_bulk_docs` - バルク操作
- `/_replicate` - レプリケーション
- `/{db}/_compact` - コンパクション

### 参考リンク
- [CouchDB Performance](https://docs.couchdb.org/en/stable/maintenance/performance.html)
- [CouchDB Best Practices](https://jo.github.io/couchdb-best-practices/)
