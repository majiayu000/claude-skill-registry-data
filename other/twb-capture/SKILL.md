---
name: twb-capture
description: Capturer un pattern de code recurrent et le cristalliser comme block TWB reutilisable
disable-model-invocation: true
argument-hint: "[description du pattern a capturer]"
allowed-tools: Read, Grep, Glob, Bash
---

# Capturer un pattern en block TWB

Analyser le code recemment genere et le cristalliser en block reutilisable.

## Etape 1 — Identifier le pattern

Examiner les fichiers touches dans la session ou le pattern decrit par l'utilisateur.
Determiner :
- La structure repetitive (quels fichiers, quelle arborescence)
- Les parties variables (noms, URLs, configs)
- Les parties fixes (structure, imports, patterns)

## Etape 2 — Templatiser

Remplacer les parties variables par des variables TWB `{{VAR_NAME}}` :
```
{{NAME}} — nom du composant/module
{{BASE_URL}} — URL de base
{{PORT}} — port du service
```

## Etape 3 — Creer le block

```bash
twb add <type> <name> --var "NAME=valeur" --var "BASE_URL=https://..."
```

Types disponibles : adapter, workflow, schema, config, frontend, preset

## Etape 4 — Documenter

Ajouter un commentaire en tete du block avec :
- Cas d'usage
- Variables requises
- Exemple d'invocation

## Etape 5 — Verifier

```bash
twb info <type> <name>
```

Confirmer que le block est bien enregistre et utilisable.

$ARGUMENTS
