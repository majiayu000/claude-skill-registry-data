---
name: gcp-operations
description: This skill should be used when the user asks to "check logs", "view Cloud Run logs", "deploy a service", "check service status", "manage secrets", "add a secret", "list services", "check what's running", or mentions GCP, Google Cloud, Cloud Run, Secret Manager, or deployment. Provides commands and guidance for operating Local Pulse services on Google Cloud Platform.
version: 1.0.0
---

# GCP Operations for Local Pulse

## Overview

Local Pulse runs on Google Cloud Platform with the following infrastructure:
- **Project ID**: `localpulse-469114`
- **Region**: `europe-west1`
- **Services**: Cloud Run (4 services), Secret Manager, Cloud Storage

---

## Cloud Run Services

### Service Inventory

| Service | Purpose | Memory | Min/Max Instances |
|---------|---------|--------|-------------------|
| `frontend` | FastAPI web server with Supabase auth | 512Mi | 1/10 (always warm) |
| `ingestion-api` | Poster upload, deduplication, triggers enrichment | 512Mi | 0/10 |
| `enrichment-worker` | Multi-provider API enrichment (Spotify, Google, etc.) | 4Gi | 0/1 |
| `model-service` | ML processing with MobileNetV3 Large | 2Gi | 0/5 |

### Check Service Status

```bash
# List all services
gcloud run services list --project=localpulse-469114 --region=europe-west1

# Get specific service details
gcloud run services describe <SERVICE_NAME> \
  --region=europe-west1 \
  --project=localpulse-469114

# Get service URL
gcloud run services describe <SERVICE_NAME> \
  --region=europe-west1 \
  --project=localpulse-469114 \
  --format='value(status.url)'
```

### Health Check Endpoints

```bash
# Frontend
curl https://frontend-940133235587.europe-west1.run.app/health

# Ingestion API
curl https://ingestion-api-940133235587.europe-west1.run.app/api/v1/health

# Enrichment Worker
curl https://enrichment-worker-940133235587.europe-west1.run.app/health

# Model Service (requires authentication)
curl -H "Authorization: Bearer $(gcloud auth print-identity-token)" \
  https://model-service-940133235587.europe-west1.run.app/health
```

---

## Viewing Logs

### Tail Logs (Real-time)

```bash
# Frontend logs
gcloud logs tail --service=frontend --region=europe-west1 --project=localpulse-469114

# Ingestion API logs
gcloud logs tail --service=ingestion-api --region=europe-west1 --project=localpulse-469114

# Enrichment Worker logs
gcloud logs tail --service=enrichment-worker --region=europe-west1 --project=localpulse-469114

# Model Service logs
gcloud logs tail --service=model-service --region=europe-west1 --project=localpulse-469114
```

### Read Recent Logs

```bash
# Last 50 log entries for a service
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=<SERVICE_NAME>" \
  --project=localpulse-469114 \
  --limit=50

# Filter by severity (ERROR, WARNING, INFO, DEBUG)
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=<SERVICE_NAME> AND severity>=ERROR" \
  --project=localpulse-469114 \
  --limit=20

# Filter by time range (last hour)
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=<SERVICE_NAME> AND timestamp>=\"$(date -u -v-1H '+%Y-%m-%dT%H:%M:%SZ')\"" \
  --project=localpulse-469114 \
  --limit=100
```

### Log Shortcuts

```bash
# Quick alias for common services
alias logs-frontend='gcloud logs tail --service=frontend --region=europe-west1 --project=localpulse-469114'
alias logs-ingestion='gcloud logs tail --service=ingestion-api --region=europe-west1 --project=localpulse-469114'
alias logs-enrichment='gcloud logs tail --service=enrichment-worker --region=europe-west1 --project=localpulse-469114'
alias logs-model='gcloud logs tail --service=model-service --region=europe-west1 --project=localpulse-469114'
```

---

## Deployment

