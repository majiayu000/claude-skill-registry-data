---
name: netlify-deploy
description: Déploiement et gestion du site MyGGV GPS sur Netlify. Utiliser pour déployer, vérifier le statut, gérer les variables d'environnement et les configurations de projet.
allowed-tools:
  - mcp__netlify__netlify-deploy-services-reader
  - mcp__netlify__netlify-deploy-services-updater
  - mcp__netlify__netlify-project-services-reader
  - mcp__netlify__netlify-project-services-updater
  - mcp__netlify__netlify-user-services-reader
  - mcp__netlify__netlify-team-services-reader
  - mcp__netlify__netlify-extension-services-reader
  - mcp__netlify__netlify-coding-rules
  - Bash
  - Read
---

# Netlify Deploy - MyGGV GPS

## Objectif

Gérer le déploiement et la configuration du site MyGGV GPS sur Netlify.

## Périmètre

### Inclus

- Déploiement du site (`deploy-site`)
- Vérification du statut des déploiements
- Gestion des variables d'environnement
- Configuration du projet (nom, formulaires, accès)
- Vérification des extensions installées

### Exclus

- Base de données → utiliser `supabase-database`
- Documentation → utiliser `archon-project`

## Configuration Actuelle

### netlify.toml

```toml
[build]
  command = "npm run build:netlify"
  publish = "dist"

[build.environment]
  NODE_VERSION = "18"
  NPM_VERSION = "9"
```

### Variables d'Environnement Requises

- `VITE_SUPABASE_URL` - URL Supabase
- `VITE_SUPABASE_ANON_KEY` - Clé publique Supabase

## Workflow de Déploiement

### 1. Avant de déployer - Vérifier les règles

```javascript
mcp__netlify__netlify -
  coding -
  rules({
    creationType: "serverless", // ou "edge-functions", "blobs", etc.
  });
```

### 2. Build local pour test

```bash
npm run build:netlify
```

### 3. Déployer sur Netlify

```javascript
mcp__netlify__netlify -
  deploy -
  services -
  updater({
    selectSchema: {
      operation: "deploy-site",
      params: {
        deployDirectory: "/home/charles/Bureau/new-ggv-gps",
        siteId: "<site-id>", // Obtenir via netlify link ou get-projects
      },
    },
  });
```

### 4. Vérifier le déploiement

```javascript
mcp__netlify__netlify -
  deploy -
  services -
  reader({
    selectSchema: {
      operation: "get-deploy",
      params: { deployId: "<deploy-id>" },
    },
  });
```

## Gestion des Variables d'Environnement

### Lister les variables

```javascript
mcp__netlify__netlify -
  project -
  services -
  updater({
    selectSchema: {
      operation: "manage-env-vars",
      params: {
        siteId: "<site-id>",
        getAllEnvVars: true,
      },
    },
  });
```

### Ajouter/Modifier une variable

```javascript
mcp__netlify__netlify -
  project -
  services -
  updater({
    selectSchema: {
      operation: "manage-env-vars",
      params: {
        siteId: "<site-id>",
        upsertEnvVar: true,
        envVarKey: "VITE_SUPABASE_URL",
        envVarValue: "https://xxx.supabase.co",
        envVarIsSecret: false,
        newVarContext: "all",
      },
    },
  });
```

## Headers de Sécurité

Le fichier `public/_headers` configure :

- X-Frame-Options: DENY
- X-Content-Type-Options: nosniff
- Referrer-Policy: strict-origin-when-cross-origin
- Permissions-Policy: geolocation autorisé

## Commandes Utiles

### Lier le projet (CLI)

```bash
cd /home/charles/Bureau/new-ggv-gps
netlify link
```

### Obtenir le site ID

```javascript
mcp__netlify__netlify -
  project -
  services -
  reader({
    selectSchema: {
      operation: "get-projects",
      params: { projectNameSearchValue: "ggv" },
    },
  });
```

## Bonnes Pratiques

1. **Toujours builder localement** avant de déployer
2. **Vérifier les variables d'environnement** sont configurées
3. **Vérifier les headers** de sécurité avec les DevTools
