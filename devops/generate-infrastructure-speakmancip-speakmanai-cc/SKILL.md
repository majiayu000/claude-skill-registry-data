---
name: generate-infrastructure
description: Generate Terraform infrastructure code (GCP/AWS/Azure) and apply pre-pentest application security hardening for a Phase 3 codebase. Use for Phase 4 of the SPEAKMAN.AI SDLC, after code generation and before pentest or environment promotion.
---

# generate-infrastructure — Phase 4: Terraform + Pre-Pentest Hardening

You generate Terraform infrastructure code and apply pre-pentest application security hardening to a Phase 3 codebase. You work in three sequential gates: reconcile the architecture against the target cloud, harden the application code, then generate Terraform. You do not deploy — you produce files a human reviews and applies.

---

## Step 0 — Collect Inputs

Ask the user:

> "Provide the following paths:
> 1. Phase 1 SAD output directory (contains `raw/` with SAD agent outputs) — or press Enter to skip if you have no SAD
> 2. Phase 2 requirements output directory (contains `raw/` with coding contracts) — or press Enter to skip
> 3. Project root (the Phase 3 codebase directory)
> 4. Target cloud provider: GCP, AWS, or Azure"

Store:
- **SAD_DIR**: path or null
- **REQ_DIR**: path or null
- **PROJECT_ROOT**: absolute path to the codebase
- **TARGET_CLOUD**: `GCP`, `AWS`, or `Azure`

---

## Step 1 — Load Context

Read everything before drawing any conclusions. Do not guess.

### 1a — SAD (if provided)

Read these files from `{SAD_DIR}/raw/` (skip any absent):
- `technical_solution_architect.txt` → **SAD_TECH**: infrastructure decisions, deployment strategy, ADRs, chosen cloud services
- `business_application_architect.txt` → **SAD_ARCH**: component catalog, data flows
- `compliance_officer.txt` → **SAD_COMPLIANCE**: compliance requirements, security controls mandated

### 1b — Requirements contracts (if provided)

Read from `{REQ_DIR}/raw/` (skip any absent):
- `api_schema.txt` → **REQ_API**: all endpoints, auth requirements, input schemas
- `database_schema.txt` → **REQ_DB**: tables/collections, data types, indexes
- `test_strategy.txt` → **REQ_TESTS**: test tooling (used to determine test runner in build scripts)

### 1c — Codebase scan

Scan the project root. Read:

1. **Service discovery**: find all directories containing a `package.json`, `requirements.txt`, `go.mod`, `Gemfile`, or `composer.json`. Each is a **service**. Store as **SERVICES** list with: `{ name, path, runtime, framework }`.

2. **Entry points**: for each service, find the main entry file (e.g. `src/main.py`, `src/main.js`, `server.js`, `app.py`, `index.js`). Read it.

3. **Docker**: find all `Dockerfile` and `docker-compose.yml` files. Note which services have them.

4. **Environment config**: read all `.env.example` files. List every environment variable each service expects. Do not read `.env` files.

5. **Auth mechanism**: grep for JWT, session, API key, OAuth patterns. Note where tokens are verified and which middleware protects routes.

6. **CORS config**: find current CORS configuration. Note the allowed origin — hardcoded or env var.

7. **Security middleware**: check whether security headers middleware exists (Helmet, custom FastAPI middleware, Django SecurityMiddleware, etc.).

8. **Rate limiting**: check whether rate limiting is applied to auth endpoints.

9. **External integrations**: grep for AI/LLM API calls, payment SDKs, OAuth providers, cloud SDK calls. These determine IAM scope.

Build **INFRA_CONTEXT**:
```
Services: [list]
Runtimes: [list]
Has Dockerfile: yes/no per service
DB type: postgres / mysql / mongodb / sqlite / etc.
Auth: JWT / sessions / API key / etc.
CORS origin: hardcoded "{value}" | env var {VAR_NAME} | absent
Security headers: present / absent
Rate limiting on auth: present / absent
External APIs: [list]
```

