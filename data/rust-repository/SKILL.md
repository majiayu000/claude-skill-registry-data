---
name: rust-repository
description: Implement the repository pattern for database abstraction with sqlx, transactions, and retry logic. Use when building data access layers.
---

# Repository Pattern

Database abstraction with sqlx, connection pooling, and production patterns.

## Basic Repository Structure

```rust
use sqlx::PgPool;

#[derive(Clone)]
pub struct VideoRepository {
    pool: PgPool,
}

impl VideoRepository {
    pub fn new(pool: PgPool) -> Self {
        Self { pool }
    }

    pub fn pool(&self) -> &PgPool {
        &self.pool
    }
}
```

## Connection Pool Setup

```rust
use sqlx::postgres::PgPoolOptions;

pub async fn create_pool(database_url: &str) -> Result<PgPool> {
    let pool = PgPoolOptions::new()
        .max_connections(5)
        .acquire_timeout(Duration::from_secs(3))
        .connect(database_url)
        .await?;

    // Verify connection
    sqlx::query("SELECT 1")
        .execute(&pool)
        .await?;

    Ok(pool)
}
```

## Typed Queries with query_as!

```rust
#[derive(Debug, Clone, sqlx::FromRow)]
pub struct VideoRecord {
    pub video_id: String,
    pub status: String,
    pub retry_count: i32,
    pub created_at: chrono::DateTime<chrono::Utc>,
}

impl VideoRepository {
    pub async fn get_by_id(&self, video_id: &str) -> Result<Option<VideoRecord>> {
        let record = sqlx::query_as!(
            VideoRecord,
            r#"SELECT video_id, status, retry_count, created_at
               FROM video_processing
               WHERE video_id = $1"#,
            video_id
        )
        .fetch_optional(&self.pool)
        .await?;

        Ok(record)
    }
}
```

## Atomic Batch Claiming with FOR UPDATE SKIP LOCKED

```rust
impl VideoRepository {
    /// Claim a batch of videos for processing.
    /// Uses FOR UPDATE SKIP LOCKED to prevent concurrent claims.
    pub async fn claim_batch(
        &self,
        count: i32,
        max_retries: i32,
    ) -> Result<Vec<VideoRecord>> {
        let mut tx = self.pool.begin().await?;

        // Select and lock rows atomically
        let rows = sqlx::query_as::<_, VideoRecord>(
            r#"SELECT video_id, status, retry_count, created_at
               FROM video_processing
               WHERE status IN ('PENDING', 'EXTRACTION_COMPLETE')
               AND retry_count < $1
               AND (retry_after IS NULL OR retry_after <= NOW())
               ORDER BY
                   CASE status
                       WHEN 'EXTRACTION_COMPLETE' THEN 0
                       ELSE 1
                   END,
                   created_at ASC
               LIMIT $2
               FOR UPDATE SKIP LOCKED"#
        )
        .bind(max_retries)
        .bind(count)
        .fetch_all(&mut *tx)
        .await?;

        // Update status for claimed rows
        for row in &rows {
            let new_status = match row.status.as_str() {
                "PENDING" => "EXTRACTION_IN_PROGRESS",
                "EXTRACTION_COMPLETE" => "EMBEDDING_IN_PROGRESS",
                _ => continue,
            };

            sqlx::query(
                "UPDATE video_processing
                 SET status = $1, updated_at = NOW()
                 WHERE video_id = $2"
            )
            .bind(new_status)
            .bind(&row.video_id)
            .execute(&mut *tx)
            .await?;
        }

        tx.commit().await?;
        Ok(rows)
    }
}
```

## Status Updates

```rust
impl VideoRepository {
    pub async fn update_status(
        &self,
        video_id: &str,
        status: &str,
        error_message: Option<&str>,
    ) -> Result<bool> {
        let result = sqlx::query(
            r#"UPDATE video_processing
               SET status = $1,
                   error_message = COALESCE($2, error_message),
                   updated_at = NOW()
               WHERE video_id = $3"#
        )
        .bind(status)
        .bind(error_message)
        .bind(video_id)
        .execute(&self.pool)
        .await?;

        Ok(result.rows_affected() > 0)
    }

    pub async fn mark_succeeded(&self, video_id: &str) -> Result<bool> {
        self.update_status(video_id, "SUCCEEDED", None).await
    }

    pub async fn mark_failed(&self, video_id: &str, error: &str) -> Result<bool> {
        self.update_status(video_id, "FAILED", Some(error)).await
    }
}
```

