---
name: infrastructure-standards
description: Infrastructure, cloud, and DevOps standards. Use when setting up new projects, configuring cloud resources, or working with IaC.
---

# Infrastructure Standards

## New Project Preferences

When starting new projects, prefer:

- **Terraform** for Infrastructure as Code
- **GCP** (Google Cloud Platform) by default, unless otherwise specified
- **Serverless** architectures that are free when idle (Cloud Run, Cloud Functions)
- **Docker Compose** for local development

## Terraform

### Project Structure
```
infrastructure/
├── main.tf           # Main configuration
├── variables.tf      # Input variables
├── outputs.tf        # Output values
├── providers.tf      # Provider configuration
├── terraform.tfvars  # Variable values (gitignored for secrets)
└── modules/          # Reusable modules
    └── api/
        ├── main.tf
        ├── variables.tf
        └── outputs.tf
```

### Best Practices
- Use remote state (GCS bucket for GCP)
- Lock state files to prevent concurrent modifications
- Use workspaces or separate state files for environments
- Tag all resources consistently
- Use modules for reusable infrastructure

### GCP Provider Setup
```hcl
terraform {
  required_version = ">= 1.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }

  backend "gcs" {
    bucket = "project-terraform-state"
    prefix = "terraform/state"
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}
```

## GCP Services

### Preferred Services (Free When Idle)

| Use Case | Service | Notes |
|----------|---------|-------|
| APIs/Backend | Cloud Run | Scale to zero, pay per request |
| Background Jobs | Cloud Functions | Event-driven, scale to zero |
| Scheduled Tasks | Cloud Scheduler + Cloud Functions | Cron-like scheduling |
| Database | Cloud SQL (small) or Firestore | Firestore has free tier |
| Storage | Cloud Storage | Pay per use |
| Auth | Firebase Auth | Free tier generous |

### Cloud Run Example
```hcl
resource "google_cloud_run_service" "api" {
  name     = "api"
  location = var.region

  template {
    spec {
      containers {
        image = "gcr.io/${var.project_id}/api:latest"

        resources {
          limits = {
            memory = "512Mi"
            cpu    = "1"
          }
        }
      }
    }

    metadata {
      annotations = {
        "autoscaling.knative.dev/minScale" = "0"  # Scale to zero
        "autoscaling.knative.dev/maxScale" = "10"
      }
    }
  }
}
```

## Docker Compose (Local Dev)

### Standard Structure
```yaml
# docker-compose.yml
version: "3.8"

services:
  api:
    build: ./api
    ports:
      - "8000:8000"
    volumes:
      - ./api:/app
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/app
    depends_on:
      - db

  web:
    build: ./web
    ports:
      - "3000:3000"
    volumes:
      - ./web:/app
      - /app/node_modules
    environment:
      - VITE_API_URL=http://localhost:8000

  db:
    image: postgres:15
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=app
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### Best Practices
- Use named volumes for persistent data
- Mount source code for hot reload in development
- Use `.env` files for environment variables (gitignored)
- Include health checks for dependent services
- Use `depends_on` with health conditions when needed

## Environment Management

### Secret Handling
- Never commit secrets to git
- Use `.env` files locally (gitignored)
- Use GCP Secret Manager for production
- Reference secrets in Terraform:

```hcl
data "google_secret_manager_secret_version" "api_key" {
  secret = "api-key"
}

resource "google_cloud_run_service" "api" {
  # ...
  template {
    spec {
      containers {
        env {
          name = "API_KEY"
          value_from {
            secret_key_ref {
              name = google_secret_manager_secret.api_key.secret_id
              key  = "latest"
            }
          }
        }
      }
    }
  }
}
```
