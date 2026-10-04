---
name: azure-prepare
description: >
  Prepare Azure environments and prerequisites before deployment.
  Use this skill when users ask for readiness checks, environment setup, or preflight planning.
  Covers landing zones, networking, identity, governance, and cost controls per Cloud Adoption Framework.
compatibility:
  models: [any-llm]
  cloud: azure
  frameworks: [cloud-adoption-framework, well-architected]
---

# Azure Prepare

Prepare subscriptions, resource groups, identity, governance, and cost controls per the Cloud Adoption Framework.
Landing zone setup is foundational; all deployments depend on this layer.

## Use This Skill When

- The user is starting a new Azure project or subscription
- Deployment keeps failing due to missing prerequisites (permissions, providers, quotas)
- The user asks for preflight checks, environment bootstrap, or landing zone design
- The user needs Azure Policy, tagging strategy, or access control baseline

## Context: Landing Zone Maturity

**Immature**: Ad hoc resource creation, no policies, inconsistent naming, mixed environments  
**Developing**: Basic resource groups, manual access control, some tagging  
**Managed**: Landing zone deployed, policies enforced, RBAC standardized, centralized logging  ← **Target**  
**Optimized**: GitOps for infrastructure, automated drift detection, cost governance, full audit trail

## Required Inputs

- **Tenant and subscription**: Tenant ID, subscription ID, billing account
- **Environment scope**: Single tenant or multi-tenant? Dev/test/prod separation?
- **Region strategy**: Primary and secondary regions, data residency constraints
- **Naming convention**: Org-env-workload-resource-seq (e.g., `contoso-prod-web-vm-01`)
- **Networking model**: Hub-spoke, vWAN, or flat? Private or public endpoints?
- **Identity model**: Entra ID only, on-premises sync, hybrid?
- **Security baseline**: Encryption, firewalls, NSGs, private link requirements
- **Team structure**: Who owns the platform? Who owns workloads?
- **Cost targets**: Monthly budget, chargeback model, reserved capacity?

## Decision Tree

```
Is this the first Azure subscription for the organization?
├─ Yes → Deploy landing zone from template (Microsoft Foundational or Enterprise)
└─ No → Align with existing landing zone patterns

Do you have on-premises infrastructure?
├─ Yes → Enable ExpressRoute, Site-to-Site VPN, DNS forwarders
└─ No → Direct internet egress acceptable

How many teams will share this subscription?
├─ Single team → Simple RBAC, one resource group per environment
└─ Multiple teams → Multiple resource groups, centralized policy, shared services

Are there compliance or regulatory requirements?
├─ Yes → Deploy Azure Policy, enable Defender, configure audit logging
└─ No → Basic security baseline sufficient
```

## Workflow

### Phase 1: Landing Zone Foundation

1. **Choose landing zone template**:
   - **Foundational** (Startups, small teams): VNet, NSG, basic RBAC
   - **Standard** (Mid-market): Hub-spoke, centralized DNS, policy enforcement
   - **Enterprise** (Large org): Management groups, policy cascade, full governance

2. **Provision landing zone**:
   ```bash
   # Use Azure landing zone Bicep templates from Microsoft
   az deployment tenant create \
     --name alz-deployment \
     --location eastus \
     --template-uri https://raw.githubusercontent.com/Azure/landing-zones-accelerator/main/templates/
   ```

3. **Validate foundational resources**:
   - Management groups created (root > platform > landing zones)
   - Subscription placed in correct management group
   - Policy definitions assigned at appropriate scope

### Phase 2: Subscription Baseline

1. **Provider registration**:
   ```bash
   # Enable required resource providers
   az provider register --namespace Microsoft.Compute
   az provider register --namespace Microsoft.Network
   az provider register --namespace Microsoft.Storage
   # (List depends on workload)
   ```

2. **Create resource groups by lifecycle**:
   - **Shared**: Logging, monitoring, networking (long-lived)
   - **Dev/Test**: Short-lived, high churn, lower security bar
   - **Production**: Long-lived, strict change controls, backup/DR

3. **Apply Azure Policy**:
   - Enforce tagging (owner, environment, cost-center)
   - Enforce encryption (storage, databases)
   - Prevent public IP creation (unless whitelisted)
   - Require network security groups

### Phase 3: Identity & Access

