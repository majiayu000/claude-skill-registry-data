---
name: memory-kg-auto
description: Automatically recall and save project memory using the Knowledge Graph MCP server at session start and end. Use by default for any software engineering task to maintain cross-session context.
---

# Memory KG Auto — Mémoire persistante automatique

## Quand s'activer

S'active automatiquement pour toute tâche d'ingénierie afin de maintenir la continuité entre sessions.

## Rituel de début de session

Au démarrage de chaque session, avant toute action productive :

1. Charger le skill `memory-kg`.
2. Exécuter :
   - `search_nodes("pariscore")`
   - `search_nodes("architecture")`
   - `search_nodes("conventions")`
   - `search_nodes("bugs")`
   - `search_nodes("user preferences")`
   - `search_nodes("decisions")`
3. Lire les entités pertinentes avec `open_nodes`.
4. Synthétiser en un paragraphe.

Si aucune mémoire n'existe, indiquer : "No prior memory found — starting fresh."

## Auto-save en cours de session

Sauvegarder immédiatement quand :

| Trigger | Entité |
|---------|--------|
| Préférence utilisateur | `user-preferences` |
| Décision architecturale | `pariscore-architecture` |
| Bug non trivial | `pariscore-bugs` |
| Convention projet | `pariscore-conventions` |
| Correction utilisateur | `user-preferences` + `pariscore-conventions` |

## Rituel de fin de session

Avant la fin de session ou d'une tâche significative :

1. `pariscore-session-log`
2. Nouvelles préférences.
3. Nouvelles conventions.
4. Bugs / leçons.
5. Décisions architecturales.

## Recherche avant édition

Avant de modifier un fichier, exécuter `search_nodes("nom-du-fichier")`.

## Règles

- Le code fait foi sur la mémoire.
- Éviter les doublons avec `search_nodes` avant `create_entities`.
- Observations concises et factuelles.