---

## Step 2 — Platform Reconciliation

Compare what the SAD specified (if provided) against what exists in the codebase and where the user wants to deploy.

Build a substitution table. For each architectural component identified, map:
- **SAD Platform** (what was originally designed — from SAD_TECH, or inferred from codebase if no SAD)
- **Target Platform** (the equivalent service on TARGET_CLOUD)
- **Change required** (code change, config change, or none)

Standard substitution mappings:

| Component | GCP | AWS | Azure |
|---|---|---|---|
| Container compute | Cloud Run | ECS Fargate / App Runner | Container Apps |
| Managed Postgres | Cloud SQL (postgres) | RDS PostgreSQL | Azure Database for PostgreSQL |
| Managed MySQL | Cloud SQL (mysql) | RDS MySQL | Azure Database for MySQL |
| MongoDB | Atlas (external) or Firestore | DocumentDB / Atlas | Cosmos DB / Atlas |
| Object storage | GCS | S3 | Azure Blob Storage |
| Secrets manager | Secret Manager | Secrets Manager | Key Vault |
| Container registry | Artifact Registry | ECR | ACR |
| CDN / load balancer | Cloud Load Balancing + Cloud Armor | ALB + WAF | Application Gateway |
| DNS | Cloud DNS | Route 53 | Azure DNS |
| Remote Terraform state | GCS bucket | S3 + DynamoDB | Azure Blob |
| Service identity | Service Account | IAM Role | Managed Identity |

Present the table to the user and ask:
> "Here is how I'll map your architecture to {TARGET_CLOUD}. Confirm or tell me what to change."

On confirmation, store final decisions as **PLATFORM_DECISIONS**.

---

## Step 3 — Pre-Pentest Security Hardening

Apply these fixes before generating Terraform. A pentest will probe all of these — fix the obvious ones now so the test surfaces real vulnerabilities, not low-hanging-fruit noise.

Work through each check. For each: read the relevant code, report what you find, apply the fix if one is needed, and note what Terraform will handle separately.

### 3.1 Security Headers

**What to check**: is security headers middleware present and configured?

**Fix for Node.js / Express:**
- If `helmet` is not in `package.json`, add it: `npm install helmet`
- In the main Express app file, add before all routes:
  ```javascript
  const helmet = require('helmet')
  app.use(helmet({
    contentSecurityPolicy: {
      directives: {
        defaultSrc: ["'self'"],
        scriptSrc: ["'self'"],
        styleSrc: ["'self'", "'unsafe-inline'"],
        imgSrc: ["'self'", "data:"],
        connectSrc: ["'self'"],
        frameAncestors: ["'none'"],
      }
    },
    hsts: { maxAge: 31536000, includeSubDomains: true, preload: true },
  }))
  ```

**Fix for FastAPI / Python:**
- Add a middleware function to the main FastAPI app:
  ```python
  from fastapi import Request
  from fastapi.responses import Response

  @app.middleware('http')
  async def add_security_headers(request: Request, call_next):
      response = await call_next(request)
      response.headers['X-Content-Type-Options'] = 'nosniff'
      response.headers['X-Frame-Options'] = 'DENY'
      response.headers['X-XSS-Protection'] = '1; mode=block'
      response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
      response.headers['Permissions-Policy'] = 'camera=(), microphone=(), geolocation=()'
      response.headers['Content-Security-Policy'] = (
          "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; "
          "img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'"
      )
      return response
  ```

**Fix for Django:** verify `django.middleware.security.SecurityMiddleware` is first in `MIDDLEWARE` and `SECURE_BROWSER_XSS_FILTER = True`, `X_FRAME_OPTIONS = 'DENY'`, `SECURE_CONTENT_TYPE_NOSNIFF = True` are set.

Note in report: HSTS with preload and minimum TLS version are enforced at the load balancer level via Terraform — do not enforce `Strict-Transport-Security` in the app if TLS is terminated at the load balancer.

---

### 3.2 CORS Configuration

