---
name: azure-deploy
description: >
  Plan and execute Azure deployments safely and repeatably for applications and infrastructure.
  Use this skill when users ask to deploy, publish, release, or provision workloads in Azure.
  Covers Infrastructure-as-Code, idempotency, health validation, and rollback strategies.
compatibility:
  models: [any-llm]
  cloud: azure
  frameworks: [well-architected, cloud-adoption-framework]
  iac: [bicep, terraform, arm-templates]
---

# Azure Deploy

Deploy workloads to Azure with a clear, low-risk process aligned with the Well-Architected Framework.
Emphasis on idempotency, repeatable IaC, comprehensive validation, and reversible rollback paths.

## Use This Skill When

- The user asks to deploy an app or service to Azure
- The user needs release automation, blue-green, or canary deployments
- The user wants Infrastructure-as-Code guidance (Bicep, Terraform)
- The user needs rollback and disaster recovery procedures
- Deployment fails and needs troubleshooting with validation steps

## Context: Deployment Maturity Model

**Stage 1: Manual** → Portal-only, error-prone, hard to audit  
**Stage 2: Semi-Automated** → Scripts with some IaC, inconsistent across environments  
**Stage 3: Fully Automated** → Declarative IaC, CI/CD, infrastructure versioned  ← **Target**  
**Stage 4: GitOps** → All changes through pull requests, fully auditable, drift detection

## Required Inputs

- **Target environment**: subscription ID, resource group, region, tenant
- **Environment stage**: dev, test, stage, prod (with distinct names)
- **Workload type**: web app, function, container app, AKS, VM, hybrid
- **Deployment method**: Azure CLI, Bicep, Terraform, ARM template, Azure Developer CLI
- **Artifact readiness**: built container image, versioned application package
- **Security context**: managed identity vs. connection string, private endpoints, secret rotation
- **Validation criteria**: health checks, endpoint tests, smoke tests, performance baselines
- **Rollback tolerance**: how many minutes can service be unavailable?

## Decision Tree

```
Is this infrastructure or application code?
├─ Infrastructure → Use Bicep or Terraform (IaC)
└─ Application → Use Azure DevOps or GitHub Actions pipeline

Is this a net-new deployment or an update?
├─ Net-new → Deploy with full validation suite
└─ Update → Blue-green or canary strategy to minimize blast radius

Do you need instant rollback capability?
├─ Yes → Blue-green deployment (dual environments, instant traffic switch)
└─ Acceptable lag → Canary (gradual rollout with monitoring)
```

## Workflow

### Phase 1: Pre-Deployment Validation (Shift-left)

1. **Verify prerequisites**:
   - Subscription access confirmed (check quota, resource limits, API provider registration)
   - Role assignments correct for service principals or managed identities
   - Naming conventions followed (avoid reserved names, region abbreviations)
   - All secrets exist in Key Vault or secure store (never hardcode)

2. **Review IaC and artifacts**:
   - Bicep/Terraform syntax validated with `bicep build` or `terraform plan`
   - No hardcoded values (use parameters and variables)
   - Dependencies explicitly declared (`dependsOn`, references)
   - Tags and metadata complete (owner, environment, cost center)

3. **Validate security posture**:
   - Network isolation: private endpoints, NSGs, firewalls
   - Identity: managed identity or service principal with least privilege
   - Data: encryption at rest and in transit
   - Secrets stored in Key Vault with access policy

### Phase 2: Artifact Preparation

1. **Build application**:
   - Compile, test, and package application code
   - Increment version number (semantic versioning)
   - Tag artifacts with build ID or commit hash for traceability

2. **Build container (if containerized)**:
   - Push to Azure Container Registry (ACR) with multi-tag (`:latest`, `:v1.2.3`, `:sha-abcd1234`)
   - Scan image for vulnerabilities using Defender for container registries
   - Verify image can be pulled from target deployment context

3. **Archive IaC**:
   - Version Bicep or Terraform files in source control
   - Pin module versions (never use `latest`)
   - Generate parameter files for each environment (dev.bicepparam, prod.bicepparam)

### Phase 3: Deployment Execution

**Option A: Declarative (Recommended)**
```bash
az deployment group create \
  --resource-group $RG \
  --template-file main.bicep \
  --parameters main.bicepparam \
  --mode Incremental
```

