---
name: doppler
description: WarRoom secret management via Doppler — single source of truth för alla secrets. .env-filer är förbjudna.
version: 1.0.0
category: security
owner: "@security"
platforms: ["windows", "linux", "macos"]
---

# 🔐 Doppler Skill (WarRoom)

Doppler är **enda källan till sanning** för alla secrets i WarRoom. `.env`-filer är strikt förbjudna.

## Setup (en gång)

```powershell
# 1. Logga in
doppler login

# 2. Koppla projektet till mappen
doppler setup --project WarRoom --config prd
```

## Pre-flight (alltid)

```powershell
doppler me 2>$null | Out-Null
if ($LASTEXITCODE -ne 0) { Write-Error "Doppler ej inloggat. Kör: doppler login"; exit 1 }
```

## Kör kommandon med secrets

```powershell
# Kör ett script med secrets injicerade
doppler run -- pwsh scripts/mitt-script.ps1

# Starta dev-server med secrets
doppler run -- npm run dev
```

## Hämta ett enskilt secret

```powershell
$value = doppler secrets get COOLIFY_WEBHOOK --plain
```

## Lägg till ett nytt secret

```powershell
# Steg 1: Spara i Doppler
doppler secrets set MITT_SECRET="värdet"

# Steg 2: Pusha till GitHub
doppler secrets get MITT_SECRET --plain | gh secret set MITT_SECRET --repo Techlemariam/WarRoom
```

## Secrets i WarRoom

| Secret | Syfte |
|:---|:---|
| `COOLIFY_WEBHOOK` | Coolify Deploy Webhook URL för Web Lite |
| `SNYK_TOKEN` | Snyk säkerhetsscanning (nightly-maintenance) |
| `GH_PAT` | GitHub PAT för automatiserade workflows |

## Synk Doppler → GitHub (alla secrets)

För att pusha *alla* Doppler-secrets till GitHub på en gång, kör bootstrap-scriptet:

```powershell
.\scripts\setup-secrets.ps1
```

## Regler

1. **Aldrig** skapa eller committa `.env`-filer
2. **Alltid** använda `doppler run --` för kommandon som behöver secrets
3. CI/CD-workflows läser från GitHub Secrets (synkat manuellt via scriptet ovan)
