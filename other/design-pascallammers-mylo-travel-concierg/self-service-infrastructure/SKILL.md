---
name: self-service-infrastructure
description: Use when designing infrastructure self-service portals, IaC templates, or automated provisioning systems. Covers Terraform modules, Pulumi, environment provisioning, and infrastructure guardrails.
allowed-tools: Read, Glob, Grep
---

# Self-Service Infrastructure

Patterns for enabling developers to provision infrastructure without tickets, while maintaining governance and control.

## When to Use This Skill

- Designing infrastructure self-service capabilities
- Creating reusable Terraform/Pulumi modules
- Building environment provisioning systems
- Implementing infrastructure guardrails
- Reducing infrastructure request bottlenecks
- Balancing developer autonomy with governance

## Self-Service Fundamentals

### What is Self-Service Infrastructure?

```text
Self-Service Infrastructure:
Enabling developers to provision and manage infrastructure
directly, without filing tickets or waiting for ops teams.

Traditional Model:
┌─────────────────────────────────────────────────────────────┐
│ Developer → Ticket → Ops Review → Manual Provision → Done  │
│                                                              │
│ Timeline: Days to weeks                                      │
│ Bottleneck: Ops team capacity                               │
│ Result: Shadow IT, workarounds, frustration                 │
└─────────────────────────────────────────────────────────────┘

Self-Service Model:
┌─────────────────────────────────────────────────────────────┐
│ Developer → Portal/API → Automatic Provision → Done         │
│                                                              │
│ Timeline: Minutes to hours                                  │
│ Bottleneck: None (automated)                                │
│ Result: Speed, consistency, compliance                      │
└─────────────────────────────────────────────────────────────┘

Self-Service Spectrum:
├── Fully Managed: Click a button, get a database
├── Template-Based: Customize from approved templates
├── Policy-Constrained: Write IaC within guardrails
└── Full Freedom: Any infrastructure (risky)

Sweet Spot: Template-Based with Policy Guardrails
```

### Key Benefits

```text
Self-Service Benefits:

For Developers:
├── Speed: Minutes instead of days
├── Autonomy: Provision when needed
├── Consistency: Same infrastructure every time
├── Learning: Understand infrastructure better
└── Ownership: More responsibility, more control

For Operations:
├── Scale: Handle more requests without more people
├── Consistency: Enforce standards automatically
├── Focus: Work on platform, not tickets
├── Audit: Clear trail of who provisioned what
└── Compliance: Built-in policy enforcement

For Organization:
├── Velocity: Faster time to market
├── Cost: Reduced ops overhead
├── Governance: Better compliance posture
├── Security: Consistent security controls
└── Efficiency: Resources provisioned when needed
```

## Self-Service Architecture

### Component Architecture

```text
Self-Service Infrastructure Architecture:

┌─────────────────────────────────────────────────────────────┐
│                     USER INTERFACE                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   Portal    │  │    CLI      │  │    API      │         │
│  │   (Web UI)  │  │ (Terraform) │  │  (REST/gRPC)│         │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘         │
│         └────────────────┼────────────────┘                 │
│                          │                                   │
├──────────────────────────┼───────────────────────────────────┤
│                          ▼                                   │
│  ┌─────────────────────────────────────────────────────┐    │
│  │               ORCHESTRATION LAYER                    │    │
│  │  ├── Request validation                              │    │
│  │  ├── Policy evaluation (OPA/Sentinel)               │    │
│  │  ├── Cost estimation                                 │    │
│  │  ├── Approval workflow (if needed)                  │    │
│  │  └── Execution orchestration                        │    │
│  └─────────────────────────────────────────────────────┘    │
│                          │                                   │
├──────────────────────────┼───────────────────────────────────┤
│                          ▼                                   │
│  ┌─────────────────────────────────────────────────────┐    │
│  │               TEMPLATE LIBRARY                       │    │
│  │  ├── Database modules (RDS, Cloud SQL)              │    │
│  │  ├── Compute modules (EKS, GKE, VMs)               │    │
│  │  ├── Storage modules (S3, GCS)                      │    │
│  │  ├── Network modules (VPC, subnets)                 │    │
│  │  └── Composite modules (full environments)          │    │
│  └─────────────────────────────────────────────────────┘    │
│                          │                                   │
├──────────────────────────┼───────────────────────────────────┤
│                          ▼                                   │
│  ┌─────────────────────────────────────────────────────┐    │
│  │               EXECUTION ENGINE                       │    │
│  │  ├── Terraform Cloud/Enterprise                     │    │
│  │  ├── Pulumi Service                                 │    │
│  │  ├── Crossplane                                     │    │
│  │  └── Cloud-native (CDK, ARM, Deployment Manager)   │    │
│  └─────────────────────────────────────────────────────┘    │
│                          │                                   │
├──────────────────────────┼───────────────────────────────────┤
│                          ▼                                   │
│  ┌─────────────────────────────────────────────────────┐    │
│  │               CLOUD PROVIDERS                        │    │
│  │  AWS  │  GCP  │  Azure  │  Kubernetes  │  Others    │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

### Request Flow

```text
Self-Service Request Flow:

