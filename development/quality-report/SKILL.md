---
name: 'quality-report'
description: "Génère un rapport complet de qualité du code incluant les vérifications TypeScript, Biome (lint/format), les tests et la couverture de code. Utilise ce skill quand l'utilisateur demande un rapport de qualité, un audit de code, ou veut vérifier l'état général du projet."
---

# Rapport de Qualité du Code

## Objectif

Ce skill exécute une suite complète de vérifications de qualité du code et génère un rapport structuré en JSON et Markdown. Il est conçu pour :

- Vérifier la conformité TypeScript (typecheck)
- Valider le linting et le formatage avec Biome
- Exécuter les tests unitaires
- Analyser la couverture de code
- Fournir un rapport détaillé et actionnable

## Processus d'exécution

1. **Demander confirmation à l'utilisateur** (optionnel) :
   - Demander si l'utilisateur souhaite un rapport complet ou ciblé (uniquement certaines vérifications)
   - Demander le niveau de détail souhaité

2. **Exécuter le script de rapport** :
   - Utiliser le script `.claude/skills/quality-report/scripts/generate-quality-report.sh` qui orchestrera toutes les vérifications
   - Le script génère automatiquement un fichier JSON avec les résultats détaillés dans `.claude/quality-system/reports/`

3. **Analyser les résultats** :
   - Lire le fichier JSON généré
   - Identifier les problèmes critiques et non-critiques
   - Calculer un score de qualité global

4. **Présenter le rapport** :
   - Utiliser le template `.claude/skills/quality-report/resources/report-template.md` pour formater la sortie
   - Inclure des recommandations basées sur les erreurs détectées
   - Proposer des actions correctives si nécessaire

## Variables d'environnement utilisées

- `CLAUDE_PROJECT_DIR` : Répertoire racine du projet
- `QUALITY_REPORT_FORMAT` : Format du rapport (json, markdown, both) - défaut: both
- `QUALITY_REPORT_DETAILED` : Niveau de détail (true/false) - défaut: true

## Exemples d'utilisation

### Exemple 1 : Rapport complet demandé par l'utilisateur

**Entrée utilisateur :** "Peux-tu me générer un rapport de qualité du code ?"

**Actions du skill :**

1. Exécuter `.claude/skills/quality-report/scripts/generate-quality-report.sh`
2. Lire le JSON de résultats dans `.claude/quality-system/reports/`
3. Formater selon le template Markdown
4. Présenter le rapport avec recommandations

**Sortie attendue :**

```markdown
# 📊 Rapport de Qualité du Code

**Date :** 2025-10-29 14:30:00
**Projet :** sebc.dev

## Résumé Exécutif

✅ Score global : 85/100

## Détails des Vérifications

### ✓ TypeScript Type Check

- Status: ✅ Passed
- Durée: 2.3s
- Aucune erreur de type détectée

### ⚠ Biome Linting

- Status: ⚠️ Warning
- Durée: 1.1s
- 3 warnings détectés dans apps/web/src/components/Button.tsx

### ✓ Tests Unitaires

- Status: ✅ Passed
- Tests: 42 passed, 0 failed
- Durée: 5.7s

### ✓ Couverture de Code

- Status: ✅ Passed
- Coverage: 87.5% (seuil: 80%)
- Fichiers non couverts: 2

## Recommandations

1. Corriger les 3 warnings Biome dans Button.tsx
2. Améliorer la couverture pour les fichiers: utils/api.ts, hooks/useAuth.ts
```

### Exemple 2 : Rapport ciblé après modification

**Entrée utilisateur :** "J'ai modifié le composant Login, vérifie que tout est OK"

**Actions du skill :**

1. Identifier les fichiers modifiés (Login.tsx, Login.test.tsx)
2. Exécuter les vérifications ciblées
3. Générer un rapport focalisé

**Sortie attendue :**

```markdown
# 📊 Rapport de Qualité - Composant Login

## Vérifications Ciblées

- Fichiers analysés: Login.tsx, Login.test.tsx

### ✓ TypeScript : OK

### ✓ Linting : OK

### ✓ Format : OK

### ✓ Tests : 8/8 passed

✅ Tous les contrôles sont passés pour le composant Login
```

## Gestion des erreurs

Si une vérification échoue de manière critique (typecheck failed, tests failed) :

1. **NE PAS bloquer** l'affichage du rapport
2. **Mettre en évidence** les erreurs critiques
3. **Proposer des solutions** basées sur le type d'erreur :
   - Type errors → Vérifier les interfaces et types
   - Lint errors → Lancer `pnpm --filter web format`
   - Test failures → Analyser les logs de test et proposer des corrections

## Notes importantes

- Ce skill utilise les mêmes vérifications que le hook PostToolUse automatique (`.claude/quality-system/hooks/quality-check.sh`)
- Il peut être invoqué manuellement à tout moment
- Les rapports sont sauvegardés dans `.claude/quality-system/reports/quality-{timestamp}.md`
- Le script est non-bloquant : il rapporte les erreurs mais ne stoppe pas l'exécution
