---
name: clusters
description: >
  Multi-cluster reference data for troubleshooting across EMEA, APAC, NAM.
  Contains kubectl contexts, ArgoCD cluster names, and Log Analytics
  workspace details per region. Auto-loaded by the troubleshooter agent.
disable-model-invocation: true
---

## Cluster Registry

Edit the values below to match your environment.

### Clusters

| Region | kubectl Context | ArgoCD Cluster Name | Azure Resource Group |
|--------|----------------|---------------------|---------------------|
| EMEA   | `aks-emea-prod` | `emea-production` | `rg-emea-prod` |
| APAC   | `aks-apac-prod` | `apac-production` | `rg-apac-prod` |
| NAM    | `aks-nam-prod`  | `nam-production`  | `rg-nam-prod`  |

### ArgoCD
Single instance manages all 3 clusters. App naming: `<service>-<region>`.
Each app's `destination.server` identifies the target cluster.

### kubectl — Target a Specific Cluster
```bash
kubectl --context=aks-emea-prod get pods -n <namespace>
kubectl --context=aks-apac-prod logs deployment/<app> --tail=200
kubectl --context=aks-nam-prod get events -n <namespace>
```

### Azure Log Analytics — Query Per Region

Resolve the workspace GUID first, then query:

```bash
# Get workspace GUID (cache for session)
WORKSPACE=$(az monitor log-analytics workspace show \
  --resource-group rg-<region>-<workload>-prod \
  --workspace-name law-<region>-<workload>-prod \
  --query customerId -o tsv)

# Query using the GUID
az monitor log-analytics query \
  --workspace "$WORKSPACE" \
  --analytics-query "<KQL>" \
  --output json
```

See the app-insights skill for table/field name mappings (e.g.
`AppEvents` instead of `customEvents`, `Properties` instead of
`customDimensions`).

### Cross-Region Comparison
```bash
for region in emea apac nam; do
  echo "=== $region ==="
  kubectl --context="aks-${region}-prod" get pods -n <ns> -l app=<svc>
done
```

```bash
WORKSPACE=$(az monitor log-analytics workspace show \
  --resource-group rg-<region>-<workload>-prod \
  --workspace-name law-<region>-<workload>-prod \
  --query customerId -o tsv) && \
az monitor log-analytics query \
  --workspace "$WORKSPACE" \
  --analytics-query "AppExceptions | where TimeGenerated > ago(2h) | summarize count() by ExceptionType" \
  --output json
```
