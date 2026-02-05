---
name: elegant-objects
description: >
  Vérifie la conformité du code PHP aux principes Elegant Objects de Yegor Bugayenko.
  Analyse un fichier spécifique ou tous les fichiers modifiés dans la branche.
allowed-tools: [Bash, Read, Grep, Glob]
model: sonnet
---

# Elegant Objects Reviewer Skill

## Usage
```
/qa:elegant-objects [fichier.php]
```
Sans argument : analyse les fichiers PHP modifiés dans la branche.

## Workflow

1. Déterminer fichiers à analyser (argument ou git diff)
2. Vérifier les règles Elegant Objects
3. Générer rapport avec score

## Règles vérifiées

### Classes
- Classes `final` (sauf abstraites)
- Max 4 attributs
- Pas de getters/setters
- Pas de méthodes statiques
- Noms sans -er (Manager, Handler, Helper...)
- Constructeur unique et simple

### Méthodes
- Pas de retour `null`
- Pas d'argument `null`
- Corps sans lignes vides ni commentaires
- CQRS : séparation commandes/queries

### Tests
- Une assertion par test (dernière instruction)
- Noms en français décrivant le comportement
- Pas de setUp/tearDown

## Score

- Violation critique: -10 points
- Violation majeure: -5 points
- Recommandation: -2 points
- Base: 100

## References

- [Patterns de détection](references/detection-patterns.md) - Regex et règles détaillées

## Notes
- Ignorer vendor/, var/, cache/
- Controllers Symfony tolérés
- Prioriser par criticité
