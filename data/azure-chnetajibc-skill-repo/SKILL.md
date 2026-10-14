---
name: azure
description: "Azure essentials: Entra ID/RBAC, VNet, App Service/AKS/Functions, Azure SQL/Cosmos DB/Redis, Service Bus, Monitor. Use for Azure decisions and deploys; research current docs per configured version."
---

# azure

Same foundations as `../foundations/`, resolved against current Azure docs.

## Activate when

- Choosing or operating Azure services; wiring Entra ID, networking, data, or deploys.

## Do NOT activate for

- AWS/GCP specifics (see aws-foundations, gcp).

## Procedure

1. Identity: Entra ID with RBAC per workload (managed identities, no secrets in config), PIM for elevation, audit logs on.
2. Network: VNet with private endpoints for data, NSGs as narrow allowlists, no public databases.
3. Compute: Functions for event-driven, App Service for steady web, AKS for containers; staged slots/rollouts with health checks.
4. Data: Azure SQL with backups + pooling, Cosmos DB per documented partition/access patterns, Azure Cache for Redis for hot reads, Service Bus decoupling slow work.
5. Observe: Azure Monitor metrics/alarms, structured logs, tracing, SLOs.
6. Research: https://learn.microsoft.com/azure/ for the configured API versions (registry: `../../research/documentation-search/references/framework-registry.yaml` — azure). Never invent service behavior; resolve against docs.
7. Verify: scratch deploy, kill-and-recover, restore drill, budget alert confirmed.

## References
- `../foundations/`, `../aws-foundations/` (procedure pattern).
