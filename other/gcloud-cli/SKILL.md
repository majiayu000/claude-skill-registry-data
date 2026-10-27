---
name: gcloud-cli
description: >
  Execute Google Cloud Platform operations using the gcloud CLI (and gsutil/bq where applicable).
  Use when the user wants to: authenticate with GCP, manage GCP resources, deploy applications,
  configure projects or IAM, view logs, run SQL/BigQuery, or interact with any GCP service from
  the command line. Triggers on phrases like "gcloud", "Google Cloud CLI", "deploy to GCP",
  "create a VM", "Cloud Run", "GKE cluster", "Cloud Storage bucket", "set GCP project",
  "service account", "Cloud Functions", "App Engine deploy", or any request to manage
  Google Cloud resources via command line.
---

# gcloud CLI

## Command Structure

```
gcloud [GROUP] [SUB-GROUP] COMMAND [FLAGS]
```

Examples:
```bash
gcloud compute instances list
gcloud run services deploy my-svc --image gcr.io/my-project/my-image
gcloud projects list
```

## Configuration

```bash
# One-time setup
gcloud init

# Set active project
gcloud config set project PROJECT_ID

# Set default region/zone
gcloud config set compute/region us-central1
gcloud config set compute/zone us-central1-a

# View current config
gcloud config list

# Named configurations (switch between projects/envs)
gcloud config configurations create staging
gcloud config configurations activate staging
```

## Authentication

```bash
# Interactive login (local dev)
gcloud auth login

# Application Default Credentials (SDK/code usage)
gcloud auth application-default login

# Service account key
gcloud auth activate-service-account SA_EMAIL --key-file=key.json

# Impersonate a service account
gcloud [COMMAND] --impersonate-service-account=SA_EMAIL

# Check who you're authenticated as
gcloud auth list
```

## Output Formatting

```bash
--format=json          # Machine-readable
--format=yaml          # Human-readable structured
--format=table(col1,col2)  # Custom table columns
--format="value(name)" # Single field extraction

# Filtering
--filter="status=RUNNING"
--filter="name ~ '^prod-'"  # regex match
--sort-by=createTime
--limit=10
```

## Useful Global Flags

| Flag | Purpose |
|------|---------|
| `--project=PROJECT_ID` | Override active project |
| `--region=REGION` | Override default region |
| `--zone=ZONE` | Override default zone |
| `--quiet` / `-q` | Skip confirmation prompts |
| `--verbosity=debug` | Debug output |
| `--dry-run` | Preview without executing (where supported) |

## Service Commands Reference

For service-specific commands (Compute Engine, Cloud Run, GKE, Cloud Storage, IAM, App Engine, Cloud Functions, Cloud SQL, BigQuery, Pub/Sub, Artifact Registry), see [references/services.md](references/services.md).

## Common Patterns

### Get resource details
```bash
gcloud RESOURCE describe RESOURCE_NAME [--region/--zone]
```

### Wait for long-running operations
```bash
# Most commands support --async; poll with:
gcloud compute operations wait OPERATION_ID
```

### Use `--format=value()` in scripts
```bash
PROJECT=$(gcloud config get-value project)
IMAGE_DIGEST=$(gcloud container images describe gcr.io/$PROJECT/app:latest --format="value(image_summary.digest)")
```

### IAM policy binding pattern
```bash
gcloud RESOURCE add-iam-policy-binding RESOURCE_ID \
  --member="serviceAccount:SA@PROJECT.iam.gserviceaccount.com" \
  --role="roles/ROLE"
```