┌─────────────────────────────────────────────────────────────┐
│ 1. REQUEST                                                   │
│    Developer: "I need a PostgreSQL database for staging"    │
│    └── Via portal, CLI, or API                              │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. VALIDATION                                                │
│    ├── User has permission?          ✓ Team member          │
│    ├── Request well-formed?          ✓ Valid config         │
│    ├── Within quotas?                ✓ Under team limit     │
│    └── Meets policy?                 ✓ Allowed instance type│
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. ENRICHMENT                                                │
│    ├── Apply defaults                 db.t3.medium          │
│    ├── Generate names                 myapp-staging-db      │
│    ├── Assign network                 staging-vpc           │
│    ├── Configure monitoring           Datadog integration   │
│    └── Estimate cost                  ~$50/month            │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. APPROVAL (if required)                                    │
│    ├── Auto-approve: staging, dev     ✓ Auto-approved       │
│    ├── Manual approve: production     (Would need approval) │
│    └── Cost threshold: >$500/month    (Would need approval) │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. EXECUTION                                                 │
│    ├── Generate Terraform             Based on template     │
│    ├── Plan                           Preview changes       │
│    ├── Apply                          Create resources      │
│    └── Verify                         Health checks         │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│ 6. DELIVERY                                                  │
│    ├── Connection string → Vault                            │
│    ├── Notification → Slack/email                           │
│    ├── Documentation → Auto-generated                       │
│    └── Registration → Service catalog                       │
└─────────────────────────────────────────────────────────────┘
```

## IaC Module Design

### Terraform Module Patterns

```text
Terraform Module Structure:

Organization-Wide Module Library:
terraform-modules/
├── databases/
│   ├── rds-postgres/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   ├── versions.tf
│   │   ├── README.md
│   │   └── examples/
│   │       ├── simple/
│   │       └── production/
│   └── elasticache-redis/
├── compute/
│   ├── eks-cluster/
│   └── ecs-service/
├── storage/
│   └── s3-bucket/
└── network/
    └── vpc/

Module Design Principles:

1. Opinionated Defaults
   # variables.tf
   variable "instance_class" {
     type        = string
     default     = "db.t3.medium"  # Sensible default
     description = "RDS instance type"

     validation {
       condition = can(regex("^db\\.(t3|r5|m5)", var.instance_class))
       error_message = "Only approved instance families allowed."
     }
   }

2. Minimal Required Inputs
   # Only require what can't be defaulted
   variable "name" {
     type        = string
     description = "Database identifier"
   }

   variable "environment" {
     type        = string
     description = "Environment (dev, staging, prod)"
   }

3. Complete Outputs
   # outputs.tf
   output "endpoint" {
     description = "Database connection endpoint"
     value       = aws_db_instance.main.endpoint
   }

   output "connection_secret_arn" {
     description = "ARN of secret with credentials"
     value       = aws_secretsmanager_secret.db_credentials.arn
   }

4. Built-in Best Practices
   # Security hardened by default
   resource "aws_db_instance" "main" {
     # Encryption always on
     storage_encrypted = true

     # No public access
     publicly_accessible = false

     # Automated backups
     backup_retention_period = var.environment == "prod" ? 30 : 7

     # Enhanced monitoring
     monitoring_interval = 60
   }
