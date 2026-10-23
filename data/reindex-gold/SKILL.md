---
name: reindex-gold
description: Rebuild the pgvector gold index after source data changes. Invoke manually — replaces each collection, do NOT trigger automatically.
disable-model-invocation: true
---

# Skill: Rebuild the Gold Index

Use when BDPM/ANSM source data has changed, Silver models were updated, or `gold.embedding` is missing or stale.

## Steps

1. **Ensure Postgres is running** (`pgvector/pgvector:pg16`):
   ```bash
   docker compose up -d
   docker compose ps
   ```

2. **Ensure Silver is up to date** (run if source data changed):
   ```bash
   uv run dotenv -f .env run -- dbt run --project-dir dbt --profiles-dir dbt
   uv run dotenv -f .env run -- dbt test --project-dir dbt --profiles-dir dbt
   ```

3. **Materialize the Gold asset**:
   ```bash
   uv run dotenv -f .env run -- uv run dagster asset materialize --select gold_embeddings
   ```

4. **Verify row counts**:
   ```bash
   uv run dotenv -f .env run -- python -c "
   from sqlalchemy import create_engine, text
   from medox.pipeline.config_pipeline import PipelineSettings
   engine = create_engine(PipelineSettings().postgres_dsn)
   with engine.connect() as conn:
       rows = conn.execute(text('SELECT collection, count(*) FROM gold.embedding GROUP BY 1')).fetchall()
       print(rows)
   "
   ```

5. **Smoke-test the agent tools**:
   ```bash
   uv run dotenv -f .env run -- python -c "
   from medox.agent.tools.tool_search_drug import search_drug
   from medox.agent.tools.tool_check_interactions import check_interactions
   print(search_drug('doliprane'))
   print(check_interactions('warfarine', 'ibuprofene'))
   "
   ```

## Collections

| Collection | Content | Rebuilt from |
|------------|---------|--------------|
| `idx_bdpm_medicament_v1` | Drug denominations + metadata | `silver_bdpm__medicament` |
| `idx_ansm_interaction_v1` | ANSM interaction pairs | `silver_ansm__interaction` |

## Rules

- Run dbt tests before reindexing when Silver changed — bad Silver data produces bad embeddings
- A rebuild replaces one collection inside a transaction — expect several minutes of embedding
- If `gold_embeddings` fails, check Postgres is up and the image is `pgvector/pgvector:pg16`