**Option B: Terraform**
```bash
terraform init -backend-config=backend.tfvars
terraform plan -var-file=prod.tfvars -out=tfplan
terraform apply tfplan
```

4. **Monitor deployment progress**:
   - Watch Azure portal Activity Log or CLI output for errors
   - Check resource creation order (dependencies respected)
   - Verify DNS, network routes, and storage connectivity as resources come online

### Phase 4: Post-Deployment Validation

1. **Smoke test**:
   - Application endpoint responds (HTTP 200, health check passes)
   - Database or data store is accessible
   - Logging and monitoring are active

2. **Integration test**:
   - Dependent services (API gateways, queues, caches) are reachable
   - Data flows through expected paths
   - Performance is within SLA targets

3. **Security validation**:
   - Public exposure is blocked (no public IPs unless required)
   - Managed identity credentials are working
   - Key Vault access is functional

4. **Compliance check**:
   - Tags and ownership metadata present
   - Resource names follow naming convention
   - Diagnostic logging configured

### Phase 5: Rollback & Recovery

**Immediate Rollback (Minutes)**:
- **Blue-green**: Switch traffic back to old deployment (instant)
- **Container/App Service**: Revert to previous deployment slot or image version

**Longer Rollback (Hours)**:
- Re-deploy previous IaC snapshot from version control
- Point application to previous database snapshot
- Update DNS or traffic manager to old infrastructure

**Full Disaster Recovery**:
- Restore from backup or failover to secondary region
- Validate data consistency and application state
- Perform security re-validation before resuming production traffic

## Output Contract

Return these sections in order:

1. **Deployment Plan Summary**
   - Environment, resource group, region
   - Estimated lead time for quota increases (if needed)
   - High-level resource inventory and costs

2. **Pre-Deployment Checklist**
   - Prerequisites validation commands or portal steps
   - Required role assignments and permissions
   - Security and networking decisions

3. **Deployment Commands or IaC**
   - Exact CLI/Terraform/Bicep commands with parameter values
   - Suggested order of operations
   - Parallel vs. sequential resource creation notes

4. **Post-Deployment Validation Checklist**
   - Smoke test steps (curl commands, portal checks)
   - Integration test scenarios
   - Performance baseline commands (ab, loadtest, etc.)

5. **Rollback Procedure**
   - Step-by-step rollback sequence
   - How long rollback takes
   - Data consistency checks post-rollback

6. **Risks and Assumptions**
   - Quota headroom assumptions
   - Blast radius if deployment fails mid-stream
   - Dependencies on external systems

## Practical Examples

### Example 1: Deploy a Container App with Traffic Split (Canary)
```
1. Deploy new revision to staging slot: 5% traffic
2. Monitor error rate and latency for 10 minutes
3. Shift to 25%, then 50%, then 100% in 10-minute intervals
4. If error spike detected, instant rollback to previous revision
```

### Example 2: Blue-Green Web App Deployment
```
1. Deploy new version to unused deployment slot (green)
2. Run smoke and integration tests against green slot
3. Swap slots: green becomes production (instant, no downtime)
4. Keep blue slot warm for quick rollback within 1 hour
```

### Example 3: Bicep Deployment with Parameter Overrides
```
az deployment group create \
  --resource-group myapp-prod \
  --template-file main.bicep \
  --parameters main.bicepparam \
  --parameters location=eastus vmCount=3 \
  --mode Incremental
```

## Guardrails

- **Never hardcode secrets or connection strings** in IaC, templates, or environment variables. Use Key Vault with managed identity.
- **Always use `--mode Incremental`** for Bicep/ARM; avoid `Complete` mode unless you intend to delete unlisted resources.
- **Avoid manual post-deployment configuration** (portal UI changes). All config must be in IaC for reproducibility.
- **Call out destructive operations** (database migrations, resource deletions, scale-down) before execution.
- **Version everything**: application code, container images, IaC modules, parameter files.
- **Never use `latest` image tag in production**; pin to specific versions.
- **Test rollback procedure before going to production**; don't assume it works untested.
- **Separate credentials by environment**; dev/test/prod each have distinct service principals and Key Vault instances.
