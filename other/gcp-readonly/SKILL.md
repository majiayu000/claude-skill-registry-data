---
name: gcp-read-only
description: Read-only Google Cloud inspection via gcloud CLI
activation_keywords: [gcp, gcloud, gce, gke, google cloud, bucket, compute]
execution_mode: server
---

# GCP Read Only Skill

Read-only operations via `gcloud`:

- `gce` — list compute instances (optional `--zones`)
- `gke` — list GKE clusters
- `buckets` — list Cloud Storage buckets
- `regions` — list compute regions

Tool: `builtin_gcp_readonly` with `operation`, optional `project`, optional `zone` (for `gce`).

Requires `gcloud` installed and authenticated on the server.
