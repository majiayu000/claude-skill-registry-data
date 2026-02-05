---
name: julien-ref-astro-install
description: Guide d'installation Astro + Tailwind sur Windows. Covers Node.js setup, pnpm, project creation, common Windows issues, and troubleshooting.
triggers:
  - installer astro
  - démarrer un projet astro
  - astro sur windows
  - erreur installation astro
  - how to install astro
  - getting started with astro
  - astro tailwind setup
  - astro
  - astro install
  - create astro project
---

# Guide d'Installation Astro + Tailwind sur Windows

**Testé sur** : Windows 10/11, Node.js 23.7.0

---

## Prérequis

### 1. Node.js (version 18.20.8+ ou 20.3.0+ ou 22.0.0+)
- Télécharger depuis : https://nodejs.org/
- Installer la version **LTS** (Long Term Support)
- Vérifier l'installation :
  ```powershell
  node --version
  # Doit afficher v18+ ou v20+ ou v22+
  ```

### 2. Gestionnaire de paquets
**Important** : Sur Windows, **pnpm** est plus fiable que npm.

```powershell
# Installer pnpm globalement
npm install -g pnpm

# Vérifier
pnpm --version
```

---

## Méthode 1 : Installation Rapide (Recommandée)

### Étape 1 : Créer le projet
```powershell
# Aller dans le dossier de travail
cd "C:\Users\VotreNom\OneDrive\Coding\MonProjet"

# Créer le projet Astro avec pnpm
pnpm create astro@latest mon-site
```

### Étape 2 : Choix lors de l'assistant
- **Template** : Empty (ou Minimal selon besoin)
- **TypeScript** : No (ou Yes si vous le souhaitez)
- **Install dependencies** : Yes
- **Initialize git** : Yes (recommandé)

### Étape 3 : Ajouter Tailwind CSS
```powershell
cd mon-site
pnpm astro add tailwind
# Accepter toutes les modifications (tapez "y")
```

### Étape 4 : Lancer le serveur
```powershell
pnpm run dev
```

Le site sera accessible sur **http://localhost:4321**

---

## Méthode 2 : Installation Manuelle (Si problèmes)

### Étape 1 : Créer la structure
```powershell
mkdir mon-site
cd mon-site
pnpm init
```

### Étape 2 : Installer les dépendances
```powershell
pnpm add astro @astrojs/tailwind tailwindcss
```

### Étape 3 : Créer les fichiers de configuration

**package.json** :
```json
{
  "name": "mon-site",
  "type": "module",
  "version": "1.0.0",
  "scripts": {
    "dev": "astro dev",
    "build": "astro build",
    "preview": "astro preview"
  },
  "dependencies": {
    "astro": "^5.14.3",
    "@astrojs/tailwind": "^5.1.5",
    "tailwindcss": "^3.4.18"
  }
}
```

**astro.config.mjs** :
```javascript
import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';

export default defineConfig({
  integrations: [tailwind()],
});
```

**tailwind.config.mjs** :
```javascript
/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

### Étape 4 : Créer la structure de dossiers
```powershell
mkdir -p src/pages
mkdir -p src/layouts
mkdir -p src/components
mkdir -p src/styles
mkdir public
```

### Étape 5 : Créer le fichier CSS global

**src/styles/global.css** :
```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

### Étape 6 : Créer un layout de base

**src/layouts/Layout.astro** :
```astro
---
import '../styles/global.css';

interface Props {
  title: string;
}

const { title } = Astro.props;
---

<!doctype html>
<html lang="fr">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width" />
    <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
    <title>{title}</title>
  </head>
  <body>
    <slot />
  </body>
</html>
```

### Étape 7 : Créer une page d'accueil

**src/pages/index.astro** :
```astro
---
import Layout from '../layouts/Layout.astro';
---

<Layout title="Mon Site Astro">
  <main class="min-h-screen bg-gray-100 flex items-center justify-center">
    <div class="text-center">
      <h1 class="text-4xl font-bold text-blue-600 mb-4">
        Bienvenue sur Astro + Tailwind
      </h1>
      <p class="text-gray-700">
        Votre site est prêt !
      </p>
    </div>
  </main>
</Layout>
```

---

## Problèmes Courants sur Windows

### Problème 1 : `npm error ERR_INVALID_ARG_TYPE`
**Solution** : Utiliser pnpm au lieu de npm
```powershell
npm install -g pnpm
pnpm install
```

### Problème 2 : Erreur de permissions
**Solution** : Lancer PowerShell en administrateur
- Clic droit sur PowerShell → "Exécuter en tant qu'administrateur"

### Problème 3 : Scripts désactivés
**Erreur** : `cannot be loaded because running scripts is disabled`

**Solution** :
```powershell
# Lancer PowerShell en administrateur
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Problème 4 : Chemins avec espaces
**Mauvais** :
```powershell
cd C:\Users\Nom Prénom\Mon Projet
```

**Bon** :
```powershell
cd "C:\Users\Nom Prénom\Mon Projet"
```

### Problème 5 : Port 4321 déjà utilisé
**Solution** : Changer le port dans `astro.config.mjs` :
```javascript
export default defineConfig({
  server: { port: 3000 },
  integrations: [tailwind()],
});
```

---

## Structure de Projet Recommandée

```
mon-site/
├── public/                 # Assets statiques (images, fonts)
│   └── favicon.svg
├── src/
│   ├── layouts/
│   │   └── Layout.astro    # Layout principal
│   ├── components/
│   │   ├── Header.astro
│   │   ├── Footer.astro
│   │   └── Button.astro
│   ├── pages/
│   │   ├── index.astro     # Page d'accueil (/)
│   │   ├── about.astro     # Page à propos (/about)
│   │   └── contact.astro   # Page contact (/contact)
│   └── styles/
│       └── global.css      # CSS global + Tailwind
├── astro.config.mjs        # Config Astro
├── tailwind.config.mjs     # Config Tailwind
├── package.json
└── tsconfig.json
```

---

## Commandes Essentielles

| Commande | Description |
|----------|-------------|
| `pnpm run dev` | Lancer serveur développement |
| `pnpm run build` | Build pour production |
| `pnpm run preview` | Prévisualiser le build |
| `pnpm astro add [integration]` | Ajouter une intégration |
| `pnpm astro check` | Vérifier erreurs TypeScript |

---

## Intégrations Utiles

### Ajouter React
```powershell
pnpm astro add react
```

### Ajouter Markdown
```powershell
pnpm astro add mdx
```

### Ajouter Sitemap
```powershell
pnpm astro add sitemap
```

---

## Hot Tips Windows

1. **Utilisez Windows Terminal** au lieu de PowerShell classique
   - Téléchargez depuis Microsoft Store
   - Meilleure expérience de développement

2. **Utilisez VS Code** avec l'extension Astro officielle
   - Extension : "Astro" (officielle)
   - Coloration syntaxique + autocomplete

3. **Git Bash** comme alternative
   - Si vous préférez les commandes Linux-style
   - Inclus avec Git for Windows

4. **WSL2** pour un environnement Linux
   - Plus stable pour le développement
   - Installation : `wsl --install`

---

## Checklist de Vérification

Avant de commencer à développer :

- [ ] Node.js ≥18 installé
- [ ] pnpm installé globalement
- [ ] Projet Astro créé
- [ ] Tailwind CSS intégré
- [ ] Serveur dev lance sans erreur (`pnpm run dev`)
- [ ] http://localhost:4321 accessible
- [ ] VS Code + Extension Astro installés
- [ ] Git initialisé (optionnel mais recommandé)