1. **Define role structure**:
   - **Subscription Owner** (2-3 people, max): Rare, emergency escalation only
   - **Resource Group Owners** (teams): Manage resources within group
   - **Workload Contributors** (developers): Deploy, configure; no delete
   - **Readers** (auditors, ops): View-only, troubleshooting

2. **Configure managed identities**:
   - System-assigned for single-app identities (App Service, Functions, AKS pods)
   - User-assigned for shared or multi-app identities
   - Never use connection strings in app settings

3. **Set up Key Vault**:
   ```bash
   az keyvault create --name "kv-${environment}-${org}" \
     --resource-group $RG --enable-rbac-authorization
   ```

### Phase 4: Networking

1. **Plan IP address space**:
   - Hub VNet: 10.0.0.0/8 reserved for platform services
   - Spoke VNets: Subdivided by workload/environment
   - Document all subnets, gateways, and external routes

2. **Deploy network infrastructure**:
   - Hub VNet with bastion host (secure RDP/SSH)
   - Spoke VNets peered to hub
   - Network Security Groups with default-deny ingress
   - Azure Firewall (hub) or Network Virtual Appliance (NVA)

3. **Configure DNS**:
   - Azure DNS zones for public DNS
   - Private DNS zones for internal resolution (*.privatelink.database.windows.net)
   - Conditional forwarders to on-premises DNS

### Phase 5: Logging & Monitoring

1. **Centralize diagnostics**:
   - All subscriptions → Central Log Analytics workspace
   - All storage accounts → Central storage for archival
   - All activity logs → Central audit trail

2. **Configure alerts**:
   - Failed logins, privilege escalation, unused roles
   - Resource deletion, policy violations
   - Cost threshold breaches

### Phase 6: Cost Governance

1. **Set budgets**:
   - Subscription-level budget with notifications at 50%, 75%, 100%
   - Resource group budgets for shared services
   - Alert on anomalies

2. **Reserved capacity** (if production):
   - Analyze 1-year usage
   - Purchase 1-year or 3-year reservations for 20-35% discount

3. **Cost allocation**:
   - Tag all resources with cost-center tag
   - Use Cost Management + Billing to show chargeback per team

## Output Contract

1. **Landing Zone Summary**
   - Subscription ID, tenant ID, region(s)
   - Chosen landing zone template and justification
   - High-level network topology

2. **Pre-Deployment Checklist**
   - Provider registration status
   - Required role assignments (who needs what)
   - API and resource type quota headroom

3. **Setup Commands or IaC**
   - Bicep template or Terraform code to replicate landing zone
   - Order of operations (dependency graph)
   - Sample parameter files for different environments

4. **Access & Governance Model**
   - Role hierarchy and assignment plan
   - Policy definitions and exceptions
   - Tagging strategy with mandatory tags

5. **Network & Identity Baseline**
   - VNet design, subnets, routing
   - Managed identity and Key Vault setup
   - DNS configuration

6. **Monitoring & Cost Plan**
   - Log Analytics workspace scope
   - Budget and alerting thresholds
   - Reserved capacity recommendation

## Practical Examples

### Example 1: Dev/Test Landing Zone
```
- Single VNet (10.1.0.0/16)
- Three subnets: app (10.1.1.0/24), data (10.1.2.0/24), mgmt (10.1.3.0/24)
- Minimal NSGs (allow internal, deny external)
- Shared Log Analytics (7-day retention)
- Budget alert at $500/month
```

### Example 2: Production Landing Zone with Hub-Spoke
```
- Hub VNet (10.0.0.0/16): Firewall, Bastion, DNS forwarders
- Spoke VNet per workload: Web (10.1.0.0/16), Data (10.2.0.0/16), API (10.3.0.0/16)
- All spokes peered to hub
- Strict NSGs per spoke with specific ingress rules
- Centralized logging to shared workspace
- 30-day retention, archive to storage after 90 days
- Budget alerts at 50%, 75%, 100% thresholds
```

## Guardrails

- **Never skip tagging strategy**; enforce with Azure Policy from day one.
- **Do not hardcode secrets** in IaC or templates; use Key Vault references.
- **Avoid manual post-setup configuration**; all infrastructure must be in IaC.
- **Do not share subscriptions across business units** unless governance is extreme.
- **Ensure network segmentation** by default; permit traffic explicitly.
- **Test landing zone teardown before production**; ensure cleanup works end-to-end.
- **Keep environment names consistent**: dev-*, test-*, prod-* naming enforced by policy.
