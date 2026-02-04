---
name: infrastructure-as-code
version: "1.0"
description: >
  Manage GCP infrastructure with Terraform using modular patterns and remote state.
  PROACTIVELY activate for: (1) writing Terraform configurations for GCP resources, (2) setting up remote state with GCS backend, (3) creating reusable Terraform modules.
  Triggers: "terraform", "infrastructure as code", "iac"
core-integration:
  techniques:
    primary: ["structured_decomposition"]
    secondary: []
  contracts:
    input: "none"
    output: "none"
  patterns: "none"
  rubrics: "none"
---

# Infrastructure as Code Skill (Terraform)

## Metadata (Tier 1)

**Keywords**: terraform, iac, infrastructure as code, module, state, tfvars

**File Patterns**: *.tf, *.tfvars, terraform.tfstate

**Modes**: gcp_dev, deployment

---

## Instructions (Tier 2)

### Remote State (MANDATORY)

```hcl
terraform {
  backend "gcs" {
    bucket = "my-tf-state"
    prefix = "terraform/prod"
  }

  required_version = ">= 1.5.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}
```

### Modular Structure

```
terraform/
├── environments/
│   ├── dev/
│   ├── staging/
│   └── prod/
└── modules/
    ├── cloud-run/
    ├── vpc/
    └── iam/
```

### Variable Management

```hcl
# variables.tf
variable "project_id" {
  type = string
}

# terraform.tfvars
project_id = "my-project"

# Use in resources
resource "google_cloud_run_service" "app" {
  project = var.project_id
}
```

### Lifecycle Management

```hcl
resource "google_cloud_run_service" "prod" {
  # ...

  lifecycle {
    prevent_destroy = true  # Protect production resources
    create_before_destroy = true  # Zero-downtime updates
  }
}
```

### Module Pattern

```hcl
module "api_service" {
  source = "../../modules/cloud-run"

  service_name = "api"
  image        = var.image_url
  min_instances = 2
  max_instances = 50
}

output "service_url" {
  value = module.api_service.url
}
```

### Best Practices

- Remote state with GCS backend + locking
- Modular design with reusable components
- No hardcoded values (use variables)
- Version pinning for providers
- Lifecycle blocks for critical resources
- Separate environments (dev/staging/prod)
- Variable validation where appropriate

### Workflow

```bash
terraform init       # Initialize
terraform fmt        # Format code
terraform validate   # Syntax check
terraform plan       # Preview changes
terraform apply      # Apply changes
```

### Anti-Patterns
- Local state in team projects
- Monolithic main.tf files
- Hardcoded credentials or secrets
- Using :latest for images
- No lifecycle blocks on production resources
- Mixing environments in same state
