---
name: operability-observation
description: "運用観測性の確保。ログ、メトリクス、ヘルスチェック、設定検証でバグを扱う能力を担保。Use when: デプロイ前チェック、障害調査が困難、原因不明、ログ設計、メトリクス設計、設定管理実装。"
---

# Operability Observation（運用観測性）

## 目的

運用不能は「バグそのもの」ではなく、**バグや障害を扱う能力の欠如**。
このスキルは、MTTR（復旧時間）を下げ、フィードバックループを閉じる。

## 観測の恩恵

- MTTR（復旧時間）を下げる
- 失敗が起きたときの"次の一手"が見える
- 本番でのフィードバックが仕様・テストへ戻り、精度向上ループが閉じる

## Procedure

### Step 1: 起動時設定検証（Fail Fast）

設定が検証されず起動後に壊れるのを防ぐ：

```python
from pydantic import BaseSettings, validator

class AppConfig(BaseSettings):
    database_url: str
    api_key: str
    max_connections: int = 10

    @validator('database_url')
    def validate_database_url(cls, v):
        if not v.startswith(('postgresql://', 'mysql://')):
            raise ValueError('Invalid database URL format')
        return v

    @validator('max_connections')
    def validate_max_connections(cls, v):
        if v < 1 or v > 100:
            raise ValueError('max_connections must be between 1 and 100')
        return v

# 起動時に検証（失敗したら即終了）
config = AppConfig()
```

### Step 2: ヘルスチェックの実装

オーケストレータが正しく扱えるようにする：

```python
# Liveness: プロセスが生きているか
@app.get("/health/live")
def liveness():
    return {"status": "ok"}

# Readiness: リクエストを受け付けられるか
@app.get("/health/ready")
async def readiness():
    checks = {
        "database": await check_db_connection(),
        "cache": await check_cache_connection(),
        "external_api": await check_external_api(),
    }

    all_healthy = all(checks.values())
    status_code = 200 if all_healthy else 503

    return JSONResponse(
        status_code=status_code,
        content={"status": "ready" if all_healthy else "not_ready", "checks": checks}
    )
```

### Step 3: 構造化ログの実装

相関できる形でログを出力：

```python
import structlog

logger = structlog.get_logger()

# 相関ID、操作名、結果、エラー分類を含める
logger.info(
    "request_processed",
    correlation_id="abc-123",
    operation="create_order",
    user_id="user-456",
    result="success",
    duration_ms=150,
)

# エラーログには分類を含める
logger.error(
    "request_failed",
    correlation_id="abc-123",
    operation="create_order",
    error_type="validation_error",  # validation_error / policy_violation / invariant_broken
    error_message="Invalid product ID",
)
```

### Step 4: 基本メトリクスの設定

最低限必要なメトリクス：

| メトリクス | 種別 | 説明 |
|-----------|------|------|
| request_latency_seconds | Histogram | リクエスト処理時間 |
| request_total | Counter | リクエスト数（status, endpoint別） |
| error_total | Counter | エラー数（error_type別） |
| active_connections | Gauge | アクティブ接続数 |
| queue_depth | Gauge | キュー深度（飽和の兆候） |

```python
from prometheus_client import Counter, Histogram, Gauge

REQUEST_LATENCY = Histogram(
    'request_latency_seconds',
    'Request latency',
    ['endpoint', 'method']
)

REQUEST_COUNT = Counter(
    'request_total',
    'Request count',
    ['endpoint', 'method', 'status']
)

ERROR_COUNT = Counter(
    'error_total',
    'Error count',
    ['error_type', 'endpoint']
)
```

### Step 5: エラー分類の設計

エラーを適切に分類し、対処可能にする：

| エラー分類 | 説明 | 対処 |
|-----------|------|------|
| validation_error | 入力検証失敗 | クライアント修正 |
| policy_violation | ビジネスルール違反 | 操作変更 |
| invariant_broken | 内部整合性違反 | 調査必要 |
| external_error | 外部システム障害 | リトライ/待機 |
| internal_error | 内部エラー | 即座に調査 |

## 最小セット

- **(F1)** 起動時設定検証（fail fast）
- **(F2)** ヘルスチェック（liveness/readiness）
- **(F3)** 構造化ログ ＋ 相関ID ＋ エラー分類
- **(F4)** 最低限のメトリクス（エラー率・レイテンシ・飽和のどれか2つでも）

## 運用チェックリスト

詳細は `references/operability-checklist.md` を参照。

## Outputs

- 設定スキーマ（Pydantic / Zod / JSON Schema等）
- ヘルスチェックエンドポイント実装
- 構造化ログ設定
- メトリクス設定
- エラー分類定義

## Examples

### Kubernetes ヘルスチェック設定

```yaml
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: app
    livenessProbe:
      httpGet:
        path: /health/live
        port: 8080
      initialDelaySeconds: 5
      periodSeconds: 10
    readinessProbe:
      httpGet:
        path: /health/ready
        port: 8080
      initialDelaySeconds: 10
      periodSeconds: 5
```

### 構造化ログ出力例

```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "level": "info",
  "event": "order_created",
  "correlation_id": "req-abc-123",
  "user_id": "user-456",
  "order_id": "order-789",
  "total_amount": 15000,
  "duration_ms": 45
}

{
  "timestamp": "2024-01-15T10:30:05Z",
  "level": "error",
  "event": "payment_failed",
  "correlation_id": "req-abc-123",
  "error_type": "external_error",
  "error_message": "Payment gateway timeout",
  "retry_count": 2
}
```
