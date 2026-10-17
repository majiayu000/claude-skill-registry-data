---
name: worker-ingestion
description: Work with ingestion workers and data pipeline for the FinOps platform
---

# Worker Ingestion

Use this skill to:
- Develop ingestion workers for different cloud providers
- Work with FOCUS specification normalization
- Test data transformations
- Debug ingestion pipelines
- Monitor ingestion jobs

## Supported Ingestion Sources
- **Azure** — Azure Cost Management API
- **AWS** — Data Exports / FOCUS API
- **GCP** — BigQuery FOCUS exports
- **OCI** — Object Storage FOCUS files
- **Snowflake** — Direct cost extracts
- **Databricks** — Job/cluster cost data
- **Grafana** — Monitoring data
- **Redis** — Infrastructure metrics
- **VMware** — Custom vSphere cost tracking

## Worker Architecture
Each worker:
1. Connects to source system
2. Extracts cost/usage data
3. Transforms to FOCUS 1.0–1.4 normalization
4. Loads to `ingest` database
5. Triggers allocation and analysis jobs

## Common Tasks

### Develop New Worker
```bash
cd services/workers/[cloud-type]-ingest
npm install
npm run dev
```

### Run Worker Job Locally
```bash
npm run job:ingest -- --provider=aws
npm run job:ingest -- --provider=azure
```

### Test Transformation Logic
```bash
npm run test:workers
npm run test:workers:watch
```

### Debug FOCUS Mapping
```bash
npm run debug:focus-mapping -- --source=aws --sample-file=input.json
```

### Check Ingestion Status
```bash
npm run status:ingestion
```