### Deploy Scripts

All deployment scripts are in the `deploy/` directory:

```bash
# Deploy frontend (always-warm instance)
./deploy/frontend.sh

# Deploy ingestion API
./deploy/ingestion.sh

# Deploy enrichment worker
./deploy/enrichment.sh

# Deploy model service (heavy ML, takes 5-10 minutes)
./deploy/model_service.sh
```

### What Each Deploy Script Does

1. **Builds Docker image** for `linux/amd64` platform
2. **Pushes to Google Container Registry** (`gcr.io/localpulse-469114/<service>:latest`)
3. **Deploys to Cloud Run** with:
   - Environment variables (bucket names, thresholds, URLs)
   - Secret references from Secret Manager
   - Resource allocation (memory, CPU, instances)
4. **Cleans up local Docker cache** to reclaim disk space

### Manual Deployment (Alternative)

```bash
# Build image
docker buildx build --platform linux/amd64 \
  -t gcr.io/localpulse-469114/<SERVICE_NAME>:latest \
  -f deploy/Dockerfile.<service> . \
  --push --provenance=false

# Deploy to Cloud Run
gcloud run deploy <SERVICE_NAME> \
  --image gcr.io/localpulse-469114/<SERVICE_NAME>:latest \
  --region europe-west1 \
  --project localpulse-469114
```

### Post-Deployment Verification

```bash
# Check deployment status
gcloud run services describe <SERVICE_NAME> \
  --region=europe-west1 \
  --project=localpulse-469114 \
  --format='value(status.conditions)'

# Verify health endpoint
curl $(gcloud run services describe <SERVICE_NAME> \
  --region=europe-west1 \
  --project=localpulse-469114 \
  --format='value(status.url)')/health
```

---

## Secret Manager

### List All Secrets

```bash
gcloud secrets list --project=localpulse-469114
```

### Secrets Inventory

| Secret Name | Purpose | Used By |
|-------------|---------|---------|
| `SUPABASE_URL` | Supabase project URL | frontend, ingestion |
| `SUPABASE_DATABASE_URL` | PostgreSQL connection string | all services |
| `SUPABASE_SECRET_KEY` | Service role key (bypasses RLS) | ingestion, enrichment |
| `SUPABASE_PUBLISHABLE_KEY` | Anon/public key (frontend auth) | frontend |
| `OPENROUTER_API_KEY` | OpenRouter API for vision/LLM | enrichment, ingestion |
| `MULTIMODAL_MODEL` | Vision model identifier | enrichment |
| `GOOGLE_PLACES_API_KEY` | Google Places API | enrichment |
| `GOOGLE_CSE_API_KEY` | Google Custom Search API | enrichment |
| `GOOGLE_CSE_ID` | Custom Search Engine ID | enrichment |
| `GOOGLE_KG_API_KEY` | Knowledge Graph API | enrichment |
| `SPOTIFY_CLIENT_ID` | Spotify API client ID | enrichment |
| `SPOTIFY_CLIENT_SECRET` | Spotify API client secret | enrichment |
| `EXA_API_KEY` | Exa web search API | enrichment |
| `MODEL_SERVICE_URL` | Internal model service URL | ingestion |
| `UPLOAD_ALLOWED_EMAILS` | JSON array of allowed uploaders | ingestion |
| `SENTRY_DSN` | Sentry error tracking | all services |
| `TELEGRAM_BOT_TOKEN` | Telegram bot API token | telegram-bot |

### Read Secret Value

```bash
# Get latest version
gcloud secrets versions access latest --secret=<SECRET_NAME> --project=localpulse-469114

# Get specific version
gcloud secrets versions access <VERSION> --secret=<SECRET_NAME> --project=localpulse-469114
```

### Create New Secret

