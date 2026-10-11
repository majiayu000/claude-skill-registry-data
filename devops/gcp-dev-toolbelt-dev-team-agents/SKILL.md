---
name: gcp
description: GCP — Cloud Run, GKE, Artifact Registry, Cloud SQL, Storage, IAM.
---

# Google Cloud Platform Deployment

## Core Principle: Serverless-First

GCP's managed services (Cloud Run, Cloud SQL) minimize operational overhead and scale to zero when not in use — ideal for cost efficiency.

---

## Recommended Stack

```
Cloud DNS → Cloud Load Balancing → Cloud Run → Cloud SQL
                                           → Memorystore (Redis)
                                           → Cloud Storage (assets)
```

---

## Artifact Registry — Container Images

```bash
# Configure Docker auth
gcloud auth configure-docker us-central1-docker.pkg.dev

# Build and push
docker build -t us-central1-docker.pkg.dev/PROJECT_ID/myrepo/myapp:$GIT_SHA .
docker push us-central1-docker.pkg.dev/PROJECT_ID/myrepo/myapp:$GIT_SHA

# Enable cleanup policy
gcloud artifacts repositories set-cleanup-policies myrepo \
  --location us-central1 \
  --policy '[{"name":"delete-old","action":"DELETE","condition":{"olderThan":"30d","tagState":"UNTAGGED"}}]'
```

## Cloud Run — Recommended Entry Point

```bash
# Deploy
gcloud run deploy myapp \
  --image us-central1-docker.pkg.dev/PROJECT_ID/myrepo/myapp:$GIT_SHA \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated \
  --min-instances 0 \
  --max-instances 10 \
  --memory 512Mi \
  --cpu 1 \
  --set-env-vars APP_ENV=production \
  --set-secrets DB_PASSWORD=myapp-db-password:latest \
  --service-account myapp-sa@PROJECT_ID.iam.gserviceaccount.com

# Map custom domain
gcloud run domain-mappings create \
  --service myapp \
  --domain myapp.example.com \
  --region us-central1
```

### Cloud Run YAML (for version control)

```yaml
# service.yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: myapp
  annotations:
    run.googleapis.com/ingress: all
spec:
  template:
    metadata:
      annotations:
        autoscaling.knative.dev/minScale: "0"
        autoscaling.knative.dev/maxScale: "10"
        run.googleapis.com/cloudsql-instances: PROJECT:REGION:INSTANCE
    spec:
      serviceAccountName: myapp-sa@PROJECT_ID.iam.gserviceaccount.com
      containers:
        - image: IMAGE_URL
          resources:
            limits:
              cpu: "1"
              memory: 512Mi
          env:
            - name: DB_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: myapp-db-password
                  key: latest
```

## Secret Manager

```bash
# Create secret
echo -n "my-password" | gcloud secrets create myapp-db-password --data-file=-

# Grant access to service account
gcloud secrets add-iam-policy-binding myapp-db-password \
  --member="serviceAccount:myapp-sa@PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
```

## IAM — Service Accounts

```bash
# Create service account for the app
gcloud iam service-accounts create myapp-sa \
  --display-name "MyApp Service Account"

# Grant minimum roles
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="serviceAccount:myapp-sa@PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/cloudsql.client"
```

**Rules**: Never use the default compute service account — create dedicated ones with minimum permissions.

## Cost Optimization

- Cloud Run scales to **zero** — no idle costs for low-traffic services
- Use `--min-instances 0` for dev/staging, `--min-instances 1` for production (eliminates cold start)
- Cloud SQL: use `db-f1-micro` for dev, `db-g1-small` for staging
- Enable **committed use discounts** for predictable Cloud Run traffic (up to 17% off)
- Set up **Budgets & Alerts** in Billing console at 50%, 80%, 100%
- Use **Cloud Storage Nearline** for infrequently accessed data

## Useful Commands

```bash
# Tail Cloud Run logs
gcloud run services logs tail myapp --region us-central1

# List revisions
gcloud run revisions list --service myapp --region us-central1

# Rollback to previous revision
gcloud run services update-traffic myapp \
  --to-revisions myapp-00023-abc=100 \
  --region us-central1

# Check costs
gcloud billing budgets list --billing-account BILLING_ACCOUNT_ID
```
