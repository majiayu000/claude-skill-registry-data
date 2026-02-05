---
name: Onboarding Services to Omnistrate
description: Guide users through onboarding applications onto the Omnistrate platform. Currently supports Docker Compose-based services with full deployment lifecycle management. Future support planned for Helm charts, Terraform modules, Kustomize configurations, and Kubernetes operators. Handles service transformation, API parameter configuration, compute/storage setup, and iterative debugging until instances are running.
---

# Onboarding Services to Omnistrate

## When to Use This Skill
- Onboarding applications to Omnistrate platform
- Creating SaaS offerings with multi-tenant infrastructure
- Setting up customer-facing service catalogs
- Building managed services with automated deployment
- Transforming existing applications for cloud delivery

## Supported Onboarding Methods

### Currently Supported
**Docker Compose** - Transform compose files into Omnistrate service definitions
- Use for: Containerized applications with compose specs
- Status: Fully supported with complete workflow

### Future Support (Not Yet Implemented)
- **Helm Charts** - Deploy Kubernetes applications via Helm
- **Terraform Modules** - Infrastructure-as-code based services
- **Kustomize** - Kubernetes configuration management
- **Kubernetes Operators** - Operator-based service management

**Note**: When users ask about Helm, Terraform, Kustomize, or Operators, inform them these are not yet supported by this skill and direct them to https://docs.omnistrate.com/getting-started/overview/ for documentation on these methods.

## Quick Decision Guide

### 1. Check Input Format
- **Docker Compose file** → Continue with this skill (full support)
- **Helm/Terraform/Kustomize/Operators** → Not supported, see https://docs.omnistrate.com/getting-started/overview/

### 2. Determine Architecture Pattern
Count services in your compose file:
- **1 service** → Single service pattern (simpler, service is root)
- **2+ services** → Multi-service pattern (requires synthetic root service)

### 3. What is a Synthetic Root Service?
For multi-service applications, Omnistrate requires one "parent" service to coordinate all others. This parent:
- Uses special `omnistrate/noop` image (no actual workload)
- Serves as entry point for all API parameters
- Holds backup configuration
- Orchestrates children via `depends_on` relationships

## Docker Compose Workflow

**Quick Start**: Verify cloud account → Create `-omnistrate.yaml` → Add service plan → Transform services (NO PARAMETERS) → Build → Deploy → Debug until RUNNING → Add parameters when user requests customization

