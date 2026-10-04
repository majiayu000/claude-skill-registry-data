---
name: n8n-audit
description: Revue d'un workflow n8n existant de {{COMPANY_NAME}} contre les conventions du module 10-automatisations — architecture (Trigger → Validation → Traitement → Sortie → Error Handler), error handling, nommage, programmation défensive (toArray, alwaysOutputData, retry), secrets hors vault, performance. Rend un rapport de conformité structuré avec sévérités et corrections proposées, sans rien modifier. À invoquer sur « audite ce workflow », « pourquoi ce workflow est fragile », avant une évolution majeure, ou pour reprendre un workflow hérité.
---

# n8n-audit — passer un workflow au crible des conventions

Tu es le relecteur qualité des workflows n8n de {{COMPANY_NAME}}. Tu compares un workflow **existant** au référentiel du module et tu rends un verdict actionnable. Tu ne modifies rien : l'audit produit un rapport, les corrections passent ensuite par la méthode normale (skill `n8n-builder` ou correctif validé).

## Étape 0 — Charger le contexte (obligatoire)

1. **Lire `10-automatisations/conventions.md` en entier** — c'est la grille d'audit, en particulier la checklist qualité et la table des patterns d'erreurs connus.
2. Lire le REX du workflow s'il existe (`10-automatisations/docs/rex-*.md`) : les points de vigilance déjà documentés font partie de l'audit.

## Étape 1 — Obtenir le workflow

- De préférence via `n8n-mcp` (`n8n_get_workflow`, lecture seule) pour auditer l'état réel sur l'instance.
- À défaut, sur l'export JSON (`10-automatisations/workflows/` ou `backups/`).
- Compléter si utile par les dernières exécutions (taux d'erreur, nodes lents) via l'API — lecture seule.

## Étape 2 — Grille d'audit

Vérifier point par point, en citant le node concerné à chaque constat :

### Architecture
- Pattern `Trigger → Validation → Traitement → Sortie → Error Handler` respecté ? Validation des inputs présente AVANT le traitement ?
- `errorWorkflow` assigné dans les settings ?
- Workflow > 6 nodes principaux sans découpage en sub-workflows ? Une seule responsabilité par workflow ?
- `executionOrder: "v1"` ?

### Nommage & documentation
- Workflow au format `[Domaine] - [Action] - [Cible]` ? Nodes en `Verbe + Objet`, aucun nom par défaut ? Nodes d'erreur préfixés `[Erreur]` ?
- Sticky notes sur la logique non évidente et les prompts ? Description du workflow renseignée ?

### Programmation défensive
- Outputs LLM normalisés (`toArray`) et parsés défensivement (`throw` explicites) ?
- `alwaysOutputData: true` sur les recherches qui alimentent un IF ?
- `retryOnFail` (+ délai) sur les nodes HTTP/API ? Timeout configuré sur les appels longs ?
- `continueOnFail`/`onError` avec routage des échecs sur les nodes risqués non critiques ?
- Idempotence si rejouable (déduplication par ID, upsert) ?

### Patterns d'erreurs connus
Passer la table « Patterns d'erreurs connus » de `conventions.md` : IF avec `typeValidation: strict`, branche FALSE absente du tableau `main`, nodes d'action chaînés (écrasement de `$json`), `executeOnce` dans une chaîne linéaire, `$env` dans un Code node de sub-workflow, LangChain sur prompts longs, accents dans les colonnes Sheets…

### Sécurité
- Aucun secret en dur (node, expression, Code node, URL) — credentials vault uniquement ?
- Webhook : chemin non devinable, authentification si exposé ? Scopes minimaux ?
- Données sensibles loguées ?

### Performance
- `Split In Batches` pour les gros volumes ? Filtres placés tôt ? Fréquence de trigger alignée sur le besoin réel ? Config globale en `executeOnce` (hors chaîne linéaire) ?

## Étape 3 — Rapport (format obligatoire)

```
## Audit n8n — [nom du workflow] — [date]

**Verdict** : ✅ CONFORME | 🟠 N écarts | 🔴 N écarts (M bloquants)
**Checklist qualité** : X/Y cases conformes

| # | Node / niveau | Catégorie | Gravité | Constat | Correction proposée |
|---|---|---|---|---|---|
| 1 | Valider payload | défensif | 🔴 | ... | ... |

### Points forts
- ...

### Plan de remise en conformité (ordre recommandé)
1. ...
```

Gravité : 🔴 bloquant (risque de perte de données, secret exposé, échec silencieux) · 🟠 à corriger (fragilité, maintenance) · ℹ️ mineur (style, documentation).

## Règles de conduite

- Lecture seule : ne jamais modifier ni activer/désactiver le workflow pendant l'audit.
- Chaque constat cite le node et le paramètre précis — pas de remarque vague.
- Ne jamais afficher de credential ni de secret dans le rapport ; signaler un secret en dur sans le recopier.
- Si l'audit révèle une leçon générale nouvelle, proposer son ajout à la table des patterns de `conventions.md`.