```bash
# From value
echo -n 'secret-value' | gcloud secrets create <SECRET_NAME> \
  --data-file=- \
  --project=localpulse-469114

# From file
gcloud secrets create <SECRET_NAME> \
  --data-file=/path/to/secret.txt \
  --project=localpulse-469114
```

### Update Existing Secret

```bash
# Add new version (does not delete old versions)
echo -n 'new-secret-value' | gcloud secrets versions add <SECRET_NAME> \
  --data-file=- \
  --project=localpulse-469114
```

### Delete Secret

```bash
# Delete specific version
gcloud secrets versions destroy <VERSION> --secret=<SECRET_NAME> --project=localpulse-469114

# Delete entire secret (all versions)
gcloud secrets delete <SECRET_NAME> --project=localpulse-469114
```

### How Secrets Are Loaded

Services use automatic environment detection:

1. **Cloud Run**: Secrets passed via `--set-secrets` in deploy scripts are mounted as environment variables
2. **Fallback**: Application code in `apps/enrichment/secrets.py` can fetch directly from Secret Manager
3. **Local Development**: Load from `.env` file (copy from `env.local.example`)

---

## Cloud Storage

### Bucket Information

- **Bucket Name**: `localpulse-posters`
- **Purpose**: Stores poster images uploaded via Telegram/ingestion API
- **Access**: Supabase Storage (primary), GCS (legacy)

### Common Operations

```bash
# List bucket contents
gsutil ls gs://localpulse-posters/

# List with details
gsutil ls -l gs://localpulse-posters/

# Download file
gsutil cp gs://localpulse-posters/<path> ./local-file

# Upload file
gsutil cp ./local-file gs://localpulse-posters/<path>

# Check bucket size
gsutil du -s gs://localpulse-posters/
```

---

## IAM Permissions

### Service Account

Default compute service account: `940133235587-compute@developer.gserviceaccount.com`

### Grant Invoker Permission

For service-to-service calls (e.g., ingestion calling model service):

```bash
gcloud run services add-iam-policy-binding <TARGET_SERVICE> \
  --member="serviceAccount:940133235587-compute@developer.gserviceaccount.com" \
  --role="roles/run.invoker" \
  --region=europe-west1 \
  --project=localpulse-469114
```

---

## Troubleshooting

### Service Not Responding

1. Check if service is running:
   ```bash
   gcloud run services describe <SERVICE_NAME> --region=europe-west1 --project=localpulse-469114
   ```

2. Check recent logs for errors:
   ```bash
   gcloud logging read "resource.labels.service_name=<SERVICE_NAME> AND severity>=ERROR" \
     --project=localpulse-469114 --limit=20
   ```

3. Verify secrets are accessible:
   ```bash
   gcloud secrets versions access latest --secret=<SECRET_NAME> --project=localpulse-469114
   ```

### Deployment Failed

1. Check build logs in Cloud Build Console
2. Verify Dockerfile exists and builds locally:
   ```bash
   docker build -f deploy/Dockerfile.<service> .
   ```
3. Check Container Registry for image:
   ```bash
   gcloud container images list --repository=gcr.io/localpulse-469114
   ```

### Authentication Issues

```bash
# Re-authenticate gcloud
gcloud auth login

# Set up application default credentials
gcloud auth application-default login

# Verify current account
gcloud auth list
```

---

## Quick Reference

### Project Constants

```bash
PROJECT_ID="localpulse-469114"
REGION="europe-west1"
```

### Common Commands Cheat Sheet

```bash
# List services
gcloud run services list --project=localpulse-469114 --region=europe-west1

# Tail logs
gcloud logs tail --service=<SERVICE> --region=europe-west1 --project=localpulse-469114

# Deploy
./deploy/<service>.sh

# List secrets
gcloud secrets list --project=localpulse-469114

# Read secret
gcloud secrets versions access latest --secret=<NAME> --project=localpulse-469114

# Update secret
echo -n 'value' | gcloud secrets versions add <NAME> --data-file=- --project=localpulse-469114
```