## Retry Logic with Exponential Backoff

```rust
impl VideoRepository {
    pub async fn handle_retryable_error(
        &self,
        video_id: &str,
        error_message: &str,
        max_retries: i32,
    ) -> Result<bool> {
        // Increment retry count
        let new_count = sqlx::query_scalar::<_, i32>(
            "UPDATE video_processing
             SET retry_count = retry_count + 1
             WHERE video_id = $1
             RETURNING retry_count"
        )
        .bind(video_id)
        .fetch_one(&self.pool)
        .await?;

        if new_count >= max_retries {
            self.mark_failed(video_id, &format!(
                "Max retries ({}) exceeded: {}",
                max_retries, error_message
            )).await?;
            return Ok(false);
        }

        // Exponential backoff: min(60 * 2^retry, 3600) seconds
        let base_delay = 60;
        let delay_secs = (base_delay * (1 << new_count)).min(3600);

        // Add jitter: ±25%
        let jitter = (delay_secs as f64 * 0.25 * (rand::random::<f64>() - 0.5)) as i64;
        let final_delay = (delay_secs as i64 + jitter).max(60);

        sqlx::query(
            "UPDATE video_processing
             SET retry_after = NOW() + $1 * INTERVAL '1 second',
                 error_message = $2,
                 status = CASE status
                     WHEN 'EMBEDDING_IN_PROGRESS' THEN 'EXTRACTION_COMPLETE'
                     ELSE 'PENDING'
                 END
             WHERE video_id = $3"
        )
        .bind(final_delay as i32)
        .bind(error_message)
        .bind(video_id)
        .execute(&self.pool)
        .await?;

        Ok(true)  // Will retry
    }
}
```

## Heartbeat for Stale Detection

```rust
impl VideoRepository {
    pub async fn update_heartbeat(&self, video_id: &str) -> Result<bool> {
        let result = sqlx::query(
            "UPDATE video_processing
             SET pc_heartbeat = NOW(), updated_at = NOW()
             WHERE video_id = $1"
        )
        .bind(video_id)
        .execute(&self.pool)
        .await?;

        Ok(result.rows_affected() > 0)
    }

    /// Reset videos stuck in processing (stale heartbeat)
    pub async fn reset_stuck_videos(&self) -> Result<u64> {
        let stale_threshold = Duration::from_secs(300);  // 5 minutes

        let result = sqlx::query(
            "UPDATE video_processing
             SET status = CASE status
                     WHEN 'EMBEDDING_IN_PROGRESS' THEN 'EXTRACTION_COMPLETE'
                     ELSE 'PENDING'
                 END
             WHERE status IN ('EXTRACTION_IN_PROGRESS', 'EMBEDDING_IN_PROGRESS')
             AND pc_heartbeat < NOW() - $1 * INTERVAL '1 second'"
        )
        .bind(stale_threshold.as_secs() as i32)
        .execute(&self.pool)
        .await?;

        Ok(result.rows_affected())
    }
}
```

## Test Mode (Read-Only)

```rust
impl VideoRepository {
    /// Fetch batch for testing without claiming (no writes)
    pub async fn fetch_test_batch(
        &self,
        count: i32,
        exclude_ids: &[String],
    ) -> Result<Vec<VideoRecord>> {
        let records = sqlx::query_as::<_, VideoRecord>(
            r#"SELECT video_id, status, retry_count, created_at
               FROM video_processing
               WHERE status IN ('PENDING', 'EXTRACTION_COMPLETE')
               AND video_id != ALL($1)
               ORDER BY created_at ASC
               LIMIT $2"#
        )
        .bind(exclude_ids)
        .bind(count)
        .fetch_all(&self.pool)
        .await?;

        Ok(records)
    }
}
```

## Guidelines

- Use connection pooling with reasonable limits
- Use `FOR UPDATE SKIP LOCKED` for concurrent batch processing
- Implement exponential backoff with jitter for retries
- Use heartbeats to detect stale/crashed processors
- Reset in-progress records on startup
- Provide test mode without writes
- Use transactions for multi-step operations

## Examples

See `hercules-local-algo/src/db/repo.rs` for complete implementation.
