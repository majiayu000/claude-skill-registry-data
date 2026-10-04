---
name: mysql-checkpointing
description: Make n8n workflows idempotent, resumable, and safe at scale using MySQL/Postgres checkpoint tables, batch processing patterns, duplicate prevention, and dynamic table creation. Use this skill whenever the user is building an n8n workflow that processes batches of data, handles webhooks, polls APIs, or runs on a schedule — phrases like "idempotent pipeline", "batch processing", "don't process duplicates", "resumable workflow", "checkpoint", "process 10000 rows", "handle failures gracefully". Also use whenever webhook handlers, ETL jobs, or scraping pipelines are being built. Use this skill proactively — missing checkpoints is the #1 cause of duplicate charges, duplicate emails, and duplicate API calls in production n8n.
---

# MySQL Checkpointing for n8n

Idempotency is not optional. Any workflow that can be re-run must produce identical results on the second run. MySQL (or Postgres — patterns are identical) is the pragmatic way.

## The three checkpoint tables every pipeline needs

### 1. `processed_items` — did we already handle this?

```sql
CREATE TABLE processed_items (
  item_key VARCHAR(255) PRIMARY KEY,      -- natural ID (webhook event_id, order_id, etc.)
  workflow_name VARCHAR(100) NOT NULL,
  processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  status VARCHAR(20) NOT NULL,            -- 'success' | 'failed' | 'skipped'
  payload_hash VARCHAR(64),               -- SHA256 of payload, detects payload changes
  INDEX idx_workflow_status (workflow_name, status),
  INDEX idx_processed_at (processed_at)
);
```

Check THIS FIRST in every workflow. Before any side-effect (email, charge, API call), `SELECT item_key FROM processed_items WHERE item_key = ?`. If it exists, exit.

### 2. `failed_jobs` — dead letter queue

```sql
CREATE TABLE failed_jobs (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  workflow_name VARCHAR(100) NOT NULL,
  item_key VARCHAR(255),
  payload JSON,
  error_message TEXT,
  error_node VARCHAR(100),                -- which n8n node failed
  retry_count INT DEFAULT 0,
  failed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_workflow_retry (workflow_name, retry_count)
);
```

Every error branch writes here. A retry workflow runs on schedule, picks up `retry_count < 3`, attempts reprocessing, bumps counter.

### 3. `batch_runs` — resumability

```sql
CREATE TABLE batch_runs (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  workflow_name VARCHAR(100),
  last_cursor VARCHAR(255),               -- last ID / timestamp processed
  items_processed INT DEFAULT 0,
  status VARCHAR(20),                     -- 'running' | 'complete' | 'failed'
  started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  completed_at TIMESTAMP NULL
);
```

For batch jobs (scraping, enrichment, imports): persist the cursor after each chunk. On restart, resume from `last_cursor` instead of starting over.

## The canonical idempotent workflow

```
1. Trigger (Webhook / Schedule)
2. Set — normalize input, compute item_key
3. MySQL — SELECT item_key FROM processed_items WHERE item_key = {{ $json.item_key }}
4. IF — results.length > 0?
   ├── True: Respond (already processed) → END
   └── False: continue
5. [Actual work: API calls, LLM, etc.]
6. IF — work succeeded?
   ├── True:
   │   7a. MySQL — INSERT INTO processed_items (item_key, workflow_name, status) VALUES (?, ?, 'success')
   │   8a. Respond success
   └── False:
       7b. MySQL — INSERT INTO failed_jobs (workflow_name, item_key, payload, error_message, error_node) VALUES (?, ?, ?, ?, ?)
       8b. Respond error (but with 2xx to prevent webhook re-delivery loops if caller retries)
```

The crucial detail: **insert into `processed_items` BEFORE responding to the caller**, not after. If insert fails, response should fail too — caller retries, which is fine because we weren't recorded.

## Batch processing pattern

For workflows processing 100s+ rows, never load all into memory:

```
1. MySQL — SELECT ... WHERE id > {{ $json.last_cursor }} ORDER BY id LIMIT 100
2. IF — results empty? → END (mark batch_run complete)
3. Split In Batches — batchSize: 10
4. [Process each item, including the idempotent check above]
5. MySQL — UPDATE batch_runs SET last_cursor = {{ last ID }}, items_processed = items_processed + batch.length WHERE id = {{ $batchRunId }}
6. Execute Workflow — call SELF recursively, passing batch_run.id
```

Why self-recursion: avoids n8n's memory limits on long-running workflows. Each invocation processes 100 items then hands off.

## Dynamic table creation pattern

For pipelines where each client/project needs its own table (e.g., scraping per domain), don't hardcode:

```javascript
// Code node
const sanitized = $input.item.json.client_id.replace(/[^a-z0-9_]/gi, '_');
const tableName = `leads_${sanitized}`;

return {
  json: {
    create_sql: `
      CREATE TABLE IF NOT EXISTS ${tableName} (
        id BIGINT AUTO_INCREMENT PRIMARY KEY,
        email VARCHAR(255) UNIQUE,
        full_name VARCHAR(255),
        enriched_at TIMESTAMP,
        INDEX idx_email (email)
      )
    `,
    table_name: tableName
  }
};
```

Then a `MySQL` node runs `{{ $json.create_sql }}`. Safe because you sanitized `client_id`.

**Never** `CREATE TABLE {{ $json.user_input }}` without sanitization — SQL injection via table name.

## Duplicate prevention beyond primary key

Primary keys catch exact duplicates. For semantic duplicates (e.g., same lead with different casing / extra whitespace), use a computed canonical key:

```javascript
// Code node before INSERT
const email = $json.email.toLowerCase().trim();
const phone = $json.phone?.replace(/\D/g, '') ?? '';
const canonical_key = `${email}|${phone}`;
return { json: { ...$json, canonical_key } };
```

Then make `canonical_key` a UNIQUE column. `INSERT ... ON DUPLICATE KEY UPDATE` handles it cleanly.

## Connection handling

- Use n8n's MySQL **credentials**, not inline connection strings.
- Set `connectionLimit: 5` in the credential — n8n can spawn many parallel executions and exhaust the DB connection pool.
- For Postgres, use `pg_bouncer` upstream if running >10 parallel executions.

## Observability

Add a dashboard query (just a Google Sheets export via scheduled workflow) that reports:
- Yesterday's processed count per workflow
- Failed jobs count per workflow (alert if >threshold)
- Median processing time (from `processed_at - started_at`)

Without this, silent regressions stay silent for weeks.

## Anti-patterns

- **Using `uuid()` as item_key when a natural key exists.** Stripe gives you `event_id`. Use it. UUID-based keys defeat idempotency because retries generate new UUIDs.
- **Checking processed_items AFTER doing the work.** Defeats the whole point. Check first, do work, record.
- **Storing huge payloads in `failed_jobs.payload`.** Truncate to 10KB or store S3 pointer. MySQL slows down with JSON columns over ~1MB.
- **No index on `processed_at`.** You'll want to query "what failed today" — without the index, full table scan.