**What to check**: is the allowed origin hardcoded, a wildcard, or read from an environment variable?

**Rule**: CORS allowed origin must always be an environment variable. Wildcard `*` on an authenticated API is a FAIL.

**Fix**: if the origin is hardcoded or wildcard, replace it with an env var read at startup. Ensure the env var is listed in `.env.example` with a description.

**Node.js / Express example:**
```javascript
const cors = require('cors')
app.use(cors({
  origin: process.env.CORS_ORIGIN,
  credentials: true,
}))
```

**FastAPI example:**
```python
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.environ['CORS_ORIGIN']],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
```

The Terraform `{env}.tfvars` will set `CORS_ORIGIN` to the correct frontend domain per environment.

---

### 3.3 Rate Limiting on Authentication Endpoints

**What to check**: are login, register, password reset, and token refresh endpoints rate-limited?

**Fix for Express:**
- If `express-rate-limit` is not installed, add it.
- Apply a strict limiter to auth routes only:
  ```javascript
  const rateLimit = require('express-rate-limit')
  const authLimiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 10,
    message: { error: 'TOO_MANY_REQUESTS', message: 'Too many attempts, try again later.' },
    standardHeaders: true,
    legacyHeaders: false,
  })
  // Apply to auth routes specifically, not all routes
  app.use('/api/auth', authLimiter)
  ```

**Fix for FastAPI:**
- If `slowapi` is not installed, add it to `requirements.txt`.
  ```python
  from slowapi import Limiter
  from slowapi.util import get_remote_address
  limiter = Limiter(key_func=get_remote_address)
  app.state.limiter = limiter

  @router.post('/login')
  @limiter.limit('10/15minutes')
  async def login(request: Request, ...):
  ```

Note: Terraform will provision Cloud Armor / WAF rules for volumetric DDoS. This rate limiter handles application-level brute force — both are needed.

---

### 3.4 Request Body Size Limits

**What to check**: is an explicit body size limit configured? Default Express limit is 100kb (usually fine), default FastAPI is unlimited (not fine).

**Fix for FastAPI**: add `ContentSizeLimitMiddleware` or enforce limits at the nginx/load balancer level. Note in report that Terraform will configure the load balancer with a max body size.

**Fix for Express**: confirm `express.json({ limit: '1mb' })` or similar is set.

---

### 3.5 Error Response Sanitization

**What to check**: do 500 error handlers forward `error.message` or stack traces to the client?

**Fix**: ensure unhandled error handlers return a static message:
- Node: `res.status(500).json({ error: 'INTERNAL_ERROR', message: 'Internal server error' })`
- FastAPI: the `@app.exception_handler(Exception)` must return a static string — `str(exc)` is a FAIL.

---

### 3.6 Secrets — Environment Variable Audit

**What to check**: read all `.env.example` files. Identify every secret value (DB password, JWT secret, API keys). These must move to the secrets manager in Terraform — they should not live in container environment variables in production.

**Do not change application code for this** — the app already reads from env vars. The change is in Terraform: instead of injecting the value directly as a Cloud Run env var, Terraform creates a Secret Manager secret and grants the service account access to it. Cloud Run then mounts it as an env var from Secret Manager at runtime.

List each secret and mark it as: **→ Terraform: Secret Manager** in the report.

---

### 3.7 Authentication Header Validation

**What to check**: does any protected endpoint accidentally trust a client-supplied user ID or role from the request body or query param instead of from the verified token?

Grep for patterns like `req.body.userId`, `request.query.role`, `req.body.isAdmin` being used for authorization decisions (rather than from the decoded JWT payload). Flag any found for manual review — do not auto-fix.

---

## Step 4 — Generate Terraform

Create the directory structure at `{PROJECT_ROOT}/infra/`:

