---
name: framework:make:all
description: Génère tous les fichiers pour une entité complète (orchestrateur)
license: MIT
version: 1.0.0
---

# Framework Make All Skill

## Description
Orchestrateur générant une stack complète Elegant Objects + DDD pour une entité.

## Usage
```
Use skill framework:make:all
```

## Variables requises
- **{EntityName}** - Nom de l'entité en PascalCase (ex: Product)
- **{properties}** - Liste des propriétés avec types (optionnel)

## Skills orchestrées

1. `framework:make:contracts` (si absent)
2. `framework:make:entity`
3. `framework:make:out`
4. `framework:make:invalide`
5. `framework:make:urls`
6. `framework:make:collection`
7. `framework:make:factory`
8. `framework:make:story`

## Outputs

| Phase | Fichiers |
|-------|----------|
| Core | Entity, Repository, RepositoryInterface |
| Patterns | Out, Invalide |
| Avancé | Urls, UrlsMessage, UrlsMessageHandler, Collection |
| Tests | Factory, Story, AppStory |

## Workflow

1. Demander EntityName et propriétés
2. Vérifier/créer Contracts
3. Exécuter séquentiellement les 8 skills
4. Afficher résumé + prochaines étapes

## Ordre d'exécution

```
contracts → entity → out/invalide → urls/collection → factory → story
```

## Notes
- Orchestrateur sans templates propres
- Ordre critique (respecte dépendances)
- Idéal pour démarrer rapidement