```

### Module Versioning

```text
Module Versioning Strategy:

Semantic Versioning:
├── MAJOR: Breaking changes (new required inputs, removed outputs)
├── MINOR: New features (new optional inputs, new outputs)
└── PATCH: Bug fixes (no interface changes)

Version Constraints:
# Allow patch updates automatically
module "database" {
  source  = "terraform.company.com/modules/rds-postgres"
  version = "~> 2.1.0"  # >=2.1.0, <2.2.0
}

# Pin to exact version (production)
module "database" {
  source  = "terraform.company.com/modules/rds-postgres"
  version = "= 2.1.3"
}

Deprecation Policy:
┌─────────────────────────────────────────────────────────────┐
│ Module Version Lifecycle                                     │
├─────────────────────────────────────────────────────────────┤
│ Current (v2.x):     Supported, new features                 │
│ Previous (v1.x):    Supported, security fixes only          │
│ Deprecated (v0.x):  Warning on use, no support              │
│ Removed:            Will not work                           │
│                                                              │
│ Notification:                                                │
│ ├── Slack announcement when version deprecated              │
│ ├── Warning in terraform plan output                        │
│ ├── Dashboard showing deprecated module usage               │
│ └── Migration guide provided                                │
└─────────────────────────────────────────────────────────────┘
```

## Policy and Guardrails

### Policy as Code

```text
Policy as Code Options:

1. HashiCorp Sentinel (Terraform Enterprise)
   # Require encryption for all storage
   import "tfplan/v2" as tfplan

   s3_buckets = filter tfplan.resource_changes as _, rc {
     rc.type is "aws_s3_bucket" and
     rc.mode is "managed" and
     (rc.change.actions contains "create" or
      rc.change.actions contains "update")
   }

   encryption_enabled = rule {
     all s3_buckets as _, bucket {
       bucket.change.after.server_side_encryption_configuration
         is not null
     }
   }

   main = rule { encryption_enabled }

2. Open Policy Agent (OPA)
   # Rego policy for Kubernetes
   package kubernetes.admission

   deny[msg] {
     input.request.kind.kind == "Pod"
     container := input.request.object.spec.containers[_]
     not container.securityContext.runAsNonRoot
     msg := "Containers must run as non-root"
   }

3. Cloud-Native Policies
   # AWS Service Control Policy
   {
     "Version": "2012-10-17",
     "Statement": [{
       "Sid": "RequireEncryption",
       "Effect": "Deny",
       "Action": ["s3:CreateBucket"],
       "Resource": "*",
       "Condition": {
         "StringNotEquals": {
           "s3:x-amz-server-side-encryption": "AES256"
         }
       }
     }]
   }
```

### Guardrail Categories

```text
Infrastructure Guardrails:

1. Security Guardrails
   ├── Encryption required (at-rest, in-transit)
   ├── No public access by default
   ├── Required security groups
   ├── IAM role requirements
   └── Vulnerability scanning

2. Cost Guardrails
   ├── Instance type restrictions
   ├── Storage size limits
   ├── Required cost tags
   ├── Budget thresholds
   └── Approval for large resources

3. Compliance Guardrails
   ├── Allowed regions (data residency)
   ├── Required logging
   ├── Backup requirements
   ├── Retention policies
   └── Audit trail requirements

4. Operational Guardrails
   ├── Naming conventions
   ├── Required tags (owner, cost-center)
   ├── Resource quotas per team
   ├── Monitoring requirements
   └── Deletion protection

Guardrail Implementation:
┌─────────────────────────────────────────────────────────────┐
│                    Guardrail Timing                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Pre-Plan (fastest feedback):                               │
│  ├── Validate terraform files                               │
│  ├── Static analysis (tfsec, checkov)                      │
│  └── Module version checks                                  │
│                                                              │
│  Post-Plan (resource-aware):                                │
│  ├── OPA/Sentinel policy evaluation                        │
│  ├── Cost estimation                                        │
│  └── Blast radius assessment                                │
│                                                              │
│  Post-Apply (verification):                                 │
│  ├── Configuration validation                               │
│  ├── Security scanning                                      │
│  └── Compliance audit                                       │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Environment Provisioning