```
infra/
  terraform/
    providers.tf
    backend.tf
    variables.tf
    outputs.tf
    main.tf
    modules/
      networking/     (if VPC required — always for AWS/Azure; GCP uses serverless VPC connector)
      compute/        (one module covering all services)
      database/       (if a managed DB is in PLATFORM_DECISIONS)
      storage/        (if object storage is in PLATFORM_DECISIONS)
      secrets/        (secrets manager resources)
      iam/            (service accounts and permissions)
    environments/
      dev.tfvars
      stg.tfvars
      prod.tfvars
  scripts/
    build.sh          (Docker build + registry push)
    deploy.sh         (terraform plan/apply wrapper)
```

Generate every file using the Write tool. Do not produce incomplete stubs — every resource must have all required attributes set.

---

### 4a — providers.tf

Lock provider versions explicitly.

**GCP:**
```hcl
terraform {
  required_version = ">= 1.5"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}
```

**AWS:**
```hcl
terraform {
  required_version = ">= 1.5"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}
```

**Azure:**
```hcl
terraform {
  required_version = ">= 1.5"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}
```

---

### 4b — backend.tf

Remote state keeps Terraform state out of the repo.

**GCP** (GCS bucket — create the bucket manually before first `terraform init`):
```hcl
terraform {
  backend "gcs" {
    bucket = "${var.project_id}-tfstate"
    prefix = "terraform/state"
  }
}
```

**AWS** (S3 + DynamoDB lock):
```hcl
terraform {
  backend "s3" {
    bucket         = "${var.project_name}-tfstate"
    key            = "terraform.tfstate"
    region         = var.aws_region
    dynamodb_table = "${var.project_name}-tfstate-lock"
    encrypt        = true
  }
}
```

**Azure** (Azure Blob):
```hcl
terraform {
  backend "azurerm" {
    resource_group_name  = "${var.project_name}-tfstate-rg"
    storage_account_name = "${var.project_name}tfstate"
    container_name       = "tfstate"
    key                  = "terraform.tfstate"
  }
}
```

---

### 4c — variables.tf

Declare every variable used across all modules. Include a `description` and `type` on each. Sensitive variables (`db_password`, `jwt_secret`) get `sensitive = true` — but these will be created by Terraform in the secrets manager, not passed in as tfvars.

Required variables for every provider:
- `environment` (string) — `dev`, `stg`, `prod`
- `project_name` (string) — used for resource naming
- Provider-specific: `project_id` + `region` for GCP; `aws_region` for AWS; `location` for Azure
- `cors_origin` (string) — frontend URL per environment
- `db_instance_tier` (string) — machine size for DB (varies by environment)
- `min_instances` / `max_instances` (number) — compute scaling per environment

---

### 4d — modules/iam/

Create a dedicated service account / managed identity for the application with least-privilege permissions.

**GCP:**
```hcl
resource "google_service_account" "app" {
  account_id   = "${var.project_name}-app-sa"
  display_name = "${var.project_name} Application Service Account"
}

# Grant Secret Manager access
resource "google_project_iam_member" "secret_accessor" {
  project = var.project_id
  role    = "roles/secretmanager.secretAccessor"
  member  = "serviceAccount:${google_service_account.app.email}"
}

# Grant Cloud SQL access (if applicable)
resource "google_project_iam_member" "cloudsql_client" {
  project = var.project_id
  role    = "roles/cloudsql.client"
  member  = "serviceAccount:${google_service_account.app.email}"
}
```

Do NOT grant `roles/editor` or `roles/owner`. Only grant the specific roles each service needs.

---

### 4e — modules/secrets/

For each secret identified in Step 3.6, create a Secret Manager / Secrets Manager / Key Vault secret. The secret VALUE is set outside Terraform (manually or via CI) — Terraform creates the resource and grants access.

**GCP example (one resource per secret):**
```hcl
resource "google_secret_manager_secret" "jwt_secret" {
  secret_id = "${var.project_name}-jwt-secret"
  replication {
    auto {}
  }
}

# Grant the app service account read access
resource "google_secret_manager_secret_iam_member" "jwt_secret_accessor" {
  secret_id = google_secret_manager_secret.jwt_secret.secret_id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${var.app_service_account_email}"
}
```

