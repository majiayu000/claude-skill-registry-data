---
name: smart
description: "Auto-apprentissage a partir des echecs et corrections — use when diagnosing errors, fixing bugs, or learning from recurring failure patterns"
model: sonnet
allowed-tools: Read, Bash, Grep, Glob, Edit
---

# Smart Learning — chainskills

Quand une erreur survient pendant le developpement du projet chainskills, suis ce processus d'auto-apprentissage.

## Workflow d'apprentissage

1. **Identifier** l'erreur (type, message, stack trace)
2. **Diagnostiquer** la cause racine (pas le symptome)
3. **Corriger** en appliquant les principes d'architecture
4. **Memoriser** le pattern pour eviter la recurrence

## Patterns frequents — chainskills

### Architecture violations

| Erreur | Cause | Fix |
|---|---|---|
| Import externe dans `src/core/` | Dependency Rule violation | Creer un port + adapter |
| Adapter instancie dans le CLI | Couplage direct | Utiliser le DI container |
| `throw` dans un use case | Wrong error pattern | Retourner `Result<T, E>` |
| `any` dans une signature | Typage faible | Utiliser generics ou `unknown` |

### Parser errors

| Erreur | Cause | Fix |
|---|---|---|
| Directive non reconnue | Plugin remark manquant | Verifier `remark-directive` config |
| Frontmatter invalide | Schema YAML incorrect | Valider avec Zod schema |
| Variable `$name` non resolue | Template engine miss | Verifier le contexte d'execution |

### Runtime errors

| Erreur | Cause | Fix |
|---|---|---|
| Step timeout | Pas de timeout configure | Ajouter timeout dans la config |
| MCP connection failed | Serveur non demarre | Verifier `chainskills serve` |
| State lost between steps | Mauvais state backend | Verifier `CHAINSKILLS_STATE_BACKEND` |

## Anti-patterns a eviter

- Ne pas importer un package npm dans `src/core/`
- Ne pas hardcoder des valeurs (URLs, seuils, secrets)
- Ne pas utiliser `console.log` au lieu du logger structure
- Ne pas faire de catch global qui avale les erreurs
- Ne pas ecrire de tests qui dependent de l'infra (DB, reseau, filesystem)