### Environment Templates

```text
Environment Provisioning:

Environment Types:
┌─────────────────────────────────────────────────────────────┐
│ Development Environment                                      │
│ ├── Purpose: Individual developer testing                   │
│ ├── Lifetime: Hours to days                                 │
│ ├── Resources: Minimal (smallest instances)                 │
│ ├── Data: Synthetic or anonymized                           │
│ └── Approval: None (within quota)                           │
├─────────────────────────────────────────────────────────────┤
│ Staging Environment                                          │
│ ├── Purpose: Integration testing, QA                        │
│ ├── Lifetime: Persistent per service                        │
│ ├── Resources: Production-like (scaled down)                │
│ ├── Data: Sanitized production subset                       │
│ └── Approval: None (within quota)                           │
├─────────────────────────────────────────────────────────────┤
│ Production Environment                                       │
│ ├── Purpose: Live customer traffic                          │
│ ├── Lifetime: Permanent                                      │
│ ├── Resources: Full capacity                                │
│ ├── Data: Real customer data                                │
│ └── Approval: Required (security review)                    │
└─────────────────────────────────────────────────────────────┘

Environment Template:
# environment/main.tf
module "network" {
  source      = "../modules/vpc"
  environment = var.environment
  cidr_block  = var.network_cidr
}

module "kubernetes" {
  source      = "../modules/eks"
  environment = var.environment
  vpc_id      = module.network.vpc_id
  node_count  = var.environment == "prod" ? 5 : 2
}

module "database" {
  source         = "../modules/rds"
  environment    = var.environment
  vpc_id         = module.network.vpc_id
  instance_class = var.environment == "prod" ? "db.r5.xlarge" : "db.t3.medium"
  multi_az       = var.environment == "prod"
}

module "cache" {
  source      = "../modules/elasticache"
  environment = var.environment
  vpc_id      = module.network.vpc_id
  node_type   = var.environment == "prod" ? "cache.r5.large" : "cache.t3.micro"
}
```

### Ephemeral Environments

```text
Ephemeral/Preview Environments:

Use Cases:
├── PR preview environments
├── Feature branch testing
├── Demo environments
├── Load testing environments
└── Incident reproduction

Lifecycle:
┌─────────────────────────────────────────────────────────────┐
│                                                              │
│  PR Created ──► Environment Created ──► Tests Run           │
│       │              │                      │               │
│       │              ▼                      ▼               │
│       │         Preview URL            PR Updated           │
│       │         Posted to PR              │                 │
│       │                                   │                 │
│       ▼                                   ▼                 │
│  PR Merged ───────────────────────► Environment Destroyed   │
│                                                              │
│  Timeout: Auto-destroy after 7 days of inactivity          │
│                                                              │
└─────────────────────────────────────────────────────────────┘

Implementation:
# .github/workflows/preview.yml
name: Preview Environment

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  deploy-preview:
    runs-on: ubuntu-latest
    steps:
      - name: Create/Update Environment
        run: |
          terraform workspace select pr-${{ github.event.pull_request.number }} || \
          terraform workspace new pr-${{ github.event.pull_request.number }}
          terraform apply -auto-approve

      - name: Comment Preview URL
        uses: actions/github-script@v6
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              body: '🚀 Preview: https://pr-${{ github.event.pull_request.number }}.preview.company.com'
            })
```

## Technology Options

### Self-Service Platforms