Secrets to create: derive from Step 3.6 list (JWT secret, DB password, any external API keys).

---

### 4f — modules/database/

Provision the managed database identified in PLATFORM_DECISIONS.

**GCP Cloud SQL (PostgreSQL):**
```hcl
resource "google_sql_database_instance" "main" {
  name             = "${var.project_name}-${var.environment}-db"
  database_version = "POSTGRES_15"
  region           = var.region
  deletion_protection = var.environment == "prod" ? true : false

  settings {
    tier = var.db_instance_tier   # e.g. "db-f1-micro" for dev, "db-g1-small" for stg/prod

    backup_configuration {
      enabled    = true
      start_time = "03:00"
    }

    ip_configuration {
      ipv4_enabled    = false      # No public IP
      private_network = google_compute_network.vpc.id
      require_ssl     = true
    }

    database_flags {
      name  = "log_connections"
      value = "on"
    }
  }
}

resource "google_sql_database" "app_db" {
  name     = var.project_name
  instance = google_sql_database_instance.main.name
}

resource "google_sql_user" "app_user" {
  name     = "${var.project_name}-app"
  instance = google_sql_database_instance.main.name
  password = random_password.db_password.result
}

resource "random_password" "db_password" {
  length  = 32
  special = true
}

# Store generated password in Secret Manager
resource "google_secret_manager_secret_version" "db_password" {
  secret      = var.db_password_secret_id
  secret_data = random_password.db_password.result
}
```

**Key rules:**
- No public IP on the database — private network only
- SSL/TLS required for connections
- `deletion_protection = true` in prod
- Backup enabled
- DB password auto-generated by Terraform and written to Secret Manager — never in tfvars

---

### 4g — modules/compute/

One Cloud Run service (or ECS task / Container App) per service in SERVICES.

**GCP Cloud Run (one resource per service):**
```hcl
resource "google_cloud_run_v2_service" "backend" {
  name     = "${var.project_name}-backend-${var.environment}"
  location = var.region

  template {
    service_account = var.app_service_account_email

    scaling {
      min_instance_count = var.min_instances
      max_instance_count = var.max_instances
    }

    containers {
      image = var.backend_image   # e.g. "us-docker.pkg.dev/{project}/{repo}/backend:{tag}"

      # Non-secret env vars injected directly
      env {
        name  = "ENVIRONMENT"
        value = var.environment
      }
      env {
        name  = "CORS_ORIGIN"
        value = var.cors_origin
      }

      # Secrets injected from Secret Manager
      env {
        name = "JWT_SECRET"
        value_source {
          secret_key_ref {
            secret  = var.jwt_secret_id
            version = "latest"
          }
        }
      }
      env {
        name = "DATABASE_URL"
        value_source {
          secret_key_ref {
            secret  = var.db_url_secret_id
            version = "latest"
          }
        }
      }

      resources {
        limits = {
          cpu    = "1"
          memory = "512Mi"
        }
      }

      startup_probe {
        http_get { path = "/health" }
        initial_delay_seconds = 5
        period_seconds        = 5
        failure_threshold     = 3
      }

      liveness_probe {
        http_get { path = "/health" }
        period_seconds    = 30
        failure_threshold = 3
      }
    }

    vpc_access {
      connector = var.vpc_connector_id
      egress    = "PRIVATE_RANGES_ONLY"
    }
  }
}

# Allow unauthenticated access (the app handles its own auth)
resource "google_cloud_run_v2_service_iam_member" "public" {
  project  = var.project_id
  location = var.region
  name     = google_cloud_run_v2_service.backend.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}
```

Generate one resource block per service in SERVICES. Pass the image reference as a variable so `build.sh` populates it separately from `terraform apply`.

---

### 4h — modules/networking/

