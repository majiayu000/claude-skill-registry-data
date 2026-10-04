---
name: playwright-mcp
description: "🌐 Serveur MCP Playwright (Microsoft) — automatisation navigateur Chromium/WebKit/Gecko via MCP. Navigation, capture screenshots, extraction DOM, soumission formulaires, PDF export, réseau intercept. 7ème serveur MCP de PariScore."
---

# 🌐 Playwright MCP Server

> **Source** : [microsoft/playwright-mcp](https://github.com/microsoft/playwright-mcp)
> **Type** : Serveur MCP (configuré dans `.mcp.json`) — PAS un skill de code
> **Auteur** : Microsoft — maintenu officiellement par l'équipe Playwright
> **Version** : `@playwright/mcp@latest` (npx)

## Pourquoi PariScore ?

| Avantage | Impact |
|----------|--------|
| **E2E visuel** | Ouvrir `localhost:3000`, naviguer onglets, capturer screenshots post-changement |
| **Scraping web fallback** | Si API externe down → naviguer directement la page source (Flashscore, SofaScore, ATP) |
| **Audit UI cross-browser** | Test visuel Chromium/Firefox/WebKit sans framework de test |
| **Extraction DOM** | Parser des pages non-API (classements, stats brutes) en récupérant le DOM nettoyé |
| **Validation responsive** | Simuler mobile/desktop pour vérifier les media queries de pariscore.html |
| **Débogage visuel** | Capturer screenshot d'un état bug → joindre au rapport d'incident |

## Configuration

Dans `.mcp.json` (déjà installé) :

```json
{
  "playwright": {
    "command": "npx",
    "args": ["-y", "@playwright/mcp@latest"]
  }
}
```

## Outils MCP disponibles

| Outil | Description | Usage PariScore |
|-------|-------------|----------------|
| `browser_navigate` | Ouvrir une URL | `http://localhost:3000` pour E2E |
| `browser_screenshot` | Capture plein écran ou sélecteur | Vérifier UI après changement |
| `browser_click` | Cliquer sur un élément | Naviguer onglets (Football, Tennis, etc.) |
| `browser_fill` | Remplir un champ input | Tester formulaires de filtres |
| `browser_select` | Sélecteur dropdown | Changer filtres (ligue, statut) |
| `browser_hover` | Survoler un élément | Tooltips, menus dynamiques |
| `browser_evaluate` | Exécuter JS dans la page | Extraire données du DOM, vérifier state JS |
| `browser_file_upload` | Uploader un fichier | Non utilisé actuellement |
| `browser_close` | Fermer le navigateur | Cleanup après test |
| `browser_tab_list` | Lister les onglets | Multi-onglet testing |
| `browser_tab_select` | Sélectionner un onglet | Naviguer entre pages |
| `browser_pdf` | Exporter en PDF | Rapports automatiques |

## Workflows types PariScore

### 1. E2E Post-Deploy
```
browser_navigate → http://localhost:3000
browser_screenshot → homepage-baseline
browser_click → #tab-football
browser_screenshot → football-tab
browser_evaluate → document.querySelectorAll('.match-card').length
```

### 2. Scraping Fallback (API down)
```
browser_navigate → https://www.flashscore.com/tennis/
browser_evaluate → Array.from(document.querySelectorAll('.event__score')).map(e => e.textContent)
```

### 3. Audit Responsive
```
// Via browser_evaluate avec viewport simulation
browser_evaluate → window.innerWidth = 375; window.dispatchEvent(new Event('resize'))
browser_screenshot → mobile-view
```

## Limites & Précautions

- **Headless uniquement** en mode MCP (pas d'UI visible pendant l'exécution)
- **Premier lancement lent** : `npx` télécharge Playwright (~50MB) si pas installé
- **Anti-bot** : Certains sites bloquent Playwright (Cloudflare, reCAPTCHA) — utiliser en fallback seulement
- **Network** : L'outil `browser_network` intercepte les requêtes réseau (utile pour debug API calls)
- **Sécurité** : Ne JAMAIS naviguer vers des URLs avec des credentials en query string

## Serveur MCP #7

| # | Serveur | Type | Fonction |
|---|---------|------|----------|
| 1 | project_fs | npx filesystem | Navigation fichiers projet |
| 2 | memory | npx memory | Knowledge graph persistant |
| 3 | git | uvx git | Opérations git structurées |
| 4 | bzzoiro-sports | HTTP | Données sportives Bzzoiro |
| 5 | sportdbdotdev | HTTP | SportDB données sportives |
| 6 | sportradar | npx mcp-remote | Sportradar via RapidAPI |
| **7** | **playwright** | **npx playwright** | **Automatisation navigateur** |

## Métiers associés

- **Audit & QA** → E2E testing visuel, validation UI
- **Recherche Web** → Scraping fallback, extraction DOM
- **Sécurité & SRE** → Débogage visuel incident, capture screenshot
- **Ingénierie** → Développement assisté par navigateur, tests manuels
