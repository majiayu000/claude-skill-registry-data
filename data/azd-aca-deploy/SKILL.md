---
name: azd-aca-deploy
description: Deploy to Azure Container Apps using azd (provision + deploy workflow)
---

# Azure Container Apps Deployment Skill

Use this skill when asked to:
- "deploy to Azure"
- "azd up"
- "provision infrastructure"
- "update the app in Azure"

## Prerequisites

Before deploying:

1. **azd installed**: `azd version`
2. **Logged in**: `azd auth login`
3. **Environment selected**: `azd env list`

## Deployment Strategies

### Full Deployment (First Time)

```bash
azd up
```

This runs provision + deploy in one command.

### Incremental Updates

| Change Type | Command | Speed |
|-------------|---------|-------|
| Bicep/Infra only | `azd provision` | Slower |
| App code only | `azd deploy` | Fast |
| Both | `azd up` | Full |

## Recommended Workflow

### For Code Changes

```bash
# 1. Run quality checks
uv run python .github/skills/python-quality/scripts/check.py

# 2. Deploy app only (fast)
azd deploy
```

### For Infrastructure Changes

```bash
# 1. Preview changes
az deployment group what-if \
  --resource-group <rg> \
  --template-file infra/main.bicep

# 2. Apply changes
azd provision
```

## Environment Management

```bash
# List environments
azd env list

# Create new environment
azd env new <name>

# Switch environment
azd env select <name>

# Delete environment (and resources)
azd down
```

## Troubleshooting

### Common Issues

1. **Auth expired**: Run `azd auth login`
2. **Wrong subscription**: Check `az account show`
3. **Resource conflicts**: Run `azd down` and `azd up` fresh

### View Logs

```bash
# Container Apps logs
az containerapp logs show \
  --name <app-name> \
  --resource-group <rg> \
  --type console
```

## Quick Script

For automated deployment:

```bash
uv run python .github/skills/azd-aca-deploy/scripts/deploy.py
```