**GCP** (Serverless VPC Access Connector — needed for Cloud Run → Cloud SQL private IP):
```hcl
resource "google_compute_network" "vpc" {
  name                    = "${var.project_name}-vpc"
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "app_subnet" {
  name          = "${var.project_name}-app-subnet"
  ip_cidr_range = "10.0.0.0/24"
  region        = var.region
  network       = google_compute_network.vpc.id
}

resource "google_vpc_access_connector" "connector" {
  name          = "${var.project_name}-connector"
  region        = var.region
  ip_cidr_range = "10.8.0.0/28"
  network       = google_compute_network.vpc.name
}
```

**AWS** (VPC + private subnets for ECS + RDS):
Create VPC, two private subnets (multi-AZ), two public subnets (for ALB), internet gateway, NAT gateway, route tables, and security groups. Restrict the DB security group to only accept traffic from the ECS task security group.

**Azure** (Virtual Network for Container Apps + Flexible Server):
Create VNet with delegated subnet for Container Apps and separate subnet for the database with service endpoints.

---

### 4i — environments/

Generate three tfvars files. All three must exist — apply uses the file for the target environment.

**dev.tfvars:**
```hcl
environment      = "dev"
cors_origin      = "http://localhost:5173"
db_instance_tier = "db-f1-micro"   # GCP example
min_instances    = 0               # Scale to zero in dev
max_instances    = 2
```

**stg.tfvars:**
```hcl
environment      = "stg"
cors_origin      = "https://stg.{project_name}.example.com"
db_instance_tier = "db-g1-small"
min_instances    = 1
max_instances    = 5
```

**prod.tfvars:**
```hcl
environment      = "prod"
cors_origin      = "https://{project_name}.example.com"
db_instance_tier = "db-n1-standard-2"
min_instances    = 2
max_instances    = 20
```

Replace placeholder domains with the user's actual domain if discoverable from the SAD.

---

### 4j — scripts/build.sh

```bash
#!/bin/bash
set -euo pipefail

ENV=${1:-dev}
TAG=${2:-latest}

# Load project name from tfvars
PROJECT_NAME=$(grep 'project_name' terraform/variables.tf | head -1 | grep -oP '(?<=default = ").*(?=")')

echo "Building and pushing images for environment: $ENV, tag: $TAG"
```

For GCP: build each service and push to Artifact Registry (`{REGION}-docker.pkg.dev/{PROJECT_ID}/{REPO}/{SERVICE}:{TAG}`).

For AWS: authenticate to ECR and push (`{ACCOUNT_ID}.dkr.ecr.{REGION}.amazonaws.com/{PROJECT_NAME}/{SERVICE}:{TAG}`).

For Azure: authenticate to ACR and push (`{REGISTRY}.azurecr.io/{SERVICE}:{TAG}`).

Include a step to run tests before building: `npm test` or `pytest` depending on runtime. If tests fail, abort the build.

---

### 4k — scripts/deploy.sh

```bash
#!/bin/bash
set -euo pipefail

ENV=${1:-dev}
ACTION=${2:-plan}    # plan or apply

echo "Running terraform $ACTION for environment: $ENV"

cd "$(dirname "$0")/../terraform"

terraform init -reconfigure

if [ "$ACTION" = "plan" ]; then
  terraform plan -var-file="environments/${ENV}.tfvars" -out="${ENV}.tfplan"
  echo ""
  echo "Plan saved to ${ENV}.tfplan. Review above, then run:"
  echo "  ./scripts/deploy.sh $ENV apply"
elif [ "$ACTION" = "apply" ]; then
  if [ -f "${ENV}.tfplan" ]; then
    terraform apply "${ENV}.tfplan"
  else
    echo "No plan file found. Run plan first:"
    echo "  ./scripts/deploy.sh $ENV plan"
    exit 1
  fi
fi
```

Apply requires a previously saved plan file — this forces the human to review before any resources are created.

---

## Step 5 — Report

Output a summary:

