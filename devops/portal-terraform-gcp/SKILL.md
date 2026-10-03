---
name: portal-terraform-gcp
description: Define minimal GCP infrastructure as code with Terraform for the Portal Centralizado de Datos Financieros — 2 Cloud Run services (frontend/backend) with scale-to-zero, GCS exports bucket, Secret Manager injection. Use when creating or modifying the infra/ module, bootstrapping the GCP project, or documenting the gcloud run deploy bridge.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Portal Terraform GCP Skill

## Rules — NON-NEGOTIABLE

- Cloud Run con `min_instances = 0` (scale-to-zero). Subir a 1 SOLO el día de demo/pruebas de usabilidad, con decisión documentada (skill `portal-finops`).
- Secrets (`GEMINI_API_KEY`, `JWT_SECRET_KEY`) SOLO en Secret Manager, inyectados a Cloud Run vía `secret_key_ref`. Jamás en `.tfvars` commiteados ni en el repo.
- `terraform.tfvars` gitignored; variables sensibles nunca con default.
- `terraform plan` revisado por humano antes de `apply`.
- Bucket de exports con lifecycle de 7 días (presupuesto §23 del plan).
- IAM least privilege: la service account de runtime solo `secretmanager.secretAccessor` + `storage.objectAdmin` sobre su bucket.
- El módulo es MÍNIMO (1 SP MUST). Staging/prod parametrizado y state en GCS son STRETCH — no construirlos sin acuerdo del equipo.

## Estructura

```
infra/
├── main.tf          # 2 Cloud Run + GCS + Secret Manager + IAM
├── variables.tf     # project_id, region, backend_image, frontend_image
├── outputs.tf       # URLs de los servicios
└── terraform.tfvars # gitignored
```

## Cloud Run backend con secrets

```hcl
# infra/main.tf
resource "google_cloud_run_v2_service" "backend" {
  name     = "portal-backend"
  location = var.region

  template {
    scaling {
      min_instance_count = 0  # scale-to-zero — FinOps academico
      max_instance_count = 2
    }
    containers {
      image = var.backend_image
      resources {
        limits = { cpu = "1", memory = "1Gi" }
      }
      env {
        name  = "GCS_EXPORTS_BUCKET"
        value = google_storage_bucket.exports.name
      }
      dynamic "env" {
        for_each = toset(["GEMINI_API_KEY", "JWT_SECRET_KEY"])
        content {
          name = env.value
          value_source {
            secret_key_ref {
              secret  = google_secret_manager_secret.app[env.value].secret_id
              version = "latest"
            }
          }
        }
      }
    }
    service_account = google_service_account.runtime.email
  }
}
```

El servicio `frontend` replica el bloque sin secrets (solo `NUXT_PUBLIC_API_BASE` apuntando al backend).

## GCS exports con lifecycle

```hcl
resource "google_storage_bucket" "exports" {
  name                        = "${var.project_id}-exports"
  location                    = var.region
  uniform_bucket_level_access = true
  lifecycle_rule {
    condition { age = 7 }   # exports viven 7 dias
    action    { type = "Delete" }
  }
}

resource "google_secret_manager_secret" "app" {
  for_each  = toset(["GEMINI_API_KEY", "JWT_SECRET_KEY"])
  secret_id = each.key
  replication { auto {} }
}
```

Los VALORES de los secrets se cargan fuera de Terraform: `echo -n "$VALUE" | gcloud secrets versions add GEMINI_API_KEY --data-file=-`.

## Bootstrap (una sola vez por proyecto)

```bash
gcloud services enable run.googleapis.com secretmanager.googleapis.com \
  storage.googleapis.com artifactregistry.googleapis.com cloudtrace.googleapis.com

gcloud iam service-accounts create portal-deploy --display-name="CI deploy"
gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:portal-deploy@${PROJECT_ID}.iam.gserviceaccount.com" \
  --role="roles/run.admin"
# + roles/artifactregistry.writer, roles/iam.serviceAccountUser
```

## Puente aceptado mientras Terraform madura

`gcloud run deploy` documentado en script es alternativa valida (criterio del plan):

```bash
# scripts/deploy_bridge.sh
gcloud run deploy portal-backend --image "$BACKEND_IMAGE" --region "$REGION" \
  --min-instances=0 --set-secrets="GEMINI_API_KEY=GEMINI_API_KEY:latest,JWT_SECRET_KEY=JWT_SECRET_KEY:latest"
```

## STRETCH (no comprometido, +2 SP)

- Módulos parametrizados por entorno (`environments/staging`, `environments/prod`).
- Backend de state en bucket GCS versionado (`terraform { backend "gcs" { ... } }`).

## QA Checklist

- [ ] `min_instances = 0` en ambos Cloud Run
- [ ] Secrets vía Secret Manager (`secret_key_ref`), sin valores en el repo
- [ ] Lifecycle 7 días en bucket de exports
- [ ] Variables `project_id`/`region`/imágenes sin defaults sensibles
- [ ] Bootstrap documentado (APIs + service account de deploy)
- [ ] `terraform fmt -check` y `terraform validate` limpios
- [ ] Plan revisado antes de apply