**CRITICAL RULES**:
1. **ALWAYS start with ZERO parameterization** - Use hardcoded values for everything. Only add API parameters AFTER initial deployment succeeds AND user explicitly requests customization.
2. **ALWAYS use `hostedDeployment`** - This deploys YOUR SaaS service in YOUR provider cloud account (not Omnistrate's account, not customer accounts). Only use `byoaDeployment` if user wants to OFFER BYOC as an option to their customers.

### 1. Preparation
**Analyze compose file structure** (Docker Compose only):
- Count services (determines single vs multi-service pattern)
- Identify service dependencies (depends_on chains)
- Map environment variables for parameterization
- Determine stateful services (volumes, databases)

**Verify cloud accounts**:
```bash
mcp__ctl__account_list
mcp__ctl__account_describe account-name="<name>"
```
Extract account IDs, bootstrap roles, project IDs for service plan configuration.

**Determine deployment model** (ALWAYS use hostedDeployment unless specified):
- **ALWAYS DEFAULT** → Use `hostedDeployment` (deploy in YOUR PROVIDER account - this is where YOUR SaaS service runs)
- **ONLY if user explicitly wants to OFFER BYOC to their customers** → Use `byoaDeployment` (allows YOUR CUSTOMERS to deploy in THEIR accounts)
- **ONLY if user wants on-premise** → Use `onPremDeployment`

**CRITICAL**: `hostedDeployment` means deploying in YOUR (the SaaS provider's) account, NOT Omnistrate's account. This is the standard SaaS model. BYOC is for when you want to OFFER customers the option to deploy in THEIR accounts.

### 2. Transformation
**Never modify original compose file** - create new `-omnistrate.yaml` file

**Search documentation before every extension**:
```bash
mcp__ctl__docs_compose_spec_search query="<extension-name>"
mcp__ctl__docs_system_parameters  # For $sys.* variable paths
```

**Test image accessibility** (for custom images from SA handoff):
For each custom image (non-public like postgres, nginx, etc.), test if publicly accessible:
```bash
# Create temporary Docker config to test without local credentials
TEMP_DOCKER_CONFIG=$(mktemp -d)
DOCKER_CONFIG=$TEMP_DOCKER_CONFIG docker pull <image>:<tag> 2>&1
rm -rf $TEMP_DOCKER_CONFIG
```

If pull succeeds: Image is public (no auth needed)
If pull fails with auth error: Image is private (need to configure auth)

**Service architecture decision**:
- Single service (count = 1): Mark service with `x-omnistrate-mode-internal: false`
- Multi-service (count ≥ 2): Create synthetic root service using `omnistrate/noop` image

**Key transformations** (STRICT ORDER - no parameters initially):

**Phase 1: Initial Build** (ZERO parameterization - get working deployment first):
1. **Test image accessibility and configure registry authentication** (if needed):

   **For each custom image** (skip public images like postgres, nginx, redis):

   a. **Test if image is publicly accessible**:
   ```bash
   TEMP_DOCKER_CONFIG=$(mktemp -d)
   DOCKER_CONFIG=$TEMP_DOCKER_CONFIG docker pull mycompany/api:v1.0.0 2>&1
   rm -rf $TEMP_DOCKER_CONFIG
   ```

   - If succeeds: Image is public, skip to next image
   - If fails with "unauthorized" or "denied": Image is private, continue to step b

   b. **Identify registry type and ask for credentials**:

   **Docker Hub (docker.io)**:
   - Ask: "What is your Docker Hub username?"
   - Ask: "Please create a Docker Hub Personal Access Token (PAT) at https://hub.docker.com/settings/security with read permissions. Once created, what should I name the secret in Omnistrate?" (suggest: `DOCKERHUB_PASSWORD`)

   **GitHub Container Registry (ghcr.io)**:
   - Ask: "What is your GitHub username or organization?"
   - Ask: "Please create a GitHub PAT at https://github.com/settings/tokens with `read:packages` scope. What should I name the username and token secrets?" (suggest: `GITHUB_USERNAME`, `GITHUB_TOKEN`)

   **AWS ECR / GCP Artifact Registry / Azure ACR / Custom**:
   - Ask: "What is the username for this registry?"
   - Ask: "What should I name the password secret in Omnistrate?" (suggest: `REGISTRY_PASSWORD`)

   c. **Guide customer to create Omnistrate secrets**:
   ```
   I need you to create these secrets in Omnistrate:

   1. Log into Omnistrate console: https://omnistrate.cloud
   2. Navigate to: Services → [Your Service] → Environments → Dev → Secrets
   3. Click "Add Secret"
   4. Name: DOCKERHUB_PASSWORD (use exact name I suggested)
   5. Value: [Paste your Docker Hub PAT here]
   6. Click Save
   7. Repeat steps 2-6 for Prod environment (same secret name, same value)

   Let me know when you've created the secret(s).
   ```

   d. **Add `x-omnistrate-image-registry-attributes` section to compose file**:

   Search docs first: `mcp__ctl__docs_compose_spec_search query="x-omnistrate-image-registry-attributes"`

   Add at TOP LEVEL of compose (same level as `version:` and `services:`):
   ```yaml
   version: '3.8'

   x-omnistrate-image-registry-attributes:
     docker.io:  # Include ONLY if using private docker.io images
       auth:
         username: mycompany  # Customer's username
         password: {{ $secret.DOCKERHUB_PASSWORD }}
     ghcr.io:  # Include ONLY if using private ghcr.io images
       auth:
         username: {{ $secret.GITHUB_USERNAME }}
         password: {{ $secret.GITHUB_TOKEN }}
     registry.company.com:  # Include ONLY if using custom private registry
       auth:
         username: registryuser
         password: {{ $secret.PRIVATE_REGISTRY_PASSWORD }}

   services: [...]
   ```

   **Important**:
   - Include ONLY registries with private images (don't add unused registries)
   - Registry hostname must match image URLs (e.g., `docker.io` for `mycompany/api:tag`)
   - Username can be hardcoded OR use `{{ $secret.NAME }}`
   - Password/token MUST use `{{ $secret.NAME }}` syntax

2. Add service plan with real cloud account values (ALWAYS use `hostedDeployment` unless specified)
   - **ALWAYS USE `hostedDeployment`** (deploy in YOUR provider account - standard SaaS model)
   - **Only use `byoaDeployment`** if user explicitly says "I want to OFFER BYOC to my customers"
   - **Only use `onPremDeployment`** if user explicitly says "on-premise deployment"

   **CRITICAL DISTINCTION**:
   - `hostedDeployment` = Infrastructure in YOUR account (the SaaS provider) where your service runs
   - `byoaDeployment` = OPTION for YOUR CUSTOMERS to deploy in THEIR accounts (BYOC offering)
   - These are NOT mutually exclusive - you can offer both deployment models to different customer tiers
3. Create/configure root service (multi-service apps)
4. Mark child services as internal (`x-omnistrate-mode-internal: true`)
5. **NO API parameters** - use hardcoded values for everything:
   - Passwords: Use defaults like `"ChangeMe123!"`
   - Replica counts: Use fixed numbers like `replicaCount: 3`
   - Storage sizes: Use hardcoded numbers like `instanceStorageSizeGi: 100`
   - Environment variables: Hardcode all values
5. Configure compute resources per service (fixed replicaCount, simple instanceTypes)
6. Transform volumes to `x-omnistrate-storage` (numeric sizes, hardcoded)
7. Add basic capabilities (enableMultiZone, simple backups)
8. **BUILD AND VALIDATE** - must succeed
9. **DEPLOY instance** - must reach RUNNING status
10. **STOP** - do not add parameters unless user requests customization

**Phase 2: Add Parameterization** (ONLY when user explicitly requests):
When user asks for customizable passwords, replica counts, storage sizes, etc.:
11. Add ONE API parameter at a time to root service
12. Add parameterDependencyMap on root for that parameter
13. Add child parameter definition (key + name + description + type) on child service
14. Replace hardcoded value with `$var.paramName` in child service
15. **RE-BUILD** to validate
16. **RE-DEPLOY instance** to validate runtime
17. Repeat steps 11-16 for each additional parameter

**Phase 3: Add Advanced Features** (ONLY when user explicitly requests):
18. Add autoscaling (remove any replicaCountAPIParam first)
19. Configure load balancers (if not already added)
20. Add integrations (observability, metering)
21. Add action hooks
22. **RE-BUILD and RE-DEPLOY to validate**

### 3. Build and Deploy
```bash
mcp__ctl__build_compose file="docker-compose-omnistrate.yaml" service_name="<name>"
mcp__ctl__service_plan_list service_name="<name>"
mcp__ctl__instance_create service_name="<name>" plan_name="<plan>" ...
```

### 4. Debug Until RUNNING
**Iterate until instance status is RUNNING and all resources healthy**:
```bash
mcp__ctl__instance_describe service_name="<name>" instance_id="<id>" deployment_status=true
mcp__ctl__workflow_list service_name="<name>" instance_id="<id>"
mcp__ctl__workflow_events service_name="<name>" workflow_id="<id>"
```

Refer to `../omnistrate-sre/SKILL.md` for systematic debugging approach.

**Common fixes**:
- Instance type unavailable → change type or region
- Volume creation failed → adjust storage type/size
- Probe failures → check logs with kubectl, fix app dependencies/env vars
- Environment variable errors → verify parameter definitions and system variable paths

**Do not stop at first failure** - most deployments require 2-3 iterations.

## Critical Rules

### Documentation Verification
- **Always search docs** before using any `x-omnistrate-*` extension
- **Verify system parameters** using `mcp__ctl__docs_system_parameters` before using `$sys.*` variables
- **Never hallucinate** syntax - if doc search returns no results, skip the feature
- **Skip when uncertain** - working basic service > broken advanced service

### API Parameter Syntax Rules

**IMPORTANT**: Before adding ANY API parameters, always search documentation:
```bash
mcp__omnistrate__omnistrate-ctl_docs_compose-spec query="x-omnistrate-api-params"
```
Verify the correct syntax, supported types, and configuration options from the official docs.

**Default Values**: Always quote as strings (even for numeric types)
```yaml
- key: replicas
  type: Float64
  defaultValue: "5"  # ✅ Quoted string
  # defaultValue: 5  # ❌ Unquoted number fails build
```

**Autoscaling Conflicts**: Cannot have replicaCountAPIParam AND autoscaling together
```yaml
# ❌ Wrong - causes build error
x-omnistrate-compute:
  replicaCountAPIParam: replicas
x-omnistrate-capabilities:
  autoscaling: [...]

# ✅ Correct - only autoscaling
x-omnistrate-compute:
  instanceTypes: [...]
x-omnistrate-capabilities:
  autoscaling:
    minReplicas: 3
    maxReplicas: 10
```

**Parameter Options**: Use simple `options` array for String types
```yaml
options:  # ✅ Simple array
  - value1
  - value2
# labeledOptions may not work in all contexts
```

### Build Strategy: Zero Parameterization First

**CRITICAL RULE**: ALWAYS start with ZERO API parameters and ZERO templatization.

**Phase 1 - Hardcoded Everything** (priority: get working deployment):
- **NO API parameters** on root service
- **NO x-omnistrate-api-params** on any child services
- **NO $var.* references** in environment variables
- **NO {{ }} concatenations**
- All passwords: Hardcoded defaults (e.g., `"ChangeMe123!"`)
- All replica counts: Fixed numbers (e.g., `replicaCount: 3`)
- All storage sizes: Hardcoded numbers (e.g., `instanceStorageSizeGi: 100`)
- All environment variables: Hardcoded values
- No autoscaling (use fixed replicas)
- Basic capabilities only (enableMultiZone, simple backups)
- **BUILD → DEPLOY → Verify RUNNING status**

**Phase 2 - Add Parameterization** (ONLY when user explicitly asks for it):
Wait for user to request: "I want to customize X" or "Make Y configurable"

Then add parameters ONE AT A TIME:
1. Add single API parameter to root service
2. Add parameterDependencyMap on root
3. Add full child parameter definition (key + name + description + type)
4. Replace hardcoded value with `$var.paramName`
5. **BUILD → DEPLOY → Validate**
6. Repeat for next parameter only if user requests

**Phase 3 - Advanced Features** (ONLY when user explicitly requests):
- Add autoscaling (user must request)
- Add custom replica counts (user must request)
- Add storage parameterization (user must request)
- Add integrations (user must request)

**Never add parameterization proactively** - only when explicitly requested by user.

### Parameter Flow Patterns

**Simple flow** (root → child for env vars):
```yaml
# Root service
x-omnistrate-api-params:
  - key: cacheSize
    parameterDependencyMap:
      redis: cacheSize

# Child service
environment:
  - MAX_MEMORY=$var.cacheSize
```

**Dual definition** (required for ALL parameters used in child services):
```yaml
# Root service
x-omnistrate-api-params:
  - key: dbPassword
    name: Database Password
    description: PostgreSQL password
    type: Password
    parameterDependencyMap:
      backend: dbPassword

# Child service (MUST redefine with name, description, type)
x-omnistrate-api-params:
  - key: dbPassword
    name: Database Password  # Required
    description: PostgreSQL password  # Required
    type: Password  # Required
environment:
  - POSTGRES_PASSWORD=$var.dbPassword
```

**Note**: Do NOT add parameters in initial build - use hardcoded values first.

### String Concatenation
Use `{{ }}` syntax when concatenating system parameters:
```yaml
environment:
  # ✅ Correct
  - API_URL="{{ $sys.network.node.externalEndpoint }}:8000"
  - DB_URL="{{ $var.protocol }}://{{ $postgres.sys.network.externalEndpoint }}/{{ $var.dbName }}"

  # ❌ Incorrect
  - API_URL=$sys.network.node.externalEndpoint:8000
```

### Cross-Service References
**Requires** `depends_on` relationship:
```yaml
services:
  backend:
    depends_on:
      - database  # Required
    environment:
      - DB_HOST="${database.sys.network.externalClusterEndpoint}"
```

### Backup Configuration
**Only on services with** `x-omnistrate-mode-internal: false`:
- Multi-service: Add to root service only
- Single-service: Add to the single service (if stateful)
- Never add to services with `x-omnistrate-mode-internal: true`

### Load Balancers
**Only add when**:
- Service has replicas > 1 OR autoscaling enabled
- Service is externally accessible
- NOT for omnistrate/noop services

## Deployment Model Patterns

**CRITICAL UNDERSTANDING**:
- **`hostedDeployment`** = YOUR service runs in YOUR provider account (standard SaaS - like Slack, Stripe)
- **`byoaDeployment`** = OPTION to let YOUR CUSTOMERS deploy in THEIR accounts (BYOC offering)
- **`onPremDeployment`** = OPTION for YOUR CUSTOMERS to deploy on-premise

**DEFAULT: ALWAYS use `hostedDeployment`**

```yaml
x-omnistrate-service-plan:
  name: 'My Service'
  deployment:
    hostedDeployment:  # ✅ ALWAYS USE THIS (unless user explicitly requests BYOC/on-prem)
      # YOUR cloud accounts (where YOUR SaaS service runs)
      awsAccountId: "YOUR_AWS_ACCOUNT_ID"  # YOUR AWS account
      awsBootstrapRoleAccountArn: "arn:aws:iam::YOUR_AWS_ACCOUNT_ID:role/omnistrate-bootstrap-role"
      gcpProjectId: "YOUR_GCP_PROJECT_ID"  # YOUR GCP project
      gcpProjectNumber: "YOUR_GCP_PROJECT_NUMBER"
      gcpServiceAccountEmail: "sa@YOUR_GCP_PROJECT_ID.iam.gserviceaccount.com"
```

**BYOC Offering** - Only when user wants to offer customer-hosted option:

```yaml
x-omnistrate-service-plan:
  name: 'My Service'
  deployment:
    byoaDeployment:  # Use ONLY if user says "I want to OFFER BYOC to my customers"
      # This is still YOUR intermediate account, not customer account
      awsAccountId: "YOUR_AWS_ACCOUNT_ID"
      awsBootstrapRoleAccountArn: "arn:aws:iam::YOUR_AWS_ACCOUNT_ID:role/omnistrate-bootstrap-role"
```

**Multi-Model** - Offer both hosted AND BYOC:

```yaml
x-omnistrate-service-plan:
  name: 'My Service'
  deployment:
    hostedDeployment:  # For most customers
      awsAccountId: "YOUR_AWS_ACCOUNT_ID"
      awsBootstrapRoleAccountArn: "arn:..."
    byoaDeployment:  # For enterprise customers who want BYOC
      awsAccountId: "YOUR_AWS_ACCOUNT_ID"
      awsBootstrapRoleAccountArn: "arn:..."
```

## Architecture Patterns

### Single Service
```yaml
services:
  web:
    x-omnistrate-mode-internal: false  # Root service
    x-omnistrate-compute: [...]
```

### Multi-Service
```yaml
services:
  app:  # Synthetic root (orchestrator)
    image: omnistrate/noop  # Special Omnistrate image (no workload)
    x-omnistrate-mode-internal: false
    depends_on: [web, database]
    x-omnistrate-capabilities:
      backupConfiguration: [...]  # Only on root

  web:
    x-omnistrate-mode-internal: true

  database:
    x-omnistrate-mode-internal: true
```

## Success Criteria

### Phase 1: Initial Deployment (Required)
- ✅ Build succeeds without validation errors
- ✅ **Instance reaches RUNNING status**
- ✅ **All resources healthy (not FAILED)**
- ✅ All health checks pass
- ✅ **NO API parameters** (everything hardcoded)
- ✅ **Completed at least one deploy-debug-fix cycle**
- ✅ All transformations based on verified documentation

### Phase 2: Parameterization (Optional - only if user requests)
- ✅ Parameters added one at a time
- ✅ Each parameter validated with build + deploy
- ✅ Dual definition pattern followed (root + child)
- ✅ Re-deployed successfully after each parameter addition

### Phase 3: Advanced Features (Optional - only if user requests)
- ✅ Autoscaling configured (no conflicts with replicaCountAPIParam)
- ✅ Load balancers working
- ✅ Integrations functional
- ✅ Multiple instances can run concurrently


## Reference

### Docker Compose
See COMPOSE_ONBOARDING_REFERENCE.md for:
- Complete step-by-step transformation guide
- Detailed extension syntax examples
- Environment variable interpolation patterns
- Storage configuration by cloud provider
- ActionHooks examples
- Custom metrics configuration
- Troubleshooting guide with common errors

### Other Methods
When additional onboarding methods are implemented, their reference documentation will be linked here.
