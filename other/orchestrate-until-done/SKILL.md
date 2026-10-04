---
name: orchestrate-until-done
description: Splits a user request into subtasks, writes .claude/completude.md, launches parallel agents, and refuses to hand back until every checkbox is done or explicitly declined. Use at the start of any multi-part task, long prompt, UCAO work, feature delivery, refactor, frontend or mobile Blade, or when the user says lance, continue, don't be lazy, don't stop halfway, or complains about relaunching. Prevents deleting mobile/desktop variants and skipping web search.
license: MIT
compatibility: Claude Code, OpenCode, Cursor, Codex, any harness that reads AGENTS.md or Agent Skills
metadata:
  author: klassci
  version: "1.0"
  hook: .claude/hooks/completude-check.sh
---

# Orchestrate until done

Ce skill existe parce que l'utilisateur ne doit **jamais** relancer pour un travail que tu pouvais finir. Le coût n'est pas le point oublié : c'est lui qui fait ta revue à ta place.

Il n'y a **pas** de moteur Workflow Claude dans ce harness (seule commande workflow = `plan-and-confirm`). OpenCode n'a pas de Stop hook : le plugin `.opencode/plugins/completude-idle.js` + ce skill + `AGENTS.md` en tiennent lieu.

Charge aussi : skill `fin-de-tache` (gabarit) et, si feature ≥ 3 fichiers, `feature-delivery` + `plan-and-confirm`.

Détails : [completude-contract.md](references/completude-contract.md) · [split-and-agents.md](references/split-and-agents.md) · [preserve-surfaces.md](references/preserve-surfaces.md) · [harness.md](references/harness.md)

## 0. Avant toute chose

Copie cette checklist dans ta réponse interne et coche-la :

```
Orchestre :
- [ ] 1. Relire la demande mot pour mot (verbes à l'impératif = points)
- [ ] 2. Ouvrir .claude/completude.md AU DÉBUT (gabarit fin-de-tache)
- [ ] 3. Internet si le monde extérieur est en jeu (loi, API, harness, produit tiers)
- [ ] 4. Lire l'architecture déjà écrite (dossier UCAO, rules, AGENTS.md) — ne pas réinventer
- [ ] 5. Découper en sous-tâches indépendantes
- [ ] 6. Lancer des agents en parallèle sur ce qui n'écrit pas le même fichier
- [ ] 7. Préserver desktop ET mobile ET print (jamais « simplifier » en supprimant une surface)
- [ ] 8. Vérifier chaque affirmation (fichier:ligne / commande / URL)
- [ ] 9. Ne rendre la main que si toutes les cases sont cochées OU dans « Non fait, et pourquoi »
```

Si tu t'apprêtes à écrire « dis-moi si tu veux que je continue » alors qu'il reste des cases : **tu es en train d'échouer**. Continue.

## 1. Découper le prompt

Relis le message utilisateur. Chaque verbe impératif, chaque « et », chaque liste numérotée est un livrable.

Interdit de paraphraser dans « Demandé, mot pour mot » : la paraphrase est l'endroit où un point disparaît.

Règles de découpe (lire [split-and-agents.md](references/split-and-agents.md) si > 6 points) :

- Un point = un résultat observable (fichier, comportement, preuve).
- Séparer *recherche* / *conception* / *code* / *preuve d'écran* / *déploiement*.
- Si un dossier d'architecture existe déjà (ex. `.opencode/structuration/ucao-uuc-dossier-2026-09/`), les lots de ce dossier **sont** les sous-tâches. Ne pas en inventer une autre liste.

## 2. Agents

Dès que deux sous-tâches n'écrivent pas les mêmes fichiers, lance-les **dans le même tour** via l'outil Task.

| Nature | subagent_type | Écrit du code ? |
|---|---|---|
| Inventaire, grep, parcours | explore | non |
| Lot d'implémentation borné | general | oui, si le lot l'autorise |
| Second angle | critique-transversale (agent fichier) | non |

Consigne obligatoire dans le prompt de l'agent :

- périmètre de fichiers ;
- « n'efface aucune variante mobile/desktop/print » ;
- ce qu'il doit **rapporter** (chemins, SHA, commandes) ;
- ce qu'il ne doit **pas** faire (commit, deploy, hors lot).

Toi, orchestrateur : tu ne dupliques pas le travail d'un agent encore en cours. Tu fusionnes ses preuves dans `completude.md`.

## 3. Architecture déjà définie

Ordre de vérité (du plus fort au plus faible) :

1. Exigences actuelles de l'utilisateur
2. Code et expériences
3. Dossier de conception déjà livré (UCAO = `ucao-uuc-dossier-2026-09/`)
4. Entretiens / artifact
5. Sites publics

Ne reconstruis pas un module que le dossier classe « réutilisable ». Ne code pas un `if (ucao)`. Suis les lots 0→N du backlog, pas l'ordre qui t'arrange.

Code non trivial : `plan-and-confirm` **sauf** si l'utilisateur a déjà dit « lance », « OKAY », « fais-le », « arrête de demander ». Alors tu exécutes le lot suivant du dossier, tu n'attends pas un second OKAY.

## 4. Surfaces UI — interdit de « simplifier »

KLASSCI a souvent **deux** (ou trois) vues pour le même écran : desktop, `_show-mobile`, PDF. Un refactor qui « nettoie » en fusionnant ou en supprimant le mobile est un **bug produit**.

Avant tout `delete_file` / rewrite Blade :

1. Glob `*mobile*`, `*print*`, `pdf*`, `sm:`, `md:` autour du fichier.
2. Si une variante existe, elle **reste**, sauf demande explicite de la retirer.
3. Le diff ne doit pas réduire le nombre de breakpoints couverts.

Détail et exemples : [preserve-surfaces.md](references/preserve-surfaces.md)

## 5. Internet

Si la tâche touche un harness, une loi, un prestataire, un format officiel, une version de framework : **fetch maintenant**. « Je suppose » n'est pas une source. Si le fetch échoue, note l'URL et l'erreur dans « Non fait », puis continue le reste.

## 6. Quand tu as le droit de t'arrêter

Seulement si :

- toutes les cases « À livrer » sont cochées **et** le tableau preuves a assez de lignes (hook : ≥ 3 cochées ⇒ ≥ 1 preuve pour 2 cases) ;
- ou chaque case restante est dans « Non fait, et pourquoi » avec un obstacle **nommé** (décision utilisateur, outil absent, risque refusé) — jamais « pas eu le temps » ;
- ou le hook Stop / plugin idle a déjà rappelé une fois et l'obstacle est réel (`stop_hook_active`).

Tu n'as **pas** le droit de t'arrêter pour : contexte long, « c'est déjà pas mal », « je propose la suite », « veux-tu que je continue ? », fatigue simulée.

## 7. Branchement hooks

- Claude Code : Stop → `.claude/hooks/completude-check.sh` (déjà dans `settings.json`).
- OpenCode : `.opencode/plugins/completude-idle.js` (session.idle + compaction).
- N'importe quel harness : le bloc **Pre-prompt** dans `AGENTS.md` (lu au démarrage).

Si tu travailles hors Claude et que le plugin n'a pas tourné : **simule le hook** avant de conclure — relis `completude.md`, compte les `[ ]`.

## 8. Commande

Utilisateur : `/orchestrate` (Claude ou OpenCode) ou « lance-toi » / « continue ». Toi : ce skill, tout de suite, sans demander confirmation du skill.
