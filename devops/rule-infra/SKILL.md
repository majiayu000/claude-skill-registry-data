---
name: rule-infra
description: MANDATORY when editing files matching ["infra/**/*.tf"]. When working on Terraform infrastructure in infra/
---

# Infrastructure Rules

## Three-Layer Application Structure
ALWAYS organize each app under `infra/<app_name>/` into three layers: `app-config/`, `service/`, and `database/`. NEVER place resource definitions in `app-config/` or configuration logic in `service/`.

Example from codebase:
```hcl
# From infra/api/app-config/prod.tf
module "prod_config" {
  source      = "./env-config"
  environment = "prod"
  network_name = "prod"
  domain_name  = "api.simpler.grants.gov"
  enable_https = true
}
```

## No AWS Data Sources in app-config
NEVER use AWS API-dependent data sources in `app-config/`. The `app-config` layer runs `terraform plan` in CI without AWS credentials. ALWAYS place AWS data source lookups in `service/`.

Example from codebase:
```hcl
# From infra/frontend/app-config/env-config/environment_variables.tf
NEW_RELIC_CLOUD_AWS_ACCOUNT_ID = "315341936575"
```

## Decomposed Config Outputs
ALWAYS structure `app-config` outputs as separate outputs per domain concern. NEVER combine unrelated concerns into a single monolithic output.

Example from codebase:
```hcl
# From infra/frontend/app-config/env-config/outputs.tf
output "database_config" { value = local.database_config }
output "feature_flags_config" { value = local.feature_flags_config }
output "monitoring_config" { value = local.monitoring_config }
output "domain_config" { value = local.domain_config }
output "service_config" { value = local.service_config }
```

## Feature-Gated Resources via count and Booleans
ALWAYS use `count = var.enable_<feature> ? 1 : 0` to conditionally create resources. ALWAYS define gating variables with `type = bool` and `default = false`. ALWAYS use indexed access `[0]` on conditional resource references.

Example from codebase:
```hcl
# From infra/modules/service/variables.tf
variable "enable_api_gateway" {
  description = "Whether to enable API Gateway for the service"
  type        = bool
  default     = false
}

# From infra/modules/service/api_gateway.tf
resource "aws_api_gateway_rest_api" "api" {
  count = var.enable_api_gateway ? 1 : 0
  name  = var.service_name
}
```

## Separate IAM Policy Documents Per Concern
ALWAYS create separate policy documents per IAM concern. ALWAYS attach runtime permissions to `app_service` role, NEVER to `task_executor`.

Example from codebase:
```hcl
# From infra/modules/service/access_control.tf
resource "aws_iam_role_policy_attachment" "email_access" {
  role       = aws_iam_role.app_service.name
  policy_arn = aws_iam_policy.email_access[0].arn
}
```

## Restrict Security Group Egress
NEVER allow unrestricted outbound traffic (`protocol = "-1"`). ALWAYS restrict egress to specific ports (443, 80, 5432).

Example from codebase:
```hcl
# From infra/modules/service/main.tf
resource "aws_security_group" "app" {
  egress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

## Two-Tier Environment Variables (Plain + SSM Secrets)
ALWAYS manage env vars through `app-config/env-config/environment_variables.tf`. Plain values go in `default_extra_environment_variables`. Sensitive values go in `secrets` with `manage_method = "manual"` and SSM path `/<app_name>/<environment>/<secret-name>`. NEVER create custom SSM parameter resources outside this pattern.

Example from codebase:
```hcl
# From infra/nofos/app-config/env-config/environment_variables.tf
locals {
  secrets = {
    API_TOKEN = {
      manage_method     = "manual"
      secret_store_name = "/nofos/${var.environment}/api-token"
    }
  }
}
```

## Feature Flags as SSM-Backed Secrets
ALWAYS define feature flags using `FEATURE_<NAME>_ON` or `FEATURE_<NAME>_OFF` with `manage_method = "manual"` and SSM path `/<app>/<env>/feature-<kebab-name>`. NEVER set feature flags in `.env` files for deployed environments.

Example from codebase:
```hcl
# From infra/frontend/app-config/env-config/environment_variables.tf
FEATURE_USER_ADMIN_OFF = {
  manage_method     = "manual"
  secret_store_name = "/${var.app_name}/${var.environment}/feature-user-admin-off"
},
```

## Shared Reusable Modules
ALWAYS place reusable components in `infra/modules/<module_name>/`. ALWAYS consume from the `service/` layer. ALWAYS include `main.tf`, `variables.tf`, and `outputs.tf`.

Example from codebase:
```hcl
# From infra/api/service/sqs.tf
module "sqs_queue" {
  source = "../../modules/sqs-queue"
  name   = "${local.prefix}${local.sqs_config.queue_name}"
}
```

## Variable Declarations
ALWAYS declare variables with `type`, `description`, and `default` for optional vars. ALWAYS use `snake_case`. ALWAYS prefer variables over locals for per-environment configuration.

Example from codebase:
```hcl
# From infra/modules/sqs-queue/variables.tf
variable "sqs_visibility_timeout_seconds" {
  description = "The visibility timeout for the SQS queue in seconds"
  type        = number
  default     = 600
}
```

## Checkov Skip Annotations
ALWAYS add a `checkov:skip` comment with the rule ID and a GitHub issue link or explanation. NEVER skip a Checkov rule without documenting why.

Example from codebase:
```hcl
# From infra/modules/service/api_gateway.tf
resource "aws_api_gateway_rest_api" "api" {
  count = var.enable_api_gateway ? 1 : 0
  name  = var.service_name
  # checkov:skip=CKV_AWS_237: Address in future work
}
```

## Lock Files Committed
ALWAYS commit `.terraform.lock.hcl` files for each deployable layer. Provider upgrades MUST appear as lock file diffs in PRs.

## No Duplicate Resource Definitions
NEVER define the same data source or resource under multiple names. ALWAYS consolidate duplicates and update all references.

## No Fragile String Matching
NEVER use `startswith()` or string matching on `var.service_name` for conditional logic. ALWAYS use explicit boolean variables.

---

## Context Enrichment

When generating significant infrastructure code (new module, new environment config, security changes), enrich your context:
- Call `get_architecture_section("infrastructure")` from the `simpler-grants-context` MCP server to understand infrastructure architectural principles
- Call `get_rule_detail("ci-cd")` for CI/CD integration patterns that infrastructure changes affect
- Consult **Compound Knowledge** for indexed documentation on infrastructure ADRs, FedRAMP requirements, and environment configuration patterns

## Related Rules

When working on Terraform infrastructure, also consult these related rules:
- **`ci-cd.mdc`** — CI/CD pipeline patterns, path-filtered triggers, environment promotion
- **`cross-domain.mdc`** — feature flags via SSM, environment variable conventions

## Specialist Validation

When generating or significantly modifying infrastructure code:

**For simple changes (adding an environment variable, updating a tag):**
No specialist invocation needed — the directives in this rule file are sufficient.

**For moderate changes (new resource, new security group rule, new IAM policy):**
Invoke `deployment-verification-agent` to validate deployment safety.

**For complex changes (new module, new service layer, security architecture changes):**
Invoke the following specialists (run in parallel where possible):
- `deployment-verification-agent` — deployment safety, rollback capability, zero-downtime concerns
- `security-sentinel` — infrastructure security (security groups, IAM policies, secret management)
- `architecture-strategist` — three-layer structure compliance, module boundaries
