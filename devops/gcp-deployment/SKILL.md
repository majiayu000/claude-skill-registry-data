---
name: gcp-deployment
description: Deep knowledge about deploying applications to Google Cloud Platform (Cloud Run, App Engine, Compute Engine).
type: transform
tier: library
domain: deploy
trigger: "when deploying to GCP"
---

## Context
Deploying {{project_name}} ({{project_type}}) to Google Cloud Platform (GCP).
You will follow a strict 6-phase Deployment Lifecycle Contract. 

## Instructions

Execute the following phases in order:

### Phase 1: Authentication
1. Ensure the `GOOGLE_APPLICATION_CREDENTIALS` environment variable is set to a valid service account key JSON file, or configure Workload Identity Federation (if inside CI/CD).
2. Authenticate the gcloud CLI: `gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS`.
3. Set the default project: `gcloud config set project <PROJECT_ID>`.

### Phase 2: Build
1. Prepare the artifacts for deployment.
2. If Cloud Run or GKE: build your Docker image (e.g., `docker build -t gcr.io/<PROJECT_ID>/<APP_NAME> .` or `gcloud builds submit --tag gcr.io/<PROJECT_ID>/<APP_NAME>`).
3. If App Engine: prepare `app.yaml`.
4. If Static Site (Cloud Storage): run `npm run build`.

### Phase 3: Install / Provisioning
1. Ensure the target GCP resources (Cloud Run services, Buckets, Compute Instances) exist and you have permissions to write to them.
2. If Cloud Storage: `gsutil ls gs://<bucket-name>`.
3. Enable necessary APIs (e.g., `gcloud services enable run.googleapis.com` if using Cloud Run).

### Phase 4: Deploy
1. Ship the artifact to GCP.
2. Cloud Run: `gcloud run deploy <SERVICE_NAME> --image gcr.io/<PROJECT_ID>/<APP_NAME> --region <REGION> --platform managed`.
3. App Engine: `gcloud app deploy`.
4. Cloud Storage: `gsutil rsync -R dist/ gs://<bucket-name>`.

### Phase 5: Checking
1. Verify the deployment was successful.
2. Cloud Run: Check the returned service URL via `curl` and inspect `gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=<SERVICE_NAME>"` if it fails.
3. App Engine: Check the target URL.
4. Ensure the service returns HTTP 200.

### Phase 6: Update / Rollback
1. If Phase 5 fails, immediately initiate a rollback.
2. Cloud Run: Route 100% of traffic to the previous revision (`gcloud run services update-traffic <SERVICE_NAME> --to-revisions=<PREVIOUS_REVISION_NAME>=100 --region <REGION>`).
3. App Engine: Roll back traffic to an older version via `gcloud app services set-traffic`.
4. Note the failure in the progress log.

## Validation
- [ ] GCP authentication succeeds.
- [ ] Build succeeds.
- [ ] Artifacts are deployed.
- [ ] Health check (curl) returns 200 OK.
