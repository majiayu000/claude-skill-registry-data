---
name: loop-autonomy
description: >
  Autonomous work loop in any project: process a backlog or plan queue item by item,
  fresh subagent per item, validate command as gate, one commit per item. Never
  claude -p. Triggers: "boucle autonome", "traite mon backlog en autonomie", "run
  nocturne", "loop-autonomy".
---

# Loop Autonomy — boucle de travail autonome, 100 % souscription

Tu vas traiter une file d'items de travail de façon autonome, item par item.
Le contrat qui rend ça fiable tient en une phrase :

> **Une itération = un item = un contexte frais = un commit = des
> post-conditions vérifiées par commande, jamais sur parole.**

Pourquoi : un agent qui s'auto-évalue déclare victoire trop tôt, un contexte
partagé accumule du bruit, un item sans vérification mesurable n'a pas de
« fini ». Chaque règle ci-dessous ferme l'un de ces trous.

**Jamais `claude -p` ni l'Agent SDK** : tout fonctionne dans la session
courante (subagents), via `/goal`, `/loop`, ou des tâches planifiées Desktop —
les mécanismes inclus dans la souscription. Si une étape te tente d'invoquer
`claude -p`, c'est que tu es en train de sortir du design : arrête-toi.

**Skills sœurs — route avant d'armer** : si l'utilisateur veut que le travail
tourne **sur le cloud** (routines claude.ai, machine locale possiblement
éteinte) ou qu'une session locale doit exécuter un plan à heure fixe, c'est
`brief-chantier` (`brief-chantier/references/nuits-planifiees.md`). Ce skill-ci
est la boucle LOCALE sur une file d'items.

## Étape 0 — L'adapter du projet (et la règle de refus)

