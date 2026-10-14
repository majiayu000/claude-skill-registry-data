---
name: azure-pro
description: Azure guidance — subscriptions and RBAC, networking, AKS/App Service choices, Entra ID, and cost management.
category: development
---

## Overview

Microsoft Azure is the enterprise cloud — deep integration with Microsoft 365, Entra ID (formerly Azure AD) as the identity backbone, and a service catalog that mirrors AWS/GCP with its own naming and hierarchy. Its management-group → subscription → resource-group hierarchy and RBAC model are the first things to internalize.

Azure rewards understanding the hierarchy, using managed identities everywhere, and choosing the right compute (App Service, Container Apps, AKS, Functions) for the team's operational maturity. This skill covers the Azure fundamentals, key services, identity, and cost management.

## When to use

- Designing architecture on Azure (choosing services).
- Setting up the hierarchy (management groups, subscriptions, resource groups).
- Configuring RBAC and managed identities.
- Building VNets (subnets, NSGs, private endpoints).
- Choosing compute (App Service, Container Apps, AKS, Functions, VMs).
- Managing costs (budgets, reservations, advisor).
- Securing Azure with Entra ID and Defender for Cloud.

## Core concepts

- **Hierarchy.** Management groups → subscriptions → resource groups → resources. Subscriptions are the billing and policy boundary; resource groups are the lifecycle boundary (deploy/delete together). Design this before creating resources.
- **RBAC.** Role assignments (role + scope + principal) with built-in roles (Contributor, Reader) and custom roles. Assign at the narrowest scope; use PIM (Privileged Identity Management) for just-in-time admin elevation.
- **Managed identities.** System-assigned (tied to a resource's lifecycle) or user-assigned (shared). The way workloads authenticate to Azure services — no stored credentials. Use them everywhere instead of connection strings and keys.
- **Entra ID.** The identity plane: users, groups, app registrations, conditional access (MFA policies, location/device rules). Human access via Entra groups, never shared credentials.
- **VNets.** Regional virtual networks with subnets; NSGs (stateful firewall rules) on subnets/NICs; no cross-region traffic without peering/ExpressRoute. Private endpoints bring PaaS services (SQL, Storage) into your VNet — no public exposure.
- **Private Link / private endpoints.** The pattern for keeping PaaS traffic private. Public endpoints on databases and storage accounts should be the exception, justified and firewalled.
- **Compute choices.** App Service (PaaS web apps, easiest), Container Apps (serverless containers, scales to zero, Dapr integration), AKS (managed Kubernetes), Functions (event-driven), VMs (full control). Container Apps is the modern default for containerized services.
- **AKS.** Managed control plane; system vs user node pools; Azure CNI networking; workload identity (federated credentials) for pod-to-Azure auth. Use when you need Kubernetes — not as the default.
- **Azure SQL / Cosmos DB.** Managed SQL Server (single DB, elastic pools, managed instances) with geo-replication; Cosmos DB for globally-distributed NoSQL with tunable consistency. Private endpoints for both.
- **Storage accounts.** Blob (object), with tiers (Hot/Cool/Cold/Archive), lifecycle management, versioning, and firewall rules. One storage account per purpose; disable public blob access by default.
- **Service Bus / Event Grid / Event Hubs.** Queues/topics (Service Bus) for enterprise messaging with dead-lettering; Event Grid for event routing; Event Hubs for streaming ingestion (Kafka-compatible endpoint available).
- **Key Vault.** Secrets, keys, certificates with RBAC/rotation — the only place secrets live. Reference via managed identity; never app settings in plaintext.
- **Monitor and Defender.** Azure Monitor (metrics, logs via Log Analytics), Application Insights for APM; Defender for Cloud for posture management and threat protection.
- **Policy.** Azure Policy enforces rules (allowed SKUs, required tags, no public storage) across scopes — the guardrail mechanism. Assign built-in initiatives before writing custom policies.
- **Cost management.** Budgets with alerts, reservations/savings plans for steady workloads, Advisor recommendations, and tagging (enforced by policy) for chargeback.
- **Bicep.** Azure's HCL-like IaC language — far less verbose than ARM JSON; the recommended path for Azure-native infrastructure as code.
- **Availability zones.** Zone-redundant vs zonal vs regional deployments — choose per RTO/RPO; zone redundancy is the production default.

## Practical workflow

1. **Design the hierarchy.** Management groups (prod/non-prod) → subscriptions per environment/team → resource groups per workload. Apply Policy at the management-group level for org-wide guardrails.
2. **Configure identity.** Entra ID groups for humans, PIM for admin roles, conditional access requiring MFA; managed identities for every workload touching Azure services.
   ```hcl
   # workload authenticates to Key Vault via managed identity — no secrets
   resource "azurerm_role_assignment" "api_kv" {
     scope                = azurerm_key_vault.main.id
     role_definition_name = "Key Vault Secrets User"
     principal_id         = azurerm_user_assigned_identity.api.principal_id
   }
   ```
3. **Build the VNet.** Hub-spoke or per-workload VNets with peering; private subnets for apps/data; NSGs with least-privilege rules; private endpoints for SQL/Storage/Key Vault; Azure Firewall or NAT gateway for controlled egress.
4. **Choose compute.** Web apps/APIs → App Service or Container Apps; event-driven → Functions; Kubernetes needs → AKS; VMs only with justification. Start with the simplest that meets requirements.
5. **Put data on PaaS.** Azure SQL with geo-replication and automated backups, or Cosmos DB for global NoSQL; storage accounts with private endpoints and lifecycle tiers.
6. **Decouple with messaging.** Service Bus queues/topics with dead-lettering for commands; Event Grid for domain events; Event Hubs for telemetry streams.
7. **Secure secrets and edge.** Key Vault for all secrets with rotation; Front Door / Application Gateway + WAF for public traffic; private endpoints everywhere internal.
8. **Monitor and control cost.** Azure Monitor workbooks + alerts on golden signals; budgets per subscription with action groups; Advisor reviews monthly; reservations after baselines stabilize.

   ```bicep
   resource kv 'Microsoft.KeyVault/vaults@2023-07-01' = {
     name: 'kv-${env}-main'
     location: location
     properties: {
       sku: { family: 'A', name: 'standard' }
       tenantId: subscription().tenantId
       enableRbacAuthorization: true
     }
   }
   ```

## Common pitfalls

- **Flat subscription sprawl** — dozens of subscriptions with no management groups or policy; design the hierarchy first.
- **Connection strings in app settings** — secrets in plaintext config; managed identity + Key Vault.
- **Public PaaS endpoints** — SQL/Storage reachable from the internet; private endpoints + firewall rules.
- **Standing admin access** — permanent Contributor/Owner assignments; PIM for just-in-time elevation.
- **Shared credentials** — service accounts with passwords in wikis; Entra ID + managed identities.
- **No Azure Policy** — untagged resources, wrong SKUs, public storage; enforce guardrails.
- **AKS by default** — Kubernetes overhead for apps Container Apps would serve; match compute to team capacity.
- **Ignoring budgets** — cost alerts with no owner; budgets need action groups and runbooks.
- **Single region for critical apps** — no geo-redundancy; design for region failure where RTO demands it.
- **NSGs wide open** — `*` source rules left from debugging; audit to least privilege.
- **No dead-lettering** — poison messages in Service Bus looping; configure DLQs.
- **Storage public access** — anonymous blob access enabled; disable by default, use SAS sparingly.
- **Untagged resources** — cost attribution impossible; enforce tags with Policy deny rules.
