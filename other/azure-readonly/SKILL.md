---
name: azure-read-only
description: Read-only Microsoft Azure inspection via Azure CLI
activation_keywords: [azure, az, microsoft, vm, aks, resource group, storage account]
execution_mode: server
---

# Azure Read Only Skill

Read-only operations via `az`:

- `vm` — list virtual machines
- `groups` — list resource groups
- `storage` — list storage accounts
- `aks` — list AKS clusters

Tool: `builtin_azure_readonly` with `operation`, optional `subscription`.

Requires Azure CLI installed and logged in (`az login`) on the server.
