---
name: "github-pr-collector"
description: "Collecte et analyse les Pull Requests GitHub avec leurs commentaires d'agents de review IA (CodeRabbit, GitHub Copilot, Codex, etc.). Utilise GitHub CLI pour récupérer les données, extrait les métadonnées des agents avec jq, et génère une structure organisée par PR et par importance dans le dossier .scd du projet. Extensible pour supporter de nouveaux agents de review."
version: "1.0.0"
dependencies:
  - "github-cli >= 2.0.0"
  - "jq >= 1.6"
---

# GitHub PR Collector Skill

## Objectif

Ce skill automatise la collecte et l'extraction des données des Pull Requests GitHub, avec support pour multiple agents de review IA (CodeRabbit, GitHub Copilot, Codex, et autres). Il optimise l'utilisation des tokens en préprocessant les données via des scripts Bash et organise les commentaires par PR et par niveau d'importance.

## Processus

### 1. Collecte des Données

Le skill utilise le script `collect-pr-data.sh` pour :
- Identifier le repository courant via `gh repo view`
- Récupérer la liste des PR en cours avec `gh pr list`
- Pour chaque PR, extraire les métadonnées complètes
- Télécharger tous les commentaires de review

### 2. Extraction des Métadonnées des Commentaires

Le script intégré extrait automatiquement :
- Les métadonnées des commentaires (id, auteur, URL)
- La sévérité via emojis (🔴 Critical, 🟠 Major, 🟡 Minor, 🔵 Trivial)
- Le titre et la description de chaque commentaire
- Classification automatique par dossiers de sévérité
- Génération d'une checklist triée par priorité

### 3. Génération de Résumés

Le script génère automatiquement :
- Un résumé détaillé par PR avec statistiques par sévérité
- Un rapport global `pr-analysis-report.md` avec vue d'ensemble
- Une checklist de suivi des commentaires triée par priorité
- Des fichiers Markdown individuels pour chaque commentaire

## Utilisation

### Déclencheurs Typiques
- "Analyse les PR en cours de ce repository"
- "Que disent les agents de review sur les dernières PR ?"
- "Donne-moi un résumé des reviews des PR ouvertes"
- "Quels sont les problèmes identifiés par les agents IA ?"
- "Collecte les données des PR pour analyse"

### Workflow Recommandé

**Étape 1 : Collecte des données** (ce skill)
```
"Collecte les données des PR en cours"
```

**Étape 2 : Analyse approfondie** (subagent pr-review-analyzer)
```
"Utilise le subagent pr-review-analyzer pour analyser les données collectées"
ou simplement
"Analyse les données des PR collectées"
```

Le subagent `pr-review-analyzer` dispose de capacités d'analyse avancées :
- Génération d'insights et de tendances
- Identification de patterns récurrents
- Recommandations d'amélioration priorisées
- Rapports exécutifs et techniques personnalisés

### Sortie

Les données sont stockées dans `.scd/github-pr-collector/` avec la structure :
```
.scd/github-pr-collector/
├── config/
│   ├── agents-patterns.json      # Configuration des agents IA
│   └── severity-mapping.json     # Mapping de sévérité
├── cache/                         # Cache temporaire (auto-nettoyé)
├── data/
│   └── pr-data/
│       ├── pr-{number}/
│       │   ├── 🔴 Critical/      # Commentaires critiques
│       │   ├── 🟠 Major/         # Commentaires majeurs  
│       │   ├── 🟡 Minor/         # Commentaires mineurs
│       │   ├── 🔵 Trivial/       # Commentaires triviaux
│       │   ├── Unclassified/     # Commentaires non classés
│       │   ├── COMMENTS_CHECKLIST.md  # Checklist triée par priorité
│       │   └── summary.md        # Résumé de la PR
│       └── pr-analysis-report.md # Rapport global
└── collect-pr.log                # Logs d'exécution
```

Un résumé est affiché à l'utilisateur avec :
- Nombre de PR analysées
- Distribution des commentaires par sévérité
- Statistiques détaillées par PR
- Lien vers les fichiers détaillés générés

## Gestion des Erreurs

Le skill gère gracieusement :
- L'absence de GitHub CLI ou d'authentification
- Les repositories sans PR
- Les PR sans commentaires d'agents IA
- Les limites de taux de l'API GitHub

## Référence

Les scripts utilisent les ressources suivantes :
- `scripts/collect-pr-data.sh` - Script principal de collecte et extraction
- `scripts/exemple.sh` - Script d'exemple pour l'extraction de métadonnées
- `.scd/github-pr-collector/config/` - Fichiers de configuration JSON
  - `agents-patterns.json` - Patterns de détection des agents IA
  - `severity-mapping.json` - Configuration des niveaux de sévérité