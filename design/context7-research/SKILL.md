---
name: context7-research
description: Workflow stratégique pour consulter la doc à jour des libs/frameworks via Context7 (anti-hallucination d'API)
---

# Skill : Recherche de doc Context7

Tu as accès à **Context7** (outils `resolve_library_id` et `query_docs`), qui donne la **documentation à jour** des bibliothèques et frameworks. C'est ton antidote à l'hallucination d'API : plutôt qu'inventer une signature de mémoire (souvent obsolète), tu consultes la source officielle.

## ⚠️ QUAND CHERCHER — Décision critique (ne gaspille pas d'étapes)

**CHERCHE** si la tâche implique une **lib/framework externe** dont tu n'es pas certain à 100% de l'API exacte. Exemples :
- React, Vue, Svelte, Angular, Solid (frameworks UI)
- Chart.js, D3.js, Three.js (visu/3D)
- Tauri, Electron (desktop)
- pandas, numpy, requests, FastAPI, Django, SQLAlchemy (Python)
- TailwindCSS, Bootstrap, Material UI (CSS/components)

**NE CHERCHE PAS** (ton expertise suffit, chercher = perte de temps et d'étapes) :
- HTML/CSS/JavaScript **vanilla pur** (DOM, events, localStorage, fetch, canvas...)
- **Algorithmes** de base (tri, recherche, graphes) — pas une question d'API
- Syntaxe du langage, structures de données, opérateurs
- Mathématiques, logique pure

**Règle d'or** : si tu hésites sur le nom d'une méthode, le nombre/type d'arguments, ou le comportement d'une option d'une lib externe → cherche. Sinon, code directement.

## 🎯 LE WORKFLOW en 3 temps (quand tu décides de chercher)

1. **RESOLVE** — appelle `resolve_library_id(query="<ce que tu veux faire>", libraryName="<nom officiel de la lib>")`.
   - `libraryName` avec la ponctuation officielle : `'Chart.js'` pas `'chartjs'`, `'Three.js'` pas `'threejs'`.
   - Parmi les résultats, retiens le libraryId au format `/org/project` (ex: `/chartjs/chart.js`).

2. **QUERY** — appelle `query_docs(libraryId="<id trouvé>", query="<ta question précise, UN sujet>")`.
   - Requête **spécifique et unique** : `'How to create a line chart with multiple datasets'` (bon) vs `'charts'` (trop vague).
   - Un seul concept par appel. Deux questions distinctes = deux appels.

3. **APPLIQUE** — utilise la signature API exacte que tu viens de lire pour **écrire ou corriger** ton code.
   - Ne te contente pas de lire : **intègre** ce que tu as appris (bon ordre d'arguments, options requises, patterns idiomatiques).

## 🛑 LIMITES strictes (anti-gaspillage)

- **Maximum 1 à 2 recherches par fichier**. Chaque appel consomme une étape sur ton budget (`max_steps=12`). Au-delà, tu risques de ne pas finir de coder.
- Dès le 1er `resolve_library_id`, choisis la lib **la plus probable**. Ne reviens pas en arrière.
- Ne cherche JAMAIS pour valider du code déjà écrit selon ta mémoire — fais confiance à ton premier jet sauf erreur explicite.

## 🪂 ÉCHEC GRACIEUX

Si un outil Context7 ne répond pas, renvoie une erreur, ou dépasse le temps : **continue sans doc**. Ta compétence de base suffit pour livrer un code fonctionnel. **Ne bloque jamais la tâche** sur Context7. N'essaie pas de relancer plusieurs fois — un échec = on passe.
