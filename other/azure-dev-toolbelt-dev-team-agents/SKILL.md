---
name: azure
description: Azure — Container Apps, AKS, ACR, Azure SQL, Cosmos DB, managed identity.
---

# Azure Deployment

## Core Principle: Managed Identity Over Credentials

Azure's Managed Identity eliminates the need to store credentials — always use it over connection strings with passwords where possible.

---

## Recommended Stack

```
Azure DNS → Azure Front Door / App Gateway → Container Apps → Azure SQL / Cosmos DB
                                                           → Azure Cache for Redis
                                                           → Blob Storage (assets)
```

---

## Azure Container Registry (ACR)

```bash
# Login
az acr login --name myregistry

# Build and push
docker build -t myregistry.azurecr.io/myapp:$GIT_SHA .
docker push myregistry.azurecr.io/myapp:$GIT_SHA

# Enable auto-purge of untagged images
az acr config retention update \
  --registry myregistry \
  --status enabled \
  --days 30 \
  --type UntaggedManifests
```

## Azure Container Apps — Recommended Entry Point

```bash
# Create environment
az containerapp env create \
  --name myapp-env \
  --resource-group myapp-rg \
  --location eastus

# Deploy app
az containerapp create \
  --name myapp \
  --resource-group myapp-rg \
  --environment myapp-env \
  --image myregistry.azurecr.io/myapp:$GIT_SHA \
  --registry-server myregistry.azurecr.io \
  --target-port 8000 \
  --ingress external \
  --min-replicas 0 \
  --max-replicas 10 \
  --cpu 0.5 \
  --memory 1Gi \
  --env-vars APP_ENV=production \
  --secrets "db-password=secretref:myapp-db-password"

# Update to new image
az containerapp update \
  --name myapp \
  --resource-group myapp-rg \
  --image myregistry.azurecr.io/myapp:$NEW_SHA
```

## Key Vault — Secrets Management

```bash
# Create Key Vault
az keyvault create \
  --name myapp-kv \
  --resource-group myapp-rg \
  --location eastus

# Store secret
az keyvault secret set \
  --vault-name myapp-kv \
  --name db-password \
  --value "supersecret"

# Grant Container App access via Managed Identity
az keyvault set-policy \
  --name myapp-kv \
  --object-id <MANAGED_IDENTITY_OBJECT_ID> \
  --secret-permissions get list
```

## Managed Identity

```bash
# Enable system-assigned identity on Container App
az containerapp identity assign \
  --name myapp \
  --resource-group myapp-rg \
  --system-assigned

# Grant ACR pull access
az role assignment create \
  --assignee <PRINCIPAL_ID> \
  --role AcrPull \
  --scope /subscriptions/SUB/resourceGroups/RG/providers/Microsoft.ContainerRegistry/registries/myregistry
```

**Rule**: Never use ACR admin credentials — use Managed Identity for AKS/Container Apps pulling from ACR.

## GitHub Actions Integration

```yaml
- name: Login to Azure
  uses: azure/login@v2
  with:
    client-id: ${{ secrets.AZURE_CLIENT_ID }}
    tenant-id: ${{ secrets.AZURE_TENANT_ID }}
    subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}

- name: Deploy to Container Apps
  run: |
    az containerapp update \
      --name myapp \
      --resource-group myapp-rg \
      --image myregistry.azurecr.io/myapp:${{ github.sha }}
```

Use **Federated Identity** (OIDC) instead of client secrets for GitHub Actions — no secret rotation needed.

## Cost Optimization

- Container Apps scale to **zero** — no idle cost for dev/staging
- Use **Spot instances** for non-critical workloads (up to 90% discount)
- Use **Azure SQL serverless** tier for dev databases — pauses when idle
- Set **Budget alerts** in Cost Management at 80% and 100% of monthly budget
- Use **Azure Reservations** for 1-3 year commitments on predictable compute (up to 72% off)
- Enable **Azure Advisor** — it actively recommends cost-saving actions

## Useful Commands

```bash
# Stream Container App logs
az containerapp logs show --name myapp --resource-group myapp-rg --follow

# List revisions
az containerapp revision list --name myapp --resource-group myapp-rg

# Rollback
az containerapp revision activate \
  --revision myapp--previous-revision-name \
  --name myapp --resource-group myapp-rg
az containerapp ingress traffic set \
  --name myapp --resource-group myapp-rg \
  --revision-weight myapp--previous-revision-name=100

# Check costs
az consumption usage list --start-date 2024-01-01 --end-date 2024-01-31
```