```
PHASE 4 — INFRASTRUCTURE & SECURITY HARDENING
Project : {project_name}
Cloud   : {TARGET_CLOUD}
Date    : {today}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PLATFORM SUBSTITUTIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{table of SAD component → Target cloud service, status: No change / Substituted}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECURITY HARDENING — APPLIED TO CODE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ {fix applied} — {file modified}
⚠ {item found but not auto-fixed} — {reason, action needed}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECURITY HARDENING — HANDLED BY TERRAFORM
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ TLS termination at load balancer
✓ DB private IP only (no public access)
✓ Secrets in {Secret Manager / Secrets Manager / Key Vault} — not in container env directly
✓ Least-privilege service account / IAM role
✓ CORS_ORIGIN injected per environment

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TERRAFORM FILES GENERATED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
infra/terraform/providers.tf
infra/terraform/backend.tf
infra/terraform/variables.tf
infra/terraform/outputs.tf
infra/terraform/main.tf
infra/terraform/modules/iam/main.tf
infra/terraform/modules/secrets/main.tf
infra/terraform/modules/database/main.tf
infra/terraform/modules/compute/main.tf
infra/terraform/modules/networking/main.tf
infra/terraform/environments/dev.tfvars
infra/terraform/environments/stg.tfvars
infra/terraform/environments/prod.tfvars
infra/scripts/build.sh
infra/scripts/deploy.sh

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECRETS — SET MANUALLY BEFORE FIRST DEPLOY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
After `terraform apply`, set these secret values manually:
{list each secret name and the CLI command to set its value}

GCP example:
  echo -n "your-value" | gcloud secrets versions add {secret-name} --data-file=-

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
NEXT STEPS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Create the Terraform state bucket (one-time, manual):
   GCP:   gsutil mb gs://{project_id}-tfstate
   AWS:   aws s3 mb s3://{project_name}-tfstate --region {region}
   Azure: az storage account create ...

2. Build and push images:
   ./infra/scripts/build.sh dev latest

3. Plan infrastructure:
   ./infra/scripts/deploy.sh dev plan

4. Review the plan, then apply:
   ./infra/scripts/deploy.sh dev apply

5. Set secret values (see SECRETS section above)

6. Run /promote-environment 1 (local → DEV) to verify the codebase is ready, then repeat
   steps 2-5 targeting `stg` to deploy to STG
7. Run /promote-environment 2 (DEV → STG) against the STG-bound codebase before it goes live
8. Run /pentest and /generate-uat-tests against the STG environment once it is live — STG,
   not DEV, is the target: it is the more stable, closer-to-production environment
9. Any code change made to fix a pentest or UAT finding invalidates the gates already
   passed. Re-run /promote-environment from Level 1, redeploy through DEV and STG again,
   and re-run pentest/UAT against the fresh STG deployment before proceeding
10. Run /promote-environment 3 (STG → PROD) once pentest is clean and UAT is 100% passing
```

---

## Rules

- **Read before writing.** Never generate Terraform for a resource that wasn't identified in Step 1. Every generated resource must trace back to a service, integration, or secret found in the codebase.
- **No secrets in tfvars.** DB passwords and API keys are either auto-generated by Terraform (DB password) or created separately via the secrets manager CLI after apply. They never appear in `.tfvars` files.
- **No public database IPs.** The database is always on a private network. Never add `0.0.0.0/0` to a database security group or IP whitelist.
- **Build and deploy are separate.** The Docker image tag is a Terraform variable — `terraform apply` does not build images. `build.sh` builds and pushes; `deploy.sh` runs Terraform which references the already-pushed image.
- **Least privilege on IAM.** Grant only the specific roles the service account needs. Never use `roles/editor`, `roles/owner`, `FullAccess` policies, or `*` in IAM statements.
- **Three environments always.** Generate dev, stg, and prod tfvars even if the user only asks for one. All three must be present before any apply.
- **Platform decisions are final after Step 2.** Do not change a platform decision in Step 4 without surfacing it to the user.
- **Skip SAD/requirements gracefully.** If SAD_DIR or REQ_DIR is null, infer architecture from the codebase alone. Note in the report what was inferred vs. read from contracts.
