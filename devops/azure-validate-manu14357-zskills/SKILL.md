---
name: azure-validate
description: >
  Validate Azure deployments against functional, security, performance, and operational criteria before production release.
  Use this skill when users ask for readiness checks, health verification, or production sign-off gates.
  Covers Well-Architected Framework validation, SLA verification, and release readiness.
compatibility:
  models: [any-llm]
  cloud: azure
  frameworks: [well-architected]
---

# Azure Validate

Systematically validate deployments against infrastructure, security, performance, and operational readiness criteria.
Provide go/no-go decision for production release.

## Use This Skill When

- The user has deployed to staging and needs production readiness verification
- The user asks for preflight checks, health verification, or sign-off gates
- Deployment is ready but needs validation against SLA and compliance requirements
- There's a need to verify monitoring, alerting, and incident response readiness

## Context: Validation Maturity

**Immature**: Manual spot checks, no automation, inconsistent criteria  
**Developing**: Some automated tests, partial validation, manual sign-off  
**Managed**: Automated checks, clear pass/fail criteria, documented gates → **Target**  
**Optimized**: Full CI/CD integration, policy-as-code, real-time compliance dashboards

## Required Inputs

- **Deployment scope**: All resources, environment, regions
- **SLA targets**: Availability (%), latency (ms, p99), throughput (req/sec)
- **Traffic model**: Expected load profile and peak burst
- **Security & compliance**: HIPAA, PCI-DSS, SOC2, audit requirements?
- **User journeys**: Critical paths to test (e.g., user signup → purchase → confirmation)
- **Acceptance criteria**: Performance baseline, error rate threshold
- **Rollback plan**: How to revert if validation fails?

## Decision Tree

```
Have all infrastructure resources been provisioned?
├─ No → BLOCK: Complete infrastructure deployment first
└─ Yes → Continue

Are all required monitoring and alerting configured?
├─ No → WARNING: Cannot track production health; recommend staging validation only
└─ Yes → Continue

Has security baseline been applied (NSGs, RBAC, encryption)?
├─ No → BLOCK: Security validation must pass before production
└─ Yes → Continue

Do all smoke tests and end-to-end flows pass?
├─ No → BLOCK: Application logic failures prevent release
└─ Yes → Continue

Does load testing meet SLA targets?
├─ No → WARNING: May fail under expected load; consider remediation
└─ Yes → READY FOR PRODUCTION
```

## Workflow

### Phase 1: Infrastructure Validation (5-10 min)

1. **Inventory and quota check**:
   ```bash
   az resource list --resource-group $RG --query "[].{name:name, type:type, state:properties.provisioningState}"
   az vm list-usage --location eastus --query "[?limit >= currentValue * 1.2].{name:name.value, current:currentValue, limit:limit}"
   ```

2. **Verify networking, storage, and databases**:
   - VNets, subnets, peering in place?
   - NSGs configured (least-privilege ingress)?
   - Encryption enabled (at-rest, in-transit)?
   - Backups with retention policy?
   - Firewall rules (internal only)?

### Phase 2: Identity & Access Validation (5 min)

1. **RBAC check**:
   - Role assignments complete and minimal?
   - No Contributor on production?
   - Service principals scoped appropriately?

2. **Key Vault & secrets**:
   - All secrets provisioned?
   - Access policies/RBAC configured?
   - Audit logging enabled?

### Phase 3: Application Health (10-15 min)

1. **Smoke tests**:
   ```bash
   curl -I https://$APP/health  # HTTP 200
   ```

2. **End-to-end flows**:
   - User signup → confirmation
   - Payment → inventory → receipt

3. **Data integrity**:
   - No unhandled exceptions
   - No orphaned records

### Phase 4: Performance & Scaling (15-30 min)

1. **Load test** (1000 req, 100 concurrent):
   - 95% complete in <500ms
   - Error rate <1%

2. **Verify auto-scaling**:
   - Scaled up under load?
   - Latency within SLA?
   - Even distribution?

3. **Cost validation**:
   - Budget vs. actual
   - Unused resources?

### Phase 5: Monitoring & Alerting (5 min)

1. **Instrumentation**:
   - Application Insights active?
   - Custom metrics for KPIs?

2. **Alerts**:
   - Rules for errors, latency, CPU?
   - Channels configured?
   - Thresholds aligned with SLA?

### Phase 6: Security & Compliance (10 min)

1. **Security baseline**:
   - Defender enabled?
   - No unintended public IPs?
   - No secrets in logs?

2. **Compliance**:
   - Audit logging enabled?
   - Encryption verified?
   - Data residency correct?

3. **Security tests**:
   - Unauthenticated cannot access admin
   - HTTPS enforced
   - No exposed secrets

### Phase 7: DR Readiness (5 min)

1. **Incident response**:
   - On-call assigned?
   - Runbooks documented?

2. **Test rollback**:
   - Previous version available?
   - Procedure documented?

## Output Contract

1. **Validation Report**: Status, date, environment
2. **Checklist Results**: Per category (PASS/WARNING/FAIL)
3. **Blocking Issues**: Must-fix before release
4. **Warnings**: Mitigations accepted?
5. **Sign-Off**: Approved by [Name, Date]

## Guardrails

- **Automate all checks**; manual spot checks miss issues.
- **Define clear pass/fail criteria** before testing.
- **Never skip security validation**; security is blocking.
- **Test rollback** before release.
- **Separate blockers from recommendations**; non-blocking warnings don't delay release.
- **Document all assumptions** (e.g., "peak load 500 req/sec").
- **Validate in production-like environment**; staging differences mask issues.
