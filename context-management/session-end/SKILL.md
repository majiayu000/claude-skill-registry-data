---
name: session-end
description: Sauvegarder l'etat de la session dans toutes les bases memoire (CRAG, KV, Knowledge Graph, Memory fichiers). Invoquer en fin de session.
disable-model-invocation: true
argument-hint: "[resume optionnel de la session]"
---

# Procedure de fin de session

Sauvegarder le travail de cette session dans TOUTES les bases memoire.

## Etape 1 — Resume de session (CRAG Session)

Appeler `mcp__crag__session_save` avec :
- `project` : nom du projet principal
- `summary` : resume en 2-3 phrases du travail fait
- `decisions` : decisions prises (comma-separated)
- `files_touched` : fichiers modifies (comma-separated)
- `errors` : erreurs rencontrees (comma-separated)
- `patterns_used` : patterns TWB utilises

## Etape 2 — Patterns et decisions (CRAG Vectoriel)

Pour chaque pattern, convention, ou decision importante decouverte :
Appeler `mcp__crag__memory_store` avec un `id` unique, `type` (pattern/decision/convention), `project`, et `tags`.

## Etape 3 — Configs rapides (CRAG KV)

Pour chaque port, commande, ou config decouverte :
Appeler `mcp__crag__kv_set` avec `key` (format projet:sujet), `value`, `category`.

## Etape 4 — Knowledge Graph

Appeler `mcp__memory__add_observations` pour enrichir les entites existantes avec les nouvelles observations.
Si de nouvelles entites ont ete decouvertes, appeler `mcp__memory__create_entities`.

## Etape 5 — Memory fichiers

Si des feedbacks utilisateur, preferences, ou contexte projet importants ont ete decouverts :
Creer ou mettre a jour les fichiers `.md` dans `.claude/projects/*/memory/`.
Mettre a jour `MEMORY.md` avec un pointeur vers chaque nouveau fichier.

## Etape 6 — Identification TWB

Lister les patterns de code generes dans cette session qui pourraient devenir des blocks TWB.
Pour chaque pattern recurrent identifie, noter :
- Nom du block potentiel
- Variables a templatiser
- Cas d'usage

Ne PAS creer les blocks (faire ca dans une session dediee avec `/twb-capture`).

## Etape 7 — Rapport final

Afficher un resume :
- Nombre d'items sauvegardes par base
- Patterns TWB identifies
- Usage estime de tokens cette session

$ARGUMENTS
