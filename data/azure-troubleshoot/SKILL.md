---
name: azure-troubleshoot
description: "Troubleshoot Azure using tool-first access, falling back to Azure CLI when necessary. Focus on Virtual Machines, AKS, Azure Container Registry, Storage Accounts, and Log Analytics."
---

# Azure Troubleshooting Skill

## General Guidance

Always use **tool-based queries first** to fetch logs, metrics, and diagnostic data.  
Only fall back to Azure CLI for deeper or unsupported inspection.

Investigations should:

1. Use Log Analytics Kusto queries with proper scoping  
2. Use Activity Logs to identify failures  
3. Use metrics when diagnosing performance issues  
4. Provide minimal, targeted remediation advice

---

## Core Services Covered

### Virtual Machines

Common issues:

- Boot failures
- OS/disk failures
- NIC/IP misconfiguration

Investigations:

- Inspect boot diagnostics logs
- Query `Heartbeat` table for VM status
- Check Activity Logs for failed start/stop operations

### AKSS

Common issues:

- Pod scheduling failures
- Node pressure
- Image pull errors (ACR auth)
- Container crashes

Investigations:

- Query `KubeEvents`
- Query `KubePodInventory`
- Inspect `ContainerLog`

### Azure Container Registry (ACR))

Common issues:

- Permission denied (RBAC)
- Token expiration

Investigations:

- Query Activity Logs for `push/write` or `pull/read` failures
- Check repository event logs

### Storage Accountss

Common issues:

- Firewall-restricted access
- SAS token expiration
- Object not found

Investigations:

- Query `StorageBlobLogs`
- Validate configuration + permissions

### Log Analytics

Best practices:

- Always filter by `_ResourceId`
- Narrow time range
- Query only the tables relevant to the service

---

## Workflow

1. Identify target service  
2. Query Log Analytics with scoped KQL  
3. Query Activity Logs  
4. Review metrics  
5. Interpret patterns  
6. Recommend targeted fixes  
