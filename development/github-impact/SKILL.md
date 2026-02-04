---
name: github-impact
description: >
  Génère automatiquement deux rapports d'impact (métier et technique) pour une PR GitHub
  et les intègre dans la description.
allowed-tools: [Bash, Read, Write, TodoWrite, Grep, Glob]
model: claude-opus-4-1-20250805
---

# GitHub PR Impact Analysis Skill

## Usage
```
/github:impact <pr-number>
```

## Workflow

1. Récupérer infos PR via `gh pr view`
2. Identifier fichiers modifiés (`gh pr diff`)
3. Analyser dépendances et templates
4. Analyser tests
5. Générer rapport métier
6. Générer rapport technique
7. Ajouter rapports à la description PR
8. Sauvegarder localement dans `.analysis-reports/`

## Rapports générés

### Rapport Métier
- Vue d'ensemble (portée, domaines, risque)
- Changements fonctionnels (nouvelles features, améliorations, corrections)
- Impact utilisateur (UX, performance, compatibilité)
- Risques identifiés + recommandations

### Rapport Technique
- Métriques (fichiers, ajouts, suppressions)
- Analyse par type (PHP, JS, Templates, Config, Assets)
- Changements architecturaux (classes, dépendances)
- Analyse sécurité
- Couverture tests
- Points d'attention (performance, compatibilité, dette technique)

## Templates détaillés

- [Rapport métier](references/business-report-template.md) - Structure et niveaux de risque
- [Rapport technique](references/technical-report-template.md) - Métriques et scripts d'analyse

## Output

```bash
# Dans la PR
<!-- IMPACT-REPORTS-START -->
[Rapport métier]
[Rapport technique]
<!-- IMPACT-REPORTS-END -->

# Local
.analysis-reports/impact_pr_{PR_NUMBER}.md
```

## Error Handling

- PR introuvable → ARRÊT
- Échec mise à jour PR → WARNING (non bloquant)