```text
Platform Comparison:

1. Terraform Cloud/Enterprise
   ├── Native Terraform experience
   ├── Policy as Code (Sentinel)
   ├── Private module registry
   ├── Cost estimation
   └── Enterprise features (SSO, audit)

2. Pulumi
   ├── Real programming languages
   ├── Strong typing and IDE support
   ├── Policy as Code (CrossGuard)
   └── Automation API

3. Crossplane
   ├── Kubernetes-native
   ├── GitOps workflow
   ├── Composition for modules
   └── Multi-cloud abstraction

4. Backstage + Terraform
   ├── Unified developer portal
   ├── Software templates
   ├── Plugin ecosystem
   └── Service catalog integration

5. Port/Cortex/OpsLevel
   ├── Commercial developer portals
   ├── Quick to implement
   ├── Built-in integrations
   └── Self-service workflows

Selection Criteria:
┌────────────────────────────────────────────────────────────┐
│ Factor               │ Best Fit                            │
├──────────────────────┼─────────────────────────────────────┤
│ Existing Terraform   │ Terraform Cloud/Enterprise         │
│ Kubernetes-first     │ Crossplane                         │
│ Developer portal     │ Backstage or commercial            │
│ Programming language │ Pulumi                             │
│ Quick start          │ Commercial (Port, OpsLevel)        │
│ Maximum control      │ Build custom                       │
└────────────────────────────────────────────────────────────┘
```

## Cost Management

### Cost Controls

```text
Cost Management in Self-Service:

1. Cost Visibility
   ├── Estimated cost shown before provisioning
   ├── Cost tags automatically applied
   ├── Per-team/project dashboards
   └── Anomaly detection and alerts

2. Cost Guardrails
   ├── Instance type restrictions
   ├── Budget thresholds by team
   ├── Approval required above threshold
   └── Auto-shutdown of unused resources

3. Cost Optimization
   ├── Right-sizing recommendations
   ├── Reserved instance suggestions
   ├── Spot instance for non-production
   └── Scheduled scaling

Cost Estimation Flow:
┌─────────────────────────────────────────────────────────────┐
│ Request: PostgreSQL database for staging                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Cost Estimate:                                             │
│  ├── Compute (db.t3.medium):        $30/month              │
│  ├── Storage (100GB gp3):           $10/month              │
│  ├── Backup storage:                ~$5/month              │
│  └── Data transfer:                 ~$5/month              │
│                                     ─────────               │
│  Estimated Total:                   ~$50/month             │
│                                                              │
│  ✓ Within team budget ($500/month quota)                   │
│  ✓ No approval required                                     │
│                                                              │
│  [Proceed] [Modify] [Cancel]                                │
└─────────────────────────────────────────────────────────────┘
```

## Best Practices

```text
Self-Service Infrastructure Best Practices:

1. Start Small, Expand Gradually
   ├── Begin with 2-3 common resources
   ├── Add based on demand
   ├── Iterate on feedback
   └── Don't try to cover everything day 1

2. Balance Autonomy and Governance
   ├── Guardrails not gates
   ├── Automate approvals where safe
   ├── Clear escalation paths
   └── Trust but verify

3. Optimize for Developer Experience
   ├── Minimal required inputs
   ├── Sensible defaults
   ├── Clear error messages
   └── Fast feedback loops

4. Maintain Module Quality
   ├── Automated testing
   ├── Documentation requirements
   ├── Versioning strategy
   └── Deprecation process

5. Monitor and Improve
   ├── Track provisioning success rate
   ├── Measure time to provision
   ├── Gather user feedback
   └── Identify automation opportunities

6. Handle Edge Cases
   ├── What if provisioning fails?
   ├── How to handle orphaned resources?
   ├── What about existing resources?
   └── How to migrate between versions?
```

## Anti-Patterns

```text
Self-Service Anti-Patterns:

1. "Self-Service Everything"
   ❌ Every possible configuration option
   ✓ Curated set of approved patterns

2. "Security Theater"
   ❌ Manual approvals that don't add value
   ✓ Automated policy enforcement

3. "Configuration Explosion"
   ❌ 50 parameters per resource
   ✓ Sensible defaults with few overrides

4. "Ignore Cost"
   ❌ No visibility into provisioned cost
   ✓ Cost estimation and budgets

5. "Build vs Buy Wrong"
   ❌ Building everything from scratch
   ✓ Use existing tools where appropriate

6. "No Escape Hatch"
   ❌ Blocking legitimate exceptions
   ✓ Process for justified deviations
```

## Related Skills

- `internal-developer-platform` - Platform engineering overview
- `golden-paths` - Standardized workflows
- `container-orchestration` - Kubernetes infrastructure
- `serverless-patterns` - Serverless infrastructure
