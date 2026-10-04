---
name: coolify-deploy
description: WarRoom-specifik Coolify-deployment — trigga deploys och inspektera tjänster via Coolify API (portad från IronForge)
version: 1.0.0
category: automation
owner: "@infrastructure"
platforms: ["windows", "linux", "macos"]
requires: []
---

# 🚀 Coolify Deploy Skill (WarRoom)

Coolify hostar **WarRoom Web Lite** — den webbläsarbaserade varianten av appen.

## Connection Details

| Webhook| Secret | Syfte |
|:---|:---|
| `COOLIFY_WEBHOOK` | Prod: Web Lite Deployment (main-branch) |
| `COOLIFY_STAGING_WEBHOOK` | Staging: Web Lite Deployment (develop-branch) |
| `COOLIFY_API_TOKEN` | API-åtkomst för att skapa/hantera tjänster |

## Deployment Flow

1. **Automatisk deploy** triggas via `coolify-deploy.yml` vid en GitHub Release.
2. **Manuell deploy**: Kör `workflow_dispatch` på `coolify-deploy.yml` i GitHub Actions UI.
3. **Direkt API**:

```powershell
# Hämta COOLIFY_API_TOKEN från GitHub Secrets / miljövariabel
$token = $env:COOLIFY_API_TOKEN
$coolifyHost = "http://<din-server>:8000"
$headers = @{
    "Authorization" = "Bearer $token"
    "Accept"        = "application/json"
}
# Lista alla tjänster
Invoke-RestMethod -Uri "$coolifyHost/api/v1/services" -Headers $headers
```

## WarRoom-tjänster på Coolify

| Tjänst | Typ | Beskrivning |
|:---|:---|:---|
| **WarRoom-web** | Static Site (Nginx/Caddy) | Web Lite Mode (React/Vite build) |

## Webhook-trigger (GitHub → Coolify)

```bash
# Trigga omdeployment manuellt
curl -X GET "$COOLIFY_WEBHOOK"
```

## Viktiga noter

- Web Lite kör `npm run build` och serverar `dist/`-mappen som static site
- `COOLIFY_WEBHOOK` och `COOLIFY_API_TOKEN` måste sättas som GitHub Secrets i repot
- Tauri Desktop/Mobile-appar deployas **inte** via Coolify — de distribueras via GitHub Releases
