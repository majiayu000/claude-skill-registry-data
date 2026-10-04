---
name: azure-specialist
description: Azure cloud services, infrastructure, ARM templates, Bicep, and Azure
  best practices. Use when asked to deploy to Azure, set up Azure VMs or App Service
  or AKS, configure Azure AD or RBAC, write ARM templates or Bicep files, set up Azure
  Functions, work with Azure Key Vault, configure Azure Monitor, or design Azure network
  topology.
allowed-tools:
- Read
- Write
- Bash
- Grep
- Glob
metadata:
  author: Daryl Lundy
  version: 2.0.0
  category: infrastructure-cloud
  tags:
  - azure
  - cloud
  - arm
  - bicep
  - aks
  - azure-ad
  - azure-functions
---

# Azure Specialist

## Activation criteria
- User language explicitly matches trigger phrases such as `deploy to Azure`, `ARM template`, `Bicep`.
- The requested work fits this skill's lane: Azure VMs, App Service, AKS, Functions, SQL Database, Blob Storage, Azure AD, RBAC.
- The task stays inside this skill's boundary and avoids adjacent areas called out as out of scope: AWS or GCP work; Terraform HCL writing (use terraform-specialist).

## First actions
1. `Glob('**/*.bicep', '**/*.arm.json', '**/azuredeploy.json', '**/main.bicep')` — find existing IaC
2. Identify: subscription context, resource group structure, whether Azure AD / Entra ID is in scope
3. Confirm IaC approach preference: Bicep (preferred for Azure-native) vs ARM JSON vs Terraform

## Decision rules
- If Terraform files exist: use terraform-specialist for provisioning; use this skill for Azure service knowledge
- For new IaC: default to Bicep over ARM JSON (cleaner syntax, same capability)
- For identity: use Managed Identities for service-to-service auth; never use service principal credentials in code
- For secrets: all secrets go through Azure Key Vault

## Output contract
- Primary artifact: Bicep file or ARM JSON template, or Azure CLI bash script
- Required: RBAC assignments scoped to least-privilege; Key Vault integration for any secrets

## Constraints
- NEVER use Owner or Contributor at subscription scope unless explicitly required
- NEVER store secrets in ARM parameters files — use Key Vault references
- Scope boundary: application code belongs to language-specific skills

## Reference
- `references/legacy-agent.md`: full service reference — VMs, App Service, AKS, Functions, SQL Database, Blob Storage, Azure Monitor, RBAC, Well-Architected Framework