Lis `.claude/loop-autonomy.json` à la racine du projet. S'il n'existe pas,
construis-le : détecte la commande de vérification (script `validate` du
package.json, sinon compose `test` + `lint` + `typecheck`, sinon l'équivalent
de l'écosystème — `cargo test`, `pytest`, `make test`…), détecte la source
d'items, propose le fichier, écris-le.

Exemple JSON, spec complète et variantes : lis `references/adapter.md`.

**Règle de refus — la plus importante du skill.** Si le projet n'a AUCUNE
commande de vérification déterministe (rien qui sorte 0/1 et qui prouve que le
travail est bon), **n'arme pas la boucle**. Explique pourquoi : sans gate
mesurable, « autonome » signifie « personne ne vérifie », et la boucle ne
ferait qu'empiler du travail non prouvé plus vite qu'un humain ne peut le
relire. Propose le chemin de remédiation (ajouter un script `validate`, même
minimal : tests + lint) et arrête-toi là. C'est un service rendu, pas un échec.

## Étape 1 — La file d'items

Format générique : un fichier JSON manipulé par `scripts/loop-queue.mjs`
(sous-commandes `init`, `next`, `mark`, `report` — lance-le sans argument pour
l'usage). Statuts : `PENDING → DONE | SKIP | FAILED | QUARANTINED |
DECISION_PENDING | PLAN_REQUIRED`. Deux échecs sur le même item →
`QUARANTINED` (on n'use pas le budget sur un item pathologique).

Si la file vient d'ailleurs (backlog HTML, plan, issues), l'adapter déclare
`queue.type: "custom"` avec ses commandes — le cycle de vie reste identique.

Au premier setup, remplis la file AVEC l'utilisateur : chaque item doit être
une unité fermée (réalisable en un commit, vérifiable par `validate`), avec un
`id` stable et un titre actionnable. Un item flou est un futur SKIP.

## Étape 2 — Préparer le terrain

1. **Branche dédiée obligatoire** : `git checkout -b loop/<date>` (ou le
   `branchPrefix` de l'adapter). Jamais la boucle sur la branche principale ni
   sur une branche de travail humain — le rollback par item utilise
   `git reset --hard`, ce qui n'est sûr que sur une branche sacrifiable.
2. **Arbre propre exigé** au départ ; sinon stoppe et fais trier l'utilisateur.
3. **Vérifie que `validate` passe AVANT le premier item.** Une boucle lancée
   sur un projet déjà rouge attribuera l'échec au mauvais item.

## Étape 3 — Choisir le mode

Demande à l'utilisateur (une seule question) : « tu restes dans le coin, ou
c'est pour tourner sans toi ? », puis lis la section correspondante de
`references/modes.md` :

| Mode | Quand | Mécanisme |
|---|---|---|
| **A — Session + /goal** | L'utilisateur est présent mais occupé | Tu boucles toi-même ; il colle la ligne `/goal` que tu lui imprimes (évaluateur indépendant qui empêche l'arrêt prématuré) |
| **B — Session + /loop rythmé** | Présent, mais il faut étaler la consommation (limites d'usage 5 h) | Un item par tick `/loop` ; même discipline |
| **C — Tâches planifiées Desktop** | Nuit / absence | Une session FRAÎCHE par tick traite UN item puis s'arrête ; la session N+1 commence par vérifier l'item de la session N |

Le mode C exige la **confirmation explicite** de l'utilisateur avant de créer
la moindre tâche planifiée, et un lock file contre les chevauchements.

## La discipline par item (tous modes)

Pour CHAQUE item, dans cet ordre :

1. **Base** : `git rev-parse HEAD` → `BASE_SHA`. Arbre propre, sinon stop.
2. **Lecture + gate de re-triage** AVANT tout code. Reclasse et passe au
   suivant si : l'item exige d'inventer une valeur/un comportement que rien ne
   spécifie → `DECISION_PENDING` (route vers le canal de décision, ne devine
   JAMAIS) ; l'item dépasse un commit propre ou touche une source de vérité →
   `PLAN_REQUIRED` (route vers le workflow de plan du projet) ; l'item dépend
   d'un système externe inaccessible → `SKIP` motivé.
3. **Implémentation par subagent frais** : dispatch un subagent (l'implémenteur
   du projet s'il existe — adapter — sinon `general-purpose`) avec le contexte
   minimal : l'item, les fichiers cibles, la commande de vérification rapide.
   TDD si le projet a des tests. Le subagent N'A PAS le droit de commit.
   *Repli autorisé* : si aucun outil de dispatch de subagent n'est disponible
   dans ton environnement (run mono-item, session restreinte), applique la
   discipline toi-même et note l'écart dans le rapport — ne bloque pas dessus.
4. **Vérification par TOI, pas par lui** : lance `validate` toi-même, en
   FOREGROUND (jamais en arrière-plan : un validate background horodate un
   succès avant d'avoir fini — c'est l'auto-vérification déguisée). Le résumé
   du subagent n'est pas une preuve ; seule la commande l'est.
5. **Échec** : un correctif ciblé, puis re-validate. Deux échecs →
   `git reset --hard BASE_SHA && git clean -fd`, marque `FAILED` (ou `SKIP` si
   la cause est claire), passe au suivant. Ne t'acharne pas : le budget de la
   boucle appartient aux items suivants.
6. **Un commit par item**, chemins explicites (jamais `git add -A` / `.`),
   message conventionnel citant l'id de l'item. Marque `DONE` dans la file
   avec le sha — la liste des commits du rapport EST la revert map humaine.
7. **Caps** : items traités ≥ `maxItemsPerRun` ou temps écoulé ≥ `maxMinutes`
   → clôture propre du run (rapport), même si la file n'est pas vide.

**Découvertes hors scope** : jamais de fix opportuniste. Ajoute un nouvel item
`PENDING` à la file (avec contexte) et reste sur l'item courant.

## Décisions et rapport

- Les `DECISION_PENDING` partent vers `decisionChannel` : `ask-user` = tu
  poses les questions EN LOT à la fin du run (pas une par une en plein vol) ;
  `command` = tu invoques la commande de l'adapter (ex. un decision hub).
- Fin de run : écris un rapport (`loop-report-<date>.md` à côté de la queue) —
  DONE avec les shas, SKIP/FAILED avec raisons, DECISION_PENDING avec les
  questions, file restante. Termine ta réponse par ce rapport : c'est ce que
  l'utilisateur lit au réveil.

## Interdits permanents

`claude -p` / Agent SDK · `bypassPermissions` · `git add -A` ou `git add .` ·
push, merge, ou toucher à la branche principale · deviner une valeur non
spécifiée · valider en background · plus d'un item par subagent · commit par
un subagent.

## Références

- `references/modes.md` — le détail opérationnel des 3 modes : template
  `/goal` exact, invocation `/loop`, prompt de tâche planifiée, lock file.
- `references/adapter.md` — spec complète de `.claude/loop-autonomy.json` +
  deux exemples (projet générique JSON, projet à backlog custom).
- `scripts/loop-queue.mjs` — le helper de file générique (exécutable tel quel,
  ne le recode pas).
